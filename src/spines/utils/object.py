# -*- coding: utf-8 -*-
"""
Utilities for working with objects.
"""
#
#   Imports
#
from collections.abc import Iterable
import inspect
from types import FunctionType
from typing import Any
from typing import Iterable as T_Iterable
from typing import Sequence
from typing import Tuple

from ..decorators.input import to_class


#
#   Functions
#

def get_doc_string(obj: Any) -> str:
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
    ret = inspect.getdoc(obj)
    if ret:
        return inspect.cleandoc(ret)
    return ret


@to_class('base', 'cls')
def get_overridden(
    base: [type, object],
    cls: [type, object],
    *types: Tuple[type, ...]
) -> Sequence[str]:
    """Gets the overridden attributes in an object of the type(s) given

    Parameters
    ----------
    base : :obj:`type` or :obj:`object`
        Base class to compare against.
    cls : :obj:`type` or :obj:`object`
        Class to get attributes overridden from `base`.
    types : type, optional
        Overridden attribute type(s) to get.

    Returns
    -------
    :obj:`list` of :obj:`str`
        List of the overridden attributes in the `cls` of the type(s)
        specified.

    """
    if not types:
        types = (object,)
    common = base.__dict__.keys() & cls.__dict__.keys()
    return sorted(
        m for m in common
        if base.__dict__[m] != cls.__dict__[m]
        and isinstance(cls.__dict__[m], types)
    )


@to_class('base', 'cls')
def get_new(
    base: [type, object],
    cls: [type, object],
    *types: Tuple[type, ...]
) -> Sequence[str]:
    """Gets the new attributes in the given `cls` that aren't in `base`

    Parameters
    ----------
    base : :obj:`type` or :obj:`object`
        Base class to compare against.
    cls : :obj:`type` or :obj:`object`
        Class to get new attributes from `base`.
    types : type, optional
        New attribute type(s) to get.

    Returns
    -------
    :obj:`list` of :obj:`str`
        List of the new attributes in the `cls` of the type(s)
        specified.

    """
    if not types:
        types = (object,)
    return sorted(
        m for m in cls.__dict__.keys()
        if m not in base.__dict__.keys()
        and isinstance(cls.__dict__[m], types)
    )


def get_overridden_functions(
    base: [type, object],
    cls: [type, object]
) -> Sequence[str]:
    """Get the overridden functions in an object.

    Parameters
    ----------
    base : :obj:`type` or :obj:`object`
        Base class to compare against.
    cls : :obj:`type` or :obj:`object`
        Class to get functions which are overridden from `base`.

    Returns
    -------
    :obj:`list` of :obj:`str`
        List of the functions which are overridden in the `cls`.

    """
    return get_overridden(base, cls, FunctionType)


def get_new_functions(
    base: [type, object],
    cls: [type, object]
) -> Sequence[str]:
    """Gets functions in the given `cls` not in the `base`

    Parameters
    ----------
    base : :obj:`type` or :obj:`object`
        Base class to compare against.
    cls : :obj:`type` or :obj:`object`
        Class to get functions which are new from `base`.

    Returns
    -------
    :obj:`list` of :obj:`str`
        List of the functions which are in `cls` and not in `base`.

    """
    return get_new(base, cls, FunctionType)


def get_overridden_properties(
    base: [type, object],
    cls: [type, object]
) -> Sequence[str]:
    """Gets the properties in the given `cls` overriden from `base`

    Parameters
    ----------
    base : :obj:`type` or :obj:`object`
        Base class to compare against.
    cls : :obj:`type` or :obj:`object`
        Class to get properties which are overridden from `base`.

    Returns
    -------
    :obj:`list` of :obj:`str`
        List of the properties which are overridden in the `cls`.

    """
    return get_overridden(base, cls, property)


def get_new_properties(
    base: [type, object],
    cls: [type, object]
) -> Sequence[str]:
    """Gets properties in the given `cls` not in the `base`

    Parameters
    ----------
    base : :obj:`type` or :obj:`object`
        Base class to compare against.
    cls : :obj:`type` or :obj:`object`
        Class to get properties which are new from `base`.

    Returns
    -------
    :obj:`list` of :obj:`str`
        List of the properties which are in `cls` and not in `base`.

    """
    return get_new(base, cls, property)


# TODO: Implement the `regex` argument filter.

@to_class('cls')
def get_matching_attributes(
    cls: [type, object],
    attribute_type: [type, T_Iterable[type], None] = None,
    visibility: [str, None] = None,
    regex: [str, T_Iterable[str], None] = None
) -> [Sequence[str], None]:
    """Gets the specified attributes in the given class

    Parameters
    ----------
    cls : :obj:`type` or :obj:`object`
        Class to get attributes from.
    attribute_type : :obj:`type` or :obj:`Iterable` of :obj:`type`,
    optional
        Type(s) of the attributes to get from the class.
    visibility : :obj:`str` or :obj:`Iterable` of :obj:`str`, optional
        Visibility of the attributes to get, can be one or more of
        'public', 'protected' or 'private'.
    regex : :obj:`str` or :obj:`Iterable` of :obj:`str`, optional
        Regex string(s) to match attribute names against.

    Returns
    -------
    :obj:`list` of :obj:`str`
        The name(s) of the attribute(s) matching the given criteria, or
        :obj:`None` if none are found.

    """
    if not isinstance(cls, type):
        cls = cls.__class__

    if not hasattr(cls, '__dict__'):
        return None

    if attribute_type is not None:
        if not isinstance(attribute_type, Iterable):
            attribute_type = (attribute_type,)
        else:
            attribute_type = tuple(x for x in attribute_type)

    if visibility is not None:
        if isinstance(visibility, str):
            visibility = (visibility.lower(),)
        else:
            visibility = tuple(x.lower() for x in visibility)

    ret = []
    for k, v in cls.__dict__.items():
        if visibility and ((k.startswith('__') and 'private' not in visibility)
                or (k.startswith('_') and 'protected' not in visibility)):  # noqa
            continue
        if attribute_type and not (issubclass(v, attribute_type)
                or isinstance(v, attribute_type)):  # noqa
            continue
        ret.append(k)
    return sorted(ret)
