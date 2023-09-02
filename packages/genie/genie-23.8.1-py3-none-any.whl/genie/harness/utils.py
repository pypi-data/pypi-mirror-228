import os
import re
import time
import json
import yaml
import logging
import difflib
import getpass
import importlib
from copy import deepcopy

from genie.libs import sdk

from genie.abstract.magic import Lookup


# Initialize the logger
logger = logging.getLogger('pyats.aetest')


def load_attribute(pkg, attr_name, device=None, suppress_warnings=False):
    """Returns a class or function from a given package

    Loads the supplied pkg argument package and if the package is defined as a genie abstract package,
    then it does a class lookup based upon device tokens as well. If the supplied pkg argument is Falsy,
    then this function just straight loads and returns the requested attribute if it's available.

    Args:
        pkg (str): The package to look in
        attr_name (str): The name of the class to look for
        device (obj): The device to use for abstraction token lookup
        suppress_warnings (bool): Optional. Supresses warning messages when True. Set to False by default.

    Returns:
        object: class or function from the package based on the attribute name 

    Raises:
        AttributeError: if the attribute cannot be found
    """
    # pkg is used for abstraction, as the package has to be imported
    # first
    if pkg:
        # Get package name
        pkg_name = pkg.split('.')[-1]
        # import it; if it explodes,  then it will error
        attribute = importlib.import_module(name=pkg)
        if getattr(attribute, '__abstract_pkg', None):
            # Lookup is cached,  so only the first time will be slow
            # Otherwise it is fast
            attribute = Lookup.from_device(device, packages={pkg_name:attribute})
            # Build the class to use to call
            items = attr_name.split('.')
            items.insert(0, pkg_name)
        else:
            items = attr_name.split('.')

        ## Lookup is cached,  so only the first time will be slow
        ## Otherwise it is fast
        #attribute = Lookup.from_device(device, packages={pkg_name:mod})

        for item in items:
            try:
                attribute = getattr(attribute, item)
            except Exception as e:
                items.insert(0, pkg)
                if not suppress_warnings:
                    logger.warning(
                        "Could not load '{item}' from '{path}'. If the attribute "
                        "exists and the path is correct, you might be missing a "
                        "'__init__.py' file."
                        .format(item=item, path=".".join(items))
                    )
                break
    else:
        # So just load it up
        module, attr_name = attr_name.rsplit('.', 1)

        # Load the module
        mod = importlib.import_module(module)

        # Find the right attribute
        try:
            attribute = getattr(mod, attr_name)
        except AttributeError as e:
            raise AttributeError("Couldn't find '{name}' in "
                                 "'{mod}'".format(name=attr_name,
                                                  mod=mod)) from e
    return attribute

def load_class(info, device=None):
    '''Load module based on information and abstract per device if needed'''
    # For each device, figure out what class to call.
    # Might not have a pkg, and only a class
    try:
        cls = info['source']['class']
    except Exception:
        # We dont know what kind of stuff they could've put there, so grab
        # everything
        raise ValueError("'source' is not provided correctly in the datafile")

    # A Trigger/Verification can have abstraction mechanism
    # baked in. If it does, add it to the end of
    # device.custom.abstraction.order
    added_context = False
    if 'abstraction' in info and hasattr(device, 'custom') and\
       'abstraction' in device.custom:

        # Add information in device.custom only for this
        # Verification/Trigger
        added_context = True
        backup_abstraction = deepcopy(device.custom['abstraction'])
        for key, value in info['abstraction'].items():
            if key == 'order':
                device.custom['abstraction']['order'].extend(value)
                continue
            device.custom['abstraction'][key] = value

    try:
        return load_attribute(info['source'].get('pkg', None), cls, device = device)
    finally:
        if added_context:
            device.custom['abstraction'] = backup_abstraction

def load_method(module, method_name, device=None):
    '''Load a module, and get the method'''

    return load_attribute(module, method_name, device = device)

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    sorted(aList, key=natural_keys) sorts in human order
    '''
    return [atoi(c) for c in re.split('(\d+)', text)]

def connect_device(device, pool_size = None, netconf_pool_size = None, summary_information=None):
    '''Connect the device'''

    # For each mapping provided, connect
    allowed_mapping = ['cli', 'yang', 'rest', 'xml', 'web', 'restconf', 'netconf', 'gnmi']
    sleep_needed = ['yang', 'restconf', 'netconf', 'gnmi']
    # Via to Alias, in case two alias use the same via
    mapper = {}
    if summary_information is None:
        summary_information = {}
    summary_information['connected'] = []

    # NetConf pool size set to pool_size if netconf_pool_size is not passed
    netconf_pool_size = pool_size if not netconf_pool_size else netconf_pool_size

    for mapping in allowed_mapping:
        # New context schema implementation
        if device.mapping.get('context', None):
            # If context connections in device.mapping connect
            connections = device.mapping['context']
            for context, connect_data in connections.items():
                for data in connect_data:
                    via = data.get('via', None)
                    alias = data.get('alias', None)
                    pool_size = data.get('pool_size', None)
                    sleep = data.get('sleep', None)

                    #For High availability (HA) devices
                    #connect to both console [a, b]
                    if isinstance(via, list):
                        if sorted(via) == ['a', 'b']:
                            try:
                                # If the device's connection object was previously initialized
                                # passing prompt_recovery as a parameter to .connect() will
                                # not work as .connect() will use the original connect params
                                if hasattr(device, alias):
                                    setattr(getattr(device, alias), 'prompt_recovery', True)

                                device.connect(alias=alias, prompt_recovery=True)
                                summary_information['connected'].append(
                                    [alias, via,
                                     netconf_pool_size if alias == 'netconf' else pool_size])
                                continue
                            except Exception as e:
                                raise Exception("'{e}'".format(e=e)) from e
                        else:
                            raise Exception("Not supported mapping list '{l}'".format(l=via))

                    # if via is not a list, use alias as via
                    if via in mapper and mapper[via] in device.connectionmgr.connections:
                        device.connectionmgr.connections[alias] = device.connectionmgr.connections[
                            mapper[via]]
                    else:
                        mapper[via] = alias

                    if 'init_exec_commands' in device.connections[via].keys():
                        init_exec_commands = device.connections[via]['init_exec_commands']
                    else:
                        abstract = Lookup.from_device(device,
                                                      packages={'sdk': sdk})
                        init_exec_commands_instance = abstract.sdk.libs. \
                            abstracted_libs.init_exec_commands.InitExecCommands()

                        init_exec_commands = init_exec_commands_instance.get_commands()
                    try:
                        if pool_size:
                            logger.info("Connecting to the device with '{ps}' "
                                        "connections pool".format(
                                            ps=netconf_pool_size if alias ==
                                            'netconf' else pool_size))
                            device.connect(alias=mapping,
                                           prompt_recovery=True,
                                           pool_size=netconf_pool_size if
                                           mapping == 'netconf' else pool_size)
                        else:
                            if hasattr(device, alias):
                                setattr(getattr(device, alias), 'prompt_recovery', True)

                            device.connect(via=via,
                                           init_exec_commands=init_exec_commands,
                                           alias=alias,
                                           prompt_recovery=True)
                    except ValueError as e:
                        raise ValueError("'{m}' was provided in the "
                                         "mapping_datafile but does not "
                                         "exists in the testbed "
                                         "file".format(m=alias)) from e
                    except Exception as e:
                        raise Exception("'{d}'".format(d=e))
                    summary_information['connected'].append([alias, via,
                                                             netconf_pool_size if alias == 'netconf' else pool_size])

                    # Need a nap?
                    if via in sleep_needed:
                        if sleep:
                            logger.info("Sleeping '{t}' after "
                                        "connecting to '{m}'".format(
                                t=via,
                                m=alias))
                            time.sleep(sleep)
                        else:
                            # Default to 5 sec
                            logger.info("Sleeping '{t}' after "
                                        "connecting to '{m}'".format(t=5,
                                                                     m=alias))
                            time.sleep(5)

            device.mapping.pop('context', None)

        elif mapping in device.mapping:
            via = device.mapping[mapping]

            # connect to both console [a, b]
            if isinstance(via, list):

                if sorted(via) == ['a', 'b']:
                    try:
                        # If the device's connection object was previously initialized
                        # passing prompt_recovery as a parameter to .connect() will
                        # not work as .connect() will use the original connect params
                        if hasattr(device, mapping):
                            setattr(getattr(device, mapping), 'prompt_recovery', True)

                        device.connect(alias=mapping, prompt_recovery=True)
                        summary_information['connected'].append(
                            [mapping, device.mapping[mapping],
                             netconf_pool_size if mapping == 'netconf' else pool_size])
                        continue
                    except Exception as e:
                        raise Exception("'{e}'".format(e=e)) from e
                else:
                    raise Exception("Not supported mapping list '{l}'".format(l=via))

            # if via is not a list
            if via in mapper and mapper[via] in device.connectionmgr.connections:
                device.connectionmgr.connections[mapping] = device.connectionmgr.connections[mapper[via]]
            else:
                mapper[via] = mapping

            if 'init_exec_commands' in device.connections[via].keys():
                init_exec_commands = device.connections[via]['init_exec_commands']
            else:
                abstract = Lookup.from_device(device,
                                              packages={'sdk': sdk})
                init_exec_commands_instance = abstract.sdk.libs. \
                    abstracted_libs.init_exec_commands.InitExecCommands()

                init_exec_commands = init_exec_commands_instance.get_commands()

            try:
                if pool_size:
                    logger.info("Connecting to the device with '{ps}' "
                                "connections pool".format(ps=netconf_pool_size if mapping == 'netconf' else pool_size))
                    device.connect(alias=mapping, prompt_recovery=True,
                        pool_size = netconf_pool_size if mapping == 'netconf' else pool_size)
                else:
                    # If the device's connection object was previously initialized
                    # passing prompt_recovery as a parameter to .connect() will
                    # not work as .connect() will use the original connect params
                    if hasattr(device, mapping):
                        setattr(getattr(device, mapping), 'prompt_recovery', True)
                    device.connect(via=device.mapping[mapping],
                                   init_exec_commands=init_exec_commands,
                                   alias=mapping,
                                   prompt_recovery=True)
            except ValueError as e:
                raise ValueError("'{m}' was provided in the "
                                 "mapping_datafile but does not "
                                 "exists in the testbed "
                                 "file".format(m=mapping)) from e
            except Exception:
                raise
            summary_information['connected'].append([mapping, device.mapping[mapping],
                                                     netconf_pool_size if mapping == 'netconf' else pool_size])

            # Need a nap?
            if mapping in sleep_needed:
                if 'sleep' in device.mapping[mapping]:
                    logger.info("Sleeping '{t}' after "
                                "connecting to '{m}'".format(
                        t=device.mapping[mapping],
                        m=mapping))
                    time.sleep(device.mapping[mapping])
                else:
                    # Default to 5 sec
                    logger.info("Sleeping '{t}' after "
                                "connecting to '{m}'".format(t=5,
                                                             m=mapping))
                    time.sleep(5)

        # Not in device.mapping, make sure it wasnt the context
        elif device.context == mapping:
            raise KeyError("'{m}' was not defined for '{d}' but "
                           "the context is {m}".format(d=device.name,
                                                       m=mapping))

def disconnect_device(device):
    '''Disconnect the device'''

    # For each mapping provided, connect
    allowed_mapping = ['cli', 'yang', 'rest', 'xml', 'web', 'restconf', 'netconf', 'gnmi']
    sleep_needed = ['yang', 'restconf', 'netconf', 'gnmi']
    # Via to Alias, in case two alias use the same via
    mapper = {}

    for mapping in allowed_mapping:
        if mapping in device.mapping:
            via = str(device.mapping[mapping])

            if via in mapper and mapper[via] in device.connectionmgr.connections:
                # Then it was already disconnected
                pass
            else:
                mapper[via] = mapping

            try:
                device.disconnect(alias=mapping)
            except ValueError as e:
                raise ValueError("'{m}' was provided in the "
                                 "mapping_datafile but does not "
                                 "exists in the testbed "
                                 "file".format(m=mapping)) from e

        # Not in device.mapping, make sure it wasnt the context
        elif device.context == mapping:
            raise KeyError("'{m}' was not defined for '{d}' but "
                           "the context is {m}".format(d=device.name,
                                                       m=mapping))

def recursive_trim(obj, keys):
    '''
    recursively strip out keys from a datastructure (obj), where:
        - if obj is dict, recursively strip keys from all children
        - if obj is list, recurse through list item and if item is dict,
          remove keys from dict recursively

    note - destructive operation on input obj
    '''

    if isinstance(obj, list):
        for item in obj:
            recursive_trim(item, keys = keys)
    elif isinstance(obj, dict):
        for k, v in list(obj.items()):
            if k in keys:
                del obj[k]
            elif isinstance(v, dict) or isinstance(v, list):
                obj[k] = recursive_trim(v, keys = keys)
    return obj


def get_url():
    mod = importlib.import_module('genie.harness.main')
    if mod.__file__.endswith('py'):
        url = 'http://wwwin-pyats.cisco.com/cisco-shared/genie/latest'
    else:
        url = 'https://pubhub.devnetcloud.com/media/genie-docs/docs/'
    return url
