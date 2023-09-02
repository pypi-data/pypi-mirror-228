
__all__ = (
    'mixedmethod',
    'managedattribute',
)

import functools
import importlib.util
import sys
import enum
import weakref
import builtins


class mixedmethod(object):
    """This decorator mutates a function defined in a class into a 'mixed'
    class and instance method.

    Usage:

        class Spam:
            @mixedmethod
            def egg(self, cls, *args, **kwargs):
                if self is None:
                    pass
                    # executed if egg was called as a class method
                    # (eg. Spam.egg())
                else:
                    pass
                    # executed if egg was called as an instance method
                    # (eg. instance.egg())

    The decorated methods need 2 implicit arguments: self and cls, the
    former being None when there is no instance in the call. This follows
    the same rule as __get__ methods in python's descriptor protocol.

    From: https://www.daniweb.com/software-development/python/code/406393/mixedmethod-mixes-class-and-instance-method-into-one-
    Modified by Jean-Sebastien Trottier <strottie@cisco.com>
    """

    def __init__(self, func):
        self.func = func
        self.__doc__ = func.__doc__
        # support for abstract methods
        self.__isabstractmethod__ = \
            bool(getattr(func, '__isabstractmethod__', False))

    def __get__(self, inst, cls):
        return functools.partial(self.func, inst, cls)

class managedattribute(object):
    '''Descriptor that declares managed attributes.

    Managed attributes lets you finely control all aspects of a class member
    variable. Think of it as a extended version of Python's `property`
    descriptor.

    Some benefits when compared to using standard class member variables:

        - Document member variables.
        - Keep declaration and initialization implementation close together.
        - Perform transformations and checking on set.
        - Perform transformations on get.

    Usage:

        - All you already know about Python's `property` descriptor works the
          same with managedattribute: Using as a decorator or directly
          instantiated, concept of getter, setter and deleter methods,
          documentation support, ...

        - The attribute name must be known, either provided using the 'name'
          argument or based on the getter method name when used as a decorator.

        - managedattribute provides a default getter that supports default
          values, initializer values and applying transformations. It is
          possible to replace the getter with your own but it is preferable to
          control it's behavior by specifying the 'gettype', 'default', 'init'
          and other related arguments when creating the managedattribute.

        - managedattribute provides a default setter that supports checking
          values and applying transformations. It is possible to replace the
          setter with your own but is preferable to control it's behavior by
          specifying the 'type' argument when creating the managedattribute.

        - managedattribute provides a default deleter that does nothing more
          than delete the value. It is possible to replace the deleter with
          your own.

    Typical uses:

        class MyClass(object):

            # An attribute that behaves normally with the added bonus that it
            # gets documented:
            attr = managedattribute(name='attr',
                                    doc='My attribute')

            # A read-only attribute with a default value. If needed, you may
            # internally set the '_attr' attribute (name prefixed by '_') of
            # your object instance to change it.
            attr = managedattribute(name='attr',
                                    read_only=True,
                                    default='my default')

            def some_method(self):
                self._attr = 'new value'

            # An attribute with a meaningful default value computed at run-time
            # using a defaulter method:
            attr = managedattribute(name='attr')

            @attr.defaulter
            def attr(self):
                return self.food_items - self.gone_bad_items

            # An attribute with an initializer. Instead of initializing the
            # value far away in your class's __init__, the initializer code is
            # kept close and only called once on first access:
            attr = managedattribute(name='attr')

            @attr.initter
            def attr(self):
                return random.randrange(100)

            # Alternatively, for simpler initializer calls, a function can be
            # provided directly:
            attr = managedattribute(name='attr',
                                    finit=dict)

            # An attribute that only accepts values that can be converted to a
            # certain type on set:
            attr = managedattribute(name='attr',
                                    type=int)

            # More advanced type-checking and transformations can be performed
            # by combining and chaining multiple rules. managedattribute
            # provides several 'test_*' functions specifically for this use but
            # any callable will do:
            attr = managedattribute(
                name='attr',
                type=(
                    None,
                    managedattribute.test_isinstance(Interface),
                    IPv4Address),
                doc='I only accept None, Interface object instances and'
                    'anything that converts to a IPv4 address')

            # An attribute that performs transformations on get to present a
            # different value than what is stored internally. For example,
            # presenting a read-only frozenset while storing a mutable set
            # internally:
            attr = managedattribute(name='attr',
                                    finit=set,
                                    read_only=True,
                                    gettype=frozenset)
    '''

    class Constants(enum.Enum):
        '''Internal contants.'''
        # not_specified: Easily detect unspecified arguments in function calls
        not_specified = 1

    # Copy all the Constants enum values as members of the managedattribute
    # class
    locals().update(Constants.__members__)

    class DefaultActions(enum.Enum):
        '''Possible actions to take when a default attribute value is required.

        Enum values correspond to the __init__ parameters that enable the
        specific action.
        '''
        function_return_default = 'fdef'
        function_set_init = 'finit'
        method_return_default = 'fdef_method'
        method_set_init = 'finit_method'
        value_return_default = 'default'
        value_set_init = 'init'

    @staticmethod
    def test_is(other):
        '''Create a transformation function that allows only the specified
        object.

        Use with the managedattribute 'type' argument to accept only specific
        objects (where `value is other`)

        Upon success, the resulting transformation function returns the value
        unchanged.

        Args:
            other: The other object to compare for identity.

        Example:

            attr = managedattribute(
                name='attr',
                type=managedattribute.test_is(True))
        '''

        msg = 'Not %r.' % (other,)

        def f(value):
            if value is not other:
                raise ValueError(msg)
            return value

        return f

    @staticmethod
    def test_isinstance(classinfo):
        '''Create a transformation function that allows only an object instance
        of the specified classes.

        Use with the managedattribute 'type' argument to accept only an
        instance of the specified classes or a subclass thereof (where
        `isinstance(value, classinfo)`)

        Upon success, the resulting transformation function returns the value
        unchanged.

        Args:
            classinfo: a single class or a tuple of classes (like Python's
                isinstance function)

        Example:

            attr = managedattribute(
                name='attr',
                type=managedattribute.test_isinstance(Interface))

            attr = managedattribute(
                name='attr',
                type=managedattribute.test_isinstance((
                    IPv4InterfaceRange,
                    IPv6InterfaceRange)))
        '''

        if not classinfo:
            raise ValueError(classinfo)
        isinstance(None, classinfo)  # Just make sure Python likes it
        msg = 'Not an instance of '
        if type(classinfo) is tuple:
            if len(classinfo) > 1:
                msg += ', '.join([c.__name__ for c in classinfo[0:-1]])
                msg += ' or '
            msg += classinfo[-1].__name__
        else:
            msg += classinfo.__name__
        msg += '.'

        def f(value):
            if not isinstance(value, classinfo):
                raise ValueError(msg)
            return value

        return f

    @staticmethod
    def test_istype(classinfo):
        '''Create a transformation function that allows only objects of the
        specified types.

        Use with the managedattribute 'type' argument to accept only an object
        of the specified types (but not subclasses) (where `type(value) is [in]
        classinfo`)

        Upon success, the resulting transformation function returns the value
        unchanged.

        Args:
            classinfo: a single class or a tuple of classes (like Python's
                isinstance function)

        Example:

            attr = managedattribute(
                name='attr',
                type=managedattribute.test_istype(int))

            attr = managedattribute(
                name='attr',
                type=managedattribute.test_istype((int, str)))
        '''

        if not classinfo:
            raise ValueError(classinfo)
        isinstance(None, classinfo)  # Just make sure Python likes it
        msg = 'Not of type '
        if type(classinfo) is tuple:
            if len(classinfo) > 1:
                msg += ', '.join([c.__name__ for c in classinfo[0:-1]])
                msg += ' or '
            msg += classinfo[-1].__name__
        else:
            msg += classinfo.__name__
        msg += '.'

        if type(classinfo) is tuple:

            def f(value):
                if type(value) not in classinfo:
                    raise ValueError(msg)
                return value

        else:

            def f(value):
                if type(value) is not classinfo:
                    raise ValueError(msg)
                return value

        return f

    @staticmethod
    def test_issubclass(classinfo):
        '''Create a transformation function that allows only a subclass of the
        specified classes.

        Use with the managedattribute 'type' argument to accept only a
        subclass of the specified classes (where `issubclass(value, classinfo)`)

        Upon success, the resulting transformation function returns the value
        unchanged.

        Args:
            classinfo: a single class or a tuple of classes (like Python's
                issubclass function)

        Example:

            attr = managedattribute(
                name='attr',
                type=managedattribute.test_issubclass(Interface))

            attr = managedattribute(
                name='attr',
                type=managedattribute.test_issubclass((
                    collections.Iterable,
                    collections.Mapping))
        '''

        if not classinfo:
            raise ValueError(classinfo)
        issubclass(object, classinfo)  # Just make sure Python likes it
        msg = 'Not a subclass of '
        if type(classinfo) is tuple:
            if len(classinfo) > 1:
                msg += ', '.join([c.__name__ for c in classinfo[0:-1]])
                msg += ' or '
            msg += classinfo[-1].__name__
        else:
            msg += classinfo.__name__
        msg += '.'

        def f(value):
            try:
                if not issubclass(value, classinfo):
                    raise ValueError(msg)
            except TypeError:
                # TypeError: issubclass() arg 1 must be a class
                raise ValueError(msg)
            return value

        return f

    @staticmethod
    def test_in(container):
        '''Create a transformation function that allows only an object
        contained in the specified container.

        Use with the managedattribute 'type' argument to accept only an object
        contained in the specified container (where `value in container`)

        Upon success, the resulting transformation function returns the value
        unchanged.

        Args:
            container: Any container, such as an iterable (list, tuple, set,
                ...), range, ...

        Example:

            attr = managedattribute(
                name='attr',
                type=managedattribute.test_in({1, 2, 3}))

            attr = managedattribute(
                name='attr',
                type=managedattribute.test_in(range(10)))
        '''

        msg = 'Not in %r.' % (container,)

        def f(value):
            if value not in container:
                raise ValueError(msg)
            return value

        return f

    @staticmethod
    def test_set_of(transforms):
        '''Create a transformation function that allows any iterable whose
        items are accepted by the specified other transformations and then
        converted to a set.

        Use with the managedattribute 'type' argument to accept any iterable
        and convert it to a set, as required.

        Upon success, the resulting transformation function returns a `set` of
        the (possibly further transformed) items.

        Args:
            transforms: Transformation functions (single or tuple thereof) to
                apply to each item of the iterable value.

        Example:

            attr = managedattribute(
                name='attr',
                type=managedattribute.test_set_of(AddressFamily))

            attr = managedattribute(
                name='attr',
                type=managedattribute.test_set_of((
                    None,
                    managedattribute.test_isinstance(Vrf),
                )))
        '''

        if type(transforms) is not tuple:
            transforms = (transforms,)
        if not transforms:
            raise ValueError('Empty tuple of transformations.')

        def f(value):
            value = iter(value)  # test iterable
            try:
                value = {
                    managedattribute._transform(e, transforms)
                    for e in value}
            except ValueError as e:
                raise ValueError('Not cast to set (%s).' % (e,))
            return value

        return f

    @staticmethod
    def test_list_of(transforms):
        '''Create a transformation function that allows any iterable whose
        items are accepted by the specified other transformations and then
        converted to a list.

        Use with the managedattribute 'type' argument to accept any iterable
        and convert it to a list, as required.

        Upon success, the resulting transformation function returns a `list` of
        the (possibly further transformed) items.

        Args:
            transforms: Transformation functions (single or tuple thereof) to
                apply to each item of the iterable value.

        Example:

            attr = managedattribute(
                name='attr',
                type=managedattribute.test_list_of(AddressFamily))

            attr = managedattribute(
                name='attr',
                type=managedattribute.test_list_of((
                    None,
                    managedattribute.test_isinstance(Vrf),
                )))
        '''

        if type(transforms) is not tuple:
            transforms = (transforms,)
        if not transforms:
            raise ValueError('Empty tuple of transformations.')

        def f(value):
            value = iter(value)  # test iterable
            try:
                value = [
                    managedattribute._transform(e, transforms)
                    for e in value]
            except ValueError as e:
                raise ValueError('Not cast to list (%s).' % (e,))
            return value

        return f

    @staticmethod
    def test_tuple_of(transforms):
        '''Create a transformation function that allows any iterable whose
        items are accepted by the specified other transformations and then
        converted to a tuple.

        Use with the managedattribute 'type' argument to accept any iterable
        and convert it to a tuple, as required.

        Upon success, the resulting transformation function returns a `tuple`
        of the (possibly further transformed) items.

        Args:
            transforms: Transformation functions (single or tuple thereof) to
                apply to each item of the iterable value.

        Example:

            attr = managedattribute(
                name='attr',
                type=managedattribute.test_tuple_of(AddressFamily))

            attr = managedattribute(
                name='attr',
                type=managedattribute.test_tuple_of((
                    None,
                    managedattribute.test_isinstance(Vrf),
                )))
        '''

        if type(transforms) is not tuple:
            transforms = (transforms,)
        if not transforms:
            raise ValueError('Empty tuple of transformations.')

        def f(value):
            value = iter(value)  # test iterable
            try:
                value = tuple(
                    managedattribute._transform(e, transforms)
                    for e in value)
            except ValueError as e:
                raise ValueError('Not cast to tuple (%s).' % (e,))
            return value

        return f

    @staticmethod
    def test_auto_ref(transforms):
        '''Create a transformation function that allows any object accepted by
        the specified other transformations and then returns a weak reference
        of it.

        Use with the managedattribute 'type' argument to create weak
        references.

        Upon success, the resulting transformation function returns a weak
        reference of the (possibly further transformed) value.

        Tip: Use with gettype=managedattribute.auto_unref

        Args:
            transforms: Transformation functions (single or tuple thereof) to
                apply to the value.

        Example:

            attr = managedattribute(
                name='attr',
                type=managedattribute.test_auto_ref(
                    managedattribute.test_isinstance(Device)),
                gettype=managedattribute.auto_unref)

            attr = managedattribute(
                name='attr',
                type=managedattribute.test_auto_ref((
                    None,
                    managedattribute.test_isinstance(Device))),
                gettype=managedattribute.auto_unref)
        '''

        if transforms is not None:
            if type(transforms) is not tuple:
                transforms = (transforms,)
            if not transforms:
                raise ValueError('Empty tuple of transformations.')

            def f(value):
                value = managedattribute._transform(value, transforms)
                return managedattribute.auto_ref(value)

            return f
        else:
            return managedattribute.auto_ref

    @staticmethod
    def auto_ref(value):
        '''Return a weak reference of the value.

        Use with the managedattribute 'type' argument to automatically create
        weak references.

        There are certain types of objects for which a weak reference cannot be
        created (None, int, ...). For those cases, the original value is
        returned as-is.

        Tip: Use with gettype=managedattribute.auto_unref

        Return:
            weakref.ref(value) or value

        Args:
            value: The value to create a weak reference of.
        Example:

            attr = managedattribute(
                name='attr',
                type=managedattribute.auto_ref,
                gettype=managedattribute.auto_unref)
        '''

        try:
            value = weakref.ref(value)
        except TypeError:
            pass
        return value

    @staticmethod
    def auto_unref(value):
        '''Return the referent object the weak reference value is pointing to.

        Use with the managedattribute 'gettype' argument to automatically
        de-reference objects.

        If the value is not a weak reference, it is returned as-is. If the
        referent object is not alive, None is returned.

        Tip: Use with type=managedattribute.test_auto_ref or auto_ref

        Args:
            value: The value to de-reference.

        Example:

            attr = managedattribute(
                name='attr',
                type=managedattribute.auto_ref,
                gettype=managedattribute.auto_unref)

            attr = managedattribute(
                name='attr',
                type=managedattribute.test_auto_ref((
                    None,
                    managedattribute.test_isinstance(Device))),
                gettype=managedattribute.auto_unref)
        '''
        if isinstance(value, weakref.ReferenceType):
            value = value()
        return value

    @staticmethod
    def _transform(value, transforms):
        '''Internal function that applies transformations to a value.

        The 'transforms' argument can be one of:
            - None. No transformation is applied, the value is returned as-is.
            - A callable. Transformation is applied by calling it with the
              value as only argument and the returned value is used.
            - A tuple of either callables or the value None. Callables are
              called as above, the special value None means that None is itself
              an allowed value and it is returned as-is.

        These callables can be classes or functions. These callables must
        either return a new value or raise ValueError or TypeError exceptions.
        If one such exception is raise, the next transformation is applied
        until either one succeeds returning a new value or all of them fail. In
        the latter case, a ValueError exception is raised summarizing all
        previous failures.

        Args:
            value: The value to transform.
            transforms: Transformations to apply.

        Return:
            possibly transformed value.
        '''
        if transforms is not None:
            if not transforms:
                raise AttributeError('can\'t set attribute')
            # Find a valid transformation
            exceptions = []
            for transform in transforms:
                try:
                    if transform is None:
                        if value is not None:
                            raise ValueError('Not None')
                    else:
                        value = transform(value)
                    break
                except (ValueError, TypeError) as e:
                    exceptions.append(e)
                    pass
            else:
                # None found!
                exceptions = [str(e) for e in exceptions]
                exceptions = [e if e.endswith('.') else e + '.'
                              for e in exceptions]
                raise ValueError('{}: {}'.format(value, ' '.join(exceptions)))
        return value

    def _default_getter(self, inst):
        '''Default getter (__get__) implementation.

        Returns the current attribute value. If none exists,
        performs the default's action (raise AttributeError, return a default
        value or initialize the attribute with a default value.)

        Before returning a value, "gettype" transformations are applied, except
        in the case where a default value is returned directly.
        '''

        attr = self.__attr or '_' + self.__name__
        try:
            # Get the value using the internal attribute name.
            value = getattr(inst, attr)
        except AttributeError:
            # No value; Consult the default (__def) and perform the appropriate
            # action (__def_action.)
            fdef = self.__def
            def_action = self.__def_action
            if def_action is None:
                # No default; Attribute is undefined.
                raise AttributeError
            elif def_action is managedattribute.DefaultActions.value_return_default:
                # Return the requested default value. Since it was supplied, do
                # not transform it.
                return fdef  # no transform
            elif def_action is managedattribute.DefaultActions.method_return_default:
                # Call the specified method; Since the method supplies the
                # value, do not transform it.
                return fdef(inst)  # no transform
            elif def_action is managedattribute.DefaultActions.function_return_default:
                # Call the specified function; Since the method supplies the
                # value, do not transform it.
                return fdef()  # no transform
            elif def_action is managedattribute.DefaultActions.value_set_init:
                # Initialize the attribute with the requested default value.
                # Since it is stored and further access will transform it,
                # allow transformations here too.
                value = fdef
            elif def_action is managedattribute.DefaultActions.method_set_init:
                # Call the specified method and initialize the attribute with
                # the requested default value. Since it is stored and further
                # access will transform it, allow transformations here too.
                value = fdef(inst)
            elif def_action is managedattribute.DefaultActions.function_set_init:
                # Call the specified function and initialize the attribute with
                # the requested default value. Since it is stored and further
                # access will transform it, allow transformations here too.
                value = fdef()
            else:
                raise ValueError(def_action)
            # Reached this point due to a new "init" value; Set, transform &
            # return.
            setattr(inst, attr, value)
        try:
            # Reached this point due to an existing value or a new "init"
            # value; Transform & return.
            # Apply transformations (__gettype)
            value = self._transform(value, self.__gettype)
        except ValueError as e:
            # Transformation failed, convert to AttributeError which is
            # appropriate for a getter.
            raise AttributeError
        # Reached this point with a transformed value; Return.
        return value

    def _default_setter(self, inst, value):
        '''Default setter (__set__) implementation.

        "type" transformations are applied and the resulting value is set using
        the internal attribute name.
        '''
        # Apply transformations (__type)
        value = self._transform(value, self.__type)
        try:
            # Set the value using the internal attribute name.
            attr = self.__attr or '_' + self.__name__
            setattr(inst, attr, value)
        except AttributeError:
            # Convert AttributeError about _name into unspecified one
            raise AttributeError

    def _default_deleter(self, inst):
        '''Default deleter (__delete__) implementation.

        Delete the internal attribute value.
        '''
        try:
            # Delete the value using the internal attribute name.
            attr = self.__attr or '_' + self.__name__
            delattr(inst, attr)
        except AttributeError:
            # Convert AttributeError about _name into unspecified one
            raise AttributeError

    def __init__(self,
                 fget=Constants.not_specified,
                 fset=Constants.not_specified,
                 fdel=Constants.not_specified,
                 fdef=Constants.not_specified,
                 fdef_method=Constants.not_specified,
                 default=Constants.not_specified,
                 finit=Constants.not_specified,
                 finit_method=Constants.not_specified,
                 init=Constants.not_specified,
                 name=None, attr=None,
                 type=None, gettype=None,
                 read_only=False,
                 doc=None):
        '''Initialize a new managedattribute.

        Args:
            fget: Getter method.
            fset: Setter method.
            fdel: Deleter method.
            fdef: Defaulter function.
            fdef_method: Defaulter method.
            default: Default value.
            finit: Initializer function.
            finit_method: Initializer method.
            init: Initial value.
            name: Name of the attribute.
            attr: Name of the internal attribute.
            type: Type of values to accept.
            gettype: Type of values to return.
            read_only: If True, the attribute is read-only.
            doc: Documentation string.
        '''
        type_ = type
        type = builtins.type
        getter_doc = False  # doc doesn't come from the getter

        if fget is not managedattribute.not_specified:
            # A getter is specified.
            if name is None:
                # Default the name to the getter's name:
                #     @managedattribute
                #     def attr_name(self):
                #         ...
                name = fget.__name__
            if doc is None:
                # Default the docimentation to the getter's doc:
                #     @managedattribute
                #     def attr_name(self):
                #         '''getter's doc'''
                #         ...
                doc = getattr(fget, '__doc__', None)
                if doc is not None:
                    getter_doc = True  # doc comes from the getter

        if read_only:
            # read-only attributes can't be set (and type-transformed) or
            # deleted
            if fset not in (None, managedattribute.not_specified):
                raise TypeError('read-only attributes cannot have a setter')
            if fdel not in (None, managedattribute.not_specified):
                raise TypeError('read-only attributes cannot have a deleter')
            if type_ is not None:
                raise TypeError('read-only attributes cannot have a type')
            fset = None
            fdel = None
            type_ = None

        if fget not in (None, managedattribute.not_specified) \
                and not callable(fget):
            raise TypeError('fget argument not callable')
        if fset not in (None, managedattribute.not_specified) \
                and not callable(fset):
            raise TypeError('fset argument not callable')
        if fdel not in (None, managedattribute.not_specified) \
                and not callable(fdel):
            raise TypeError('fdel argument not callable')

        if sum([
                fdef is not managedattribute.not_specified,
                fdef_method is not managedattribute.not_specified,
                default is not managedattribute.not_specified,
                finit is not managedattribute.not_specified,
                finit_method is not managedattribute.not_specified,
                init is not managedattribute.not_specified]) > 1:
            raise TypeError('fdef, fdef_method, default, finit, finit_method'
                            ' and init arguments are all mutually exclusive')
        if fdef is not managedattribute.not_specified:
            if fdef is not None and not callable(fdef):
                raise TypeError('fdef argument not callable')
            fdef = fdef
            def_action = fdef and managedattribute.DefaultActions('fdef')
        elif fdef_method is not managedattribute.not_specified:
            if fdef_method is not None and not callable(fdef_method):
                raise TypeError('fdef_method argument not callable')
            fdef = fdef_method
            def_action = fdef and managedattribute.DefaultActions('fdef_method')
        elif default is not managedattribute.not_specified:
            fdef = default
            def_action = managedattribute.DefaultActions('default')
        elif finit is not managedattribute.not_specified:
            if finit is not None and not callable(finit):
                raise TypeError('finit argument not callable')
            fdef = finit
            def_action = fdef and managedattribute.DefaultActions('finit')
        elif finit_method is not managedattribute.not_specified:
            if finit_method is not None and not callable(finit_method):
                raise TypeError('finit_method argument not callable')
            fdef = finit_method
            def_action = fdef and managedattribute.DefaultActions('finit_method')
        elif init is not managedattribute.not_specified:
            fdef = init
            def_action = managedattribute.DefaultActions('init')
        else:
            fdef = None
            def_action = None

        if name is None:
            # name is mandatory as it is used for the default internal
            # attribute name and in raising meaningful AttributeError
            # exceptions.
            raise TypeError('name argument missing')
        if type(name) is not str:
            raise TypeError('name argument not a str')
        if doc is not None and type(doc) is not str:
            raise TypeError('doc argument not a str')
        if type_ is not None:
            if type(type_) is not tuple:
                # Single transformation => singleton
                type_ = (type_,)
            for transform in type_:
                if transform is not None and not callable(transform):
                    raise TypeError('type argument not callable')
        if gettype is not None:
            if type(gettype) is not tuple:
                # Single transformation => singleton
                gettype = (gettype,)
            for transform in gettype:
                if transform is not None and not callable(transform):
                    raise TypeError('gettype argument not callable')

        # Save all settings to private attributes
        self.__get = fget
        self.__set = fset
        self.__del = fdel
        self.__def = fdef
        self.__def_action = def_action
        self.__name__ = name
        self.__attr = attr
        self.__getter_doc = getter_doc
        self.__doc__ = doc
        self.__type = type_
        self.__gettype = gettype

        super().__init__()

    def copy(self, **kwargs):
        '''Copy this instance and allow overriding any of the new instance's
        __init__ arguments.'''
        # Initialize a copy using private attributes
        d = {
            'fget': self.__get,
            'fset': self.__set,
            'fdel': self.__del,
            'fdef': managedattribute.not_specified,
            'fdef_method': managedattribute.not_specified,
            'default': managedattribute.not_specified,
            'finit': managedattribute.not_specified,
            'finit_method': managedattribute.not_specified,
            'init': managedattribute.not_specified,
            'name': self.__name__,
            'attr': self.__attr,
            'doc': None if self.__getter_doc else self.__doc__,
            'type': self.__type,
            'gettype': self.__gettype,
        }
        # See if any keyword arguments correspond to default actions...
        if not any(
                (e.value in kwargs)
                for e in managedattribute.DefaultActions.__members__.values()):
            # No default action arguments given
            if self.__def_action:
                # Convert the __def/__def_action private attributes into
                # __init__'s corresponding argument
                d[self.__def_action.value] = self.__def
            else:
                # Degenerate "no default value" case.
                d['fdef'] = None
        # Update defaults with the caller's overrides.
        # Any invalid keyword will cause __init__ to raise TypeError. Not
        # checking them here allows better subclassing support.
        d.update(kwargs)
        # Create the new managedattribute (or subclass)
        return type(self)(**d)

    def __copy__(self):
        '''Default copy(self) implementation.'''
        return self.copy()

    def getter(self, fget):
        '''Descriptor to change the getter on a managedattribute.

        A getter, just like with Python's property, takes charge of return the
        value of an attribute.

        Args:
            fget: Getter method.

        Example:

            attr = managedattribute(name='attr')

            @attr.getter
            def attr(self):
                """Compute and return the value of attr"""
                return compute(self._value)
        '''
        if fget is not None and not callable(fget):
            raise TypeError('getter argument not callable')
        return self.copy(fget=fget)

    def setter(self, fset):
        '''Descriptor to change the setter on a managedattribute.

        A setter, just like with Python's property, takes charge of setting the
        value of an attribute.

        Args:
            fset: Setter method.

        Example:

            attr = managedattribute(name='attr')

            @attr.setter
            def attr(self, value):
                self._attr = compute(value)
        '''
        if fset is not None and not callable(fset):
            raise TypeError('setter argument not callable')
        return self.copy(fset=fset)

    def deleter(self, fdel):
        '''Descriptor to change the deleter on a managedattribute.

        A deleter, just like with Python's property, takes charge of deleting
        the value of an attribute.

        Args:
            fdet: Deleter method.

        Example:

            attr = managedattribute(name='attr')

            @attr.deleter
            def attr(self):
                del self._attr
        '''
        if fdel is not None and not callable(fdel):
            raise TypeError('deleter argument not callable')
        return self.copy(fdel=fdel)

    def defaulter(self, fdef):
        '''Descriptor to change the defaulter on a managedattribute.

        The defaulter method is called by managedattribute's default getter if
        the attribute does not exist for the object instance.

        The method's return value will be returned to the caller getting the
        attribute. 'gettype' transformations are NOT applied.

        Args:
            fdef: Defaulter method.

        Example:

            attr = managedattribute(name='attr')

            @attr.defaulter
            def attr(self):
                return 'default value'
        '''
        if fdef is not None and not callable(fdef):
            raise TypeError('defaulter argument not callable')
        return self.copy(fdef_method=fdef)

    def initter(self, finit):
        '''Descriptor to change the initter on a managedattribute.

        The initter method is called by managedattribute's default getter if
        the attribute does not exist for the object instance.

        The method's return value will be used to initialize the object
        instance's attribute value. 'gettype' transformations are applied and
        the transformed value returned to the caller getting the attribute.

        Args:
            finit: Initter method.

        Example:

            attr = managedattribute(name='attr')

            @attr.initter
            def attr(self):
                return MyClass()
        '''
        if finit is not None and not callable(finit):
            raise TypeError('initter argument not callable')
        return self.copy(finit_method=finit)

    def __get__(self, inst, cls=None):
        '''Implement the descriptor __set__ protocol.

        Called when the attribute value is to be retrieved (get):
            descriptor = cls.attr
            value = inst.attr
            value = getattr(inst, 'attr')
        '''
        if inst is None:
            # No instance; Invoked from the owner class:
            #    descriptor = MyClass.attr
            # Return the descriptor itself
            return self
        # With instance, Invoked from the object instance:
        #     value = inst.attr
        fget = self.__get
        if fget is None:
            # No getter; write-only!
            # Same error message as property's
            raise AttributeError('unreadable attribute')
        if fget is managedattribute.not_specified:
            # No custom getter; Use managedattribute's default getter
            # implementation.
            fget = self._default_getter
        try:
            # Call the getter and return the value.
            return fget(inst)
        except AttributeError as e:
            # In no error message was provided, default it to the attribute
            # name.
            e.args = e.args or (self.__name__,)
            raise

    def __set__(self, inst, value):
        '''Implement the descriptor __set__ protocol.

        Called when the attribute value is to be set:
            inst.attr = value
            setattr(inst, 'attr', value)
        '''
        # Invoked from the object instance:
        #     inst.attr = value
        fset = self.__set
        if fset is None:
            # No setter; read-only!
            # Same error message as property's
            raise AttributeError('can\'t set attribute')
        if fset is managedattribute.not_specified:
            # No custom setter; Use managedattribute's default setter
            # implementation.
            fset = self._default_setter
        try:
            # Call the setter and return the value (typically None.)
            return fset(inst, value)
        except AttributeError as e:
            # In no error message was provided, default it to the attribute
            # name.
            e.args = e.args or (self.__name__,)
            raise

    def __delete__(self, inst):
        '''Implement the descriptor __del__ protocol.

        Called when the attribute value is to be deleted:
            del inst.attr
            delattr(inst, 'attr')
        '''
        # Invoked from the object instance:
        #     del inst.attr
        fdel = self.__del
        if fdel is None:
            # No deleter; read-only!
            # Same error message as property's
            raise AttributeError('can\'t delete attribute')
        if fdel is managedattribute.not_specified:
            # No custom deleter; Use managedattribute's default deleter
            # implementation.
            fdel = self._default_deleter
        try:
            # Call the deleter and return the value (typically None.)
            return fdel(inst)
        except AttributeError as e:
            # In no error message was provided, default it to the attribute
            # name.
            e.args = e.args or (self.__name__,)
            raise

    @property
    def __isabstractmethod__(self):
        '''True if any of the methods used to compose the descriptor are
        abstract.'''
        fget = self.__get
        if fget not in (None, managedattribute.not_specified) \
                and getattr(fget, "__isabstractmethod__", False):
            return True
        fset = self.__set
        if fset not in (None, managedattribute.not_specified) \
                and getattr(fset, "__isabstractmethod__", False):
            return True
        fdel = self.__del
        if fdel not in (None, managedattribute.not_specified) \
                and getattr(fdel, "__isabstractmethod__", False):
            return True
        fdef = self.__def
        if fdef is not None \
                and self.__def_action in (
                    managedattribute.DefaultActions.function_return_default,
                    managedattribute.DefaultActions.function_set_init,
                    managedattribute.DefaultActions.method_return_default,
                    managedattribute.DefaultActions.method_set_init) \
                and getattr(fdef, "__isabstractmethod__", False):
            return True
        return False

    def _inherit(self, inst):
        '''Return a new instance appropriate for inheriting the attribute in a
        different object.

        Helper method used by AttributesInheriter. Computes the parent object's
        current attribute value and presents it as the default to the inheriter
        object. AttributesInheriter takes care of multiple-inheritance:

            class Parent():
                attr = managedattribute(...)

            parent = Parent()
            parent.attr = 'p'
            inheriter1 = AttributesInheriter(parent=parent)
            inheriter1.attr = 'i1'
            inheriter2 = AttributesInheriter(parent=inheriter1)

            value = inheriter2.attr  # value = 'i1'
            # Logic:
            #     descriptor = Parent.attr  # __get is None
            #     descriptor = descriptor._inherit(parent)  # copy(default='p')
            #     descriptor = descriptor._inherit(inheriter1)  # copy(default='i1')
            #     value = descriptor.__get__(inheriter2)  #  value = 'i1'
        '''
        if self.__get is None:
            # Unreadable attribute, return as-is
            return self
        try:
            # Compute the parent object's current attribute value
            default = self.__get__(inst)
        except AttributeError:
            # There is current value; Force clearing all default-handling
            # keywords
            default = managedattribute.not_specified
        return self.copy(default=default)

# vim: ft=python et sw=4
