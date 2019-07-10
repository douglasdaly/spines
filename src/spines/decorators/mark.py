# -*- coding: utf-8 -*-
"""
Decorators related to marking objects and their attributes.
"""
from __future__ import annotations

from functools import wraps
from typing import Callable


def override(func: Callable) -> Callable:
    """Marks the given function as overridden

    Parameters
    ----------
    func : Callable
        The function to mark as overridden.

    Returns
    -------
    Callable
        The new method with the overridden wrapper.

    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    wrapper.__overridden__ = True
    return wrapper
