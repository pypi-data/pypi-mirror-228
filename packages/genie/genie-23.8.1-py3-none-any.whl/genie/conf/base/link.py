import functools
import weakref

from pyats.datastructures import WeakList
from pyats.topology.exceptions import DuplicateInterfaceConnectionError,\
    LinkError

from pyats.topology.link import Link as pyatsLink

from .base import Base, LinkFeature
from .decorator import log_it
from .exceptions import SingleLoopbackConnectionError,\
    LoopbackConnectionTypeError


@functools.total_ordering
class Link(Base, pyatsLink):
    """ Link class

    `Link` class contains all the link level information and
    functionalities.

    Args:
        name (`str`): link name
        alias (`str`): link alias
        interfaces (`list`): a list of Interface objects
                             associate with current Link object
        obj_state ('str'): Store the state of the object
        features ('list'): Device features
        pyats_link (`pyATS Link`): interval to hold pyats link

    Returns:
            a `Link` object

    Examples:

        >>> link = Link(name="r1-r2-1", interfaces=interfaces)
        <genie.conf.base.link.Link object at 0xf6b5a06c>

    """
    _name = None  # mandatory (read-only hash key)
    _testbed = None
    aliases = None  # []
    features = None  # set()
    interfaces = None  # WeakList
    obj_state = 'active'

    def __init__(self,
                 name,
                 features=(),
                 interfaces=(),
                 **kwargs):

        self.aliases = []
        self.features = set()
        self.interfaces = WeakList()

        super().__init__(name=name, **kwargs)

        for intf in interfaces:
            self.connect_interface(intf)

        # features object were provided
        for feature in features:
            self.add_feature(feature)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, key):
        self._name = key

    @property
    def devices(self):
        """Read-Only property to get devices on this link"""
        return tuple(set([intf.device for intf in self.interfaces]))

    def testbed(self):
        """Link testbed property getter

        Returns the Testbed object current link associate with, or None.
        """
        if self._testbed:
            # Get the actual testbed object
            return self._testbed()
        elif self.interfaces:
            for interface in self.interfaces:
                for device in interface.devices:
                    if hasattr('testbed', device):
                        self._testbed = device.testbed
                        return device.testbed
        return None

    @log_it
    def connect_interface(self, interface):
        """ method to connect a interface to this link

        API to connect a `Interface` obj to current `Link` obj,
        also associate the 'links' attribute with this interface obj

        Args:
            interface (`Interface`): interface object

        Returns:
            `None`

        Examples:
            Import related packages

            >>> from genie.base.link import Link

            Create a Link obj

            >>> link = Link(name='r1-r2-1')

            Create a Interface obj

            >>> from genie.base.interface import Interface
            >>> intf = Interface(name='ethernet3/4')

            connect the interface to this link

            >>> link.connect_interface(interface=intf)
        """
        if interface in self.interfaces:
            raise DuplicateInterfaceConnectionError(interface.name, self.name)

        self.interfaces.append(interface)
        interface.link = self
        # Links under Genie Interface object is deprecated
        # Placed the below workaround to bypass the Unittest (commented out)
        # interface._on_added_from_link(self)

    @log_it
    def disconnect_interface(self, interface):
        """ method to disconnect a interface from this link

        API to disconnect a `Interface` obj from current `Link` obj,
        also remove the association from the interface obj.

        Args:
            interafce (`Interface`): interface object

        Returns:
            `None`

        Examples:
            create testbed obj from yaml

            >>> genie_tb = Genie.init(tb=yaml)

            get a link obj named 'ri-r2-1' from the testbed

            >>> link = genie_tb.find_links(name=Or('r1-r2-1'))

            Create a Interface obj

            >>> from genie.base.interface import Interface
            >>> intf = Interface(name='ethernet3/4')

            disconnect the interface from this link

            >>> link.disconnect_interface(interface=intf)
        """
        # Check that this instance is in this link
        if interface not in self.interfaces:
            raise LinkError(interface.name, self.name)

        # Update interface obj
        self.interfaces.remove(interface)
        interface.link = None
        # Links under Genie Interface object is deprecated
        # Placed the below workaround to bypass the Unittest (commented out)
        # interface._on_removed_from_link(self)

    @log_it
    def find_interfaces(self, *rs, iterable=None, count=None,
                        cls=None, obj_state='active', **kwargs):
        """Find interface objects from link object or of a provided iterable

        API to get `Interface` obj(s) from current `Link` obj or provided
        iterable.

        The list can also filtered down with specific keyword arguments. Those
        keyword argument must match the attribute and the value can either be
        a callable, or a specific value. One common use case is to use pyATS
        Logic testing as callable, which gives you Or/And/Not functionality.

        pyATS logic testing:
        http://wwwin-pyats.cisco.com/documentation/html/datastructures/logic.html#logic-tests

        If no kwargs is given, then all the `Interface` objs within this link
        are returned if their `obj_state` match with the requires state

        Return:
            `list`: a list of `Interface` objects, or empty if nothing matches

        Args:
            iterable (`list`): Iterable of interfaces. If it is provided, then
                               it will find within this iterable. If it is not
                               provided, then it will use the link interfaces
                               list.
            count (`int`): Quantity of interfaces will be returned, by default
                           it returns all
            obj_state ('Callable' or 'value'): State of the objects wanted, can
                                               be specified as a callable, or a
                                               specific value
            kwargs (`dict`) : Gives the user ability to fine tune the API to
                              return only filtered objects. It can be done via
                              callable, or specific value

        Return:
            `list`: a list of `Interfaces` objects, or empty if nothing matches

        Examples:

            Create a Testbed obj from yaml file

            >>> from genie.conf import Genie
            >>> genie_tb = Genie.init(tb=yaml)

            Get a link obj

            >>> link = genie_tb.find_links(name=Or('r1-r2-1'))

            Get all interface objects under this link

            >>> link.find_interfaces()

            [<genie.conf.base.interface.EthernetInterface object at 0xf6b5ae8c>,
            <genie.conf.base.interface.EthernetInterface object at 0xf6b5ac6c>]

            Get 1 interface object

            >>> link.find_interfaces(count=1)

            [<genie.conf.base.interface.EthernetInterface object at 0xf6b5a12c>]

            Get all interface objects which has name 'ethernet4/1' filtered
            with specific value

            >>> link.find_interfaces(name='ethernet4/1')
            []

            Get all interface objects which has name 'ethernet4/1' filtered
            with pyATS logical callable

            >>> link.find_interfaces(name=Or('ethernet4/1'))
            []

            Iterable provided, so will find within this list

            >>> interfaces =\
             [<genie.conf.base.interface.EthernetInterface object at 0xf6b5a12c>,
              <genie.conf.base.interface.EthernetInterface object at 0xf6b5a9ac>]

            >>> link.find_interfaces(iterable=interfaces,
                                       name=Or('ethernet4/1'))
        """
        if cls is None:
            # TODO : Fix circular import
            from .interface import BaseInterface
            cls = BaseInterface

        # Default use case, no iterable was given so use the link.interfaces
        if iterable is None:
            iterable = self.interfaces

        return self._find_objects(*rs, iterable=iterable, count=count,
                                  cls=cls, obj_state=obj_state, **kwargs)

    @log_it
    def add_feature(self, feature):
        """ method to add a feature to this link

        API to add a `Feature` obj to current `Link` obj,
        also associate the Link attribute with this feature obj

        Args:
            feature (`Feature`): feature object

        Returns:
            `None`

        Examples:
            Import related packages

            >>> from genie.base.link import Link

            Create a link obj

            >>> L1 = Link(tested = tb, name = 'r1-r2-1')

            Create a Feature obj

            add the feature into this device

            >>> link.add_feature(feature=feature)
        """
        assert isinstance(feature, LinkFeature)
        self.features.add(feature)
        feature._on_added_from_link(self)

        # For all the register_name
        if hasattr(feature, 'register_name'):
            for name, value in feature.register_name.items():
                try:
                    # This could be a dict, a list, a simple variable
                    attr = getattr(self, name)
                    if isinstance(attr, list) or isinstance(attr, tuple):
                        for item in getattr(self, name):
                            setattr(item, value, feature)
                    elif isinstance(attr, dict):
                        for key, obj in getattr(self, name).item():
                            setattr(obj, value, feature)
                    else:
                        # Add more if needed
                        setattr(attr, value, feature)
                except:
                    pass

    @log_it
    def remove_feature(self, feature):
        """ method to add a feature to this link

        API to add a `Feature` obj to current `Link` obj,
        also associate the Link attribute with this feature obj

        Args:
            feature (`Feature`): feature object

        Returns:
            `None`

        Examples:
            Import related packages

            >>> from genie.base.link import Link

            Create a link obj

            >>> L1 = Link(tested = tb, name = 'r1-r2-1')

            Create a Feature obj

            add the feature into this device

            >>> link.remove_feature(feature=feature)
        """
        self.features.remove(feature)
        feature._on_removed_from_link(self)

        # For all the register_name
        if hasattr(feature, 'register_name'):
            for name, value in feature.register_name.items():
                try:
                    # This could be a dict, a list, a simple variable
                    attr = getattr(self, name)
                    if isinstance(attr, list) or isinstance(attr, tuple):
                        for intf in getattr(self, name):
                            setattr(intf, value, None)
                    elif isinstance(attr, dict):
                        for key, obj in getattr(self, name).item():
                            setattr(obj, value, None)
                    else:
                        # Add more if needed
                        setattr(attr, value, None)
                except:
                    pass

    @log_it
    def find_features(self, *rs, iterable=None, count=None, cls=LinkFeature,
                      **kwargs):
        """Find feature objects from link object or from a provided iterable

        API to get `Feature` obj(s) from current `Link` obj or provided
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

        If no kwargs is given, then all the `Feature` objs within this link
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
            the link features list.

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
        # Default use case, no iterable was given so use the link.features
        if iterable is None:
            iterable = self.features

        return self._find_objects(*rs, iterable=iterable, count=count, cls=cls,
                                  **kwargs)

    def __lt__(self, other):
        '''Implement `self < other`.'''
        if not isinstance(other, Link):
            return NotImplemented
        return self.name < other.name

    def __hash__(self):
        return hash(self.name)


class LoopbackLink(Link):
    """ LoopbackLink class

        LoopbackLink inherits from Link class to handle 'loopback-type'
        virtual links (soft links). a lookbackLink  will be the link to connect
        loopback type interfaces

    Args:
        name (`str`): loopback link name
        alias (`str`): loopback link alias
        interfaces (`WeakList`): a list of Interface objects
                                 associate with current LoopbackLink object
    Returns:
            a `LoopbackLink` object

    Examples:
        >>> loop_link = LoopbackLink(name="r1-r2-loop", interfaces=interfaces)

        <genie.conf.base.link.LoopbackLink object at 0xf3c5a06d>
    """

    def __init__(self,
                 name,
                 interfaces=None,
                 **kwargs):

        super().__init__(name=name, **kwargs)

        self.interfaces = WeakList()
        if interfaces:
            # LoopbackLink obj has 1 to many relationship with
            # LoopbackInterface obj, 1 link can only contains 1 loopback
            # interface, but 1 loopback interface can be connected with
            # multiple lookback links
            if len(interfaces) > 1:
                raise Exception
            self.connect_interface(interfaces[0])

    @log_it
    def connect_interface(self, interface):
        """ method to connect a loopback type interface to this virtual link

        API to connect a `LoopbackInterface` obj to current `LoopbackLink` obj,
        also associate the 'links' attribute with this loopback interface obj.

        Args:
            interface (`LoopbackInterface`): loopback interface object

        Returns:
            `None`. If the interface is not a 'LoopbackInterface' type object,
            exception will be raised

        Examples:
            Import related packages

            >>> from genie.base.link import LoopbackLink

            Create a LoopbackLink obj

            >>> loop_link = LoopbackLink(name='r1-r2-loop')

            Create a LoopbackInterface obj

            >>> from genie.base.interface import LoopbackInterface
            >>> intf = LoopbackInterface(name='loopback1')

            connect the interface to this link

            >>> loop_link.connect_interface(interface=intf)
        """
        # Circular
        from .interface import LoopbackInterface
        if self.interfaces:
            raise SingleLoopbackConnectionError()
        if not isinstance(interface, LoopbackInterface):
            raise LoopbackConnectionTypeError()

        super().connect_interface(interface)


class VirtualLink(Link):
    '''Base class for virtual links.

    A virtual link models non-physical indirect connections between interfaces
    that is defined via network protocols. For example, the `BridgeDomain` and
    `Xconnect` classes maintain logical `VirtualLink` objects that connect
    client-side interfaces together.
    '''
    pass


class EmulatedLink(Link):
    '''Base class for emulated links.

    An emulated link models non-physical connections between physical and
    emulated (`EmulatedDevice`) devices' interfaces.
    '''
    pass
