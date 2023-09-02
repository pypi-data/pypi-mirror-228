#TODO More unittest
from functools import total_ordering

class DiffList(list):
    def __str__(self):
        return '\n'.join([str(item) for item in self])

class DiffDict(object):
    '''Take two dictionary, and create a diff

    Output is very similar to Linux diff
    '''

    def __init__(self, d1, d2):
        '''Accepts two dictionary'''
        self.d1 = d1
        self.d2 = d2

    def findDiff(self, path='', **kwargs):
        '''Figure out the difference'''

        # Figure out the diff
        self.diffs = self._findDiff(d1=self.d2, d2=self.d1, path=path)

    def added(self):
        return DiffList(sorted([item for item in self.diffs
                              if isinstance(item, DictDiffAddItem)]))
    def removed(self):
        return DiffList(sorted([item for item in self.diffs
                              if isinstance(item, DictDiffRemoveItem)]))
    def modified(self):
        return DiffList(sorted([item for item in self.diffs
                              if isinstance(item, DictDiffDiffItem)]))

    def __str__(self):
        return str(self.diffs)

    def _findDiff(self, d1, d2, path=''):
        # Compare each key, see if is new, removed, or similar

        items = DiffList()
        d1_keys = set(d1.keys())
        d2_keys = set(d2.keys())
        intersect_keys = d1_keys.intersection(d2_keys)

        # Get the diff
        added = d1_keys - d2_keys
        removed = d2_keys - d1_keys

        for add in added:
            # Then create added items
            items.append(DictDiffAddItem(item=add, path=path,
                                         value=d1[add]))
        for remove in removed:
            # Then create removed items
            items.append(DictDiffRemoveItem(item=remove, path=path,
                                            value=d2[remove]))

        # Intersect keys are the similar keys
        # If they are similar, we need to go deeper in the dictionary, to see if
        # there is difference later
        for key in intersect_keys:
            ppath = path
            if type(d1[key]) is dict and type(d2[key]) is dict:
                if ppath == "":
                    ppath = key
                else:
                    ppath = ppath + "['" + key + "']"
                items.extend(self._findDiff(d1=d1[key], d2=d2[key], path=ppath))

            # A value
            elif d1[key] != d2[key]:
                if ppath == "":
                    ppath = key
                else:
                    ppath = ppath + "['" + key + "']"
                items.append(DictDiffDiffItem(value=d1[key],
                                              old_value=d2[key],
                                              path=ppath))
        return items

@total_ordering
class DictDiffItem(object):
    def __init__(self, value, path, item=None):
        self.item = item
        self._path = path
        self.value = value

    def __lt__(self, other):
        return self.path < other.path

class DictDiffAddItem(DictDiffItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._path:
            self.path = "{path}['{item}']".format(path=self._path,
                                                  item=self.item)
        else:
            self.path = self.item

    def __str__(self):
        return " +{path}: {value}".format(path=self.path,
                                          value=self.value)

class DictDiffRemoveItem(DictDiffItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._path:
            self.path = "{path}['{item}']".format(path=self._path,
                                                  item=self.item)
        else:
            self.path = self.item

    def __str__(self):
        return " -{path}: {value}".format(path=self.path,
                                          value=self.value)

class DictDiffDiffItem(DictDiffItem):
    def __init__(self, old_value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.new_value = self.value
        del self.value
        self.old_value = old_value
        self.path = self._path

    def __str__(self):
        return ' +{path}: {value}\n -{path}: {old_value}'\
               .format(path=self.path, value=self.new_value,
                       old_value=self.old_value)
