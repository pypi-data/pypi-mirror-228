import re
import ast
import logging

from typing import Iterable

# genie
from genie.utils.loadattr import str_to_list

# pyats
from pyats.datastructures.listdict import ListDict
from pyats.datastructures.listdict import IndexMarker

log = logging.getLogger(__name__)


class Dq(object):
    def __init__(self, var=None):
        if not var:
            var = {}
        self.var = var or {}
        self.paths = ListDict(var)

    def __iter__(self):
        yield from self.paths

    def __repr__(self):
        return 'Dq(paths={})'.format(self.paths)

    def __getitem__(self, key):
        return self.paths[key]

    def __len__(self):
        return len(self.paths)

    def __eq__(self, other):
        return self.paths == other.paths

    def contains(self, value, regex=False, _contains=True, level=None, escape_special_chars=None,
                 ignore_case=False):

        # if value specified, special chars that are specified will be escaped.
        if escape_special_chars:
            value = self._escape_special_chars(value, escape_special_chars)

        new = Dq()
        for item in self:
            if self._contains(value, item, _contains=_contains, regex=regex, ignore_case=ignore_case):
                new.paths.append(item)

        if not level:
            return new

        new_level = Dq()
        # get new path from lower/upper level based on given `level`
        for item in new.paths:
            if len(item.path[:level]) == 0:
                value = item.path[len(item.path)-1]
            else:
                try:
                    value = item.path[:level][-1]
                except IndexError:
                    return new_level
            paths = self if _contains else new.paths
            # do `contains` agains new path based on given `level`
            for item2 in paths:
                if (self._contains(
                        value, item2, _contains=_contains, regex=regex)
                        and item2 not in new_level.paths):
                    new_level.paths.append(item2)

        return new_level

    def not_contains(self, *args, **kwargs):
        return self.contains(_contains=False, *args, **kwargs)

    def _contains(self, value, item, _contains=False, regex=False, ignore_case=False):

        # create a tuple made of all the keys in a path and its value
        full_path = item.path + (item.value,)

        if isinstance(value, (list, tuple)):
            return self._contains_value_is_list(value, item, full_path, regex, _contains)

        # if user send regex in
        if regex:
            return self._item_in_full_path_regex(value, full_path, _contains, ignore_case=ignore_case)

        # if the input is not regex validate it here otherwise return false
        return bool((value in full_path) and _contains or\
           (value not in full_path) and not _contains)

    def _item_in_full_path_regex(self, value, full_path, _contains, ignore_case=False):
        # checks if a regex matches an item in the full path

        #To handle the case insensitive
        flags=0
        if ignore_case:
            flags=re.IGNORECASE

        # as soon as there is one match we check the return value
        for path in full_path:
            if not isinstance(path, IndexMarker) and re.fullmatch(str(value), str(path), flags):
                break
        else:
            # if not break then not a match
            return not _contains
        return bool(_contains)

    # Contains key and value
    def contains_key_value(self, key, value, key_regex=False, value_regex=False ,_contains=True, escape_special_chars_key=None,
                           escape_special_chars_value=None, ignore_case_key=False, ignore_case_value=False):

        # if value specified, special chars that are specified will be escaped.
        if escape_special_chars_key:
            key = self._escape_special_chars(key, escape_special_chars_key)

        if escape_special_chars_value:
            value = self._escape_special_chars(value, escape_special_chars_value)

        # Make sure that key is then followed by value
        new = Dq()
        for item in self:
            full_path = item.path + (item.value,)

            # collecting all the indices of possible matches between the inputs
            # and keys and value in an item fullpath
            key_indices =  self._item_matched_full_path(key, full_path, key_regex, ignore_case_key=ignore_case_key)

            # if we have a list of indices than we have matches
            # now we just have to make sure that key and value are back to back
            if key_indices:
                if (isinstance(value, (list, tuple)) and \
                    self._contains_value_is_list(value, item, full_path, value_regex, _contains, key_indices=key_indices)) or \
                    self._contains_key_value(value, full_path, key_indices, value_regex, _contains, ignore_case_value=ignore_case_value):
                    new.paths.append(item)
            elif not _contains:
                new.paths.append(item)
        return new

    def _contains_value_is_list(self, value, item, full_path, regex, _contains, key_indices=None):

        # if the query value is a list, e.g. contains([1,2,3])
        # OR contains_key_value('key', [1,2,3])
        if regex:
            return False

        for path in full_path:

            if isinstance(path, IndexMarker):
                exclude_length = item.path.index(path) - 1
                if isinstance(full_path[exclude_length], IndexMarker):
                    continue
                if key_indices and exclude_length not in key_indices:
                    continue
                item_value = self._subdict(item, exclude_length)
                if value == item_value:
                    break
        else:
            # if we found no key and value
            return not _contains
        return bool(_contains)

    def not_contains_key_value(self, *args, **kwargs):
        return self.contains_key_value(_contains=False, *args, **kwargs)

    def _item_matched_full_path(self, value, full_path, _regex, ignore_case_key=False, ignore_case_value=False):

        ret_list = []
        for item in full_path:

            if _regex and not isinstance(item, IndexMarker):

                # To handle the case insensitive
                flags = 0
                if ignore_case_key or ignore_case_value:
                    flags = re.IGNORECASE

                # if the input is regex do the pattern matching
                p = re.compile(str(value), flags)
                m = p.fullmatch(str(item))

            else:
                # otherwise check for equal and set m to True or False
                m = (item == value)

            if m:
                # check for indices of the matched items and collect them.
                temp_list = self._index_collector(item, full_path)
                ret_list.extend(temp_list)

        return ret_list

    def _index_collector(self, value, full_path):

        # collect all the matched items indices

        indices_list = set()
        offset = -1
        while True:
            try:
                offset = full_path.index(value, offset+1)
            except ValueError:
                break
            indices_list.add(offset)

        return list(indices_list)

    def _contains_key_value(self, value, full_path, key_indices, value_regex, _contains, ignore_case_value=False):

        value_indices = self._item_matched_full_path(value, full_path, value_regex, ignore_case_value=ignore_case_value)

        for key_index in key_indices:

            # find one key and value that matches the inputs
            # and are back to back in full_path
            if key_index +1 in value_indices:
                break
        else:
            # if we found no key and value
            return not _contains
        return bool(_contains)

    def value_operator(self, key, operator, value):
        # It only works for float so make sure value is float
        # If not an float, try to convert to an float, else its game over
        try:
            value = float(value)
        except ValueError:
            raise Exception('{} must be of type int'.format(value))

        # For each path, make sure key is there, check the value after to see
        # if it has the value expected
        # Could call contains, but it would requires to loop over the data
        # twice,
        new = Dq()
        for item in self:
            try:
                found_value = self._find_item_value(item, key)
            except ValueError:
                continue

            try:
                found_value = float(found_value)
            except ValueError:
                log.debug('{} is not of type float'.format(found_value))
                raise Exception('{} must be of type float'.format(found_value))

            if not self._evaluate_operator(found_value, value, operator):
                continue

            # the key of this location should be the value we want

            # Find the value
            new.paths.append(item)
        return new

    def sum_value_operator(self, key, operator, value):
        # It only works for float so make sure value is float
        # If not an float, try to convert to an float, else its game over
        try:
            value = float(value)
        except ValueError:
            raise Exception('{} must be of type float'.format(value))

        # For each path, make sure key is there, check the value after to see
        # if it has the value expected
        # Could call contains, but it would requires to loop over the data
        # twice,
        sum_value = 0
        found_flag = False
        new = Dq()
        for item in self:
            try:
                found_value = self._find_item_value(item, key)
            except ValueError:
                continue

            try:
                found_value = float(found_value)
            except ValueError:
                log.debug('{} is not of type float'.format(found_value))
                raise Exception('{} must be of type float'.format(found_value))

            sum_value += found_value
            found_flag = True

        if self._evaluate_operator(sum_value, value, operator) and found_flag:
            log.debug('sum_value_of_{}: {}'.format(key, sum_value))
            new.paths.append(((key,), sum_value))

        return new

    def _evaluate_operator(self, value_left, value_right, operator):
        if operator == '>':
            return value_left > value_right
        elif operator == '<':
            return value_left < value_right
        elif operator == '>=':
            return value_left >= value_right
        elif operator == '<=':
            return value_left <= value_right
        elif operator == '==':
            return value_left == value_right
        elif operator == '!=':
            return value_left != value_right
        else:
            raise Exception('Operator {} is not supported'.format(operator))

    # Method which does not return a Dq
    # They are "ender" methods

    def get_values(self, key, index=None, ignore_case_key=False):
        # Return a list of all the values of this key
        # This does not create back a Dq
        values = []
        exclude = set()
        # This method must make sure it doesn't add multiple times the same
        # element - This happen when using get_values and it isn't a leaf of the
        # dict.
        # Easy way, check which item contains this field, and remove them
        # This is what exclude does
        for item in self:
            next_item = any(
                item.path[:exclude_length] == exclude_path
                for exclude_length, exclude_path in exclude
            )

            if next_item:
                continue
            # Get_values can also receive the nested level as a number
            # Useful when we want the first level and it doesn't have a parent
            if not isinstance(key, int) and\
                    key[0] == '[' and key[-1] == ']' and\
                    key[1:-1].isdigit():
                try:
                    value = item[0][int(key[1:-1])]
                except IndexError:
                    continue
            else:
                try:
                    value = self._find_item_value(item, key)
                except ValueError:
                    continue

            if item.value == value and value not in item.path:
                values.append(value)
                continue

            # If the key matches any item before the last element of the item.path
            # the exclude length would be equal exclude_path above and continues the second loop
            # which in turns prevent copy printing of non leaf values
            try :
                exclude_length = item.path.index(value) + 1
            except ValueError:

                # The value to the key is a list.
                # parse the input dictionary up to the key and extract its value to append into the result
                exclude_length = item.path.index(key)
                value = self._subdict(item, exclude_length)

            finally:
                exclude_path = item.path[:exclude_length]
                exclude.add((exclude_length, exclude_path))
                if isinstance(value, (list, tuple)):
                    values.extend(value)
                else:
                    values.append(value)

        # Allow to return a specific index or range of index when calling
        # get_values
        if index is None:
            return values
        index = str(index).strip('[]').split(':')
        if len(index) == 1:
            try:
                return values[int(index[0])]
            except IndexError:
                return []
        slice_ = slice(*[int(p) if p else None for p in index])
        return values[slice_]

    def _subdict(self, item, exclude_length):

        value_dict = self.reconstruct()

        for i in item.path[:exclude_length+1]:
            # if an IndexMarker exist in the value exclude item.path
            # A list is inside the initial list
            # it is necessary to go inside the nested dictionary that is within a list
            if isinstance(i, IndexMarker):
                value_dict = value_dict[i.index]
                continue

            value_dict = value_dict[i]

        return value_dict

    def count(self):
        # Return how many matches is remaining
        return len(self)

    def raw(self, key):
        # key: "['0']['bla']['aa'][0]"
        keys = str_to_list(key)

        # Just return what was asked by the user
        reconstruct = self.reconstruct()

        # Loop through each key provided; at the end return the value
        # We check of str first, than int to cover both cases
        for key in keys:
            try:
                reconstruct = reconstruct[str(key)]
            except (KeyError, TypeError):
                # TypeError is for string
                try:
                    reconstruct = reconstruct[int(key)]
                except (ValueError, KeyError):
                    # Could not find the value, either as a str or an int
                    raise KeyError("'{k} does not exists in the "\
                                   "dictionary".format(k=key))
        return reconstruct

    def reconstruct(self):
        return self.paths.reconstruct()

    def _find_item_value(self, item, key):
        # Find a key in the item and get the value out of it
        k_index = item.path.index(key)
        # Convert to dict
        dp = Dq()
        dp.paths.append(item)
        item_dict = dp.reconstruct()
        for element in item.path[:k_index+1]:
            if isinstance(element, IndexMarker):
                item_dict = item_dict[0]
                continue

            item_dict = item_dict[element]

        # Check the type of return value and return the appropriate item
        if isinstance(item_dict, dict):
            return list(item_dict.keys())[0]
        # if Iterable but not dict, we need to iterate through the values within the list again
        elif isinstance(item_dict, list):
            # Checks if item_dict has only an empty list and and returns [[]]
            if len(item_dict) == 1 and item_dict[0] == []:
                return item_dict

            return item_dict[0] if len(item_dict) > 1 else []
        else:
            return item_dict

    # This would check if the queries to the dictionary is valid
    @staticmethod
    def query_validator(query):

        query_list = Dq._splitted_query_list(query)
        # if empty than no query or not appropriate query
        if not query_list:
            return False

        p = re.compile(r'(?P<function>\w+)\((?P<arguments>[\S\s]+)?\)')

        for query in query_list:
            m = p.match(query)
            # if functions are not valid or it does not follow proper function defnition convention return False
            if not m or not hasattr(Dq, m.groupdict()['function']):
                return False

        return True

    # if valid this would return the value outputs
    @staticmethod
    def str_to_dq_query(output, query):
        query_list = Dq._splitted_query_list(query)
        p = re.compile(r'(?P<function>\w+)\((?P<arguments>[\S\s]+)?\)')
        try :
            dq_output = Dq(output)
        except Exception as e:
            raise Exception('Issue creating filtering object, as the output is not as expected, {}'.format(str(e)))

        for query in query_list:
            # Will never go in the first time, as dq_output is created above
            # If subsequent aren't a Dq object, than fail
            if not isinstance(dq_output, Dq):
                raise Exception('The output of the previous function does not'
                                ' provide the appropriate input for the next function ==> {}'.format(previous_filter))

            m = p.match(query)
            function = m.groupdict()['function']
            if m.groupdict()['arguments']:
                arguments = m.groupdict()['arguments']
                tree = ast.parse("f({})".format(arguments))
                funccall = tree.body[0].value
                args = [ast.literal_eval(arg) for arg in funccall.args]
                kwargs = {arg.arg: ast.literal_eval(arg.value) for arg in funccall.keywords}
                # Calling the function
                dq_output = getattr(dq_output, function)(*args, **kwargs)
            else:
                dq_output = getattr(dq_output, function)()

            previous_filter = filter
        return dq_output.reconstruct() if isinstance(dq_output, Dq) \
            else dq_output

    @staticmethod
    def _splitted_query_list(query):

        # In blitz where right now this function gets called the most
        # include/exclude values could be int/bool
        # In case query is not Iterable case to string
        if not isinstance(query, Iterable):
            query = str(query)

        for i in range(len(query)):

            # if last element of the array no point of checking that element
            if i != len(query) - 1:
                if query[i] == '.':
                    if query[i-1] == ')' and query[i+1].isalpha():
                        query = query[:i] + ';' + query[i+1:]

        # This change is needed for query validator to return false
        # in dq for cases that query is not string and is dict or list.
        # When query_validator returns false,
        # for instance in blitz the code can recognize the input
        # as a non_dq_query and act accordingly.
        try:
            query_list = query.split(';')
        except AttributeError:
            return []

        return query_list

    def _escape_special_chars(self, user_input, special_char_list):

        # special chars specified by users will be escaped
        for special_char in special_char_list:
            try:
                user_input = user_input.replace(special_char, r"\{}".format(special_char))
            except AttributeError as e:
                raise AttributeError('Special characters cannot be skipped when the input is not'
                                     ' a string. {}'.format(e))

        return user_input

#from genie.testbed import load
#tb = load('jb.yaml')
#dev = tb.devices['csr1000v-1']
#dev.connect()
##
#x = dev.parse('show module')
# x = {'rp': {'1': {'NX-OSv Supervisor Module': {'ports': '0', 'model': 'N7K-SUP1', 'status': 'active', 'software': '7.3(0)D1(1)', 'hardware': '0.0', 'slot/world_wide_name': '--', 'mac_address': '5e-00-40-01-00-00 to 5e-00-40-01-07-ff', 'serial_number': 'TM40010000B'}}}, 'lc': {'2': {'NX-OSv Ethernet Module': {'ports': '48', 'model': 'N7K-F248XP-25', 'status': 'ok', 'software': 'NA', 'hardware': '0.0', 'slot/world_wide_name': '--', 'mac_address': '02-00-0c-00-02-00 to 02-00-0c-00-02-7f', 'serial_number': 'TM40010000C'}}, '3': {'NX-OSv Ethernet Module': {'ports': '48', 'model': 'N7K-F248XP-25', 'status': 'ok', 'software': 'NA', 'hardware': '0.0', 'slot/world_wide_name': '--', 'mac_address': '02-00-0c-00-03-00 to 02-00-0c-00-03-7f', 'serial_number': 'TM40010000D'}}, '4': {'NX-OSv Ethernet Module': {'ports': '48', 'model': 'N7K-F248XP-25', 'status': 'ok', 'software': 'NA', 'hardware': '0.0', 'slot/world_wide_name': [1,2,3], 'mac_address': '02-00-0c-00-04-00 to 02-00-0c-00-04-7f', 'serial_number': 'TM40010000E'}}}}
#o1 = {'total_peers': 1, 'total_established_peers': 1, 'local_as': 65000, 'vrf': {'default': {'local_as': 65000, 'vrf_peers': 1, 'vrf_established_peers': 1, 'router_id': '10.2.2.2', 'neighbor': {'10.1.1.1': {'remote_as': 65000, 'connections_dropped': 1, 'last_flap': '3d14h', 'last_read': '00:00:01', 'last_write': '00:00:32', 'state': 'established', 'local_port': 179, 'remote_port': [1,3,2,9], 'notifications_sent': 1, 'notifications_received': 0}}}}}

#o2 = {'vrf': {'default': {'neighbor': {'10.1.1.1': {'address_family': {'ipv4 unicast': {'neighbor_table_version': 4, 'as': 65000, 'msg_rcvd': 5694, 'msg_sent': 5175, 'tbl_ver': 11, 'inq': 0, 'outq': 0, 'up_down': '3d14h', 'state_pfxrcd': '1', 'prefix_received': '1', 'state': 'established', 'route_identifier': '10.2.2.2', 'local_as': 65000, 'bgp_table_version': 11, 'config_peers': 1, 'capable_peers': 1, 'attribute_entries': '[2/288]', 'as_path_entries': '[0/0]', 'community_entries': '[0/0]', 'clusterlist_entries': '[0/0]', 'prefixes': {'total_entries': 2, 'memory_usage': 288}, 'path': {'total_entries': 2, 'memory_usage': 288}}}}}}}}
#rs = R(["slot", "(?P<val1>.*)", "lc", "(?P<val2>.*)", "state", "up"])
##ret = find([x], rs, filter_=False, all_keys=True)
#
##y = Dq('ok', x)
##x = Dq('status', x)
##x = Dq(x, 'status')
##x = Dq(x).not_contains_key('state', 'Established')
##x.contains('qweqwe')
#
##In [2]: jmespath.search('*.{\"oper_status\":oper_status}[?oper_status==`up`]', xinfo)
#
# UNCOMMENT ME
#mod = Dq(x)
#mod.raw("[rp][1]")
#mod.contains([1,2,3])
#od = Dq(o1)
#mod.raw("[rp][1][NX-OSv Supervisor Module][model][0]")
#mod.contains('.*ware', regex=True)
#mod.not_contains('.*(address|number).*', regex=True)
#mod.not_contains('1|4', regex=True).not_contains('.*ware', regex=True)
#mod.contains('(1|4)', regex=True).not_contains('.*ware', regex=True).not_contains('2')
#mod.contains_key_value('model', 'N7K.*', value_regex=True)
#mod.contains_key_value('ports', 'N7K.*', value_regex=True)
#mod.contains_key_value('model', 'N7K')
#mod.contains_key_value('NX-OSv.*', '.*ware', key_regex=True, value_regex=True)
#mod.not_contains_key_value('lc', '(3|4)', value_regex=True).not_contains('N7.*', regex=True).not_contains('NA')
#mod.get_values('lc', index=1)
#mod.get_values('lc', index='1')
#mod.get_values('lc', index='1:')
#mod.get_values('lc')
#mod.contains('status').not_contains('lc')
#mod.value_operator('lc', '==', 2)
#mod.reconstruct()
#
## TODO do we need to support multiple element? Right now supports OR
#
##mod.contains_key_value('status', 'baana')
##mod.value_operator('status', '==', 'baana')
#
#mod.contains_key_value('status', 'ok')
#mod.not_contains_key_value('status', 'ok')
#
#mod.value_operator('lc', '>', '2')
#
#y = Dq(o2)
#y.contains('state')
#y.contains('total_entries')
#y.value_operator('total_entries', '<', 5)
#y.value_operator('total_entries', '>', 5)
#y.value_operator('total_entries', '<=', 5)
#y.value_operator('total_entries', '>=', 5)
## Those two, I am not sure if we should keep as same as contains key and not
## contains key
#y.value_operator('total_entries', '==', 5)
#y.value_operator('total_entries', '!=', 5)
#
#mod.contains_key_value('lc', '2')
#mod.get_values('lc')
#y.get_values('total_entries')
#mod.not_contains_key_value('lc', '2')
#
