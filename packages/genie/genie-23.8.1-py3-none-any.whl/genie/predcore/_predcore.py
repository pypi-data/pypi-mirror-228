'''
Predicate and Pre-Requisite Classes
===================================

:mod:`predcore` offers a collection of predicate and pre-requisite base
classes that provide a foundation for convenient, powerful and complex
condition-driven testing.

'''

import sys
import logging
import collections
import time
from difflib import SequenceMatcher

python3 = sys.version_info >= (3,0)

if python3:
    from inspect import signature
else:
    from inspect import getcallargs

# module level logger
logger = logging.getLogger(__name__)

DEFAULT_INTERVAL = 2


class PredicateTestedFalseSignal(AssertionError):
    """Signal raised when `assert_test <Predicate.assert_test>` is called on a
       `Predicate` that tests `False`.  As described in result_behavior_,
       the user is expected to catch this signal.

.. _result_behavior:  http://wwwin-pyats.cisco.com/documentation/html/aetest/results.html#result-behavior
    """
#
# PredicateTestedFalseSignal is also used to terminate a pre-requisite loop
# when it tests `False`.
#
    def __init__(self, value='', *args):
        """ __init__ of PredicateTestedFalseSignal

        Allows to capture extra arguments that were passed to this Exception.
        Joins all the extra argument into self.args tuple to display
        to the user
        """

        # Capture all extra argument given to the exception
        self.args = ('\n'.join(t for t in (value,) + args),)

class PredicateTestedTrueSignal(AssertionError):
    """Signal used to terminate a pre-requisite loop when it tests `True`."""

# http://stackoverflow.com/questions/11301138/\
# how-to-check-if-variable-is-string-with-python-2-and-3-compatibility
try:
    basestring  # attempt to evaluate basestring
    def isstr(s):
        return isinstance(s, basestring)
except NameError:
    def isstr(s):
        return isinstance(s, str)

def flatten(seq):
    ''' Generator that recursively unwraps a series of objects
        into a flat sequence.
    '''
    for arg in seq:
        if isinstance(arg, collections.abc.Iterable) and not isstr(arg):
            for f in flatten(arg):
                yield f
        else:
            yield arg


###############################################################################
# Predicate base class.
###############################################################################
class Predicate(object):
    """This class allows for testing the truth of some condition.

    This class should be inherited and a `test` method defined
    that returns `True` or `False` as appropriate.

    Whenever the object is tested for truth (for example, in an `if`
    statement), the `test` method is automatically called.

    The `dump` method, if overloaded, is called automatically when
    appropriate and allows the user to express the object's state in an
    easy-to-read manner to assist with debugging and failure diagnosis.
    """

    last_result = None
    """The result of the most recent truth test done on the predicate.  It
       defaults to `None` and is set to either `True` or `False` based on the
       results of the last truth test.
    """

    def test (self):
        '''Override this method to actually perform the predicate test.'''
        return False


    def __nonzero__ (self):
        self.last_result = bool(self.test())
        return self.last_result


    # Python3 internally calls __bool__ when an object is tested for truth,
    # Python2 internally calls __nonzero__.
    __bool__ = __nonzero__

    # Calling the predicate performs a truth test.
    # This is to make predcore interoperable with other implementations
    # (such as those in threading.wait_for and asyncio.wait_for).
    #
    # Any attempt to pass parameters into the call results in an
    # exception thrown (since this implementation sets the predicate state
    # on construction).
    __call__ = __nonzero__


    def assert_test (self, *args):
        """
        Perform a truth test on the predicate, and if it does not test
        `True`, raise `PredicateTestedFalseSignal`.

        The result of `dump <Predicate.dump>` is saved in the exception for
        debug purposes.

        Parameters
        ----------
        `args`:  `str`
            User-defined positional arguments to be passed to
            `PredicateTestedFalseSignal` if the predicate does not test
            `True`.
        """
        if not self:
            dumpText = self.dump()

            if args:
                args = tuple(list(args) + [dumpText])
                raise PredicateTestedFalseSignal (*args)
            else:
                raise PredicateTestedFalseSignal (dumpText)


    def dump(self):
        ''' Dump the predicate's internal state for debugging and logging
            purposes.
        '''
        return "Predicate (last_result = {})".format(self.last_result)


###############################################################################
# Pre-requisite predicate looping / waiting base classes.
###############################################################################

class TimedPredicate (Predicate):
    '''This base class provides basic predicate timing services.
    '''

    def __init__ (self, *test_args, **kwargs):
        """
        Parameters
        ----------
        test_args :  series of positional arguments containing a series of \
            objects to test
            All positional arguments are first flattened into a single list
            before they are tested for truth.

        timeout : `int`
            The maximum amount of time in seconds to continue testing the
            objects in the series.
            Defaults to ``None``.

        interval :  `int`
            The interval in seconds for which the remaining objects are
            rechecked.
            Defaults to 2.

        iterations : `int`
            The maximum number of times to check the objects.
            Defaults to ``None``.


        .. note::
            You must specify either `timeout` or `iterations`, but you
            cannot specify both, otherwise a `ValueError` is raised.

        .. note::
            If `timeout` is less than `interval` a warning is logged
            explaining that un-necessary waiting may occur.
            If `interval` is left at its default, it is automatically
            decreased to the value of `timeout`.
        """

        self.last_elapsed_time = None
        """Indicates the amount of time it took the last use to become true."""

        # Intentially implement using Python2 idiom in order to prevent
        # splitting this module for py2/py3.
        timeout    = kwargs.pop('timeout', None)
        iterations = kwargs.pop('iterations', None)
        interval   = kwargs.pop('interval', DEFAULT_INTERVAL)
        if timeout and iterations:
            raise ValueError (
                "timeout and iterations are mutually exclusive, " \
                "yet they were both specified.")

        if not timeout and not iterations:
            raise ValueError (
                "Neither timeout nor iterations were specified.  " \
                "Please specify at least one.")

        if iterations:
            self._iterations = iterations
            self._timeout = iterations * interval
        else:
            if timeout < interval:
                logger.warning("The timeout was specified as {}, which being "\
                "less than the interval value {} could lead to "\
                "unnecessary waiting.".format(timeout, interval))
                if interval == DEFAULT_INTERVAL:
                    logger.warning(\
                        "Reassigning the default interval value to {}.".\
                        format(timeout))
                    interval = timeout
            self._timeout = timeout

        self._interval = interval
        self.object_list = list(test_args)
        self.object_list = [ item for item in flatten(self.object_list) ]


    def timed_iterate(self, testFunction, valToReturnOnTimeout):
        '''
        Periodically call a test function.

        A `ValueError` is raised if the testFunction passed in is not
        callable.

        Parameters
        ----------
        testFunction : `callable`
            Function to call periodically

        valToReturnOnTimeout : `bool`
            Value to return if timeout expires.
        '''
        if not callable(testFunction):
            raise ValueError ("testFunction must be a callable.")

        logger.debug(
            "{} is checking predicates over {:0.1f}s at "
            "{:0.1f}s intervals.".\
            format(self.__class__.__name__,self._timeout, self._interval))
        interval = self._interval
        start_time = time.time()
        end_time = start_time + self._timeout
        current_time = start_time

        while current_time < end_time:
            cstime = current_time
            self.last_elapsed_time = time.time() - start_time
            logger.debug("Elapsed time [{:0.1f}s of {:0.1f}s] ".\
                format(self.last_elapsed_time, self._timeout))
            try:
                testFunction()
            finally:
                self.last_elapsed_time = time.time() - start_time
            #
            # Now sleep the amount of time remaining in our check interval.
            #
            current_time = self.sleepUntilCheckIntervalExpired(
                                cstime, interval)
            self.last_elapsed_time = current_time - start_time
        return valToReturnOnTimeout


    @staticmethod
    def sleepUntilCheckIntervalExpired (cstime, interval):
        '''If there is time remaining in the current interval, then
           sleep to the end of the interval.

           Parameters
           ----------

           cstime : `float`
               The time when the current interval started

           interval : `float`
               The interval length.


           Returns
           -------
           current_time : `float`
        '''
        current_time = time.time()
        dtime = current_time - cstime
        if dtime < interval:
            timeToSleep = interval - dtime
            logger.debug(
                "Sleeping remaining {:0.1f} seconds in interval".\
                format(timeToSleep))
            time.sleep(timeToSleep)
        current_time = time.time()
        return current_time


    @property
    def time_remaining (self):
        ''' Calculate the time remaining in the predicate.
            Since timed truth tests are typically blocking operations, this
            is typically checked before or after a truth test
            has been executed.  It may also be useful during debugging.
        '''
        if self.last_elapsed_time:
            left = self._timeout - self.last_elapsed_time
            return 0 if left < 0 else left
        else:
            return self._timeout




class Prerequisite (TimedPredicate):
    """ Periodically test a series of objects for truth until they all test
        `True` or a timeout expires.

        This predicate tests `True` if all objects in the series test
        `True`.

        This predicate tests `False` if one or more objects in the series
        continue to test `False` until a timeout expires.

        If any of the objects in the series has a `dump <Predicate.dump>`
        method (for example, the object inherits from `Predicate`), this
        method is automatically invoked in order to provide debug information
        to the user.

        `Pre-requisites <Prerequisite>` once instantiated can be tested multiple
        times. Each time the truth of the pre-requisite is taken all the objects
        are scheduled for retesting.

        Objects are tested in the order passed. Once an object becomes
        `True` it is no longer tested (i.e., it is removed from the list of
        objects to be tested for a given test of the `Prerequisite`).
    """

    def __init__ (self, *test_args, **kwargs):
        """
        Parameters
        ----------
        test_args :  series of positional arguments containing a series of \
            objects to test
            All positional arguments are first flattened into a single list
            before they are tested for truth.

        timeout : `int`
            The maximum amount of time in seconds to continue testing the
            objects in the series, measured from the time the last truth test
            was invoked.
            Defaults to ``None``.

        interval :  `int`
            The interval in seconds for which the remaining objects are
            rechecked.
            Defaults to 2.

        iterations : `int`
            The maximum number of times to check the objects.
            Defaults to ``None``.


        .. note::
            You must specify either `timeout` or `iterations`, but you
            cannot specify both, otherwise a `ValueError` is raised.

        .. note::
            If `timeout` is less than `interval` a warning is logged
            explaining that un-necessary waiting may occur.
            If `interval` is left at its default, it is automatically
            decreased to the value of `timeout`.
        """

        self.andPredicate = None

        super(Prerequisite, self).__init__ (*test_args, **kwargs)


    def test_during_iteration(self):
        '''
        Execute class-specific test logic.

        In order to exit from the iteration loop and cause this predicate to
        test `True`, this method is expected to raise
        PredicateTestedTrueSignal.

        In order to exit from the iteration loop and cause this predicate to
        test `False`, this method is expected to raise
        PredicateTestedFalseSignal.

        These signals are expected to be caught in test() method of this class
        and transformed into the appropriate `bool` return codes.
        '''
        #
        # Check remaining predicates for truth (but if one tests `False`,
        # the remaining predicates are not tested).
        #
        if self.andPredicate:
            #
            # Since all predicates tested `True`, terminate the iteration
            # because this predicate has now tested `True`.
            #
            raise PredicateTestedTrueSignal
        else:
            # At least one predicate in the list failed.
            # Log the failure reason for the user.
            logger.info(self.andPredicate.dump())

            # Remove any predicates that have already tested `True`.
            self.andPredicate.remove_last_passed()

            # Continue iteration.


    def test (self):
        self.andPredicate = AndPredicate(*self.object_list)
        #
        # If not all the predicates tested `True` before the timeout expired,
        # then the predicate fails.
        #
        try:
            return self.timed_iterate(
                testFunction         = self.test_during_iteration,
                valToReturnOnTimeout = False)
        except PredicateTestedTrueSignal:
            return True



    def dump (self):
        if self.last_elapsed_time:
            last_elapsed = float("{0:.2f}".format(self.last_elapsed_time))
        else:
            last_elapsed = None

        # Use "is" to avoid doing a truth test on andPredicate.
        if self.andPredicate is None:
            return ("{} (max wait time: {}, last elapsed: {})".\
                    format(\
                        self.__class__.__name__,
                        self._timeout,
                        last_elapsed))
        else:
            andDumpText = self.andPredicate.dump()

            return ("{} (max wait time: {}, last elapsed: {}, \n{})".\
                    format(\
                        self.__class__.__name__,
                        self._timeout,
                        last_elapsed, andDumpText))


class PrerequisiteWhile (Prerequisite):
    """ Periodically test a series of objects for truth until either a
        timeout expires or one or more objects test `False`.

        This predicate tests `True` if all objects in the series continue to
        test `True` until a timeout expires.

        This predicate tests `False` if one or more objects in the series
        test `False`.

        If any of the input objects has a `dump <Predicate.dump>` method
        (for example, the object inherits from `Predicate`), this method is
        automatically invoked in order to provide debug information to the
        user.

        Pre-requisites once instantiated can be tested multiple times. Each time
        the truth of the pre-requisite is taken all the objects are scheduled
        for retesting.

        Objects are tested in the order passed.
    """


    def test_during_iteration(self):
        '''
        Execute class-specific test logic.

        In order to exit from the iteration loop and cause this predicate to
        test `True`, this method is expected to raise
        PredicateTestedTrueSignal.

        In order to exit from the iteration loop and cause this predicate to
        test `False`, this method is expected to raise
        PredicateTestedFalseSignal.

        These signals are expected to be caught in this class' test() method
        and transformed into the appropriate `bool` return codes.
        '''
        #
        # Test contained predicates and terminate iteration if one or more
        # tests `False`.
        #
        if not self.andPredicate:
            #
            # At least one predicate in the list failed, this means
            # the containing predicate has failed.
            #
            raise PredicateTestedFalseSignal

        # Continue iteration.


    def test (self):
        self.andPredicate = AndPredicate(*self.object_list)
        #
        # If any of the predicates tested `False` before the timeout expired,
        # then the predicate fails.
        #
        try:
            return self.timed_iterate(
                testFunction         = self.test_during_iteration,
                valToReturnOnTimeout = True)
        except PredicateTestedFalseSignal:
            return False



###############################################################################
# Predicate base classes allowing logical grouping of predicates
###############################################################################


class AndPredicate (Predicate):
    "Logical AND of a series of objects."

    def __init__ (self, *test_args):
        """
        Each object in the series is tested in order until one evaluates to
        `False`.

        This predicate tests `True` only when all objects in the series
        test `True`.

        This predicate tests `False` if at least one object in the
        series tests `False`.

        If any object in the series inherits from `Predicate` then its
        `dump <Predicate.dump>` method is called when appropriate.

        This predicate can be seen as wrapping/containing the series of
        objects.

        The series of objects is scheduled for retesting each time the
        predicate is tested for truth.


        Parameters
        ----------
        test_args :  series of positional arguments
            All positional arguments are considered as part of a list of
            objects that must all test `True` in order for this predicate
            to test `True`.
            All positional arguments are first flattened into a single list
            before they are tested for truth.

        """

        self.object_list = [ item for item in flatten(list(test_args)) ]
        """List of predicates passed in by the user."""

        self.last_passed = []
        """List of objects that tested `True`
           after the predicate was last tested for truth."""

        self.last_failed = []
        """List of objects that tested `False`
           after the predicate was last tested for truth."""

        self.last_untested = self.object_list
        """List of objects that were not tested for truth
           after the predicate was last tested for truth."""


    def test (self):
        self.last_untested = list(self.object_list)
        self.last_failed = []
        self.last_passed = []

        while self.last_untested:
            obj = self.last_untested.pop(0)
            if hasattr(obj, 'dump'):
                logger.debug("AndPredicate is checking predicate: {}, {}".
                    format(obj.dump(), str(obj)))
            else:
                logger.debug("AndPredicate is checking predicate: {}".
                    format(str(obj)))
            if obj:
                self.last_passed.append(obj)
            else:
                self.last_failed.append(obj)
                return False
        return True


    def remove_last_passed(self):
        '''Remove from this predicate
           all contained predicates that have already passed'''

        for obj in self.last_passed:
            try:
                self.object_list.remove(obj)
            except ValueError:
                pass


    def dump (self):
        return ("AndPredicate (\npassed  : {},\n\n"
                "failed  : {},\n\nuntested: {})".\
                    format(\
                    "\n          ".join([ obj.dump() \
                        if hasattr(obj, 'dump') else str(obj)\
                        for obj in self.last_passed ]),
                    "\n          ".join([ obj.dump() \
                        if hasattr(obj, 'dump') else str(obj)\
                        for obj in self.last_failed ]),
                    "\n          ".join([ obj.dump() \
                        if hasattr(obj, 'dump') else str(obj)\
                        for obj in self.last_untested ])))


class OrPredicate (Predicate):
    "Logical OR of a series of objects."

    def __init__ (self, *test_args):
        """
        Each object in the series is tested in order until one evaluates to
        `True`.

        This predicate tests `True` if at least one object in the
        series tests `True`.

        This predicate tests `False` only when all objects in the series
        test `False`.

        If any object in the series inherits from `Predicate` then its
        `dump <Predicate.dump>` method is called when appropriate.

        This predicate can be seen as wrapping/containing the series of
        objects.

        The series of objects is scheduled for retesting each time the
        predicate is tested for truth.


        Parameters
        ----------
        test_args :  series of positional arguments
            All positional arguments are considered as part of a list of
            objects that must all test `False` in order for this predicate
            to test `False`.
            All positional arguments are first flattened into a single list
            before they are tested for truth.

        """

        self.object_list = [ item for item in flatten(list(test_args)) ]
        """List of predicates passed in by the user."""

        self.last_passed = []
        """List of objects that tested `True`
           after the predicate was last tested for truth."""

        self.last_failed = []
        """List of objects that tested `False`
           after the predicate was last tested for truth."""

        self.last_untested = self.object_list
        """List of objects that were not tested for truth
           after the predicate was last tested for truth."""


    def test (self):
        self.last_untested = list(self.object_list)
        self.last_failed = []
        self.last_passed = []

        while self.last_untested:
            obj = self.last_untested.pop(0)
            if hasattr(obj, 'dump'):
                logger.debug("OrPredicate is checking predicate: {}, {}".
                    format(obj.dump(), str(obj)))
            else:
                logger.debug("OrPredicate is checking predicate: {}".
                    format(str(obj)))
            if obj:
                self.last_passed.append(obj)
                return True
            self.last_failed.append(obj)
        return False


    def dump (self):
        return ("OrPredicate (\npassed  : {},\n\n"
                "failed  : {},\n\nuntested: {})".\
                    format(\
                    "\n          ".join([ obj.dump() \
                        if hasattr(obj, 'dump') else str(obj)\
                        for obj in self.last_passed ]),
                    "\n          ".join([ obj.dump() \
                        if hasattr(obj, 'dump') else str(obj)\
                        for obj in self.last_failed ]),
                    "\n          ".join([ obj.dump() \
                        if hasattr(obj, 'dump') else str(obj)\
                        for obj in self.last_untested ])))


class NotPredicate (Predicate):
    "Logical NOT of an object"

    def __init__ (self, object_to_test):
        """
        This predicate tests `True` if the input object tests `False`.

        This predicate tests `False` if the input object tests `True`.

        This predicate can be seen as wrapping/containing the input object.

        If the input object inherits from `Predicate` then its
        `dump <Predicate.dump>` method is called when appropriate.

        Parameters
        ----------
        object_to_test : `object`

        """

        self.object_to_test = object_to_test
        """User-specified object to test."""

    def test (self):
        return not self.object_to_test

    def dump (self):
        obj = self.object_to_test
        return "NotPredicate ({})".\
                    format(obj.dump() if hasattr(obj, 'dump') else str(obj))



###############################################################################
# Other useful Predicate base classes
###############################################################################


class InPredicate (Predicate):
    "Predicate that tests membership of a candidate object in a sequence"

    def __init__ (self, candidate_member_object, sequence):
        """
        This predicate tests `True` if the candidate object is a member of
        the sequence, otherwise it tests `False`.

        Parameters
        ----------
        candidate_member_object : `object`

        sequence : Iterable such as `str`, `list` or `tuple`.

        """

        self.candidate_member_object = candidate_member_object
        """Candidate object to test for membership in sequence."""

        self.sequence = sequence
        """Sequence potentially having candidate object as a member."""

    def test (self):
        return self.candidate_member_object in self.sequence

    def dump (self):
        return "InPredicate ({}, {})".format(\
                    self.candidate_member_object, self.sequence)


def print_func (func, *args, **kwargs):
    '''Given a function and a set of arg/kwarg inputs, construct a
       human-readable representation of the function being called showing which
       parameters are being set to which values.
    '''

    if python3:
        sig = signature(func)
        par = sig.parameters
        bobj = sig.bind(*args, **kwargs)
        #
        # Insert default arguments (since bind ignores them).
        #
        for param in par.values():
            if (param.name not in bobj.arguments
                    and param.default is not param.empty):
                bobj.arguments[param.name] = param.default

        callargs = bobj.arguments
    else:
        callargs = getcallargs(func, *args, **kwargs)

    first_arg = True
    func_call_text = []
    func_call_text.append("{} (".format(func.__name__))
    nonfirst_separator=', '
    separator = ''
    for arg in callargs:
        func_call_text.append("{}{}={!r}".format(
                                           separator, arg, callargs[arg]))
        if first_arg:
            first_arg = False
            separator = nonfirst_separator
    func_call_text.append(")")

    return ''.join(func_call_text)




class FunctionCallEqualsPredicate(Predicate):
    """Predicate that, when tested, calls a user-specified function with
       user-specified arguments.

       The predicate tests `True` if the function returns the expected result.

       The predicate tests `False` if the function does not return the expected
       result.

       For example::

           >>> from predcore import FunctionCallEqualsPredicate

           >>> def isEven(number):
           ...   return (number % 2) == 0

           >>> pred = FunctionCallEqualsPredicate(isEven, True, 1)
           >>> True if pred else False
           False

           >>> pred = FunctionCallEqualsPredicate(isEven, True, 4)
           >>> True if pred else False
           True


       Another example of using this predicate to test for a regex match
       (also showing use of keyword arguments)::

           >>> import re
           >>> pred = FunctionCallEqualsPredicate(function=re.findall,
           ...  expected_function_result=[],
           ...  pattern='banana',string='in the apple orchard')

           >>> True if pred else False
           True

           >>> pred = FunctionCallEqualsPredicate(function=re.findall,
           ...  expected_function_result=['apple'],
           ...  pattern='apple',string='in the apple orchard')

           >>> True if pred else False
           True

           >>> pred.dump()
           "FunctionCallEqualsPredicate (
           (findall (pattern='banana', string='in the apple orchard', flags=0) == []),
           ComparisonSucceeded)"



       Another example of using this predicate to do numeric comparisons.
       Let's try "less than"::

           >>> pred = FunctionCallEqualsPredicate(lambda a,b: a < b, True, 1, 2)
           >>> True if pred else False
           True

           >>> pred = FunctionCallEqualsPredicate(lambda a,b: a < b, True, 2, 1)
           >>> True if pred else False
           False


    """
    def __init__(self, function, expected_function_result, *args, **kwargs):
        """
        Parameters
        ----------

          function :
               The function to call.

          expected_function_result :
               if function returns this expected result then the predicate
               tests `True`.

          args : variable number of positional args
               positional arguments to pass to function.

          kwargs : variable number of keyword args
               keyword arguments to pass to function.
        """
        self.func = function
        self.expected_function_result = expected_function_result
        self.args = args
        self.kwargs = kwargs
        self.last_function_result = None

    def dump(self):
        dumpList = []
        dumpList.append("FunctionCallEqualsPredicate (\n({} \n== {})".
                format(print_func(self.func, *self.args, **self.kwargs),
                      self.expected_function_result))
        if self.last_result is None:
            dumpList.append (" , \nNotTestedYet")
        else:
            if self.last_result:
                dumpList.append(", \nComparisonSucceeded")
            else:
                dumpList.append(", \nComparisonFailed (actual = {})".
                    format(self.last_function_result))
        dumpList.append(")")
        return ''.join(dumpList)

    def test (self):
        self.last_function_result = self.func(*self.args, **self.kwargs)
        return self.last_function_result == self.expected_function_result


class InRangePredicate(Predicate):
    """Predicate that, when tested, verifies that a given integer belongs to
       one or more user-specified ranges.

       NOTE, in Python, ranges are half-open, for example::

           >>> 1 in range(1,10)
           True

           >>> 9 in range(1,10)
           True

           >>> 10 in range(1,10)
           False



       This predicate tests `True` if the number is within the specified
       range, or is within at least one of a series of specified ranges.

       This predicate tests `False` if the number is outside the specified
       range or ranges.

       For example::

           from predcore import InRangePredicate

           allowable_numbers=[]
           allowable_ranges = [range(1,3), range(7,15)]
           for number in range(1,10):
               pred = InRangePredicate(number, *allowable_ranges)
               if pred:
                   allowable_numbers.append(number)
           print ("Allowable numbers : {}".format(allowable_numbers))


       Output from the previous example::

           Allowable numbers : [1, 2, 7, 8, 9]

    """
    def __init__(self, number, *args):
        """
        Parameters
        ----------

          number : `int`
               The number to check.

          args : variable number of positional range args
               A series of range arguments.

        """
        self.args = args
        self.number = number


    def dump(self):
        dumpList = []
        rangeList = []
        next_delimiter = ', '
        delimiter = ''
        for nextRange in self.args:
            if type(nextRange) is range:
                #
                # If possible, use start/stop members to reconstruct range
                # limits.  py3 timeit testing proves this is more real time
                # time efficient than the alternate algorithm.
                #
                rangeStart = nextRange.start
                rangeStop  = nextRange.stop
            else:
                #
                # This alternate range reconstruction algorithm is to be used
                # with py2 range and xrange.
                #
                rangeStart = nextRange[0]
                rangeStop  = nextRange[-1] + 1

            rangeList.append("{}({}, {})".\
                format(delimiter, rangeStart, rangeStop))

            if not delimiter:
                delimiter = next_delimiter
        dumpList.append("InRangePredicate (({} in {})".
                format(self.number, ''.join(rangeList)))
        if self.last_result is None:
            dumpList.append (" , \nNotTestedYet")
        else:
            if self.last_result:
                dumpList.append(", \nInRange")
            else:
                dumpList.append(", \nNotInRange")
        dumpList.append(")")
        return ''.join(dumpList)

    def test (self):
        for nextRange in self.args:
            if self.number in nextRange:
                return True
        return False


class IterableEqualPredicate(Predicate):
    """ Base class containing common logic for processing equality of
        an actual and an expected iterable object.
    """
    def __init__(self, actual_iterable, expected_iterable):
        """
        Parameters
        ----------

          actual_iterable : :ref:`python:collections-abstract-base-classes`
              The actual iterable object to check for equality.
              All items are first flattened into a single list
              before they are compared.

          expected_iterable : :ref:`python:collections-abstract-base-classes`
              The expected iterable object to check for equality.
              All items are first flattened into a single list
              before they are compared.


        A `ValueError` is raised if one or both of the inputs are not iterables.
        """
        self.actual_iterable = actual_iterable
        self.expected_iterable = expected_iterable

        if not isinstance(actual_iterable, collections.abc.Iterable):
            raise ValueError("actual_iterable is not an iterable")

        if not isinstance(expected_iterable, collections.abc.Iterable):
            raise ValueError("expected_iterable is not an iterable")

        self.actual_set = set([ item for item in flatten(actual_iterable) ])
        self.expected_set = set([ item for item in flatten(expected_iterable) ])
        self.intersect = self.actual_set.intersection(self.expected_set)

    @property
    def items_only_in_actual_set(self):
        return self.actual_set - self.intersect

    @property
    def items_only_in_expected_set(self):
        return self.expected_set - self.intersect

    @property
    def items_in_both_sets(self):
        return self.intersect

    def test(self):
        return self.actual_set == self.expected_set

    def dump_additional_data_on_test_failure(self, dumpList, printComma):
        pass

    def dump(self):
        dumpList = []
        dumpList.append("{} (\n".format(self.__class__.__name__))
        actual_items = [item for item in self.actual_set]
        expected_items = [item for item in self.expected_set]
        dumpList.append ("(test if actual {} \n== expected {})".format(
                            actual_items, expected_items))
        if self.last_result is None:
            dumpList.append (", \nNotTestedYet")
        else:
            if self.last_result:
                dumpList.append(", \nAreEqual")
            else:
                itemsOnlyInActualSet   = \
                    [item for item in self.items_only_in_actual_set]
                itemsOnlyInExpectedSet = \
                    [item for item in self.items_only_in_expected_set]
                dumpList.append(", \nAreNotEqual : (\n")
                if itemsOnlyInActualSet:
                    dumpList.append(
                        "ItemsInActualButNotInExpected : {}".
                        format(itemsOnlyInActualSet))
                    if itemsOnlyInExpectedSet:
                        dumpList.append(", \n")

                if itemsOnlyInExpectedSet:
                    dumpList.append(
                        "ItemsInExpectedButNotInActual : {}".
                        format(itemsOnlyInExpectedSet))
                self.dump_additional_data_on_test_failure(dumpList,
                    (itemsOnlyInActualSet or itemsOnlyInExpectedSet))
                dumpList.append(")")
        dumpList.append(")")
        return ''.join(dumpList)


class ListEqualPredicate(IterableEqualPredicate):
    """
    An object of this class tests `True` when an actual and an expected
    list are compared and are found to contain identical items.

    The order of each list's items is ignored and all duplicate items
    are removed.

    Each list must contain a series of objects that, once flattened, are
    hashable.  If not, an exception is raised on construction.

    For example::

            >>> from predcore import ListEqualPredicate
            >>> pred = ListEqualPredicate([1,2,3], [3,[2,1]])
            >>> True if pred else False
            True

            >>> pred = ListEqualPredicate([1,2,3], [4,3,2,1])
            >>> True if pred else False
            False

            >>> print(pred.dump())
            'ListEqualPredicate (
            (test if actual [1, 2, 3]
            == expected [1, 2, 3, 4]),
            AreNotEqual : (
            ItemsInExpectedButNotInActual : [4]))'


    """

    def __init__(self, actual_list, expected_list):
        """
        Parameters
        ----------

          actual_list : :ref:`Iterable <python:collections-abstract-base-classes>`
              The actual list to check for equality.
              All items are first flattened into a single list
              before they are compared.

          expected_list : :ref:`Iterable <python:collections-abstract-base-classes>`
              The expected list to check for equality.
              All items are first flattened into a single list
              before they are compared.


        A `ValueError` is raised if one or both of the inputs are not iterables.
        """

        super(ListEqualPredicate, self). \
            __init__(actual_list, expected_list)


class DictEqualPredicate(IterableEqualPredicate):
    """
    An object of this class tests `True` when an actual and an expected
    dictionary are compared and are found to be equal.

    For example::

            >>> from predcore import DictEqualPredicate
            >>> pred = DictEqualPredicate(
                {'first' : 1, 'second' : 2, 'third' : 3},
                {'third' : 3, 'second' : 2, 'first' : 1})
            >>> True if pred else False
            True

            >>> pred = DictEqualPredicate(
                {'first' : 1, 'second' : 2, 'third' : 3},
                {'third' : 30, 'second' : 2, 'first' : 1, 'fourth' : 4})
            >>> True if pred else False
            False

            >>> pred.dump()
            "DictEqualPredicate (
            (test if actual ['second', 'third', 'first']
            == expected ['second', 'third', 'fourth', 'first']),
            AreNotEqual : (
            ItemsInExpectedButNotInActual : ['fourth'],
            UnexpectedValue (Item third has value 3 (expected 30))))"

    """

    def __init__(self, actual_dict, expected_dict):
        """
        Parameters
        ----------

          actual_dict : :ref:`Mapping <python:collections-abstract-base-classes>`
              The actual `dictionary <dict>` to check for equality.

          expected_dict : :ref:`Mapping <python:collections-abstract-base-classes>`
              The expected `dictionary <dict>` to check for equality.


        A `ValueError` is raised if one or both of the inputs are not
        `dictionaries <dict>`.
        """

        if not isinstance(actual_dict, collections.abc.Mapping):
            raise ValueError("actual_dict is not a dictionary")

        if not isinstance(expected_dict, collections.abc.Mapping):
            raise ValueError("expected_dict is not a dictionary")

        super(DictEqualPredicate, self). \
            __init__(actual_dict, expected_dict)

        self.changedKeys = self.keys_with_changed_values()


    def keys_with_changed_values(self):
        return set(o for o in self.items_in_both_sets \
            if self.actual_iterable[o] != self.expected_iterable[o])


    def test(self):
        """ This predicate tests `True` only if the actual and expected
            dictionaries have the same keys, and all the values are equal.
        """
        return super(DictEqualPredicate, self).test() \
               and not bool(self.changedKeys)


    def dump_additional_data_on_test_failure(self, dumpList, printComma):
        if self.changedKeys:
            if printComma:
                dumpList.append(", \n")
            dumpList.append("UnexpectedValue (")
            delimiter = ''
            next_delimiter = ', \n'
            for key in self.changedKeys:
                dumpList.append("{}Item {} has value {} (expected {})".
                    format(delimiter, key, self.actual_iterable[key],
                                           self.expected_iterable[key]))
                if not delimiter:
                    delimiter = next_delimiter
            dumpList.append(")")


class IsSubsetPredicate(Predicate):
    """
    An object of this class tests `True` when an iterable is a subset of
    another iterable.

    The order of each list's items is ignored and all duplicate items
    are removed.

    Each list must contain a series of objects that, once flattened, are
    hashable.  If not, an exception is raised on construction.

    For example::

            >>> from predcore import IsSubsetPredicate
            >>> pred = IsSubsetPredicate([1,2,3], [5,4,3,2,1])
            >>> True if pred else False
            True

            >>> pred = IsSubsetPredicate([1,2,3], [4,3,1])
            >>> True if pred else False
            False

    """

    def __init__(self, first_iterable, is_subset_of_iterable):
        """
        Parameters
        ----------

          first_iterable : :ref:`Iterable <python:collections-abstract-base-classes>`
              The iterable whose items are tested as being a potential
              subset of `is_subset_of_iterable`.
              All items are first flattened into a single list
              before they are compared.

          is_subset_of_iterable : :ref:`Iterable <python:collections-abstract-base-classes>`
              The items in `first_iterable` are tested as being a potential
              subset of this iterable.
              All items are first flattened into a single list
              before they are compared.


        A `ValueError` is raised if one or both of the inputs are not iterables.
        """
        if not isinstance(first_iterable, collections.abc.Iterable):
            raise ValueError("first_iterable is not an iterable")

        if not isinstance(is_subset_of_iterable, collections.abc.Iterable):
            raise ValueError("is_subset_of_iterable is not an iterable")

        self.first_set = set([ item for item in flatten(first_iterable) ])
        self.is_subset_of_set = \
            set([ item for item in flatten(is_subset_of_iterable) ])


    def test(self):
        return self.first_set.issubset(self.is_subset_of_set)

    def dump(self):
        dumpList = []
        dumpList.append("{} (".format(self.__class__.__name__))
        first_items = [item for item in self.first_set]
        is_subset_of_items = [item for item in self.is_subset_of_set]
        dumpList.append ("(test if {} is a subset of {})".format(
                            first_items, is_subset_of_items))
        if self.last_result is None:
            dumpList.append (", \nNotTestedYet")
        else:
            if self.last_result:
                dumpList.append(", \nIsSubset")
            else:
                dumpList.append(", \nIsNotSubset")
        dumpList.append(")")
        return ''.join(dumpList)


class IsSupersetPredicate(Predicate):
    """
    An object of this class tests `True` when an iterable is a superset of
    another iterable.

    The order of each list's items is ignored and all duplicate items
    are removed.

    Each list must contain a series of objects that, once flattened, are
    hashable.  If not, an exception is raised on construction.

    For example::

            >>> from predcore import IsSupersetPredicate
            >>> pred = IsSupersetPredicate([1,2,3,4,5], [3,2])
            >>> True if pred else False
            True

            >>> pred = IsSupersetPredicate([1,2,3], [4,3,2,1])
            >>> True if pred else False
            False

    """

    def __init__(self, first_iterable, is_superset_of_iterable):
        """
        Parameters
        ----------

          first_iterable : :ref:`Iterable <python:collections-abstract-base-classes>`
              The iterable whose items are tested as being a potential
              superset of `is_superset_of_iterable`.
              All items are first flattened into a single list
              before they are compared.

          is_superset_of_iterable : :ref:`Iterable <python:collections-abstract-base-classes>`
              The items in `first_iterable` are tested as being a potential
              superset of this iterable.
              All items are first flattened into a single list
              before they are compared.


        A `ValueError` is raised if one or both of the inputs are not iterables.
        """

        if not isinstance(first_iterable, collections.abc.Iterable):
            raise ValueError("first_iterable is not an iterable")

        if not isinstance(is_superset_of_iterable, collections.abc.Iterable):
            raise ValueError("is_superset_of_iterable is not an iterable")

        self.first_set = set([ item for item in flatten(first_iterable) ])
        self.is_superset_of_set = \
            set([ item for item in flatten(is_superset_of_iterable) ])


    def test(self):
        return self.first_set.issuperset(self.is_superset_of_set)

    def dump(self):
        dumpList = []
        dumpList.append("{} (".format(self.__class__.__name__))
        first_items = [item for item in self.first_set]
        is_superset_of_items = [item for item in self.is_superset_of_set]
        dumpList.append ("(test if {} is a superset of {})".format(
                            first_items, is_superset_of_items))
        if self.last_result is None:
            dumpList.append (", \nNotTestedYet")
        else:
            if self.last_result:
                dumpList.append(", \nIsSuperset")
            else:
                dumpList.append(", \nIsNotSuperset")
        dumpList.append(")")
        return ''.join(dumpList)


class IsSequenceEqualDiffPredicate(Predicate):
    """
    An object of this class tests `True` when an actual list is equal to
    an expected list.

    If they are not equal, the `dump <Predicate.dump>` method contains the
    differences, expressed in a diff-like format.  It shows how one would
    transform the actual list into the expected list by adding and removing
    elements from the actual list.

    Each list must contain a series of objects that, once flattened, are
    hashable.  If not, an exception is raised on construction.

    By default, a nonzero `context_lines` excludes the majority of the
    unchanged items from the diff and clusters are presented and separated
    by "@@" lines detailing the diff's current slice within each sequence
    (this is similar to the concept of a 'unified diff')::

            >>> from predcore import IsSequenceEqualDiffPredicate
            >>> pred = IsSequenceEqualDiffPredicate([1,2,3,4,5], [1,2,3,4,5])
            >>> True if pred else False
            True

            >>> pred = IsSequenceEqualDiffPredicate([4,5,6,7], [1,2,3,4,5,6,7,8,9,10])
            >>> True if pred else False
            False

            >>> print(pred.dump())
            IsSequenceEqualDiffPredicate (
            (test if actual [4, 5, 6, 7] == expected [1,2,3,4,5,6,7,8,9,10]),
            AreNotEqual : (
            @@ -[0:0], +[0:3] @@
            +[1, 2, 3]
             [4]
            @@ -[3:4], +[6:7] @@
             [7]
            +[8, 9, 10]
            ))


    It is also possible to disable the `context_lines` feature and
    just request a straight diff::

            >>> pred = IsSequenceEqualDiffPredicate([4,5,6,7], [1,2,3,4,5,6,7,8,9,10],
                context_lines=0)
            >>> True if pred else False
            False

            >>> print(pred.dump())
            IsSequenceEqualDiffPredicate (
            (test if actual [4, 5, 6, 7] == expected [1,2,3,4,5,6,7,8,9,10]),
            AreNotEqual : (
            +[1, 2, 3]
             [4, 5, 6, 7]
            +[8, 9, 10]
            ))
    """

    def __init__(self, actual_sequence, expected_sequence, context_lines = 1):
        """
        Parameters
        ----------

          actual_sequence : :ref:`Sequence <python:collections-abstract-base-classes>`
              The actual sequence to check for equality.
              All items are first flattened into a single list
              before they are compared.

          expected_sequence : :ref:`Sequence <python:collections-abstract-base-classes>`
              The expected sequence to check for equality.
              All items are first flattened into a single list
              before they are compared.

          context_lines : `int`
              The number of unchanged elements to show before and after a
              cluster of diffs.  If set to 0, then no clustering is done and
              all elements are included in the diff.  This parameter defaults
              to 1.


        A `ValueError` is raised if one or both of the inputs are not sequences.
        """

        if not isinstance(actual_sequence, collections.abc.Sequence):
            raise ValueError("actual_sequence is not a sequence")

        if not isinstance(expected_sequence, collections.abc.Sequence):
            raise ValueError("expected_sequence is not a sequence")

        self.actual_sequence = [ item for item in flatten(actual_sequence) ]
        self.expected_sequence = [ item for item in flatten(expected_sequence) ]
        self.context_lines = context_lines

        self.diff_char = {'insert':'+', 'equal':' ', 'delete':'-'}

    def test(self):
        return self.actual_sequence == self.expected_sequence


    def format_diff_line(self, tag, i1, i2, j1, j2):
        """Format a line of SequenceMatcher diff output."""

        if tag == "insert" or tag == "equal":
            line = "{}{}\n".\
             format(self.diff_char[tag],self.expected_sequence[j1:j2])

        if tag == "delete":
            line = "{}{}\n".\
             format(self.diff_char[tag],self.actual_sequence[i1:i2])

        if tag == "replace":
            line = "{}{}\n{}{}\n".\
            format(self.diff_char['delete'], self.actual_sequence[i1:i2],
                   self.diff_char['insert'], self.expected_sequence[j1:j2])
        return line


    def dump(self):
        dumpList = []
        dumpList.append("{} (\n".format(self.__class__.__name__))
        dumpList.append ("(test if actual {} \n== expected {})".format(
                            self.actual_sequence, self.expected_sequence))
        if self.last_result is None:
            dumpList.append (", \nNotTestedYet")
        else:
            if self.last_result:
                dumpList.append(", \nAreEqual")
            else:
                dumpList.append(", \nAreNotEqual : (\n")

                s = SequenceMatcher(None,
                        self.actual_sequence,
                        self.expected_sequence, autojunk=False)
                if self.context_lines:
                    for cluster in s.get_grouped_opcodes(self.context_lines):
                        tag, i1, i2, j1, j2 = cluster[0]
                        dumpList.append( \
                            '@@ -[{}:{}], +[{}:{}] @@\n'.format(i1, i2, j1, j2))
                        for tag, i1, i2, j1, j2 in cluster:
                            dumpList.append(\
                                self.format_diff_line(tag, i1, i2, j1, j2))
                else:
                    for tag, i1, i2, j1, j2 in s.get_opcodes():
                        dumpList.append(\
                            self.format_diff_line(tag, i1, i2, j1, j2))
                dumpList.append(")")
        dumpList.append(")")
        return ''.join(dumpList)
