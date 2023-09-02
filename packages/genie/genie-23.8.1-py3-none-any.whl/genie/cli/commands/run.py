import logging
import sys
import warnings

from pyats.cli.base import Command, Subcommand
from pyats.cli.base import CustomHelpFormatter

# use the global runtime
from pyats.easypy import runtime


from . import job
from genie.harness.main import Genie


logger = logging.getLogger(__name__)

# hack until pyats run testcase is done - Nathan
def _get_cmd():
    # if it's called from pyats then this cmd will be renamed to 'genie'
    # case for called by genie, need to raise deprecation warning
    if sys.argv[0].endswith('/genie'):
        if len(sys.argv) >=2 and sys.argv[1] == 'run':
            warnings.warn(
                message="Starting v20.1, 'genie run' command is deprecated. Please use "
                        "'pyats run genie' command "
                        "instead.",
                category=DeprecationWarning)
        return 'run'
    # pyats
    else:
        return 'genie'

class RunCommand(Command):
    run_cmd_name = _get_cmd()
    name = run_cmd_name
    help = 'Run Genie triggers & verifications in pyATS runtime environment'
    description = '''
    Run Genie harness in a generated job file, generated report and result
    '''

    usage = '''{prog} [options]

Example
-------
  {prog} --trigger-uids "Or('Sleep')" --testbed-file /path/to/testbed.yaml
  {prog} --trigger-uids "Or('Sleep')" --verification-uids "Or('Ospf')" --testbed-file /path/to/testbed.yaml --html-logs .
'''

    description = '''
'''
    standard_logging = False

    def main(self, argv):
        def print_help():
            Genie(parser=runtime.parser)
            type(runtime).print_help(runtime)

        runtime.print_help = print_help


        # configuration for running this guy
        modulename = job.__name__
        classname = job.GenieJob.__qualname__

        configuration = {
            'components': {
                'job': {
                    'class': '{module}.{class_}'.format(module = modulename,
                                                        class_ = classname),
                }
            }
        }

        # run and exit
        return runtime.main(argv = argv,
                            configuration = configuration)

