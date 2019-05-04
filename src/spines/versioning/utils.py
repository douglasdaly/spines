# -*- coding: utf-8 -*-
"""
Utility functions for the spines versioning sub-package.
"""
#
#   Imports
#
from collections import OrderedDict
from collections.abc import Iterable
import difflib
import inspect
import re
from textwrap import dedent
from types import FunctionType
from typing import Any
from typing import Dict
from typing import Iterable as T_Iterable
from typing import List
from typing import OrderedDict as T_OrderedDict
from typing import Sequence
from typing import Tuple
import unicodedata

from .._vendored import autopep8 as _v_autopep8


#
#   Functions
#

def slugify(value: str, allow_unicode: bool = False) -> str:
    """Slugifys the given string

    Convert to ASCII if 'allow_unicode' is False. Convert spaces to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Convert to lowercase. Also strip leading and trailing whitespace.

    .. note::
        Modified (barely) from Django:
        https://github.com/django/django/blob/master/django/utils/text.py

    Parameters
    ----------
    value : str
        String to slugify.
    allow_unicode : bool, optional
        Whether or not to allow unicode characters.

    Returns
    -------
    str
        Slugified string.

    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')\
                           .decode('ascii')
    value = re.sub(r'[^\w\s-]', '_', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)


def get_doc_string(obj) -> str:
    """Gets the documentation string for the given object

    Parameters
    ----------
    obj : object
        Object to get docstring for.

    Returns
    -------
    str
        Docstring of the given object.

    """
    return inspect.cleandoc(inspect.getdoc(obj))


def get_diff(a: [str, T_Iterable[str]], b: [str, T_Iterable[str]], n=3):
    """Gets the differences between text data

    Parameters
    ----------
    a : :obj:`str` or :obj:`Iterable` of :obj:`str`
        Text to compare from.
    b : :obj:`str` or :obj:`Iterable` of :obj:`str`
        Text to compare with.
    n : int, optional
        Lines of context to show around differences.

    Returns
    -------
    str
        Differences between the texts.

    """
    if isinstance(a, str):
        a = a.splitlines()
    if isinstance(b, str):
        b = b.splitlines()
    return ''.join(
        difflib.context_diff(a, b, fromfile='Current', tofile='New', n=n)
    )


def get_changes(
    a: [str, T_Iterable[str]],
    b: [str, T_Iterable[str]]
) -> List[tuple]:
    """Gets the full set of changes required to go from a to b

    Parameters
    ----------
    a : :obj:`str` or :obj:`Iterable` of :obj:`str`
        Text to start from.
    b : :obj:`str` or :obj:`Iterable` of :obj:`str`
        Text to get changes to get to.

    Returns
    -------
    :obj:`list` of :obj:`tuple`
        List of five-tuples of operation, from start index, from end
        index, to start index and to end index.

    """
    if not isinstance(a, str):
        a = '\n'.join(a)
    if not isinstance(b, list):
        b = '\n'.join(b)
    s = difflib.SequenceMatcher(None, a, b)
    return s.get_opcodes()


# Function-related

def get_function_bytes(func: FunctionType) -> bytes:
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
    bytecode = get_function_bytecode(func)
    consts = func.__code__.co_consts[1:]
    dep_objs = func.__code__.co_names
    all_vars = func.__code__.co_varnames
    parameters, rtype = get_function_spec(func)

    ret = []
    for k, v in parameters.items():
        ret.append('parameter:%s[%s,%s]' % (k, v[0], v[0]))
    ret.append('rtype:%s' % rtype)
    for v in (consts, dep_objs, all_vars):
        for i_v in v:
            ret.append('str:%s' % i_v)
    return bytecode + ','.join(ret).encode()


def get_function_bytecode(func: FunctionType) -> bytes:
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


def get_function_source(func: FunctionType) -> str:
    """Gets the source code for the given function

    Parameters
    ----------
    func : callable
        Function to get source code of.

    Returns
    -------
    str
        Function source code, with PEP8 formatting applied.

    """
    raw_source = dedent(inspect.getsource(func))
    return _v_autopep8.fix_code(raw_source)


def get_function_spec(
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


def get_function_dependencies(func: FunctionType) -> Tuple[str, ...]:
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
