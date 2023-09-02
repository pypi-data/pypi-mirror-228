from genie.utils.dq import Dq

from pyats.utils.yaml import Loader, markup
from pyats.topology.loader.markup import TestbedMarkupProcessor

from .schema import mappingdatafile_schema,\
                    triggerdatafile_schema,\
                    verificationdatafile_schema,\
                    configdatafile_schema,\
                    ptsdatafile_schema, \
                    subsectiondatafile_schema

# declare module as infra
__genie_infra__ = True


class CommonLoader(Loader):
    '''CommonLoader

    Subclass of utils.yaml.Loader class that performs loading the
    datafiles that drives the testscript (or, acts as inputs that sets variables
    and parameters in a testscript).
    '''
    def __init__(self, testbed = None, enable_extensions = True):
        '''built-in __init__

        instantiates base class Loader with datafile schema and support
        for one datafile to extend another datafile via the use of recursive
        file loading.
        '''
        self.testbed = testbed.raw_config if testbed else None
        super().__init__(enable_extensions = enable_extensions,
                         markupprocessor=self.markup_processor,
                         postprocessor = self.remove_extends,
                         schema=self.schema,
                         preserve_order=True)

    def markup_processor(self, content):
        """ Markup processor that adds access to the testbed object in
            other datafiles via markup syntax: %{testbed.<var>.<var>}
        """

        # add testbed datafile to the current datafile
        if self.testbed:

            # Temp fix. self.testbed is equal to post-extend but pre-markup.
            # So we need to resolve the testbed markups first as these will not
            # resolve once they are added to the datafile under 'testbed' key
            tb_processor = TestbedMarkupProcessor()
            self.testbed = tb_processor(self.testbed)

            # collecting all the device aliases and their names
            device_dict = self._device_alias_dict(self.testbed.get('devices'))
            # collecting all the topology interfaces aliases and Links device aliases
            interface_dict = self._topology_alias_dict(self.testbed.get('topology'))
            content.update({'testbed': self.testbed})
            # updating testbed['devices']
            content = self._testbed_device_updater(content, device_dict)
            # updating testbed['topology']
            content = self._testbed_topology_updater(content, interface_dict)

        # do markup processing
        processor = markup.Processor()
        content = processor(content)

        # remove testbed datafile from the current datafile
        if self.testbed:
            _ = content.pop('testbed', ())

        return content

    def remove_extends(self, content):
        # Ignore result
        _ = content.pop('extends', ())
        return content

    def _device_alias_dict(self, devices):

        # mapping devices and their alias storing them in a dict 
        alias_mapping_dict = {}
        for dev_name, dev_data in devices.items():
            if dev_data.get('alias'):
                alias_mapping_dict.update({dev_data['alias']: dev_name})

        return alias_mapping_dict

    def _testbed_device_updater(self, content_dict, device_dict):

        for device_alias, device in device_dict.items():
            # add device name to _name under device
            content_dict['testbed']['devices'][device]['_name'] = device

            # duplicate pointer to the device object
            content_dict['testbed']['devices'][device_alias] = content_dict['testbed']['devices'][device]

            # if topology exists storing the device by its alias inside the topology section
            if content_dict['testbed'].get('topology') and device in content_dict['testbed']['topology']:
                content_dict['testbed']['topology'][device_alias] = content_dict['testbed']['topology'][device]

        return content_dict

    def _topology_alias_dict(self, topology):

        # mapping Links and interfaces in topology section by their alias
        alias_mapping_dict = {}
        alias_mapping_dict['interfaces'] = {}
        alias_mapping_dict['links'] = {}

        # if no topology then return empty dict
        if not topology:
            return alias_mapping_dict

        for dev_name, dev_data in topology.items():

            # if topology has Links in them store Links devices by their alias
            if dev_name == 'links':
                for link, link_data in dev_data.items():
                    dev_data[link]['_name'] = link
                links_alias_dict = self._device_alias_dict(dev_data)
                alias_mapping_dict.update({'links':links_alias_dict})
                continue

            # add device name under _name
            dev_data['_name'] = dev_name

            # Update topology[<dev_name>]['interface'][<interface>] by its interface alias
            alias_mapping_dict['interfaces'].update({dev_name:{}})
            for interface, interface_data in dev_data['interfaces'].items():

                # add interface name under _name
                interface_data['_name'] = interface
                if interface_data.get('alias'):
                    alias_mapping_dict['interfaces'][dev_name].update({interface_data['alias']:interface})

        return alias_mapping_dict

    def _testbed_topology_updater(self, content_dict, interface_dict):

        # creating duplicate pointer to Links devices by their alias
        for link_dev_name, link_dev_data in interface_dict['links'].items():
            content_dict['testbed']['topology']['links'][link_dev_name] = content_dict['testbed']['topology']['links'][link_dev_data]

        # creating duplicate pointer to interface for each device by its alias
        for device_name, interface_aliases in interface_dict['interfaces'].items():
            for alias, interface in interface_aliases.items():
                content_dict['testbed']['topology'][device_name]['interfaces'][alias] = content_dict['testbed']['topology'][device_name]['interfaces'][interface]

        return content_dict

class MappingdatafileLoader(CommonLoader):
    '''MappingfileLoader

    Subclass of CommonLoader class that performs loading the Mapping
    datafile that drives the testscript (or, acts as inputs that sets variables
    and parameters in a testscript).
    '''

    schema = mappingdatafile_schema


class TriggerdatafileLoader(CommonLoader):
    '''TriggerdatafileLoader

    Subclass of CommonLoader class that performs loading the trigger
    datafiles that drives the testscript (or, acts as inputs that sets
    variables and parameters in a testscript).
    '''

    schema = triggerdatafile_schema


class VerificationdatafileLoader(CommonLoader):
    '''VerificationdatafileLoader

    Subclass of CommonLoader class that performs loading the verification
    datafiles that drives the testscript (or, acts as inputs that sets
    variables and parameters in a testscript).
    '''

    schema = verificationdatafile_schema


class ConfigdatafileLoader(CommonLoader):
    '''ConfigdatafileLoader

    Subclass of CommonLoader class that performs loading the config
    datafiles that drives the testscript (or, acts as inputs that sets
    variables and parameters in a testscript).
    '''

    schema = configdatafile_schema

class PtsdatafileLoader(CommonLoader):
    '''ConfigdatafileLoader

    Subclass of CommonLoader class that performs loading the config
    datafiles that drives the testscript (or, acts as inputs that sets
    variables and parameters in a testscript).
    '''

    schema = ptsdatafile_schema

class SubsectiondatafileLoader(CommonLoader):
    '''SubsectiondatafileLoader

    Subclass of CommonLoader class that performs loading the config
    datafiles that drives the testscript (or, acts as inputs that sets
    variables and parameters in a testscript).
    '''

    schema = subsectiondatafile_schema
