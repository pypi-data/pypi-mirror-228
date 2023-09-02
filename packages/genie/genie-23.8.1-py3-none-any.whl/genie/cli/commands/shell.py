import sys
import code
import dill
import logging

# support IPython
try:
    from IPython import start_ipython
    from traitlets.config.loader import Config
except ImportError:
    start_ipython = None

from pyats.topology import loader
from pyats.cli.base import Command

# internal logger
logger = logging.getLogger(__name__)

class ShellCommand(Command):
    '''
    Simple command to enter python shell and load Genie testbed yaml file a
    testbed variable.
    '''

    name = 'shell'
    help = ('enter Python shell, loading a pyATS testbed file '
            'and/or pickled data')
    description = '''
Enters typical python interactive shell, setting global variable 'testbed' and
'pickle_data', containing the loaded testbed objects, and unpickled data.
'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parser.add_argument('--testbed-file',
                                 dest = 'testbed',
                                 metavar = 'FILE',
                                 type = loader.load,
                                 default = None,
                                 help = 'testbed file to load')

        self.parser.add_argument('--pickle-file',
                                 dest = 'pickle_file',
                                 metavar = 'FILE',
                                 type = str,
                                 default = None,
                                 help = 'input file to unpickled into usable '
                                        'data')

        self.parser.add_argument('--no-ipython',
                                 action = 'store_false',
                                 dest = 'ipython',
                                 default = True,
                                 help = 'do not use IPython (when installed)')

    def parse_args(self, argv):
        # inject general group options
        self.add_general_opts(self.parser)

        # do the parsing
        args, unknown = self.parser.parse_known_args(argv)
        sys.argv = sys.argv[:1]+unknown
        return args

    def run(self, args):
        if not args.testbed:
            tb_file = None
        else:
            tb_file = args.testbed.testbed_file
        banner = '''\
Welcome to pyATS Interactive Shell
==================================
Python %s

>>> from pyats.topology.loader import load
>>> testbed = load('%s')\
''' % (sys.version, tb_file)

        if args.pickle_file:
            with open(args.pickle_file, 'rb') as f:
                pickle_data = dill.load(f)
            banner += '''
>>> with open('%s', 'rb') as f:
>>>     pickle_data = dill.load(f)\
''' % args.pickle_file
        else:
            pickle_data = None

        banner += '''
-------------------------------------------------------------------------------\
            '''

        namespace = {'testbed': args.testbed, 'pickle_data': pickle_data}

        if args.ipython and start_ipython:
            # wipe sys.argv because IPython doesn't like it
            sys.argv = sys.argv[:1]
            ipython_config = Config()
            ipython_config.TerminalInteractiveShell.banner1 = banner

            return start_ipython(config = ipython_config,
                                 user_ns = namespace)
        else:
            return code.interact(banner = banner,
                                 local = namespace)
