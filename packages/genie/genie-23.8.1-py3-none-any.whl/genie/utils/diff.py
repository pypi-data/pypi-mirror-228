import re

try:
    # This attribute was removed in python 3.7+.
    # Can be removed once 3.6 support is dropped.
    Pattern = re._pattern_type
except AttributeError:
    # Python 3.7+
    Pattern = re.Pattern

from .config import Config

from collections import OrderedDict

from genie.base import Base as _genie_Base
from genie.conf.base.base import FeatureBase
from genie.conf.base.attributes import (SubAttributesDict,
                                        SubAttributes)


class DiffList(list):
    """List with a modified __str__ to print each item of the diff"""
    def __str__(self):
        return '\n'.join([str(item) for item in self])

    def diff_string(self, diff_type):
        if not diff_type in ['+', '-']:
            raise ValueError("diff_type must be either '+' or '-'.")

        return '\n'.join([item.diff_string() for item in filter(lambda i: hasattr(i, 'sign') and\
            i.sign == diff_type, self)])


class ExcludeList(list):
    """List with a regexp capable __contains__"""
    def __contains__(self, item):
        # The trick is some of self could be a regex, so loop
        # over each and see if match
        for elem in self:
            try:
                if isinstance(elem, Pattern) and elem.match(item):
                    return True
            except TypeError:
                # There a few item that cannot be ignored
                # But try to str it
                try:
                    if isinstance(elem, Pattern) and elem.match(str(item)):
                        return True
                except:
                    # Can't, check parent maybe
                    pass

        return super().__contains__(item)


class Diff(object):
    """Class to compare two objects together.

    Supports the following objects: [Dict, Config, and Conf Features Output]
    First and Second object must be of the same type. The output is similar
    to a Linux diff.

    Args:
        obj1 (dict/Config Object/Conf Feature): First object to compare

        obj2 (dict/Config Object/Conf Feature): Second object to compare

        mode (str, None, optional): Used to choose the type of diff used.
            - 'add' will show only the added lines.
            - 'remove' will show only the removed lines.
            - 'modified' will show only the modified lines.
            - 'None' will show everything.
            Defaults to None.

        exclude (str, list, optional): Item or a list of items to ignore during
            the diff comparison. Items can be a regular expression but they must
            start with a parentheses.

        verbose (bool, optional): When True the diff will show all elements
            contained within a list wether they have been modified or not. When
            False the diff will only show modified elements in the list.
            Defaults to False.

        list_order (bool, optional): When True the diff will ignore the order
            of the elements inside a list. Defaults to False.

    Returns:
        Diff object

    Examples:
        Diff between two dicts

        >>> a = {'a':5, 'b':7, 'c':{'ca':8, 'cb':9}}
        >>> b = {'a':5, 'f':7, 'c':{'ca':8, 'cb':9}}

        >>> dd = Diff(a,b)
        >>> dd.findDiff()
        >>> str(dd)
        '+f: 7\n-b: 7'
    """

    # When creating the object, you select a mode
    # Either all the added keys, removed or modified keys
    # or all of them combined (Which is the default)
    allowed_mode = ['add', 'remove', 'modified', None]

    def __init__(self, obj1, obj2, mode=None, exclude=None, verbose=False, list_order=False):

        if mode not in self.allowed_mode:
            raise ValueError("'{gm}' is not part of the available mode "
                             "{m}".format(gm=self.mode, m=self.allowed_mode))

        # Make sure they are both the same type
        if not isinstance(obj1, obj2.__class__):
            raise TypeError('Both object are not of the same type, '
                            'cannot be compared\n {o1}\n'
                            '{o2}'.format(o1=type(obj1), o2=type(obj2)))

        self.mode = mode
        self.obj1 = obj1
        self.obj2 = obj2
        self.verbose = verbose
        self.list_order = list_order

        # A config object is stored as an object with a dict
        # to contain the configuration. We need to let the code
        # know that the dict is actually coming from Config type
        if isinstance(self.obj1, Config):
            self.config = True
        else:
            self.config = False

        # Field to exclude
        self.exclude = ExcludeList(['_parent', 'parent'])
        self._callables = []

        if exclude:
            # Standardize the input
            if not isinstance(exclude, list):
                exclude = [exclude]

            for exc in exclude:
                if callable(exc):
                    self._callables.append(exc)
                    continue

                # Regex must start with a parentheses
                if exc.startswith('('):
                    try:
                        exc = re.compile(exc)
                    except Exception as e:
                        raise ValueError("'{exc}' is not a valid regex "
                                         "expression".format(exc=exc)) from e

                self.exclude.append(exc)

    def __str__(self):
        return str(self.diffs)

    def diff_string(self, diff_type):
        if not hasattr(self, 'diffs'):
            return ''

        return self.diffs.diff_string(diff_type)

    def findDiff(self):
        """Find all the diffs"""
        self.diffs = self._findDiff_obj(obj1=self.obj2, obj2=self.obj1)

    def _findDiff_obj(self, obj1, obj2, path='', iterable_parent=False):
        """Recursive function to figure out the diff between two objects"""
        # List to hold the UnchangedItem/AddedItem/RemovedItem/ModifiedItem
        # objects
        items = DiffList()

        # First verify if they are the same object
        if id(obj1) == id(obj2):
            # Its the same object, so no difference
            return items

        # Find the keys! Whatever type, I just want the keys.
        obj1_keys = set(self._get_keys(obj1))
        obj2_keys = set(self._get_keys(obj2))

        # Get the added, removed, and modified keys
        added_keys = obj1_keys - obj2_keys
        removed_keys = obj2_keys - obj1_keys
        intersected_keys = obj1_keys.intersection(obj2_keys)

        for key in sorted(added_keys, key=sorter):
            if (self.mode and self.mode != 'add') or (key in self.exclude):
                continue

            # Execute any callables and skip if they return True
            if self._execute_callables(key, path):
                continue

            # managedattribute names start with an underscore, this removes it.
            key = self._convert(obj1, key)

            value = self._get_attr(obj1, key)

            # For list/tuple dynamically create index in path
            if isinstance(obj1, list) or isinstance(obj1, tuple):
                key = 'index[{}]'.format(key)

            added = AddedItem(
                item=key,
                path=path,
                value=value,
                exclude=self.exclude,
                config=self.config)

            items.append(added)

        for key in sorted(removed_keys, key=sorter):
            if (self.mode and self.mode != 'remove') or (key in self.exclude):
                continue

            # Execute any callables and skip if they return True
            if self._execute_callables(key, path):
                continue

            # managedattribute names start with an underscore, this removes it.
            name = self._convert(obj2, key)

            value = self._get_attr(obj2, name)

            # For list/tuple dynamically create index in path
            if isinstance(obj2, list) or isinstance(obj2, tuple):
                name = 'index[{}]'.format(name)

            removed = RemovedItem(
                item=name,
                path=path,
                value=value,
                exclude=self.exclude,
                config=self.config)

            items.append(removed)

        is_different = False

        for key in sorted(intersected_keys, key=sorter):
            if key in self.exclude:
                continue

            # Execute any callables and skip if they return True
            if self._execute_callables(key, path):
                continue

            # Find the value of this key.  Somehow!
            obj1_item = self._get_attr(obj1, key)
            obj2_item = self._get_attr(obj2, key)

            # Check if the type is one that we need to dig further.
            # Multilevel ?
            if self._is_recursive(obj1_item, obj2_item):

                # managedattribute names start with an underscore, this removes it.
                key = self._convert(obj1, key)

                # Figure out how to build the path.
                temp_path = self._get_path(obj1, path, key)

                iterable_parent |= isinstance(obj1_item, list) or \
                                   isinstance(obj1_item, tuple)

                if iterable_parent and self.list_order:
                    # Find diff but ignore changes to the order of elements
                    diff_items = self._diff_list_ignoring_index(
                        obj1_item, obj2_item, temp_path)

                else:
                    diff_items = self._findDiff_obj(
                        obj1=obj1_item,
                        obj2=obj2_item,
                        path=temp_path,
                        iterable_parent=iterable_parent)

                modified = ModifiedItem(
                    items=diff_items,
                    exclude=self.exclude,
                    config=self.config,
                    keep_order=self.verbose and iterable_parent)

                # If it found something that was different
                if modified.path:
                    items.append(modified)

            # If no multilevel, then its a simple Value
            elif obj1_item != obj2_item:
                if self.mode and self.mode != 'modified':
                    continue

                is_different = True

                # managedattribute names start with an underscore, this removes it.
                name1 = self._convert(obj1, key)
                name2 = self._convert(obj2, key)

                # As we know, managedattribute add a _ in front
                # of the variable.
                # So we just converted for both object.
                # This is great, if both were converted. But what if one wasnt!
                # Then uses the key format. (With underscore)
                # Though if both were removed, then uses the new format
                # (without underscore)
                if name1 == name2:
                    key = name1

                # For list/tuple dynamically create index in path
                if isinstance(obj1, list) or isinstance(obj1, tuple):
                    key = 'index[{}]'.format(key)

                # Create a + object
                added = AddedItem(
                    item=key,
                    path=path,
                    value=obj1_item,
                    config=self.config)

                # Create a - object
                removed = RemovedItem(
                    item=key,
                    path=path,
                    value=obj2_item,
                    exclude=self.exclude,
                    config=self.config)

                # Create a -+ object
                # Minus first just like Linux diff
                modified = ModifiedItem(
                    items=[removed, added],
                    exclude=self.exclude,
                    config=self.config)

                items.append(modified)

            elif self.verbose and iterable_parent:
                key = self._convert(obj1, key)

                # For list/tuple dynamically create index in path
                if isinstance(obj1, list) or isinstance(obj1, tuple):
                    key = 'index[{}]'.format(key)

                unchanged = UnchangedItem(
                    item=key,
                    path=path,
                    value=obj1_item,
                    config=self.config)

                items.append(unchanged)

        if self.verbose and not is_different:
            items = DiffList(filter(lambda i: not isinstance(i, UnchangedItem), items))

        return items

    def _diff_list_ignoring_index(self, obj1_item, obj2_item, temp_path):
        """Does a diff on a list but ignores index changes. For example
        if an element moves to a different index but the values remain
        the same then it wont be shown in the diff."""

        def _get_diffs(list1, list2, func, path, list_of_items):
            """Actual logic for finding the diffs"""

            # Sort the lists and the elements to ensure a smooth comparison
            list1 = recursive_sort(list1)
            list2 = recursive_sort(list2)

            diff_list = [item for item in list1 if item not in list2]
            for list_item in diff_list:
                # Find all indices where x exists in list1
                indices = [i for i, x in enumerate(list1) if x == list_item]

                for index in indices:
                    item = func(
                        item='index[{}]'.format(index),
                        path=path,
                        value=list1[index],
                        config=self.config)

                    list_of_items.append(item)

        items = []
        # checking for items removed
        _get_diffs(obj2_item, obj1_item, RemovedItem, temp_path, items)
        # checking for items added
        _get_diffs(obj1_item, obj2_item, AddedItem, temp_path, items)

        return items

    def _convert(self, obj, var):
        """Convert managed attribute name to name expected by the user"""
        # Useful when parsing Conf Object
        # Check if it has _ at the front, and if it was added
        # as part of managedattribute
        try:
            var.startswith('_')
        except AttributeError:
            return var

        no_underscore = var[1:]
        # check if it exists in the class
        if hasattr(self._find_parent_class(obj), no_underscore):
            return no_underscore
        return var

    def _find_parent_class(self, obj):
        """Find the top level parent class; useful for Conf object """
        # Useful when parsing Conf Object
        if hasattr(obj, 'parent'):
            return self._find_parent_class(obj.parent)
        return obj.__class__

    # Small helper APIs to make the findDiff code dynamic
    def _get_keys(self, obj):
        """Find the keys to compare

        For an object it will be __dict__.keys()
        For a dict, it will be .keys()
        For Config object it will use .config.keys()
        """
        if isinstance(obj, dict) or isinstance(obj, SubAttributesDict):
            return obj.keys()

        elif issubclass(obj.__class__, FeatureBase) or\
                isinstance(obj, SubAttributes) or\
                isinstance(obj, _genie_Base):
            return obj.__dict__.keys()

        elif isinstance(obj, Config):
            return obj.config.keys()

        elif isinstance(obj, list) or\
                isinstance(obj, tuple):
            return [index for index, value in enumerate(obj)]

        raise TypeError('Type {t} is not supported'.format(t=type(obj)))

    def _get_attr(self, obj, name):
        """Retrieve value of an attribute name for an object"""
        if isinstance(obj, dict) or\
                isinstance(obj, SubAttributesDict) or\
                isinstance(obj, list) or\
                isinstance(obj, tuple):
            return obj[name]

        elif issubclass(obj.__class__, FeatureBase) or\
                isinstance(obj, SubAttributes) or\
                isinstance(obj, _genie_Base):
            return getattr(obj, name)

        elif isinstance(obj, Config):
            return obj.config[name]

        raise TypeError('Type {t} is not supported'.format(t=type(obj)))

    def _get_path(self, obj, path, key):
        """Figure out how to build the path

        Square brackets for dict, and dict like,
        dot for object
        """
        if path == '':
            return str(key)

        # Path is always built the same way for the object
        # we are aware of
        if isinstance(obj, dict) or\
                isinstance(obj, SubAttributesDict) or\
                issubclass(obj.__class__, FeatureBase) or\
                isinstance(obj, SubAttributes) or\
                isinstance(obj, _genie_Base) or\
                isinstance(obj, Config):
            return path + "\n" + str(key)

        elif isinstance(obj, list) or\
                isinstance(obj, tuple):
            return path + "\n" + 'index[{}]'.format(key)

        raise TypeError('Type {t} is not supported'.format(t=type(obj)))

    def _is_recursive(self, obj1, obj2):
        """Is obj1 and obj2 objects that we need to dig further in?"""
        if (isinstance(obj1, SubAttributesDict) and
            isinstance(obj2, SubAttributesDict)) or\
           (isinstance(obj1, SubAttributes) and\
            isinstance(obj2, SubAttributes)) or\
           (isinstance(obj1, dict) and
            isinstance(obj2, dict)) or\
           (isinstance(obj1, _genie_Base) and\
            isinstance(obj2, _genie_Base)) or\
           (isinstance(obj1, list) and\
            isinstance(obj2, list)) or\
           (isinstance(obj1, tuple) and\
            isinstance(obj2, tuple)):
            return True
        else:
            # Nope,  just a normal value
            return False

    def _execute_callables(self, key, path):
        for ca in self._callables:
            # If this explodes its the users issue.
            if ca(key, _path=path):
                return True
        else:
            return False

class BaseItem(object):
    """Parent for Add/Remove for dictionary comparison """
    def __init__(self, value, path, item, config, exclude=None):
        self.value = value
        self.path = path
        self.item = item
        self.config = config
        self.exclude = exclude or []

    def __str__(self):
        # For each line of path, add a sign and some indentation
        ret = []
        indent = 0
        # If no path,  then no path :)
        if self.path:
            for line in self.path.splitlines():
                ret.append('{s}{i}{line}{c}'.format(
                    s=self.sign,
                    i=' '*indent,
                    line=line,
                    c=':' if not self.config else '',))

                indent += 1

        # Now depending on previous indentation,  expand the value
        # Keep in mind value could be 1 value,  or many. It depends where the
        # diff happened.
        value = expand(self.value, indent+1, sign=self.sign,
                       colon=not self.config)
        ret.append('{s}{i}{item}{c}{value}'.format(
            s=self.sign,
            i=' '*indent,
            item=self.item,
            c=':' if not self.config else '',
            value=value))

        return '\n'.join(ret)

    def diff_string(self):
        # For each line of path add indentation
        ret = []
        indent = 0
        # If no path, then no path :)
        if self.path:
            for line in self.path.splitlines():
                ret.append('{i}{line}'.format(i=' '*indent, line=line))
                indent += 1

        # Now depending on previous indentation,  expand the value
        # Keep in mind value could be 1 value,  or many. It depends where the
        # diff happened.
        value = expand(self.value, indent+1, sign='', colon=False)
        ret.append('{i}{item}{value}'.format(
            i=' '*indent,
            item=self.item,
            value=value))

        return '\n'.join(ret)


class UnchangedItem(BaseItem):
    def __init__(self, *args, **kwargs):
        self.sign = ' '
        super().__init__(*args, **kwargs)


class AddedItem(BaseItem):
    def __init__(self, *args, **kwargs):
        self.sign = '+'
        super().__init__(*args, **kwargs)


class RemovedItem(BaseItem):
    def __init__(self, *args, **kwargs):
        self.sign = '-'
        super().__init__(*args, **kwargs)


class ModifiedItem(object):
    """Diff Add/Remove/Diff objects together"""
    def __init__(self, items, exclude=None, config=False, keep_order=False):
        # For each of the items,
        self.items = items
        self.config = config
        self.keep_order = keep_order

        if items:
            if all(item.path == items[0].path for item in items):
                # All paths are the same so use the first
                self.path = items[0].path
            else:
                # Paths are different. Find where the path differs.
                diff_index = 0
                for sp, ip in zip(items[0].path.splitlines(),
                                  items[1].path.splitlines()):
                    if sp == ip:
                        diff_index += 1
                    else:
                        break
                self.path = '\n'.join(items[0].path.splitlines()[:diff_index])
        else:
            self.path = ''

        # Just for sorting
        self.item = ''
        self.exclude = exclude or []

    def __str__(self):
        ret = []
        indent = 0
        # If no path, then no path :)
        if self.path:
            for line in self.path.splitlines():
                ret.append(' {i}{line}{c}'.format(
                    i=' '*indent,
                    line=line,
                    c=':' if not self.config else ''))

                indent += 1

        # Find how much path to remove (already printed)
        remove = len(self.path.splitlines())
        iterable_obj = self.items

        if not self.keep_order:
            iterable_obj = sorted(self.items, key=lambda i: str(i.item))

        for item in iterable_obj:
            ret.append('\n'.join(str(item).splitlines()[remove:]))

        return '\n'.join(ret)

def expand(d, indent, sign='', colon=True):
    """ expand datastructure into line by line diff type representation
    by recursively going through values - Adding indexes for list/tuples"""
    ret = []

    if isinstance(d, dict):
        for k,v in sorted(d.items(), key=lambda i: str(i)):
            # add key
            ret.append('\n{s}{i}{k}{c}'.format(
                s=sign,
                i=' '*indent,
                k=k,
                c=':' if colon else ''))

            # recurse to check values of the key
            ret.append(expand(v, indent+1, sign, colon))
    elif isinstance(d, (list, tuple)):
        for k,v in enumerate(d):
            # add each index[]
            ret.append('\n{s}{i}index[{k}]{c}'.format(
                s=sign,
                i=' '*indent,
                k=k,
                c=':' if colon else ''))

            # recurse to check values in the index
            ret.append(expand(v, indent+1, sign, colon))
    else:
        # this is a single value (not an iterable)
        if str(d):
            ret.append(' ' + str(d))

    return ''.join(ret)

def sorter(item):
    """Sorter function.
    int > str > dict > list > other"""
    if isinstance(item, int):
        return 0, item
    if isinstance(item, str):
        return 1, item
    if isinstance(item, dict):
        keys = [str(i) for i in item.keys()]
        return 2, keys
    if isinstance(item, list):
        return 3, item.sort(key=sorter)
    return 4, item

def recursive_sort(item):
    if isinstance(item, list):
        for index, value in enumerate(item):
            item[index] = recursive_sort(value)
        item.sort(key=sorter)
        return item
    elif isinstance(item, dict):
        for key, value in item.items():
            item.update({key: recursive_sort(value)})
        return OrderedDict(sorted(item.items(), key=sorter))
    else:
        return item
