# -*- coding: utf-8 -*-
"""
Decorators for hooking functions.
"""
#
#   Imports
#
from functools import wraps


#
#   Decorators
#

def add_callback(
    callback: callable,
    *args,
    pass_args: bool = False,
    pass_kwargs: bool = False,
    pass_returned: bool = True,
    **kwargs
) -> callable:
    """Adds a the given callback to the function

    Parameters
    ----------
    callback : callable
        The callback to call when the function completes.
    args : optional
        Additional arguments to pass to the callback.
    pass_args : bool, optional
        Pass the arguments for the hooked function to the callback (the
        ordering, if this is set and `args` are specified, will be the
        function's args then the given `args`), the default is
        :obj:`False`.
    pass_kwargs : bool, optional
        Pass the keyword arguments for the hooked function to the
        callback (the precedence, if this is set and `kwargs` are
        specified, will be the function's kwargs updated with the given
        `kwargs`), the default is :obj:`False`.
    pass_returned : bool, optional
        Whether or not to pass the hooked function's return value to the
        callback as the first argument (default is :obj:`True`).
    kwargs : optional
        Additional keyword arguments to pass to the callback.

    Returns
    -------
    callable
        The hooked function.

    """
    def _wrap_outer(func):

        @wraps(func)
        def _wrap_inner(*fn_args, **fn_kwargs):
            ret = func(*fn_args, **fn_kwargs)

            if pass_args:
                args = fn_args + args
            if pass_kwargs:
                t_kws = fn_kwargs.copy()
                t_kws.update(kwargs)
                kwargs = t_kws

            if pass_returned:
                callback(ret, *args, **kwargs)
            else:
                callback(*args, **kwargs)

            return ret

        if not hasattr(_wrap_inner, '__hooked__'):
            _wrap_inner.__hooked__ = True
        return _wrap_inner

    return _wrap_outer
