import os
import sys
import json
import shutil
import logging
from tqdm import tqdm

from pyats.cli.base import Command

import importlib
# import pcall
try:
    pcall = importlib.import_module('pyats.async').pcall
except ImportError:
    from pyats.async_ import pcall
# # import pcall
# from pyats.async import pcall

from genie.conf import Genie
from genie.utils.diff import Diff
from genie.utils.summary import Summary
from genie.harness.datafile.loader import PtsdatafileLoader,\
                                          VerificationdatafileLoader


CLEAN_OPS = ['callables', 'maker', 'diff_ignore']

# internal logger
log = logging.getLogger(__name__)
# Remove pyATS logger added by easypy __init__
log.root.handlers = []

class DiffCommand(Command):
    '''
    Command to diff two snapshots saved to file
    '''

    name = 'diff'
    help = 'Command to diff two snapshots saved to file or directory'
    description = '''
Diff two feature or parser snapshots saved to file or directory
Default exclusion can be found at $VIRTUAL_ENV/genie_yamls/pts_datafile.yaml
    '''

    usage = '''{prog} [commands] [options]

Example
-------
  {prog} file1 file2
  {prog} dir1 dir2
  {prog} dir1 dir2 --exclude "age"
  {prog} dir1 dir2 --no-default-exclusion --exclude "age" "uptime"
'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parser.add_argument('a',
                                 metavar = '[file or directory]',
                                 type = str,
                                 help = 'file/directory of pre=snapshot')
        self.parser.add_argument('b',
                                 metavar = '[file or directory]',
                                 type = str,
                                 help = 'file/directory of post-snapshot')
        self.parser.add_argument('--output', default='.',
                                 help='Which directory to store logs, by '
                                      'default it will be current directory (Optional)')
        self.parser.add_argument('--exclude', nargs='*',
                                 help='Keys to exclude when '
                                      'saving the Feature (Optional)')
        self.parser.add_argument('--no-default-exclusion',
                                 action='store_true',
                                 help='Do not use the default exclude keys (Optional)')
        self.parser.add_argument('--archive-dir',
                                 type = str,
                                 metavar = '',
                                 dest = 'archive_dir',
                                 help = 'Directory to store a .zip of the output')
        self.parser.add_argument('--list-order',
                                 action = 'store_true',
                                 help = 'Compare two lists irrelevant of their order(Optional)')

    def parse_args(self, argv):
        # inject general group options
        self.add_general_opts(self.parser)

        # do the parsing
        args, unknown = self.parser.parse_known_args(argv)
        sys.argv = sys.argv[:1]+unknown
        return args

    def run(self, args):

        # Diff the file/directory
        # Did they provide a file or a directory?
        a = args.a
        b = args.b
        archive_dir = args.archive_dir
        exclude = args.exclude
        list_order = args.list_order
        self.no_default_exclusion = args.no_default_exclusion
        self.verbose = args.verbose

        exclude = exclude if exclude else []

        self.directory = args.output
        os.makedirs(self.directory, exist_ok=True)
        # Report nicely
        if os.path.isdir(a) and os.path.isdir(b):
            # Dir mode
            summary = Summary('Genie Diff Summary between directories {a}/ and {b}/'.format(a=a, b=b), 80)

            self._diff_directory(a, b, exclude, summary, list_order)
        elif os.path.isfile(a) and os.path.isfile(b):
            # File mode
            summary = Summary('Genie Diff Summary between file {a} and {b}'.format(a=a, b=b), 80)
            self._diff_file(a, b, exclude, summary, list_order)
        elif not os.path.exists(a):
            # a does not exists
            raise Exception('{a}: No such file or directory'.format(a=a))
        elif not os.path.exists(b):
            # a does not exists
            raise Exception('{b}: No such file or directory'.format(b=b))
        else:
            # Mismatch, error out
            raise Exception('{a} and {b} must be either both a file or '
                            'both a directory'.format(a=a, b=b))
        summary.print()
        if self.directory != '.' and archive_dir:
            # Copy output directory to this location
            archive = os.path.join(archive_dir, 'snapshot')
            log.info("Creating archive file: {a}.zip".format(a=archive))
            shutil.make_archive(archive, 'zip', self.directory)


    def _diff_directory(self, a, b, exclude, summary, list_order):
        seen_file = []
        for root, dirs, files in tqdm(os.walk(a)):
            for file_ in files:
                seen_file.append(file_)
                # Make this file is an ops/parser structure
                # See if this file exists in b directory
                # If it does, compare
                # If it doesnt, skip this file
                file_a = os.path.join(a, file_)
                file_b = os.path.join(b, file_)
                if file_.endswith('ops.txt') or file_.endswith('feature.txt'):
                    style = 'pts'
                elif file_.endswith('parsed.txt'):
                    style = 'parser'
                else:
                    continue
                if not os.path.isfile(file_b):
                    summary.add_message(' File: {f}'.format(f=file_))
                    summary.add_message('  - Only in {a}'.format(a=a))
                    summary.add_sep_line()
                    continue
                self._diff_file(file_a, file_b, exclude, summary, list_order)


        # For completness, make sure no file from b is not forgotten in the
        # summary table
        for root, dirs, files in os.walk(b):
            for file_ in files:
                if file_ in seen_file:
                    continue
                if not file_.endswith('ops.txt') and not file_.endswith('parsed.txt'):
                    continue
                # Then it was not seen in a, just make sure
                file_a = os.path.join(a, file_)
                if not os.path.isfile(file_a):
                    summary.add_message(' File: {f}'.format(f=file_))
                    summary.add_message('  - Only in {b}'.format(b=b))
                    summary.add_sep_line()
                    continue

    def _diff_file(self, a, b, exclude, summary, list_order):
        # Compare those files
        with open(a, 'r') as f: 
            a_output = json.load(f)

        with open(b, 'r') as f:
            b_output = json.load(f)

        file_name = os.path.basename(a)

        # Figure out the exclude!
        if self.no_default_exclusion:
            # Just use exclude
            exclude = exclude
        else:
            # Get the class information
            # Exclude should be part of the output
            exclude = b_output.get('_exclude', a_output.get('_exclude', [])) + exclude

        diff = Diff(a_output, b_output, exclude=exclude, verbose=self.verbose, list_order=list_order)
        diff.findDiff()

        summary.add_message(' File: {file}'.format(file=os.path.basename(a)))
        if str(diff):
            diff_file = os.path.join(self.directory, 'diff_{file}'
                                                     .format(file=file_name))
            with open(diff_file, 'w') as f:
                f.write('--- {a}\n'.format(a=a))
                f.write('+++ {b}\n'.format(b=b))
                f.write(str(diff))
            summary.add_message("  - Diff can be found at {f}"\
                                .format(file=os.path.basename(a),
                                        f=diff_file))
            summary.add_sep_line()
        else:
            summary.add_message("  - Identical".format(file=os.path.basename(a)))
            summary.add_sep_line()
