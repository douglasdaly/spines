# -*- coding: utf-8 -*-
"""
Decorators for parameters module.
"""
#
#   Imports
#
from functools import wraps


#
#   Decorators
#

def state_changed(func):
    """Decorator indicating a function which changes the state

    Parameters
    ----------
    func : callable
        The function to wrap.

    Returns
    -------
    callable
        The wrapped function.

    """
    @wraps(func)
    def wrapped(self, *args, **kwargs):
        ret = func(self, *args, **kwargs)
        self._finalized = False
        return ret
    return wrapped
