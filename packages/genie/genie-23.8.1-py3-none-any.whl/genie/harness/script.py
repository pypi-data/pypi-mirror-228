import os
import shutil
import logging
import yaml
import json

from pyats.easypy import runtime
from pyats.log.utils import banner
from pyats.aetest.script import TestScript
from pyats.aetest.datafile import DatafileLoader
from pyats.aetest.exceptions import DatafileError

from genie.conf import Genie

from genie.harness.datafile.loader import MappingdatafileLoader,\
                                          TriggerdatafileLoader,\
                                          VerificationdatafileLoader,\
                                          ConfigdatafileLoader,\
                                          PtsdatafileLoader, \
                                          SubsectiondatafileLoader
from genie.libs.sdk import genie_yamls


# module level logger
logger = logging.getLogger(__name__)

# declare module as infra
__aetest_infra__ = True


class TestScript(TestScript):
    '''TestScript class

    Class that wraps a test script module. A test script in python is just a
    python module (type.ModuleType). This is not an extension of the module
    type. Rather, it's a class wraps the module and provides additional
    functionality (such as test parametrization).

    Note
    ----
        technically a TestScript class should inherit from TestContainer since
        it really is a container. However, there are practical differences
        between the two, such as a TestContainer being indirectly inherited by
        the user, and TestScript being totally transparent to the user, etc.
        Thus, this class inherit from the base TestItem instead.
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.verf = {}
        self.verification_uids = None
        self.trigger_uids = None
        self.verification_groups = None
        self.trigger_groups = None
        self.pts_features = ''
        self.script_type = 'genie.harness'

    def _validate_datafiles(self, testbed, trigger_datafile, verification_datafile,
                            pts_datafile, config_datafile, subsection_datafile):

        if 'uut' in testbed.devices and not trigger_datafile and\
           testbed.devices['uut'].os in genie_yamls.trigger_datafiles:
            # Then try to figure out which file to use base on uut
            # There is a limitation right now, only UUT triggers will be loaded
            # It is hardcoded for now for os. - If need more, we need
            # an abstraction based
            trigger_datafile =\
                   genie_yamls.trigger_datafiles[testbed.devices['uut'].os]
        elif not trigger_datafile:
            trigger_datafile = ''

        if 'uut' in testbed.devices and not verification_datafile and\
           testbed.devices['uut'].os in genie_yamls.verification_datafiles:
            # Then try to figure out which file to use base on uut
            # There is a limitation right now, only UUT triggers will be loaded
            # It is hardcoded for now for os. - If need more, we need
            # an abstraction based
            verification_datafile =\
                   genie_yamls.verification_datafiles[testbed.devices['uut'].os]
        elif not verification_datafile:
            verification_datafile = ''

        # Use default one
        if pts_datafile is None:
            pts_datafile = genie_yamls.pts_datafile

        if subsection_datafile is None:
            subsection_datafile = genie_yamls.subsection_datafile

        logger.info(banner('Genie datafiles used:'))
        logger.info('Trigger datafile          | {d}'.format(d=trigger_datafile))
        logger.info('Verification  datafile    | {d}'.format(d=verification_datafile))
        logger.info('Pts datafile              | {d}'.format(d=pts_datafile))
        logger.info('Subsection datafile       | {d}'.format(d=subsection_datafile))
        logger.info('Config datafile           | {d}'.format(d=config_datafile))

        return (trigger_datafile, verification_datafile, pts_datafile,
                config_datafile, subsection_datafile)

    def load_genie_datafiles(self, testbed, datafile, trigger_datafile,
                             verification_datafile, pts_datafile,
                             config_datafile,
                             subsection_datafile):
        '''load genie datafiles

        Loads the content of input datafile into dictionary

        Arguments
        ---------
            trigger_datafile (str): path of trigger datafile
            verification_datafile (str): path of verification datafile
            pts_datafile (str): path of pts datafile
            config_datafile (str): path of configs datafile
            subsection_datafile (str): path of subsections datafile
        '''
        trigger_datafile, verification_datafile, pts_datafile, config_datafile,\
            subsection_datafile = self._validate_datafiles(testbed,
                                                           trigger_datafile,
                                                           verification_datafile,
                                                           pts_datafile,
                                                           config_datafile,
                                                           subsection_datafile)
        # Copy all those files in the runtime directory
        for directory in [trigger_datafile, verification_datafile,
                          pts_datafile, config_datafile,
                          subsection_datafile]:
            try:
                shutil.copy(directory, runtime.directory)
            except:
                # Best effort
                pass

        self.triggers = self._load(trigger_datafile, TriggerdatafileLoader, testbed)
        self.verifications = self._load(verification_datafile,
                                        VerificationdatafileLoader, testbed)
        self.pts_data = self._load(pts_datafile, PtsdatafileLoader, testbed)
        self.config_data = self._load(config_datafile, ConfigdatafileLoader, testbed)
        self.subsection_data = self._load(subsection_datafile,
                                          SubsectiondatafileLoader, testbed)

        # Set triggers global parameters
        global_parameters = self.triggers.get('parameters', {})
        self.parameters.update(global_parameters)

        # save extended datafiles in the runtime directory
        datafile_dict = {
            'triggers': trigger_datafile,
            'verifications': verification_datafile,
            'pts_data': pts_datafile,
            'config_data': config_datafile,
            'subsection_data': subsection_datafile,
        }
        for datafile, filename in datafile_dict.items():
            if not filename:
                continue
            extended_datafile = getattr(self, datafile)
            # extended datafile name <filename>_extended.yaml
            filen, ext = os.path.splitext(filename)
            location = runtime.directory + '/' + filen.split(
                '/')[-1] + '_extended' + ext
            # open base datafile
            if str(filename).startswith('http'):
                datafile_yaml = DatafileLoader().load(filename)
            else:
                with open(filename, 'r') as f:
                    datafile_yaml = yaml.safe_load(f)
            # attach 'extended' file only when 'extends' exists
            if 'extends' in datafile_yaml.keys():
                try:
                    with open(location, 'w') as f:
                        # We dont want to dump OrderedDict objects as yaml wont
                        # be able to load them later. This converts the entire
                        # dictionary into a regular dict.
                        extended_datafile = json.loads(json.dumps(extended_datafile))
                        yaml.dump(extended_datafile, f)
                except Exception:
                    # Best effort
                    pass

    def _load(self, datafile, cls = None, testbed=None):

        loader_cls = cls or DatafileLoader
        if datafile == '':
            # No datafile was provided
            return {}
        try:
            loader = loader_cls(testbed)
            data = loader.load(datafile)
        except Exception as e:
            raise DatafileError("Failed to load the datafile '%s'"
                                % datafile) from e
        return data

    def organize_testbed(self, testbed, mapping_datafile, devices):

        testbed = Genie.init(testbed)
        self.mapping_data = self.default_mapping(mapping_datafile, testbed,
            devices)

        try:
            shutil.copy(mapping_datafile, runtime.directory)
        except:
            # Best effort
            pass

        # Only care about the device which are in mapping
        for dev, info in self.mapping_data['devices'].items():
            # find the device
            try:
                device = testbed.devices[dev]
            except (KeyError, Exception) as e:
                raise KeyError("Device '{dev}' is either defined in the "
                               "mapping file or passed in the job file "
                               "but does not exists in the testbed.".format(
                                dev=dev)) from None

            #Check if both new and old schema are used
            if "context" in info and "context" in info['mapping']:
                raise KeyError("In mapping datafile, context '{d}' was defined in "
                               "both new and old schema styles. "
                               "Use only one schema style. "
                               "Multiple schemas are not allowed".format(d=device.context))

            # Check if label was provided
            if 'label' in info:
                device.alias = info['label']

            # If no context, use default which is cli
            if 'context' in info:
                device.context = info['context']
            else:
                device.context = 'cli'

            # Set mapping
            # Cli is mandatory
            if 'mapping' not in info:
                raise KeyError("Key 'mapping' is missing in the "
                               "'mapping_datafile' for '{d}'".format(d=dev))

            # To check the context in old schema
            if device.context not in info['mapping']:
                # To check the context in new schema
                if device.context not in info['mapping']['context']:
                    raise KeyError("context '{k}' is missing in the "
                                   "'mapping_datafile' for "
                                   "'{d}'".format(k=device.context, d=dev))

            if 'cli' in info['mapping']:
                device.mapping['cli'] = info['mapping']['cli']

            # Yang is optional
            if 'yang' in info['mapping']:
                device.mapping['yang'] = info['mapping']['yang']
            # Yang is optional
            if 'netconf' in info['mapping']:
                device.mapping['netconf'] = info['mapping']['netconf']
            # Yang is optional
            if 'restconf' in info['mapping']:
                device.mapping['restconf'] = info['mapping']['restconf']
            # Yang is optional
            if 'gnmi' in info['mapping']:
                device.mapping['gnmi'] = info['mapping']['gnmi']
            # Rest is optional
            if 'rest' in info['mapping']:
                device.mapping['rest'] = info['mapping']['rest']
            # Xml is optional
            if 'xml' in info['mapping']:
                device.mapping['xml'] = info['mapping']['xml']
            # Web is optional
            if 'web' in info['mapping']:
                device.mapping['web'] = info['mapping']['web']
            # For new schema context
            if 'context' in info['mapping']:
                device.mapping['context'] = info['mapping']['context']

        if 'topology' in self.mapping_data:
            # handle links
            if 'links' in self.mapping_data['topology']:
                link_dict = {i.name: i for i in testbed.links}

                for link_name, link_data in self.mapping_data['topology']['links'].items():
                    # link_name must exist in testbed

                    if link_name not in link_dict:
                        raise KeyError("Link '{}' is defined in mapping file "
                                       "but does not exist in testbed.".format(
                                                    link_name)) from None
                    if 'label' in link_data:
                        link_dict[link_name].alias = link_data['label']

            # handle interfaces
            for device_name, interfaces in self.mapping_data['topology'].items():
                # skip links
                if device_name == "links":
                    continue

                # device name must be specified in testbed
                if not device_name in testbed.devices:
                    raise KeyError("Device '{}' is defined in the mapping file "
                                   "but does not exist in testbed.".format(
                                                        device_name)) from None

                # tap into interfaces dictionary
                interfaces = interfaces.setdefault('interfaces', {})

                for interface_name, interface_data in interfaces.items():
                    # interface name must be in testbed
                    if interface_name not in testbed.devices[device_name].interfaces:
                        raise KeyError("Interface '{}' is defined in mapping file "
                                       "but does not exist in testbed.".format(
                                                    interface_name)) from None
                    if 'label' in interface_data:
                        testbed.devices[device_name].interfaces[interface_name].alias = interface_data['label']

        return testbed

    def default_mapping(self, mapping_datafile, testbed, devices):

        if mapping_datafile:
            mapping_dict = self._load(mapping_datafile, MappingdatafileLoader)
            return mapping_dict

        mapping_dict = {}
        mapping_dict.setdefault('devices', {})
        trimmed_connections = {}

        # Check if devices were provided in the job file
        if devices:
            iterator=devices
        else:
            iterator=testbed.devices

        for device in iterator:

            mapping_dict['devices'].setdefault(device, {})
            # Defaulting context to 'cli'
            mapping_dict['devices'][device]['context'] = 'cli'
            mapping_dict['devices'][device].setdefault('mapping', {})

            # If single connection use it otherwise default connection name to 'cli'
            try:
                trimmed_connections = {
                    key: value for (key,value) in testbed.devices[device].\
                    connections.items() if key != 'defaults'}
            except KeyError:
                # Case when user provides a device that is not found in yaml file
                # This exception is perfectly handled later with an explicit
                # user message
                pass

            if len(trimmed_connections.keys()) == 1:
                via, value = dict(trimmed_connections).popitem()
                mapping_dict['devices'][device]['mapping']['cli'] = via
            elif 'cli' in trimmed_connections.keys():
                mapping_dict['devices'][device]['mapping']['cli'] = 'cli'
            elif 'vty' in trimmed_connections.keys():
                mapping_dict['devices'][device]['mapping']['cli'] = 'vty'
            elif 'a' in trimmed_connections.keys() and 'b' not in trimmed_connections.keys():
                mapping_dict['devices'][device]['mapping']['cli'] = 'a'
            elif 'a' in trimmed_connections.keys() and 'b' in trimmed_connections.keys():
                mapping_dict['devices'][device]['mapping']['cli'] = ['a', 'b']
            else:
                raise Exception("Connection named 'cli' not found in testbed "
                                "YAML file for device '{}'".format(device))

        return mapping_dict
