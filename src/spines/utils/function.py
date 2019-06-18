# -*- coding: utf-8 -*-
"""
Utilities for working with functions.
"""
from collections import OrderedDict
import inspect
from types import FunctionType
from typing import Any
from typing import Dict
from typing import Tuple

try:
    from typing import OrderedDict as T_OrderedDict
except ImportError:
    T_OrderedDict = Dict

from .string import format_code_style


def get_hash_bytes(func: FunctionType) -> bytes:
    """Gets a byte-representation of a function object for hashing

    Parameters
    ----------
    func : callable
        Function to get bytes for.

    Returns
    -------
    bytes
        Byte representation of the function.

    """
    bytecode = get_bytecode(func)
    consts = func.__code__.co_consts[1:]
    dep_objs = func.__code__.co_names
    all_vars = func.__code__.co_varnames
    parameters, rtype = get_specification(func)

    ret = []
    for k, v in parameters.items():
        ret.append('parameter:%s[%s,%s]' % (k, v[0], v[0]))
    ret.append('rtype:%s' % rtype)
    for v in (consts, dep_objs, all_vars):
        for i_v in v:
            ret.append('str:%s' % i_v)
    return bytecode + ','.join(ret).encode()


def get_bytecode(func: FunctionType) -> bytes:
    """Gets the byte code for the given function object

    Parameters
    ----------
    func : callable
        Function to get bytes for.

    Returns
    -------
    bytes
        Byte representation of the function.

    """
    return func.__code__.co_code


def get_specification(
    func: FunctionType
) -> Tuple[T_OrderedDict[str, Tuple[type, Any]], type]:
    """Gets the parameters and return type for a function object

    Parameters
    ----------
    func : callable
        Function to get parameters for.

    Returns
    -------
    :obj:`OrderedDict` of :obj:`str` to :obj:`Tuple` of (:obj:`type:,
    :obj:`object`), :obj:`type`
        Tuple with the first element as a dictionary of parameter name
        to parameter type and default value (if any are specified,
        otherwise :obj:`object` for each type and :obj:`None` for the
        default value).  The second element as the return type for the
        function (if specified, otherwise :obj:`object`).

    """
    fn_sig = inspect.signature(func)
    params = OrderedDict()
    for k, v in fn_sig.parameters.items():
        params[k] = (
            None if v.annotation is fn_sig.empty else v.annotation,
            None if v.default is fn_sig.empty else v.default
        )
    rtype = (None if fn_sig.return_annotation is fn_sig.empty
             else fn_sig.return_annotation)
    return params, rtype


def get_dependencies(func: FunctionType) -> Tuple[str, ...]:
    """Gets the names of other callables the given one uses

    Parameters
    ----------
    func : callable
        Function to get the dependent callables for.

    Returns
    -------
    :obj:`tuple` of :obj:`str`
        The names of the callables used in the given function, in the
        order they're called in the function.

    """
    return func.__code__.co_names


def get_source(func: FunctionType, pep8: bool = True) -> str:
    """Gets the source code for the given function

    Parameters
    ----------
    func : callable
        Function to get source code of.
    pep8 : bool, optional
        Format the code to PEP8 standards (default is :obj:`True`).

    Returns
    -------
    str
        Function source code, with optional PEP8 formatting applied.

    """
    code = inspect.getsource(func)
    if code and format:
        return format_code_style(code)
    return code
