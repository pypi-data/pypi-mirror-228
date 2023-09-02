import os
import json
import shutil
import logging
from tqdm import tqdm
from itertools import product
from genie.ops.utils import get_ops, get_ops_exclude
from collections import OrderedDict
from genie.libs import ops as OpsDir
from pyats.aetest.utils import format_filter_exception

from pyats.cli.base import Command

# import pcall
import importlib
try:
    pcall = importlib.import_module('pyats.async').pcall
except ImportError:
    from pyats.async_ import pcall
# # import pcall
# from pyats.async import pcall

from genie.conf import Genie
from genie.utils.config import Config
from genie.utils.summary import Summary


from unicon.logs import UniconFileHandler
from unicon.core.errors import ConnectionError


# internal logger
log = logging.getLogger(__name__)
EXCLUDE_OPS = ['__init__.py', '__pycache__', 'tests', 'vxlan_consistency']


class LearnCommand(Command):
    '''
    Command to learn Ops object and save to file
    '''

    name = 'learn'
    help = 'Command to learn device features and save to file'
    description = '''
Learn device feature and parse into Python datastructures

    List of available features: https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/models'''

    usage = '''{prog} [commands] [options]

Example
-------
  {prog} ospf --testbed-file /path/to/testbed.yaml
  {prog} ospf --testbed-file /path/to/testbed.yaml --output features_snapshots/ --devices "nxos-osv-1"
  {prog} ospf config interface bgp platform --testbed-file /path/to/testbed.yaml --output features_snapshots/
'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parser.add_argument('ops',
                                 type=str,
                                 nargs='*',
                                 help='List of Feature to learn, comma '
                                      'separated, ospf,bgp ; all can instead '
                                      'be provided to learn all features')
        self.parser.add_argument('--testbed-file',
                                 help='specify testbed_file yaml',
                                 type=str)
        self.parser.add_argument('--devices',
                                 nargs='*',
                                 help='"DEVICE_1 DEVICE_2", space'
                                      'separated, if not provided '
                                      'it will learn on '
                                      'all devices (Optional)')
        self.parser.add_argument('--output', default='.',
                                 help='Which directory to store logs, by '
                                      'default it will be current directory (Optional)')
        self.parser.add_argument('--single-process',
                                 action='store_true',
                                 help='Learn one device at the time instead of in parallel (Optional)')
        self.parser.add_argument('--via',
                                 nargs='*',
                                 help='List of connection to use per device "nxos-1:ssh"')
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

    def parse_args(self, argv):
        # inject general group options
        self.add_general_opts(self.parser)

        # do the parsing
        args, unknown = self.parser.parse_known_args(argv)
        import sys
        sys.argv = sys.argv[:1]+unknown
        return args

    def run(self, args):

        if not args.testbed_file:
            raise Exception('No --testbed-file provided, genie learn --help '
                            'for usage')

        if not args.ops:
            raise Exception('No feature provided, genie learn --help for usage')

        testbed = Genie.init(args.testbed_file)
        devices = args.devices if args.devices else testbed.devices
        archive_dir = args.archive_dir

        via_args = args.via if args.via else []
        # Convert to dict
        self.vias = {}
        for device_via in via_args:
            device, via = device_via.split(':')
            self.vias[device] = via


        directory = args.output
        os.makedirs(directory, exist_ok=True)
        single = args.single_process
        learn_hostname = args.learn_hostname
        learn_os = args.learn_os

        self._learn_ops(args.ops, devices, directory, testbed,
                        single, learn_hostname, learn_os)

        if directory != '.' and archive_dir:
            # Copy output directory to this location
            archive = os.path.join(archive_dir, 'snapshot')
            log.info("Creating archive file: {a}.zip".format(a=archive))
            shutil.make_archive(archive, 'zip', directory)

    def _learn_ops(self, ops_list, devices, directory, testbed, single,
                   learn_hostname, learn_os):
        '''Learn OPS' features on multiple devices'''
        if len(ops_list) == 1 and ops_list[0] == 'all':
            # Figure out what to learn
            # Not supported yet
            ops_location = OpsDir.__file__
            ops_location = os.path.dirname(OpsDir.__file__)
            ops_list = []
            # We do this to only get the first level,  non recursive
            root, dirs, files = next(os.walk(ops_location))
            for dir_ in sorted(dirs):
                if dir_ in EXCLUDE_OPS:
                    continue
                ops_list.append(dir_)
            ops_list.append('config')

        log.info("\nLearning '{o}' on devices "\
                 "'{d}'".format(o=ops_list, d=list(devices)))

        summary_table = OrderedDict()
        devices_obj = []
        for device in devices:
            if device in testbed.devices:
                dev = testbed.devices[device]
                kwargs = {}
                if dev.name in self.vias:
                    kwargs['via'] = self.vias[dev.name]
                elif dev.alias in self.vias:
                    kwargs['via'] = self.vias[dev.alias]

                # Store log of connection to a different file
                logfile = '{d}/connection_{device}.txt'.format(d=directory,
                                                               device=device)
                try:
                    devices_obj.append(dev)
                    dev.connect(log_stdout=False,
                                logfile=logfile,
                                init_config_commands=[],
                                learn_hostname=learn_hostname,
                                learn_os=learn_os,
                                **kwargs)
                    summary_table[dev.name] = OrderedDict({'connected': logfile})
                except ConnectionError:
                    summary_table[dev.name] = OrderedDict({'not_connected': logfile})
            else:
                # Decision to take - Right now its a very friendly tool.
                # Should it crash? I think staying friendly is the right way to
                # do it
                summary_table[dev.name] = OrderedDict({'connected': False})

        # If no devices exists
        if not devices_obj:
            log.error('No devices provided exists')
            return

        for ops in tqdm(ops_list):
            if single:
                output = []
                for device in devices_obj:
                    output.append(self._retrieve_ops(device, ops, directory))
            else:
                output = pcall(self._retrieve_ops, iargs = product(devices_obj,
                                                                   [ops],
                                                                   [directory]))


            for item in output:
                ops_file, console_file, exception_file, device = item

                summary_table[device][ops] = OrderedDict()
                summary_table[device][ops]['console'] = console_file
                summary_table[device][ops]['ops'] = ops_file
                summary_table[device][ops]['exception'] = exception_file

        for device, data in summary_table.items():
            # Report nicely
            summary = Summary('Genie Learn Summary for device {d}'
                              .format(d=device), 80)

            if 'connected' in data:
                if data['connected']:
                    summary.add_message(' Connected to {d}'.format(d=device))
                    summary.add_message(' -   Log: {log}'.format(log=data['connected']))
                else:
                    summary.add_message(" Device '{d}' does not exist in the "
                                        " Testbed file".format(d=device))
            if 'not_connected' in data:
                summary.add_message(' Failed to connect to {d}'.format(d=device))
                summary.add_message(' -   Log: {log}'.format(log=data['not_connected']))

            summary.add_sep_line()

            for i, items in enumerate(data.items()):
                ops, info = items
                if ops == 'connected' or ops == 'not_connected':
                    continue

                if info['exception']:
                    # Could not learn this feature
                    summary.add_message(" Could not learn feature '{o}'".format(o=ops))
                    if info['exception']:
                        summary.add_message(' -  Exception:      {l}'
                                            .format(l=info['exception']))
                    if info['ops'] is None and info['console'] is None:
                        dev = testbed.devices[device]
                        if dev.os == 'generic':
                            summary.add_message(" -  Mandatory field 'os' was "
                                                "not given in the yaml file")
                        else:
                            summary.add_message(" -  Feature not yet developed for this os")
                        if not i == len(data)-1:
                            summary.add_sep_line()
                        continue
                else:
                    summary.add_message(" Learnt feature '{o}'".format(o=ops))

                summary.add_message(' -  Ops structure:  {l}'
                                    .format(l=info['ops']))
                summary.add_message(' -  Device Console: {l}'
                                    .format(l=info['console']))
                if not i == len(data)-1:
                    summary.add_sep_line()
            summary.add_subtitle_line()
            summary.print()
            log.info('\n')


    def _retrieve_ops(self, device, feature, directory):

        # Remove current handler, so it doesnt print to screen
        # Add handler to unicon
        # Create directory if doesnt exists
        console_file_name = "{dir}/{o}_{do}_{dn}_console.txt"\
                                .format(o=feature,
                                        do=device.os,
                                        dn=device.name,
                                        dir=directory)

        # Save to file the structure
        ops_file_name = "{dir}/{o}_{do}_{dn}_ops.txt"\
                            .format(o=feature,
                                    do=device.os,
                                    dn=device.name,
                                    dir=directory)

        exception_file_name = None

        # Find right object
        if feature == 'config':
            # Remove all handlers
            # We want to print to a specific file,
            # as its a different fork
            backup_handlers = log.root.handlers
            device.log.handlers = []
            log.root.handlers = []

            # Create new filehandler
            # And add to root logger and device (Unicon use its own handler for some
            # reason)
            fh = logging.FileHandler(console_file_name)
            fh.setLevel(logging.INFO)
            log.root.addHandler(fh)
            log.root.setLevel(logging.INFO)

            fh = UniconFileHandler(console_file_name, 'w+')
            fh.setLevel(logging.INFO)
            device.log.addHandler(fh)
            device.log.setLevel(logging.INFO)
            config = device.api.get_running_config_dict()
        else:
            try:
                Ops = get_ops(feature, device)
            except LookupError as e:
                # Could not find library for this, so just return
                exception_file_name = "{dir}/{o}_{do}_{dn}_exception.txt"\
                                       .format(o=feature,
                                               do=device.os,
                                               dn=device.name,
                                               dir=directory)
                msg = '{f} is not yet developed for device '\
                      '{d}\n\n'.format(f=feature, d=device.name)
                with open(exception_file_name, 'w') as f:
                    f.write(msg)
                    f.write(format_filter_exception(exc_type=type(e),
                                                    exc_value=e,
                                                    tb=e.__traceback__))


                return (None, None, exception_file_name, device.name)

            # Remove all handlers
            # We want to print to a specific file,
            # as its a different fork
            backup_handlers = log.root.handlers
            device.log.handlers = []
            log.root.handlers = []

            # Create new filehandler
            # And add to root logger and device (Unicon use its own handler for some
            # reason)
            fh = logging.FileHandler(console_file_name)
            fh.setLevel(logging.INFO)
            log.root.addHandler(fh)
            log.root.setLevel(logging.INFO)

            fh = UniconFileHandler(console_file_name, 'w+')
            fh.setLevel(logging.INFO)
            device.log.addHandler(fh)
            device.log.setLevel(logging.INFO)



        if feature == 'config':
            log.root.handlers = backup_handlers
            with open(ops_file_name, 'w') as f:
                f.write(json.dumps(config, sort_keys=True, indent=2, separators=(',', ': ')))
            return (ops_file_name, console_file_name, exception_file_name, device.name)

        else:
            ops = Ops(device)
            try:
                ops.learn()
            except Exception as e:
                # Save to file
                log.root.handlers = backup_handlers
                exception_file_name = "{dir}/{o}_{do}_{dn}_exception.txt"\
                                       .format(o=feature,
                                               do=device.os,
                                               dn=device.name,
                                               dir=directory)
                if hasattr(e, 'parser'):
                    msg = 'Issue while parsing: {p}\n\n'\
                          .format(p=e.parser.__class__)
                else:
                    msg = 'Issue while building the feature\n\n'

                with open(exception_file_name, 'w') as f:
                    f.write(msg)
                    f.write(format_filter_exception(exc_type=type(e),
                                                    exc_value=e,
                                                    tb=e.__traceback__))


        # Change device object to name, to make it comparable
        ops.device = ops.device.name
        log.root.handlers = backup_handlers
        output = ops.to_dict()
        if directory:
            # This is useful for the Diff functionality, need to know the class
            # so we can check the exclude keys
            try:
                output['_exclude'] = get_ops_exclude(feature, device)
            except Exception:
                output['_exclude'] = []

        with open(ops_file_name, 'w') as f:
            f.write(json.dumps(output, sort_keys=True, indent=2, separators=(',', ': ')))

        return (ops_file_name, console_file_name, exception_file_name, device.name)
