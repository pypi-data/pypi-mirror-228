'''Interface module'''

__all__ = (
    'BaseInterface',
    'PhysicalInterface',
    'VirtualInterface',
    'PseudoInterface',
    'LoopbackInterface',
)

import functools
import re
import warnings
import weakref
from enum import Enum

from pyats.datastructures import WeakList
from pyats.topology.interface import Interface as pyatsInterface

from .base import ConfigurableBase, InterfaceFeature
from .link import Link, LoopbackLink
from .utils import organize
from .decorator import log_it
from .exceptions import UnknownInterfaceTypeError
from .warnings import GenieLibsConfNotAvailableWarning


@functools.total_ordering
class BaseInterface(pyatsInterface, ConfigurableBase):
    """Base interface class

    `BaseInterface` inherits `Base' class
    It is the super class of `PhysicalInterface` and `VirtualInterface`.

    Args:
        name (`str`): interface name - recommend the name to be
                      a full interface name (for example: ethernet3/3,
                      not eth3/3, not e3/3, etc)
        device (`Device`): the device obj this interface belongs to
        links (`WeakList`): a list of `Link` objects the interface belongs to
        alias ('str'): interface alias, defaults to interface name
        aliases ('list'): list of interface alias
        pyats_interface (Interface): internal var to hold ats Interface object
        kwargs (`dict`) : gives the user ability to assign some or all
                          interface attributes while creating the interface
                          object.

    Returns:
            a `BaseInterface` object

    Examples:
        >>> from genie.conf.base.interface import BaseInterface
        >>> intf = Interface(name='ethernet3/4', device=device)

        <genie.libs.conf.interface.nxos.EthernetInterface object at 0xf6b5b84c>
    """
    alias = None
    aliases = None  # []
    features = None  # set()
    links = None  # WeakList
    vrf = None
    obj_state = 'active'

    def __new__(cls, *args, **kwargs):

        factory_cls = cls
        if factory_cls is BaseInterface:
            # Create the genie.libs version so the community can implement
            # extra functionality.
            try:
                import genie.libs.conf.interface as XbuModule
                factory_cls = XbuModule.Interface
            except (ImportError, AttributeError) as e:
                warnings.warn(
                    'Community-based Genie version not available;'
                    ' Extended Interface functionality will not be available:'
                    ' {e}'.format(e=e),
                    GenieLibsConfNotAvailableWarning)

        if factory_cls is not cls:
            self = factory_cls.__new__(factory_cls, *args, **kwargs)
        elif super().__new__ is object.__new__:
            try:
                self = super().__new__(factory_cls)
            except TypeError:
                # This mean no implementation at all exists for this OS
                # just use the community-base Genie version
                try:
                    factory_cls = BaseInterface
                    self = super().__new__(factory_cls)
                except (ImportError, AttributeError) as e:
                    warnings.warn(
                        'Community-based Genie version not available;'
                        ' Extended Interface functionality will not be'
                        ' available: {e}'.format(e=e),
                                       GenieLibsConfNotAvailableWarning)
        else:
            self = super().__new__(factory_cls, *args, **kwargs)
        return self


    def __init__(self,
                 name,
                 type= None,
                 device=None,
                 links=(),
                 features=(),
                 alias=None,
                 attach=True,
                 *args,
                 **kwargs):

        self.aliases = []
        # ats topology bases requires the passed object to has alias attribute
        if not alias:
            self.alias = name
        self.features = set()
        self.links = WeakList()
        self.name = name

        # Let's add this interface (self), to the device
        if attach and device:
            device.add_interface(self)
        elif device:
            self.device = device

        pyatsInterface.__init__(self, name, type, alias=alias, **kwargs)

        ConfigurableBase.__init__(self, **kwargs)

        for link in links:
            # Let's connect this interface (self), to the device
            link.connect_interface(self)

        # Feature objects were provided
        for feature in features:
            self.add_feature(feature)

    def __eq__(self, other):
        if not isinstance(other, BaseInterface):
            return NotImplemented
        # return (self.device, self.name) == (other.device, other.name)
        return (self.name, self.device) == (other.name, other.device)

    def __lt__(self, other):
        if not isinstance(other, BaseInterface):
            return NotImplemented
        return (self.device, self.name) < (other.device, other.name)

    def __hash__(self):
        # return hash((self.device, self.name))
        return hash(self.name)

    def __repr__(self):
        try:
            name = self.name
            device_name = self.device.name
        except:
            return super().__repr__()
        else:
            return '<%s object %r on %r at 0x%x>' % (
                self.__class__.__name__,
                name,
                device_name,
                id(self))

    @property
    def links(self):
        """Interface link property getter

        Returns the link object current interface associate with, or None.
        """
        warnings.warn(message = "Starting v2.2.0, 'links' is deprecated "
                                "from the interface Genie object. Use "
                                "'link' instead.",
                      category = DeprecationWarning,
                      stacklevel = 2)

        # if self.link = None this will raise *** TypeError: 'NoneType' object
        # is not iterable
        if self.link:
            # __iter__ of the link object returns link.interfaces in pyats so
            # we needed to instantiate the WeakList first before adding link to
            # it.
            weak = WeakList()
            weak.append(self.link)
            return weak
        else:
            return WeakList()

    @links.setter
    def links(self, link):
        """Interface link property setter
        """
        if link:
            self.link = link

    @property
    def testbed(self):
        if self.device:
            return self.device.testbed

    @log_it
    def _on_added_from_device(self, device):
        '''Action to be taken when adding an interface to a device

        Action to be taken when adding an interface to a device

        Args:
            device (`Device`): device object

        Returns:
            `None`

        '''
        self.device = device

    @log_it
    def _on_removed_from_device(self, *args, **kwargs):
        '''Action to be taken when removing an interface from a device

        Action to be taken when removing an interface from a device

        Args:
            `None`

        Returns:
            `None`

        '''

        self.device = None

    @log_it
    def _on_added_from_link(self, link):
        '''Action to be taken when adding a link to an interface

        Action to be taken when adding a link to an interface

        Args:
            link (`Link`): link object

        Returns:
            `None`
        '''

        # Make sure not to add duplicates
        pass
        # if link not in self.links:
        #     self.links.append(link)

    @log_it
    def _on_removed_from_link(self, link):
        '''Action to be taken when removing a link from an interface

        Action to be taken when removing a link to from an interface

        Args:
            link (`Link`): link object

        Returns:
            `None`
        '''
        pass
        # if link in self.links:
        #     self.links.remove(link)

    @log_it
    def add_feature(self, feature):
        """method to add a feature to this interface

        API to add a `Feature` obj to current `Interface` obj.

        Args:
            feature (`Feature`): feature object

        Returns:
            `None`

        Examples:
            Create a Feature obj

            >>> feature = myFeature()

            add the feature into this interface

            >>> interface.add_feature(feature=feature)
        """
        assert isinstance(feature, InterfaceFeature)
        self.features.add(feature)
        feature._on_added_from_interface(self)

    @log_it
    def remove_feature(self, feature):
        """method to remove a feature from this interface

        API to remove a `Feature` obj from current `Interface` obj.

        Args:
            feature (`Feature`): feature object

        Returns:
            `None`

        Examples:
            Create a Feature obj

            >>> feature = myFeature()

            add the feature into this interface

            >>> interface.add_feature(feature=feature)
            >>> ...

            remove the feature from this interface

            >>> interface.remove_feature(feature=feature)
        """
        self.features.remove(feature)
        feature._on_removed_from_interface(self)

    @log_it
    def find_features(self, *rs, iterable=None, count=None,
                      cls=InterfaceFeature, **kwargs):
        """Find feature objects from interface object or from a provided
        iterable

        API to get `Feature` obj(s) from current `Interface` obj or provided
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

        If no kwargs is given, then all the `Feature` objs within this
        interface are returned if their `obj_state` match with the requires
        state, which is active by default.

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
            the interface features list.

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
        # Default use case, no iterable was given so use the interface.features
        if iterable is None:
            iterable = self.features

        return self._find_objects(*rs, iterable=iterable, count=count, cls=cls,
                                  **kwargs)

    def build_config(self, **kwargs):
        '''Place holder in case missing of os implementation

        In the use case there is no configurable interface for a specific
        OS, then this function will be called when configuring the testbed
        or the device. It make sure the code won't crash because of this'''
        return ''

    def build_unconfig(self, **kwargs):
        '''Place holder in case missing of os implementation

        In the use case there is no configurable interface for a specific
        OS, then this function will be called when configuring the testbed
        or the device. It make sure the code won't crash because of this'''
        return ''


class PhysicalInterface(BaseInterface):
    pass


class VirtualInterface(BaseInterface):
    pass


class PseudoInterface(VirtualInterface):
    pass


class LoopbackInterface(VirtualInterface):
    """LoopbackInterface base class for "loopback" interfaces

    Loopback interfaces are virtual interfaces that automatically create a
    virtual "loopback link". This link of type LoopbackLink can be retrieved
    using the "link" attribute.

    """

    # No need for the link property as it is already handled by the parent class

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._link = LoopbackLink(testbed=self.testbed,
                             name='{}:{}'.format(self.device.name, self.name),
                             interfaces=[self])

