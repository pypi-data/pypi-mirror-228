# Python
import os
import time
import dill
import json
import logging
import pathlib
import jsonpickle
import prettytable
from traceback import format_exc
from concurrent.futures import ThreadPoolExecutor

# ATS
from pyats import aetest
# import pcall
import importlib
try:
    pcall = importlib.import_module('pyats.async').pcall
except ImportError:
    from pyats.async_ import pcall
# # import pcall
# from pyats.async import pcall
from pyats.easypy import runtime
from pyats.log.utils import banner
from pyats.aetest import CommonSetup, CommonCleanup
from genie.abstract import Lookup
from genie.utils import Dq

# Import FileUtils core utilities
from pyats.utils.fileutils import FileUtils

# Import zip_longest
from itertools import zip_longest

# Genie
from genie.libs import sdk
from genie.utils.diff import Diff
from genie.utils.config import Config
from genie.utils.summary import Summary
from genie.utils.timeout import Timeout
from genie.utils.profile import Profile, unpickle, pickle, summarize_comparison, pickle_traffic, unpickle_traffic, unpickle_stream_data
from .utils import load_class, connect_device
from genie.harness.exceptions import GenieTgnError
# Unicon
from unicon.eal.dialogs import Statement, Dialog

# Module variables
log = logging.getLogger(__name__)

EXCLUDED_DEVICE_TYPES = ['tgn', 'ixia']

# Valid file transfer protocols
VALID_FILE_TRANSFER_PROTOCOL = ['tftp']
# TODO - change design for valid protocols

# Subsections for CommonSetup / CommonCleanup

# subsections for common_setup
def connect(self, testbed, steps, parallel=True):
    '''Connect to all the devices defined in mapping file'''

    # Figure out which devices to connect to
    devs = []
    devs_as_provided = []
    for dev in self.parent.mapping_data['devices']:
        device = testbed.devices[dev]
        if device.type in EXCLUDED_DEVICE_TYPES:
            log.info("This subsection is not supported for TGN device "
                     "'{}'".format(device.name))
            continue
        devs.append(device)
        devs_as_provided.append(dev)

    log.info("Connect to all the devices described in the "
             "'Mapping Datafile' and 'Testbed file': {devs}"
             .format(devs=', '.join([dev.name for dev in devs])))
    log.info('For more information visit Genie connection section '
             'documentation: '
             '{url}/harness/user/gettingstarted.html#set-up\n'
             .format(url=self.parent.url))

    # Only take care of the devices defined in mapping file
    # Hold summary information
    summary_information = {}
    errored_message = {}

    def connection_task(dev):
        device = testbed.devices[dev]

        pool_size = self.parent.mapping_data['devices'][dev].\
                                                 get('pool_size', None)

        netconf_pool_size = self.parent.mapping_data['devices'][dev].\
                                                 get('netconf_pool_size', None)

        summary_information[device] = {}

        try:
            connect_device(device, pool_size, netconf_pool_size, summary_information[device])
        except Exception as e:
            # log the traceback otherwise its impossible to debug
            log.error(format_exc())

            errored_message[dev] = e
            return

        # Workaround until logging get fixed by ATS team
        log.info('')
        log.info(banner("Identifying device '{d}' management interface".format(
            d=device.name)))

        # Set management_interface to None so that the attribute exists on the
        # device, even if no management interface is found.
        device.management_interface = None

        # Retrieve the device corresponding management interface name
        for connection_name in device.connections.keys():
            if 'ip' in device.connections[connection_name].keys():
                # get the ip address as a string
                ipaddress = device.connections[connection_name]['ip'].exploded
                # pass the ip to the learn_management API
                device.learn_management(ipaddress)
                # Workaround until logging get fixed by ATS team
                # Exit for loop if management interface found to save time
                if device.management_interface:
                    # Workaround until logging get fixed by ATS team
                    log.info('')
                    log.info("Device '{d}' management interface is '{m}'"
                             .format(d=device.name,
                                     m=device.management_interface))
                    break
            else:
                continue
        else:
            log.info('')
            log.info("Device '{d}' does not have a management interface "
                     "configured which could be found"
                     .format(d=device.name))

    if parallel:
        # Connect to all devices in devs_as_provided in parallel
        with ThreadPoolExecutor(max_workers=len(devs_as_provided)) as executor:
            executor.map(connection_task, devs_as_provided)
    else:
        for dev in devs_as_provided:
            connection_task(dev)

    log.info('\n')
    # Create Summary
    summary = Summary(title='Connection Summary', width=150)

    # Case when connection establishment failed for one of the devices
    if errored_message:
        for dev in errored_message.keys():
            remain_dev_list = list(self.parent.mapping_data['devices'].keys())
            remain_dev_list.remove(dev)

            msg = "Failed to establish connection, {e}. Scroll up for tracebacks.".\
                  format(e=errored_message[dev])
            summary.summarize_section(message=msg, level='error',
                                      device=dev)

            if remain_dev_list:
                # In case only 1 device - and couldnt connect
                summary.add_message(msg="* Summary for devices: '{}'".\
                                        format(', '.join(remain_dev_list)))
                summary.add_sep_line()
                msg = "Didn't try to establish connection due "\
                      "to failure in establishing connection with one of the "\
                      "required devices '{d}'".format(d=dev)
                summary.summarize_section(message=msg)

            summary.print()
            log.info('\nInformation about devices and connections can be '
                     'found in the Testbed file and Mapping datafile')
            self.errored("Failed to establish connection to {dev}. "
                         "Please check summary table for details"
                         .format(dev=dev),
                         goto = ['common_cleanup'])

    for dev in sorted(self.parent.mapping_data['devices']):
        device = testbed.devices[dev]

        if device not in summary_information:
            msg = 'Connection to this device has not been '\
                  'established - This is expected'
            summary.summarize_section(message=msg, device=device.name)
            continue

        # No idea how can this happen, but dont want the code to crash without
        # saying why
        if 'connected' not in summary_information[device]:
            raise Exception("Connection to '{d}' is not successfull")

        for information in summary_information[device]['connected']:
            alias, via, pool_size = information
            msg = "Connected with alias '{a}' using "\
                  "connection '{v}'".format(a=alias, v=via)
            if pool_size is not None:
                msg = msg + " with '{p}' connection pool".format(p=pool_size)

            summary.summarize_section(message=msg, device=device.name)

    summary.print()
    log.info('\nInformation about devices and connections can be found in the '
             'Testbed file and Mapping datafile')


def disconnect(self, testbed, steps):
    '''Disconnect to all the devices defined in mapping file'''

    # Only take care of the devices defined in mapping file
    summary_information = {}
    for dev in sorted(self.parent.mapping_data['devices']):
        device = testbed.devices[dev]
        summary_information[device] = {'alias':[]}

        # For each mapping provided, connect
        allowed_mapping = ['cli', 'yang', 'rest', 'xml', 'web', 'restconf', 'netconf', 'gnmi']

        # Needed for abstraction for some connection; Need a better way
        if hasattr(device, 'context'):
            device.context = device.context
        if device.type in EXCLUDED_DEVICE_TYPES:
            log.info("This subsection is not supported for "
                     "TGN device '{}'".format(device.name))
            continue

        for mapping in allowed_mapping:
            if mapping in device.mapping:
                try:
                    # If HA connection, disconnect from mapped alias, not from
                    # the list of connections
                    if device.mapping[mapping] == ['a', 'b']:
                        device.disconnect(alias=mapping)
                    else:
                        device.disconnect(alias=device.mapping[mapping])

                except ValueError as e:
                    raise ValueError("'{m}' was provided in the "
                                     "mapping_datafile but does not "
                                     "exists in the testbed "
                                     "file".format(m=mapping)) from e
                summary_information[device]['alias'].append(mapping)

    # Create Summary
    summary = Summary(title='Disconnection Summary', width=150)
    for dev in sorted(self.parent.mapping_data['devices']):
        device = testbed.devices[dev]

        if device not in summary_information or\
            'alias' not in summary_information[device] or\
            not summary_information[device]['alias']:
            msg = "Disconnection to this device has not been "\
                  "executed - This is expected"
            summary.summarize_section(message=msg,
                device=device.name)
            continue

        for alias in summary_information[device]['alias']:
            msg = "Disconnected with alias '{a}'".format(a=alias)
            summary.summarize_section(message=msg,
                device=device.name)

    summary.print()
    log.info('\nInformation about devices and connections can be found in the '
             'Testbed file and Mapping datafile')


def _configure_find_protocol(self, protocol, testbed, summary):
    address = None
    if protocol:
        # If the user chosen protocol is not in the testbed file, error
        # subsection
        if protocol not in testbed.servers:
            msg = "'{p}' protocol server is missing from the "\
                  "testbed file".format(p=protocol)
            summary.summarize_section(message=msg, level='error')
            summary.print()
            log.info("\n")
            self.errored("\n'{p}' protocol server must be provided in the "
                         "testbed file".format(p=protocol))

        # If the user chosen protocol doesn't have address, error the subsection
        if not hasattr(testbed.servers[protocol], 'address'):
            msg = "'{p}' protocol server is missing the "\
                  "address in the testbed yaml file".format(p=protocol)
            summary.summarize_section(message=msg, level='error')
            summary.print()

            log.info("\n")
            self.errored("A file transfer protocol '{p}' has been provided, "
                         "but no server info found in the testbed "
                         "yaml datafile.Example;\nservers:\n    {p}:\n"
                         "        server: 'server_name'\n        "
                         "address: 'server address'\n        "
                         "username: 'username accessing the server'\n        "
                         "password: 'password when accessinhg the server'\n"
                         "        path: 'default path on the server'".\
                         format(p=protocol))
        else:
            address = testbed.servers[protocol].address
    else:
        # If user didn't pass the transfer protocol to be used, will pick one
        # as per the servers passed in the testbed yaml file
        if hasattr(testbed, 'servers') and testbed.servers:
            for item in sorted(testbed.servers):
                if item in VALID_FILE_TRANSFER_PROTOCOL:
                    # If protocol doesn't have address, skip to the next one
                    if hasattr(testbed.servers[item], 'address'):
                        address = testbed.servers[item].address
                    else:
                        continue

                    # Only set protocol if an address is found
                    protocol = item
                    break

    return address, protocol


def _get_config_sequence(device_config_items):
    ''' Get list of sequence numbers from the config sequence
    dictionaries from the config data

    Args
        device_config_items (dict): Dictionary with sequence as the key
    Returns:
        sorted list of sequence numbers
    '''
    sequence = set()
    # create lists of sequence numbers from config data
    for device_dict in device_config_items:
        sequence.update(set(device_dict.keys()))

    return sorted(sequence, key=int)


def configure(self, testbed, steps):
    '''Configure the devices'''

    # Setup transfer protocol
    log.info("Configure each device with the configuration provided in the "
             "'Config datafile'")
    log.info('For more information visit Genie configure section '
             '{url}/harness/user/gettingstarted.html#configuration'
             .format(url=self.parent.url))

    # Retrieve config_datafile info
    configs = self.parent.config_data

    # Protocol to use to copy the configuration on the device
    protocol = self.parent.filetransfer_protocol or None

    # Create Summary
    summary = Summary(title='Configuration Summary', width=150)

    address, protocol = _configure_find_protocol(self, protocol, testbed, summary)

    if not protocol:
        # No protocol found, so check if transfer is required or not. If
        # required then error out for missing server info. If not, Skip as no
        # server info is required since there are no transfers.
        dq_configs = Dq(configs)
        if configs and 'devices' in configs and dq_configs.contains('config'):
            msg = "Can't proceed with configuration, Server "\
                "info is missing from the testbed yaml file"
            summary.summarize_section(message=msg, level='error')
            summary.print()
            # Configs copy is required but server info is not found
            log.info("\n")
            self.errored("To copy the configuration to the devices, a server "
                        "must be provided in the testbed datafile. "
                        "Supported types: {ps}"
                        .format(ps=', '.join(VALID_FILE_TRANSFER_PROTOCOL)))

        elif configs and 'devices' in configs and dq_configs.contains('jinja2_config'):
            pass

        else:
            msg = "No configuration to apply on any device"
            summary.summarize_section(message=msg, level='warning')
            summary.print()
            log.info("\n")
            self.skipped("No configuration to be applied on any device")

    # Now setup transfer protocol for each device in the mapping file
    if protocol:
        set_filetransfer_argument(self, testbed, address, protocol)

    if not configs or configs and not 'devices' in configs:
        msg = "No configuration to apply on any device"
        summary.summarize_section(message=msg, level='warning')
        summary.print()
        log.info("\n")
        self.skipped("No configuration to be applied on any device")

    # Create the big list to be distributed over pcall later
    functions_list = []
    device_dict = {}

    # get sequence list
    sequence = _get_config_sequence(configs['devices'].values())

    # This sort by name - for consistency
    for dev, config in sorted(configs['devices'].items()):
        # Create a list for the device related configs. To be used later in
        # the pcall function districution
        device_configs_list = []

        # Find coresponding device object
        try:
            device = testbed.devices[dev]
        except KeyError:
            raise Exception("Couldn't configure '{d}' as it does not"
                            "exists in the testbed file but is defined in the "
                            "config datafile".format(d=dev))

        if device.type in EXCLUDED_DEVICE_TYPES:
            # Already printed at the top about not for TGN - No need to repeat
            continue

        # process config items for each sequence
        for seq in sequence:
            conf = config.get(seq)

            # empty config_dict will be used as 'filler' to ensure sequential execution
            config_dict = {
                'device': device,
                'source': '',
                'destination': '',
                'invalid': [],
                'type': None,
                'rendered': '',
                'sleep': 0,
                'config_file': '',
                'verify': '',
                'sequence': seq
            }

            if not conf:
                # append filler to ensure config sequence
                device_configs_list.append(config_dict)
                continue

            # 1) If type is not provided - default is common setup - so only
            #    run there
            # 2) If type is provided, only run where it is asked
            type_ = conf.get('type', 'setup')
            if type_ not in ['setup', 'cleanup']:
                self.failed("Configuration 'type' must be either setup or cleanup - "
                                  "not '{t}'".format(t=type_))

            if (type_ == 'setup' and isinstance(self, CommonCleanup)) or \
               (type_ == 'cleanup' and isinstance(self, CommonSetup)):
                # append filler to ensure config sequence
                device_configs_list.append(config_dict)
                continue

            config_dict = {}

            # If jinja2 config is present
            if conf.get('jinja2_config'):
                try:
                    fullpath = pathlib.Path(conf.get('jinja2_config'))
                    log.debug(f'fullpath: {fullpath}')

                    path = str(fullpath.absolute().parent)
                    log.debug(f'path: {path}')
                    file = fullpath.name
                    jinja2_arguments = conf.get('jinja2_arguments', {})
                    rendered = device.api.load_jinja_template(
                        path = path,
                        file = file,
                        **jinja2_arguments
                    )
                except Exception:
                    msg = f"Provided Jinja2 file {fullpath} is not valid " \
                          f"for device {dev} seq {seq} " \
                          f"with jinja2_arguments\n{json.dumps(jinja2_arguments)}"
                    log.exception(msg)
                    self.failed(goto = ['common_cleanup'])

                config_dict = {
                    'device': device,
                    'sleep': conf.get('sleep', 0),
                    'rendered': rendered,
                    'type': 'jinja',
                    'config_file': conf.get('jinja2_config'),
                    'configure_arguments': conf.get('configure_arguments', {}),
                    'verify': conf.get('verify'),
                    'sequence': seq
                    }

            else:
                # TODO - rewrite this after geniefiletransferutils change
                if testbed.devices[dev].os == 'junos':
                    URL = "{username}@{address}:/{config_file}".\
                        format(username=device.filetransfer_attributes['username'],
                                address=address, config_file=conf['config'])

                    # Gather the device related config info
                    config_dict = {
                        'device': device,
                        'source': URL,
                        'destination': '',
                        'invalid': conf.get('invalid', []),
                        'sleep': conf.get('sleep', 0),
                        'config_file': conf['config'],
                        'verify': conf.get('verify'),
                        }
                else:
                    # Build the URL passed to filetransferutils package
                    URL = '{e}://{address}/{config_file}'.format(e=protocol,
                        address=address, config_file=conf['config'])

                    # Gather the device related config info
                    config_dict = {
                        'device': device,
                        'source': URL,
                        'destination': 'running-config',
                        'invalid': conf.get('invalid', []),
                        'sleep': conf.get('sleep', 0),
                        'config_file': conf['config'],
                        'verify': conf.get('verify'),
                        }

            # Add vrf only if specified in config datafile
            if 'vrf' in conf:
                config_dict['vrf'] = conf.get('vrf')

            # Create the device-configs dictionary
            device_configs_list.append(config_dict)

        # If no configuration to apply - do not add device_configs_list to
        # device_dict
        if device_configs_list:
            device_dict[dev] = device_configs_list

    try:
        # Apply configs using the asynchronous approach
        pcall_configure(device_dict)
    except Exception as e:
        devices = [k  for  k in  device_dict.keys()]
        msg = "Failed in applying configuration(s) on one of the devices '{d}'".\
            format(d=', '.join(devices))
        summary.summarize_section(message=msg, level='error', end=False)
        summary.print()
        log.info("\n")
        log.exception('Failed to configure devices')
        self.failed("{err}".format(err=e), goto = ['common_cleanup'])

    for dev in device_dict:
        summary.add_message(msg="Successfully applied the following "
            "configuration(s) on device: {}".format(dev))
        summary.add_sep_line()
        for config_url in device_dict[dev]:
            if config_url.get('config_file'):
                summary.add_message(msg="{} ({})".format(
                    config_url['config_file'],
                    config_url.get('sequence')))
        summary.add_subtitle_line()

    summary.print()
    log.info("\n")

    if 'sleep' in configs:
        log.info("Sleeping for '{s}' seconds to make sure the configuration is "
                 "stable. Sleeping time can be adjusted in the configuration "
                 "datafile".format(s=configs['sleep']))
        time.sleep(configs['sleep'])

    log.info('Configuration applied on the following devices: {devs}'
             .format(devs=', '.join(device_dict.keys())))


def pcall_configure(device_dict):
    '''Use asynchronous execution when applying configurations to devices.

    Args:
        funtions_list (list of callable): List of copy functions, relevant callable per device.
        device_dict (dict): Dictionary with key of device name and value a list of
                            dictionaries with config details for each device.

            device_dict = {
                "device_name": [config_dict, config_dict, ...]
            }

            config details:

                    config_dict = {
                        'device': # Device class instance,
                        'source': # URL with source of config data
                        'rendered': # Config text to apply
                        'type': 'jinja' # jinja or None
                        'destination': # Destination on device
                        'invalid': # List of regex patterns
                        'sleep': # Wait time after config apply
                        'config_file': # Config file to load
                        'verify': # Dict with verify method and options
                        'sequence': # Sequence number of config
                        'configure_arguments': # unicon configure service arguments
                    }
    '''

    timeout_verification = []

    # Prepare the config data in the format to be passed to pcall
    for async_configs in zip_longest(*list(device_dict.values())):
        pcall_list = []

        for device_config_info in async_configs:
            if not device_config_info:
                continue

            if not (device_config_info.get('rendered') \
                or device_config_info.get('config_file')):
                continue

            pcall_dict = \
                {k:v for k,v in device_config_info.items() if k not in ['sleep', 'verify']}

            pcall_list.append(pcall_dict)

            # Build the verify verification list
            verify = device_config_info.get('verify')
            if verify:
                timeout_verification.append({'device':device_config_info['device'],
                                             'args':verify})

        if pcall_list:
            try:
                log.info(banner("Applying configurations in parallel"))
                for item in pcall_list:
                    log.info("Applying '{p}' on '{d}' #{s}".format(p=item['config_file'],
                        d=item['device'], s=item.get('sequence')))

                # Use multiple targets pcall functionality
                pcall(_configure_on_device, ikwargs = pcall_list)

                # Sleep for x amount of time after applying configuration
                sleep_time = max(device_config_info['sleep']
                    for device_config_info in async_configs
                    if device_config_info and 'sleep' in device_config_info)
                if sleep_time:
                    log.info("Sleeping for the '{s}' seconds , the longest provided"
                            " in the config datafile per configuration file".\
                            format(s=sleep_time))
                    time.sleep(sleep_time)

            except Exception as e:
                log.error("Issue while applying the configuration on the devices.")
                raise

    # If provided, verify configuration with a callable
    if timeout_verification:
        pcall(verify_configuration, ikwargs = timeout_verification)

    log.info(banner("Checking devices are still alive after applying "
             "configuration"))
    for config_item in device_dict.values():
        dev = config_item[0]['device']
        try:
            # Checking device is still alive after applying configuration
            log.info("Sending empty command on device '{d}'".format(
                d=dev.name))
            dev.execute('')
        except Exception as e:
            log.error(str(e))
            raise Exception("{d} is not responding after applying "
                "configuration".format(d=dev.name)) from e


def _configure_on_device(**kwargs):
    ''' Helper function for pcall to configure devices
    '''
    device = kwargs.get('device')
    rendered = kwargs.get('rendered')
    configure_arguments = kwargs.get('configure_arguments', {})
    type_ = kwargs.pop('type', None)
    config_file = kwargs.get('config_file')

    if not device:
        log.error(f'No device {kwargs}')
        return

    if type_ == 'jinja':
        device.configure(rendered, **configure_arguments)
    elif config_file:
        # Extract the device platform corresponding copy function
        copyfunction = FileUtils.from_device(device).copyfile
        copyfunction(**kwargs)
    else:
        log.info(f'Nothing to configure for device {device} with {kwargs}')


def verify_configuration(device, args):
    if not args:
        return

    # Verify all is there
    for value in ['method', 'max_time', 'interval']:
        if value not in args or not args[value]:
            raise Exception("timeout has been provided but '{v}' "
                            "is missing".format(v=value))

    # Load the method
    full_name = args.get('method')
    try:
        # last value is the function name
        module_path, method_name = full_name.rsplit('.', 1)
    except Exception as e:
        raise Exception("Method name '{m}' is not a valid "
                        "one\n{e}".format(m=full_name, e=e))

    try:
        module = importlib.import_module(module_path)
        method = getattr(module, method_name)
    except Exception as e:
        raise Exception("Could not find '{m}' - It could not be loaded\n"
                        "{e}".format(m=full_name, e=e))

    # Instantiate the timeout
    max_time = args.get('max_time', 0)
    interval = args.get('interval', 0)
    kwargs = args.get('parameters', {})
    kwargs['device'] = device
    log.info("{method} has been provided to verify the configuration"
             .format(method=full_name))
    timeout = Timeout(max_time=max_time,
                      interval=interval)

    while timeout.iterate():
        try:
            if method(**kwargs):
                break
        except Exception as e:
            log.error("{method} has raised an exception - "
                      "Trying again\n{e}".format(method=full_name, e=e))
        timeout.sleep()
    else:
        raise Exception("{method} failed to verify the configuration")


def set_filetransfer_argument(self, testbed, address, protocol):
    '''Add filetransfer argument to the device object to be used in copying
    to/from device during the run'''

    for dev in sorted(self.parent.mapping_data['devices']):
        device = testbed.devices[dev]

        # Skip this step for TGN devices
        if device.type in EXCLUDED_DEVICE_TYPES:
            log.info("This subsection is not supported for TGN device '{}'".\
                format(device.name))
            continue

        # Instantiate a filetransferutils instance for the device, corresponding
        # to the device specific OS
        device.filetransfer = FileUtils.from_device(device)
        device.filetransfer_attributes = {}
        device.filetransfer_attributes['server_address'] = address
        device.filetransfer_attributes['protocol'] = protocol
        for attribute in ['path', 'username', 'password']:
            device.filetransfer_attributes[attribute] = \
                                testbed.servers[protocol].get(attribute, None)

        if self.parent.debug_plugin:
            if os.path.isfile(self.parent.debug_plugin) or\
                'debug_plugin' in device.custom:
                # If it is a file (single debug plugin case)
                # or its just a path and debug pligun is defined under
                # device.custom
                abstract = Lookup.from_device(device,
                                              packages={'sdk':sdk})
                ha = abstract.sdk.libs.abstracted_libs.ha.HA(
                    device=device, filetransfer=device.filetransfer)
                device.debug_plugin = ha.get_debug_plugin(self.parent.debug_plugin)
            else:
                # Case of multiple debug plugins but current device
                # has no debug_plugin defined under device.custom
                continue


def check_config(self, testbed, testscript, steps, devices=None, include_os=None,
                 exclude_os=None, include_devices=None, exclude_devices=None):

    '''Take snapshot of configuration for each devices'''

    log.info("Take a snapshot of the configuration of each device. In the "
             "Common Cleanup, the same process will be done to make sure no "
             "extra configuration remains on the devices")

    log.info('For more information visit Genie check_config section '
             '{url}/harness/user/gettingstarted.html#check-config'
             .format(url=self.parent.url))

    if exclude_devices:
        log.info("Excluded devices by exclude_devices: {exclude_devices}".format(
            exclude_devices=exclude_devices))

    if include_devices:
        log.info("Included devices by include_devices: {include_devices}".format(
            include_devices=include_devices))

    if include_os:
        log.info("Included OS by include_os: {include_os}"
                 .format(include_os=include_os))

    if exclude_os:
        log.info("Excluded OS by exclude_os: {exclude_os}"
                 .format(exclude_os=exclude_os))

    if not None in [exclude_devices, include_devices]:
        if set(exclude_devices).intersection(include_devices):
            raise ValueError("Same device is specified in both include and exclude devices filter. "
                             "Use only one filter. Both are not allowed")

    if not None in [exclude_os, include_os]:
        if set(exclude_os).intersection(include_os):
            raise ValueError("Same os is specified in both include and exclude os filter. "
                             "Use only one filter. Both are not allowed")

    accepted_devices = []
    accepted_devices_name = []
    # Create a dictionary to save the steps output for printing the summary
    # at the end
    self.check_config_summary = {}

    device_list = []

    # Uniform them as devices object (as could be name/alias)
    if devices:
        if "all" not in devices.keys():
            for device in devices:
                if device in testbed.devices:
                    dev = testbed.devices[device]
                    accepted_devices.append(dev)

                    if devices[device]:
                        if 'file_name' in devices[device]:
                            dev.file_name = devices[device]['file_name']
                    else:
                        self.errored("Issue while taking configuration, file name is "
                                     "missing for the device {}".format(device))
                        return

                    if 'file_location' in devices[device]:
                        dev.file_location = devices[device]['file_location']

                    # Useful for messages
                    accepted_devices_name.append(dev.name)
                else:
                    raise ValueError("'{dev}' is not a valid device"
                                     .format(dev=device))


    for dev in sorted(self.parent.mapping_data['devices']):

        if exclude_devices and dev in exclude_devices:
            continue

        if include_devices and dev not in include_devices:
            continue

        # Find device from testbed yaml file based on device name
        device = testbed.devices[dev]

        if include_os and device.os not in include_os:
            continue

        if exclude_os and device.os in exclude_os:
            continue

        if dev in testbed.devices:
            device_list.append(testbed.devices[dev])

        if devices:
            if "all" not in devices.keys() and device not in accepted_devices:
                device_list.remove(device)
                summary_msg = "Skipped configuration check, "\
                              "device is not in the provided devices list: "\
                              "'{devices}'".\
                              format(devices=', '.join(accepted_devices_name))
                self.check_config_summary[dev] = summary_msg


            #To add file_name when "all" is given:
            if "all" in devices.keys():
                for name, dev_obj in testbed.devices.items():
                    device = testbed.devices[name]
                    if devices['all']:
                        if 'file_name' in devices['all']:
                            device.file_name = devices['all']['file_name']
                    else:
                        self.errored("Issue while taking configuration file name is "
                                     "missing for all the devices")
                        return

                    if 'file_location' in devices['all']:
                        device.file_location = devices['all']['file_location']

        if device in device_list and device.type in EXCLUDED_DEVICE_TYPES:
            device_list.remove(device)
            summary_msg = "Skipped configuration check, subsection "\
                          "is not supported for TGN devices"
            self.check_config_summary[dev] = summary_msg


    configs = {}
    config_snapshot_failed = False
    async_conf_snapshot_output = pcall(asynchronous_configure_snapshot,
        device=tuple(device_list),
        ckwargs={'configs':configs,
        'section': self.parent
        })

    for item in async_conf_snapshot_output:
        for dev in item.keys():
            if 'config_snapshot_failed' in item[dev]:
                self.check_config_summary[dev] = [item[dev]['summary_msg']]
                config_snapshot_failed = True
            else:
                self.check_config_summary[dev] = item[dev]['summary_msg']
                configs[dev] = item[dev]['config']

    # Take config which was applied on the device, if any
    testscript.parameters['configs'] = configs

    # Create Summary
    summary = Summary(title='Check config Summary', width=150)

    for dev, msg in self.check_config_summary.items():
        if isinstance(msg, list):
            summary.summarize_section(message=msg[0], device=dev,
                level='error')
        else:
            summary.summarize_section(message=msg, device=dev)

    summary.print()
    log.info("\n")

    if config_snapshot_failed:
        self.errored("Issue while taking configuration snapshot on one of "
                     "the devices, check summary table for details")

def initialize_traffic_tcl(self, testbed, steps):

    log.info("Starts the traffic")
    log.info('For more information visit Genie traffic section '
             '{url}/userguide/harness/user/traffic.html'
             .format(url=self.parent.url))

    if not self.parent.tgn_keys['tgn_enable']:
        self.skipped("Traffic not enabled; 'tgn_enable' is set to False")

    tgn_device = None

    for dev in testbed.find_devices(type='tgn'):

        # Set TGN device
        tgn_device = dev

        # Check if device is found in mapping context
        if not hasattr(self.parent, 'mapping_data') or \
           tgn_device.name not in self.parent.mapping_data['devices']:
            self.skipped("TGN '{}' information not found in mapping datafile".\
                         format(tgn_device.name))

        # Get TGN mapping context info
        alias = self.parent.mapping_data['devices'][tgn_device.name]['context']
        via = self.parent.mapping_data['devices'][tgn_device.name]\
              ['mapping'][alias]

        # Check if tgn_keys exists
        if not hasattr(self.parent, 'tgn_keys'):
            self.skipped("TGN arguments not configured.")

        # Set all parameters provided by the user to the device object.
        for key in self.parent.tgn_keys:
            setattr(tgn_device, key, self.parent.tgn_keys[key])

        # Check if TGN has been previously configured and user only wants to
        # connect to TGN and not load configuration file
        if tgn_device.tgn_skip_configuration:
            configuration = None
            log.info(banner("User has elected to skip loading configuration "
                            "on TGN '{d}'.\nContinuing execution assuming that "
                            "TGN '{d}' has been correctly\nconfigured by user "
                            "prior to launching Genie.".\
                            format(d=tgn_device.name)))
            step_message = "Connect to TGN '{}'".format(tgn_device.name)
        else:
            # Check if config file exists
            if not hasattr(self.parent, 'config_data') or \
               not self.parent.config_data:
                self.skipped("Device configuration datafile not provided.")

            # Check if TGN information provided in config datafile
            if tgn_device.name not in self.parent.config_data['devices']:
                self.skipped("TGN '{}' information not found in configuration "
                             "datafile".format(tgn_device.name))

            # Get configuration file for TGN device
            configurations = self.parent.config_data['devices'][tgn_device.name]
            if len(configurations) != 1:
                self.failed("Multiple configuration files found for TGN '{}'. "
                            "Only single configuration file loading supported.".\
                            format(tgn_device.name))
            num = list(configurations)[0]
            configuration = self.parent.config_data['devices']\
                            [tgn_device.name][num]['config']
            step_message = "Connect to TGN '{}' and load configuration".\
                            format(tgn_device.name)

        #####################################################
        #                   ENABLE TRAFFIC                  #
        #####################################################

        # Connect to TGN and load configuration
        with steps.start(step_message) as step:
            try:
                if configuration:
                    tgn_device.connect(via=via, alias=alias, config=configuration)
                else:
                    tgn_device.connect(via=via, alias=alias)
                # Set connection alias
                connection_alias = getattr(tgn_device, alias)
                step.passed("Successfully connected to TGN {}".\
                            format(tgn_device.name))
            except GenieTgnError as e:
                step.failed("Aborting subsection: Unable to connect to TGN "
                            "'{d}'".format(d=tgn_device.name,e=e),
                            from_exception=e)

        # Learn the traffic configuration
        with steps.start("Learn traffic configuration on TGN '{}'".\
                         format(tgn_device.name)) as step:
            try:
                connection_alias.learn_traffic_streams()
                step.passed("Successfully learnt traffic configuration "
                            "on TGN {}".format(tgn_device.name))
            except GenieTgnError as e:
                step.failed("Aborting subsection: Unable to learn traffic "
                            "configuration on TGN '{d}'".\
                            format(d=tgn_device.name, e=e), from_exception=e)

        # Start routing engine
        with steps.start("Start routing engine on TGN '{}'".\
                         format(tgn_device.name)) as step:
            try:
                connection_alias.start_routing()
                step.passed("Successfully started routing engine on TGN "
                            "'{}'".format(tgn_device.name))
            except GenieTgnError as e:
                step.failed("Aborting subsection: Unable to start routing "
                            "engine on TGN '{d}'".\
                            format(d=tgn_device.name, e=e), from_exception=e)

        # Wait after starting routing engine
        log.info("Waiting {} seconds after starting TGN routing engine.".\
                 format(tgn_device.tgn_routing_threshold))
        time.sleep(tgn_device.tgn_routing_threshold)

        # Initialize TGN in preparation for starting traffic
        with steps.start("Initialize TGN ARP, ND, PIM on TGN '{}'".\
                         format(tgn_device.name)) as step:
            try:
                connection_alias.initialize_tgn_ArpNdPim()
                step.passed("Successfully initialized ARP, ND, PIM on TGN "
                            "'{}'".format(tgn_device.name))
            except GenieTgnError as e:
                step.passx("Warning - Unable to initialize ARP, ND, PIM on TGN "
                           "{d} - continuing execution".\
                           format(d=tgn_device.name, e=e), from_exception=e)

        # Start traffic
        with steps.start("Start TGN traffic on TGN '{}'".\
                         format(tgn_device.name)) as step:
            try:
                connection_alias.start_traffic()
                step.passed("Successfully started traffic on TGN '{}'".\
                            format(tgn_device.name))
            except GenieTgnError as e:
                step.failed("Aborting subsection: Unable to start traffic on "
                            "TGN '{d}'".format(d=tgn_device.name, e=e),
                            from_exception=e)

        # Wait for traffic to establish
        log.info("Waiting {} seconds after starting traffic for steady state "
                 "to be reached".format(tgn_device.tgn_first_sample_threshold))
        time.sleep(tgn_device.tgn_first_sample_threshold)

        # Get current packet rate to validate traffic is flowing
        with steps.start("Collecting first sample of traffic rates "
                         "on TGN '{}'".format(tgn_device.name)) as step:
            try:
                connection_alias.get_current_packet_rate(first_sample=True)
                step.passed("Successfully collected first sample of traffic "
                            "rates on TGN '{}'".format(tgn_device.name))
            except GenieTgnError as e:
                step.failed("Aborting subsection: Unable to colled first "
                            "sample of traffic rates on TGN '{d}'".\
                            format(d=tgn_device.name, e=e),
                            from_exception=e)

        #####################################################
        #                   PROFILE TRAFFIC                 #
        #####################################################

        # Collect reference traffic rates
        with steps.start("Collect reference traffic rates on TGN '{}'".\
                         format(tgn_device.name)) as step:
            try:
                connection_alias.get_reference_packet_rate()
                step.passed("Successfully collected reference traffic rates on "
                            "TGN '{}'".format(tgn_device.name))
            except GenieTgnError as e:
                step.failed("Aborting subsection: Unable to collect reference "
                            "traffic rates on TGN '{d}'".\
                            format(d=tgn_device.name, e=e), from_exception=e)

        # Validate Traffic loss (if any) is within expected percentage
        with steps.start("Validate traffic loss (if any) is within expected "
                         "tolerance: {num}% on TGN '{d}'".format(
                         num=tgn_device.tgn_traffic_loss_tolerance_percentage,
                         d=tgn_device.name)) as step:
            try:
                connection_alias.check_traffic_loss()
                step.passed("Successfully validated traffic loss is within "
                            "expected tolerance on TGN '{}'".\
                            format(tgn_device.name))
            except GenieTgnError as e:
                step.failed("Aborting subsection: Unexpected traffic loss is "
                            "observed on TGN '{d}'".\
                            format(d=tgn_device.name, e=e), from_exception=e)

    if not tgn_device:
        self.skipped("No traffic generator devices has been found in the "
                     "testbed.")


def initialize_traffic(self, testbed, steps):
    '''Connect to traffic generator device, load configuration, start protocols and traffic'''

    log.info("Connect to traffic generator device and configure/start traffic")
    log.info('For more information visit Genie traffic section '
             '{url}/userguide/harness/user/traffic.html'
             .format(url=self.parent.url))

    tgn_devices = testbed.find_devices(type='tgn')
    if not tgn_devices:
        self.skipped("Traffic generator devices not found in testbed YAML")

    for dev in tgn_devices:

        if dev.name not in self.parent.mapping_data['devices']:
            self.skipped("Traffic generator devices not specified in --devices")

        # -----------------------------------
        # Connect to traffic generator device
        # -----------------------------------
        step_message = "Connect to traffic generator device '{}'".format(dev.name)
        with steps.start(step_message) as step:
            try:
                # Connect to TGN
                dev.connect(via='tgn')
            except GenieTgnError as e:
                step.failed(from_exception=e, reason=\
                    "Error while connecting to traffic generator device '{}'".\
                    format(dev.name))
            step.passed("Successfully connected to traffic generator device '{}'".\
                        format(dev.name))

        # ---------------------------------------------------------------
        # Load configuration and assign ports on traffic generator device
        # ---------------------------------------------------------------
        step_message = "Load configuration and assign ports on traffic generator device '{}'".\
                       format(dev.name)
        with steps.start(step_message) as step:

            if self.parent.tgn_disable_load_configuration:
                step.passed("SKIP: 'tgn_disable_load_configuration' set to True.")
            else:
                # Check if user has provided config_datafile.yaml to gRun
                if not hasattr(self.parent, 'config_data') or\
                    not self.parent.config_data:
                    self.skipped("Argument 'config_datafile' is not provided in"
                                 " the jobfile or the command line arguments.")

                # Check if TGN information provided in config_datafile.yaml
                if dev.name not in self.parent.config_data['devices']:
                    self.skipped("Device '{}' configuration information not "
                                 "provided in config_datafile".format(dev.name))

                # Get configuration information for TGN device in config_datafile
                configurations = self.parent.config_data['devices']\
                                    [dev.name]

                # Check if multiple configuration files given for TGN device
                if len(configurations) != 1:
                    self.failed("Multiple configuration files found for device"
                                " '{}'\nOnly single configuration file loading"
                                " is supported".format(dev.name))

                # Get configuration file for TGN device
                config_file = self.parent.config_data['devices']\
                                [dev.name][list(configurations)[0]]\
                                ['config']

                # Load configuration
                try:
                    dev.load_configuration(configuration=config_file,
                            wait_time=self.parent.tgn_load_configuration_time)
                except GenieTgnError as e:
                    step.failed(from_exception=e, reason=\
                        "Error while loading static configuration file onto "
                        "traffic generator device '{d}'".\
                        format(f=config_file, d=dev.name))
                else:
                    log.info("Successfully loaded static configuration file onto"
                             " traffic generator device '{}'".format(dev.name))

            if self.parent.tgn_disable_assign_ports:
                step.passed("SKIP: 'tgn_disable_assign_ports' set to True.")
            else:
                # Assigning physical ports to virtual ports
                try:
                    dev.assign_ixia_ports(wait_time=self.parent.tgn_assign_ports_time)
                except GenieTgnError as e:
                    step.failed(from_exception=e, reason=\
                        "Error while assigning physical ports to virtual ports "
                        "in configuration on traffic generator device '{}'".\
                        format(dev.name))
                else:
                    log.info("Successfully assigned physical ports to virtual "
                            "ports in configuration on traffic generator "
                            "device '{}'".format(dev.name))

                step.passed("Successfully loaded static configuration file onto"
                            " traffic generator device '{}' and assigned ports".\
                            format(dev.name))

        # -------------------------------------------
        # Start protocols on traffic generator device
        # -------------------------------------------
        step_message = "Start protocols on traffic generator device '{}'".\
                        format(dev.name)
        with steps.start(step_message) as step:
            if self.parent.tgn_disable_start_protocols:
                step.passed("SKIP: 'tgn_disable_start_protocols' set to True.")
            else:
                try:
                    # Start all protocols
                    dev.start_all_protocols(wait_time=self.parent.tgn_protocols_convergence_time)
                except GenieTgnError as e:
                    step.failed(from_exception=e, reason=\
                        "Error while starting all protocols on traffic generator"
                        " device '{}'".format(dev.name))
                step.passed("Successfully started all protocols on traffic "
                            "generator device '{}'".format(dev.name))

        # ------------------------------------------------------
        # Regenerate traffic streams on traffic generator device
        # ------------------------------------------------------
        step_message = "Regenerate traffic streams on traffic generator device '{}'".\
                        format(dev.name)
        with steps.start(step_message) as step:
            if self.parent.tgn_disable_regenerate_traffic:
                step.passed("SKIP: 'tgn_disable_regenerate_traffic' set to True.")
            else:
                try:
                    # Get a list of all traffic streams configured
                    traffic_items = dev.get_traffic_stream_names()
                except GenieTgnError as e:
                    step.failed(from_exception=e, reason=\
                                "Error while getting all traffic streams "
                                "configured on traffic generator device '{}'".\
                                format(dev.name))
                try:
                    # Regenerate all the traffic stream
                    dev.generate_traffic_streams(traffic_streams=traffic_items,
                        wait_time=self.parent.tgn_regenerate_traffic_time)
                except GenieTgnError as e:
                    step.failed(from_exception=e, reason=\
                                "Error while regenerating traffic items on "
                                "traffic generator device '{}'".\
                                format(dev.name))
                step.passed("Successfully regenerated all traffic streams on "
                            "traffic generator device '{}'".format(dev.name))

        # -----------------------------------------------
        # Apply L2/L3 traffic on traffic generator device
        # -----------------------------------------------
        step_message = "Apply L2/L3 traffic on traffic generator device '{}'".\
                        format(dev.name)
        with steps.start(step_message) as step:
            if self.parent.tgn_disable_apply_traffic:
                step.passed("SKIP: 'tgn_disable_apply_traffic' set to True.")
            else:
                try:
                    dev.apply_traffic(wait_time=self.parent.tgn_apply_traffic_time)
                except GenieTgnError as e:
                    step.failed(from_exception=e, reason=\
                        "Error while applying L2/L3 traffic on traffic generator"
                        " device '{}'".format(dev.name))
                step.passed("Successfully applied L2/L3 traffic on traffic "
                            "generator device '{}'".format(dev.name))

        # ------------------------------------------------
        # Send ARP/NS packet from traffic generator device
        # ------------------------------------------------
        step_message = "Send ARP/NS packet from traffic generator device '{}'".\
                        format(dev.name)
        with steps.start(step_message) as step:
            arp_pass = False ; ns_pass = False

            # Send ARP
            if self.parent.tgn_disable_send_arp:
                arp_pass = True
                log.info("SKIP: 'tgn_disable_send_arp' set to True.")
            else:
                try:
                    dev.send_arp(wait_time=self.parent.tgn_arp_wait_time)
                except GenieTgnError as e:
                    step.failed(from_exception=e, reason=\
                        "Error while sending ARP from traffic generator device"
                        " '{}'".format(dev.name))
                else:
                    arp_pass = True
                    log.info("Successfully sent ARP from traffic generator "
                             "device '{}'".format(dev.name))

            # Send NS
            if self.parent.tgn_disable_send_ns:
                ns_pass = True
                log.info("SKIP: 'tgn_disable_send_ns' set to True.")
            else:
                try:
                    dev.send_ns(wait_time=self.parent.tgn_ns_wait_time)
                except GenieTgnError as e:
                    step.failed(from_exception=e, reason=\
                        "Error while sending NS packet from traffic generator "
                        "device '{}'".format(dev.name))
                else:
                    ns_pass = True
                    log.info("Successfully sent NS packet from traffic generator "
                             "device '{}'".format(dev.name))

            # Set result for this step
            if arp_pass and ns_pass:
                step.passed("Successfully sent ARP/NS packet from traffic "
                            "generator device '{}".format(dev.name))
            else:
                step.failed("Error while sending ARP/NS packet from traffic "
                            "generator device '{}".format(dev.name))

        # -----------------------------------------------
        # Start L2/L3 traffic on traffic generator device
        # -----------------------------------------------
        step_message = "Start L2/L3 traffic on traffic generator device '{}'".\
                        format(dev.name)
        with steps.start(step_message) as step:
            if self.parent.tgn_disable_start_traffic:
                step.passed("SKIP: 'tgn_disable_start_traffic' set to True.")
            else:
                try:
                    dev.start_traffic(wait_time=self.parent.tgn_steady_state_convergence_time)
                except GenieTgnError as e:
                    step.failed(from_exception=e, reason=\
                        "Unable to start L2/L3 traffic on traffic generator "
                        "device '{}'".format(dev.name))
                step.passed("Successfully started L2/L3 traffic on traffic "
                            "generator device '{}'".format(dev.name))

        # ------------------------------------------------------------------------
        # Clear all traffic, port, protocol statistics on traffic generator device
        # ------------------------------------------------------------------------
        step_message = "Clear all traffic, port, protocol statistics on traffic generator device '{}'".\
                        format(dev.name)
        with steps.start(step_message) as step:
            if self.parent.tgn_disable_clear_statistics:
                step.passed("SKIP: 'tgn_disable_clear_statistics' set to True.")
            else:
                try:
                    dev.clear_statistics(wait_time=self.parent.tgn_clear_stats_time)
                except GenieTgnError as e:
                    step.failed(from_exception=e, reason=\
                        "Error while clear statistics on traffic generator "
                        "device '{}'".format(dev.name))
                step.passed("Successfully cleared statistics on traffic "
                            "generator device '{}'".format(dev.name))

        # --------------------------------------------------------------------
        # Create custom traffic items view 'GENIE' on traffic generator device
        # --------------------------------------------------------------------
        step_message = "Create custom traffic items view 'GENIE' on traffic generator '{}'".\
                        format(dev.name)
        with steps.start(step_message) as step:
            try:
                dev.create_genie_statistics_view(
                    view_create_interval=self.parent.tgn_view_create_interval,
                    view_create_iteration=self.parent.tgn_view_create_iteration,
                    disable_tracking=self.parent.tgn_disable_tracking_filter,
                    disable_port_pair=self.parent.tgn_disable_port_pair_filter)
            except GenieTgnError as e:
                step.failed(from_exception=e, reason=\
                    "Unable to created custom traffic items view 'GENIE' on "
                    "traffic generator device '{}'".format(dev.name))
            step.passed("Successfully created custom traffic items view 'GENIE'"
                        "on traffic generator device '{}'".format(dev.name))

        # ------------------------------------------------------
        # Verify traffic loss (if any) within expected tolerance
        # ------------------------------------------------------
        step_message = "Verify traffic loss (if any) within expected tolerance on traffic generator device '{}'".\
                        format(dev.name)
        with steps.start(step_message) as step:
            if self.parent.tgn_disable_check_traffic_loss:
                step.passed("SKIP: 'tgn_disable_check_traffic_loss' set to True.")
            else:
                log.info(banner("Checking for traffic outage/loss on all configured traffic streams"))
                # Check if user provided file containing traffic stream data
                streams_dict = {}
                if self.parent.tgn_traffic_streams_data:
                    streams_dict = unpickle_stream_data(
                                    file=self.parent.tgn_traffic_streams_data,
                                    copy=True, copy_file='initialize_traffic_stream_data')
                    # Print to logs
                    log.info("User has provided outage/tolerance values for the following streams:")
                    for stream in streams_dict['traffic_streams']:
                        log.info("-> {}".format(stream))
                    # Check if streams passed in are valid
                    for stream in streams_dict['traffic_streams']:
                        if stream not in dev.get_traffic_stream_names():
                            log.error("WARNING: Traffic item '{}' was not found "
                                      "in configuration but provided in traffic "
                                      "streams YAML".format(stream))
                # Check for traffic loss
                try:
                    dev.check_traffic_loss(max_outage=self.parent.tgn_traffic_outage_tolerance,
                                           loss_tolerance=self.parent.tgn_traffic_loss_tolerance,
                                           rate_tolerance=self.parent.tgn_traffic_rate_tolerance,
                                           check_iteration=self.parent.tgn_stabilization_iteration,
                                           check_interval=self.parent.tgn_stabilization_interval,
                                           traffic_streams=self.parent.tgn_check_traffic_streams,
                                           outage_dict=streams_dict,
                                           disable_port_pair=self.parent.tgn_disable_port_pair_filter,)
                except GenieTgnError as e:
                    log.error(e)
                    step.failed(from_exception=e, reason="Traffic outage/loss "
                                "observed for configured traffic streams.")
                else:
                    step.passed("Traffic outage/loss is within expected "
                                "thresholds for all traffic streams.")


def profile_traffic(self, testbed, steps):
    '''Connect to traffic generator device, create traffic profile, compare to golden profile'''

    log.info("Create profile of traffic streams and compare to golden profile")
    log.info('For more information visit Genie traffic section '
             '{url}/userguide/harness/user/traffic.html'
             .format(url=self.parent.url))

    tgn_devices = testbed.find_devices(type='tgn')

    if not tgn_devices:
        self.skipped("Traffic generator devices not found in testbed YAML")

    for dev in tgn_devices:

        if dev.name not in self.parent.mapping_data['devices']:
            self.skipped("Traffic generator devices not specified in --devices")

        # -----------------------------------
        # Connect to traffic generator device
        # -----------------------------------
        step_message = "Connect to traffic generator device '{}'".\
                        format(dev.name)
        with steps.start(step_message) as step:
            try:
                # Connect to TGN
                dev.connect(via='tgn')
            except GenieTgnError as e:
                step.failed(from_exception=e, reason=\
                    "Error while connecting to traffic generator device '{}'".\
                    format(dev.name))
            # Set TGN connection class
            #self.tgn_conn = getattr(dev, dev.context)
            step.passed("Successfully connected to traffic generator device "
                        "'{}'".format(dev.name))

        # ---------------------------------------------------------------------------------
        # Create and save traffic profile of configured streams on traffic generator device
        # ---------------------------------------------------------------------------------
        step_message = "Create and save traffic profile of configured streams on traffic generator device '{}'".\
                        format(dev.name)
        with steps.start(step_message) as step:
            try:
                tgn_profile = dev.create_traffic_streams_table(
                        set_golden=True,
                        clear_stats=self.parent.tgn_disable_profile_clear_stats,
                        clear_stats_time=self.parent.tgn_clear_stats_time)
            except GenieTgnError as e:
                step.failed(from_exception=e, reason=\
                            "Error while creating snapshot profile of traffic "
                            "stream configured on traffic generator device '{}'".\
                            format(dev.name))
            log.info("Successfully created snapshot profile of traffic streams "
                     "configured on traffic generator device '{}'".\
                     format(dev.name))

            # Save traffic profile to logs
            try:
                tgn_profile_file = pickle_traffic(tgn_profile=tgn_profile,
                                    tgn_profile_name='golden_traffic_profile')
            except Exception as e:
                step.failed(from_exception=e, reason=\
                    "Error while saving golden traffic profile to runtime logs")
            step.passed("Saved traffic profile to runtime logs")

        # --------------------------------------------------------------------------------------
        # Compare current traffic profile to golden traffic profile for traffic generator device
        # --------------------------------------------------------------------------------------
        step_message = "Compare current traffic profile to golden traffic profile for traffic generator device '{}".\
                        format(dev.name)
        with steps.start(step_message) as step:
            if self.parent.tgn_golden_profile:
                # Extract TGN golden profile
                log.info(banner("User Provided Golden Traffic Profile"))
                try:
                    unpicked_tgn_profile = unpickle_traffic(self.parent.tgn_golden_profile)
                except Exception as e:
                    step.failed(from_exception=e, reason=\
                        "Error while unpacking golden traffic profile into "
                        "table format")
                log.info(unpicked_tgn_profile)

                # Compare current traffic profile to golden profile
                try:
                    dev.compare_traffic_profile(profile1=tgn_profile,
                                                profile2=unpicked_tgn_profile,
                                                loss_tolerance=self.parent.tgn_profile_traffic_loss_tolerance,
                                                rate_tolerance=self.parent.tgn_profile_rate_loss_tolerance)
                except GenieTgnError as e:
                    log.error(e)
                    step.failed(reason="Unexpected differences while comparing "
                                "current traffic to golden traffic profile")
                step.passed("Verified key, values between current traffic "
                            "profile and golden traffic profile match")
            else:
                self.passed("SKIP: 'tgn_golden_profile' not provided.")


# subsections for common_cleanup
def check_post_config(self, testbed, testscript, steps, configs):
    '''Verify the configuration for the devices has not changed'''
    log.info("Verify if the devices' configuration has been modified within "
             "the run. A new snapshot is taken and is compared with the one "
             "taken in Common Setup")
    log.info("For more information visit Genie check_config section "
             "{url}/harness/user/gettingstarted.html#check-config"
             .format(url=self.parent.url))

    if not configs:
        self.skipped("No initial configuration was taken in Common Setup")

    device_list = []

    # Create summary table
    summary = Summary(title='Check Post configuration Summary', width=150)

    # compare configurations on the devices which has collect show run in common_setup
    for dev in sorted(configs.keys()):
        device = testbed.devices[dev]
        device_list.append(device)

        if device.type in EXCLUDED_DEVICE_TYPES:
            device_list.remove(device)
            summary_msg = "Verify configuration snapshot is not "\
                          "supported for TGN device"
            summary.summarize_section(message=summary_msg,
                                      device=dev)

    post_configs = {}
    passx_result = False

    async_conf_snapshot_output = pcall(asynchronous_configure_snapshot,
                                       device=tuple(device_list),
                                       ckwargs={'configs':post_configs})

    for item in async_conf_snapshot_output:
        for dev in item.keys():
            if 'config_snapshot_failed' in item[dev]:
                passx_result = True
                summary.summarize_section(message=item[dev]['summary_msg'],
                                          device=dev, level='error')
            else:
                post_configs[dev] = item[dev]['config']

    testscript.parameters['post_configs'] = post_configs

    failed = []
    passed = []
    for device, c in configs.items():
        if device not in post_configs:
            # A device disapeared?
            if passx_result:
                msg = "Configuration snapshot was taken in Common Setup "\
                      "but failed while taking in the Common Cleanup"
            else:
                msg = "Configuration snapshot was taken in Common Setup "\
                      "but no snapshot was taken in the Common Cleanup"
            summary.summarize_section(message=msg,
                device=device, level='error')
            continue

        # Default
        exclude = ['device', 'maker', 'diff_ignore', 'callables',
                   r'(Current configuration.*)', r'(.*Load for.*)', r'(.*[t|T]ime source.*)',
                   r'(^[Wed|Thu|Fri|Sat|Sun|Mon|Tue]+ +[Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec]+ +\d{1,2} +\d{1,2}:\d{1,2}:\d{1,2}[\.]\d{1,3} +[A-Z]{3})']
        # Support regex, but need to start with ( )
        # Might need to be dynamic set at a later date.
        if 'exclude_config_check' in self.parent.config_data:
            exclude.extend(self.parent.config_data['exclude_config_check'])

        # Find the diff
        if isinstance(c, str) or isinstance(post_configs[device], str):
            log.warning("Could not diff configuration for device "
                        "'{d}'".format(d=device))
            continue

        diff = Diff(c, post_configs[device], exclude=exclude)
        try:
            diff.findDiff()
        except Exception:
            log.exception("Could not diff configuration for device "
                          "'{d}'".format(d=device))
            # It can happen Diff cannot diff correctly,  report it; but
            # Keep going so we can see all the diffs
            continue

        if len(diff.diffs):
            failed.append((device, diff))
        else:
            passed.append(device)

    for device, diff in sorted(failed):
        summary.summarize_profile(device=device, diff=diff, PTS=False)

    for device in sorted(passed):
        summary.summarize_profile(device=device, PTS=False)

    if failed:
        summary.print()
        log.info("\n")
        self.failed('Comparison of Configuration in Common Setup and Common '
                    'Cleanup has been modified.  Check the summary table for '
                    'more details')

    # All snapshots comparison passed
    summary.print()
    log.info("\n")

    if passx_result:
        self.passx("Post configuration snapshot is missing for one of "
                   "the devices but a snapshot was taken in the "
                   "Common Setup, Check summary table for details")


# subsections for common_cleanup
def stop_traffic_tcl(self, testbed, steps):

    log.info("Stops the traffic")
    log.info('For more information visit Genie traffic section '
             '{url}/userguide/harness/user/traffic.html'
             .format(url=self.parent.url))

    tgn_device = None

    for dev in testbed.find_devices(type='tgn'):

        # Set TGN device
        tgn_device = dev

        # Check if device is found in mapping context
        if not hasattr(self.parent, 'mapping_data') or \
           tgn_device.name not in self.parent.mapping_data['devices']:
            self.skipped("TGN '{}' information not found in mapping datafile".\
                         format(tgn_device.name))

        # Check if TGN is connected
        if not tgn_device.is_connected():
            self.skipped("TGN '{}' not connected.".format(tgn_device.name))

        # Get TGN mapping context info
        alias = self.parent.mapping_data['devices'][dev.name]['context']

        # Set connection alias
        connection_alias = getattr(tgn_device, alias)

        if self.parent.tgn_keys['tgn_disable_traffic_post_execution']:
            # Stop the traffic
            log.info("Stopping traffic")
            try:
                connection_alias.stop_traffic()
            except GenieTgnError as e:
                self.failed("Unable to stop traffic after Genie execution.",
                            from_exception=e)
        else:
            self.skipped("User has elected *NOT* to stop traffic after Genie "
                         "execution completes.")

    if not tgn_device:
        self.skipped("No traffic generator devices has been found in the "
                     "testbed.")


# subsections for common_cleanup
def stop_traffic(self, testbed, steps):

    log.info("Stop protocols and traffic on traffic generator")
    log.info('For more information visit Genie traffic section '
             '{url}/userguide/harness/user/traffic.html'
             .format(url=self.parent.url))

    tgn_devices = testbed.find_devices(type='tgn')

    if not tgn_devices:
        self.skipped("Traffic generator devices not found in testbed YAML")

    for dev in tgn_devices:

        if dev.name not in self.parent.mapping_data['devices']:
            self.skipped("Traffic generator devices not specified in --devices")

        # -----------------------------------
        # Connect to traffic generator device
        # -----------------------------------
        step_message = "Connect to traffic generator device '{}'".format(dev.name)
        with steps.start(step_message) as step:
            try:
                # Connect to TGN
                dev.connect(via='tgn')
            except GenieTgnError as e:
                step.failed(from_exception=e, reason=\
                    "Error while connecting to traffic generator device '{}'".\
                    format(dev.name))
            step.passed("Successfully connected to traffic generator device '{}'".\
                        format(dev.name))

        # ------------------------------------------
        # Stop protocols on traffic generator device
        # ------------------------------------------
        step_message = "Stop protocols on traffic generator device '{}'".\
                        format(dev.name)
        with steps.start(step_message) as step:
            try:
                dev.stop_all_protocols(wait_time=self.parent.tgn_stop_protocols_time)
            except GenieTgnError as e:
                    step.failed(from_exception=e, reason=\
                        "Error while stoping all protocols on traffic generator"
                        " device '{}'".format(dev.name))
            step.passed("Successfully stopped all protocols on traffic generator"
                        " device '{}'".format(dev.name))

        # ----------------------------------------------
        # Stop L2/L3 traffic on traffic generator device
        # ----------------------------------------------
        step_message = "Stop L2/L3 traffic on traffic generator device '{}'".\
                        format(dev.name)
        with steps.start(step_message) as step:
            try:
               dev.stop_traffic(wait_time=self.parent.tgn_stop_traffic_time)
            except GenieTgnError as e:
                    step.failed(from_exception=e, reason=\
                        "Unable to stop L2/L3 traffic on traffic generator "
                        "device '{}'".format(dev.name))
            step.passed("Successfully stopped L2/L3 traffic on traffic generator"
                        " device '{}'".format(dev.name))


        # ------------------------------------------------
        # Remove configuration on traffic generator device
        # ------------------------------------------------
        if self.parent.tgn_remove_configuration:
            step_message = "Remove configuration on traffic generator device '{}'".\
                            format(dev.name)
            with steps.start(step_message) as step:
                try:
                    dev.remove_configuration(
                            wait_time=self.parent.tgn_remove_configuration_time)
                except GenieTgnError as e:
                    step.failed(from_exception=e, reason=\
                        "Unable to remove configuration on traffic generator "
                        "device '{}'".format(dev.name))
                step.passed("Successfully removed configuration on traffic "
                            "generator device '{}'".format(dev.name))

class ProfileSystem(object):

    def ProfileSystem(self, feature, container, testscript, testbed, steps):
        if isinstance(self, CommonSetup):
            log.info("Take a snapshot of '{f}' to be compared within the Common"
                     " Cleanup This verify the feature stability after "
                     "executing all the triggers"
                     .format(f=feature))
        elif isinstance(self, CommonCleanup):
            log.info("Take a snapshot of '{f}' and compare it with the snapshot"
                     " taken in Common Setup. This verify the feature "
                     "stability after executing all the triggers "
                     .format(f=feature))

        log.info("'pts' data file controls the features to be learnt and "
            "on which devices, Check the provided 'pts' data file")

        log.info('For more information visit Genie PTS section '
                 '{url}/harness/user/gettingstarted.html#pts'
                 .format(url=self.parent.url))

        # Initialize 'pts' dictionary for adding the learnt objects later
        testscript.parameters.setdefault('pts', {}).setdefault(feature, {})

        # A container to keep track of the features learnt to pickle
        # 'only' after learning all
        if 'learnt_dict' not in testscript.parameters:
            testscript.parameters['learnt_dict'] = {}

        # Learn feature
        try:
            learnt_output = Profile.learn_features(
                features=[feature],
                pts_data=self.parent.pts_data,
                current_instance= self.uid,
                testbed=testbed,
                testscript=testscript)
        except KeyError:
            # Error as user need to add to pts_data
            self.errored("'{f}' does not exists in pts_data "
                       "file".format(f=feature))
        except Exception as e:
            self.errored("Issue while profiling '{f}' feature"
                         .format(f=feature), from_exception=e)

        # TODO: To fix - always passing now
        testscript.parameters['pts'] = learnt_output

        # If needed, do Golden compare
        if isinstance(self, CommonSetup):

            # If Golden, then compare here!
            if hasattr(self.parent, 'pts_golden_config') and\
               self.parent.pts_golden_config:

                # Check if provided golden_pts is a file or not, if not a file
                # then will get the golden_pts file from the branch directory
                if not os.path.isfile(testscript.pts_golden_config) and \
                    'BRANCH' in os.environ:
                    loc = '{branch}/golden_pts'.format(
                        branch=os.environ['BRANCH'])
                    self.parent.pts_golden_config = os.path.join(
                        testscript.pts_golden_config, loc)
                    if not os.path.exists(self.parent.pts_golden_config):
                        self.failed("Golden pts file is not found under the "
                                    "image branch directory '{loc}'".format(
                                        loc=self.parent.pts_golden_config))
                    log.info("Golden PTS file path is '{}'".format(
                        self.parent.pts_golden_config))

                # We should unpickle self.parent.pts_golden_config here
                try:
                    unpickled_golden = unpickle(self.parent.pts_golden_config)
                except Exception as e:
                    self.failed("Failed in processing the provided "
                                "golden PTS file '{f}', please verify its a "
                                "valid file".\
                                format(f=self.parent.pts_golden_config),
                                from_exception=e)

                if feature not in unpickled_golden:
                    self.skipped("No information about '{f}' in the "
                                 "golden config".format(f=feature))

                # Do the comparison
                compare_result = Profile.compare(
                    compare1=unpickled_golden,
                    compare2=learnt_output,
                    pts_data=self.parent.pts_data,
                    testbed=testbed,
                    verf_data=self.parent.verifications)

                summarize_comparison(
                    summarized_dict=compare_result,
                    passed_feature=feature,
                    print_not_compared=False)

                if compare_result[feature]['failed']:
                    self.failed('Comparison between pts_golden_config and '
                           'snapshot is different, '
                           'Check the summary table for more details')
            else:
                # Create Summary
                summary = Summary(title='{f} PTS Summary'.format(
                    f=feature.title()), width=150)

                for device in learnt_output[feature]:
                    msg = "No comparison to be performed, "\
                          "'pts_golden_config' is not provided"

                    summary.summarize_section(device=device, message=msg)

                summary.print()
                log.info("\n")

        # For CommonCleanup, compare with what was stored in CommonSetups
        elif isinstance(self, CommonCleanup):

            # Do the comparison
            compare_result = Profile.compare(
                compare1=testscript.parameters['pts'],
                compare2=learnt_output,
                pts_data=self.parent.pts_data,
                testbed=testbed,
                verf_data=self.parent.verifications)


            summarize_comparison(
                summarized_dict=compare_result,
                passed_feature=feature,
                print_not_compared=False)

            if compare_result[feature]['failed']:
                self.failed('Comparison between snapshot taken at '
                        'common setup and the one taken at common cleanup are '
                        'not equal, Check the summary table for more details')


def asynchronous_configure_snapshot(device, configs, section=None):
    '''Use asynchronous execution when taking configuration snapshots'''

    configs[device.name] = {}

    # get abstract command
    abstract = Lookup.from_device(device,
                                  packages={'sdk':sdk})
    conf_command = abstract.sdk.libs.abstracted_libs.configure_snapshot_command\
        .ConfigureSnapshotCommand()

    if not conf_command.command:
        # No configuration to send
        configs[device.name]['config'] = 'N/A'
        configs[device.name]['summary_msg'] = \
            "Successfully saved configuration snapshot"
        return configs

    try:
        config = Config(device.execute(conf_command.command))
        config.tree()
        configs[device.name]['config'] = config
        configs[device.name]['summary_msg'] = \
            "Successfully saved configuration snapshot"

        if section and hasattr(device, 'file_name'):
            #overriding the default directory
            if hasattr(device, 'file_location') and isinstance(device.file_location, str):
                default_dir = device.file_location
                log.warning("Overriding the default directory with {}".format(default_dir))
            else:
                default_dir = abstract.sdk.libs.abstracted_libs.subsection \
                    .get_default_dir(device)

            if default_dir and default_dir[-1:]!='/':
                default_dir = default_dir + '/'

            restore = abstract.sdk.libs.abstracted_libs.restore.Restore()
            restore.save_configuration_to_file(
                device=device,
                file_name=device.file_name,
                default_dir=default_dir
            )
    except Exception as e:
        configs[device.name]['config_snapshot_failed'] = True
        configs[device.name]['summary_msg'] = \
            "Failed to save configuration snapshot {}".format(str(e))

    return configs

# subsections for common_cleanup
def delete_plugin(self, testbed, testscript, steps):

    '''Delete all the plugins associated with the device during the run'''
    log.info("Delete all the devices' debug plugins copied during the run")

    dialog = Dialog([
        Statement(pattern=r'.*Do you want to delete.*',
                  action='sendline(y)',
                  loop_continue=True,
                  continue_timer=False)])

    for dev in testbed.devices:
        device = testbed.devices[dev]
        if device.is_connected() and hasattr(device, 'debug_plugin'):
            try:
                device.execute('delete {dp}'.format(dp=device.debug_plugin),
                    reply=dialog)
            except Exception as e:
                self.failed("Unable to delete debug plugin from device {dev}".format(
                    dev=dev), from_exception=e)
        else:
            continue
