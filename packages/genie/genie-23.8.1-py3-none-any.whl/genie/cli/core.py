from pyats.cli.core import CLI
import warnings
from pyats.log.warnings import enable_deprecation_warnings

class CLI(CLI):
    enable_deprecation_warnings('genie\..*|__main__')
    warnings.warn(
        message="Starting v20.1, 'genie' command is deprecated. All of genie's "
                "subcommands has been moved to pyats. Please use 'pyats' command "
                "instead.",
        category=DeprecationWarning)

    COMMANDS_ENTRYPOINT = 'genie.cli.commands'
    PROG = 'genie'
    USAGE = '''{prog} <command> [options]'''.format(prog = PROG)
    EPILOG = '''
        Run '{prog} <command> --help' for more information on a command.
    '''.format(prog = PROG)
