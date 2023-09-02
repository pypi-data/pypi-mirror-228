import re
import os
import copy
import types
import inspect
import logging
import functools
from pkg_resources import iter_entry_points
from collections import ChainMap, OrderedDict, Counter

from pyats.easypy import runtime
from pyats.utils.dicts import recursive_update
from pyats import configuration as cfg
from .discovery_helper import Verifications
from pyats.aetest import base, container, processors
from pyats.aetest import CommonSetup, CommonCleanup
from pyats.aetest.parameters import ParameterDict
from pyats.aetest.base import Source, TestableMeta
from pyats.aetest.loop import loopable, get_iterations
from pyats.aetest.sections import SetupSection, CleanupSection
from pyats.aetest.discovery import ScriptDiscovery, TestcaseDiscovery,\
                                 CommonDiscovery
from pyats.log import managed_handlers

from genie.libs.sdk.triggers.template.devicenotfound import TriggerDeviceNotFound

# To simplify trigger writting
from genie.libs import ops, conf, sdk, parser
from genie.abstract import Lookup

from genie.utils import Dq
from .utils import load_class, load_method, load_attribute
from ..ops.base.base import Base as BaseOps
from .commons import ProfileSystem
from .base import TestcaseVerification, TestcaseVerificationOps, Trigger,\
                  TestcaseVerificationCallable
from .script import TestScript
from .standalone import GenieStandalones

log = logging.getLogger(__name__)

# Entrypoint group to extend genie libraries (e.g. in genielibs.cisco)
TRIGGER_ENTRY_POINT = 'genie.libs.sdk.triggers'
# Pyats config path to specify which local/external pkg to look in for triggers
PYATS_EXT_TRIGGER_CFG_PATH = 'pyats.libs.external.trigger'
# Env variable to specify which local/external pkg to look in for triggers
PYATS_EXT_TRIGGER_ENV_NAME = 'PYATS_LIBS_EXTERNAL_TRIGGER'

class GenieScriptDiscover(ScriptDiscovery):
    '''Genie script discoverer'''

    def __init__(self, *args, **kwargs):
        # Used for tracking duplicate UIDs and assigning a counter
        self.uid_counter = {}

        super().__init__(*args, **kwargs)

    def __iter__(self):
        for section in self.discover():
            # Make sure they are all of the right type
            if not isinstance(section, container.TestContainer):
                raise TypeError('Expected sections inheriting from '
                                'aetest.TestContainer class but got: %s'
                                % section)
            if loopable(section):
                # Get a clean initial version of the parameters and result
                parameters = section.parameters.copy()
                results = section.result.clone()
                # section is marked to be looped
                # offer up each iteration in its own class instance
                for iteration in get_iterations(section):
                    # Set uid, parameters, parent, and result
                    # TODO: Incorporate this into pyATS properly
                    section.uid = iteration.uid
                    section.parameters = parameters.copy()
                    section.parameters.update(iteration.parameters)
                    section.parent = self.target
                    section.result = results
                    yield section
            else:
                yield section

    def discover(self):
        '''Discover class to find common_.* and trigger/verifications'''
        CommonSetup_obj = CommonSetup(parent=self.target)
        CommonSetup_obj.__doc__ = 'Genie Common Setup'

        if hasattr(self.target, 'subsection_data'):
            # Retrieve the pre, post and exception corresponding to the
            # Commonsetup section.
            pre, post, exception = _load_processors(
                self.target.subsection_data['setup'], self.target)

            # Append the corresponding processors
            # Attach susbsection datafiles parameters to the CommonSetup_obj
            if 'telemetry_plugins' in self.target.subsection_data['setup']:
                CommonSetup_obj.parameters.update(
                    {'telemetry_plugins':self.target.subsection_data['setup']\
                    ['telemetry_plugins']})

            processors.add(CommonSetup_obj, pre=pre, post=post,
                exception=exception)

        # Yield the common setup
        yield CommonSetup_obj

        # gets lists of trigger and verification uids to load from the following script arguments:
        # 'trigger_uids', 'trigger_groups', 'verification_uids', 'verification_groups'
        triggers, verifications = self._get_triggers_and_verifications_to_load()

        # learn order to load triggers and verifications
        trigger_order, verification_order = self._get_trigger_verification_order()

        try:
            # Actually load trigger objects from datafile
            triggers = self._parse_datafiles(
                self.target.triggers, order=trigger_order, to_load=triggers)
        except ValueError as e:
            # One or more triggers failed to load from the trigger datafile.
            # Run the common cleanup then re-raise the current exception to exit.
            log.error(str(e) + " Going directly to common cleanup.")
            yield self._get_common_cleanup()
            raise

        # If randomize, randomize them
        if self.target.random:
            triggers = sorted(
                triggers, key = lambda x: self.target.random.random())

        if hasattr(self.target, 'parallel_verifications'):
            parallel_verifications = self.target.parallel_verifications
        else:
            parallel_verifications = False

        if verifications:
            # runtime is a singleton.
            # Synchro is a multiprocessing Manager object
            # to allow interprocess data retention attached to the runtime object.
            if parallel_verifications:
                log.info("Running parallel verifications...")
                managed_handlers.tasklog.enableForked(consolidate=True)
                runtime.verf = runtime.synchro.dict()
                
                # instantiate synchro dicts to all devices in advance to avoid race condition
                for device in self.target.parameters['testbed'].devices:
                    runtime.verf[device] = runtime.synchro.dict()

            verify_container = Verifications(
                parent=self.target,
                parallel_verifications=parallel_verifications)
            _verf_uid = verify_container.uid

        for trigger in triggers:
            # Get all the Verifications
            verfs = self._parse_datafiles(
                self.target.verifications,
                verification=True,
                order=verification_order,
                to_load=verifications)

            if verfs:
                # instantiating new container for trigger verifications
                verify_container = Verifications(
                    parent=self.target,
                    parallel_verifications=parallel_verifications)
                verify_container.uid = _verf_uid + "." + trigger.uid

                for verf in verfs:
                    try:
                        if 'skip_global_verifications' in trigger.parameters and\
                        verf.uid.split('.', 1)[0] in\
                            trigger.parameters['skip_global_verifications']:
                            # Skipping global verification as requested
                            continue
                    except UnboundLocalError:
                        # No trigger was executed, so no skip global verification
                        pass
                    verify_container.verifiers.append(verf)

                yield verify_container
            yield trigger

        # the end of all triggers,  run again 1 last time all the verifications
        verfs = self._parse_datafiles(
            self.target.verifications,
            verification=True,
            order=verification_order,
            to_load=verifications)

        if verfs:
            # instantiating new container for post trigger verifications
            verify_container = Verifications(
                parent=self.target,
                parallel_verifications=parallel_verifications)
            verify_container.uid = "Verifications.post"

            for verf in verfs:
                # This is the last one, but still if last trigger asked to skip
                # Then skip the global verification
                try:
                    if 'skip_global_verifications' in trigger.parameters and\
                    verf.uid.split('.', 1)[0] in\
                        trigger.parameters['skip_global_verifications']:
                        # Skipping global verification as requested
                        continue
                except UnboundLocalError:
                    # No trigger was executed, so no skip global verification
                    pass
                verify_container.verifiers.append(verf)

            yield verify_container

        # Yield the common cleanup
        yield self._get_common_cleanup()

    def _get_common_cleanup(self):
        """ Builds the common cleanup object

            returns:
                CommonCleanup: common cleanup object
        """
        CommonClean_obj = CommonCleanup(parent=self.target)
        CommonClean_obj.__doc__ = 'Genie Common Cleanup'

        if hasattr(self.target, 'subsection_data'):
            # Retrieve the pre,post and exception corresponding to the
            # Commoncleanup section.
            pre, post, exception = _load_processors(
                self.target.subsection_data['cleanup'], self.target)

            # Attach susbsection datafiles parameters to the CommonClean_obj
            if 'telemetry_plugins' in self.target.subsection_data['cleanup']:
                CommonClean_obj.parameters.update(
                    {'telemetry_plugins':self.target.subsection_data['cleanup']\
                    ['telemetry_plugins']})

            processors.add(CommonClean_obj, pre=pre, post=post,
                exception=exception)

        return CommonClean_obj

    def _get_trigger_verification_order(self):
        """ Return the triggers and verifications in order specified by:

        self.target.trigger_uids or self.target.verification_uids if these are of list type
        self.target.triggers.order or self.target.verifications.order if they exist

        Returns:
            (dict, dict) Tuple with dictionary with triggers and verifications ordered with above logic.

            ({"triggers": {"<name>": dict()}}, {"verifications": {"<name>": dict()})

        """
        ret = {}
        for item in ['trigger', 'verification']:
            uids = getattr(self.target, '{}_uids'.format(item))

            if isinstance(uids, list):
                order = uids
            else:
                datafile = getattr(self.target, '{}s'.format(item))
                # Get the order if specified by the user using the 'order' key in the datafile.
                # The order is a list of strings OR a list of dictionaries
                try:
                    order = datafile.get('order', [])
                except Exception:
                    order = []

            # Create a list of ordered items, this creates a list of dictionaries
            ordered_items = []
            for name in order:
                if isinstance(name, dict):
                    ordered_items.append(name)
                else:
                    # remove anything in the name after first dot... no idea why
                    name1 = re.sub(r'\.[\w]+', '', name)
                    ordered_items.append({name1:{}})

            ret[item] = ordered_items

        return ret['trigger'], ret['verification']

    def _get_triggers_and_verifications_to_load(self):
        """ gets triggers and verifications using the requirements from:
                - self.target.trigger_uids and/or self.target.trigger_groups
                - self.target.verification_uids and/or self.target.verification_groups

            returns:
                tuple: triggers_to_load, verifications_to_load

        """
        ret = {}
        uids_items = {}
        groups_items = {}
        for item in ['trigger', 'verification']:
            ret[item] = []
            uids_items[item] = []
            groups_items[item] = []

            uids = getattr(self.target, '{}_uids'.format(item))
            groups = getattr(self.target, '{}_groups'.format(item))

            # nothing to run for 'item'
            if not uids and not groups:
                continue

            if uids:
                if isinstance(uids, list):
                    uids_items[item] = uids
                else:
                    # pyATS datastructure logic (And() Or() etc...)
                    _type = '{trigger_verification}_{uids_groups}'\
                        .format(trigger_verification=item,
                                uids_groups='uids')

                    uids_items[item] = self._get_triggers_verifications_via_callable(
                        _type=_type, _callable=uids)
            if groups:
                if isinstance(groups, list):
                    groups_items[item] = groups
                else:
                    # pyATS datastructure logic (And() Or() etc...)
                    _type = '{trigger_verification}_{uids_groups}'\
                        .format(trigger_verification=item,
                                uids_groups='groups')

                    groups_items[item] = self._get_triggers_verifications_via_callable(
                        _type=_type, _callable=groups)

            log.debug('{item}_uids: {items}'.format(item=item, items=uids_items[item]))
            log.debug('{item}_groups: {items}'.format(item=item, items=groups_items[item]))
            if uids_items[item] and groups_items[item]:
                ret[item] = list(set(uids_items[item]) & set(groups_items[item]))
            elif uids_items[item]:
                ret[item] = uids_items[item]
            elif groups_items[item]:
                ret[item] = groups_items[item]
            log.debug('elected {item}s: {items}'.format(item=item, items=ret[item]))

        return ret['trigger'], ret['verification']

    def _get_triggers_verifications_via_callable(self, _type=None, _callable=None):
        """ gets triggers or verifications from pyATS datastructure callable

            args:
                _type (str): Where the callable came from. One of:
                    'trigger_uids', 'trigger_groups', 'verification_uids', or 'verification_groups'
                _callable (callable): pyATS datastructure callable like:
                    'And()', 'Or()', etc.

            returns:
                list: Trigger or verification uids
        """
        items = []

        attribute = 'triggers' if 'trigger' in _type else 'verifications'
        attribute_items = getattr(self.target, attribute)

        if not attribute_items:
            return items

        for item in attribute_items:

            # Skip this item if it is not a dict. For example, the 'order' item is a list
            if not isinstance(attribute_items[item], dict):
                continue

            if 'uids' in _type:
                value = item
            elif 'groups' in _type:
                value = attribute_items[item].get('groups')

            # Skip this item if it is a special schema keyword
            special_items = ['variables', 'parameters', 'global_processors']
            if attribute == 'triggers':
                special_items.append('data')

            if value and _callable(value) and value not in special_items:
                items.append(item)

        return items

    def _parse_datafiles(self, data_values, verification=False, order=None, to_load=None):
        '''From the information of the datafiles, get the testcases ready

        Args:
            datavalues (OrderedDict): Ordered dictionary with trigger
                                      or verification data
            verification (bool): Boolean indicating the data passed
                                 are verifications instead of triggers.
            order (list of dict): List of dictionaries with order of triggers
                                  to load, optionally with datavalue overrides.
            to_load (list): list of triggers or verifications names to load

        Returns:
            (list of classes): List of Trigger or Verification classes

        '''
        # Return list of trigger and verifications
        ret = []

        # If no data was provided, then just get out
        if not data_values:

            return ret

        # Create a list of names from the order specified by the user.
        # User can specify a list of strings OR a list of dictionaries
        # as value for the order key in the datafile.
        # This list is used to check if there are items not in the named list
        order_names = [list(name.keys())[0] if isinstance(name, dict) else name for name in order]

        if to_load:
            # check all items in 'to_load' exist in the datafile
            if not set(to_load).issubset(list(data_values.keys())):
                raise ValueError(
                    "The following items specified through either the "
                    "'{type}_uids' or the '{type}_groups' do not exist "
                    "in the datafile: '{items}'."
                    .format(type='verification' if verification else 'trigger',
                        items=list(set(to_load)-set(list(data_values.keys())))
                    )
                )

            # add any remaining items to load that are not in the 'order' field
            for item in to_load:
                if item not in order_names:
                    order.append(item)

        # load elements in order
        for item in order:
            # If the order item is a dictionary,
            # set name to the first dictionary key.
            # The order dictionary only supports a singly entry.
            if isinstance(item, dict):
                name = list(item.keys())[0]
                item_values = {name: item.get(name) or {}}
            else:
                name = item
                item_values = {}

            if name not in to_load:
                continue

            # self.uid_counter is used for tracking duplicates
            if name not in self.uid_counter:
                if order_names.count(name) > 1 or verification:
                    self.uid_counter.update({name: 1})
                else:
                    self.uid_counter.update({name: None})
            else:
                self.uid_counter[name] += 1

            # load and add to return object
            try:
                # Create copy of default data values
                # and apply overrides specified as part
                # of the order section.
                item_data_values = recursive_update({}, data_values)
                item_data_values = recursive_update(item_data_values, item_values)
                loaded = self._load_item(
                    name,
                    item_data_values,
                    verification=verification,
                    counter=self.uid_counter[name])

                ret.extend(loaded)
            except Exception as e:
                raise Exception("Issue while loading {n}".format(n=name)) from e

        return ret

    def _clean_data(self, data):
        ret = {}
        for d, values in data.items():
            try:
                values['source']
            except Exception:
                ret[d] = values
        return ret

    def _load_item(self, item, data_values, verification, counter=0):

        # If not a dict, then just get out
        testcase = data_values[item]
        if not isinstance(testcase, dict):
            raise NotImplementedError

        # Get clean data. This mean not information about triggers or
        # verifications
        clean_data = self._clean_data(data_values)

        # Get the testbed, as will be needed to abstract the right library
        tb = self.target.parameters['testbed']

        libs = []

        # Get the devices specified in the trigger
        try:
            items = testcase['devices']
        except KeyError:
            # find devices in testcase and use one of them for discovery
            # when coming to here, most possibly Blitz or pyATS Health Check
            devices = Dq(testcase).get_values('device')
            found_device = []
            for device in devices:
                # avoid %VARIABLES since it's dynamic in testcase
                if '%VARIABLES' not in device:
                    found_device.append(device)
            if found_device:
                items = [found_device[0]]
            else:
                # need to set something to create empty trigger later
                # in case even `device` is not found
                # so pickup one of device from testbed object
                try:
                    items = [tb.find_devices()[0].name]
                except IndexError:
                    # a case no device in testbed object
                    items = ['uut']

        # This could be for many devices, so loop over it
        for dev in items:

            # Check if any devices attributes exists
            info = testcase.get('devices_attributes', {}).get(dev, {})
            # Make sure info is not None
            if info == 'None':
                info = {}

            # Create a chainmap of where the information can be taken from.
            # Location of the datafiles
            d = ChainMap(info, testcase, clean_data)

            # dev can be either one of its alias or device name
            # This will return the device object
            try:
                device = tb.devices[dev]
            except KeyError:
                # Create empty trigger
                trigger = TriggerDeviceNotFound(
                    parent=self.target,
                    uid='{name}.{dev}'.format(name=item, dev=dev)
                )

                # If groups exist, add them so the trigger will be ran and reported
                if 'groups' in testcase:
                    setattr(trigger, 'groups', testcase['groups'])

                libs.append(trigger)
                continue

            # Check for matching external trigger(s) and update trigger 'source'
            # dict values if a match is found
            if not verification and 'source' in d:
                external_source = self._get_external_triggers(
                    device=device,
                    source=d['source']
                )
                if external_source:
                    d['source'].update(external_source)

            # Load the class and do the abstraction
            if 'sub_order' in d or 'sub_triggers' in d or 'sub_verifications' in d:
                # Ooo its a GenieStandalones
                lib = GenieStandalones
            else:
                lib = load_class(d, device)

            # Adjust name  <name>.<device>.<counter>.<count>
            # Where counter and count is optional
            # if alias use device.alias
            if device.aliases:
                name = device.aliases[0]
            else:
                name = device.name
            name = '{i}.{dev}'.format(i=item, dev=name)
            if counter is not None:
                # If run many times, add a counter
                name = '{n}.{c}'.format(n=name, c=counter)

            # If verification here
            if verification:
                # For verification; need to create a new class which
                # inherits from testcase. Depending of the type of verification
                if isinstance(lib, types.FunctionType):
                    parents = (TestcaseVerificationCallable,)
                elif issubclass(lib, BaseOps):
                    parents = (TestcaseVerificationOps,)
                else:
                    raise TypeError("'{l}' is of wrong type for "
                                    "Verifications".format(l=lib))

                # Create the class
                lib, lib.child = type(name, parents, {}), lib
                # So the testcase will point to the actual class
                # But the subsection will point to the parents
                lib.source = Source(lib.child, objcls=lib.child.__class__)
            else:
                # Trigger then
                # Verify it inherits from Testcase
                if not isinstance(lib, TestableMeta):
                    raise TypeError("'{l}' is of wrong type for "
                                    "Trigger".format(l=lib))


            count = d['count'] if 'count' in d else 1

            # Load pre/post/exception processors
            pre, post, exception = _load_processors(testcase, device,
                                                    data_values, self.target)

            # Default value
            temp_name = name
            for rep in range(count):
                if count > 1:
                    # Then add count to the name
                    temp_name = '{n}.{rep}'.format(n=name, rep=rep+1)

                # Instantiate it
                kwargs = {}
                if issubclass(GenieStandalones, lib):
                    kwargs = {'order':d.get('sub_order', []),
                              'verifications':d.get('sub_verifications', []),
                              'triggers':d.get('sub_triggers', []),
                              'cls':None}
                lib_ins = lib(parent=self.target, uid=temp_name, **kwargs)

                # add raw data for later use (e.g. hashing)
                lib_ins.testdata = testcase

                # only set tims_uid if provided by the user in the datafile
                if testcase.get('tims_uid'):
                    tims_uid = testcase.get('tims_uid')
                    lib_ins.tims_uid = tims_uid

                    # override the testcase UID if user provided CLI argument
                    if runtime.args.tims_override_uid:
                        # store the original UID as name if user did not override the name
                        if not lib_ins.name:
                            lib_ins.name = f'{temp_name} ({tims_uid})'
                        lib_ins.uid = tims_uid
                    else:
                        # Append the tims UID to the testcase name
                        if lib_ins.name:
                            lib_ins.name = lib_ins.name + f' ({tims_uid})'
                        else:
                            lib_ins.name = f'{lib_ins.uid} ({tims_uid})'

                # need a new copy of verify
                try:
                    verify = copy_func(lib_ins.verify)
                    # Bind it
                    verify.__get__(lib_ins)
                    lib_ins.verify.parameters = ParameterDict()
                except AttributeError:
                    # Possible if callable, it has no .verify
                    pass
                # Update uut to be the wanted device
                lib_ins.parameters['uut'] = device
                # Pass an abstraction object to simplify writting trigger
                lib_ins.parameters['abstract'] = Lookup.from_device(device,
                                                                    packages={'sdk':sdk,
                                                                              'conf':conf,
                                                                              'ops':ops,
                                                                              'parser':parser})
                # Load Processors
                processors.add(lib_ins, pre=pre, post=post, exception=exception)

                if verification:
                    # Pass parser_kwargs object
                    lib_ins.parameters['parser_kwargs'] = testcase.get(
                                                                'parameters',{})

                # Remember tha chainmap ? Well take everything from it
                # and add it to this object via parameters.
                # Except if ignored,  or setter then it is set to the object
                ignore = set(['source', 'devices', 'devices_attributes',
                              'count', 'parameters', 'processors'])
                setter = ['groups', 'description']
                for k, value in d.items():
                    # Ignore a few keys
                    if k in ignore:
                        continue
                    if k in setter:
                        setattr(lib_ins, k, value)
                    else:
                        lib_ins.parameters[k] = value
                libs.append(lib_ins)

        return libs

    def _get_external_triggers(self, device, source) -> dict:
        """Returns a trigger from genie.libs.cisco or a local/external package if
        module and trigger name match

        Args:
            device (obj): The device to use for abstraction token lookup
            source (dict): a trigger's source subdict from the trigger datafile

        Returns:
            dict: contains keys 'pkg' and 'class' for the found external trigger

        Raises:
            ValueError: if device is not defined
        """

        if not isinstance(source, dict):
            # Incorrect format for trigger passed in, don't override
            return

        # Get full class name/module location
        if "pkg" in source:
            name = f"{source['pkg']}.{source['class']}"
        else:
            name = f"{source['class']}"

        if not name.startswith(TRIGGER_ENTRY_POINT):
            # Custom user trigger, so don't override with local/entrypoint triggers
            return

        relative_class_name = name.replace(f"{TRIGGER_ENTRY_POINT}.", '')
        pkgs = []

        # Check for external/local package
        ext_trigger_package = cfg.get(PYATS_EXT_TRIGGER_CFG_PATH, None) or \
                              os.environ.get(PYATS_EXT_TRIGGER_ENV_NAME)
        if ext_trigger_package:
            pkgs.append(ext_trigger_package)

        # Check for entrypoints
        for entry in iter_entry_points(group=TRIGGER_ENTRY_POINT):
            pkgs.append(entry.module_name)

        # Loop through the pkgs that the class might be in
        for pkg in pkgs:
            try:
                new_class = load_attribute(pkg, relative_class_name,
                                        device, suppress_warnings=True)
            except ValueError:
                # ValueError occurs if device is not defined
                continue

            if new_class.__name__ == relative_class_name.split(".")[-1]:
                log.debug(
                    f"Default {TRIGGER_ENTRY_POINT} class for "
                    f"'{relative_class_name}' superseded. Using class from "
                    f"'{pkg}' instead")
                return {'pkg': pkg, 'class': relative_class_name}


class GenieTestcasesDiscover(TestcaseDiscovery):

    def discover(self):
        '''Discover the section to executes and local verification'''
        # Discover normal section under this testcase
        sections = super().discover()
        for section in sections:

            # Clear any existing processors incase this trigger
            # is ran more than once
            if hasattr(section, '__processors__'):
                section.__processors__.clear()

            if 'sections' in self.target.parameters:
                for section_name in self.target.parameters['sections']:
                    if section.__name__ == section_name:
                        # Grab section parameters. If they exist create a frozen function with them
                        # and replace the section with it
                        sec_parameters = self.target.parameters['sections'][section_name].get('parameters')
                        if sec_parameters:
                            if not hasattr(section, 'parameters'):
                                if inspect.ismethod(section):
                                    section = section.__func__
                                setattr(section, 'parameters', dict())
                            section.parameters.update(sec_parameters)

                        # Load processors
                        pre, post, exception = _load_processors(
                            self.target.parameters['sections'][section_name],
                            self.target.parameters['uut'])

                        processors.add(section,
                                       pre=pre,
                                       post=post,
                                       exception=exception)

        if not isinstance(self.target, Trigger):
            # Then just move on to the next step
            return sections

        setup = None
        cleanup = None
        # Discover local verifications for specific testcase.
        pre_local = []
        post_local = []

        # Verify if it has local verification(s) to execute
        try:
            local_verifications = self.target.__parameters__['verifications']
        except KeyError:
            # No local verification; so move to next step
            return sections

        # It could take two form
        if not local_verifications or local_verifications == 'None':
            return sections

        # Get clean data. This mean not information about verifications
        clean_data = self._clean_data(self.target.parent.verifications)

        # Extract setup/cleanup section from sections list
        if sections:
            setup_section, cleanup_section = sections[0], sections[-1]
            if issubclass(setup_section.__testcls__, SetupSection):
                sections = sections[1:]
                setup = setup_section
            if issubclass(cleanup_section.__testcls__, CleanupSection):
                sections = sections[:-1]
                cleanup = cleanup_section

        # Local verification can be executed on many devices, so take care of
        # that
        for lver, vinfo in sorted(local_verifications.items()):

            # Check in the main verification file to make sure it exists
            try:
                item = self.target.parent.verifications[lver]
            except AttributeError as e:
                # By default its an empty dict,  so it should never get here
                raise AttributeError('Local verification require a verification'
                                     'datafile, which was not provided.') from e
            except KeyError as e:
                raise KeyError('Local verification {value} does not exists '
                               'in the given verification '
                               'datafile'.format(value=lver)) from e

            # Good now need to loop over each device
            # Verify it has devices
            if 'devices' not in vinfo:
                # Then we don't run this local verification. Same rule as all
                # the others
                continue

            # Parent Information for that verification
            parent_info = self.target.parent.verifications[lver]
            # Merge parser_kwargs information for verification
            parser_kwargs = parent_info.get('parser_kwargs', {}).copy()
            parser_kwargs.update(vinfo.get('parameters', {}))
            local_verify_data = dict(parser_kwargs=parser_kwargs)

            # Loop over all devices defined in the local verification block
            for dev in vinfo['devices']:

                # Find the device
                # This will return the device object
                device = self.target.parameters['testbed'].devices[dev]

                # Load the Verification class which was defined by Verification
                # yaml file
                lib = load_class(item, device)

                # Create chainmap for where to find the value for this
                # source verification
                cm = []

                # Information for this local verification
                info = vinfo.get('devices_attributes', {}).get(dev, {})

                if info:
                    cm.append(info)

                # Information for Verification for that device if exists
                try:
                    verf = self.target.parent.verifications[lver].\
                            get('devices_attributes', {}).get(dev, {})
                    if verf:
                        cm.append(verf)
                except:
                    # No device for it, which doesn't make much sense, but move on
                    pass

                # Information for that verification
                cm.append(parent_info)
                cm.append(clean_data)
                cm.append(local_verify_data)

                d = ChainMap(*cm)

                count = d['count'] if 'count' in d else 1

                # Need to create a new class which inherits from testcase.
                # Depending of the type of verification
                if isinstance(lib, types.FunctionType):
                    parents = (TestcaseVerificationCallable,)
                elif issubclass(lib, BaseOps):
                    parents = (TestcaseVerificationOps,)
                else:
                    raise TypeError("'{l}' is of wrong type for "
                                    "Verifications".format(l=lib))
                # if alias use device.alias
                if device.aliases:
                    name = device.aliases[0]
                else:
                    name = device.name
                name = '{i}.{dev}'.format(i=lver, dev=name)

                # So for pre, set it up here
                pre_lib, pre_lib.child = type(name, parents, {}), lib
                pre_lib.verify.source = Source(pre_lib.child,
                                               objcls=pre_lib.child.__class__)
                pre_lib.verify = copy_func(pre_lib.verify)
                pre_lib.verify.parameters = ParameterDict()

                # Change uid
                pre_lib.verify.uid = 'pre_' + name
                pre_lib = pre_lib(parent=self.target, uid='pre_' + name)
                pre_lib.verify.parameters['uut'] = device
                pre_local.append(pre_lib.verify)

                # If no count
                temp_name = name

                # The count does not make sense for local verification pre_
                # but it make sense for post_
                for rep in range(count):
                    if count > 1:
                        temp_name = '{n}.{rep}'.format(n=name, rep=rep+1)

                    # Create the class
                    post_lib, post_lib.child = type(name, parents, {}), lib

                    # So the testcase will point to the actual class
                    # But the subsection will point to the parents
                    post_lib.verify.source = Source(post_lib.child,
                                                objcls=post_lib.child.__class__)
                    post_lib.verify = copy_func(post_lib.verify)
                    post_lib.verify.parameters = ParameterDict()

                    ignore = ['source', 'devices', 'devices_attributes']
                    for k, value in d.items():
                        # Ignore a few keys
                        if k in ignore:
                            continue
                        if k == 'parameters':
                            # pyATS already have parameters, so we prefix it
                            # with genie_parameters to make it different
                            k = 'genie_' + k
                        pre_lib.verify.parameters[k] = value
                        post_lib.verify.parameters[k] = value

                    # Create a new instance of function
                    # Diff class instance, still have exactly the same
                    # function obj. So need to create a new copy
                    post_lib.verify.uid = 'post_' + temp_name

                    post_lib = post_lib(parent=self.target,
                                        uid='post_' + temp_name)
                    post_lib.verify.parameters['uut'] = device

                    post_local.append(post_lib.verify)

        return self._order(sections, pre_local, post_local, setup, cleanup)

    def _order(self, sections, pre_local, post_local, setup=None, cleanup=None):
        '''Set order of execution'''

        # build the section list with local verification
        # --------------------------
        ordered = pre_local + sections + post_local

        # Setup runs first (stick to front of list)
        if setup is not None:
            ordered.insert(0, setup)

        # Cleanup runs last
        if cleanup is not None:
            ordered.append(cleanup)

        # return the ordered list
        return ordered

    def _clean_data(self, data):
        ret = {}
        for d, values in data.items():
            try:
                values['source']
            except Exception:
                ret[d] = values
        return ret

class GenieCommonDiscovery(CommonDiscovery):

    def _discover_profile(self, features, location):
        # Create a subsection for it
        container = {}

        pts_sections = []
        for feature in features:

            # Is it a show command or a feature?
            # All features should be a single word and not start with show
            # Hope that rule is strong enough...
            if not feature.startswith('show') and len(feature.split()) == 1:
                # Yep a feature!
                type_ = 'feature'
            else:
                # A show command
                type_ = 'show'

            # Make sure feature exists
            try:
                info = self.target.parent.pts_data[feature]
            except KeyError as e:
                # Error as user need to add to pts_data
                if type_ == 'feature':
                    raise KeyError("'{f}' does not exists in pts_data "
                                   "file".format(f=feature)) from e
                else:
                    # Still good just no exclude
                    self.target.parent.pts_data[feature] = {'devices':['uut']}

            try:
                device = info['devices']
            except KeyError:
                # no device so do not run
                continue

            # And make sure it isnt empty
            if not len(device):
                # no device
                continue

            func = copy_func(ProfileSystem.ProfileSystem)
            func.uid = 'profile_{n}_{l}'.format(n=feature.replace(' ', '_'),
                                                l=location)
            func.parameters = {'feature':feature, 'container':container}
            func.source = Source(ProfileSystem.ProfileSystem,
                                 objcls=func.__class__)
            # Bind it and append to the section list
            pts_sections.append(func.__get__(self.target, func.__testcls__))
        return pts_sections

class GenieCommonSetupDiscover(GenieCommonDiscovery):

    def __iter__(self):
        '''Built-in function __iter__

        Generator function, yielding each testable item within this container in
        the order of appearance inside the test cases. This is the main
        mechanism that allows looping through Common Section's child items.

        This function relies on discover's returned list of sub sections in
        their sorted runtime order. It then takes each object class, instantiate
         them and run each. In case an object is looped, the loop iterations are
        processed.
        '''
        for section in self.discover():
            if not hasattr(section, '__testcls__'):
                raise TypeError("Expected a subsection object with "
                                "'__testcls__' set by the section decorator")
            # discovered Subsection
            # ------------------------
            if loopable(section):
                # section is marked to be looped
                # offer up each iteration in its own class instance
                for iteration in get_iterations(section):
                    yield section.__testcls__(section,
                                              uid = iteration.uid,
                                              parameters = iteration.parameters,
                                              parent = self.target)
            else:
                # run section a single time.
                yield section.__testcls__(section, parent = self.target)

    def discover(self):
        # Normal sections
        # Return unbounded method
        sections = super().discover()

        # process common data file
        orderer, new_sections = get_common_subsection(self.target, 'setup')
        sections = sections + new_sections

        # Add the pts
        pts_features = self.target.parent.pts_features
        if isinstance(pts_features, str):
            pts_features = self.target.parent.pts_features.split()

        # Alright for each of those features, we are doing PTS

        # Create a subsection for it
        container = {}
        sections.extend(self._discover_profile(pts_features, 'pre'))

        return order_common_subsection(sections, orderer, 'setup')

class GenieCommonCleanupDiscover(GenieCommonDiscovery):

    def discover(self):
        # Normal sections
        # Return unbounded method
        sections = super().discover()

        # process common data file
        orderer, new_sections = get_common_subsection(self.target, 'cleanup')
        sections = sections + new_sections

        # Add the pts
        pts_features = self.target.parent.pts_features
        if isinstance(pts_features, str):
            pts_features = self.target.parent.pts_features.split()

        # Alright for each of those features, we are doing PTS
        sections.extend(self._discover_profile(pts_features, 'post'))

        return order_common_subsection(sections, orderer, 'cleanup')

def deep_dict_update(global_dic, local_dic):
    '''Update global_dic with local_dic.
       For order, append order defined in global_processors after the local
       ones and remove duplications'''
    for key in local_dic:
        if key == 'order':
            global_dic['order'] = list(OrderedDict.fromkeys(local_dic \
                .get('order', []) + global_dic.get('order', [])).keys())
        elif key in global_dic and isinstance(global_dic[key], dict) \
                               and isinstance(local_dic[key], dict):
            deep_dict_update(global_dic[key], local_dic[key])
        else:
            global_dic[key] = local_dic[key]
    return global_dic

def _load_processors(testcase, device=None, data_values=None, target=None):
    '''load processors from trigger data file'''
    # Get processors from testcase
    _processors = testcase.get('processors', {})

    # Check if any global
    if data_values and 'global_processors' in data_values:
        _processors_global = copy.deepcopy(data_values['global_processors'])
        _processors = deep_dict_update(_processors_global, _processors)

    # Load pre processors
    pre_processors = _load_processor(_processors.get('pre', {}),
                                     device, target)
    # Load post processors
    post_processors = _load_processor(_processors.get('post', {}),
                                      device, target)
    # Load exception processors
    exceptions = _load_processor(_processors.get('exception', {}),
                                 device, target)
    return pre_processors, post_processors, exceptions

def _load_processor(processors_data, device=None, target=None):
    '''load processors'''
    if not isinstance(processors_data, dict):
        raise ValueError("Invalid dictionary; cannot translate '%s' into a "
                         "processor object" % processors_data)
    # Default order
    order = processors_data.get('order', [])
    processors_mapping = {}
    _processors = []

    if not set(order).issubset(list(processors_data.keys())):
        #todo
        raise Exception('processor found in order not found in datafile')

    # add any remaining items to load that are not in the 'order' field
    for item in processors_data.keys():
        if item not in order:
            order.append(item)

    # enhanced genie schema, a dictionary that utilizes abstraction and
    #  supports pre/post/exception processor with parameters
    for name in order:
        processor = processors_data[name]

        if name == 'order':
            order = processor
            continue
        pkg = processor.get('pkg', None)
        method_name = processor.get('method', None)

        # Load the method and do the abstraction
        method = load_method(pkg, method_name, device)

        params = processor.get('parameters', {})
        if params:
            method = functools.partial(method, **params)

        processors_mapping.update({name: [method]})

        if method:
            method.__report__ = True
            _processors.append(method)

    return _processors

def copy_func(f):
    """Based on http://stackoverflow.com/a/6528148/190597 (Glenn Maynard)"""
    g = types.FunctionType(f.__code__, f.__globals__, name=f.__name__,
                           argdefs=f.__defaults__,
                           closure=f.__closure__)
    g = functools.update_wrapper(g, f)
    # This is needed as pyats do a inspect.unwrap and the wrap go back to the
    # function
    del g.__wrapped__
    g.__kwdefaults__ = f.__kwdefaults__
    return g

def order_common_subsection(items, orderer, type_):
    '''Set the order of common subsections and filter them'''
    if not orderer:
        # no order provided, don't sort
        return items

    if orderer == ['None']:
        return []

    ret = []
    # Check for duplicate in the orderer list
    # Via a quick check
    if len(orderer) != len(set(orderer)):
        # There is atleast one duplicate!
        seen = set()
        twice = set(i for i in orderer if i in seen or seen.add(i))
        # Set the correct msg
        raise ValueError("Duplicate value has been found "
                         "in the subsection datafile in the field "
                         "{msg} 'order'" "\r\n{dup}".format(dup=twice,
                                                            msg=type_))
    if not items:
        raise ValueError("{msg} 'order' was specified in "
                         "the datafile, but no subsection "
                         "is available to sort.".format(msg=type_))

    # No duplicate, we need to verify if the name given in
    # order exists in the subsection datafile.
    for name in orderer:
        # Check if it exists in the data_values
        execute = []
        if name.startswith('('):
            # Then assume its a regex!
            try:
                com = re.compile(name)
            except Exception as e:
                raise ValueError("'{name}' is not a valid regex "
                                 "expression".format(name=name))\
                                 from e
            for item in items:
                if com.match(item.uid) and item not in execute and\
                   item not in ret:
                    execute.append(item)
        else:
            execute = [item for item in items if \
                                    getattr(item, 'uid', item.__name__) == name]
        if not execute:
            raise ValueError("{msg} '{name}' was "
                             "specified in the field 'order', "
                             "but does not exists in the "
                             "datafile.".format(name=name, msg=type_))

        ret.extend(execute)

    # Quick fix for PTS - Karim will do permanent fix later.
    for item in items:
        if item not in ret and\
           getattr(item, 'uid', item.__name__).startswith('profile_'):
            if getattr(item, 'uid', item.__name__) != 'profile_traffic':
                ret.append(item)
    return ret

def get_common_subsection(target, type_):
    """ get_common_subsection

        retreive subsection from subsection_datafile
        Also retrieve processors
    """

    orderer = []
    subsections = []

    # process common data file
    if getattr(target.parent, 'subsection_data', None):

        subsection_data = target.parent.subsection_data.get(type_, None)
        if subsection_data:

            # process order config
            orderer = subsection_data.get('order', [])

            # process sections config
            sections = subsection_data.get('sections', None)

            if isinstance(sections, list):
                for subsection in sections:
                    # Load the method and skip the abstraction
                    if isinstance(subsection, str):
                        subsection = load_method(None, subsection)

                    func = copy_func(subsection)
                    func.uid = func.__name__
                    func.source = Source(subsection,
                                         objcls=func.__class__)
                    if func.source.name == 'unknown':
                        func.source.name = target.source.name
                        func.source.location = target.source.location
                    # Bind it and append to the section list
                    subsections.append(func.__get__(target, func.__testcls__))
            elif isinstance(sections, dict):
                for uid, subsection in sections.items():
                    method_name = subsection.get('method', None)

                    # no method, use key instead
                    if method_name is None and uid:
                        method_name = uid

                    # Load the method and skip the abstraction
                    method = load_method(None, method_name)
                    pre, post, exception = _load_processors(
                                                    subsection,
                                                    target=target)
                    processors.add(method, pre=pre, post=post,
                        exception=exception)

                    func = copy_func(method)
                    func.uid = uid
                    func.parameters = subsection.get('parameters', {})
                    func.source = Source(subsection,
                                         objcls=func.__class__)
                    if func.source.name == 'unknown':
                        func.source.name = target.source.name
                        func.source.location = target.source.location
                    # Bind it and append to the section list
                    subsections.append(func.__get__(target, func.__testcls__))
    return orderer, subsections
