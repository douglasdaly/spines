# -*- coding: utf-8 -*-
"""
Decorators for modifying function's inputs
"""
#
#   Imports
#
from functools import wraps
from inspect import signature
from typing import Tuple
from typing import Union


#
#   Decorators
#

def to_class(*args: Tuple[Union[int, str], ...]) -> Tuple[type, ...]:
    """Converts input(s) to types from inputs specified

    Parameters
    ----------
    args : :obj:`int` or :obj:`str`
        Input arguments to convert to class type, either the index of
        the argument in the wrapped function's arguments or the name
        of the argument or keyword argument.

    Returns
    -------
    callable
        The wrapped function.

    """
    def _wrap_outer(func):
        sig = signature(func, follow_wrapped=True)
        ind_args = [k for k, v in sig.parameters.items()
                    if v.default == sig.empty]

        a_idxs = []
        kw_nms = []
        for i in args:
            if isinstance(i, int):
                a_idxs.append[i]
            else:
                if i in ind_args:
                    a_idxs.append(ind_args.index(i))
                else:
                    kw_nms.append(i)
        a_idxs = sorted(a_idxs)

        @wraps(func)
        def _wrap_inner(*w_args, **w_kwargs):
            n_args = []
            for i, a in enumerate(w_args):
                if i in a_idxs and not isinstance(a, type):
                    n_args.append(a.__class__)
                else:
                    n_args.append(a)

            for kw in kw_nms:
                if not isinstance(w_kwargs[kw], type):
                    w_kwargs[kw] = w_kwargs[kw].__class__

            return func(*n_args, **w_kwargs)

        return _wrap_inner

    return _wrap_outer
