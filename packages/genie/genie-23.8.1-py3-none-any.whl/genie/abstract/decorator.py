import sys
import inspect
import functools

from .magic import default_builder

from .package import AbstractPackage

def default_token_getter(obj, attrs):
    '''default_token_getter

    default api to be used by the LookupDecorator in order to collect the
    provided attributes during runtime.

    This api first attempts to get obj.<attr>. If not found, attempts to collect
    from obj.device.<attr>, else raise error.

    Arguments
    ---------
        obj (object): object to collect attribute from
        attrs (list of strings): names of attribute to get

    Returns
    -------
        collected attributes
    '''
    attributes = []

    for attr in attrs:
        if hasattr(obj, attr):
            attributes.append(getattr(obj, attr))
        elif not hasattr(obj, 'device') or not hasattr(obj.device, attr):
                raise AttributeError("No attribute '%s' on '%s'" % (attr, obj))
        else:
            attributes.append(getattr(obj.device, attr))
    return tuple(attributes)

def from_device_token_getter(obj, defaults = []):
    '''from_device_token_getter

    default api to be used by the LookupFromDeviceDecorator in order to collect
    the provided attributes during runtime.

    This api first attempts to get attributes from device.custom.abstraction.
    If not found, falls back to provided defaults.

    This api first attempts to get obj.<attr>. If not found, attempts to collect
    from obj.device.<attr>, else raise error.

    Arguments
    ---------
        obj (object): object to collect attribute from
        attrs (list of strings): names of attribute to get

    Returns
    -------
        collected attributes
    '''
    # look into device.custom.abstraction first
    attrs = []

    device = getattr(obj, 'device', None)
    if device and getattr(device, 'custom', None):
        abstraction = getattr(device.custom, 'abstraction',
                                  device.custom.get('abstraction', None))
        if abstraction:
            attrs = abstraction.get('order', None)

    return default_token_getter(obj, attrs or defaults)

class LookupDecorator(object):
    '''LookupDecorator

    This class is to be used as a decorator on class methods in abstracted
    packages. It allows dynamic class method references: eg, calling obj.b()
    first performs a lookup on the tokens, and if found, calls the class.b from
    the actual token matching.

    This class is built on the python descriptor mechanism.

    Note
    ----
        This class functions based on the same principles as the AbstractPackage
        and Lookup() combination. However, instead of using declare_package()
        at the root of an abstraction package. this decorator treats the calling
        class's module as the root of a new abstraction package, and goes from
        there.

    Examples
    --------
        class MyClass(object):

            @LookupDecorator('os')
            def do_work(self):
                pass

    Arguments
    ---------
        *attrs (list of str): list of attributes to collect token information.
        builder (func): function used for creating the lookup token sequence
        attr_getter (func): function to call to collect object attributes
        **builder_kwargs (kwargs): any other keyword arguments for the
                                   sequence builder.

    '''
    def __init__(self, *attrs,
                        builder = default_builder,
                        attr_getter = default_token_getter,
                        **builder_kwargs):

        # attributes and getters to lookup for tokens
        self._attrs = attrs
        self._getter = attr_getter

        # method that got decorated
        self._method = None

        # lookup order builder and its kwargs
        self._builder = builder
        self._builder_kwargs = builder_kwargs

    def __call__(self, method):
        '''__call__

        called as part of the descriptor action. Stores the method internally
        and builds a new abstraction package at this module level if needed.
        '''

        # store method internally
        self._method = method
        self._method_name = method.__name__

        return self

    def __get__(self, instance, owner):
        '''__get__

        python descriptor protocol: __get__. This is called when the user
        performs an attribute get on this decorated method. This is where the
        method abstraction mechanism takes place:

            - find the tokens by reading the specified attributes from object
            - build the abstraction sequence
            - perform lookup, make sure to use full class qualified name
            - call the looked-up method.
        '''

        # special condition when class.method is referenced directly.
        if instance is None:
            return self._method

        module = sys.modules[owner.__module__]

        if not module.__file__.endswith('__init__.py'):
            names = module.__name__.split('.')
            # not a package, find parent package
            for i in range(len(names)-1, -1, -1):
                parent = '.'.join(names[:i])

                try:
                    if sys.modules[parent].__file__.endswith('__init__.py'):
                        break
                except (KeyError, AttributeError):
                    pass
            else:
                raise LookupError('LookupDecorator must be used within a '
                                  'package. Got %s' % module.__file__)

            module = sys.modules[parent]

        module_name = module.__name__

        if not hasattr(module, '__abstract_pkg'):
            # instanciate the abstraction package
            # (always delay to avoid circular reference due to recursive import)
            module.__abstract_pkg = AbstractPackage(module_name, delay = True)

        # store internally
        package = module.__abstract_pkg

        # mnake sure the abstract_pkg is learnt
        package.learn()

        # convert attrs to tokens
        tokens = self._getter(instance, self._attrs)

        # combine tokens into lookup sequence
        sequence = self._builder(tokens, **self._builder_kwargs)

        # do lookup
        relpath = tuple(owner.__module__.split('.'))

        # find the full qualified name (including parent class)
        #  'Evpn.InterfaceAttributes.EthernetSegmentAttributes.BgpAttributes'
        name, *rest = owner.__qualname__.split('.')

        cls = None

        for seq in sequence:
            try:
                cls = package.lookup(relpath, seq, name)
            except LookupError:
                pass
            else:
                break

        if not cls:
            raise LookupError("Cannot find combination based on the following "
                              "criterion: \n"
                              " relative path = %s\n"
                              "   search path = %s\n"
                              "        target = %s" % (relpath, seq, name))

        try:
            for name in rest:
                cls = getattr(cls, name)
        except AttributeError:
            raise LookupError("Class '%s' in '%s' is missing method definition "
                              "'%s'" % (cls.__qualname__, cls.__module__, name))

        try:
            func = getattr(cls, self._method_name)
        except AttributeError:
            raise LookupError("Class '%s' in '%s' is missing method definition "
                              "'%s'" % (cls.__qualname__,
                                        cls.__module__,
                                        self._method_name))

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(instance, *args, **kwargs)
            except NotImplementedError as e:
                raise

        return wrapper

def lookup_from_device(*args, **kwargs):
    '''lookup_from_device

    The actual LookupDecorator.from_device decorator

    If decorator is called without arguments (no ()), the method would be the
    first argument. we need to manually call dunder __call__().

    If it is called with arguments, then we need to return the actual decorator
    that takes in the method.

    '''
    # decorator LookupDecorator.from_device is called
    if len(args) == 1 and not kwargs and callable(args[0]):
        return LookupDecorator(attr_getter = from_device_token_getter)(args[0])

    # decorator LookupDecorator.from_device(...) is called
    # unset attr_getter in the kwargs to avoid duplicated keys
    kwargs.pop('attr_getter', None)
    # called with arguments
    return LookupDecorator(*args, attr_getter = from_device_token_getter,
                           **kwargs)

LookupDecorator.from_device = lookup_from_device
