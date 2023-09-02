from collections import defaultdict, UserDict
import collections.abc
from copy import copy
from inspect import ismethod, isclass
import logging
import string


from pyats.log import warnings
from genie.decorator import managedattribute
from .base import Base, ConfigurableBase
from .interface import BaseInterface
from .decorator import log_it

log = logging.getLogger(__name__)

_marker = object()


class UnsupportedAttributeWarning(UserWarning):
    """Warning class for Unsupported Attributes

    UnsupportedAttributeWarning throws the warning when
    user requests object attribute not supported

    """
    pass


def _PyType_Lookup(cls, name):
    '''Internal API to look for a name through the MRO.

    This is basically the same as Python's _PyType_Lookup, except no caching is
    provided.
    '''

    # keep a strong reference to mro because cls->tp_mro can be replaced during
    # PyDict_GetItem(dict, name)
    try:
        mro = cls.__mro__
    except AttributeError:
        # (Hopefully never reached)
        # If mro is NULL, the cls is either not yet initialized by PyType_Ready(),
        # or already cleared by type_clear(). Either way the safest thing to do is
        # to return NULL.
        return None

    # Lookup the attribute in each base of the mro and return the first
    # occurence, or None.
    res = None
    for base in mro:
        basedict = base.__dict__
        try:
            res = basedict[name]
        except KeyError:
            pass
        else:
            break

    return res

class AttributesInheriter(object):
    """Base class for AttributesInheriter objects

    AttributesInheriter allows inheriting attributes from a parent object

    Example:

        >>> class A(object):
        ...     a = 1
        ...
        >>> class B(AttributesInheriter):
        ...     pass
        ...
        >>> a = A()
        >>> b = B(parent=a)
        >>> a.a
        1
        >>> b.a
        1
        >>> a.a = 2
        >>> a.a
        2
        >>> b.a
        2
        >>> b.a = 3
        >>> a.a
        2
        >>> b.a
        3

    """
    parent = None

    def __init__(self, parent, **kwargs):
        '''Initialize an AttributesInheriter instance.

        Args:
            parent: the parent object from which to inherit attributes.
                If None, no parent will be set.
        '''

        if parent is not None:
            self.parent = parent
        super().__init__(**kwargs)

    def __inheritmanagedattribute__(self, name):
        '''Internal function used to inherit an attribute defined using a
        managedattribute descriptor.

        When inheriting from a managedattribute, all of the original behavior
        (type checking, transformations, ...) must be inherited as well. Only
        the default value rules (including initializers) are not inherited.
        Instead, the new managedattribute returned will cary the current parent
        value as default back up to the child.

        Returns:
            A new managedattribute instance or None.
        '''

        if name.startswith('_') or name == 'parent':
            # Not inheritable
            return None

        parent = getattr(self, 'parent', None)
        if parent is not None:
            # Maybe parent object's class defines 'name' as a managedattribute
            attr = getattr(type(parent), name, None)
            if attr is not None:
                if isinstance(attr, managedattribute):
                    attr = attr._inherit(parent)
                    if attr is None:
                        # Doesn't want to be inherited!
                        return None
                else:
                    attr = None
            if attr is None:
                # Maybe parent object supports __inheritmanagedattribute__
                f = getattr(parent, '__inheritmanagedattribute__', None)
                if f:
                    attr = f(name)
            if attr is not None:
                attr = attr._inherit(self)
                if attr is None:
                    # Doesn't want to be inherited!
                    return None
                return attr
        # No corresponding managedattribute found
        return None

    def __getattribute__(self, name):
        '''Implements getting an attribute's value.

        See __getattribute_inherit__ for the actual implementation.
        '''
        # Quick test to avoid recursion
        if name.startswith('_') or name == 'parent':
            # Not inheritable
            return super().__getattribute__(name)

        return self.__getattribute_inherit__(name, test_inherit=False)

    def __getattribute_inherit__(self, name, test_inherit):
        '''Implements getting an attribute's value and testing for it's
        inheritance.

        When the object has no such attribute, Lookup the "parent" object for
        an inherited value. Methods are not inherited as they would be bound to
        the parent object, not the child.

        When the parent attribute is a managedattribute descriptor, the
        descriptor is inherited with all it's rules (except for it's default
        value which is evaluated at the parent level.) and is then given the
        task of getting the local value.

        Returns:
            If test_inherit is True:
                - Return True if attribute is inherited.
                - Return False if attribute is not inherited or not set.
            If test_inherit is False:
                - Return the (possibly inherited) attribute value.
        '''

        # This is basically the same as Python's
        # _PyObject_GenericGetAttrWithDict.
        #
        # The only reason the parent inheriting work is not done within
        # __getattr__ is that it is not possible to catch original
        # AttributeError exceptions from local descriptors.

        if name.startswith('_') or name == 'parent':
            # Not inheritable
            return super().__getattribute__(name) \
                if not test_inherit else False

        cls = type(self)
        descr = _PyType_Lookup(cls, name)

        f = None
        if descr is not None:
            f = getattr(descr, '__get__', None)
            if f is not None \
                    and hasattr(descr, '__set__'):  # PyDescr_IsData
                # This is a data descriptor
                return f(self, cls) if not test_inherit else False

        dct = getattr(self, '__dict__', None)
        if dct is not None:
            try:
                value = dct[name]
            except KeyError:
                pass
            else:
                return value if not test_inherit else False

        # -- START --
        # This is where __getattribute__ differs from
        # _PyObject_GenericGetAttrWithDict!
        if descr is None:
            descr = self.__inheritmanagedattribute__(name)
            if descr is not None:
                f = descr.__get__
            if f is not None:
                # Inherited a managedattribute descriptor from the parent.
                return f(self, cls) if not test_inherit else '_' + name not in self.__dict__
            else:
                # No managedattribute descriptor inherited.
                # Look for a inheritable value.
                try:
                    value = getattr(self.parent, name)
                except AttributeError:
                    pass
                else:
                    if ismethod(value):
                        # Do not inherit methods bound to the parent
                        pass
                    else:
                        # Inherit value from the parent
                        return value if not test_inherit else True
        # -- END --

        if f is not None:
            # This is a descriptor (but not a data descriptor)
            return f(self, cls) if not test_inherit else False

        if descr is not None:
            # This is a value (but not a descriptor)
            return descr if not test_inherit else False

        if test_inherit:
            return False
        else:
            raise AttributeError(
                "'%.50s' object has no attribute '%s'"
                % (cls.__name__, name))

    def __setattr__(self, name, value):
        '''Implements setting an attribute's value.

        When the object has no such attribute, Lookup the "parent" object for a
        inherited value.

        When the parent attribute is a managedattribute descriptor, the
        descriptor is inherited with all it's rules (except for it's default
        value which is evaluated at the parent level.) and is then given the
        task of setting the attribute value locally.
        '''

        # This is basically the same as Python's
        # _PyObject_GenericSetAttrWithDict.

        if name.startswith('_') or name == 'parent':
            # Not inheritable
            return super().__setattr__(name, value)

        cls = type(self)
        descr = _PyType_Lookup(cls, name)

        f = None
        if descr is not None:
            f = getattr(descr, '__set__', None)
            if f is not None:
                # and hasattr(descr, '__set__'):  # PyDescr_IsData
                # This is a data descriptor
                return f(self, value)

        # -- START --
        # This is where __setattr__ differs from
        # _PyObject_GenericSetAttrWithDict!
        if descr is None:
            descr = self.__inheritmanagedattribute__(name)
            if descr is not None:
                f = descr.__set__
                return f(self, value)
        # -- END --

        dct = getattr(self, '__dict__', None)
        if dct is not None:
            try:
                dct[name] = value
                return
            except KeyError:
                raise AttributeError(name)

        if f is not None:
            # This is a descriptor (but not a data descriptor)
            # (never reached)
            return f(self, cls)

        if descr is not None:
            raise AttributeError(
                "'%.50s' object attribute '%s' is read-only"
                % (cls.__name__, name))

        raise AttributeError(
            "'%.100s' object has no attribute '%s'"
            % (cls.__name__, name))

    def __delattr__(self, name):
        '''Implements deleting an attribute's value.

        When the object has no such attribute, Lookup the "parent" object for a
        inherited value.

        When the parent attribute is a managedattribute descriptor, the
        descriptor is inherited with all it's rules (except for it's default
        value which is evaluated at the parent level.) and is then given the
        task of deleting the attribute locally.
        '''

        # This is basically the same as Python's
        # _PyObject_GenericSetAttrWithDict (with NULL value).

        if name.startswith('_') or name == 'parent':
            # Not inheritable
            return super().__delattr__(name)

        cls = type(self)
        descr = _PyType_Lookup(cls, name)

        f = None
        if descr is not None:
            f = getattr(descr, '__delete__', None)  # __delete__ ~= __set__
            if f is not None:
                # and hasattr(descr, '__set__'):  # PyDescr_IsData
                # This is a data descriptor
                return f(self)

        # -- START --
        # This is where __delattr__ differs from
        # _PyObject_GenericSetAttrWithDict!
        if descr is None:
            mattr = self.__inheritmanagedattribute__(name)
            if mattr is not None:
                return mattr.__delete__(self)
        # -- END --

        dct = getattr(self, '__dict__', None)
        if dct is not None:
            try:
                del dct[name]
                return
            except KeyError:
                raise AttributeError(name)

        if f is not None:
            # This is a descriptor (but not a data descriptor)
            # (never reached)
            return f(self, cls)

        if descr is not None:
            raise AttributeError(
                "'%.50s' object attribute '%s' is read-only"
                % (cls.__name__, name))

        raise AttributeError(
            "'%.100s' object has no attribute '%s'"
            % (cls.__name__, name))

    def __dir__(self):
        '''Implements returning a list of valid attributes for this object.

        Aside from the default Python behavior of listing the object's
        attributes, the list of attributes that can be inherited from the
        parent object is also included.

        Out of this list of attributes, some may not be available at runtime.
        '''

        result = set(super().__dir__())
        try:
            # For sake of speed, do not check for parent methods.
            result.update(
                name for name in self.parent.__dir__()
                if not name.startswith('_'))
        except:
            pass
        return list(result)

    def isinherited(self, name):
        '''Return true if the attribute is inheritted from the parent object.

        See __getattribute_inherit__ for the actual implementation.
        '''

        return self.__getattribute_inherit__(name, test_inherit=True)

    def __repr__(self):
        '''Implement `repr(self)`.'''
        return '<%s object at 0x%x w/ parent %r>' % (
            self.__class__.__name__,
            id(self),
            self.parent)


class SubAttributes(AttributesInheriter, ConfigurableBase):
    '''Base class for all Subattributes objects

    SubAttributes is typically used to define configurable subsets of a
    feature. Default attribute values are inherited from the parent object.
    '''

    @property
    def testbed(self):
        '''The testbed is read-only and always taken from the parent'''
        return self.parent.testbed


class KeyedSubAttributes(SubAttributes):
    '''Base class for a Key-aware version of SubAttributes.

    KeyedSubAttributes is typically used to define configurable subsets of a
    feature that are stored in a SubAttributesDict structure. Default attribute
    values are inherited from the parent object.

    Contrary to the base SubAttributes class, KeyedSubAttributes tracks the key
    that is used in the related SubAttributesDict so that it is available to
    the child object as well.

    KeyedSubAttributes must be sub-classed and it is the task of the sub-class
    to handle the "key" attribute upon initialization and track it's value for
    future use.

    Sub-classes can optionally declare 2 special class methods (or static
    methods) to interact with SubAttributesDict:

        @classmethod
        def _sanitize_key(cls, key):
            """Attempt to convert the key to a MyType"""
            try:
                key = MyType(key)
            except ValueError:
                pass
            return key

        @classmethod
        def _assert_key_allowed(cls, key):
            """Make sure that the key is of type MyType"""
            if not isinstance(key, MyType):
                raise KeyError

    '''

    def __init__(self, parent, key=_marker):
        '''Initialize a KeyedSubAttributes instance.

        Args:
            parent: Parent object passed on to the parent class unchanged.
            key: Must be consumed by sub-classes; If received here, a TypeError
                will be raised.
        '''
        if key is not _marker:
            raise TypeError('{cls}.__init__ must consume the "key" argument!'.
                            format(cls=type(self).__name__))
        super().__init__(parent=parent)


class DeviceSubAttributes(KeyedSubAttributes):
    '''Base class for SubAttributes objects keyed by device names.

    Use with SubAttributesDict.

    Allowed keys include strings (device names) or Device objects (from which
    the device name is extracted.)
    '''

    device_name = managedattribute(
        name='device_name',
        read_only=True,  # key
        doc='The device name (read-only key)')

    @property
    def device(self):
        '''The Device object associated with the device_name key.

        This is a helper property to hide the logic required for manual lookup.'''
        try:
            return self.testbed.devices[self.device_name]
        except KeyError:
            raise AttributeError(
                '%r object has no attribute %r'
                % (type(self).__name__, 'device'))

    @property
    def os(self):
        '''The OS associated with the device.

        This is a helper property for APIs that query an object's "os" attribute.'''
        return self.device.os

    @property
    def interfaces(self):
        '''The subset of interfaces associated with the device.

        This is a helper property that filters the parent's interfaces and only yields the ones associated with the device.
        '''
        device = self.device
        for interface in self.parent.interfaces:
            if interface.device is device:
                yield interface

    @classmethod
    def _assert_key_allowed(cls, key):
        '''Makes sure that the key is a string (such as a device name.)'''
        if not isinstance(key, str):
            raise KeyError('Only string keys allowed')

    def __init__(self, parent, key):
        '''Initialize a DeviceSubAttributes instance.

        Args:
            parent: Parent object passed on to the parent class unchanged.
            key: The key tracked as "device_name" for later use.
        '''
        self._device_name = key
        super().__init__(parent=parent)

    def __repr__(self):
        '''Implement `repr(self)`.'''
        return '<%s object at 0x%x for device %r w/ parent %r>' % (
            self.__class__.__name__,
            id(self),
            self.device_name,
            self.parent)


class InterfaceSubAttributes(KeyedSubAttributes):
    '''Base class for SubAttributes objects keyed by interface names.

    Use with SubAttributesDict, preferably with a parent object that has a
    "device" attribute, such as DeviceSubAttributes.

    Allowed keys include strings (interfaces names) or Interface objects (from
    which the interface name is extracted.)
    '''

    interface_name = managedattribute(
        name='interface_name',
        read_only=True,  # key
        doc='The interface name (read-only key)')

    @property
    def interface(self):
        '''The Interface object associated with the device_name key.

        This is a helper property to hide the logic required for manual lookup.'''
        try:
            return self.device.interfaces[self.interface_name]
        except KeyError:
            raise AttributeError(
                '%r object has no attribute %r'
                % (type(self).__name__, 'interface'))

    @classmethod
    def _assert_key_allowed(cls, key):
        '''Makes sure that the key is a string (such as an interface name.)'''
        if not isinstance(key, str):
            raise KeyError('Only string keys allowed')

    def __init__(self, parent, key):
        '''Initialize a InterfaceSubAttributes instance.

        Args:
            parent: Parent object passed on to the parent class unchanged.
            key: The key tracked as "interface_name" for later use.
        '''
        self._interface_name = key
        super().__init__(parent=parent)

    def __repr__(self):
        '''Implement `repr(self)`.'''
        return '<%s object at 0x%x for interface %r w/ parent %r>' % (
            self.__class__.__name__,
            id(self),
            self.interface_name,
            self.parent)


class SanitizedDict(UserDict):
    '''Base class for dictionaries that allow only specific types of keys and
    items.

    Sub-classes are encouraged to redefine the _sanitize_key, _sanitize_item
    and _assert_key_allowed methods to suit their needs.
    '''

    def __contains__(self, key):
        '''Implements the "in" operator.

        They key is sanitized such that it is looked up in the expected format.
        '''

        key = self._sanitize_key(key)
        return super().__contains__(key)

    def __delitem__(self, key):
        '''Implements the "del self[]" operator.

        They key is sanitized such that it is looked up in the expected format.
        '''
        key = self._sanitize_key(key)
        return super().__delitem__(key)

    def __getitem__(self, key):
        '''Implements the "self[]" item getter operator.

        They key is sanitized such that it is looked up in the expected format.
        '''
        key = self._sanitize_key(key)
        return super().__getitem__(key)

    def __setitem__(self, key, item):
        '''Implements the "self[]" item setter operator.

        They key and item are sanitized and only allowed ones are permitted.
        '''
        key = self._sanitize_key(key)
        self._assert_key_allowed(key)
        item = self._sanitize_item(item)
        self._assert_item_allowed(item)
        return super().__setitem__(key, item)

    def _sanitize_key(self, key):
        '''Default key sanitizer method.

        Default implementation does nothing.

        Sub-classes are encouraged to redefine this method to suit their needs.

        Implementation is expected to attempt conversion of the key argument
        into appropriate types for keying into the dictionary. If conversion is
        not possible or not desired, the original key should be returned
        unchanged without raising an exception.

        Returns:
            key
        '''
        return key

    def _sanitize_item(self, item):
        '''Default item sanitizer method.

        Default implementation does nothing.

        Implementation is expected to attempt conversion of the item argument
        into appropriate types for storing into the dictionary. If conversion
        is not possible or not desired, the original item should be returned
        unchanged without raising an exception.

        Returns:
            item
        '''
        return item

    def _assert_key_allowed(self, key):
        '''Default key assertion method.

        Default implementation does nothing.

        Implementation is expected to raise a KeyError exception if the key is
        not allowed (such as an undesired value or type.)

        Returns:
            None
        '''
        pass

    def _assert_item_allowed(self, item):
        '''Default item assertion method.

        Default implementation does nothing.

        Implementation is expected to raise a ValueError exception if the item
        is not allowed (such as an undesired value or type.)

        Returns:
            None
        '''
        pass

    __marker = object()

    def pop(self, key, default=__marker):
        '''D.pop(k[,d]) -> v, remove specified key and return the corresponding value.
        If key is not found, d is returned if given, otherwise KeyError is raised.
        '''
        # If __missing__ is implemented, UserDict's pop (inherited from
        # MutableMapping) does not behave properly and missing items are
        # instantiated and popped immediately. This is a behavior differs
        # from defaultdict/dict's and is corrected here.
        key = self._sanitize_key(key)
        if default is self.__marker:
            return self.data.pop(key)
        else:
            return self.data.pop(key, default)

    def setdefault(self, key, default=None):
        '''D.setdefault(k[,d]) -> D.get(k,d), also set D[k]=d if k not in D'''
        # If __missing__ is implemented, UserDict's setdefault (inherited from
        # MutableMapping) does not behave properly and missing items are
        # instantiated instead of being set to the requested default value.
        # This is a behavior differs from defaultdict/dict's and is corrected
        # here.

        # Sanitize once to avoid 3 costly conversions in the worst case.
        key = self._sanitize_key(key)
        if key not in self:
            self[key] = default
        # Force a lookup even in default's case to return the sanitized item.
        return self[key]


class SubAttributesDict(SanitizedDict):
    '''Dictionary class appropriate for storing SubAttributes items.

    Used for storing SubAttributes and KeyedSubAttributes items in a
    dictionary structure.

    SubAttributesDict automatically instantiates missing items and points them
    to the parent object owning the dictionary so that the items can inherit
    their attributes from this parent.
    '''

    def __init__(self, cls, parent, parent_keys_attribute=None,
                 *args, **kwargs):
        '''Initialized a SubAttributesDict object.

        If the "cls" class passed as argument defines it's own `_sanitize_key`
        or `_assert_key_allowed` class methods, these will override the default
        implementations provided by SubAttributesDict. The `_sort_key` method
        can also be defined to provide a default key function to sort sequence
        or mapping values.

        Args:
            cls: Typically a SubAttributes or KeyedSubAttributes class or
                subclass. Can also be a function that returns appropriate
                items. Used to instantiate missing items.
            parent: The parent object from which items will inherit.
            parent_keys_attribute: Optional attribute name of the parent object
                which lists the currently allowed keys for this dictionary.
            args: Passed unchanged to the base class.
            kwargs: Passed unchanged to the base class.
        '''

        self._cls = cls
        self._parent = parent
        self._parent_keys_attribute = parent_keys_attribute

        func = getattr(self._cls, '_sanitize_key', None)
        if func:
            self._sanitize_key = func

        func = getattr(self._cls, '_assert_key_allowed', None)
        if func:
            self._assert_key_allowed = func

        func = getattr(self._cls, '_sort_key', None)
        if func:
            self._sort_key = func

        super().__init__(*args, **kwargs)

    def __iter__(self):
        '''Implement the iter(self) functionality.

        If a "parent_keys_attribute" attribute was provided on __init__, this
        attribute of the parent object will be queried and an iterator of the
        sanitized keys will be returned.

        Otherwise, the default iterator is returned representing the keys
        currently in the dictionary.

        Returns:
            iterator object
        '''
        parent_keys_attribute = self._parent_keys_attribute
        if parent_keys_attribute is None:
            return super().__iter__()
        keys = getattr(self._parent, parent_keys_attribute)
        return (self._sanitize_key(key) for key in keys)

    def __len__(self):
        '''Implement the len(self) functionality.

        If a "parent_keys_attribute" attribute was provided on __init__, this
        attribute of the parent object will be queried and it's length rturned.

        Returns:
            int
        '''
        parent_keys_attribute = self._parent_keys_attribute
        if parent_keys_attribute is None:
            return super().__len__()
        keys = getattr(self._parent, parent_keys_attribute)
        if not isinstance(keys, collections.abc.Sized):
            # Such as a generator
            keys = list(keys)
        return len(keys)

    def clear(self):
        '''Remove all items from the dictionary.

        Returns:
            None
        '''
        # UserDict's clear (inherited from MutableMapping) uses a series of
        # popitems calls which rely on interation of the remaining keys. If a
        # fixed list of keys is provided, it is possible that extra items (that
        # were previously allowed but not anymore) are left behind.

        # Invoke the default behavior, allowing mixin classes to intercept
        # normally.
        super().clear()
        # Clear any leftovers. No need to spend extra time checking if fixed
        # keys are in use.
        self.data.clear()

    def popitem(self):
        '''D.popitem() -> (k, v), remove and return some (key, value) pair
           as a 2-tuple; but raise KeyError if D is empty.
        '''
        # When a fixed list of keys is provided, UserDict's popitem (inherited
        # from MutableMapping) uses next(iter(self)) and so always pops the
        # first key, whether it exists or not. Also, since __missing__ is
        # implemented, an infinite loop is possible.
        parent_keys_attribute = self._parent_keys_attribute
        if parent_keys_attribute is None:
            return super().popitem()
        # Could use self.data.popitem() but since we have a list of keys, might
        # as well respect the order.
        keys = getattr(self._parent, parent_keys_attribute)
        for key in (self._sanitize_key(key) for key in keys):
            if key in self:
                return key, self.pop(key)
        raise KeyError

    def _sanitize_key(self, key):
        '''Default key sanitizing implementation.

        The "name" attribute of key objects derived from genie.conf.Base is
        used in place of the object.
        '''
        if isinstance(key, Base):
            key = getattr(key, 'name', key)
        return key

    def _assert_key_allowed(self, key):
        '''Default implementation that checks if a key is allowed.

        If a "parent_keys_attribute" attribute was provided on __init__, this
        attribute of the parent object will be queried and a key not in this
        list will be rejected.

        If the function/class used to instantiate missing items has a
        "allowed_keys" attribute, this attribute is queried and a key not in
        this list will be rejected.
        '''
        parent_keys_attribute = self._parent_keys_attribute
        if parent_keys_attribute is not None:
            keys = getattr(self._parent, parent_keys_attribute)
            allowed_keys = [self._sanitize_key(key) for key in keys]
            if key not in allowed_keys:
                raise KeyError(
                    '{cls}\'s parent only accepts {allowed_keys}, not {key!r}'.
                    format(cls=self._cls.__name__,
                           allowed_keys=allowed_keys,
                           key=key))
        allowed_keys = getattr(self._cls, 'allowed_keys', None)
        if allowed_keys is not None:
            # Allowed_keys from the class are expected to be already sanitized.
            # allowed_keys = [self._sanitize_key(key) for key in allowed_keys]
            if key not in allowed_keys:
                raise KeyError(
                    '{cls} only accepts {allowed_keys}, not {key!r}'.
                    format(cls=self._cls.__name__,
                           allowed_keys=allowed_keys,
                           key=key))

    def __missing__(self, key):
        '''Instantiate a new item when key is not in the dictionary.

        The function/class used to instantiate missing items is called with the
        "parent" keyword argument, passing it the same parent object that was
        used on initialization of SubAttributesDict. If it is a subclass of
        KeyedSubAttributes, it will also be provided with the "key" keyword
        argument.
        '''
        # Item is missing at specified key; Create one.
        self._assert_key_allowed(key)
        if isclass(self._cls) and issubclass(self._cls, KeyedSubAttributes):
            item = self._cls(parent=self._parent, key=key)
        else:
            item = self._cls(parent=self._parent)
        self[key] = item
        return self[key]


class AttributesHelper(object):
    '''Helper class used to select accessible/allowed attributes of an object.

    '''

    def __init__(self, obj, attributes=None):
        '''Initialize a new AttributesHelper object.

        Args:
            obj: The source object from which attributes are to be selected.
            attributes: The attributes selection specification.

        Attributes selection specification:

        The "attributes" argument is used to create filters that limit the set
        of accessible/allowed attributes. It can take several forms:

            - None: The None "wildcard" value means "no restriction". When
                using None, all attributes are allowed from the source object
                or any sub-attributes.

            - AttributesHelper: The copy constructor. The specification from
                this other AttributesHelper object is copied over. As a
                precaution against misuse, it is verified that both the other
                AttributesHelper and this one refer to the same source object.

            - str: An attribute name represented as a string. The string is
                split on '__' to allow specifying sub-attributes.

            - sequence: (list, tuple, ...) The first element represents
                attributes applicable to the source object, further elements
                apply to sub-attributes. Each element of the sequence can be a
                string or a sequence of elements. An empty sequence is
                equivalent to a single empty element, which menas "no more
                attributes".

            - mapping: (dict, ...) Keys represent attribute names applicable to
                the source object, values represent specifications for
                sub-attributes. The special '*' key represents defaults for any
                attribute name that is not mapped.

        Example:

            >>> a = SimpleNamespace(a1=1, a2=2, aN=None,
            ...     b=SimpleNamespace(b1=1, b2=2, bN=None))

            >>> attributes = AttributesHelper(a)
            >>> attributes.value('a1')
            1
            >>> attributes.value('a2')
            2
            >>> attributes.value('aN')
            # None, as expected
            >>> sub, attributes2 = attributes.namespace('b')
            >>> sub
            namespace(b1=1, b2=2, bN=None)
            >>> attributes2.value('b1')
            1
            >>> attributes2.value('b2')
            2
            >>> attributes2.value('bN')
            # None, as expected

            >>> attributes = AttributesHelper(a, attributes='a1')
            >>> attributes.value('a1')
            1
            >>> attributes.value('a2')
            # None, not allowed
            >>> attributes.value('aN')
            # None, not allowed
            >>> sub, attributes2 = attributes.namespace('b')
            >>> sub
            # None, not allowed

            >>> attributes = AttributesHelper(a, attributes='b__b1')
            >>> attributes.value('a1')
            # None, not allowed
            >>> attributes.value('a2')
            # None, not allowed
            >>> attributes.value('aN')
            # None, not allowed
            >>> sub, attributes2 = attributes.namespace('b')
            >>> sub
            namespace(b1=1, b2=2, bN=None)
            >>> attributes2.value('b1')
            1
            >>> attributes2.value('b2')
            # None, not allowed
            >>> attributes2.value('bN')
            # None, not allowed

        '''

        self.obj = obj
        self.attributes = self._create_attributes(attributes)

    def _create_attributes(self, attributes):
        '''Internal method to convert an attributes specification from any of
        the supported formats into a dictionary.

        Only the keys are transformed, items are kept as raw sub-attributes to
        be passed to _create_attributes again as needed.

        Returns:
           new attributes dictionary
       '''

        if attributes is None:
            # wildcard -- everything allowed
            return None
        elif isinstance(attributes, AttributesHelper):
            # ~Copy constructor
            if attributes.obj is not None and attributes.obj is not self.obj:
                raise ValueError("Instantiating {} for a different object!"\
                                 .format(type(self).__name__))
            return copy(attributes.attributes)
        elif isinstance(attributes, str):
            # key -> {key: None}
            # key__attr -> {key: attr}
            l = attributes.split('__', 1)
            return self._create_attributes({
                l[0]: l[1] if len(l) > 1 else None,
            })
        elif isinstance(attributes, collections.abc.Sequence):
            if not attributes:
                # empty sequence => no more attributes
                return {}
            else:
                keys = attributes[0]
                sub_attributes = attributes[1:] \
                    if len(attributes) > 1 else None
                if (isinstance(keys, collections.abc.Sequence) and
                        not isinstance(keys, str)):
                    # ([keys], sub-attributes, ...)
                    return self._create_attributes({
                        key: sub_attributes for key in keys})
                else:
                    # (key, sub-attributes, ...)
                    return self._create_attributes({keys: sub_attributes})
        elif isinstance(attributes, collections.abc.Mapping):
            # {key: sub-attributes, ...[, '*': defaults]}
            if '*' in attributes:
                def_subattributes = attributes['*']
                attributes = defaultdict(
                    (lambda: def_subattributes), attributes)
                del attributes['*']
            else:
                attributes = copy(attributes)
            return attributes
        else:
            # key (in another format, such as an int index)
            return {attributes: None}

    def value_generator(self, name,
                        force=False, default=_marker, inherited=None):
        '''Generator to select an attribute's value.

        Use with Python's "for" statement. The wrapped block of code will
        execute once only if the requested attribute is allowed, exists and
        is valid.

        This method returns a python generator that yields at most 1 value.

        Example:
            for value in helper.value_generator('router_id'):
                configurations.append_line('router-id {}'.format(value))
        '''

        log.debug('value_generator(name=%r, force=%r, default=%r, \
                  inherited=%r)',
                  name, force, default, inherited)
        # name allowed?
        if (not force and
                self.attributes is not None and
                name not in self.attributes):
            return  # Not yielding anything

        try:
            value = getattr(self.obj, name)
        except AttributeError:
            value = None
            # TODO inherited?
        else:
            # support AttributesInheriter.isinherited
            if (inherited is not None and
                    self.obj.isinherited(name) is not inherited):
                return  # Not yielding anything

        if value is None:
            if default is _marker:
                return  # Not yielding anything
            value = default

        log.debug('  yield: %r', value)
        yield value

    def value(self, *args, **kwargs):
        '''Select an attribute's value.

        Use with Python's "=" operator to retrieve an attribute if the
        requested attribute is allowed, exists and is valid, else None is
        returned.

        Example:
            value = helper.value('router_id')
            if value is not None:
                configurations.append_line('router-id {}'.format(value))
        '''

        for value in self.value_generator(*args, **kwargs):
            return value
        return None

    def namespace_generator(self, name,
                            force=False, inherited=None):
        '''Generator to select an attribute's namespace.

        Use with Python's "for" statement. The wrapped block of code will
        execute once only if the requested namespace is allowed, exists and
        is valid. It will return a tuple of 2 elements:
            - namespace value
            - new AttributesHelper instance

        This method returns a python generator that yields at most 1 tuple.

        Example:
            for ns, attributes2 in helper.namespace_generator('bgp'):
                configurations += ns.build_config(apply=False,
                                                  attributes=attributes2)
        '''

        log.debug('namespace_generator(name=%r, force=%r, inherited=%r)',
                  name, force, inherited)

        for namespace in self.value_generator(name, force=force,
                                              inherited=inherited):

            sub_attributes = self.attributes.get(name)\
                if self.attributes is not None else None
            sub_attributes = AttributesHelper(obj=namespace,
                                              attributes=sub_attributes)

            log.debug('  yield: %r, %r', namespace, sub_attributes)
            yield namespace, sub_attributes

    def namespace(self, name,
                  force=False, inherited=None):
        '''Select an attribute's namespace.

        If the requested attribute is allowed, exists and is value, it will
        return a tuple of 2 elements:
            - namespace value
            - new AttributesHelper instance
        Otherwise, it returns a tuple containing 2 None elements.

        Example:
            ns, attributes2 = helper.namespace_generator('bgp')
            if ns is not None:
                configurations += ns.build_config(apply=False,
                                                  attributes=attributes2)
        '''

        log.debug('namespace(name=%r, force=%r, inherited=%r)',
                  name, force, inherited)

        for namespace, sub_attributes in self.namespace_generator(
                name, force=force, inherited=inherited):
            return namespace, sub_attributes
        return (None, None)

    def sequence_values(self, name, values=None, cmp=None,
                        force=False, inherited=None, sort=False):
        '''Iterator for a sequence attribute's values.

        Use with Python's "for" statement. The wrapped block of code will
        execute for each of the sequence's values each time returning a tuple
        of 2 elements:
            - value
            - new AttributesHelper instance
        If the values argument is specified, only values listed will be
        iterated.

        Example:
            for value, attributes2 in helper.sequence_values('evis',
                    values=self.evis):
                configurations += value.build_config(apply=False,
                    attributes=attributes2).splitlines()
        '''

        log.debug('sequence_values(name=%r, values=%r, force=%r, \
                  inherited=%r, sort=%r)',
                  name, values, force, inherited, sort)
        for sequence, allowed_sub_attributes \
                in self.namespace_generator(name, force=force,
                                            inherited=inherited):

            if not isinstance(sequence, collections.abc.Iterable):
                raise ValueError('attribute {} is not iterable: {!r}'\
                                 .format(name, sequence))

            allowed_sub_attributes = allowed_sub_attributes.attributes
            if allowed_sub_attributes is None:
                allowed_sub_attributes = defaultdict(type(None))

            if values is None:
                values = list(sequence)
            else:
                values = set(values)
                values = [value for value in sequence if value in values]
            log.debug('  values = %r', values)

            log.debug('  allowed_sub_attributes = %r', allowed_sub_attributes)

            if sort is not False:
                try:
                    _sort_key = None \
                        if sort is True else sort
                    values = sorted(values, key=_sort_key)
                except:
                    pass

            for value in values:
                try:
                    sub_attributes = allowed_sub_attributes[value]
                except KeyError:
                    if cmp is not None:
                        try:
                            for key, sub_attributes \
                                    in allowed_sub_attributes.items():
                                if cmp(value, key):
                                    break
                            else:
                                continue
                        except:
                            continue
                    else:
                        continue
                attributes2 = AttributesHelper(obj=value,
                                               attributes=sub_attributes)
                log.debug('  yield: %r, %r', value, attributes2)
                yield value, attributes2

    def mapping_items(self, name, keys=None, cmp=None,
                      force=False, inherited=None, sort=False):
        '''Iterator for a mapping attribute's items.

        Use with Python's "for" statement. The wrapped block of code will
        execute for each of the mapping's items each time returning a tuple of
        3 elements:
            - key
            - value
            - new AttributesHelper instance
        If the keys argument is specified, only items for the keys listed will
        be iterated.

        Example:
            for key, value, attributes2 in helper.mapping_items('device_attr',
                    keys=self.devices):
                cfgs[key] = attr.build_config(apply=False,
                                              attributes=attributes2)
        '''

        log.debug('mapping_items(name=%r, keys=%r, force=%r, \
                  inherited=%r, sort=%r)',
                  name, keys, force, inherited, sort)
        for mapping, allowed_sub_attributes \
                in self.namespace_generator(name, force=force,
                                            inherited=inherited):

            if not isinstance(mapping, collections.abc.Mapping):
                raise ValueError('attribute {} is not a mapping: {!r}'\
                                 .format(name, mapping))

            allowed_sub_attributes = allowed_sub_attributes.attributes
            if allowed_sub_attributes is None:
                allowed_sub_attributes = defaultdict(type(None))

            # support SubAttributesDict._sanitize_key
            _sanitize_key = getattr(mapping, '_sanitize_key', None)

            if keys is None:
                keys = set(mapping.keys())
            else:
                keys = set(keys)
                if _sanitize_key:
                    keys = set(_sanitize_key(key) for key in keys)
            log.debug('  keys = %r', keys)

            if _sanitize_key:
                old_items = list(allowed_sub_attributes.items())
                allowed_sub_attributes.clear()
                allowed_sub_attributes.update({
                    _sanitize_key(key): value for key, value in old_items})
            log.debug('  allowed_sub_attributes = %r', allowed_sub_attributes)

            if sort is not False:
                try:
                    _sort_key = getattr(mapping, '_sort_key', None) \
                        if sort is True else sort
                    keys = sorted(keys, key=_sort_key)
                except:
                    pass

            for key in keys:
                try:
                    value = mapping[key]
                except KeyError:
                    continue
                try:
                    sub_attributes = allowed_sub_attributes[key]
                except KeyError:
                    if cmp is not None:
                        try:
                            for key, sub_attributes \
                                    in allowed_sub_attributes.items():
                                if cmp(value, key):
                                    break
                                else:
                                    continue
                        except:
                            continue
                        else:
                            continue
                    continue
                attributes2 = AttributesHelper(obj=value,
                                               attributes=sub_attributes)
                log.debug('  yield: %r, %r, %r', key, value, attributes2)
                yield key, value, attributes2

    def mapping_keys(self, *args, **kwargs):
        '''Iterator for a mapping attribute's keys.

        Similar to mapping_items but returns tuples of 2 elements:
            - key
            - new AttributesHelper instance
        '''
        for key, value, attributes2 in self.mapping_items(*args, **kwargs):
            yield key, attributes2

    def mapping_values(self, *args, **kwargs):
        '''Iterator for a mapping attribute's values.

        Similar to mapping_items but returns tuples of 2 elements:
            - value
            - new AttributesHelper instance
        '''
        for key, value, attributes2 in self.mapping_items(*args, **kwargs):
            yield value, attributes2

    def __eq__(self, other):
        '''Equality operation, for unittest purposes'''
        if not isinstance(other, AttributesHelper):
            return NotImplemented
        return self.obj is other.obj and self.attributes == other.attributes

    def __repr__(self):
        return '{cls}(obj={obj!r}, attributes={a!r}'.format(
            cls=type(self).__name__,
            obj=self.obj,
            a=self.attributes)

    @property
    def iswildcard(self):
        '''Return True if wildcard processing is in effect and all attributes
        are allowed.

        Example:
            >>> attributes = AttributesHelper(self)
            >>> attributes.iswildcard
            True
            >>> attributes = AttributesHelper(self, attributes=None)
            >>> attributes.iswildcard
            True
            >>> attributes = AttributesHelper(self, attributes='a__b')
            >>> attributes.iswildcard
            False
        '''
        return self.attributes is None

    class Formatter(string.Formatter):
        '''Internal string formatter class that only accepts formatting strings
        composed of allowed attributes.

        See AttributesHelper.format.
        '''

        class ValueNotAllowed(Exception):
            '''Internal exception used to quickly get out of a multiple call
            stack levels when a value is not allowed.
            '''
            pass

        def __init__(self, attributes):
            '''Formatter initializer.

            Args:
                attributes: The AttributesHelper instance from which attributes are queried
            '''
            self.attributes = attributes

        def get_value(self, key, args, kwargs):
            '''Retrieve a given field value.

            The key argument will be either an integer or a string. If it is an
            integer, it represents the index of the positional argument in
            args; if it is a string, then it represents a named argument in
            kwargs.

            If kwargs does not contain a the named argument, the
            AttributesHelper instance is queried using it's value(key) method.

            Argumentes to be passed to AttributesHelper.value can be specified in
            kwargs, such as 'force', 'default' and 'inherited'. The 'transform'
            argument can be used to perform extra transformations on the value.
            All these keywords arguments may be prefixed with '<key>_' to be
            more targeted and unambiguous.

            Raises:
                ValueNotAllowed if the AttributesHelper does not allow the value

            Return:
                value
            '''
            if isinstance(key, int):
                # Index of the positional argument in args
                return args[key]
            else:
                try:
                    # Named argument in kwargs
                    return kwargs[key]
                except KeyError:
                    # Query the AttributesHelper instance.
                    # Grab arguments to pass on to AttributesHelper.value
                    value_kwargs = {}
                    for arg in ('force', 'default', 'inherited'):
                        try:
                            value_kwargs[arg] = kwargs[arg + '_' + key]
                        except KeyError:
                            try:
                                value_kwargs[arg] = kwargs[arg]
                            except KeyError:
                                pass
                    for value in self.attributes.value_generator(
                            key, **value_kwargs):
                        # AttributesHelper allowed the key attribute.
                        # Perform any requested transformations
                        try:
                            transform = kwargs['transform_' + key]
                        except KeyError:
                            transform = kwargs.get('transform', None)
                        if transform is not None:
                            if isinstance(transform, collections.abc.Mapping):
                                try:
                                    value = transform[value]
                                except KeyError as e:
                                    warnings.warn(
                                        '{} = {!r}: {}'.format(key, value, e),
                                        UnsupportedAttributeWarning)
                                    raise self.ValueNotAllowed(key)
                            else:
                                try:
                                    value = transform(value)
                                except (ValueError, TypeError) as e:
                                    warnings.warn(
                                        '{} = {!r}: {}'.format(key, value, e),
                                        UnsupportedAttributeWarning)
                                    raise self.ValueNotAllowed(key)
                            if value is None:
                                raise self.ValueNotAllowed(key)
                        return value
                    else:
                        # AttributesHelper did not allow the key attribute.
                        raise self.ValueNotAllowed(key)

    def format(self, format_string, *args, **kwargs):
        '''Perform a string formatting operation.

        Using standard Python Format String Syntax, formats a string by
        substituting fields with values from arguments or from attributes of
        the source object.

        Args:
            format_string: Standard Python Format String Syntax.
            force, default, inherited: arguments to pass to the
                AttributesHelper.value method to control argument selection.
                (can be prefixed with '<field>_')
            transform: function or mapping of functions to apply
                transformations to value. (can be prefixed with '<field>_')
            args: List of positional arguments for index fields. 'first arg is {0}'
            kwargs: List of keyword arguments for identifier fields. e.g.: 'my arg is {my_arg}'

        Return:
            The formatted string if all fields are allowed.
            The empty string ('') if any field is not allowed.

        Example:

            >>> vrf = Vrf('blue', description='a vrf')
            >>> attributes = AttributesHelper(vrf, attributes='description')
            >>> attributes.format('vrf context {name}')
            ''
            >>> attributes.format('vrf context {name}', force=True)
            'vrf context blue'
            >>> attributes.format('description {description}')
            'description a vrf'
            >>> vrf.description = None
            >>> attributes.format('description {description}')
            ''
            >>> attributes.format('my arg {my_arg}', my_arg=123)
            'my arg 123'
            >>> attributes.format('my arg 0x{my_arg:08x}', my_arg=123)
            'my arg 0x0000007b'
        '''
        formatter = self.Formatter(self)
        try:
            return formatter.format(format_string, *args, **kwargs)
        except formatter.ValueNotAllowed:
            return ''

    def format_dict(self, format_string_dict, *args, **kwargs):
        '''Perform string formatting operations on both keys and items of a dictionary.

        Return:
            Dictionary of formatted keys and items.
            En empty dictionary if any attribute is not allowed.
        '''
        formatter = self.Formatter(self)
        try:
            return {
                formatter.format(k, *args, **kwargs):
                formatter.format(v, *args, **kwargs)
                for k, v in format_string_dict.items()}
        except formatter.ValueNotAllowed:
            return {}

    def format_list(self, format_string_list, *args, **kwargs):
        '''Perform string formatting operations on all elements of a list or iterable.

        Return:
            List of formatted items.
            En empty list if any attribute is not allowed.
        '''
        formatter = self.Formatter(self)
        try:
            return [
                formatter.format(e, *args, **kwargs)
                for e in format_string_list]
        except formatter.ValueNotAllowed:
            return []

class AttributesHelper2(AttributesHelper):
    ''' 
    Only difference with AttributesHelper is to allow instantiate with 
    different object
    '''
    def _create_attributes(self, attributes):
        '''Internal method to convert an attributes specification from any of
        the supported formats into a dictionary.

        Only the keys are transformed, items are kept as raw sub-attributes to
        be passed to _create_attributes again as needed.

        Returns:
           new attributes dictionary
       '''

        if attributes is None:
            # wildcard -- everything allowed
            return None
        elif isinstance(attributes, AttributesHelper):
            # ~Copy constructor
            return copy(attributes.attributes)
        elif isinstance(attributes, str):
            # key -> {key: None}
            # key__attr -> {key: attr}
            l = attributes.split('__', 1)
            return self._create_attributes({
                l[0]: l[1] if len(l) > 1 else None,
            })
        elif isinstance(attributes, collections.abc.Sequence):
            if not attributes:
                # empty sequence => no more attributes
                return {}
            else:
                keys = attributes[0]
                sub_attributes = attributes[1:] \
                    if len(attributes) > 1 else None
                if (isinstance(keys, collections.abc.Sequence) and
                        not isinstance(keys, str)):
                    # ([keys], sub-attributes, ...)
                    return self._create_attributes({
                        key: sub_attributes for key in keys})
                else:
                    # (key, sub-attributes, ...)
                    return self._create_attributes({keys: sub_attributes})
        elif isinstance(attributes, collections.abc.Mapping):
            # {key: sub-attributes, ...[, '*': defaults]}
            if '*' in attributes:
                def_subattributes = attributes['*']
                attributes = defaultdict(
                    (lambda: def_subattributes), attributes)
                del attributes['*']
            else:
                attributes = copy(attributes)
            return attributes
        else:
            # key (in another format, such as an int index)
            return {attributes: None}