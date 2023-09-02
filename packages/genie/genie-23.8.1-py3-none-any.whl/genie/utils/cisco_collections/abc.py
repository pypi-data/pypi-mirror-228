
__all__ = (
    'Range',
)

import abc
import collections
import collections.abc


class Range(collections.abc.Sequence):
    '''All the operations on a read-only range.

    Concrete subclasses must override:
        - __init__(stop)
        - __init__(start, stop[, step])
        - start
        - stop
        - step
        - __len__()       (implement Sized)
        - __getitem__(i)  (implement Sequence)

    It is also suggested to provide optimal:
        - index(value, [start, [stop]])
        - __iter__()      (implement Iterable)
        - __contains__()  (implement Container)
        - __reversed__()
        - __eq__(other)
        - __ne__(other)
    '''

    __slots__ = ()

    @abc.abstractmethod
    def __init__(self):
        super().__init__()

    @property
    @abc.abstractmethod
    def start(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def stop(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def step(self):
        raise NotImplementedError

    def count(self, value):
        'R.count(value) -> integer -- return number of occurrences of value'
        return 1 if value in self else 0

    def __eq__(self, other):
        if not isinstance(other, Range):
            return NotImplemented
        return len(self) == len(other) and all(
            a == b for a, b in zip(self, other))

    def __ne__(self, other):
        eq = self == other
        if eq is NotImplemented:
            return NotImplemented
        return not eq

    def __hash__(self):
        # Implementation equivalent to range.__hash__
        l = len(self)
        if not l:
            return hash((l, None, None))
        if l == 1:
            return hash((l, self.start, None))
        return hash((l, self.start, self.step))

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Range:
            for B in C.__mro__:
                if (any("start" in B.__dict__ for B in C.__mro__)
                        and any("stop" in B.__dict__ for B in C.__mro__)
                        and any("step" in B.__dict__ for B in C.__mro__)):
                    return True
        return NotImplemented

Range.register(range)

# vim: ft=python et sw=4
