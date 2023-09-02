'''
    Device class
'''

import inspect
import json
import logging
import weakref
import warnings
import functools
from genie.libs import sdk
from genie.ops.utils import get_ops, get_ops_features
from genie.libs.parser.utils import get_parser, get_parser_commands
from genie.libs.parser.utils.common import format_output
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from pyats.datastructures.logic import And, Not, Or
from pyats.datastructures import AttrDict
from pyats.topology.exceptions import UnknownInterfaceError
from pyats.topology.exceptions import DuplicateInterfaceError
from pyats.topology.device import Device as PyatsDevice
from pyats.topology.bases import TopologyDict

from genie.abstract import Lookup
from genie.utils.config import Config

from .base import ConfigurableBase, DeviceFeature
from .decorator import log_it
from . import api
from .interface import BaseInterface
from .warnings import GenieLibsConfNotAvailableWarning
from .utils import QDict

# module level logger
logger = logging.getLogger(__name__)

CONFIG_CMDS = {'show running-config', 'show configuration'}


@functools.total_ordering
class Device(PyatsDevice, ConfigurableBase):
    """Device class

    `Device` class contains all the device level information and
    functionalities.

    Args:
        name (`str`): device name
        pyats_device (`Device`): internal var to hold ats Device object
        aliases (`list`): list of aliases for the device
        roles (`list`): list of roles
        type(`str`): device type
        interfaces (`TopologyDict`): a `TopologyDict` of Interface objects
                             associate with current Device object
        obj_state ('str'): Store the state of the object
        features ('list'): Device features
        kwargs (`dict`) : gives the user ability to assign some or all
                          device attributes while creating the device
                          object..

    Returns:
            a `Device` object

    Examples:
        >>> device = Device(name="PE1", pyats_device=device,
        ...          interfaces=interfaces
            <genie.conf.base.device.Device object at 0xf6b5a06c>

    """
    _platform = None
    _os = None
    aliases = None  # []
    features = None  # set()
    obj_state = 'active'
    roles = None  # []

    def __new__(cls, *args, **kwargs):

        factory_cls = cls
        if factory_cls is Device:
            # Create the genie.libs version so the community can implement
            # extra functionality.
            try:
                import genie.libs.conf.device as GenieLibsModule
                factory_cls = GenieLibsModule.Device
            except (ImportError, AttributeError) as e:
                warnings.warn(
                    'Community-based Genie version not available;'
                    ' Extended Device functionality will not be available:'
                    ' {e}'.format(e=e),
                    GenieLibsConfNotAvailableWarning)

        if factory_cls is not cls:
            self = factory_cls.__new__(factory_cls, *args, **kwargs)
        elif super().__new__ is object.__new__:
            self = super().__new__(factory_cls)
        else:
            self = super().__new__(factory_cls, *args, **kwargs)
        return self

    def __init__(self,
                 name,
                 alias = None,
                 tacacs = None,
                 connections = None,
                 passwords = None,
                 clean = None,
                 custom = None,
                 credentials=None,
                 context='cli',
                 interfaces=TopologyDict(),
                 features=(),
                 **kwargs):

        self.context = context
        self.aliases = []
        self.features = set()
        self._name = name
        self.roles = []
        self.mapping = {}

        # attribute required for feature learning but only set during genie harness connect stage
        self.management_interface = None

        self.api = api.API(self)
        PyatsDevice.__init__(self, name, alias=alias, tacacs=tacacs,
            connections=connections, passwords=passwords, clean=clean,
            interfaces=interfaces, custom=custom, credentials=credentials, **kwargs)

        ConfigurableBase.__init__(self, **kwargs)

        # features object were provided
        for feature in features:
            self.add_feature(feature)

    def __eq__(self, other):
        '''Implement `self == other`.

        Two Device instances are considered equal if they have the same `name`
        and belong to the same `testbed`.
        '''
        if not isinstance(other, Device):
            return NotImplemented
        return (self.name, self.testbed) == (other.name, other.testbed)

    def __lt__(self, other):
        '''Implement `self < other`.'''
        if not isinstance(other, Device):
            return NotImplemented
        return self.name < other.name

    def __hash__(self):
        return hash(self.name)

    @log_it
    def find_interfaces(self, *rs, iterable=None, count=None,
                        cls=BaseInterface, obj_state='active', **kwargs):
        """Find interface objects from device object or from a provided
        iterable

        API to get `Interface` obj(s) from current `Device` obj or provided
        iterable.

        The interfaces can also filtered down with specific keyword arguments.
        Those keyword argument must match the attribute and the value. The
        value can either be a callable or a specific value. One common use
        case of callable is pyATS Logic testing, which gives you Or/And/Not
        functionality. Many requirement can be given, and only interfaces
        matching all requirements will be returned. Requirements are provided
        via the R class if more than one is wanted.

        Filtering on attributes of Interface object is also possible with
        a special syntax:

            Look for an interface that has attribute1 and
            has attributes 2 that is equal to value

            <attributes1>__<attributes2> = <value>

        This can be chained as much as wanted

        `pyATS logic testing <http://wwwin-pyats.cisco.com/documentation/html/datastructures/logic.html#logic-tests>`_

        If no kwargs is given, then all the `Interface` objs within this device
        are returned if their `obj_state` match with the requires state, which
        is active by default.

        Returns
        -------
            `list`: a `list` of `Interface` objects, or empty list if nothing
             matches

        Parameters
        ----------
        rs : ``*args``
            Positional argument of requirements to find particular object

        iterable : `list`
            Iterable of interfaces. If it is provided, then it will find
            within this iterable. If it is not provided, then it will use
            the device interfaces list.

        count : `int`
            Quantity of interfaces will be returned, by default
            it returns all

        obj_state : 'Callable' or 'value'
            State of the objects wanted, can be specified as a callable,
            or a specific value

        kwargs : `dict`
            Gives the user ability to fine tune the API to return only
            filtered objects. It can be done via callable,
            or specific value

        Examples
        --------
            Create a Testbed obj from yaml file:

            ::

                >>> from genie.conf import Genie
                >>> from genie.conf.base.utils import R

            Get all interface objects under this device:

            ::

                >>> device.find_interfaces()
                [<genie.Genie.base.interface.EthernetInterface object at 0xf6b5ae8c>,
                <genie.Genie.base.interface.EthernetInterface object at 0xf6b5ac6c>,
                <genie.Genie.base.interface.EthernetInterface object at 0xf6b5ad8c>,
                <genie.Genie.base.interface.EthernetInterface object at 0xf6b5aecc>,
                <genie.Genie.base.interface.EthernetInterface object at 0xf6b5a12c>,
                <genie.Genie.base.interface.EthernetInterface object at 0xf6b5a9ac>]

            Get 2 interface objects:

            ::

                >>> device.find_interfaces(count=2)
                [<genie.Genie.base.interface.EthernetInterface object at 0xf6b5a12c>,
                <genie.Genie.base.interface.EthernetInterface object at 0xf6b5a9ac>]

            Get all interface objects which has name 'ethernet4/1' filtered
            with the specific value:

            ::

                >>> device.find_interfaces(name='ethernet4/1')

            Get a list of devices objects which are not named PE1, filtered
            with pyATS logic callable:

            ::

                >>> device = Genie.find_devices(name=Not('^PE1$'))
                [<genie.Genie.base.interface.EthernetInterface object at 0xf6b5a9ac>]

            Iterable provided, so will find within this list, filtered with
            pyATS logic callable:

            ::

                >>> interfaces = [
                 <genie.Genie.base.interface.EthernetInterface object at 0xf6b5a12c>,
                 <genie.Genie.base.interface.EthernetInterface object at 0xf6b5a9ac>]

                >>> device.find_interfaces(iterable=interfaces,
                                           name=Or('ethernet4/1'))

            Get all the interfaces of type ethernet that have speed 1000:

            ::

                >>> device.find_interfaces(type='ethernet', speed=1000)

        """
        # Default use case, no iterable was given so use the testbed.links
        if iterable is None:
            iterable = self.interfaces

        # The returned interfaces are of type Topodict and not a set anymore.
        # The else is for the scenario of passing a list to the find_devices
        # and not a dictionary.
        if isinstance(iterable, dict):
            return self._find_objects(*rs, iterable=set(iterable.values()),
                count=count, cls=cls, obj_state=obj_state, **kwargs)
        else:
            return self._find_objects(*rs, iterable=iterable,
                count=count, cls=cls, obj_state=obj_state, **kwargs)

    @log_it
    def add_feature(self, feature):
        """method to add a feature to this device

        API to add a `Feature` obj to current `Device` obj.

        Args:
            feature (`Feature`): feature object

        Returns:
            `None`

        Examples:
            Create a Feature obj

            >>> feature = myFeature()

            add the feature into this device

            >>> device.add_feature(feature=feature)
        """
        assert isinstance(feature, DeviceFeature)
        self.features.add(feature)
        feature._on_added_from_device(self)

    @log_it
    def remove_feature(self, feature):
        """method to remove a feature from this device

        API to remove a `Feature` obj from current `Device` obj.

        Args:
            feature (`Feature`): feature object

        Returns:
            `None`

        Examples:
            Create a Feature obj

            >>> feature = myFeature()

            add the feature into this device

            >>> device.add_feature(feature=feature)
            >>> ...

            remove the feature from this device

            >>> device.remove_feature(feature=feature)
        """
        self.features.remove(feature)
        feature._on_removed_from_device(self)

    @log_it
    def find_features(self, *rs, iterable=None, count=None, cls=DeviceFeature,
                      **kwargs):
        """Find feature objects from device object or from a provided iterable

        API to get `Feature` obj(s) from current `Device` obj or provided
        iterable.

        The features can also filtered down with specific keyword arguments.
        Those keyword argument must match the attribute and the value. The
        value can either be a callable or a specific value. One common use
        case of callable is pyATS Logic testing, which gives you Or/And/Not
        functionality. Many requirement can be given, and only features
        matching all requirements will be returned. Requirements are provided
        via the R class if more than one is wanted.

        Filtering on attributes of Feature object is also possible with
        a special syntax:

            Look for an feature that has attribute1 and
            has attributes 2 that is equal to value

            <attributes1>__<attributes2> = <value>

        This can be chained as much as wanted

        `pyATS logic testing <http://wwwin-pyats.cisco.com/documentation/html/datastructures/logic.html#logic-tests>`_

        If no kwargs is given, then all the `Feature` objs within this device
        are returned

        Returns
        -------
            `list`: a `list` of `Feature` objects, or empty list if nothing
             matches

        Parameters
        ----------
        rs : ``*args``
            Positional argument of requirements to find particular object

        iterable : `list`
            Iterable of features. If it is provided, then it will find
            within this iterable. If it is not provided, then it will use
            the device features list.

        count : `int`
            Quantity of features will be returned, by default
            it returns all

        kwargs : `dict`
            Gives the user ability to fine tune the API to return only
            filtered objects. It can be done via callable,
            or specific value

        """
        # Default use case, no iterable was given so use the device.features
        if iterable is None:
            iterable = self.features

        return self._find_objects(*rs, iterable=iterable, count=count, cls=cls,
                                  **kwargs)

    @log_it
    def _on_added_from_testbed(self, testbed):
        """Action to be taken when adding a device/link to a testbed

        Action to be taken when adding a device/link to a testbed

        Args:
            testbed (`Testbed`): testbed object

        Returns:
            `None`

        """
        self.testbed = testbed

    @log_it
    def _on_removed_from_testbed(self):
        """Action to be taken when removing a device/link from a testbed

        Action to be taken when removing a device/link from a testbed

        Args:
            `None`

        Returns:
            `None`

        """
        self.testbed = None

    @property
    def platform(self):
        # dynamic platform attribute to allow up-to-date value once connection
        # to the device is made and platform discovery is done.
        platform = self._platform
        if platform is not None:
            return platform
        else:
            series = getattr(self, 'series', None)
            if series is not None:
                warnings.warn("The 'series' key has been deprecated, it is replaced"
                              " by the 'platform' key.", DeprecationWarning)
            platform = series or getattr(self, 'type', None)
            return platform

    @platform.setter
    def platform(self, value):
        self._platform = value

    def learn_management(self, connection_ip):
        """method to learn the management interface name on the device.

        It will add the retrieved interface name as an attribute to the device
        object.

        Args:
            connection_ip (`str`): connection ip address

        Returns:
            `None`

        Examples:
            >>> device.learn_management(ipaddress)

        """

        # Lookup for the device os
        lookup = Lookup.from_device(self, packages={'sdk':sdk})

        # Creating an instnace of ManagementInterface
        managment_interface_instance = lookup.sdk.libs.abstracted_libs.\
            management_interface.ManagementInterface()

        # Get the corresponding managment interface name
        # Stick the management interface name as an attribute to the device obj
        if isinstance(connection_ip, list):
            address_list = connection_ip
        # if it's not a list, put it in a list
        else:
            address_list = [connection_ip]

        try:
            for ip in address_list:
                self.management_interface = managment_interface_instance.\
                    get_interface_name(device=self, ipaddress=ip)
                # if found one among the list of addresses, then stop
                if self.management_interface is not None:
                    break

        except AttributeError:
            # Capture the case if the device.os is not part of the abstracted
            # function in genie.libs.sdk
            self.management_interface = None

    def _parse_all(self, alias='cli', **kwargs):
        cmds = get_parser_commands(self)
        ret = {}
        for cmd in cmds:
            try:
                parser, parser_kwargs = get_parser(cmd, self)
                kwargs.update(parser_kwargs)
                context = 'cli'
                if 'context' in kwargs:
                    context = kwargs['context']
                    del kwargs['context']
                output = parser(getattr(self, alias), context=context).parse(**kwargs)
                ret[cmd] = output
            except Exception as e:
                ret[cmd] = {'errored': e}
        return ret

    def parse(self, command, alias='', fuzzy=False, continue_on_failure=False, context='cli', **kwargs):

        if not alias:
            alias = self.connectionmgr.connections._default_alias

        if command in CONFIG_CMDS:
            return self.api.get_running_config_dict()
        if command == 'all':
            return self._parse_all()
        parsers = get_parser(command, self, fuzzy)
        if not fuzzy:
            return self._get_parser_output(kwargs, parsers[0], parsers[1], 
                                                                        alias, context)
        else:
            return_dict = {}
            for found_command, parser, parser_kwargs in parsers:
                try:
                    return_dict[found_command] = self._get_parser_output(
                        kwargs.copy(), parser, parser_kwargs, alias)
                except SchemaEmptyParserError:
                    return_dict[found_command] = QDict({})
                except Exception as e: 
                    if continue_on_failure:
                        return_dict.setdefault('exceptions', {}).setdefault(
                                                        found_command, str(e))
                    else:
                        raise Exception(str(e))
            return return_dict

    def _get_parser_output(self, copy, parser, parser_kwargs, alias='cli', context='cli'):
        copy.update(parser_kwargs)

        if 'context' in copy:
            context = copy['context']
            del copy['context']

        out = None
        parser_instance = None
        # need to pop here so that timeout will not cause issue even in else clause
        timeout = copy.pop('timeout', None)
        if self.is_connected(alias=alias):
            orig_exec_timeout = None
            if timeout:
                # save original execute timeout
                orig_exec_timeout = self.execute.timeout
                self.execute.timeout = timeout
            try:
                parser_instance = parser(getattr(self, alias), context=context)
                out = parser_instance.parse(**copy)
            except Exception:
                raise
            finally:
                # restore original execute timeout
                if orig_exec_timeout is not None:
                    self.execute.timeout = orig_exec_timeout
        # if device is not connected, output must be provided to run a parser
        else:
            if 'output' not in copy:
                raise TypeError('device is not connected, ' +
                                'output must be provided.')
            parser_instance = parser(self, context=context)
            out = parser_instance.parse(**copy)

        # return a QD-enabled dictionary
        parsed_output = QDict(out)
        if hasattr(parser_instance, 'raw_output'):
            logger.debug("Adding raw_output to parsed_output:")
            parsed_output.raw_output = parser_instance.raw_output

        if logger.getEffectiveLevel() <= logging.DEBUG:
            logger.debug(format_output(out, tab=2))

        return parsed_output

    def _learn_all(self, **kwargs):
        features = get_ops_features()
        ret={}
        for feature in features:
            try:
                if feature == 'config':
                    ret[feature] = self.api.get_running_config_dict()
                    continue

                ops = get_ops(feature, self)
                o_instance = ops(self, **kwargs)

                # Remove connections, attributes and commands from kwargs
                kwargs.pop('connections', None)
                kwargs.pop('attributes', None)
                kwargs.pop('commands', None)

                o_instance.learn(**kwargs)
                ret[feature] = o_instance
            except Exception as e:
                ret[feature] = {'errored': e}
        return ret

    def learn(self, feature, **kwargs):
        # learn all features
        if feature == 'all':
            return self._learn_all(**kwargs)

        # special case for config
        if feature == 'config':
            return self.api.get_running_config_dict()
        ops = get_ops(feature, self)
        o_instance = ops(self, **kwargs)

        # Remove connections, attributes and commands from kwargs
        kwargs.pop('connections', None)
        kwargs.pop('attributes', None)
        kwargs.pop('commands', None)
        o_instance.learn(**kwargs)
        logger.debug(json.dumps(o_instance.to_dict(), indent=2, sort_keys=True))
        return o_instance
