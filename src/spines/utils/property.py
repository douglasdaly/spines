# -*- coding: utf-8 -*-
"""
Utilities for working with properties.
"""
#
#   Imports
#
from .function import get_source as get_source_fn
from .string import format_code_style


#
#   Functions
#

def get_source(prop: property, pep8: bool = True) -> str:
    """Gets the source code for the given property

    Parameters
    ----------
    prop : property
        The property object to get source code for.
    pep8 : bool, optional
        Whether or not to format the code to PEP8 (default is
        :obj:`True`).

    Returns
    -------
    str
        Source code for the given property.

    """
    ret = ""
    if prop.fget:
        ret += get_source_fn(prop.fget) + '\n'
    if prop.fset:
        ret += get_source_fn(prop.fset) + '\n'
    if prop.fdel:
        ret += get_source_fn(prop.fdel) + '\n'
    if pep8:
        ret = format_code_style(ret)
    return ret
