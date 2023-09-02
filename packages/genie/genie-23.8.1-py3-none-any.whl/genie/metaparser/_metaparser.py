"""metaparser - the infrastructure class to define and regulate parser object
execution.

"""

import os
import logging
import pprint

# Unicon
import unicon

try:
    from pyats import tcl
except Exception:
    pass

from pyats.log.utils import banner
from pyats.datastructures.listdict import ListDict

from .util.schemaengine import Schema, Path, Any
from .util import merge_dict
from .util.traceabledict import TraceableDict
from .util.exceptions import SchemaEmptyParserError, SchemaMissingKeyError, \
                             ParseSelectedKeysException, InvalidCommandError,\
                             SchemaUnsupportedKeyError

logger = logging.getLogger(__name__)


class classproperty(property):
    """ decorator class to access the class property
    """
    def __get__(self, obj, type_):
        return self.fget.__get__(None, type_)()


class MetaParser(object):
    """Base parser class for all Genie parser classes

    All parser classes will inherit from MetaParser class, for example:
    `ShowVersion`, etc.

    Args:
        device (`Device`): device which the parser function will be applied to
        context (`str`): a keyword only arg acting as a selector for user to
                         choose which parsing mechanism will be used to current
                         parsing task.
                         choices of: 'cl', 'xml', 'yang', default is 'cli'.
        kwargs (`dict`) : gives the user ability to assign extra attributes
                          while creating the parser object.
    Returns:
            a `metaparser` object

    Examples:
        >>> from xbu_shared.parser.nxos.show_version import ShowVersion
        >>> p = ShowVersion()

        <parser.nxos.show_version.ShowVersion object at 0xf6e0ec6c>

    Class variables:

        schema (`dict`): defines the common data structure among all types of
                         device output (cli, xml, yang) current metaparser
                         supports.
        key_traceable('bool'): enable the parser output key usage tracing
                               functionality, default value is 'False'
        CONTEXT_LIST (`tuple`): static variable defines valid contexts

        DEFAULT_CONTEXT (`str`):  constant variable with value 'cli'


    """

    # *************************
    # schema - class variable
    #
    # Default value is `None`, allows subclass parser objects to overwrite:
    # Typical scenario is:
    # the first user who defines the first parsing mechanism (e.g.: cli ()) in
    # parser class will also define the schema for the output structure.
    # At the end of the parsing process, parser engine (MetaParser) will do
    # schema checking to make sure the parser always return the output
    # (nested dict) that has the same data structure across all supported
    # parsing mechanisms (cli(), yang(), xml()).
    #
    # Example of schema (show version) - nested dict
    #    schema = {'cmp': {
    #                    'module': {
    #                             Any(): {
    #                                     'bios_compile_time': str,
    #                                     'bios_version': str,
    #                                     'image_compile_time': str,
    #                                     'image_version': str,
    #                                     'status': str},}},
    #              'hardware': {
    #                    'bootflash': str,
    #                    'chassis': str,
    #                    'cpu': str,
    #                    'device_name': str,
    #                    'memory': str,
    #                    'model': str,
    #                    'processor_board_id': str,
    #                    'slots': str,
    #                    Any(): Any(),},}
    #
    # Here Any() in schema acting like a wildcard character, usually used to
    # presenting the variable keys within the dictionary. To use Any obj:
    # from genie.metaparser.util.schemaengine import Any

    schema = None
    command = None

    # To enable/disable the key usage traceability of metaparser
    key_traceable = False

    CONTEXT_LIST = ('cli', 'xml', 'yang', 'rest')
    DEFAULT_CONTEXT = 'cli'

    def __init__(self, device, *, context=DEFAULT_CONTEXT, **kwargs):
        """class initialization - set attributes for the parser object
        according to user's input.

        parsed_output (`dicts`): holds the raw output before the filtering
        """

        if isinstance(context, str):
            context = [context]

        self.device = device
        unduplicated_context_list = []

        for contxt in context:
            # Check for the context list duplicates before calling the schema
            # engine.
            if contxt not in unduplicated_context_list:
                unduplicated_context_list.append(contxt)
            assert contxt in self.CONTEXT_LIST, \
                'unknown context {context} supplied in parser'.\
                format(context=contxt)

        self.context = unduplicated_context_list

        # For each kwargs, set it to its value
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.parsed_output = None

    def call_parser(self, context):
        """
           This function returns the object context and raise
           an attribute error if not found.
        """
        try:
            return getattr(self, context)
        except AttributeError as e:
            raise AttributeError("'{context}' has not been "
                                 "defined in class '{cls}'."
                                 "Make sure the parser object has correct "
                                 "context method associate with."
                                 .format(context=context,
                                         cls=type(self).__name__)) from None

    def parse_selected_keys(self, selected_keys, output, **kwargs):
        """
           This function retrieves the corresponding selected_keys
           portion of the parsed output.
        """
        # filtering desired keys
        new_list_dict = ListDict()
        output_list_dict = ListDict(output)
        for key in selected_keys:
            key_matched = False
            key_path = Path(key)
            for path, value in output_list_dict:
                if key_path == Path(path):
                    new_list_dict.append((path, value))
                    key_matched = True
            if not key_matched:
                self.key_unmatched = key
                # Raise that specific exception to check later if there is any
                # further attempt with another context.
                raise ParseSelectedKeysException

        return new_list_dict.reconstruct()

    def parse(self, *, selected_keys=None, context=None, ignore_update=True,
              warn_unsupported_keys=None, **kwargs):
        """public method for users to call to execute a parser

        API runs correct parsing methods according to the 'context' user
        specific in the constructor.

        Procedure of parse function:

        1.Select specific parsing mechanism (cli(), xml(), yang()) based on
        'context' input. Each parsing mechanism defined in subclass parser
        object should include 3 steps:
        - Get the output from the device
        - Run existing parser or self implemented parser with the output
        - Transform the output into 'schema' compatible dictionary
        and return. Detail steps to implement parsing mechanism please
        read template.py within the package.

        2.Schema checking - metaparser will do schema checking to make sure the
        parsing mechanism returns correct data structure.

        3.Apply user defined filter on output, only selected key-value pairs
        will be returned as the original format from the output.

        Args:
            selected_keys (`list`): keyword-only arg, a filtering mechanism
                                    which allows user to select desired keys
                                    (nested keys) from the raw parser output
                                    and reform a new dict containing only those
                                    selected key-value pairs.

                                    selected_keys can be a list of list or a
                                    list of tuple which contains flattened
                                    nested keys from the output dictionary.
                                    Python regular expression pattern can be
                                    used to define matching key format.

                                    For example: selected_keys =
                                      [['a', 'b'], [r'.*', 'c'], [r'^d', r'.*']]

                                    Here 'r' in front of the key string
                                    indicates the 'raw string literal' used as
                                    the Python regexp pattern.

            warn_unsupported_keys (bool): Log warning instead of raising an
                                          exception when unsupported keys
                                          are found.

            kwarg (dict)s: gives the user ability to pass extra parameters.

        Return:
            a nested `dict` obj

        Example:
            >>> parser = ShowVersion(device=uut, context='xml')

            get the entire output

            >>> output = parser.parse()

            get the output only contains specific keys selected by users

            >>> selected_keys = [['hardware', 'bootflash'],
                                 [r'.*', 'kickstart'],
                                 ['reason'],
                                 [r'^kernel', r'.*']]

            >>> output = parser.parse(selected_keys = selected_keys)

            >>> {'hardware':      {'bootflash': '2048256'},
                 'kernel_uptime': {'days': '113',
                                   'hours': '2',
                                   'minutes': '42',
                                   'seconds': '5'},
                 'reason':       'Unknown',
                 'software':     {'kickstart': 'version 6.2(6)',
                                  'kickstart_compile_time': '12/5/2013',
                    'kickstart_image_file': 'bootflash:///kickstart.6.2.bin'}}
        """
        if warn_unsupported_keys is None:
            warn_unsupported_keys = os.environ.get(
                'GENIEPARSER_WARN_UNSUPPORTED_KEYS') in ['True', 'true', '1']

        keys = None
        missing_keys_list = []

        record_raw_data = kwargs.pop('raw_data', False)
        if record_raw_data:
            self.raw_output = []
            if self.device.connected:
                # store the raw output of device.execute calls
                def execute_wrapper(func):
                    def wrapper(*args, **kwargs):
                        output = func(*args, **kwargs)
                        self.raw_output.append({
                            'command': ' '.join(args),
                            'kwargs': kwargs,
                            'output': output
                        })
                        return output
                    return wrapper

                self.device.execute = execute_wrapper(self.device.execute)
            else:
                # if device is disconnected, return the output provided
                self.raw_output = [{
                    'command': self.cli_command,
                    'kwargs': {
                        k: v for k, v in kwargs.items()
                        if k != 'output'
                    },
                    'output': kwargs.get('output')
                }]

        for indx, contxt in enumerate(self.context):
            call = self.call_parser(contxt)
            # Check if it is the first context. If a previous context has been
            # already run, we will only return the merge between the outputs.
            if indx == 0:
                try:
                    output = call(**kwargs)
                except unicon.core.errors.SubCommandFailure as e:
                    # Capture the error and propagate it to the maker in ops.
                    raise InvalidCommandError from e
            else:
                old_output = output
                new_output = call(**kwargs)
                output = merge_dict(old_output, new_output,
                                    ignore_update=ignore_update)
            self.parsed_output = output

            # check for schema
            if self.schema:
                try:
                    output = Schema(self.schema).validate(
                        output, command=self.command,
                        warn_unsupported_keys=warn_unsupported_keys)
                    # save this value before any manipulation
                    self.parsed_output = output
                    self.schema_validated = True
                except (SchemaEmptyParserError, SchemaUnsupportedKeyError):
                    raise
                except SchemaMissingKeyError as e:
                    # collecting the missing keys
                    e.parser = self
                    if e.path not in missing_keys_list:
                        missing_keys_list.append(e.path)
                    # As the previous parser call didnt satisfy all the keys,
                    # calling the fallback type
                    if contxt is not self.context[-1]:
                        logger.info("Context '%s' did not satisfy all the "
                                    "schema keys checking now with '%s'"
                                    %(contxt, self.context[indx+1]))
                    else:
                        raise
                    continue
                except Exception as e:
                    raise Exception("Parser {cls} schema checking failed".format(
                                    cls=type(self).__name__)) from e

            # filtering desired keys
            # selected_keys passed by the user
            if selected_keys:
                keys = selected_keys
            # missing_keys_list are the keys missing from the schema
            elif missing_keys_list:
                keys = missing_keys_list

            if keys:
                try:
                    output = self.parse_selected_keys(keys,
                                                      output, **kwargs)
                except ParseSelectedKeysException:
                    # Some passed keys didn't match during parse_selected_keys
                    # function call. Check if another parse call to be tried
                    # or just raise the KeyError exception.
                    self.schema_not_validated = not self.schema_validated
                    if self.schema_not_validated & \
                        indx == self.context.index(self.context[-1]):
                        raise KeyError("The selected key '{key}' is not found "
                               "in parser output, key selection failed".
                               format(key=self.key_unmatched))
                    else:
                        pass

            # Check for the parser output type (should be of type dictionary)
            if self.parsed_output and not isinstance(self.parsed_output, dict):
                raise TypeError("Output of parser '%s'.'%s' is of type '%s' "
                                "while the parser output should be a 'dict'."
                                % (self, contxt, type(self.parsed_output)))

            # adding traceable functionality
            if MetaParser.key_traceable:
                # adding key tracing ability to parser obj
                traced_dict_name = self.__module__ + '.' + self.__class__.__name__
                if traced_dict_name not in TraceableDict.tracer:
                        TraceableDict.tracer[traced_dict_name] = set()
                traced_dict = TraceableDict.convert(output, traced_dict_name)
                return traced_dict
            else:
                return output

    @classproperty
    @classmethod
    def tracer(cls):
        """ class level property

        This allows the MetaParser to access the global tracer information

        Example:
            >>> import pprint
            >>> pprint.pprint(MetaParser.tracer)
        """
        return TraceableDict.tracer

def tclparser(pkgrequire):
    def evaluation(function):
        if hasattr(tclparser, 'ran'):
            return
        tclparser.ran=True
        try:
            path  = os.environ['XBU_SHARED']
        except:
            # then use existing Tcl tree location
            try:
                tcl_loc = os.environ['AUTOTEST']
            except:
                raise KeyError("'AUTOTEST' and 'XBU_SHARED'\
                               are not defined under user environ")

            path = os.path.join(tcl_loc, 'xBU-shared')
            if not os.path.isdir(path):
                raise ValueError("{path} is not an accessible path".
                                  format(path=path))

        if path not in tcl.eval('set auto_path'):
            tcl.eval('lappend ::auto_path {0}'.format(path))
            tcl.eval(pkgrequire)
        return function
    return evaluation


def enable_key_usage_trace(section):
    """ method to enable the global traceability of parser output key usage

    This module method designed to be used as a pyats pre-processor
    """
    MetaParser.key_traceable = True

def log_key_usage_trace(section):
    """ method to log overall parser output key usage

    This module method designed to be used as a pyats post-processor
    """
    logger.info(banner('Metaparser Key Usage'))

    record = pprint.pformat(MetaParser.tracer)
    logger.info(record)
