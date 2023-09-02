import os
import sys
import logging
import argparse
from functools import partial
from collections import ChainMap

from genie.conf import Genie
from genie.abstract import Lookup
from genie.harness.utils import load_class
from genie.conf.base.testbed import Testbed
from genie.libs import conf, ops, sdk, parser

from ..utils.timeout import Timeout
from .script import TestScript
from .base import TestcaseVerificationOps, Template

from pyats.aetest import Testcase
from pyats.aetest.signals import AEtestInternalSignals

log = logging.getLogger(__name__)

# env var to determine whether CLI is legacy style
LEGACY_CLI = os.environ.get('PYATS_CLI_STYLE', 'legacy') == 'legacy'


def run_genie_sdk(section, steps, tests, uut='uut', parameters=None):
    '''Api to run any Triggers and Verification

    Allow to execute all Genie Triggers and Verifications as steps of a
    pyATS Testcase
    '''

    if not parameters:
        parameters = {}

    # Contains useful apis
    standalone = GenieStandalones(section, parent=section.parent)

    # Get device object
    if isinstance(uut, str):
        device = section.parameters['testbed'].devices[uut]
    else:
        device = uut

    for trigger in parameters:
        if isinstance(parameters[trigger], dict):
            if not parameters[trigger].get('devices', {}):
                parameters[trigger]['devices'] = [uut]

    if not parameters.get('devices'):
        parameters['devices'] = [uut]

    standalone.uut = device.name
    standalone.parameters['uut'] = device
    standalone._new_check_datafile(section.parent)

    for testcase_name in tests:
        # Is it a trigger?
        if testcase_name in section.parent.triggers:
            # Then load trigger
            params = dict(parameters, **parameters.get(testcase_name, {}))
            testcase_ins = standalone._load_trigger(testcase_name, params)
        elif testcase_name in section.parent.verifications:
            # Then load verifications
            params = dict(parameters, **parameters.get(testcase_name, {}))
            testcase_ins = standalone._load_verification(testcase_name, params)
        else:
            raise Exception("Cannot find '{t}'".format(t=testcase_name))
        failed = []
        # for the list of triggers in testcase_ins
        for tig in testcase_ins:
            with steps.start(tig.uid, continue_=True) as step:
                for temp_section in tig:
                    temp_section.parameters['steps'] = step
                    temp_section.parameters.internal['steps'] = step
                    try:
                        temp_section()
                    except AEtestInternalSignals as e:
                        # Result handled in step - pass
                        pass
                    except Exception as e:
                        # Good, but keep going
                        # Make the step fail
                        failed.append(e)
                        continue

                if failed:
                    for fail in failed:
                        log.error(fail)
                    step.failed(failed)


class Standalone(object):
    '''Class containing useful funcs for Genie Standalone mode'''
    def _new_check_datafile(cls, parent):

        trigger_datafile, verification_datafile = CmdArgs.get_argument()

        # Do we have a tb?
        if not 'testbed' in parent.parameters:
            raise Exception('Genie Verification requires a Testbed')

        tb = parent.parameters['testbed']

        # This both converts the testbed and sets up device.mapping which
        # is required in some triggers
        genie_testscript = TestScript(module=parent.module)
        parent.parameters['testbed'] = tb = genie_testscript.organize_testbed(tb, None, None)

        # Was a uut provided? else use uut as default
        uut = cls.uut if hasattr(cls, 'uut') else 'uut'

        if uut not in tb.devices:
            raise Exception("Device '{u}' does not exists".format(u=uut))

        uut = tb.devices[uut]

        # Check if this section has already been run, if so, do not run it
        # twice
        if not hasattr(parent, 'triggers'):
            # Its either that, or a lot more of hacking/monkey patching
            parent._validate_datafiles = partial(TestScript._validate_datafiles, parent)
            parent._load = partial(TestScript._load, parent)

            # Make sure it loads even if no uut
            alias = 'uut'
            if uut.alias != 'uut':
                alias = uut.alias
                uut.alias = 'uut'

            # Load the Trigger datafile
            TestScript.load_genie_datafiles(parent, tb, {}, trigger_datafile, verification_datafile,
                                            None, {}, None)
            # Reset Alias
            if alias != 'uut':
                uut.alias = alias

        # If uut is not connected, take care of it
        if not uut.is_connected():
            uut.connect()

        # Now take care of abstraction
        if 'abstract' not in parent.parameters:
            abstract = Lookup.from_device(uut,
                                          packages={'sdk':sdk,
                                                    'conf':conf,
                                                    'ops':ops,
                                                    'parser':parser})
            parent.parameters['abstract'] = abstract

    def _update_parameters(self, data, dev):
        # Create chainmap for where to find the value for this
        # source verification
        cm = []

        # Information for this Verification/Trigger
        info = data.get('devices_attributes', {}).get(dev, {})

        if info:
            cm.append(info)
        cm.append(data)

        d = ChainMap(*cm)
        return d

    def _add_parameters(self, data, parameters):
        ignore = set(['source', 'devices', 'devices_attributes',
                      'count', 'parameters', 'processors'])
        setter = ['groups']
        for k, value in data.items():
            # Ignore a few keys
            if k in ignore:
                continue

            # If provided in class, then overwrite the datafile
            if hasattr(self, k):
                value = getattr(self, k)

            if k in setter:
                setattr(self, k, value)
            else:
                parameters[k] = value
        return parameters


class GenieStandalones(Testcase, Standalone):
    '''New class with __iter__ modification so we can add the
    Triggers and Verifications'''
    def __init__(self, cls, verifications=None, triggers=None, order=None, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self._cls = cls
        self.verifications = verifications if verifications else\
                                         getattr(self._cls, 'verifications', [])
        self.triggers = triggers if triggers else\
                                         getattr(self._cls, 'triggers', [])
        self.order = order if order else getattr(self._cls, 'order', [])

    def _load_trigger(self, name, params=None):
        task = self
        while task.parent:
            task = task.parent

        # Get data for triggers
        uut = self.parameters['uut']
        if name not in task.triggers:
            raise Exception("'{n}' is not a valid trigger".format(n=name))
        triggers = []
        data = task.triggers[name]

        data = self._update_parameters(data, uut)
        parameters = {'uut': uut}
        parameters = self._add_parameters(data, parameters, name=name)
        # if params provided via args, just update parameters
        if params:
            parameters.update(params)

        # loop over devices in parameters
        for dev in parameters['devices']:
            device = task.parameters['testbed'].devices[dev]

            parameters['uut'] = device
            count = parameters.get('count',1)
            # get all ip addresses from the connections
            addresses = [v['ip'] for k, v in device.connections.items() if 'ip' in v]
            device.learn_management(addresses)
            # if trigger uses mapping, we need to update the data loaded from the
            # yaml file
            trigger_cls = load_class(data, device)
            name_dev='{n}.{d}'.format(n=name,d=dev)
            if hasattr(trigger_cls, 'mapping') and trigger_cls.mapping:
                if 'static' in parameters:
                    task.triggers[name]['static'] = \
                        parameters['static']
                if 'num_values' in parameters:
                    task.triggers[name]['num_values'] = \
                        parameters['num_values']

            # duplicate the same trigger based on count
            for i in range(count):
                # if count is one then dont show it in uid
                if count>1:
                    name_dev_count = '{n}.{d}'.format(n=name_dev, d=i+1)
                else:
                    name_dev_count = name_dev

                # create instance
                trigger_dev_ins = trigger_cls(parameters=parameters,
                                              uid=name_dev_count,
                                              parent=self)
                triggers.append(trigger_dev_ins)
        return triggers

    def _load_verification(self, name, params=None):
        task = self
        while task.parent:
            task = task.parent
        # Get data for verifications
        uut = self.parameters['uut']
        if name not in task.verifications:
            raise Exception("'{n}' is not a valid verification".format(n=name))
        verifications = []
        data = task.verifications[name]

        # Needed for Verification
        if not hasattr(task, 'verf'):
            task.verf = {}

        data = self._update_parameters(data, uut)
        parameters = {'uut': uut}
        parameters = self._add_parameters(data, parameters, name)
        # if params provided via args, just update parameters
        if params:
            parameters.update(params)
        for dev in parameters['devices']:
            device = task.parameters['testbed'].devices[dev]

            parameters['uut'] = device
            count = parameters.get('count',1)
            name_dev = '{n}.{d}'.format(n=name, d=dev)
            # duplicate the same trigger based on count
            for i in range(count):
                # if count is one then dont show it in uid
                if count > 1:
                    name_dev_count = '{n}.{d}'.format(n=name_dev, d=i + 1)
                else:
                    name_dev_count = name_dev

                # create instance
                verification_ins = TestcaseVerificationOps(parameters=parameters,
                                                           uid=name_dev_count,
                                                           parent=self)
                verification_ins.child = Template
                verification_ins.verification = name
                verifications.append(verification_ins)

        return verifications

    def _name_expander(self, container, name=None):
        ret = []
        if not isinstance(container, list):
            name = name or container.uid
            for section in container:
                section.uid = '{n}_{s}'.format(n=name,
                                               s=section.uid)
                ret.append(section)
        else:
            # if it's a list then we expand the list of triggers
            for triggers in container:
                name = triggers.uid
                for section in triggers:
                    section.uid = '{n}_{s}'.format(n=name,
                                                   s=section.uid)
                    ret.append(section)
        return ret

    def sorter(self, triggers, verifications, local, order):
        sections = []
        if not order:
            # Then the Genie Classic
            # Ignore all local sections
            # Ver - Trig - Ver - Trig - Ver ...
            for trigger in triggers:
                for verification in verifications:
                    cls_verification = self._load_verification(verification)
                    sections.extend(self._name_expander(cls_verification,
                                                        verification))

                cls_trigger = self._load_trigger(trigger)
                sections.extend(self._name_expander(cls_trigger))

            for verification in verifications:
                cls_verification = self._load_verification(verification)
                sections.extend(self._name_expander(cls_verification))
            return sections

        # Then follow whatever they defined in the order
        for item in order:
            if item in triggers:
                cls_trigger = self._load_trigger(item)
                sections.extend(self._name_expander(cls_trigger))
            elif item in verifications:
                cls_verification = self._load_verification(item)
                sections.extend(self._name_expander(cls_verification, item))
            elif item in local:
                # Then local just add it
                sections.extend(local[item])
            else:
                raise Exception("No idea what is '{i}".format(i=item))

        return sections

    def _update_parameters(self, data, dev):
        # Create chainmap for where to find the value for this
        # source verification
        cm = []

        # Information for this Verification/Trigger
        info = data.get('devices_attributes', {}).get(dev, {})

        if info:
            cm.append(info)
        cm.append(data)

        d = ChainMap(*cm)
        return d

    def _add_parameters(self, data, parameters, name=None):
        ignore = set(['source', 'devices_attributes',
                      'parameters', 'processors'])
        setter = ['groups']
        for k, value in data.items():
            # Ignore a few keys
            if k in ignore:
                continue

            # If provided in class, then overwrite the datafile
            if hasattr(self._cls, k):
                value = getattr(self._cls, k)

            if k in setter:
                setattr(self, k, value)
            else:
                parameters[k] = value

        # Check if custom_arguments is provided, and update parameters from it
        if name and hasattr(self._cls,
                            'custom_arguments') and name in self._cls.custom_arguments:
            for k in self._cls.custom_arguments[name]:
                if k in ignore:
                    continue
                parameters[k] = self._cls.custom_arguments[name][k]

        return parameters

    def _local_sections(self):
        categorized = {}
        tc_ins = self._cls(_default=True, parent=self)
        for section in tc_ins:
            name = section.function.__name__
            categorized.setdefault(name, [])
            categorized[name].append(section)
        return categorized

    def __iter__(self):
        uut = self.parameters['uut']

        # Collect all the sections to execute
        sections = []

        # Let's sort the triggers based on order
        tests = []

        local_sections = self._local_sections() if self._cls else {}

        # Sort the sections
        sections = self.sorter(triggers=self.triggers,
                               verifications=self.verifications,
                               local=local_sections,
                               order=self.order)
        # Now add a unique identifier for each
        for i, section in enumerate(sections):
            section.uid = '{s}.{i}'.format(s=section.uid, i=i+1)

        for section in sections:

            # override uut to section's uut
            if 'uut' in section.parameters:
                self.parameters['uut'] = section.parameters['uut']

            if 'timeout' in section.parameters:
                if not isinstance(section.parameters['timeout'], Timeout):
                    section.parameters['timeout'] = \
                        Timeout(max_time=section.parameters['timeout'].get('max_time', 0),
                                interval=section.parameters['timeout'].get('interval', 0))
            # We got to reset the timeout when a new trigger is started
            yield section


class GenieStandalone(Testcase, Standalone):
    '''We need to modify the __iter__ but also keep track of the orignal
    class,  so this temporary class play this role'''
    def __new__(cls, _default=False, *args, **kwargs):

        # In case parent set some important stuff
        parent = kwargs['parent']
        if _default:
            return super().__new__(cls)
        super(Testcase, cls).__new__(cls)

        cls._new_check_datafile(cls, parent)

        # Was a uut provided? else use uut as default
        tb = parent.parameters['testbed']
        cls.uut = cls.uut if hasattr(cls, 'uut') else 'uut'
        if cls.uut not in tb.devices:
            raise Exception("Device '{u}' does not exists".format(u=cls.uut))

        # Add parameters
        parameters = {}
        parameters['uut'] = tb.devices[cls.uut]

        if hasattr(cls, 'triggers') or hasattr(cls, 'verifications'):
            # In case parent set some important stuff
            #super(TriggerStandalone, cls).__new__(cls)
            parent = kwargs['parent']
            return GenieStandalones(cls=cls, uid=cls.__name__, parameters=parameters, *args, **kwargs)
        else:
            raise Exception("Need to provided 'triggers' or 'verifications'")


class CmdArgs(object):
    trigger_datafile_opt = {}
    verification_datafile_opt = {}
    @classmethod
    def get_argument(cls):
        if cls.trigger_datafile_opt and cls.verification_datafile_opt:
            return (cls.trigger_datafile_opt, cls.verification_datafile_opt)
        parsers = argparse.ArgumentParser()
        if LEGACY_CLI:
            trigger_datafile_arg = ['-trigger_datafile']
            verification_datafile_arg = ['-verification_datafile']
        else:
            trigger_datafile_arg = ['--trigger-datafile']
            verification_datafile_arg = ['--verification-datafile']
        group_cli_run_genie_sdk = parsers.add_argument_group('cli_standalone')
        group_cli_run_genie_sdk.add_argument(*trigger_datafile_arg,
                                             nargs='?',
                                             metavar='FILE',
                                             type=str,
                                             default={},
                                             help='Trigger datafile')
        group_cli_run_genie_sdk.add_argument(*verification_datafile_arg,
                                             nargs='?',
                                             metavar='FILE',
                                             type=str,
                                             default={},
                                             help='Verification datafile')

        # parse known arguments ('trigger_datafile', 'verification_datafile') only,
        # and pass the remaining arguments on to other script
        cliargs, unknown = parsers.parse_known_args(sys.argv[1:])
        sys.argv = sys.argv[:1] + unknown

        cls.trigger_datafile_opt = cliargs.trigger_datafile
        cls.verification_datafile_opt = cliargs.verification_datafile
        return (cls.trigger_datafile_opt, cls.verification_datafile_opt)
