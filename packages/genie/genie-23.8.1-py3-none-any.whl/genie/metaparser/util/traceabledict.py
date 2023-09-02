"""TraceableDict - a new data structure inherits from Python dict, which allows 
the nested-key usages to be tracked.

"""

import copy

class TraceableDict(dict):
    """TraceableDict

    A subclass of Python dict that provides functionality of key usage tracking.
    The class allows to convert the common dict into TraceableDict data 
    structure. All common Python dict key usage functionalities, for example:
         - dict['xx']
         - dict.keys()
         - dict.items()
         - dict.values()
         - dict.get()
         - dict.copy()
         - dict.pop()
    will be traced and saved into class variable - `tracer` for future access.

    Args:

        key_map (`dict`): dict to store the current key name and its key path,
                          for example {'aaa': ('a', 'aa', 'aaa'), 'b':('b',)}
        dictname (`str`): dictionary identity.
                         choices of: 'cl', 'xml', 'yang', default is 'cli'.
    Returns:
            a `TraceableDict` object

    Examples:
        >>> from .util.traceabledict import TraceableDict
        >>> t = TraceableDict.convert(dict)
        >>> assert('TraceableDict'== t.__class__.__name__)

    Class variables:

        tracer (`dict`): class variable to hold dictionary name and its key 
                         usage record, for example: 
                         {name1: {usage}, name2: {usage}}
    """

    tracer = {}

    def __init__(self, *args, **kwargs):
        # define {key name, key path} pair
        self.key_map = {}
        self.dictname = None
        super().__init__(*args, **kwargs)

    def __getitem__(self, item):
        """ tracing key usage when accessing dict: dict['xxx']

        note: only trace the leaf key to avoid fragment key confusion
        """
        res = super().__getitem__(item)
        if not isinstance(res, TraceableDict):
            TraceableDict.tracer[self.dictname].add(self.key_map[item])
        return res

    def get(self, item):
        """ tracing key usage when accessing dict: dict.get('xxx')

        note: only trace the leaf key to avoid fragment key confusion
        """
        res = super().get(item)
        if not isinstance(res, TraceableDict):
            TraceableDict.tracer[self.dictname].add(self.key_map[item])
        return res

    def keys(self):
        """ tracing key usage when accessing dict: dict.keys()
        """
        for item in super().keys():
            TraceableDict.tracer[self.dictname].add(self.key_map[item])
        return super().keys()
    
    def values(self):
        """ tracing key usage when accessing dict: dict.values()
        """
        self.keys()
        return super().values()

    def items(self):
        """ tracing key usage when accessing dict: dict.items()
        """
        self.keys()
        return super().items()
    
    def copy(self):
        """ tracing key usage when accessing dict: dict.copy()

        note: copy itself won't trace any key usage, but the copied dict will 
        continuously be able to trace key usages.
        """
        res = super().copy()
        return TraceableDict.convert(res, self.dictname)

    def pop(self, item):
        """ tracing key usage when accessing dict: dict.pop('xxx')
        """
        TraceableDict.tracer[self.dictname].add(self.key_map[item])
        super().pop(item)

    @staticmethod
    def convert(d, name, parent_key=None):
        """recursively convert Pyhton dict/nested dict into `TraceableDict`

        Args:
            d (`dict`): the dictionary needs to be converted
            name (`str`): TraceableDict name
            parent_key (`list`): the parent key path which leads to this 
                                 dictionary. for example:
                                 for dic = {'a': {'aa': 'xxx'}}
                                 parent_key will be None for dic, 
                                 and will be ['a'] for dic['a']
        Return:
            a `TraceableDict` obj
        
        Example:
            >>> from .util.traceabledict import TraceableDict
            >>> d = {'a': {'aa': 'xxx'}}
            >>> t = TraceableDict.convert(d, 'my_traced_dict')

        """
        if parent_key is None:
            parent_key = []

        r_tracedict = TraceableDict()
        
        if isinstance(d, TraceableDict):
            items = super().items()
        else:
            items = d.items()

        for item, value in items:
            key_path = copy.deepcopy(parent_key)
            key_path.append(item)
            r_tracedict.key_map[item] = tuple(key_path)
            
            if isinstance(value, dict):
                sub_dict = TraceableDict.convert(value, name, parent_key=key_path)
                r_tracedict[item] = sub_dict
            else:
                r_tracedict[item] = value
        r_tracedict.dictname = name
        return r_tracedict