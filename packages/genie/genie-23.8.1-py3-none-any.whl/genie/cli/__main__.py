
import os
# Enforce new CLI argument style
os.environ['PYATS_CLI_STYLE'] = 'modern'

from .core import CLI

from .commands.learn import LearnCommand
from .commands.diff import DiffCommand
from .commands.parser import ParserCommand
from .commands.run import RunCommand
from .commands.shell import ShellCommand
from .commands.dnac import DnacCommand
from .commands.create import CreateCommand
from .commands.develop import DevelopCommand
from .commands.undevelop import UndevelopCommand

CORE_CMDS=[
    LearnCommand,
    DiffCommand,
    ParserCommand,
    RunCommand,
    ShellCommand,
    DnacCommand,
    CreateCommand,
    DevelopCommand,
    UndevelopCommand,
]

def main(argv=None):
    '''
    entrypoint for console_script
    '''

    return CLI(prog=CLI.PROG,
               usage=CLI.USAGE,
               epilog=CLI.EPILOG,
               commands=CORE_CMDS).main(argv)

if __name__ == '__main__':
    '''
    __main__ in case someone called this from the commandline
    '''
    main()
