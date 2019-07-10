# -*- coding: utf-8 -*-
"""
Decorators for Models
"""
from __future__ import annotations

from functools import wraps
from typing import Callable


def negate(func: Callable) -> Callable:
    """Negate's the given functions output

    Parameters
    ----------
    func : callable
        The function to wrap.

    Returns
    -------
    callable
        The new function.

    """
    @wraps(func)
    def _wrapper(*args, **kwargs):
        return -func(*args, **kwargs)
    return _wrapper


def inverse(func: Callable) -> Callable:
    """Inverts the given function's output

    Parameters
    ----------
    func : callable
        The function to wrap.

    Returns
    -------
    callable
        The new function.

    """
    @wraps(func)
    def _wrapper(*args, **kwargs):
        return 1.0 / func(*args, **kwargs)
    return _wrapper
