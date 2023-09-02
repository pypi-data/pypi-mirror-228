import logging, string, sys, inspect, argparse, collections
from re import compile
from re import match
from re import search
from re import sub
from re import escape

python3 = sys.version_info >= (3,0)

logger = logging.getLogger(__name__)

if python3:
    def warning(s):
        logger.warning(s)
else:
    def warning(s):
        logger.warn(s)

supported_oses = [ 'ios', 'iosxr', 'iosxe', 'nxos', 'calvados', 'iox',
                              'pix', 'asa', 'sanos', 'dcos', 'aireos', 'linux' ]

###############################################################################
# _mk_parser_gen_t base class.
###############################################################################
class _mk_parser_gen_t:
    '''This class converts special show command markup into parsergen input
       syntax.

       Description of mkpg markup syntax:

       XxX.... or
       Xx<desc>X....

       desc is the string to label the match in the table
       x is literal and x is one of:

       A - address (ipv4 or ipv6)
       B - bracketing - match value inside parens, braces brackets
       C - comma - match value up to comma
       I - interface name
       F - floating point number
       H - hex number
       M - mac address
       N - number
       R - newline requires
       P - prefix address (ipv4 or ipv6)
       q - quotes - match value inside double quotes
       S - non-space
       T - time (00:0:00)
       W - word

       or XXX<regex>XXX... or
       or XXX<regex><desc>XXX...

       regex is a regular expression
       desc is the string to label the match in the table
    '''

    regex = {
        'A': r"[A-Fa-f0-9:\.]+",
        'B': r"[^\)\]\}]+",
        'C': r"[^,]+",
        'F': r"\d+.\d+",
        'H': r"(?:0x)?[a-fA-F0-9]+",
        'I': r"[-A-Za-z0-9\._/:]+",
        'M': r"[0-9A-Za-z\.\:]+",
        'N': r"\d+",
        'P': r"[A-Fa-f0-9/:\.]+",
        'Q': r'[^\"]+',
        'R': r"[^\r\n]+",
        'S': r"\S+",
        'T': r"\d{2}:\d{2}:\d{2}",
        'W': r"\w+",
    }

    def __init__ (self):
        bigstr = "|".join([ "X{}(?:<[^>]+>)?X{}".format(key, value) \
            for key, value in self.regex.items() ])
        self.allregex = compile(r"(?:" + bigstr + "|"
                    r"X[xX]X(?:<(?P<regex>[^>]+)>)(?:<(?P<desc>[^>]+)>)?X[xX]X"
                    ")")

        # Lowercase means this item shouldn't be matched as a group
        regex_new = self.regex.copy()
        keys = self.regex.keys()
        for k in keys:
            regex_new[k.lower()] = self.regex[k]
        self.regex = regex_new

        bigstr = "|".join([ "X{}(?:<[^>]+>)?X{}".format(key, value) \
            for key, value in self.regex.items() ])

        self._alloptregex = compile(\
            r"(?:" + bigstr + "|"
            r"X[xX]X(?:<(?P<regex>[^>]+)>)(?:<(?P<desc>[^>]+)>)?X[xX]X"
            ")")

        self._descregex = r"X(.)(?:<([^>]+)>)?X"

        self._postItemDescRegex = compile(r"\S*\s+([^,\r\n]+)[,\r\n]*")

        self._cleanUpPdescRegex = compile(r"[^\w-]")

        # XXX need to replace space with ' \s*'
        # XXX need to allow for optional values.

        self._commands = {}
        self._regexdict = {}
        self._regexkeydict = {}
        self.prefixDescSet = set()
        self._autoKeyJoinChar=''


    def escape (self, line):
        line = sub("\(", "\\(", line)
        line = sub("\)", "\\)", line)
        line = sub("\?", "\\?", line)
        line = sub("\+", "\\+", line)
        line = sub("\*", "\\*", line)
        line = sub("\[", "\\[", line)
        line = sub("\]", "\\]", line)
        line = sub(r"\s+$", r"\\s+", line)
        return line

    def convert (self, os, line, groupnum):
        '''Render an output line, given a line of marked-up input.

        Isolate the marked-up pattern corresponding to the indicated group
        number and:
          - replace it with the required regular expression,
          - apply grouping parentheses,
          - auto-create the regex key by scanning surrounding text if the
            user has not specified the key name.

        Returns
        -------
            The regex key and value to include in the final output.

        Parameters
        ----------
        os : `str`
            The operating system name for which the line is being rendered

        line : `str`
            The line of marked-up input to render

        groupnum : `int`
            The marked-up pattern in the line to isolate (0-based).
        '''
        descs = {}
        rematch = self._alloptregex.search(line)
        count = 0
        desclist = []
        prevmatch = None
        pdesc = ""
        #logger.debug ("convert : os={}, line={}, groupnum={}".\
        #   format(os, line, groupnum))
        while rematch:
            #logger.debug("count={}, groupnum={}".format(count,groupnum))
            #logger.debug("desclist={}".format(desclist))
            m = match(self._descregex, rematch.group(0))
            optional = m.group(1).islower()
            # if m.group(1).islower() and count != groupnum:
            #     #print("rematch.group(0) is {} m.group(1) is \
            # {}".format(rematch.group(0), m.group(1)))
            #     optional = "(?:"
            # else:
            #     # print("rematch.group(0) is {} m.group(1) is \
            # {}".format(rematch.group(0), m.group(1)))
            #     optional = ""

            if not prevmatch:
                #s = optional + self.escape(line[:rematch.start()])
                trailingText = line
                s = self.escape(line[:rematch.start()])
            else:
                #s = s[:prevmatch] + optional + \
                # self.escape(s[prevmatch:rematch.start()])
                #logger.debug("s at top of loop ={}".format(s))
                trailingText = s
                s = s[:prevmatch] + self.escape(s[prevmatch:rematch.start()])

            #
            # At this point, s contains leading text to the left of the current
            # match.  This text is typically used to auto-assign the regex key
            # if the user has not explicitly done so.
            #
            # trailingText contains trailing text to the right of the current
            # match.  This text may be needed to assign the regex key in some
            # cases.
            #

            # print("s is {}".format(s))

            # Groupnum is the in the nth (zero based) regex we expect to match
            # in the line
            if count == groupnum and not optional:
                s += "("

            #logger.debug("s={}".format(s))
            # use the text between matches to try and get a desc.
            if count == groupnum:
                if rematch.group('desc'):
                    pdesc = rematch.group('desc')
                else:
                    pdesc = m.group(2)
                if pdesc:
                    desclist = []
            if not pdesc and count <= groupnum:
                # Look for text before the current match.
                if prevmatch:
                    pdesc = s[prevmatch:rematch.start()]
                else:
                    pdesc = s[:rematch.start()]
                #logger.debug("pdesc (text preceding match)={}".format(pdesc))

                # Examine text after the current match to catch cases such as:
                # 0 packets output, 10 output errors
                #
                # where the text to use to create the name follows the
                # matched item and terminates with an EOL or comma.
                # In this example the names would be chosen as
                # packets-output and output-errors

                #logger.debug("s={}".format(s))
                #logger.debug("trailingText={}".format(trailingText))
                #logger.debug("linepostmatch={}".
                #    format(trailingText[rematch.start():]))
                #logger.debug("trailingText to search={}".\
                #   format(trailingText[rematch.start():]))

                postItemDescMatch = \
                    self._postItemDescRegex.match(
                        trailingText[rematch.start():])

                if postItemDescMatch:
                    # If there was a previous match, then only use the text
                    # after the current match if there was only a comma between
                    # the previous and current match and no other usable
                    # preceding text.
                    #
                    # Also, if there is usable leading text present and also
                    # trailing text present between the current item and a
                    # comma or newline, prefer the leading text.

                    if count == groupnum:
                        if (pdesc.rfind(',') > -1):
                            desclist = []
                            # Strip out all characters preceding the comma
                            # from the text preceding the current match, and
                            # remove all non-alphanumeric characters.
                            # If there are any characters left, prefer this
                            # leading text.  Otherwise, prefer the following
                            # text.
                            pdesc = pdesc.replace(' is', '')
                            pdesc = sub('[^\w]', '', sub('[^,]*,', '', pdesc))

                        if not pdesc or \
                          (pdesc and  pdesc.rfind('\\s') >= 0):
                            pdesc = postItemDescMatch.group(1)
                #logger.debug("pdesc={}".format(pdesc))
                index = pdesc.rfind(',')
                if index > -1:
                    desclist = []
                pdesc = pdesc[index+1:]
                pdesc = pdesc.strip()
                pdesc = pdesc.rstrip()
                # This happens b/c we replace ' ' with '\s+'
                pdesc = pdesc.rstrip(':\\')
                pdesc = pdesc.rstrip(':')
                pdesc = pdesc.lower()
                pdesc = pdesc.replace(' ', self._autoKeyJoinChar)
                pdesc = pdesc.replace('/', self._autoKeyJoinChar)
                pdesc = pdesc.replace('\t', self._autoKeyJoinChar)
                index = pdesc.rfind(self._autoKeyJoinChar+"is")
                if index > 0:
                    pdesc = pdesc[:index]
                if not pdesc:
                    pdesc = "unknown"
                pdesc = sub(self._cleanUpPdescRegex, '', pdesc)

            if rematch.group('regex'):
                s += rematch.group('regex')
            else:
                # get the markup type
                t = m.group(1)
                # add in the regex for that markup type
                s += self.regex[t]
                # better defaults for the description
                if pdesc == "unknown":
                    t = t.upper()
                    if t == "A":
                        pdesc = "addr"
                    elif t == "I":
                        pdesc = "intf"
                    elif t == "P":
                        pdesc = "prefix"

            if count == groupnum and not optional:
                s += ")"

            # make sure desc is unique
            if pdesc:
                if count == groupnum:
                    if pdesc in descs:
                        descs[pdesc] += 1
                        pdesc += "_" + str(descs[pdesc])
                    else:
                        descs[pdesc] = 0
                if count <= groupnum:
                    desclist.append(pdesc)

            count += 1
            #logger.debug('Reassigning prevmatch to {}'.format(len(s)))
            prevmatch = len(s)
            if not rematch.group('regex'):
                s += line[rematch.end():]
            else:
                # Special case we need to remove whatever matched the user
                # regex
                end = line[rematch.end():]
                regex2 = rematch.group('regex')
                match2 = search(regex2, end)
                assert match2 is not None, \
                    "ERROR: regex: '{}' doesn't match {}".\
                        format(regex2, end)

                s += end[match2.end():]
            # if optional:
            #     line = s + ")?"
            #     prevmatch += 2
            # else:
            line = s
            #logger.debug("Reassigned line to {}".format(line))
            rematch = self._alloptregex.search(line)

        # Should we be making sure that the users specification actually
        # matches the data?

        if prevmatch < len(line):
            line = line[:prevmatch] + self.escape(line[prevmatch:])
            # if optional:
            #     line += ")?"

        #line = sub(r'(\\-)+', '-', line) # This looks wrong
        #line = sub(r'(\\ )+', ' ', line) # This looks wrong
        #line = sub(r'(\\\t)+', '\t', line)

        # Change beginning space into 1 or more. not anymore.
        line = sub(r'^([ \t])+', r'\\s+', line)

        line = sub(r':([ \t])+', r':\\s+', line)
        line = sub(r'([ \t])+:', r'\\s+:', line)

        # Change spaces or tabs into one or more whitespaces
        # The problem is that this puts multiple spaces between normal
        # identifying words which might be if somewhat confusing.
        #line = sub(r"\s+", "\\s+", line)

        # We really want to do this for the space right before the matching
        # regex.  I guess or something to handle tag, value pairs without a :
        # line = sub(r'([ \t])+', ':\\s+', line)
        desclist = \
            [ sub('-$', '', sub('--*', '-', desc)) for desc in desclist ]
        return self._autoKeyJoinChar.join(desclist), line

    def _desc_max (self, os, output):
        desclen = 0
        for line in output.split("\n"):
            for count, rematch in enumerate(self.allregex.finditer(line)):
                desc, retext = self.convert(os, line, count)
                if len(desc) > desclen:
                    desclen = len(desc)
        return desclen


    def generate_output (self, generate_regex_tags=False,
        called_from_parsergen=False):
        '''
            Generate output synthesized from the marked-up input.
            This output can be consumed by a Python interpreter or placed
            into a separate file.

            Parameters
            ----------
            generate_regex_tags : `bool`
                If `True`, then generate an ordered list of regex tags
                synthesized from the marked-up input.  This helps power
                convenience features that allow for auto-creation of
                attr/value pairs during a parse-with-fill operation, and
                allow for automatic reordering of client's key/value pairs
                (since _parser_gen_t is extremely order-sensitive).
                This extra list is then passed into `extend`.
                If `False`, then the ordered list is neither generated nor
                passed into `extend`.

            called_from_parsergen : `bool`
                If `True`, then call the extend API through the parsergen
                package to ensure the right set of supported platforms are
                loaded.
                If `False`, then call the extend API through parsergen.core
                directly.
                Defaults to `False`.
        '''
        output = ''
        if called_from_parsergen:
            output += "from genie import parsergen as pgen\n"
        else:
            output += "from genie.parsergen import core as pcore\n"
        oses = sorted(self._commands.keys())

        #--------------------------+
        # First print the commands
        #--------------------------+
        output += "show_commands = {\n"
        for os in oses:
            maxlen = 0
            for cmd in self._commands[os].keys():
                l = len(cmd)
                if l > maxlen:
                    maxlen = l
            output += "    '{}': {{\n".format(os.lower())
            for cmd, showcmd in sorted(self._commands[os].items()):
                spaces = " " * (maxlen - len(cmd))
                output += \
                    "        '{}'{}: '{}',\n".format(cmd, spaces, showcmd)
            output += "    },\n"
        output += "}\n"

        #---------------------+
        # Now print the regex
        #---------------------+
        output += "regex = {\n"
        for os in oses:
            output += "    '{}': {{\n".format(os.lower())
            for cmd, markup in sorted(self._commands[os].items()):
                output += "        #\n"
                output += "        # {} ('{}')\n".\
                    format(cmd, self._commands[os][cmd])
                output += "        #\n"
                output += '{}\n'.format(self._regexdict[os][cmd])
            output += "    },\n"
        output += "}\n"

        if generate_regex_tags:
            #------------------------------------+
            # Now print the ordered regex key list
            #------------------------------------+
            output += "regex_tags = {\n"
            for os in oses:
                output += "    '{}': [\n".format(os.lower())
                for cmd, markup in sorted(self._commands[os].items()):
                    output += "        #\n"
                    output += "        # {} ('{}')\n".\
                        format(cmd, self._commands[os][cmd])
                    output += "        #\n"
                    output += '{}\n'.format(self._regexkeydict[os][cmd])
                output += "    ],\n"
            output += "}\n"
            if called_from_parsergen:
                output += "pgen.extend (regex, show_commands, regex_tags)\n"
            else:
                output += "pcore.extend (regex, show_commands, regex_tags)\n"
        else:
            if called_from_parsergen:
                output += "pgen.extend (regex, show_commands)\n"
            else:
                output += "pcore.extend (regex, show_commands)\n"
        return output

    def convert_output (self, showcmd, prefix, output, os, cmd):
        if not cmd:
            cmd = showcmd.replace(' ', '_').replace('-', '_').upper()

        if os is None:
            os = 'IOX'

        desclen = self._desc_max(os, output)

        if os not in self._commands:
            self._commands[os] = {}
            self._regexdict[os] = {}
            self._regexkeydict[os] = {}

            # assert cmd not in commands[os]
        self._commands[os][cmd] = showcmd
        indent = " " * 8

        self._regexdict[os][cmd] = ""
        self._regexkeydict[os][cmd] = ""
        for line in output.split("\n"):
            for count, rematch in enumerate(self._alloptregex.finditer(line)):
                #logger.debug("XXXprocessing count: {} match: {}".\
                #    format(count, rematch.group(0)))
                m = match(self._descregex, rematch.group(0))
                if m.group(1).islower():
                    continue
                desc, retext = self.convert(os, line, count)
                spaces = " " * (desclen - len(desc))
                self._regexdict[os][cmd] += "{}'{}.{}'{} : r'{}',\n".format(\
                    indent, prefix, desc, spaces, retext)
                self._regexkeydict[os][cmd] += "{}'{}.{}'{} ,\n".format(\
                    indent, prefix, desc, spaces)
                prefixDesc = '{}.{}.{}'.format(os, prefix, desc)
                if prefixDesc in self.prefixDescSet:
                    warning(\
                        '{} has been defined more than once '
                        '(command {},existing re{}, new re {}).'.\
                        format(prefixDesc, cmd, self._regexdict[os][cmd],
                               retext))
                else:
                    #logger.debug("Adding {} : {}".format(prefixDesc, retext))
                    self.prefixDescSet.add(prefixDesc)


    def process_marked_up_input (self,markup_iterator,auto_key_join_char='-'):
        ''' Process marked-up show command input.

            The OS, CMD, SHOWCMD and PREFIX sections may appear in any
            order, but the MARKUP section must always come last.

            Although the ACTUAL section is ignored, users may find it useful
            in order to indicate the unmarked-up raw show output.
        '''
        assert isinstance(markup_iterator, collections.abc.Iterable), \
            "Must provide an iterator to process_marked_up_input."

        self._autoKeyJoinChar=auto_key_join_char
        cmd = ""
        showcmd = ""
        prefix = ""
        markup = ""
        inmarkup = False

        logger.debug("process_marked_up_input")
        os = None

        for (line_number, line) in enumerate(markup_iterator):
            if not line:
                continue

            #logger.debug("process_marked_up_input (#{:<3}) : {}".\
            #format(line_number, line))
            m = match('OS: (.+)', line)
            if m:
                oldos = os
                os = m.group(1).lower()
                assert os in supported_oses, \
                    "Unknown OS {}, must be one of {}".\
                        format(os, supported_oses)

                inmarkup = False
                if markup:
                    self.convert_output(showcmd, prefix, markup, oldos, cmd)
                    showcmd = prefix = cmd = None
                    markup = ""

                # if os is not None and oldos is not None:
                #     print("    }},".format(os.lower()))
                # if os is not None:
                #     print("    '{}': {{".format(os.lower()))

                continue

            m = match('CMD: (.+)', line)
            if m:
                inmarkup = False
                if markup:
                    self.convert_output(showcmd, prefix, markup, os, cmd)
                    showcmd = prefix = cmd = markup = ""
                cmd = m.group(1)
                continue
            m = match('SHOWCMD: (.+)', line)
            if m:
                inmarkup = False
                if markup:
                    self.convert_output(showcmd, prefix, markup, os, cmd)
                    showcmd = prefix = cmd = markup = ""
                showcmd = m.group(1)
                continue

            m = match('PREFIX: (.+)', line)
            if m:
                inmarkup = False
                if markup:
                    self.convert_output(showcmd, prefix, markup, os, cmd)
                    showcmd = prefix = cmd = markup = ""
                prefix = m.group(1)
                continue

            if line.startswith("MARKUP:"):
                assert not inmarkup, \
                  "Found two back-to-back MARKUP sections at line number {}."\
                    .format(line_number)
                assert not markup, "error processing marked-up input."
                inmarkup = True
                continue

            if inmarkup:
                markup += line
                if '\n' not in line:
                    markup += '\n'

        if inmarkup and markup:
            inmarkup = False
            self.convert_output(showcmd, prefix, markup, os, cmd)
            showcmd = prefix = cmd = markup = ""
            # if os is not None:
            #     print("    }},".format(os.lower()))

def extend_markup (marked_up_input, auto_key_join_char = '-' ):
    ''' Allows an external module to extend the dictionary of
    `regular expressions<re>` and known show commands by specifying marked-up
    show command text (see :ref:`parsergen.core_markup`)

    This input text is transformed, and then automatically passed to
    `extend`.



    Parameters
    ----------
    marked_up_input : `str`
        Marked-up show command input

    auto_key_join_char : `str`
        For those marked up blocks where no name is provided, the key name
        is inferred from the CLI text surrounding the block.  This can involve
        joining multiple words that are in close proximity to the block.
        These words are joined together with this character, which defaults
        to ``-`` (dash).  Only alphanumeric characters are accepted,
        a recommended alternate value is ``_`` (underscore).

    '''
    mkpg = _mk_parser_gen_t()
    mkpg.process_marked_up_input (iter(marked_up_input.splitlines()),
        auto_key_join_char)
    mkpg_output = mkpg.generate_output(generate_regex_tags=True)

    #
    # Call the extend API with the auto-generated show command and
    # regular expression dictionaries.
    #
    exec(mkpg_output)

def extend (regex_ext=None, show_cmds = None, regex_tags = None):
    ''' Allows an external module to extend the dictionary of
    `regular expressions<re>` and known show commands.

    :mod:`parsergen.core` keeps its master `regular expression<re>` dictionary
    in the member ``parsergen.core._glb_regex``, its master show command
    dictionary in the member ``parsergen.core._glb_show_commands`` and its
    master regex tag list in the member ``parsergen.core._glb_regex_tags``.

    Parameters
    ----------
    regex_ext : A dictionary of `regular expressions <re>` or a \
        `dict` of `dictionaries<dict>` of `regular expressions <re>` keyed by \
        OS type
        A series of tags (keys) and their corresponding `regexes<re>` (values).
        A `regex<re>` may also be expressed as a `list` of `regexes<re>`
        (this feature can help allow a parser to continue working across
        multiple releases in which CLI text changes).

    show_cmds : A dictionary of `str` or a `dict` of `dictionaries<dict>` of \
        `str` keyed by  OS type
        A series of generic CLI command tags (keys) and their corresponding CLI
        command equivalents (values). CLI commands are specified as `str` and
        may contain string formatting arguments.

    regex_tags : A `dict` of `lists<list>` of regex tags keyed by  OS type
        A series of tags (keys).  This allows parsergen.core to store the original
        order order the tags were declared to enable users to implement a
        pattern-driven auto-parse-fill feature.

    '''
    def _add(rd, r, d):
        if r in rd and rd[r] != d:
            warning("%s already exists, please change name" % r)
        else:
            rd[r] = d

    rds = []
    if regex_ext:
        rds.append((_glb_regex, regex_ext))

    if show_cmds:
        rds.append((_glb_show_commands, show_cmds))

    for rd, ext in rds:
        if python3:
            ext_items = iter(ext.items())
        else:
            ext_items = ext.iteritems()

        for key, value in ext_items:
            if key in supported_oses:
                if key not in rd:
                    rd[key] = {}
                rd2 = rd[key]
                if python3:
                    value_items = iter(value.items())
                else:
                    value_items = value.iteritems()
                for k2, v2 in value_items:
                    _add(rd2, k2, v2)
            else:
                _add(rd, key, value)

    if regex_tags:
        for os in regex_tags:
            if os in supported_oses:
                if os not in _glb_regex_tags:
                    _glb_regex_tags[os] = []
                for tag in regex_tags[os]:
                    if tag in _glb_regex_tags[os]:
                        warning("regex tag {} already exists, "
                                "please change name".format(tag))
                    else:
                        _glb_regex_tags[os].append(tag)
            else:
                warning("os {} is not one of the supported oses {}.".
                    format(os, supported_oses))

ext_dictio = {}
''' OUTPUT VARIABLE
 In this dictionary we make all extracted values accessible from outside
 for further analysis. It can be filled with oper_fill.
 It is indexed by a unique key (such as router name).
'''

text_to_parse = {}
'''INPUT VARIABLE
This dictionary holds the text to parse.
It is indexed by a unique key (such as router name).
'''





''' PARSERGEN module

This module is a generic parser for indented show commands. The goal is to
provide a common API for parsing of any kind of text-like output coming from
a show command. It's not related to a particular process nor does it make
any assumption on the output it is going to parse.

Main functions are:
    - match input regular expressions in the given order
    - extendible dictionary of regular expressions

HOW IT WORKS

Parsergen tries to match grammar and values of regular expressions in the show
command output. The main idea is to exploit the structured form of the output
printed by a common datalist operations. The regular expressions matching is
tried thru a hierarchical process.

'''

_glb_regex = { }

''' REGULAR EXPRESSIONS

Dictionary containing all known regular expressions in the form:
{
      'alias1' : '...',
      'alias2' : '...',
}

Alternatively, this dictionary may have the form:
{
    'os1' : {
        'alias1' : '...',
        'alias2' : '...',
    }

    'os2' : {
        'alias1' : '...',
        'alias2' : '...',
    }
}

Where ``os1`` and ``os2`` represent a valid operating system name.

A naming convention should be used for aliases to reduce the probability
of encoding the same alias twice :

      processname.class1-class2-...-classN

For instance the mtu value of an xconnect retrieved from l2vpn_mgr process
will be :

      l2vpn.xcon-mtu

IMPORTANT : build your regex dictionary in an external file and extend this
global one thru the extend function. Recommendation : call extend function from
the suite_prologue of your suite.

The :ref:`mkpg-index` script may be used to autogenerate this regex dictionary.

'''

def _get_regex (routerOs, attribute):
    if routerOs in _glb_regex and attribute in _glb_regex[routerOs]:
        return _glb_regex[routerOs][attribute]
    if attribute in _glb_regex:
        return _glb_regex[attribute]
    return None


_glb_show_commands = {}

'''
SHOW COMMANDS - not mandatory
List of known show commands in the form :
{
   1 : 'show ...',
   2 : 'show ...,
}

IMPORTANT : build your dictionary in an external file and extend this global
            one thru the extend function. Recommendation : call extend function
            from the suite_prologue of your suite.
'''

_glb_regex_tags = {}
'''This dictionary holds for each OS name an ordered list of the regex keys
in the order they were defined by the user.  This is done as an assist in
helping the user construct their list of regex keys to parse when doing a
parse-with-fill operation (since order is important, mixing the order of two
regex keys up can cause the parse to fail).  This dictionary can also be used
to auto-order user (attr,value) pairs for the parse-with-compare operation.
{
    'os1' : [
        'alias1' ,
        'alias2' ,
    ]

    'os2' : {
        'alias1',
        'alias2',
    }
}'''


def is_int (s):
    try:
        int(s)
        return True
    except ValueError:
        return False

###############################################################################
# DefaultFormatter base class.
###############################################################################
class DefaultFormatter (string.Formatter):
    """String formatter that allows for embedded default values using
       {[key|index]=<defval>} syntax

    >>> formatter = DefaultFormatter()
    >>> s ="{: {align}{=18}}{=default-value!r}{mykey=another-default}{noneval}"
    >>> formatter.format(s, "firstval", 20, noneval=None, align='>')
    "            firstval'default-value'another-defaultNone"
    >>> formatter.format(s, "firstval", noneval=None, align='>')
    "          firstval'default-value'another-defaultNone"
    """
    def __init__ (self, defidxval = None, defkeyval = None):
        """Create a formatter object.

        :Parameters:
          - *defidxval* - The default value for missing index paramteres
          - *defkeyval* - The default value for missing keyword paramteres
        """
        self.defidxval = defidxval
        self.defkeyval = defkeyval
        super(DefaultFormatter, self).__init__()


    def vformat (self, fmt, args, kwargs):
        #logger.debug ("vformat({})".format((fmt, args, kwargs)))

        # Reset our per format values
        self.posarg = -1
        self.defval = None
        rv = super(DefaultFormatter, self).vformat(fmt, args, kwargs)
        return rv

    def get_field (self, field, args, kwargs):
        #logger.debug ("get_field({}, posarg={})".
        #    format((field, args, kwargs), self.posarg))
        self.defval = None
        m = match(r'(.*)=(.*)', field)
        if m:
            self.defval = m.group(2)
            field = m.group(1)
        if field == '' or (python3 and is_int(field)):
            self.posarg += 1
            field = str(self.posarg)
        else:
            if is_int(field):
                self.posarg = int(field)
        rv = super(DefaultFormatter, self).get_field(field, args, kwargs)
        #logger.debug ("get_field({}) => {}\n".
        #    format((field, args, kwargs), rv))
        return rv

    def get_value (self, key, args, kwargs):
        #logger.debug ("get_value({})".format((key, args, kwargs)))
        #logger.debug ("defval={}, defidxval={}".
        #    format(self.defval, self.defkeyval))
        if isstr(key):
            try:
                rv = kwargs[key]
                #
                # User has specified a placeholder to select default key.
                #
                if rv is None:
                    raise KeyError
            except KeyError:
                if self.defval is None and self.defkeyval is None:
                    raise
                if self.defval is None:
                    rv = self.defkeyval
                else:
                    rv = self.defval
        else:
            try:
                rv = args[key]
                #
                # User has specified a placeholder for a default value.
                #
                if rv is None:
                    raise IndexError
            except IndexError:
                if self.defval is None and self.defidxval is None:
                    raise
                if self.defval is None:
                    rv = self.defidxval
                else:
                    rv = self.defval
        #logger.debug ("get_value({}) => {}\n".
        #    format((key, args, kwargs), rv))
        return rv


def _get_show_command (routerOs, show_cmd_arg):
    args = []
    kwargs = {}
    if not isstr(show_cmd_arg) and hasattr(show_cmd_arg, '__getitem__'):
        show_cmd = show_cmd_arg[0]
        try:
            args = show_cmd_arg[1]
            kwargs = show_cmd_arg[2]
        except IndexError:
            pass
        if isstr(args):
            args = [ args ]
    else:
        show_cmd = show_cmd_arg

    if routerOs in _glb_show_commands and \
            show_cmd in _glb_show_commands[routerOs]:
        cmd = _glb_show_commands[routerOs][show_cmd]
    elif show_cmd in _glb_show_commands:
        cmd = _glb_show_commands[show_cmd]
    else:
        cmd = show_cmd

    cmd = DefaultFormatter().vformat(cmd, args, kwargs)
    return cmd


###############################################################################
# _parser_gen_t base class.
###############################################################################
class _parser_gen_t:
    ''' Class that parses non-tabular "show" command output based on the input
    lists of `regex<re>` tags and expected values.
    '''
    _dictio = {}

    def __init__(self, routerOs, attributes, values,  \
                       fill = False, parse_key = '', skip = False):
        ''' Creates an object to parse non-tabular "show" command output.

        Parameters
        ----------
        routerOs : `str`
            The operating system name of the router
             whose output we are parsing.

        attributes : `list` of regex tags
            list of regex tags.  These tags must have been
            previously associated with `regexes<re>` via the
            `extend` or `extend_markup` APIs.

        values : `list`
            In the case where **fill** is `True`, each value can be either a
            single object or a tuple of objects (multiple values are then
            considered in the match).  In the case where **fill** is `False`,
            the first value in the list is expected to be set to a
            non-``None`` value (either a simple object or a tuple), while the
            remaining values in the list are expected to be set to ``None``
            in order to instruct the parser which fields to parse.

        fill : `bool`
            If `True`, then match all non-`None` values and fill all `None`
            values.  If `False`, determine the actual value of each
            attribute and ensure it matches the expected value.
            Defaults to `False`.

        skip : `bool`
            Whether or not to ignore unmatched attributes(regex tags).
            If `True`, then ignore any attributes (regex tags) whose
            associated `regexes<re>` do not match the text to parse.
            One reason to specify this option could be when the text to parse
            is expected to contain optional content lines.
            Defaults to `False`.

        parse_key : `str`
            Unique key to identify the textual output to parse.  The text is
            expected to be populated in
            ``parsergen.core.text_to_parse[parse_key]``.  For example,
            this field could be set to the router name.  Defaults to
            ``''`` (empty string).

        '''
        # Since the skip algorithm is destructive, make a copy to ensure the
        # user's attribute list is not modified.
        self._attributes = list(attributes)

        self._values     = values
        self._routerOs   = routerOs.lower()
        self._parse_key  = parse_key
        ext_dictio[parse_key] = {}
        assert self._routerOs in supported_oses, \
            "The operating system {} is not supported, try using one of {}.".\
                format(routerOs, supported_oses)

        # start logs
        self._errors = []
        self.error(self.__class__.__name__)

        # fill the dictionary without testing (oper_fill)
        self._fill = fill
        self._skip = skip

        if self._fill:
            assert self._values, \
                "values list cannot be empty"
            assert self._values[0] is not None, \
                "Cannot perform the fill operation unless the first \
                 value is not None"

        # Do not strip leading or trailing spaces, since these could be
        # expected.
        self._text_to_parse = text_to_parse[parse_key].strip("\t\n\r\f\v")


        # launch parser
        self._parser()

    def _parser_check_scope(self, regex_done, line):
        for reg in regex_done:
            if reg.match(line) != None:
                logger.debug("Regular expression hierarchy violated at "
                                  "line '%s' (hint: overlapping regular "
                                  "expression in the same predicate and on "
                                  "different line ?" % line)

                return False
        return True

    def _parser_current_matching(self, value_to_match, value_found):
        ''' Loop thru the list of associated values to find the matching if any

        :Parameters:
          - `value_to_match` () - value to be matched
          - `value_found` () - value extracted by the regular expression
        '''
        # if we just moved to next line, check that we're still in the same
        # bag, otherwise we may hit false matching (for instance we find the
        # expected values into another section of the output).

        if not isstr(value_to_match) and \
                isinstance(value_to_match, collections.abc.Iterable):
            for value in value_to_match:
                if str(value) == value_found : return True
        else :
            if str(value_to_match) == value_found : return True

        return False

    def _parser_future_matching (self, regex, regex_done, line):
        """ Check future matching (in the not analyzed output) for current
        regular expression.
        Return True if the regex can be found in the same bag, False otherwise

        :Parameters:
          - `regex_done` (`list`) - list of compile objects already analyzed
          - `regex` () - current regex
          - `line` () - current line
        """

        # index of current line
        idx = self._text_to_parse.find(line)
        if idx == -1 : return False

        # quick check to verify whether the current regex will have a
        # future matching
        idx += len(line)
        regex = "(.*[\n])*.*"+regex
        m = compile(regex).match(self._text_to_parse[idx:])
        if m == None: return False

        # the current regex must find a match within the same output section
        # to be valid
        lines = self._text_to_parse[idx:].split("\n")
        for line in lines:
            line = line.replace("\r","")
            m_next = compile(regex).match(line)
            for reg in regex_done:
                m_done = reg.match(line)
                if m_done != None: break
            if m_done != None: return False
            if m_next != None and m_done == None: return True

        if m_next != None: return True

    def _parser_delete_non_matching (self, lines, regex_tags):
        """ Remove any regex tag whose pattern(s) do not match the
        text to parse.

        :Parameters:
          - `lines` () - output to parser, split into lines
          - `regex_tags` () - list of regexes to parse
        """

        remove_list = []

        for regex_tag in regex_tags:
            regitem = _get_regex(self._routerOs, regex_tag)
            if isstr(regitem):
                regex_def_l = (regitem, '')
            else :
                regex_def_l = regitem

            for regex_def_n in regex_def_l:
                if len(regex_def_n) < 2 : continue
                regex_n = compile(regex_def_n)

                remove_regex = True

                for line in lines:
                    match_n = regex_n.match(line)
                    if match_n:
                       remove_regex = False
                       break

                if remove_regex:
                    remove_list.append(regex_tag)
                    #print("Removing {}".format(regex_tag))

        for regex_tag in remove_list:
            regex_tags.remove(regex_tag)


    def _parser(self):
        ''' Generic parsing function. It identifies the desired bag in the
        datalist based on the order of the regex list and tries to match all
        regex in the given order. if not, it returns a list of unmatched
        values.
        '''
        # initialize working variables
        dictio = {}
        regex_done = []
        regex_previous = ''

        # Split the output into lines
        lines = self._text_to_parse.split("\n")

        # If requested, remove any attributes (regex tags) which don't match
        # any line of the output.
        if self._skip:
            self._parser_delete_non_matching(lines, self._attributes)

        # Make a copy of the attributes array, as the parsing algorithm is
        # destructive.
        attributes = list(self._attributes)
        attribute_n = attributes[0]
        attribute_n_idx = 0
        none_wild_match = []

        # initilize exit conditions
        (sequence_validate, sequence_started) = (True, False)

        # loop thru the output lines
        for lineno, line in enumerate(lines):
            line = line.replace("\r","")
            #logger.debug("_parser (#{:<3}) : {}".format(lineno, line))

            # check the hierarchy search
            if self._parser_check_scope(regex_done, line) == False:
                sequence_validate = False
                break

            regitem = _get_regex(self._routerOs, attribute_n)
            if isstr(regitem):
                regex_def_l = (regitem, '')
            else :
                regex_def_l = regitem

            regex_def_idx = 0
            found_regex = False
            goto_nextline = False

            regex_same_line = []
            for regex_def_n in regex_def_l:
                assert regex_def_n is not None, \
                    "The attribute {} (OS={}) was not found. \
                     Was it added via the extend API?".\
                        format(attribute_n, self._routerOs)

                regex_def_idx = regex_def_idx + 1
                if len(regex_def_n) < 2 : continue
                if found_regex : break
                if goto_nextline : break
                regex_n = compile(regex_def_n)

                match_n = regex_n.match(line)

                match_on_line = 0
                # looping thru regex that finds a match on the same line
                while match_n and sequence_validate :
                    # numbers of regular expressions matching on one line
                    match_on_line += 1
                    # found current regex to True
                    found_regex = True
                    # move to next regex to False
                    move_to_next = False
                    # check the expected value and save into the external
                    # dictionary
                    ext_dictio[self._parse_key][attribute_n] = match_n.group(1)
                    # TRUE : parsing is successful and value matches
                    value_n = self._values[attribute_n_idx]
                    #if isinstance(value_n, type(())):
                    if not isstr(value_n) and \
                            isinstance(value_n, collections.abc.Iterable):
                        if regex_def_idx < len(value_n):
                            # N values, 1 regular expression
                            value_to_match = value_n
                        elif regex_def_idx - 1 < len(value_n):
                            # N values, N regular espressions
                            value_to_match = value_n[regex_def_idx - 1]
                        else :
                            # inconsistent case, pick up first value
                            value_to_match = value_n[0]
                    else :
                        # 1 value
                        value_to_match = value_n

                    # we store the regex executed on the same line so we don't
                    # use the same twice
                    regitem = _get_regex(self._routerOs, attribute_n)
                    if regitem in regex_same_line:
                        goto_nextline = True
                        break
                    else:
                        regex_same_line.append(regitem)

                    if self._fill == True and value_to_match == None:
                        dictio[attribute_n] = True
                        sequence_started = True
                        move_to_next = True
                    elif value_to_match == None:
                        # Here we are matching anything to establish a change
                        # in hierarchy
                        # If a later value fails we want to reset back to this
                        # point and keep trying
                        none_wild_match.append([])
                        dictio[attribute_n] = True
                        sequence_started = True
                        move_to_next = True
                    else :
                        if self._parser_current_matching(\
                                value_to_match, match_n.group(1)) :
                            dictio[attribute_n] = True
                            sequence_started = True
                            move_to_next = True
                        else :
                            # FALSE : parsing is successful but value does not
                            # match
                            dictio[attribute_n] = {"value":match_n.group(1), \
                                                   "line":lineno}
                            # If the regex sequence is already started, we have
                            #  to invalidate the parsing and return False,
                            # indeed it means that some of the expected values
                            # does not match the targeted bag.
                            #
                            # The cases where the sequence is still true are :
                            #  - sequence not yet started, then we are still
                            #    looking for the targeted bag
                            #  - two identical regex with different names could
                            #     be used to match different
                            #     part of the output
                            #     (ex primary and backup pw of an xconnect)
                            if (sequence_started and
                                regex_previous != regex_n and
                                self._fill == False and
                                self._parser_future_matching(regex_def_n, \
                                    regex_done, line) == False):
                                if none_wild_match:
                                    # We have a wildcard match for hierarchy
                                    # but a failed value match so push the
                                    # attributes back onto the stack and
                                    # unwind what we've done
                                    #print "value: {} != {} in line {} \
                                    # with wildcard".format(match_n.group(1), \
                                    # value_to_match, line)
                                    restore_attrs = none_wild_match.pop()
                                    for attr in reversed(restore_attrs):
                                        #print "restoring attribute {}".\
                                        #format(attr)
                                        del dictio[attr]
                                        del ext_dictio[self._parse_key][attr]
                                        attributes[0:0] = [ attr ]
                                        attribute_n_idx -= 1

                                        popped = regex_done.pop()
                                        #print "regex no longer done {}".\
                                        #format(popped)
                                        if regex_done:
                                            regex_previous = regex_done[-1]
                                        else:
                                            regex_previous = None
                                    goto_nextline = True
                                    attribute_n = attributes[0]
                                    #print "attributes: {}".format(attributes)
                                else:
                                    sequence_validate = False
                            # exit the loop
                            break

                    if move_to_next :
                        if none_wild_match:
                            # if we have a wildcard match, save this attribute
                            none_wild_match[-1].append(attribute_n)

                        # delete matched attribute
                        attributes.remove(attribute_n)
                        # move to next element if there are are remaining
                        if len(attributes) >= 1 :
                            # consider new attribute, first in the list to
                            # preserve hierarchy
                            attribute_n = attributes[0]
                            # when a regex is matched, we don't expect another
                            # match as it could refer to an inner level
                            regex_done.append(regex_n)
                            regex_previous = regex_n
                            # compile new regex
                            regex_n = compile(\
                                self.__get_regex_def(attribute_n, line))
                            #regex_n = compile(regex[attribute_n])
                            match_n = regex_n.match(line)
                            attribute_n_idx = attribute_n_idx + 1
                        else :
                            # checked everything
                            break

            if not attributes:
                break

        for i, attr in enumerate(self._attributes):
            # regex did not match as expected (we passed None)
            if (attr not in dictio.keys()) and  (self._values[i] == None) :
                 dictio[attr] = True

        self._dictio = dictio
        self._validate = sequence_validate
        #logger.debug("VALUES : %s " % self._values)
        #logger.debug("ATTRIBUTES : %s " % self._attributes)
        #logger.debug("DICTIO : %s " % dictio)

    def __get_regex_def(self, attribute_n, line):
        ''' We can associate multiple regular expression to an attribute, so we
        loop thru all the associated to find a possible match if any

        :Parameters:
          - `attribute_n` () - alias for the attribute
          - `line` () - current line

        '''
        regitem = _get_regex(self._routerOs, attribute_n)
        if isstr(regitem):
            return regitem

        regex_def_l = regitem
        for regex_def_n in regex_def_l:
            if compile(regex_def_n).match(line) != None:
                return regex_def_n

        # no match possible, just return something
        return 'NO_MATCH_POSSIBLE'

    def _parser_validate(self):
        ''' Report the parse result to the user.
        When the parsing is done, we validate its results by looking at the
        built dictionary. It must have as many values as requested and all of
        them should be True.

        Returns
        -------
        A tuple (``parse_succeeded``, ``dictio``, ``msg``)


        Where ``parse_succeeded`` is set to `True` if the parse
        succeeded and `False` otherwise.  ``dictio`` is a
        `dictionary<dict>` containing a list of keys that the
        parser successfully parsed, with values set to `True` if the parse
        was completed for that key.
        If the parse failed, then ``msg`` is populated with a further
        diagnosis of the reason for the parse failure.
        '''
        if not self._validate :
            return (False, self._dictio, "")
        else :
            if len(self._attributes) != len(self._dictio.keys()) :
                return (False, self._dictio, "# Values != # attributes, " +
                         '# attr: ' + str(len(self._attributes)) +
                         ', # keys: ' + str(len(self._dictio.keys())) +
                         ". attributes with the same name given in input ?")
            else :
                if python3:
                    dictio_items = iter(self._dictio.items())
                else:
                    dictio_items = self._dictio.iteritems()
                for (k, i) in dictio_items :
                    if i != True : return (False, self._dictio, "")
        return (True, self._dictio, "")


    def error(self, msg):
        self._errors.append(msg)

    def __str__(self):
        return "\n".join(self._errors)


#
# Classes to assist in parsing tabular data (since parsergen is not designed
# to do this):
#
# September 12 2009, Christian E. Hopps

# http://stackoverflow.com/questions/11301138/\
# how-to-check-if-variable-is-string-with-python-2-and-3-compatibility
try:
    basestring  # attempt to evaluate basestring
    def isstr(s):
        return isinstance(s, basestring)
except NameError:
    def isstr(s):
        return isinstance(s, str)

###############################################################################
# column_result_t base class.
###############################################################################
class column_result_t (object):
    """Superclass of table result parsers.

    The inheriting class should define an add_entries method that
    is called with the entry text. This method should add entries to
    the object.
    """

    field_mapping = { }
    """Dictionary of types indexed by field name indicating mappings for
    fields."""

    table_title_mapping = None
    """A possible list of mapping functions for table title value keys."""

    #------------------+
    # Abstract Methods
    #------------------+

    def add_entry (self, line, header_fields, field_delims):
        "Must be provided by concrete sub-class"
        assert False, "add_entry must be implemented by concrete sub-class"

    def get_init_info (self,
                       output,
                       header_fields,
                       table_terminal_pattern,
                       skip_header,
                       table_title_pattern,
                       right_justified,
                       label_fields,
                       skip_line):
        """Override this and pass None for header_fields to get called back
           with output"""
        assert False, "get_init_info must be overridden by concrete sub-class"

    #-----------------+
    # Regular Methods
    #-----------------+

    def compile_header_pattern (self, header_fields):
        "Compile a header pattern from the given header fields"
        #
        # Create the header regexp groups are as follows:
        # group  1:     prefix space,
        # group 2n:     header titles
        # group 2n + 1: following space

        # Initializing variables
        header_pattern = ""
        header_pattern_augment = ""
        multi_line_header = []
        self.multi_line = True

        def ordering_header (loop, pattern):
            header_pattern = pattern
            for field in loop:
                space = r"([ \t]*)("
                header_pattern += space + field + r")"
            return header_pattern

        # Handling the multiple line header case
        if all(isinstance(i, list) for i in header_fields):
            for lst in header_fields:
                header_pattern = ordering_header(
                    lst, header_pattern) + r"([ \n]*)"
        else:
            self.multi_line = False
            header_pattern = ordering_header(header_fields, header_pattern)

        header_pattern += r"[ \t]*[\n\r]+"
        return compile(header_pattern)

    def align_table (self, table_to_parse, header_fields, label_fields,
                     delimiter, right_justified):
        '''A function to align all the table fields before parsing operation'''

        # Initializing Variables
        # Maximum spaces to be added over the header fields assuring no overlap
        # between headers/table items
        maximum_spaces = 20

        # A list for a the temporary header fields
        temp_header_list = []

        # A list for a the final aligned rows
        aligned_row = []

        # A list for a temp aligned rows before adjusting as per the
        # longest header length
        temp_aligned_row = []

        # A list for a the final aligned header
        aligned_header = []

        # A list for a temp aligned header before adjusting as per the
        # longest header length
        temp_aligned_header = []

        # A list to collect the header list items length/len(item)
        header_length_list = []

        # A string to gather the final constructed table after alignment
        new_table = ''

        if delimiter == '':
            delimiter = '|'

        # Check for equal length header fields
        if self.multi_line:
            the_length = len(header_fields[0])
            for key in header_fields:
                if len(key) != the_length:
                    raise AttributeError("Header fields are not of the "
                                    "same length. Please provide equal "
                                    "length header fields")

        # Replacing empty header items with "header missing" keyword
        original_table_to_parse = table_to_parse

        # Support for python later versions
        # Changed in version 3.7: Unknown escapes in repl consisting of '\' and an ASCII letter now are errors.
        if delimiter == '\\s':
            delimiter = r'\\s'

        regex_substitute_from = r'{s}{k}{l}'.format(s = escape(delimiter),
                                                   k = r" +",
                                                   l = escape(delimiter))
        regex_substitute_to = r'{s}{k}{l}'.format(s = delimiter,
                                                 k = "header_missing",
                                                 l = delimiter)

        table_to_parse = sub(regex_substitute_from, regex_substitute_to,
                            table_to_parse)

        # Replacing delimiter with specific pattern "#_D_#"
        table_to_parse = table_to_parse.replace(delimiter,'#_D_#')
        rows = [line.strip().\
            split('#_D_#') for line in table_to_parse.split('\n')]

        # Checking tables' rows and classify them as header or table item row
        for itm in rows:
            def intersection_check(compare_text, compare_regexp):
                """ Compare a line from the text to parse with header regexp """

                intersect = set()
                for text,regexp in zip(compare_text, compare_regexp):
                    pattern = compile(regexp)

                    stripped_text = text.strip()

                    if pattern.match(stripped_text):
                        intersect.add(regexp)
                # Corner case here when second line of table header has only
                # one item that is a compensation for the case where header
                # field has same item as the row field.
                if len(intersect) >= 2:
                    temp_header_list.append(itm)

            # not search('   +', line) is placed to cover the corner case of
            # the tables who has delimiters only on the table header and not
            # on the table body
            if len(itm) == 1 and (not search('   +', itm[0])):
                continue
            else:
                # Append header items to the table header
                # Multi-header line table
                if self.multi_line:
                    if len(itm) == the_length + 1 and\
                        itm[0] == '':
                        temp_itm = [i for i in itm if i != '']
                        temp_itm = [''] + temp_itm
                    else:
                        temp_itm = [i for i in itm if i != '']
                    for header in header_fields:
                        intersection_check(temp_itm, header)
                else:
                    # Single-header line table
                    temp_itm = [i for i in itm if i != '']
                    intersection_check(temp_itm, header_fields)

                # Append non-header items to the table rows
                if itm not in temp_header_list:
                    for row_item in itm:
                        if row_item != '':
                            temp_aligned_row.append(row_item)
                    temp_aligned_row.append('new_line')

        # Getting headers length
        for hdr in temp_header_list:
            for itm in hdr:
                if itm !='':
                    temp_aligned_header.append(itm)
                    if hdr == temp_header_list[0]:
                        header_length_list.append(len(itm))
            temp_aligned_header.append('new_line')

        # Setting the table field length
        if header_length_list:
            max_header_field = max(header_length_list) + maximum_spaces

            # Start aligning header elements
            for item in temp_aligned_header:
                if right_justified:
                    aligned_header.append(item.rstrip().rjust(max_header_field))
                else:
                    aligned_header.append(item.lstrip().ljust(max_header_field))

            # Start aligning row elements
            for item in temp_aligned_row:
                if right_justified:
                    aligned_row.append(item.rstrip().rjust(max_header_field))
                else:
                    aligned_row.append(item.lstrip().ljust(max_header_field))

            # Placing delimiter back in the table
            aligned_header = [(delimiter.join(aligned_header))]
            aligned_header = aligned_header.pop()

            if right_justified:
                aligned_header = sub(r"(\s)+new_line+","\n",aligned_header)
            else:
                aligned_header = sub(r"new_line(\s)+","\n",aligned_header)

            aligned_header = aligned_header.replace('header_missing',
                                                    ' '*max_header_field)

            # Placing delimiter back in the table
            aligned_row = [(delimiter.join(aligned_row))]
            aligned_row = aligned_row.pop()

            if right_justified:
                aligned_row = sub(r"(\s)+new_line","\n",aligned_row)
                aligned_row = sub(r"(\s)+header_missing",
                    ' '*max_header_field, aligned_row)
            else:
                aligned_row = sub(r"new_line(\s)+","\n",aligned_row)
                aligned_row = sub(r"header_missing(\s)+",
                    ' '*max_header_field, aligned_row)

            # Reconstructing the table with separators
            new_table = '{s}{k}+----+\n{l}{j}\n'.format(
                s = delimiter,
                k = aligned_header,
                l = delimiter,
                j = aligned_row)
            return new_table
        else:
            return original_table_to_parse

    def __init__ (self,
                  header_fields,
                  table_terminal_pattern,
                  skip_header,
                  table_title_pattern = None,
                  right_justified = False,
                  label_fields = None,
                  skip_line = None,
                  parse_key = '',
                  delimiter=''):

        self.entrydict = {}
        """For multiple tables results values keyed on match groups from
           table_title_pattern regex."""

        #
        # If header_fields is None call sub-class to get init info,
        # pass in the command output, this allows the sub-class to
        # try different patterns
        #
        if header_fields == None:
            (header_fields,
             table_terminal_pattern,
             skip_header,
             table_title_pattern,
             right_justified,
             label_fields,
             skip_line) = self.get_init_info(text_to_parse[parse_key],
                                             header_fields,
                                             table_terminal_pattern,
                                             skip_header,
                                             table_title_pattern,
                                             right_justified,
                                             label_fields,
                                             skip_line)

        header_search = self.compile_header_pattern(header_fields)

        if table_title_pattern:
            new_table = ''
            table_title = ''
            originale_table_title = []
            out = text_to_parse[parse_key]
            self._text_to_parse = ''
            all_tables = {}
            for line in out.splitlines():
                end_of_table_pattern = \
                    compile(r'(?P<Title>[^/\s]+/[^/\s]+/[^/\s]+/\S+)\s*#$')
                if (line == '') or (end_of_table_pattern.match(line)) or\
                    '---' in line:
                    continue
                p1 = compile(table_title_pattern)
                m = p1.match(line)
                if m:
                    table_title = m.string
                    all_tables[table_title] = []
                if table_title and (line != table_title):
                    all_tables[table_title].append(line)
                    all_tables[table_title].append('\n')
            for key in all_tables.keys():
                lst_to_str = ''.join(all_tables[key])
                multiple_table = self.align_table(lst_to_str,
                                                  header_fields,
                                                  label_fields,
                                                  delimiter,
                                                  right_justified)
                multiple_table = '{f}\n{z}'.format(f=key, z= multiple_table)
                self._text_to_parse += multiple_table
        else:
            self._text_to_parse = self.align_table(text_to_parse[parse_key],
                                                   header_fields,
                                                   label_fields,
                                                   delimiter,
                                                   right_justified)

        # Get rid of tabs in output
        self._text_to_parse = self._text_to_parse.expandtabs()

        # Get rid of table delimiters prior to parsing
        if self.multi_line:
            if delimiter == '':
                delimiter = '|'

        self._text_to_parse = self._text_to_parse.replace(delimiter,'')

        if label_fields == None:
            if self.multi_line:
                label_fields = []
                if len(header_fields) == 2:
                    for x,y in zip(header_fields[0],header_fields[1]):
                        new_string = '{f} {z}'.format(f=x, z= y)
                        new_string = new_string.replace('\\', '')
                        label_fields.append(new_string)
                else:
                    for x,y,z in zip(
                        header_fields[0],header_fields[1],header_fields[2]):
                        new_string = '{f} {l} {k}'.format(f=x, l= y, k=z)
                        new_string = new_string.replace('\\', '')
                        label_fields.append(new_string)
            else:
                label_fields = header_fields

        if table_title_pattern:
            mtable_search = compile(table_title_pattern)
        else:
            mtable_search = None

        prevheaderend = 0
        # Support the case when device output contains "\r\n"
        self._text_to_parse = \
            self._text_to_parse.replace("\r\n", "\n")
        self._text_to_parse += '\n'

        for m in header_search.finditer(self._text_to_parse):
            startpos = m.end(0)
            #
            # Goto the next header to find the end.
            #
            m2 = header_search.search(self._text_to_parse, startpos)
            if m2 == None:
                endpos = len(self._text_to_parse)
            else:
                endpos = m2.start(0)

            #
            # Get the field delims
            #
            prevend = 0
            if right_justified:
                field_delims = []
                prevend = 0
                for j in range(1, len(header_fields) * 2, 2):
                    spc = m.group(j)
                    hdr = m.group(j + 1)
                    field_delims.append((prevend, prevend + len(hdr) + \
                        len(spc)))
                    prevend = field_delims[-1][1]
            else:
                try:
                    next_col_preceding_whitespace = len(m.group(3))
                except IndexError:
                    next_col_preceding_whitespace = 0
                field_delims = [ (0, len(m.group(1)) + len(m.group(2)) + \
                    next_col_preceding_whitespace) ]
                prevend = field_delims[-1][1]
                if self.multi_line:
                    headers_length = len(header_fields[0])
                else:
                    headers_length = len(header_fields)
                for j in range(4, headers_length * 2 + 1, 2):
                    hdr = m.group(j)
                    if j + 1 < len(m.groups()):
                        spc = m.group(j + 1)
                    else:
                        spc = ''
                    field_delims.append((prevend, prevend + len(hdr) + \
                        len(spc)))
                    prevend = field_delims[-1][1]

            if skip_header:
                skip_pattern = compile(skip_header + r".*\n")
                sm = skip_pattern.search(self._text_to_parse, startpos)
                if not sm:
                    continue
                startpos = sm.end(0)

            #
            # Get the entries
            #
            entry_pattern = compile(r".*\n")
            # entry_output = self._text_to_parse[startpos:endpos]



            for em in entry_pattern.finditer(\
                    self._text_to_parse, startpos, endpos):
                # If we have a terminal pattern look for it
                if table_terminal_pattern:
                    tpm = search(table_terminal_pattern, em.group(0))
                    if tpm:
                        endpos = startpos + tpm.end(0)
                        break

                # we also terminate the table if we see the title pattern
                if table_title_pattern:
                    tpm = search(table_title_pattern, em.group(0))
                    if tpm:
                        endpos = startpos + tpm.end(0)
                        break

                # skip any line without letters or digits in it, this
                # should skip table graphics
                #
                if not search(r"[a-zA-Z0-9]+", em.group(0)):
                    continue

                #
                # Skip any line that matches skip_line
                #
                if skip_line and search(skip_line, em.group(0)):
                    continue

                eline = em.group(0).rstrip()
                self.add_entry(eline, label_fields, field_delims)

            #
            # Now search in between the last end and the header fields for
            # a title match.
            #
            if mtable_search:
                mhmoutput = self._text_to_parse[prevheaderend:startpos]
                mhm = mtable_search.search(mhmoutput)
                if mhm:
                    self._add_entries_to_results(mhm.groups())
                prevheaderend = endpos
        if len(self.entrydict):
            self.entries = self.entrydict

    def _add_entries_to_results (self, titlevalues):
        """Use list of TITLEVALUES to index a multi-dim dictionary to store
           latest self.entries."""
        td = self.entrydict
        tend = len(titlevalues) - 1
        for i, tv in enumerate(titlevalues):
            if self.table_title_mapping != None:
                tv = self.table_title_mapping[i](tv)
            if i == tend:
                if tv in td:
                    warning(\
                      "Warning non-unique result found table title keys " +
                      str(titlevalues) + " in " + str(self))
                td[tv] = self.entries
            elif tv in td:
                td = td[tv]
            else:
                td[tv] = dict()
                td = td[tv]

        etype = type(self.entries)
        self.entries = etype()

    def _map_entry_field (self, header, field):
        """Map the field value based on the header field name

        This function uses class dictionary variable ``field_mapping`` to
        lookup a type (value) based on the header field name (key). If found
        that type is passed the field value and the resulting object is used
        in the results.

        Allowed types: function, method, or [ function_or_method, *args ]
        """
        #logger.debug (" _map_entry_field header={}, field={}".\
        #    format(header, field))
        if header in self.field_mapping and \
                self.field_mapping[header] is not None:
            mapper = self.field_mapping[header]
            if type(mapper) == type(self._map_entry_field):
                return mapper(field)
            elif inspect.ismethod(mapper):
                return mapper(self, field)
            if type(mapper) is list:
                mlist = mapper
                mapper = mlist[0]
                mlist = mlist[1:]
                if inspect.ismethod(mapper):
                    return mapper(self, field, *mlist)
                else:
                    return mapper(field, *mlist)
            else:
                return mapper(field)
        return field

    def cleanup_entry_field (self, header, field):
        """Override this method to cleanup or coerce any field.

        If the field is not going to be an index field then you can
        additionally coerce the type to any type you wish (i.e., non-sorting)
        """
        return field

    def _find_entry_in_list (self, regex, entries):
        for ent in entries:
            self.last_find_match = search(regex, ent[0])
            if self.last_find_match != None:
                return ent
        return None

    def find_entry_index_list (self, index_list):
        """Find an entry given a list of indices. Return None if not there."""
        edict = self.entries
        for index in index_list:
            if index not in edict:
                return None
            edict = edict[index]
        return edict


###############################################################################
# column_table_result_core_t base class.
###############################################################################
class column_table_result_core_t (column_result_t):
    """Class that parses tabular "show" command output.


    `Example`::

        from genie.parsergen import core
        parsergen.core.text_to_parse[''] = '''
        RP/0/0/CPU0:one#show rib clients
        Thu Sep 17 11:41:18.164 EDT
        Process              Location         Client ID  Redist   Proto
        bcdl_agent           node0_0_CPU0     0          insync   no
        '''

        from genie.parsergen.core import column_table_result_core_t
        res = column_table_result_core_t(
            ["Process", "Location", "Client ID", "Redist", "Proto"])
        print res.entries['bcdl_agent']['Location']

    will print ``node0_0_CPU0`` ::

     parsergen.core.text_to_parse[''] = '''
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

     res = column_table_result_core_t ( header_fields=
                                   ["System Id", "Metric", "Next-Hop",
                                    "Interface", "SNPA"],
                                  index=[0,3])
     print res.entries['three']['Gi0/0/0/1']['SNPA']

    will print ``02db.ebba.ecc4`` ::

        print res.entries['one']['']['Metric']

    will print ``--``

    .. note:: The tabular parsing behavior may be customized via
        :ref:`subclassing<parsergen.core-non-tabular-parser-subclass-example>`.
    """

    index_objects = True
    '''If True then mapped index fields will be used for keys (default).'''

    index_mapped_string = False
    '''If True then the __str__ of mapped index fields will be used for keys'''

    def __init__ (self,
                  header_fields = None,
                  table_terminal_pattern = None,
                  index = 0,
                  skip_header = None,
                  table_title_pattern = None,
                  right_justified = False,
                  label_fields = None,
                  skip_line = None,
                  parse_key = '',
                  delimiter = ''):
        """Creates an object to parse tabular "show" command output.

        Returns
        -------

          Parsed results are obtained by using the column positions of the
          header field. The entry starts with the column of the first header
          character and ends just prior to the next header column.

          The object returned has a dictionary named ``entries`` which is
          keyed by the entry value corresponding to the header at `index`.
          Each key in ``entries`` is indexed by the corresponding
          `header_fields` name (or `label_fields` name if specified).

        Parameters
        ----------
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
            If `True`, then the header labels are considered right justified.
            Defaults to `False`.

        label_fields : `list` of `str`
            If specified, then the ``entries`` object will contain these keys
            instead of those specified in `header_fields`.  There must be a
            corresponding entry in `label_fields` for each entry in
            `header_fields`.

        skip_line :  `str`
            If specified, then any line matching this pattern will be skipped.

        parse_key : `str`
            Key to identify the tabular textual output to parse.  The text to
            parse is expected to be populated in
            ``parsergen.core.text_to_parse[parse_key]``.  For example, this field
            could be set to the router name.  Defaults to `''` (empty string).

        delimiter :  `str`
            Table delimiter pattern that allows for columns' borders
            identification.
        """

        self.entries = {}
        '''A dictionary containing the results of the show command.'''

        if isinstance(index, int):
            self.index = [ index ]
        elif isinstance(index, list):
            self.index = index
        else:
            raise ValueError(str(index) + " is not an int or list of ints")

        column_result_t.__init__(self,
                                 header_fields,
                                 table_terminal_pattern,
                                 skip_header,
                                 table_title_pattern,
                                 right_justified,
                                 label_fields,
                                 skip_line,
                                 parse_key,
                                 delimiter)

    def add_entry (self, line, header_fields, field_delims):
        #logger.debug("line={}, header_fields={}, field_delims={}".\
        #    format(line, header_fields, field_delims))
        fields = {}
        indexfields = [""] * len(self.index)
        lastheader = len(header_fields) - 1
        for i, hdr in enumerate(header_fields):
            if i == lastheader:
                field = line[field_delims[i][0]:]
            else:
                field = line[field_delims[i][0]:field_delims[i][1]]
            field = field.strip()
            field = self.cleanup_entry_field(hdr, field)
            mappedfield = self._map_entry_field(hdr, field)
            if i in self.index:
                # If the mapped field name has a cmp and hash function use it
                # as index
                #
                # if the mapped field name is still a string use it as index
                #
                if (self.index_objects and
                    hasattr(mappedfield, '__cmp__') and
                    hasattr(mappedfield, '__hash__')):
                    indexfields[self.index.index(i)] = mappedfield
                elif isstr(mappedfield):
                    indexfields[self.index.index(i)] = mappedfield
                elif self.index_mapped_string and \
                        hasattr(mappedfield, '__str__'):
                    indexfields[self.index.index(i)] = str(mappedfield)
                else:
                    indexfields[self.index.index(i)] = field
            fields[hdr] = mappedfield

        #
        # now enter the result creating dicts as needed.
        #
        cdict = self.entries
        lastindex = len(indexfields) - 1
        for i, indexfield in enumerate(indexfields):
            if indexfield in cdict:
                if i == lastindex:
                    #warning(
                    # "Warning non-unique result found for keys " +
                    # str(indexfields) +
                    #                  " in " + str(self))
                    cdict[indexfield] = fields
                else:
                    cdict = cdict[indexfield]
            elif i == lastindex:
                cdict[indexfield] = fields
            else:
                cdict[indexfield] = dict()
                cdict = cdict[indexfield]
