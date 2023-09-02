import re
import copy
import json
import logging
from itertools import chain, product
from collections import deque, OrderedDict
from genie.libs.parser.utils.common import get_parser

from .exceptions import InvalidDest
# import pcall
import importlib
try:
    pcall = importlib.import_module('pyats.async').pcall
except ImportError:
    from pyats.async_ import pcall
# # import pcall
# from pyats.async import pcall
from pyats.connections.pool import ConnectionPool
from genie.metaparser.util.schemaengine import Schema
from genie.metaparser.util.exceptions import SchemaEmptyParserError,\
                                       InvalidCommandError

from genie.utils.summary import Summary
from genie.conf.base.utils import QDict
# module level logger
log = logging.getLogger(__name__)


def _product_dict(dicts):
    # If parser_kwargs has a list, then do permutation
    # Convert to a list
    dicts = dicts.copy()
    for key, value in dicts.items():
        if isinstance(value, str):
            # IF value has text, then split it, if no text, then ['']
            # as product needs value in the empty list
            dicts[key] = value.split(',') if value else ['']
        elif isinstance(value, int):
            dicts[key] = [value]
        elif value is None:
            dicts[key] = ['']
        else:
            dicts[key] = list(value)

    keys = dicts.keys()
    vals = dicts.values()
    for instance in product(*vals):
        yield dict(zip(keys, instance))

def _merge_dict(a, b, path=None):
    '''merges b into a for as many level as there is'''
    # Dict to use to return
    ret = a
    if path is None:
        path = []
    for key in b:
        if key in ret:
            if isinstance(ret[key], dict) and isinstance(b[key], dict):
                _merge_dict(ret[key], b[key], path + [str(key)])
            elif ret[key] == b[key]:
                # same leaf value so do nothing
                pass
            else:
                # Any other case
                raise Exception('{key} cannot be merged as it already '
                                'exists with type '
                                '{ty}.'.format(key=key, ty=type(ret[key])))
        else:
            ret[key] = b[key]
            if key in b.leaf_dict:
                ret.leaf_dict[key] = b.leaf_dict[key]

    return ret


class CmdDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.leaf_dict = {}

def keep_going(output, cmd):
    ''' Recursively loop over the dict until we reach the deepest level
        then we assing the cmd to the dictionary keys.
    '''

    output = CmdDict(output)
    for key, value in output.items():
        if isinstance(value, dict):
            # We didn't reach the end of the dictionary yet.
            output[key] = keep_going(value, cmd)
        else:
            output.leaf_dict[key] = cmd

    return output

def _list_to_dict(path, output, cmd):
    '''From a list create a dictionary structure

    Last value of the list is the value of the dictionary'''
    ret = CmdDict()
    for item in path:
        current_level = ret
        length = len(item)
        i = 0
        for part in item:
            if i == length-1:
                if isinstance(output, dict):
                    # We didn't reach the end of the dictionary yet.
                    current_level[part] = keep_going(output, cmd)
                else:
                    current_level[part] = output
                    current_level.leaf_dict[part] = cmd
                continue
            elif part not in current_level:
                current_level[part] = CmdDict()
            current_level = current_level[part]
            i+=1
    return ret


class Maker(object):
    """Base class for all genie.conf objects

    Base class for all objects of the genie.conf infrastructure.
    All of these objects are related to a Testbed.

    `__init__` allows to set all `**kwargs` to be set automatically
    in the object.
    """
    def __init__(self, parent, attributes=None, commands=None, raw_data=False):

        # Verify if any attributes were given
        if attributes:
            assert type(attributes) == list, "'attributes' needs to be a "\
                                             "'list'. {attributes} is of type"\
                                             " '{ty}'".format(
                                                     attributes=attributes,
                                                     ty=type(attributes))
            self.attributes = attributes
        else:
            # Default is an empty list
            self.attributes = []

        if commands:
            assert type(commands) == list, "'commands' needs to be a "\
                                           "'list'. {commands} is of type "\
                                           "'{ty}'".format(commands=commands,
                                                           ty=type(commands))
            self.commands = commands
        else:
            self.commands = []

        self.parent = parent
        self.leafs = []
        self.outputs = {}
        self._keys = []
        self.raw_data = raw_data
        self.reset_parameters()

    def reset_parameters(self):
        self.summary_table = {}
        # Initializing 'Learn commands' dictionary under summary_table
        # 'Command': 'command related keys (ex: vrf:Blue)'
        self.summary_table['Learn commands'] = OrderedDict()
        self.summary_table['Executed Fine'] = []
        self.summary_table['Not accepted'] = []
        self.summary_table['Empty'] = []

    def add_leaf(self, *, cmd, device, src, dest, keys=None, callables=None,
                 action=None, **kwargs):
        '''Add a leaf to Maker'''
        # If any leaf receive a kwargs with a list value, create a product of
        # these list
        parser_kwargs = _product_dict(kwargs)
        for kwarg in parser_kwargs:
            self.leafs.append(Leaf(parent=self.parent, attributes=self.attributes,
                                   outputs=self.outputs, keys=self._keys,
                                   cmd=cmd, device=device, src=src, dest=dest,
                                   callables=callables, action=action, **kwarg))

    def make(self, **kwargs):
        '''Create all the leafs'''

        self.print = kwargs.get('final_call', None)

        if self.print:
            # Need to delete since we pass the kwargs to the parser later
            del kwargs['final_call']

        # Variables to control which cli to learn, and which
        # to use already learnt cli.
        after = []
        learnt = {}
        to_learn = OrderedDict()
        self.commands_copy = []

        # Let's figure out which leaf do we run
        # And send the cmd to the device for those ones

        # Check for the commands' list provided by the user
        if self.commands:
            self.commands_copy = self.commands.copy()

        for leaf in self.leafs:
            # Check if leaf cmd is among the ones sent by the user to be learnt
            if isinstance(leaf.cmd, str):
                # leaf.device is the connection and not the device object
                # we need the device object, and get_parser also return the arguments
                # which we dont need for finding the parser cls
                leaf.command = re.sub(' +', ' ', leaf.cmd)
                try:
                    leaf.cmd = get_parser(leaf.cmd, leaf.device.device)[0]
                except Exception as e:
                    raise Exception("Could not find parser class for command '{command}'"\
                        .format(command=leaf.cmd))

            if self.commands:
                if leaf.cmd in self.commands:
                    # Checking user's sent commands validity (if the command
                    # is part of the feature ops structure). If not, will
                    # raise a ValueError later.
                    try:
                        self.commands_copy.remove(leaf.cmd)
                    except ValueError:
                        pass
                else:
                    continue

            # Verify if this leaf has already been created
            if leaf._made is True:
                # No need to do it again
                continue
            try:
                # Normalize src/dest and callables
                leaf._normalize(callables=self.parent.callables)

                # From src/dest, verify via attributes if we should execute
                # this leaf
                if leaf._validate():
                    # Check if any attributes has been sent in the leaf.

                    # 1: Learnt 
                    if leaf.cmd in self.outputs and\
                       leaf._str_kwargs in self.outputs[leaf.cmd]:
                        # Then already learnt
                        # Then after
                        after.append(leaf)

                    # 2: Not learnt, but will be learn so wait
                    elif leaf.cmd in to_learn and\
                         leaf._str_kwargs in to_learn[leaf.cmd]:
                        # Will be learn later, so wait
                        after.append(leaf)

                    # 3: Not learnt
                    else:
                        if leaf.cmd not in to_learn:
                            to_learn[leaf.cmd] = {}
                        to_learn[leaf.cmd][leaf._str_kwargs] = leaf
                else:
                    continue

            # Capture users error, not related to output
            except (AttributeError, ValueError, TypeError) as e:
                # If user do self.bla and bla doesn't exists
                # If user do t.bla, but only self are supported
                # Wrong regex; cannot merge keys
                raise Exception("Creation of the leaf with 'src' {src} failed "
                                "to be created."
                                .format(src=list(leaf.src))) from e
            # Error around the output, dont explode,
            # report it, but move on.
            except Exception as e:
                # Could not create this leaf
                log.debug("Creation of leaf with src {src} failed to "
                          "be created; {e}" .format(src=list(leaf.src), e=e))

        # Check if the user has provided the accurate commands that are part
        # of the ops structure, otherwise raise ValueError Exception
        # with self.print, make sure it's checked only at end of Ops
        if self.print and self.commands_copy:
            raise ValueError("Provided commands '{cmd}' "
                "is not part of the '{feature}' "
                "ops structure.".format(cmd=self.commands_copy,
                                        feature=self.parent))

        self.learned = to_learn

        if to_learn:
            if 'Learn commands' not in self.summary_table:
                self.summary_table['Learn commands'] = to_learn

            self.summary_table['Learn commands'].update(to_learn)

            async_list = []
            invalid_cmds = []
            empty_cmds = []
            passed_cmds = []
            for cmd, value in to_learn.items():
                for keyword, leaf in value.items():
                    # Initialize dict of outptus
                    if cmd not in self.outputs:
                        self.outputs[cmd] = {}

                    # If device inherits from connectionPool, use pcall,
                    # otherwise use
                    if isinstance(leaf.device, ConnectionPool):
                        if kwargs:
                            # Attaching the keyword arguments to the
                            # corresponding leaf
                            leaf.pcall_kwargs.update(kwargs)
                        async_list.append(leaf)
                    else:
                        # normal call
                        out = self._call_parser(leaf, **kwargs)
                        if out == 'empty':
                            empty_cmds.append(leaf)
                        elif out == 'invalid':
                            invalid_cmds.append(leaf)
                        else:
                            passed_cmds.append(leaf)
                        if log.getEffectiveLevel() <= logging.DEBUG:
                            log.debug(json.dumps(out, indent=2))
                        leaf.output = out
                        self.outputs[leaf.cmd][leaf._str_kwargs] = out

            if async_list:
                out = pcall(self._send_cmd, leaf=async_list)
                for output2, leaf in zip(out, async_list):
                    if output2 == 'empty':
                        empty_cmds.append(leaf)
                    elif output2 == 'invalid':
                        invalid_cmds.append(leaf)
                    else:
                        passed_cmds.append(leaf)
                    leaf.output = output2
                    self.outputs[leaf.cmd][leaf._str_kwargs] = output2

            self.summary_table['Executed Fine'].extend(passed_cmds)
            self.summary_table['Not accepted'].extend(invalid_cmds)
            self.summary_table['Empty'].extend(empty_cmds)

        if self.print:
            self.summarize_show_commands()

        # Populate the leaf in after
        for leaf in after:
            leaf.output = self.outputs[leaf.cmd][leaf._str_kwargs]

        # Go make all the leafs now
        leaves = [item for k, value in to_learn.items()\
                       for keywords, item in value.items()]
        for leaf in chain(leaves, after):
            try:
                leaf.make()

            # Capture users error, not related to output
            except (AttributeError, ValueError, TypeError) as e:
                # If user do self.bla and bla doesn't exists
                # If user do t.bla, but only self are supported
                # Wrong regex; cannot merge keys
                raise Exception("Creation of the leaf with 'src' {src} failed "
                                "to be created."
                                .format(src=list(leaf.src))) from e

            except InvalidDest:
                raise
            # Error around the output, dont explode,
            # report it, but move on.
            except Exception as e:
                # Could not create this leaf
                log.debug("Creation of leaf with src {src} failed to "
                          "be created; {e}" .format(src=list(leaf.src), e=e))

        if self.print:
            self._verify_schema()

    def _verify_schema(self):
       # Only difference, first value of dict are actually variables
       # of self.parent
       if not hasattr(self.parent, 'schema') or self.attributes or\
          self.commands:
           return False
       for key, value in self.parent.schema.items():
           # For each key, verify the dict
           if not hasattr(self.parent, key):
               # If the key does not exists at all under this ops object
               continue
           output = Schema(self.parent.schema[key]).validate(getattr(self.parent, key))


    def _call_parser(self, leaf, device=None, **kwargs):
        if not device:
            device = leaf.device
        cm = leaf.parent.context_manager

        if leaf.pcall_kwargs:
            parser_kwargs = dict(leaf.kwargs, **leaf.pcall_kwargs)
        else:
            parser_kwargs = dict(leaf.kwargs, **kwargs)
        if self.raw_data:
            parser_kwargs.update({'raw_data': self.raw_data})

        if leaf.cmd in cm:
            # Fallback meachanism will work if a list of contexts is sent
            if isinstance (cm[leaf.cmd], list):
                context_list = [key.value for key in cm[leaf.cmd]]
            else:
                context_list = cm[leaf.cmd].value

            try:
                ret = leaf.cmd(device=device,
                               context=context_list, command=leaf.command)
                out = QDict(ret.parse(**parser_kwargs))
                if hasattr(ret, 'raw_output'):
                    out.raw_output = ret.raw_output
            except SchemaEmptyParserError as e:
                log.info('Could not learn {cmd}\n{e}'.format(cmd=leaf.cmd, e=e))
                return 'empty'
            except InvalidCommandError as e:
                log.info('Could not learn {cmd}\n{e}'.format(cmd=leaf.cmd, e=e))
                return 'invalid'
        else:
            # Default cli
            try:
                ret = leaf.cmd(device=device, command=leaf.command)
                out = QDict(ret.parse(**parser_kwargs))
                if hasattr(ret, 'raw_output'):
                    out.raw_output = ret.raw_output
            except SchemaEmptyParserError as e:
                log.info('Could not learn {cmd}\n{e}'.format(cmd=leaf.cmd, e=e))
                return 'empty'
            except InvalidCommandError as e:
                log.info('Could not learn {cmd}\n{e}'.format(cmd=leaf.cmd, e=e))
                return 'invalid'
        return out

    def _send_cmd(self, leaf):
        '''Call genie.metaparser with acquired connection'''

        # Acquire connection
        with leaf.device.allocate() as conn:
            # Call the parser
            return self._call_parser(leaf, device=conn)

    def _reset(self):
        self.leafs = []
        self.outputs = {}
        for keys in self._keys:
            try:
                delattr(self.parent, keys)
            except:
                pass
        self._keys = []

    def dict_to_obj(self, conf, struct_to_map, struct=None):
        '''
            A method that converts the given dictionary into a conf object
            format.

            Args:
                self (`obj`): Maker object.
                conf (`obj`): Conf object to be filled with the passed
                              dictionary keys.
                struct_to_map (`dict`): Dictionary that has the attributes to
                                        mapped to the conf object.
                struct (`list`): List of structural attributes in the conf
                                 object.
        '''

        keys_to_loop_over = []

        # Capture the first instance of the recursive
        if struct:
            self.device = self.parent.device
            self.old_struct = struct
            conf = conf.device_attr[self.device]
            if hasattr(conf, 'devices'):
                conf.devices.append(self.device)

        # First add, current level, non structural keys to the conf object
        for key in struct_to_map.keys():
            if isinstance(struct_to_map[key], dict):
                keys_to_loop_over.append(key)
            else:
                setattr(conf,key,struct_to_map[key])

        # Loop over the current level structural keys
        for key in keys_to_loop_over:
            # Check if the key itself is a dictionary, then we need to recall
            # the function to continue building our conf object.
            if isinstance(struct_to_map[key],dict):
                # Check if the key is one of the structure keys.
                if key in self.old_struct:
                    # In case of a structural key (Ex: peer_session_attr)
                    # address
                    conf_tmp = getattr(conf, key)
                else:
                    # In case of a non-structural key, isntance of the
                    # the structural key. (Ex: PEER-SESSION)
                    conf_tmp = conf[key]

                # Call recursive to get deeper in the structure
                self.dict_to_obj(conf=conf_tmp,\
                                 struct_to_map=struct_to_map[key])

            # If key is a normal key (not a dictionary)
            else:
                setattr(conf,key,struct_to_map[key])

        return conf

    def summarize_show_commands(self):
        '''Build a summary table for the commands'''

        iterator_list = [self.summary_table['Executed Fine'],\
            self.summary_table['Not accepted'],\
            self.summary_table['Empty']]

        msg_list = ["- Parsed commands",\
                    "- Commands not accepted on the device",\
                    "- Commands with empty output"]

        # Build the summary table
        summary = Summary(title= "Commands for learning feature '{ops}'".\
            format(ops=self.parent.__class__.__name__), width=150)

        for iterator, msg in zip(iterator_list, msg_list):
            if not iterator:
                continue
            summary.add_message(msg=msg)
            summary.add_sep_line()
            for leaf in iterator:
                if leaf.kwargs:
                    summary.add_message(msg="  cmd: {cmd}, "
                                            "arguments: {cmd_key}".\
                        format(cmd=leaf.cmd, cmd_key=leaf._str_kwargs))
                else:
                    summary.add_message(msg="  cmd: {cmd}".format(
                        cmd=leaf.cmd))
            summary.add_subtitle_line()

        summary.print()

        self.reset_parameters()


class Leaf(object):
    '''Object mentioning where to take the information and where to store it'''
    def __init__(self, *, parent, cmd, device, src, dest, attributes,
                 outputs, keys=None, callables=None, action=None, command='', **kwargs):

        self.pcall_kwargs = {}
        self.cmd = cmd
        self.command = command
        self.device = device
        # Extra arguments to send to the parser
        self.kwargs = kwargs
        sorted_kwargs = '{' if kwargs.keys() else ''
        last = len(kwargs.keys())
        # Sorting kwargs before stringing to avoid relearning similar branch
        for key in sorted(kwargs.keys()):
            last -= 1
            sorted_kwargs += "'{y}':'{s}'".format(y=key, s=kwargs[key])
            sorted_kwargs += '}' if last == 0 else ','

        self._str_kwargs = sorted_kwargs if kwargs else ''

        # To store the outputs of devices associated with a parser
        self.outputs = outputs
        self._keys = keys

        assert type(src) == str, "'Leaf' 'src' needs to be a 'str'. {src} "\
                                 "is of type '{ty}'".format(src=src,
                                                            ty=type(src))
        self.dest = dest
        self.src = src
        self.parent = parent
        self._made = False

        if not callables:
            self.callables = {}
        else:
            self.callables = callables

        assert type(dest) == str, "'Leaf' 'dest' needs to be a "\
                                  "'str'. {dest} is of type "\
                                  "'{ty}'".format(dest=dest, ty=type(dest))

        # dest='[process][(?P<rip>.*)][vrf][(?P<vv>.*)]',
        self.dest = dest

        # attributes='[process][rip-1][vrf][(?P<vv>.*)]',
        self.attributes = attributes
        if action is None:
            # Return whatever was given to it
            self.action = lambda x: x
        else:
            self.action = action

    def _str_to_list(self, string):
        reg = re.findall('\(.*?\)', string)
        # Remove it from src and keep track of the position
        reg_src = {}
        reg_space = {}
        if reg:
            for reg_item in reg:
                reg_src[string.find(reg_item)] = reg_item
                string = string.replace(reg_item, ' ' * len(reg_item), 1)

        # Another corner case; if any of the variable has space into them
        # got to remove those too and add to reg_src
        reg = re.findall('[\w]+\s+[\w]+.*?]', string)
        if reg:
            for reg_item in reg:
                reg_item = reg_item.replace(']', '')
                new_item = reg_item.replace(' ', '~')
                reg_space[new_item] = reg_item
                string = string.replace(reg_item, new_item)

        string = string.replace('[', ' ').replace(']', ' ')

        # Now put it back
        if reg_src:
            for key, value in reg_src.items():
                string = string[:key] + value + string[key+len(value):]
        ret_list = string.split()

        # Now go put back the reg_space
        new_ret = deque()
        for i, item in enumerate(ret_list):
            if item in reg_space:
                item = reg_space[item]
            new_ret.append(item)
        return new_ret

    def _validate(self):
        # So many scenarios!
        # Break down self.attributes
        # Loop over each attributes
        structure = []
        use = False

        # No restriction, so use it
        if not self.attributes:
            return True

        for attr in self.attributes:

            # Split the string
            attr = self._str_to_list(attr)

            # Loop over each item
            for atts, att in zip(attr, self.dest):
                if att.startswith('{'):
                    att = att.format(self=self.parent)

                # They could be the same
                if atts == att:
                    structure.append('[{atts}]'.format(atts=atts))
                    continue

                # Regex
                if atts.startswith('('):

                    try:
                        com = re.compile(atts)
                    except Exception as e:
                        raise ValueError("'{atts}' is not a valid regex "
                                         "expression".format(atts=atts)) from e

                    if not att.startswith('('):
                        # Match it then;
                        val = com.match(att)
                        if not val:
                            break

                        if val:
                            continue
                        break

                    # This is ONLY valid if com.pattern is .*
                    elif com.pattern == '(.*)':
                        continue
                    else:
                        break

                # Last scenario, self.dest has regex, see if it matches with
                # attr
                if att.startswith('(?P'):
                    # Compile it and see if it matches with atts
                    try:
                        com = re.compile(att)
                    except Exception as e:
                        raise ValueError("'{att}' is not a valid regex "
                                         "expression".format(att=att)) from e

                    val = com.match(atts)
                    if val:
                        # Great it matches, replace it
                        # When Moving to python 3.5, can the conversion
                        index = list(self.dest).index(att)
                        self.dest[index] = atts

                        # Do the same for src
                        try:
                            index = list(self.src).index(att)
                        except ValueError as e:
                            raise ValueError("'{att}' does not exists in 'src'"
                                             " {src}"
                                             .format(att=att,
                                                     src=self.src)) from e
                        self.src[index] = atts

                        continue
                    # IF not a regex,   then it could be a callable
                    # If it is a callable,  then impossible to know if wanted or
                    # not. So take safest path and allow it.
                    reg = re.findall('\{(.*?)\}', att)
                    # As findall returns list, all good
                    if len(reg) == 1:
                        if reg[0] in self.callables:
                            continue
                    break
                else:
                    # Do not use
                    break
            else:
                # All good
                if len(attr) > len(self.dest):
                    continue

                use = True
                break

        if use:
            return ''.join(structure)
        else:
            return None

    def _normalize(self, callables):

        # Get Output
        self._made = True
        self.src = self._str_to_list(self.src)
        self.dest = self._str_to_list(self.dest)

        # Finally normalize callable
        if callables:
            # merge, but self.callables get priority
            callables.update(self.callables)
            self.callables = callables

    def _get_regex_groups(self, items):
        '''Get the regex groups for src/dest'''

        groups = set()
        for item in items:
            if item.startswith('(?P'):
                try:
                    com = re.compile(item)
                except Exception as e:
                    raise ValueError("'{item}' is not a valid regex "
                                     "expression".format(item=item)) from e

                # Get the group name
                groups.add(list(com.groupindex)[0])
        return groups

    def make(self):

        # Check which of the groups are missing in the dest
        # Find the regex/callable group in src
        src_groups = self._get_regex_groups(self.src)
        dest_groups = self._get_regex_groups(self.dest)

        # Groups in src but not in dest
        # Groups that must have only 1 branch as they were not defined in the
        # dest. If there is more than 1 branch, then it makes no sense and an
        # exception should be raised.
        # Which one of the src does not exists in dest
        self.monitor_groups = src_groups - dest_groups

        # Match Structure of src with output
        # and take in note the regex match
        ret = self._parse_single_src(self.output, src=self.src)

        # out is now the value
        # Check dest and build as we go

        # The first key is the dest name where to store it on the object
        # Take a copy

        dest = deque(self.dest)
        key = dest.popleft()

        # Now from ret; go build the structure to store in the object
        ret = self._build_dest(dest=dest, output=ret)

        # Not merged
        # If there is no key, then perfect, just create one with the right
        # value.
        try:
            value = getattr(self.parent, key)
        except:
            setattr(self.parent, key, ret)
            self._keys.append(key)
            return

        # It just got more complicated.
        # we need to merge temp_dict with whatever already exists
        # we can **only** merge dictionary, anything else, we raise an
        # exception
        if not isinstance(value, dict):
            raise ValueError("'{value}' cannot be merged as it is not a "
                             "dictionary but of type '{ty}'."
                             .format(value=value, ty=type(value)))

        if not isinstance(ret, dict):
            raise ValueError("'{ret}' cannot be merged as it is not a "
                             "dictionary but of type '{ty}'."
                             .format(ret=ret, ty=type(ret)))

        # Alright let's merge them
        try:
            value = copy.deepcopy(value)
            setattr(self.parent, key, _merge_dict(value, ret))
            self._keys.append(key)
        except Exception as e:
            raise ValueError('Cannot set {key} to the object'.format(key=key))\
                             from e

    def _build_dest(self, dest, output):

        # We are at the end (leaf), just set the value

        # Dict holding structure
        # Now loop over the rest and start building!
        ret_value = []
        # Find how many correct path there is
        if not isinstance(output, AttributesOptions):
            # This mean there is No regex
            outputs = [output]
            temp = [[]]
        else:
            # There is regex!
            # We need to first verify which one of the output are valid in
            # regards with the regex
            correct_output = output.items
            if correct_output == []:
                # No correct_output
                # Just get out with exception so nothing get set
                raise Exception("No matching output for '{dest}'"
                                .format(dest=dest))

            outputs = []
            temp = []
            for dst in dest:
                if not dst.startswith('(?'):
                    # Ignore for this step
                    continue
                try:
                    com = re.compile(dst)
                except Exception as e:
                    raise ValueError("'{item}' is not a valid regex "
                                     "expression".format(item=dst)) from e

                # Get the group name
                var = list(com.groupindex)[0]
                for out in output.items:
                    try:
                        # Until Python 3.5; then can remove list
                        index = list(out.variables).index(var)
                    except ValueError:
                        correct_output.remove(out)
                        raise ValueError("'{var}' is not in the possible group"
                                         " of choice: '{variables}'"
                                         .format(variables=out.variables,
                                                 var=var))

                    reg = re.findall('\{(.*?)\}', dst)
                    if len(reg) == 1:
                        if reg[0] in self.callables:
                            val = out.key[index]
                        else:
                            raise ValueError("'{reg}' is not defined in "
                                             "'callables' dictionary"
                                             .format(reg=reg[0]))
                    else:
                        val = com.match(str(out.key[index]))
                    if val is None:
                        # No match for this output
                        correct_output.remove(out)
                        continue

            for correct in correct_output:
                # For each valid option, add an empty list
                # We are doing that to know how many paths do we need to
                # create with the output.
                outputs.append(correct.output)
                temp.append([])

        # This is possible, as the first word of dest is removed
        # to become the variable name
        length = len(dest)
        if length == 0:
            # Limitation, can only be variable
            # If output is regex,  convert to real ouput
            if isinstance(output, AttributesOptions):
                items_output = output.items
                # It should be only 1
                if len(items_output) > 1:
                    raise InvalidDest("The output contains more than 1 branch, "
                                      "but no regex was provided in the dest")
                output = output.items[0].output
            return self.action(output)

        # We've found the correct outputs, now to create the path + add output
        for i, item in enumerate(dest):
            # Regex
            if item.startswith('(?'):
                # Now go check the possible values in there

                try:
                    com = re.compile(item)
                except Exception as e:
                    raise Exception("'{item}' is not a valid regex "
                                    "expression".format(item=item)) from e

                # Get the group name
                var = list(com.groupindex)[0]
                for option, temp_item, out in zip(correct_output, temp,
                                                  outputs):
                    # Until Python 3.5; then can remove list
                    index = list(option.variables).index(var)
                    value = option.key[index]

                    if i == length-1:
                        # Last element, so add the output now
                        # Special case
                        if option.output == '__remove__':
                            value = self.action(value)
                            ret_value.append(_list_to_dict([temp_item], value,
                                                           self.cmd))
                        else:
                            temp_item.append(value)
                            output = self.action(option.output)
                            ret_value.append(_list_to_dict([temp_item],
                                                           output, self.cmd))
                    else:
                        # Not at the last element, keep building the structure
                        temp_item.append(value)

            # Attribute Substitution
            elif item.startswith('{'):
                value = item.format(self=self.parent)
                for temp_item, out in zip(temp, outputs):
                    if i == length-1:
                        # Last element, so add the output now
                        temp_item.append(value)
                        out = self.action(out)
                        ret_value.append(_list_to_dict([temp_item], out,
                                                       self.cmd))
                    else:
                        # Not at the last element, keep building the structure
                        temp_item.append(value)

            # Just a normal value
            else:
                for temp_item, out in zip(temp, outputs):
                    if i == length-1:
                        # Last element, so add the output now
                        temp_item.append(item)
                        out = self.action(out)
                        ret_value.append(_list_to_dict([temp_item], out,
                                                       self.cmd))
                    else:
                        # Not at the last element, keep building the structure
                        temp_item.append(item)

        # Now let's merge those dicts before returning them
        merged = {}
        for ret in ret_value:
            try:
                ret = copy.deepcopy(ret)
            except Exception as e:
                pass

            merged = _merge_dict(ret, merged)
        return merged

    def _parse_single_src(self, output, src, option=None):

        # Its possible src is empty, then just return output
        # Will be possible because of recursive call
        if src == []:
            return output
        src_temp = deque(src)
        length = len(src)
        for item in src:
            src_temp.popleft()
            # make sure item match with the structure of output

            # Regex
            if item.startswith('('):
                # Alright, now we need to branch out
                # Parse each key into a new dictionary, store the value
                output = self._parse_multi_src(item, output, option=option,
                                               src=src_temp)
                break

            # Attribute Substitution
            # {self.instance_id}
            elif item.startswith('{'):
                if 'self.' not in item:
                    raise TypeError("Attribute substitution is only possible "
                                    "for 'self' object, not for '{item}' "
                                    "object".format(item=item))
                value = item.format(self=self.parent)
                try:
                    output = output[value]
                except:
                    raise KeyError('{value} is not a valid key for {out}'
                                   .format(value=value, out=output))
            # Just a normal value
            # [vrf]
            else:
                try:
                    output = output[item]
                except:
                    # Dead end
                    raise NameError("Cannot find '{item}' in '{out}'".
                                    format(item=item, out=output))

        # Return result
        return output

    def _parse_multi_src(self, item, output, src, option):
        # There was a regex,  and got here to handle it

        # [(?P<rip>.*)]
        # Compile it first to get the name of that variable
        # Verify if it is a match, or a sub

        # Keep track of the number of path found
        amount = 0

        try:
            com = re.compile(item)
        except Exception as e:
            raise Exception('{item} is not a valid regex '
                            'expression'.format(item=item)) from e
        var = list(com.groupindex)[0]

        if not option:
            # Root of the tree
            option = AttributesOptions()
        else:
            option.var.append()

        try:
            iterable = output.items()
        except:
            # just a value
            ret = self._parse_single_src(output, src)
            option.create_branch(var=var, key=ret)
            option.items[-1].output = '__remove__'
            return option

        reg = re.findall('\{(.*?)\}', item)
        for key, value in iterable:
            # rip-1
            if len(reg) == 1:
                # Callable
                if reg[0] in self.callables:
                    val = self.callables[reg[0]](key)
                else:
                    raise ValueError("'{reg}' is not defined in 'callables' "
                                     "dictionary".format(reg=reg[0]))
            else:
                val = com.match(str(key))
                if val is not None:
                    val = key

            if val is None:
                # Key is not matching, so ignore this branch
                continue

            # Alright key is a valid output for var
            # Need a new branch
            # Check the future now
            try:
                ret = self._parse_single_src(value, src)
            except ValueError:
                raise
            except Exception as e:
                # This value is not accetable!\
                continue

            if isinstance(ret, AttributesOptions):
                for item in ret.items:
                    # Add var + key
                    item.variables.appendleft(var)
                    item.key.appendleft(val)
                    option.items.append(item)
            else:
                # Ah output!
                option.create_branch(var=var, key=val)
                option.items[-1].output = ret
                amount += 1

        if var in self.monitor_groups and amount > 1 and\
           len(option.items) > 1:
            raise InvalidDest("'{var}' was not provided in 'dest' but was "
                              "provided in 'src'. This is only valid if "
                              "'{var}' only returned one branch of value, "
                              "but it has {n} "
                              "branches".format(var=var, n=len(option.items)))
        return option


class AttributesOptions(object):
    def __init__(self):
        self.items = []

    def create_branch(self, var, key):
        self.items.append(AttributeOption(var, key))


class AttributeOption(object):
    def __init__(self, var, key):
        self.variables = deque([var])
        self.key = deque([key])
        self.output = None
