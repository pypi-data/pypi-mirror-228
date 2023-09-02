import sys
import contextlib

class AbstractToken(object):
    '''AbstractToken

    Describes an arbitrary named token within an abstracted package. Normally
    this class instance is stored under a var called "__abstract_token" on the 
    given module.

    Arguments
    ---------
        module (ModuleType): python module object
    '''
    
    def __init__(self, modulename):
        # name of this token
        # (last item in the name chain)
        self.name = modulename.split('.')[-1]

        self.modulename = modulename

    @property
    def module(self):
        '''module

        returns the python module object assoicated with this token
        '''

        # lookup package name in sys.modules
        return sys.modules[self.modulename]


class TokenChain(object):
    '''TokenChain

    Internal class. Used to track the current chain of tokens in the recursive
    import process. 

    Arguments
    ---------
        chain (list): list of token chains to start with, default to empty list.
    '''
    
    def __init__(self, chain = None):

        # store chain internally
        self._chain = chain or []

    @contextlib.contextmanager
    def track(self, module):
        '''track

        context manager api allowing auto-tracking of tokens using the with 
        statement. On entry, stors the discovered token (if any) internally, 
        on exit, removes that token from tracking.

        Arguments
        ---------
            module (ModuleType): module object to add to tracking

        Example
        -------
            >>> with tokenchain.track(module):
            ...     pass
        '''
        
        # get the token from module object
        token = getattr(module, '__abstract_token', None)

        if token is not None:
            # track token if discovered
            self._chain.append(token)

            yield self

            # remove token from tracking after exiting scope.
            self._chain.pop(-1)
        else:
            # nothing to track
            yield self

    def __iter__(self):
        '''__iter__

        allows this object to be iterable, iterating through the currently known
        list of tokens.
        '''
        return iter(self._chain)

    def to_tuple(self):
        '''to_tuples

        returns all currently tracked tokens in a tuple. This is needed as the
        abstracted package uses token tuples as keys for lookup.
        '''
        return tuple(i.name for i in self._chain)

    def __str__(self):
        return str(self.to_tuple())

    def __repr__(self):
        return str(self)

    def copy(self):
        return type(self)(self._chain.copy())

    def __contains__(self, value):
        '''__contains__

        api to enable checking whether a given token is part of this chain.
        can be used with either AbstractToken objects or just a string token 
        name.
        '''
        return value in self._chain or value in [i.name for i in self._chain]

