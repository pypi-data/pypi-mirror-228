import logging

try:
    from cookiecutter.main import cookiecutter
except ImportError:
    cookiecutter = None
    
from pyats.cli.base import CommandWithSubcommands

logger = logging.getLogger(__name__)

class CreateCommand(CommandWithSubcommands):
    name = 'create'
    help = 'Create Testbed, parser, triggers, ...'

    SUBCOMMANDS = []
    SUBCMDS_ENTRYPOINT = 'genie.cli.commands.create'

def checkCookiecutterStatus():
    logger.info("Checking if cookiecutter is installed...")
    # check that cookiecutter can be imported
    if cookiecutter is None:
        raise Exception('Cookiecutter is not installed, '
                        'you could install it using this command: '
                        'pip install cookiecutter')
