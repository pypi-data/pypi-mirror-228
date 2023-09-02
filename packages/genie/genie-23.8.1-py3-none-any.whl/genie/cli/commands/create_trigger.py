import os
import sys
import string
import logging

from pyats.cli.base import Command, Subcommand, ERROR
from pyats.cli.base import CustomHelpFormatter

try:
    from cookiecutter.main import cookiecutter
except ImportError:
    cookiecutter = None

from .create import checkCookiecutterStatus

logger = logging.getLogger(__name__)

DEFAULT_COOKIE = "https://github.com/CiscoTestAutomation/genie-trigger-template"

ALLOWED_CHARSET = set(string.ascii_lowercase + 
                      string.ascii_uppercase + 
                      string.digits + '_.-')

def string_in(s, charset):
    return all(char in charset for char in s)

class CreateTrigger(Subcommand):
    '''
    Creates a new Genie trigger from cookiecutter template
    '''

    name = 'trigger'
    help = 'create a new Genie trigger from template'
    description = '''
    create a Genie trigger from cookiecutter template, located at:
    %s
    ''' % DEFAULT_COOKIE

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parser.add_argument('--trigger-name',
                                 type = str,
                                 help = "name of trigger to be generated")

        self.parser.add_argument('--action',
                                 type = str,
                                 help = "action the trigger will perform")

        self.parser.add_argument('--undo-action',
                                 type = str,
                                 help = "undo action the trigger will perform")

    def run(self, args):
        checkCookiecutterStatus()

        while not args.trigger_name:
            trigger_name = input('Trigger Name: ').strip()
            if trigger_name and string_in(trigger_name, ALLOWED_CHARSET):
                args.trigger_name = trigger_name
                break
            logger.error('Please provide a parser name within the '
                         'allowed character set: [A-Za-z_]+')

        while not args.action:
            action = input('Action the trigger will perform (ex. Add): ').strip()
            if action and string_in(action, ALLOWED_CHARSET):
                args.action = action
                break
            logger.error('Please provide a parser name within the '
                         'allowed character set: [A-Za-z_]+')

        while not args.undo_action:
            undo_action = input('Undo action the trigger will perform (ex. Remove): ').strip()
            if undo_action and string_in(undo_action, ALLOWED_CHARSET):
                args.undo_action = undo_action
                break
            logger.error('Please provide a parser name within the '
                         'allowed character set: [A-Za-z_]+')

        logger.info("Generating your project...")
        cookiecutter(DEFAULT_COOKIE, 
                     no_input = True,
                     extra_context = {
                        'trigger_name': args.trigger_name, 
                        'action': args.action, 
                        'undo_action': args.undo_action
                     })


