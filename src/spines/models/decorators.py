# -*- coding: utf-8 -*-
"""
Decorators for Models
"""
#
#   Imports
#
from functools import wraps
from typing import Type

from ..parameters.store import ParameterStore


#
#   Decorators
#

def finalize_pre(func, store: Type[ParameterStore]):
    """Finalizes the store prior to executing the function

    Parameters
    ----------
    func : callable
        The function to wrap.
    store : ParameterStore
        The parameter store to finalize.

    Returns
    -------
    callable
        The wrapped function.

    Raises
    ------
    MissingParameterException
        If there's a parameter missing from the required parameters in
        the given `store`.

    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not store.final:
            store.finalize()
        return func(*args, **kwargs)
    return wrapper


def finalize_post(func, store: Type[ParameterStore]):
    """Finalizes the store prior to executing the function

    Parameters
    ----------
    func : callable
        The function to wrap.
    store : ParameterStore
        The parameter store to finalize.

    Returns
    -------
    callable
        The wrapped function.

    Raises
    ------
    MissingParameterException
        If there's a parameter missing from the required parameters in
        the given `store`.

    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        if not store.final:
            store.finalize()
        return ret
    return wrapper


def inverse_from_func(func, from_fn):
    """Creates a function from the given error function

    Parameters
    ----------
    func : callable
        The function to replace.
    from_fn : callable
        The other function to use as the basis for the new function.

    Returns
    -------
    callable
        The new function.

    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return -from_fn(*args, **kwargs)
    return wrapper


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
    wrapper.__is_overridden = True
    return wrapper
