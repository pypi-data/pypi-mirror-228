import os
import sys
import types
import inspect
import pkgutil
import weakref
import importlib
import threading

from .token import AbstractToken, TokenChain

class AbstractPackage(object):
    '''AbstractPackage
    
    An abstract package is one where its import paths are two parth: the 
    relative information part, and the tokenization part. With the proper tools,
    abstract packages allows users to make calls to classes/methods/etc without
    having to explicitly specify the import/module path, and only use the 
    informational one. 

        from my_library.nxos.ospf import Ospf
                 |        |    |
                 |      token  |
             library pkg       |
                         information path

    When an abstract package is learnt, all child modules within the given 
    module (if it is a) package, will be loaded recursively in order to build 
    the abstraction matrix/database. Normally this class instance is stored 
    under a var called "__abstract_pkg" on the given module.

    Note
    ----
        A packge is a module that contains other modules. 

    Arguments
    ---------
        obj (str/ModuleType): python module name (module.__name__) or object
        delay (bool): flag whether to delay the learning/loading of this
                      module's child modules.
    '''

    def __init__(self, obj, delay = False):

        # an abstraction package has a root name
        # (the same as its original module name)
        self.name = obj.__name__ if isinstance(obj, types.ModuleType) else obj

        # matrix storing the token/module mapping
        self.matrix = {}

        # lock for thread race condition during learning
        self._lock = threading.Lock()

        # learn only when there's no delay
        if not delay: 
            self.learn()

    @property
    def paths(self):
        '''paths

        search paths for this package's children modules.
            - if it's a namespace package, __path__ is a list
            - else, default to its [__file__, ]
            - note: could've used ModuleSpec (__spec__) instead for python 3.4+

        '''
        return getattr(self.module, '__path__', 
                       [os.path.dirname(self.module.__file__), ])

    @property
    def learnt(self):
        '''learnt

        property, returns True if the matrix is not empty (learnt). Otherwise,
        returns false.
        '''

        with self._lock:
            return bool(self.matrix)

    @property
    def module(self):
        '''module

        returns the python module object assoicated with this abstracted package
        '''

        # lookup package name in sys.modules
        return sys.modules[self.name]
    
    def learn(self):
        '''learn

        recursively learn this package's child content
        '''

        # quick exit if it is already learnt (has content)
        if self.learnt:
            return

        with self._lock:
            # import all children packages at once
            try:
                children = _find_children(name = self.name, 
                                          paths = self.paths)
            except ImportError:
                raise
            except Exception:
                raise

            # include the package itself as root
            self.register(tuple(self.name.split('.')), None, self.module)

            # register all children of this package
            for relpath, tokens, module in children:
                self.register(relpath, tokens, module)

    def __contains__(self, relpath):
        return relpath in self.matrix

    def register(self, relpath, tokens, module):
        '''register

        store a module internally with its relative name and token path in
        the internal matrix.

        Arguments
        ---------
            relpath (tuple): tuple of relative name for this module, eg
                             ('a', 'b', 'c') for a.b.c
            tokens (tuple): tuple of tokens associated with this module
            module (ModuleType): module object to register
        '''

        # avoid duplicate path/token combo
        if relpath in self.matrix and tokens in self.matrix[relpath]:
            raise ValueError("Duplicate relative path/token combination. \n"
                             "Already know: %s for %s/%s\n"
                             "and got %s" % (self.matrix[relpath][tokens],
                                             relpath, tokens, module))
        
        self.matrix.setdefault(relpath, {})[tokens or ()] = module

    def lookup(self, relpath, tokens, name):
        try:
            return getattr(self.matrix[relpath][tokens], name)

        except (KeyError, AttributeError):
            raise LookupError("No such combinations:\n"
                              "     relpath = %s\n"
                              "     tokens = %s\n"
                              "     name = %s'" % (relpath, tokens, name))

def _find_children(name, paths, tokens = None):
    '''find_modules

    Internal generator. Returns all child modules in a given package, along
    with their relative name and recognized tokens. This generator is 
    functionally similar to python's built in pkgutil.walk_packages().

    Arguments
    ---------
        name (str): package name
        paths (list): list of directory paths to search for child modules.
        tokens (list): internal static list, tracking the current known tokens
                       when this function is called recursively.
    
    Returns
    -------
        [(relpath, tokens, module), ...]
    '''

    if tokens is None:
        tokens = TokenChain()

    # pkgutil expects a prefix
    name = name if name.endswith('.') else name + '.'

    # helper function
    def seen(p, m = []):
        if p in m:
            return True
        m.append(p)

    for importer, absname, ispkg in pkgutil.iter_modules(paths, name):

        # ignore tests modules for sanity
        if absname.endswith('.tests'):
            continue

        # import the actual module
        try:
            module = importlib.import_module(absname)
        except Exception as err:
            err.absname = absname
            raise

        # expoded form (split by .)
        absname_exploded = absname.split('.')

        # track token declarations
        with tokens.track(module):

            # relative name -> no tokens
            relpath = tuple(i for i in absname_exploded if i not in tokens)
            
            # make a copy of the token to avoid same-obj ref
            # (relpath, tokens, module obj)
            yield (relpath, tokens.to_tuple(), module)

            if ispkg:
                # avoid traversing paths items we've seen before
                child_paths = [p for p in getattr(module, '__path__', []) 
                                                                 if not seen(p)]

                # return all child modules
                yield from _find_children(absname, child_paths, tokens)
        

