import os
import json
import logging
import importlib
import shutil
import re
from tqdm import tqdm
from genie.libs import parser

from genie.conf import Genie
from pyats.cli.base import Command
from genie.abstract import Lookup
from genie.utils.config import Config
from genie.utils.summary import Summary
from unicon.logs import UniconFileHandler
from genie.conf.base.device import CONFIG_CMDS
from genie.libs.parser.utils import get_parser_exclude, get_parser
from pyats.aetest.utils import format_filter_exception
from genie.metaparser.util.exceptions import SchemaEmptyParserError

from unicon.core.errors import ConnectionError


log = logging.getLogger(__name__)

class ParserCommand(Command):
    '''
    Command to parse device show commands
    '''

    name = 'parse'
    help = 'Command to parse show commands'
    description = '''
Parse CLI commands into Pythonic datastructures
    '''
    usage = '''{prog} [commands] [options]

Example
-------
  {prog} "show interfaces" --testbed-file /path/to/testbed.yaml --devices uut
  {prog} "show interfaces" --testbed-file /path/to/testbed.yaml --devices uut --output my_parsed_output/
  {prog} "show interfaces" "show version" --testbed-file /path/to/testbed.yaml --devices helper
'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parser.add_argument('commands',
                                 type=str,
                                 metavar = 'COMMANDS',
                                 nargs='*',
                                 help='Show command(s) to parse, all can instead '
                                      'be provided to parse all commands')

        self.parser.add_argument('--testbed-file',
                                 help='specify testbed_file yaml',
                                 required = True,
                                 type=str)

        self.parser.add_argument('--devices',
                                 type=str,
                                 nargs='*',
                                 help='Devices to issue commands to')

        self.parser.add_argument('--output',
                                 help='Directory to store output files to.\n'
                                      'When not provided, prints parsed JSON '
                                      'output to screen. (Optional)')

        self.parser.add_argument('--via',
                                 nargs='*',
                                 help='List of connection to use per device "nxos-1:ssh"')

        self.parser.add_argument('--fuzzy',
                                action='store_true',
                                help = 'Enable fuzzy matching for commands')

        self.parser.add_argument('--raw',
                                 action='store_true',
                                 help='Store device output without parsing it')

        self.parser.add_argument('--timeout',
                                 type=int,
                                 help='Devices execution timeout')

        self.parser.add_argument('--developer',
                                 action='store_true',
                                 help='Parser coloured developer mode')

        self.parser.add_argument('--archive-dir',
                                 type = str,
                                 metavar = '',
                                 dest = 'archive_dir',
                                 help = 'Directory to store a .zip of the output')

        self.parser.add_argument('--learn-hostname',
                                 action='store_true',
                                 help='Learn the device hostname during connection (Optional)')

        self.parser.add_argument('--learn-os',
                                 action='store_true',
                                 help='Learn the device OS during connection (Optional)')

        self.parser.add_argument('--rest',
                                 action='store_true',
                                 help='run rest commands')

    def parse_args(self, argv):
        # inject general group options
        self.add_general_opts(self.parser)

        # do the parsing
        args, unknown = self.parser.parse_known_args(argv)
        import sys
        sys.argv = sys.argv[:1]+unknown
        return args

    def run(self, args):
        self.raw = args.raw
        self.timeout = args.timeout
        self.fuzzy = args.fuzzy
        self.rest = args.rest

        # are we saving to dir
        directory = args.output
        archive_dir = args.archive_dir

        if args.developer:
            import genie.gre
        global re
        import re

        mod = importlib.import_module('genie.libs.parser')
        connection_logs = None
        # Find json file
        parsers = os.path.join(mod.__path__[0], 'parsers.json')

        # Make sure it exists
        if not os.path.isfile(parsers):
            raise Exception('parsers.json does not exists, make sure you '
                            'are running with latest version of '
                            'genie.libs.parsers')


        # Open all the parsers in json file
        with open(parsers) as f:
            data = json.load(f)

        via_args = args.via if args.via else []
        # Convert to dict
        self.vias = {}
        for device_via in via_args:
            device, via = device_via.split(':')
            self.vias[device] = via

        # Create Genie Tb
        testbed = Genie.init(args.testbed_file)

        # Get devices or defaults
        devices = args.devices if args.devices else testbed.devices

        for device_name in devices:
            connection_failed = False
            commands = args.commands.copy()
            try:
                device = testbed.devices[device_name]
            except Exception:
                raise Exception("Could not find device '{d}' in Testbed "
                                "file".format(d=device_name))

            if directory:
                os.makedirs(directory, exist_ok=True)

                summary = Summary("Genie {prog_name} Summary for {d}"
                                  .format(prog_name='Execute' if self.raw else 'Parse', d=device.name), 80)
            else:
                summary = None

            connection_kwargs = {
                'log_stdout': False,
                'learn_hostname': args.learn_hostname,
                'learn_os': args.learn_os
            }

            if directory:
                connection_logs = '{d}/connection_{device}.txt'.format(d=directory,
                                                     device=device.name)
                connection_kwargs.update(logfile=connection_logs)

            if self.loglevel < logging.INFO:
                connection_kwargs.update(log_stdout = True)

            if device.name in self.vias:
                connection_kwargs['via'] = self.vias[device.name]
            elif device.alias in self.vias:
                connection_kwargs['via'] = self.vias[device.alias]

            connection_kwargs.update({'init_config_commands': []})

            if self.rest:

                device.log = logging.getLogger('rest.connector.libs.apic.implementation')

                if connection_logs:
                    fh = logging.FileHandler(connection_logs)
                    device.log.addHandler(fh)
                    device.log.propagate = False

            try:
                device.connect(**connection_kwargs)
            except ConnectionError:
                connection_failed = True

            # Set device execution timeout
            if self.timeout:
                device.execute.timeout = self.timeout

            if summary:
                if connection_failed:
                    summary.add_message(' Failed to connect to {d}'.format(d=device.name))
                else:
                    summary.add_message(' Connected to {d}'.format(d=device.name))
                summary.add_message(' -  Log: {log}'.format(log=connection_logs))
                summary.add_sep_line()

            if len(commands) == 1 and commands[0] == 'all':
                # Remove all commands which contains { as this requires
                # extra kwargs which cannot be guessed dynamically
                # Remove the one that arent related to this os
                commands = self._filter_all_commands(data, device)

            if self.loglevel > logging.INFO:
                commands = commands
            else:
                commands = tqdm(commands)

            for command in commands:
                try:
                    data = get_parser(command, device, fuzzy=self.fuzzy)
                except Exception as e:
                    # Could not find a match
                    msg = "Could not find parser for '{c}'".format(c=command)
                    msg += "\n\nDetails:\n{d}".format(d=str(e))
                    if not self.rest:
                        if summary:
                            summary.add_message(msg)
                            summary.add_sep_line()
                        else:
                            log.error(msg)
                        continue

                if self.fuzzy:
                    for datum in data:
                        found_command, found_data, kwargs = datum

                        for key, value in kwargs.items():
                            found_command = found_command.replace('{' +
                                key + '}', value)

                        self.parse(found_data, device, directory, found_command,
                                            summary, args.developer, kwargs)
                elif self.rest:
                    self.parse('', device, directory, command, summary)
                else:
                    self.parse(data[0], device, directory, command,
                                            summary, args.developer, data[1])

            if summary:
                summary.print()

        if directory and archive_dir:
            # Copy output directory to this location
            archive = os.path.join(archive_dir, 'snapshot')
            log.info("Creating archive file: {a}.zip".format(a=archive))
            shutil.make_archive(archive, 'zip', directory)

    def _filter_all_commands(self, data, device):
        commands = []
        for command, values in data.items():
            if '{' in command or command == 'tokens' or device.os not in values:
                continue
            commands.append(command)
        return commands

    def parse(self, data, device, directory, command, summary, developer=None, kwargs=None):
        # See if right abstraction exists
        if kwargs is None:
            kwargs = {}

        console_logs = '{d}/{device}_{cmd}_console.txt'.format(
                                                   d=directory,
                                                   cmd=command.replace(' ', '-').replace('/', '-').replace('|','pipe'),
                                                   device=device.name)

        if not self.raw:
            parsed_logs = '{d}/{device}_{cmd}_parsed.txt'.format(
                                                       d=directory,
                                                       cmd=command.replace(' ', '-').replace('/', '-').replace('|','pipe'),
                                                       device=device.name)

        backup_handlers = log.root.handlers.copy()
        backup_device_handler = device.log.handlers.copy()

        if self.loglevel > logging.INFO:
            device.log.handlers = []
            log.root.handlers = []

        if directory:

            # Create new filehandler
            # And add to root logger and device (Unicon use its own handler for some
            # reason)
            fh = logging.FileHandler(console_logs)
            fh.setLevel(logging.INFO)
            log.root.addHandler(fh)
            log.root.setLevel(logging.INFO)

            if self.rest:

                exisiting_fh = device.log.handlers[0]
                exisiting_fh.close()
                device.log.removeHandler(exisiting_fh)
                device.log.addHandler(fh)
                device.log.setLevel(logging.INFO)
            else:
                fh = UniconFileHandler(console_logs, 'w+')
                fh.setLevel(logging.INFO)
                device.log.addHandler(fh)
                device.log.setLevel(logging.INFO)
        try:
            if self.raw:
                output = device.execute(command)
            elif self.rest:
                output = device.get(command)
            else:
                if command in CONFIG_CMDS:
                    output = device.api.get_running_config_dict()
                else:
                    output = device.parse(command)
        except SchemaEmptyParserError:
            if summary:
                # That's okay
                summary.add_message(" Parsed command '{c}' but it returned "
                                    "empty".format(c=command))
                summary.add_message(' -  Device Console: {l}'
                                    .format(l=console_logs))
                summary.add_sep_line()
            else:
                log.error(" Parsed command '{c}' but it returned "
                                    "empty".format(c=command))
            return
        except Exception as e:
            # That's not okay!
            if summary:
                exception_file = '{d}/{device}_{cmd}_exception.txt'.format(
                                                   d=directory,
                                                   cmd=command.replace(' ', '-').replace('/', '-').replace('|','pipe'),
                                                   device=device.name)

                summary.add_message(" Could not {prog_name} '{c}'".format(prog_name='execute' if self.raw else 'parse',
                                                                          c=command))
                summary.add_message(' -  Exception:      {l}'
                                    .format(l=exception_file))

                if device.os == 'generic':
                    summary.add_message(" -  Mandatory field 'os' was "
                                        "not given in the yaml file")
                else:
                    summary.add_message(' -  Device Console: {l}'
                                        .format(l=console_logs))
                summary.add_sep_line()
                msg = 'Issue with the {prog_name} {cls}\n\n'.format(prog_name='show command' if self.raw else 'parser',
                                                                    cls=command)
                with open(exception_file, 'w') as f:
                    f.write(msg)
                    f.write(format_filter_exception(exc_type=type(e),
                                                    exc_value=e,
                                                    tb=e.__traceback__))
            else:
                log.exception('Issue with the {prog_name} {cls}\n\n'.format(prog_name='show command' if self.raw else 'parser',
                                                                            cls=command))
            return

        finally:
            # Put back logger
            log.root.handlers = backup_handlers
            device.log.handlers = backup_device_handler


        # add summary
        if summary:
            # If developer mode, than change file console for coloured output
            if developer:
                file_name, ext = console_logs.split('.')
                dev_file = os.path.join(file_name+'_dev.')+ext
                with open(dev_file, 'w') as f:
                    f.write(re.colour_output())
                    f.write('\nDeveloper percentage: {p}'.format(p=re.percentage()))
                re.reset()

            summary.add_message(" {prog_name} command '{c}'".format(prog_name='Executed' if self.raw else 'Parsed',
                                                                    c=command))
            if not self.raw:
                summary.add_message(' -  Parsed structure: {l}'
                                    .format(l=parsed_logs))
                if developer:
                    summary.add_message(' -  Developer console: {l}'
                                        .format(l=dev_file))
            summary.add_message(' -  Device Console:   {l}'
                                .format(l=console_logs))
            summary.add_sep_line()

        if self.raw:
            if not directory:
                print(output)

        else:
            # Add metadata in the output
            if directory and data:
                # This is useful for the Diff functionality, need to know exclude keys
                try:
                    output['_exclude'] = get_parser_exclude(command, device)
                except Exception:
                    output['_exclude'] = []
            try:
                formatted_json = json.dumps(output,
                                            sort_keys=True,
                                            indent=2,
                                            separators=(',', ': '))
            except Exception:
                formatted_json = json.dumps(json.loads(json.dumps(output)),
                                            sort_keys=True,
                                            indent=2,
                                            separators=(',', ': '))

            if directory:
                with open(parsed_logs, 'w') as f:
                    f.write(formatted_json)
            else:
                print(formatted_json)
