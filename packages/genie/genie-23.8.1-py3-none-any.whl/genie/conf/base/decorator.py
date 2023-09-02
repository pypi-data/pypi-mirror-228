import logging
from functools import wraps
from copy import copy

from pyats.log.utils import banner


def log_it(func):
    """
    Log entering and exiting function. It includes,  arguments and returning
    element.
    """

    @wraps(func)
    def inner(*args, **kwargs):
        log = logging.getLogger(__name__)
        log.debug(banner('Entering {func} with argument: '
                         '{a} {k}'.format(func=func.__name__,
                                          a=args, k=kwargs)))
        try:
            ret = func(*args, **kwargs)
            msg = "return value {ret}".format(ret=ret)
            return ret
        except Exception as exc:
            msg = "exception {exc}".format(exc=exc)
            raise
        finally:
            log.debug(banner('Exiting {func} with '
                             '{msg}'.format(func=func.__name__, msg=msg)))
    return inner

# vim: ft=python et sw=4
