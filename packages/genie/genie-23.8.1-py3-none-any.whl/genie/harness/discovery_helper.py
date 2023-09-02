import logging
import multiprocessing as mp
from pyats.aetest import executer, runtime
from pyats.aetest.container import TestContainer
from pyats.results import Errored, Passed
from pyats.reporter.exceptions import DuplicateIDError


multiprocessing = mp.get_context('fork')

class Verifications(TestContainer):
    # __context_type__ = 'Verifications'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parallel_verifications = kwargs.get('parallel_verifications', False)

        if self.parallel_verifications:
            self.__context_type__ = 'ParallelVerifications'
        else:
            self.__context_type__ = 'Verifications'

        self.verifiers = []

    def __iter__(self):
        yield from self.verifiers

    def __str__(self):
        '''Context __str__

        Formats the logging output

        Example
        -------
            >>> str(section)
        '''
        return 'testcase %s' %(self.uid)

    def __call__(self, **parameters):
        '''Built-in function __call__

        Call function, allowing each TestContainer objects to be "callable",
        e.g. executable directly. This is the main mechanism that runs the given
        TestContainer object. The following steps are performed when a call
        is made:

            0. update container parameters if provided
            1. open each child testable's report context
            2. run each child-testable within this testable
            3. close each child testable's report context

        Example
        -------
            >>> tc = TestContainer()
            >>> tc() # run everything contained within.

        Arguments
        ---------
            parameters (dict): any key/value parameters that should apple to
                               this round of execution.

        Returns
        -------
            the rolled-up result of all contained TestItems.

        '''

        # update local params to include call
        self.parameters.update(parameters)

        if self.parallel_verifications:
            # run each contained TestItem as a separate process
            procs = []
            for section in self:
                p = multiprocessing.Process(name=f"{section.uid}", target=run, args=(section,))
                procs.append(p)
                p.start()
            for p in procs:
                p.join()
        else:
            for section in self:
                run(section)

        # Each verification is not parented to this class, so result rollup does not apply. 
        # Must query the report server for the actual rolled up result
        self.result = self.reporter.get_section().get('result')

def run(section):
    """wrap the usual executor to provide context"""
    try:
        with section:
            executer.execute(section)
    except DuplicateIDError:
        # Section errored, continue execution
        section.result = Errored.clone(reason = f'Duplicate Section ID: {section.uid}')
