# Python
import logging, string, re, sys

# tcl, for device OS retrieve
try:
    from pyats import tcl
except:
    # Carry on as ats doesn't have tcl package
    pass

# core
from genie.parsergen import core

ext_dictio = core.ext_dictio
_glb_regex = core._glb_regex
_glb_show_commands = core._glb_show_commands
_glb_regex_tags = core._glb_regex_tags

# Predcore
from genie.predcore import Predicate

core.supported_oses = [ 'ios', 'iosxr', 'iosxe', 'nxos', 'calvados', 'iox',
                              'pix', 'asa', 'sanos', 'dcos', 'aireos', 'linux' ]

supported_oses = core.supported_oses

python3 = sys.version_info >= (3,0)

logger = logging.getLogger(__name__)

def get_os_type(device, alias = None):
    '''Get the OS of the given router'''
    conn = eval("device.{alias}".format(alias=alias)) if alias else device

    try:
        if device.is_connected(alias=alias):
            if hasattr(device, 'os'):
                return device.os
            elif hasattr(conn, 'handle'):
                try:
                    return tcl.eval('{} get_os_type'.format(conn.handle)).lower()
                except:
                    raise Exception("'%s' doesn't have 'os'" %device)
            else:
                return "unknown"
        else:
            return "unknown"
    except TypeError:
        # When passed device is a connection object
        if not hasattr(device, 'name'):
            device.name = device.hostname
        if device.is_connected:
            if hasattr(device, 'os'):
                return device.os
            elif hasattr(conn, 'handle'):
                try:
                    return tcl.eval('{} get_os_type'.format(conn.handle)).lower()
                except:
                    raise Exception("'%s' doesn't have 'os'" %device)
            else:
                return "unknown"
        else:
            return "unknown"

##############################################################################
#                             NON-TABULAR PARSER                             #
##############################################################################


def extend_markup (marked_up_input):
    ''' Allows an external module to extend :mod:`parsergen`'s
    dictionary of `regular expressions<re>` , `regex<re>` tags and known show
    commands by specifying marked-up show command text
    (see :ref:`core_markup`)

    This input text is transformed, and then automatically passed to
    `~parsergen.extend`.

    Parameters
    ----------
    marked_up_input : `str`
        Marked-up show command input
    '''
    core.extend_markup(marked_up_input)

def extend (regex_ext=None, show_cmds = None, regex_tags = None):
    ''' Allows an external module to extend :mod:`parsergen`'s
    `dictionary<dict>` of `regular expressions<re>`, known show commands and
    `regex<re>` tags.

    :mod:`parsergen` keeps its master `regular expression<re>`
    `dictionary<dict>`  in the member ``parsergen._glb_regex``, its master
    show command `dictionary<dict>` in the member
    ``parsergen._glb_show_commands`` and its master regex tag
    `dictionary<dict>` in the member ``parsergen._glb_regex_tags``.

    It is possible to register CLI show commands without specifying any
    regular expressions, since `~parsergen.oper_fill_tabular` also uses this
    CLI tag/command repository to format its CLI commands.

    Parameters
    ----------
    regex_ext : A `dict` of `dictionaries<dict>` of `regular expressions <re>`\
        keyed by  OS type and regex tag
        A series of tags (keys) and their corresponding `regexes<re>` (values).
        Any `regex<re>` in this dictionary may also be expressed as a `list`
        (this feature allows the same regex tag to match multiple patterns,
        and is intended on enabling parsers to work correctly across
        multiple releases across which CLI text may have changed).

    show_cmds :  A `dict` of  `dictionaries<dict>` of  `str` keyed by  \
        OS type and generic CLI command tag
        A series of generic CLI command tags (keys) and their corresponding
        CLI command equivalents (values). The values may contain string
        formatting characters, including equal signs, as documented in
        :ref:`how-to-specify-show-commands`.

    regex_tags : A `dict` of `lists<list>` of regex tags keyed by  OS type
        A series of tags (keys).  This allows :mod:`parsergen` to
        store the original order order the tags were declared.  This
        parameter must be specified in order to make use of the
        `regex_tag_fill_pattern` parameter of `~parsergen.oper_fill` and
        in order to enable the auto-attrvalpair-reordering feature offered
        by `~parsergen.oper_check`.

    '''
    core.extend(regex_ext, show_cmds, regex_tags)

# http://stackoverflow.com/questions/11301138/\
# how-to-check-if-variable-is-string-with-python-2-and-3-compatibility
try:
    basestring  # attempt to evaluate basestring
    def isstr(s):
        return isinstance(s, basestring)
except NameError:
    def isstr(s):
        return isinstance(s, str)

class CmdCache():
    ''' This class holds the CLI command cache and associated cache update
        logic.
    '''
    cache = {}
    ''' CACHE OF LAST SHOW COMMAND
    This dictionary contains the last received show command, indexed by
    device name.  It contains the last received show command output from
    the device.
    It's used to allow parsing when the refresh_cache flag is set to False.
    '''

    def refresh_cache(self, obj, show_command):
        ''' Refresh the cache

        Parameters
        ---------

        obj : `parsergen.oper_check` or `parsergen.oper_fill_tabular` object
            Object that is asking for a cache refresh.

        show_command : `str` or `tuple`
            The show command to execute.
        '''
        show_cmd = core._get_show_command( obj._device_os,  show_command)

        if not obj._device_conn_alias:
            core.text_to_parse[obj._device.name] = \
                obj._device.execute(show_cmd)
        else:
            core.text_to_parse[obj._device.name] = \
                eval("obj._device.{alias}.execute(show_cmd)".\
                format(alias=obj._device_conn_alias))

        obj._refresh_cache = obj._refresh_cache_init

        self.cache[obj._device.name] = \
            core.text_to_parse[obj._device.name]

showCmdCache = CmdCache()
'''
This object holds the cache of previously executed show commands.
'''

class oper_check(Predicate):
    ''' Optionally run a show command on a device, parse user-requested
        fields, and compare these fields against expected values.
    '''

    def __init__(self, device = None, show_command = None, attrvalpairs = None,
                       refresh_cache = False, negate = False,
                       device_conn_alias = None, device_output = None,
                       device_os = None):
        """
            Create an object to parse and check CLI command output.

            Parameters
            ----------

            device : `Device()`
                The device to run the show command on.

            show_command : `str` or `tuple` of \
                (`str`, `list` of positional formatting args, \
                `dict` of keyword formatting args)
                The key into the show command dictionary previously passed to
                `~parsergen.extend` or the actual show command to issue.
                If the corresponding show command dictionary string contains
                formatting fields, specify these arguments using a `tuple`.
                Remember to use ``None`` as a placeholder if you are combining
                default and non-default fields(see
                :ref:`how-to-specify-show-commands`).

            attrvalpairs :  `list` of `tuples<tuple>` (`str`, `str` or `tuple`)
                An ordered list of (attribute/value) pairs.
                Parsergen must have been taught the relationship between
                attributes and regular expressions, which is done via the
                `~parsergen.extend` API.
                If a value is expressed as a `tuple`, then each member of
                the tuple is considered as a potential match.
                These pairs are reordered on behalf of the user if all
                attributes are present in ``parsergen._glb_regex_tag``
                (which is automatically populated via
                `~parsergen.extend_markup` and optionally populated via
                `~parsergen.extend`).

            refresh_cache : `bool`
                If ``True``, refresh the cache by running the indicated show
                command on the device, and then parse this output.
                If ``False``, parse the previously cached show command
                output for this device.  Defaults to ``True``.

            negate : `bool`
                If ``True``, negate the result (ie. treat a failure like a
                success).  Defaults to ``False``.

            device_conn_alias : `str`
                If specified, assume the device was connected to under the
                indicated alias.
                Otherwise, the default alias is assumed.
                For details, please see
                http://wwwin-pyats.cisco.com/documentation/latest/connections/manager.html#connection-manager

        """
        if attrvalpairs is None:
            raise TypeError("'%s' missing 1 required positional argument: "
                            "'attrvalpairs'" %self)

        self.raw_cli = device_output
        self._errors = []
        self._show_command = show_command
        self._refresh_cache = refresh_cache
        self._refresh_cache_init = refresh_cache
        if device:
            self._device = device
            self._device_conn_alias = device_conn_alias
            self._device_os = get_os_type(device=self._device,
                                          alias=self._device_conn_alias)
        elif self.raw_cli:
            # parsergen.ext_dictio['device_name'] needs a device name to
            # access the parsed dictionary. In case of no real device passed to
            # parsergen, 'device_name' will be used as the ext_dictio handler.
            device = Device('device_name')
            self._device = device
            self._device_conn_alias = 'any'
            self._device_os = device_os
        else:
            raise AttributeError("Neither 'device' nor 'device_output' "
                                 "has been passed when calling '%s'" %self)

        self._fill = False

        #
        # NOTE: _skip is set to False because no use cases for this feature
        #       are forseen when running the parser in "compare" mode
        #       (as opposed to "fill" mode).
        #
        self._skip = False
        self._negate = negate
        self.process_attrvalpairs(attrvalpairs, self._device_os)

    def process_attrvalpairs(self, attrvalpairs, os, reorder=True):
        ''' Process a list of tuples of attr/value pairs into a form
            that parsercare can use.
        '''
        #
        # First, check if every attribute the user is requesting is
        # present in the optional parsergen.core global regex tag list.
        # If all are present, then it is possible to double-check the
        # order of the user's provided (key,value) pairs and even re-order
        # the pairs if required.  parsergen.core can fail if the (key, value)
        # pair order does not match the order originally passed to the
        # extend API.
        #
        reordered_attrvalpairs = []
        if reorder:
            if _glb_regex_tags:
                for pc_regex_tag in _glb_regex_tags[os]:
                    for avp in attrvalpairs:
                        if pc_regex_tag == avp[0]:
                            reordered_attrvalpairs.append(avp)

        # Only reorder the user's pairs if all attrs were found in
        # parsergen.core's master regexp tag list.  If any were not found,
        # then we don't have enough information to reorder the pairs.
        if len(reordered_attrvalpairs) == len(attrvalpairs):
            attrvalpairs = reordered_attrvalpairs

        if (attrvalpairs and (type(attrvalpairs[0]) is tuple)):
            (attributes, values) = \
                zip(*[(item[0], item[1]) for item in attrvalpairs])
            self._attributes = list(attributes)
            self._values     = list(values)

            self._values_debug = self._values
        else:
            self.error("attrvalpairs is invalid {}".\
                format(attrvalpairs))




    def result(self, result):
        if self._negate:
            return not result
        else:
            return result

    def parse(self):
        ''' Perform the parsing and retrieve results.

        Returns
        -------
        `bool`
            Returns ``True`` if the parsing was successful.
            The values passed in as ``None`` will be filled in
            ``parsergen.ext_dictio[device_name]``.
            Returns ``False`` if the parsing failed.  The user may
            obtain a failure analysis by calling :class:`python:str` on the
            parsing object.
        '''


        # clean errors
        self._errors = []

        # preliminary checks on attributes
        for attr in self._attributes :
            regitem = core._get_regex(self._device_os, attr)
            if not regitem:
                logger.warning(\
                    'No regular expression defined for attribute %s' % attr)
                return False

        if self.raw_cli:
            core.text_to_parse[self._device.name] = self.raw_cli
        else:
            # check if cache has to be refreshed
            if self._refresh_cache :
                showCmdCache.refresh_cache(self, self._show_command)
            elif self._device.name not in showCmdCache.cache.keys():
                logger.warning(\
                  ('refresh_cache = False but no output found for %s ' + \
                  '=> collect output') \
                        %self._device.name)
                showCmdCache.refresh_cache(self, self._show_command)
            else:
                core.text_to_parse[self._device.name] = \
                    showCmdCache.cache[self._device.name]

        parser = core._parser_gen_t(\
                     self._device_os, \
                     self._attributes, self._values, \
                     self._fill,  self._device.name, self._skip)
        (validate, dictio, msg) = parser._parser_validate()
        if validate : return self.result(True)

        # log the error from _parser_validate
        self.error(msg)
        self.error("Node: %s, Show command: %s" \
                    % (self._device.name, self._show_command))

        # the sequence was not validated, print useful log information
        self._refresh_cache = True
        for idx, attr in enumerate(self._attributes) :
            if attr not in dictio.keys():
                self.error(\
                    ("Attribute %s not found in the show command " + \
                    "(or parsergen stopped before at an error)") \
                        % attr)
            elif dictio[attr] != True :
                self.error("Attribute %s has value '%s' (expected '%s')" %
                           (attr, dictio[attr]["value"], self._values[idx]), \
                           line=dictio[attr]["line"])
        return self.result(False)

    def error(self, msg, line=sys.maxsize):
        self._errors.append([line,msg])
        self._errors.sort(key=lambda x : x[0])


    def __str__(self):
        attrList = "Parsergen attributes : "

        for i in range(len(self._attributes)):
            attrList = attrList + ("%s : %s - " % \
                    (self._attributes[i], self._values_debug[i]))

        if self._errors:
            attrList = attrList + "\n\n: Diagnosis : \n" + "\n".\
                    join(map(lambda x : x[1], self._errors))
            if core.text_to_parse[self._device.name] is not None and \
               self._refresh_cache == True:
                attrList = attrList + "\n"
                for lineno, line in  enumerate(\
                        core.text_to_parse[self._device.name].\
                        split("\n")):
                    for error in self._errors:
                        if error[0] == lineno:
                            line = line.ljust(80) + "<=== %s" % error[1]
                            break
                    attrList += line + "\n"

        return attrList

    def test(self):
        return self.parse()

    def dump(self):
        return str(self)

class oper_fill (oper_check):
    ''' Optionally run a show command on a device and parse user-requested
        fields.
    '''
    def __init__(self, device = None, show_command = None, attrvalpairs = None,
        refresh_cache = False, regex_tag_fill_pattern='', skip = False,
        device_conn_alias = None, device_output = None, device_os = None):
        """
            Create an object to parse CLI command output.

            Parameters
            ----------

            device : `Device()`
                The device to run the show command on.

            show_command : `str` or `tuple` of \
                (`str`, `list` of positional formatting args, \
                `dict` of keyword formatting args)
                The key into the show command dictionary previously passed to
                `extend` or the actual show command to issue.
                If the corresponding show command dictionary string contains
                formatting fields, specify these arguments using a `tuple`.
                Remember to use ``None`` as a placeholder if you are combining
                default and non-default fields(see
                :ref:`how-to-specify-show-commands`).

            attrvalpairs :  `list` of `tuples<tuple>` (`str`, `str` or `tuple`)
                An ordered list of attribute/value pairs.  A value of `None`
                requests a fill for that attribute.
                The very first value cannot be `None`.
                Parsergen must have been taught the relationship between
                attributes and regular expressions, which is done via the
                `~parsergen.extend` API.
                If a value is expressed as a `tuple`, then each member of
                the tuple is considered as a potential match.

            refresh_cache : `bool`
                If ``True``, refresh the cache by running the indicated show
                command on the device, and then parse this output.
                If ``False``, parse the previously cached show command
                output for this device.  Defaults to ``True``.

            regex_tag_fill_pattern : `regular expression<re>`
                Regular expression to use to select a group of regex tags
                to fill.  The tags will be added to the attrvalpairs list
                as (tag, None) in the same order as found in
                ``parsergen._glb_regex_tag`` (which is automatically
                populated via `~parsergen.extend_markup` and optionally
                populated via `~parsergen.extend`).

            skip : `bool`
                Whether or not to ignore unmatched attributes (regex tags).
                If ``True``, then ignore any attributes (regex tags) whose
                associated `regexes<re>` do not match the text to parse.
                One reason to specify this option could be when the text to
                parse could contain optional content lines.
                Defaults to ``False``.

            device_conn_alias : `str`
                If specified, assume the device was connected to under the
                indicated alias.
                Otherwise, the default alias is assumed.
                For details, please see
                http://wwwin-pyats.cisco.com/documentation/latest/connections/manager.html#connection-manager



            .. warning:: If you specify a non-`None`
                ``regex_tag_fill_pattern`` then ensure none of your
                (attr, value) pairs have a value of ``None``,
                otherwise parser failure can result.

            Example use to obtain interface state values::

                parsergen.oper_fill(R1, 'show interfaces',
                            [ ('im.intf-name',       'GigabitEthernet0/0/0/1'),
                              ('im.intf-status',      None),
                              ('im.intf-line-status', None),
                              ('im.intf-mtu',         None),
                              ('im.intf-bw',          None),
                              ('im.intf-arptype',     None)
                            ],
                            refresh_cache=True)


            The values passed in as ``None`` will be filled in
            ``parsergen.ext_dictio[device_name]``.

            Note that, in case of output with multiple entries, eg datalist,
            `~parsergen.oper_fill` needs a hook in the code in order to target
            the desired values.  For instance, in the above example, it's
            using the name of the interfaces to hook into that section of the
            output.

            This class may not be the best choice to parse tabular data.

            .. note:: Please consider using the
              `~parsergen.oper_fill_tabular` class for parsing
              tabular results as it is generally far easier.  For output that
              contains both tabular and non-tabular data, it is also possible
              to use both mechanisms to parse different parts of the output.

            Example of accessing the filled in values::

               >>> parsergen.ext_dictio[R1.name]['im.intf-line-status'] # doctest: +SKIP
               'Up'
               >>> parsergen.ext_dictio[R1.name]['im.intf-mtu']         # doctest: +SKIP
               '1500'
        """
        if attrvalpairs is None:
            raise TypeError("'%s' missing 1 required positional argument: "
                            "'attrvalpairs'" % self)

        self.raw_cli = device_output
        self._errors = []
        self._show_command = show_command
        self._refresh_cache = refresh_cache
        self._refresh_cache_init = refresh_cache
        if device:
            self._device             = device
            self._device_conn_alias  = device_conn_alias
            self._device_os          = get_os_type(
                device=self._device, alias=self._device_conn_alias)
        elif self.raw_cli:
            device = Device('device_name')
            self._device = device
            self._device_conn_alias = 'any'
            self._device_os = device_os
        else:
            raise AttributeError("Neither 'device' nor 'device_output' "
                                 "has been passed when calling '%s'" %self)
        self._fill = True
        self._skip = skip
        self._negate = False
        if regex_tag_fill_pattern:
            user_attrs = []
            for valpair in attrvalpairs:
                user_attrs.append(valpair[0])
            addedValPairs = [(tag, None) \
                for tag in _glb_regex_tags[self._device_os] \
                if re.match('.*'+regex_tag_fill_pattern, tag)]
            for valpair in addedValPairs :
                # Don't insert a (attr, val) pair already specified by the user
                # NOTE : If the user specifies (attr, val) pairs with val=None
                #        and also specifies a non-None regex_tag_fill_pattern
                #        then the user risks parser breakage, because
                #        to ensure real-time efficiency, the pairs are not
                #        reordered.
                if valpair[0] not in user_attrs:
                    attrvalpairs.append(valpair)

            # Don't reorder because this would just duplicate effort - we
            # just ensured the attr/val pairs matching the pattern are
            # already ordered.
            self.process_attrvalpairs(
                attrvalpairs, self._device_os, reorder=False)
        else:
            # User is specifying a hand-picked set of keys to parse, but
            # they may not be in the same order as given in the markup,
            # so reorder now to prevent core parser failure.
            self.process_attrvalpairs(
                attrvalpairs, self._device_os, reorder=True)



##############################################################################
#                                TABULAR PARSER                              #
##############################################################################
class oper_fill_tabular (core.column_table_result_core_t):
    """
    Class that parses tabular "show" command output.


    `Example`::

        show_command_output_example = '''
            RP/0/0/CPU0:one#show rib clients
            Thu Sep 17 11:41:18.164 EDT
            Process              Location         Client ID  Redist   Proto
            bcdl_agent           node0_0_CPU0     0          insync   no
        '''

        from genie.parsergen import oper_fill_tabular
        res = oper_fill_tabular(
            device=device1,
            show_command="show rib clients",
            header_fields =
                ["Process", "Location", "Client ID", "Redist", "Proto"])
        print res.entries['bcdl_agent']['Location']

    will print ``node0_0_CPU0`` ::

     set second_show_command_output_example '''
     RP/0/0/CPU0:one#show isis topology level 1
     Sat Sep 19 14:46:33.902 EDT

     IS-IS ring paths to IPv4 Unicast (Level-1) routers
     System Id       Metric  Next-Hop        Interface       SNPA
     one             --
     two             10      two             Gi0/0/0/0       *PtoP*
     two             10      two             Gi0/0/0/1       02db.ebba.ecc4
     three           20      two             Gi0/0/0/0       *PtoP*
     three           20      two             Gi0/0/0/1       02db.ebba.ecc4
     '''

     res = oper_fill_tabular ( device=device1,
                               show_command="show isis topology level 1",
                               header_fields=
                                   ["System Id", "Metric", "Next-Hop",
                                    "Interface", "SNPA"],
                                  index=[0,3])
     print res.entries['three']['Gi0/0/0/1']['SNPA']

    will print ``02db.ebba.ecc4`` ::

        print res.entries['one']['']['Metric']

    will print ``--``

    .. note:: The tabular parsing behavior may be customized via subclassing.
     Please refer to :ref:`core-non-tabular-parser-subclass-example`
     and :download:`tabular_parser_subclass.py <../examples/parsergen/pyAtsStandaloneUt/tabular_parser_subclass.py>` for examples.
    """

    def __init__ (self,
                  device = None,
                  show_command = None,
                  refresh_cache = True,
                  header_fields = None,
                  table_terminal_pattern = None,
                  index = 0,
                  skip_header = None,
                  table_title_pattern = None,
                  right_justified = False,
                  label_fields = None,
                  is_run_command = False,
                  skip_line = None,
                  device_conn_alias = None,
                  device_output = None,
                  device_os = None,
                  delimiter=''):

        """Creates a results object that parses tabular "show" command output.

        :Returns:

          Parsed results are obtained by using the column positions of the
          header field. The entry starts with the column of the first header
          character and ends just prior to the next header column.

          The object returned has a dictionary named ``entries`` which is
          keyed by the entry value corresponding to the header at `index`.
          Each key in ``entries`` is indexed by the corresponding
          `header_fields` name (or `label_fields` name if specified).

        Parameters
        ----------
        device : `Device()`
            The device to run the show command on.

        device_conn_alias : `str`
            If specified, assume the device was connected to under the
            indicated alias.
            Otherwise, the default alias is assumed.
            For details, please see
            https://developer.cisco.com/docs/pyats/
            ConnectionMeta - > Connection Manager

        show_command : `str` or `tuple` of \
            (`str`, `list` of positional formatting args, \
            `dict` of keyword formatting args)
            The key into the show command dictionary previously passed to
            `extend` or the actual show command to issue.
            If the corresponding show command dictionary string contains
            formatting fields, specify these arguments using a `tuple`.

        refresh_cache : `bool`
            If ``True``, refresh the cache by running the indicated show
            command on the device again, and then parse this output.
            If ``False``, parse the previously cached show command
            output.  Defaults to ``True``.

        header_fields :  `list` of `str`
            List of column headings to parse.  If not specified, it must be
            provided via a subclass via ``get_init_info``.

        table_terminal_pattern : `str`
            If specified, this is the pattern to terminate the search for
            results.

        index : `int` or `list` of `int`
            Defaults to the first field (0). If more fields are required to
            guarantee uniqueness pass a list of indices in `index` and that
            many dictionaries will be returned keyed by the given field values
            at those indices.

        skip_header : `str`
            If specified, then the input between the header fields and this
            pattern are skipped before entries are looked for.

        table_title_pattern : `str`
            If specified, this pattern allows multiple tables to be identified.
            Results will be a dictionary of matches keyed on
            ``group('Title')`` of the regex.
            (e.g., a pattern like ``r'(?P<Title>Port (\w+))'`` would match
            ``"Port GigabitEthernet_0_0_0_0 ..."`` and the key would be
            ``'GigabitEthernet_0_0_0_0'``).

        right_justified : `bool`
            If ``True``, then the header labels are considered right justified.
            Defaults to ``False``.

        label_fields : `list` of `str`
            If specified, then the ``entries`` object will contain these keys
            instead of those specified in `header_fields`.  There must be a
            corresponding entry in `label_fields` for each entry in
            `header_fields`.

        skip_line :  `str`
            If specified, then any line matching this pattern will be skipped.

        delimiter :  `str`
            Table delimiter pattern that allows for columns' borders
            identification.
        """
        self.entries = {}
        '''A dictionary containing the results of the show command.'''

        self._refresh_cache      = refresh_cache
        self._refresh_cache_init = refresh_cache
        self._show_command       = show_command
        if device:
            self._device             = device
            self._device_conn_alias  = device_conn_alias
            self._device_os          = get_os_type(
                device=self._device, alias=self._device_conn_alias)
        elif device_output:
            device = Device('device_name')
            self._device = device
            self._device_conn_alias = 'any'
            self._device_os = device_os
        else:
            raise AttributeError("Neither 'device' nor 'device_output' "
                                 "(device output might be empty) "
                                 "has been passed when calling '%s'" %self)

        if isinstance(index, int):
            self.index = [ index ]
        elif isinstance(index, list):
            self.index = index
        else:
            raise ValueError(str(index) + " is not an int or list of ints")

        if device_output:
            core.text_to_parse[self._device.name] = device_output
        else:
            # check if cache has to be refreshed
            if self._refresh_cache :
                showCmdCache.refresh_cache(self, self._show_command)
            elif self._device.name not in showCmdCache.cache.keys():
                logger.warning(\
                  ('refresh_cache = False but no output found for %s ' + \
                  '=> collect output') \
                        %self._device.name)
                showCmdCache.refresh_cache(self, self._show_command)
            else:
                core.text_to_parse[self._device.name] = \
                    showCmdCache.cache[self._device.name]

        # Support the case when device output contains "\r\n"
        core.text_to_parse[self._device.name] = \
            core.text_to_parse[self._device.name].replace("\r\n", "\n")
        core.text_to_parse[self._device.name] += '\n'

        # Call parsergen.core
        core.column_table_result_core_t.__init__(self,
                                                 header_fields,
                                                 table_terminal_pattern,
                                                 index,
                                                 skip_header,
                                                 table_title_pattern,
                                                 right_justified,
                                                 label_fields,
                                                 skip_line,
                                                 self._device.name,
                                                 delimiter)

###############################################################################
# Device base class.
###############################################################################
class Device():

    """
    Defining a device class to eliminate parsergen
    dependency on a device object
    """

    def __init__ (self, name, *args, **kwargs):
        self.name = name

    def execute(self, *args, **kwargs):
        pass

    def is_connected(self, alias, *args, **kwargs):
        return True
