'''Testbed module'''

import inspect
import warnings
import logging
import gc

from pyats.topology.bases import TopologyDict
from pyats.topology.testbed import Testbed
from pyats.topology.exceptions import DuplicateDeviceError, UnknownDeviceError,\
    DuplicateLinkError

from .base import Base, ConfigurableBase
from .base import FeatureBase, DeviceFeature, LinkFeature, InterfaceFeature
from .link import Link
from .device import Device
from .interface import BaseInterface
from .decorator import log_it
from .exceptions import UnknownLinkError
from .warnings import GenieLibsConfNotAvailableWarning
from genie.conf.base.utils import IPv4InterfaceCache, IPv6InterfaceCache,\
    MACCache

logger = logging.getLogger(__name__)


class Testbed(ConfigurableBase, Testbed):
    """ Testbed class

    `Testbed` class contains all the testbed level information and
    functionalities.

    Args:
        name (`str`): testbed name
        _pyats_testbed (`Testbed`): internal var to hold ats Testbed object
        devices (`list`): a `list` of device objects associatel
                                  with current testbed object
        links (`list`): a `list` of link objects that associate
                                with current testbed object

    Returns:
            a `Testbed` object


    Examples:
        >>> tb = Testbed(name="N7K", devices=devices, links=links)
        <genie.libs.conf.testbed.Testbed object at 0xf6b5a06c>
    """

    def __new__(cls, *args, **kwargs):

        factory_cls = cls
        if factory_cls is Testbed:
            # Create the genie.libs version so the community can implement
            # extra functionality.
            try:
                import genie.libs.conf.testbed as XbuModule
                factory_cls = XbuModule.Testbed
            except (ImportError, AttributeError) as e:
                warnings.warn(
                    'Community-based Genie version not available;'
                    ' Extended Testbed functionality will not be available:'
                    ' {e}'.format(e=e),
                    GenieLibsConfNotAvailableWarning)

        if factory_cls is not cls:
            self = factory_cls.__new__(factory_cls, *args, **kwargs)
        elif super().__new__ is object.__new__:
            self = super().__new__(factory_cls)
        else:
            self = super().__new__(factory_cls, *args, **kwargs)
        return self

    def __init__(self, name=None, links=None, devices=None,
                 **kwargs):
        """ Init Testbed object """
        super().__init__(name=name, **kwargs)

        self.ipv4_cache = IPv4InterfaceCache()
        self.ipv6_cache = IPv6InterfaceCache()
        self.mac_cache = MACCache()

        # Contains all the testbed devices object
        if devices:
            for device in devices:
                self.add_device(device)

    def object_instances(self, cls=Base, subclasses=True):
        if not inspect.isclass(cls) or not issubclass(cls, Base):
            raise ValueError(
                '%r is not a subclass of %s' % (cls, Base.__qualname__))
        return cls._Base_instances(testbed=self, subclasses=subclasses)

    @property
    def testbed(self):
        '''Enables genie.conf.Base to know which testbed this Testbed is a part
           of.'''
        return self

    @log_it
    def find_devices(self, *rs, iterable=None, count=None, cls=Device,
                     obj_state='active', **kwargs):
        """Find devices objects from testbed object or of a provided iterable

        API to get `Device` obj(s) from current `Testbed` obj or provided
        iterable.

        The list can also filtered down with specific keyword arguments. Those
        keyword argument must match the attribute and the value can either be
        a callable, or a specific value. One common use case is to use pyATS
        Logic testing as callable, which gives you Or/And/Not functionality.

        pyATS logic testing:
        http://wwwin-pyats.cisco.com/documentation/html/datastructures/logic.html#logic-tests

        If no kwargs is given, then all the `Device` objs within this device
        are returned if their `obj_state` match with the requires state

        Parameters
        ----------
        rs : ``*args``
            Positional argument of requirements to find particular object

        iterable : `list`
            Iterable of devices. If it is provided, then it will find
            within this iterable. If it is not provided,
            then it will use the testbed devices list.

        count : `int`
            Quantity of devices will be returned, by default it returns all

        obj_state : 'Callable' or 'value'
            State of the objects wanted, can be specified as a callable,
            or a specific value

        kwargs : `dict`
            Gives the user ability to fine tune the API to return only
            filtered objects. It can be done via callable,
            or specific value

        Returns
        -------
            `list`: a list of `Device` objects, or empty if nothing matches

        Raises:

        Examples:
            create a Testbed obj from yaml file

            >>> from genie.conf import Genie
            >>> genie_tb = Genie.init(tb=yaml)

            Get all Device object

            >>> genie_tb.find_devices()

            [<genie.conf.base.device.Device object at 0xf6b5a92c>,
            <genie.conf.base.device.Device object at 0xf6b5aa4c>,
            <genie.conf.base.device.Device object at 0xf6b5b36c>,
            <genie.conf.base.device.Device object at 0xf6b5b3ec>,
            <genie.conf.base.device.Device object at 0xf6b5b40c>,
            <genie.conf.base.device.Device object at 0xf6b5b42c>,
            <genie.conf.base.device.Device object at 0xf6b5b52c>,
            <genie.conf.base.device.Device object at 0xf6b5b16c>]

            Get 2 device objects

            >>> genie_tb.find_devices(count=2)

            [<genie.conf.base.device.Device object at 0xf6b5a92c>,
            <genie.conf.base.device.Device object at 0xf6b5aa4c>,]

            Get all the devicee objects which has name 'PE1' filtered
            with the specific value

            >>> genie_tb.find_devices(name='PE1')

            Get all device objects which has name 'PE1'

            >>> genie_tb.find_devices(name=Or('^PE1$'))

            [<genie.conf.base.device.Device object at 0xf6b5a92c>]

            Get all device objects with alias contains either 'P1' or 'P2'
            genie_tb.find_devices(alias=Or('P1', 'P2'))

            []

            Iterable provided, so will find within this list

            >>> devices = [<genie.genie.base.device.Device object at 0xf6b5a92c>,
                           <genie.genie.base.device.Device object at 0xf6b5aa4c>,]

            >>> genie_tb.find_devices(iterable=devices, name=Or('^PE1$'))

        """

        # Default use case, no iterable was given so use the testbed.links
        if iterable is None:
            iterable = self.devices

        # The returned devices are of type Topodict and not a set anymore.
        # The else is for the scenario of passing a list to the find_devices
        # and not a dictionary.
        if isinstance(iterable, dict):
            return self._find_objects(*rs, iterable=set(iterable.values()),
                count=count, cls=cls, obj_state=obj_state, **kwargs)
        else:
            return self._find_objects(*rs, iterable=iterable,
                count=count, cls=cls, obj_state=obj_state, **kwargs)

    @log_it
    def find_links(self, *rs, iterable=None, count=None, cls=Link,
                   obj_state='active', **kwargs):
        """Find link objects from testbed object or from a provided iterable

        API to get `Link` obj(s) from current `Testbed` obj or provided
        iterable.

        The list can also filtered down with specific keyword arguments. Those
        keyword argument must match the attribute and the value can either be
        a callable, or a specific value. One common use case is to use pyATS
        Logic testing as callable, which gives you Or/And/Not functionality.

        pyATS logic testing:
        http://wwwin-pyats.cisco.com/documentation/html/datastructures/logic.html#logic-tests

        If no kwargs is given, then all the `Link` objs within this testbed
        are returned if their `obj_state` match with the requires state

        Parameters
        ----------
            rs : ``*args``
                Positional argument of requirements to find particular object

            iterable : `list`
                Iterable of links. If it is provided, then it will find
                within this iterable. If it is not provided,
                then it will use the testbed links list.

            count : `int`
                Quantity of links will be returned, by default it returns all

            obj_state : 'Callable' or 'value'
                State of the objects wanted, can be specified as a callable,
                or a specific value

            kwargs : `dict`
                Gives the user ability to fine tune the API to return only
                filtered objects. It can be done via callable,
                or specific value

        Returns
        -------
            `list`: a list of `Link` objects, or empty if nothing matches

        Examples
        --------
            create a Testbed obj from yaml file

            >>> from genie.conf import Genie
            >>> genie_tb = Genie.init(tb=yaml)

            Get all Link object

            >>> genie_Tb.find_links()
            [<genie.conf.base.link.Link object at 0xf6b5b60c>,
            <genie.conf.base.link.Link object at 0xf6b5b6cc>,
            <genie.conf.base.link.Link object at 0xf6b5b62c>,
            <genie.conf.base.link.Link object at 0xf6b5b72c>]

            Get 2 link objects

            >>> genie_tb.find_links(count=2)

            [<genie.conf.base.link.Link object at 0xf6b5b60c>,
            <genie.conf.base.link.Link object at 0xf6b5b6cc>, ]

            Get all link objects which has name 'r1-r2-1' filtered
            with the specific value

            >>> genie_tb.find_links(name=Or('^r1-r2-1$'))

            Get all link objects which has name 'r1-r2-1' filtered
            with pyATS logic callable

            >>> genie_tb.find_links(name=Or('^r1-r2-1$'))

            [<genie.conf.base.link.Link object at 0xf6b5b62c>,]

            Iterable provided, so will find within this list

            >>> links = [<genie.conf.base.link.Link object at 0xf6b5b60c>,
                         <genie.conf.base.link.Link object at 0xf6b5b62c>]

            >>> genie_tb.find_links(iterable=links, name=Or('^r1-r2-1$'))

            [<genie.conf.base.link.Link object at 0xf6b5b62c>,]
        """

        # Default use case, no iterable was given so use the testbed.links
        if iterable is None:
            iterable = self.links

        return self._find_objects(*rs, iterable=iterable, count=count, cls=cls,
                                  obj_state=obj_state, **kwargs)

    @log_it
    def find_interfaces(self, *rs, iterable=None, count=None,
                        cls=BaseInterface, obj_state='active', **kwargs):
        """Find interface objects from testbed object or from a provided
        iterable

        API to get `Interface` obj(s) from current `Testbed` obj or provided
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

        If no kwargs is given, then all the `Interface` objs within this
        testbed are returned if their `obj_state` match with the requires
        state, which is active by default.

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
            the testbed interfaces list.

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

            Get all interface objects under this testbed:

            ::

                >>> testbed.find_interfaces()
                [<genie.Genie.base.interface.EthernetInterface object at 0xf6b5ae8c>,
                <genie.Genie.base.interface.EthernetInterface object at 0xf6b5ac6c>,
                <genie.Genie.base.interface.EthernetInterface object at 0xf6b5ad8c>,
                <genie.Genie.base.interface.EthernetInterface object at 0xf6b5aecc>,
                <genie.Genie.base.interface.EthernetInterface object at 0xf6b5a12c>,
                <genie.Genie.base.interface.EthernetInterface object at 0xf6b5a9ac>]

            Get 2 interface objects:

            ::

                >>> testbed.find_interfaces(count=2)
                [<genie.Genie.base.interface.EthernetInterface object at 0xf6b5a12c>,
                <genie.Genie.base.interface.EthernetInterface object at 0xf6b5a9ac>]

            Get all interface objects which has name 'ethernet4/1' filtered
            with the specific value:

            ::

                >>> testbed.find_interfaces(name='ethernet4/1')

            Get all the interfaces of type ethernet that have speed 1000:

            ::

                >>> testbed.find_interfaces(type='ethernet', speed=1000)

        """
        # Default use case, no iterable was given so use the testbed.interfaces
        if iterable is None:
            iterable = self.interfaces

        # The returned interfaces are of type tuple and not a set anymore.
        # The else is for the scenario of passing a tuple to the find_interfaces
        # and not a dictionary.
        if isinstance(iterable, dict):
            return self._find_objects(*rs, iterable=set(iterable.values()),
                count=count, cls=cls, obj_state=obj_state, **kwargs)
        else:
            return self._find_objects(*rs, iterable=iterable,
                count=count, cls=cls, obj_state=obj_state, **kwargs)

    @property
    def interfaces(self):
        interfaces = []
        for device in self.devices.values():
            interfaces.extend(device.interfaces.values())

        return tuple(interfaces)

    def set_active_interfaces(self, interfaces):
        active_objects = set(interfaces.values())
        del interfaces

        for obj in list(active_objects):
            if isinstance(obj, BaseInterface):
                active_objects.add(obj.device)
            elif isinstance(obj, Link):
                for intf in obj.interfaces:
                    active_objects.add(intf)
                    active_objects.add(intf.device)

        for obj in active_objects:
            obj.obj_state = 'active'

        for device in self.devices.values():
            if device not in active_objects:
                device.obj_state = 'inactive'
            for intf in set(device.interfaces.values()) - active_objects:
                intf.obj_state = 'inactive'
        for link in set(self.links) - active_objects:
            if len(set(link.interfaces) & active_objects) >= 2:
                # Link implicitly activated because 2 or more interfaces are
                link.obj_state = 'active'
            else:
                link.obj_state = 'inactive'

    @property
    def features(self):
        features = set()
        for l in (self.devices, self.links, self.interfaces):
            for e in l:
                features.update(e.features)
        return features

    @log_it
    def find_features(self, *rs, iterable=None, count=None, cls=FeatureBase,
                      **kwargs):
        """Find feature objects from testbed object or from a provided iterable

        API to get `Feature` obj(s) from current `Testbed` obj or provided
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

        If no kwargs is given, then all the `Feature` objs within this testbed
        are returned if their `obj_state` match with the requires state, which
        is active by default.

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
            the testbed features list.

        count : `int`
            Quantity of features will be returned, by default
            it returns all

        obj_state : 'Callable' or 'value'
            State of the objects wanted, can be specified as a callable,
            or a specific value

        kwargs : `dict`
            Gives the user ability to fine tune the API to return only
            filtered objects. It can be done via callable,
            or specific value

        """
        # Default use case, no iterable was given so use the testbed.features
        if iterable is None:
            iterable = self.features

        return self._find_objects(*rs, iterable=iterable, count=count, cls=cls,
                                  **kwargs)
