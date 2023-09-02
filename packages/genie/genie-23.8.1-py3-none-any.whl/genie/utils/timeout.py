import time
import logging
from pyats.results import (Passed, Failed, Aborted, Errored, Skipped,
                         Blocked, Passx)

log = logging.getLogger(__name__)

class Timeout(object):
    '''In any kind of automation, there is a need of polling. Try to do a
       check/action, verify if expected result is there, if not, sleep for some time
       and repeat up to a maximum time.'''
      
    def __init__(self, max_time, interval, disable_log=False):
        '''max_time is in seconds
               interval is in second
               
               Try up to max_time seconds, and between interval wait interval
               seconds
        '''

        self.max_time = max_time
        self.interval = interval
        self.snapshot_time = time.time()
        self.one_more_time = False
        self.count = 1
        self.disable_log = disable_log

        if self.max_time and self.interval and not self.disable_log:
            log.info('Starting a timeout with maximum time of {mt} seconds with '
                     'interval of {i} seconds, Test case will fail after the '
                     'maximum time set'.format(mt=self.max_time,
                                               i=self.interval))

    @property
    def timeout(self):
        return self.snapshot_time + self.max_time

    def iterate(self):
        if self.max_time is None and self.interval is None:
            return False

        if self.one_more_time:
            if not self.disable_log:
                log.info('Performing the last attempt')
            self.one_more_time = False
            return True
        keep_going = time.time() < self.timeout
        if not keep_going:
            if not self.disable_log:
                log.info('Ran out of time for this timeout')
        return keep_going

    def sleep(self):
        if self.max_time is None and self.interval is None:
            return

        remaining_time = self.timeout - time.time()
        if remaining_time < 0:
            # Ran out of time!
            if not self.disable_log:
                log.info('0 second remaining; Will not sleep')
            return

        sleep_time = self.interval
        if remaining_time < self.interval:
            sleep_time = remaining_time
            self.one_more_time = True
        if not self.disable_log:
            log.info("{0:.2f} seconds remaining; Sleeping for {1:.2f} seconds. "
                     "'{v}' attempt(s) have been performed".format(
                      remaining_time, sleep_time, v=self.count))
        self.count += 1

        time.sleep(sleep_time)

class TempResult(object):
    def __init__(self, container = None):
        self.container = container
        self.goto = None
        self.temp_result = Passed
        self.reason = None
        self.from_exception = None

    def passed(self, reason = None, from_exception = None, goto = None):
        return self._update_result(temp_result=Passed, reason=reason,
                                   from_exception = from_exception, goto=goto)

    def failed(self, reason = None, from_exception = None, goto = None):
        return self._update_result(temp_result=Failed, reason=reason,
                                   from_exception = from_exception, goto=goto)

    def aborted(self, reason = None, from_exception = None, goto = None):
        return self._update_result(temp_result=Aborted, reason=reason,
                                   from_exception = from_exception, goto=goto)

    def errored(self, reason = None, from_exception = None, goto = None):
        return self._update_result(temp_result=Errored, reason=reason,
                                   from_exception = from_exception, goto=goto)

    def skipped(self, reason = None, from_exception = None, goto = None):
        return self._update_result(temp_result=Skipped, reason=reason,
                                   from_exception = from_exception, goto=goto)

    def blocked(self, reason = None, from_exception = None, goto = None):
        return self._update_result(temp_result=Blocked, reason=reason,
                                   from_exception = from_exception, goto=goto)

    def passx(self, reason = None, from_exception = None, goto = None):
        return self._update_result(temp_result=Passx, reason=reason,
                                   from_exception = from_exception, goto=goto)

    def _update_result(self, temp_result, reason, from_exception, goto):
        log.info(reason)
        self.temp_result = temp_result
        self.reason = reason
        self.goto = goto
        self.from_exception = from_exception

    def result(self):
        kwargs = {'reason':self.reason,
                 'from_exception':self.from_exception}
        if self.goto:
            kwargs['goto'] = self.goto

        if self.temp_result == Passed:
            self.container.passed(**kwargs)
        elif self.temp_result == Failed:
            self.container.failed(**kwargs)
        elif self.temp_result == Aborted:
            self.container.aborted(**kwargs)
        elif self.temp_result == Errored:
            self.container.errored(**kwargs)
        elif self.temp_result == Skipped:
            self.container.skipped(**kwargs)

