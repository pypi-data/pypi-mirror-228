import sys
import logging

# Backward compatibility with pyAts
try:
    from pyats.utils.import_utils import FlexImporter
    inheritable = FlexImporter
except ImportError:
    from pyats.aetest import loader
    inheritable = loader.__class__

from .script import TestScript

# declare module as infra
__genie_infra__ = True

MODULE_PREFIX = 'genie.harness.genie_testscript'

# Needed to overwrite to call Genie own testscript and not aetest
class GenieLoader(inheritable):

    def __init__(self):
        super().__init__(MODULE_PREFIX)

    def load(self, testable, uid = None, reporter = None):
        '''Load testable target into a TestScript

        API to load user supplied testable to an .script.TestScript class,
        allowing the engine to run the TestScript class directly.

        Arguments
        ---------

            testable (obj): testable object. Could be a file, a ModuleType, name
                            of a loaded module, or an absolute module path
            uid (TestableId): assigned uid for the task running this testable
            reporter (BaseRootReporter): reporter for this task

        Returns
        -------

            TestScript() class instantiated.

        '''

        # For backward compatibility with pyATS
        if hasattr(self, 'load_module'):
            module_func = self.load_module
        else:
            module_func = super().load

        try:
            # turn testable into module
            module = module_func(testable)

            # convert into module standard TestScript object
            testscript = TestScript(module, uid=uid, reporter=reporter)

        except Exception as exc:
            # any sort of exception = failed to import
            raise Exception('Failed to load %s' % testable) from exc

        else:
            return testscript
