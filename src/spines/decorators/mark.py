# -*- coding: utf-8 -*-
"""
Decorators related to marking objects and their attributes.
"""
#
#   Imports
#
from functools import wraps


#
#   Decorators
#

def override(func):
    """Marks the given function as overridden

    Parameters
    ----------
    func : callable
        The function to mark as overridden.

    Returns
    -------
    callable
        The new method with the overridden wrapper.

    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    wrapper.__overridden__ = True
    return wrapper
