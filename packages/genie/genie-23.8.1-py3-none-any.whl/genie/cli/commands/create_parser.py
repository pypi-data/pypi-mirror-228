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

DEFAULT_COOKIE = "https://github.com/CiscoTestAutomation/genie-parser-template"

ALLOWED_CHARSET = set(string.ascii_lowercase + 
                      string.ascii_uppercase + 
                      string.digits + '_.-')

def string_in(s, charset):
    return all(char in charset for char in s)

class CreateParser(Subcommand):
    '''
    Creates a new Genie parser from cookiecutter template
    '''

    name = 'parser'
    help = 'create a new Genie parser from template'
    description = '''
    create a Genie parser from cookiecutter template, located at:
    %s
    ''' % DEFAULT_COOKIE

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parser.add_argument('--parser-name',
                                 type = str,
                                 help = "name of parser to be generated")

        self.parser.add_argument('--os',
                                 type = str,
                                 help = "Cisco OS for the parser")

    def run(self, args):
        checkCookiecutterStatus()

        while not args.parser_name:
            parser_name = input('Parser Name: ').strip()
            
            if parser_name and string_in(parser_name, ALLOWED_CHARSET):
                args.parser_name = parser_name
                break
            
            logger.error('Please provide a parser name within the '
                         'allowed character set: [A-Za-z_]+')
        
        while not args.os:
            cisco_os = input("Cisco OS for the parser [IOS/IOSXE/IOSXR/NXOS]: ").strip().lower()
            
            if cisco_os and string_in(cisco_os, ALLOWED_CHARSET):
                args.os = cisco_os
                break
            
            logger.error('Please provide a parser name within the '
                         'allowed character set: [A-Za-z_]+')


        logger.info("Generating your project...")
        cookiecutter(DEFAULT_COOKIE, 
                     no_input = True,
                     extra_context = {
                        'parser_name': args.parser_name, 
                        'cisco_OS': args.os
                     })

