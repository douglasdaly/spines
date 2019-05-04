# -*- coding: utf-8 -*-
"""
Utilities for working with objects.
"""
#
#   Imports
#
from collections.abc import Iterable
from typing import Iterable as T_Iterable
from typing import Sequence


#
#   Functions
#

def get_overridden_methods(
    base: [type, object],
    cls: [type, object]
) -> Sequence[str]:
    """Get the overridden methods in an object.

    Parameters
    ----------
    base : :obj:`type` or :obj:`object`
        Base class to compare against.
    cls : :obj:`type` or :obj:`object`
        Class to get methods which are overridden from `base`.

    Returns
    -------
    :obj:`list` of :obj:`str`
        List of the methods which are overridden in the `cls`.

    """
    if not isinstance(base, type):
        base = base.__class__
    if not isinstance(cls, type):
        cls = cls.__class__
    common = base.__dict__.keys() & cls.__dict__.keys()
    return [
        m for m in common if base.__dict__[m] != cls.__dict__[m]
        and callable(cls.__dict__[m])
    ]


def get_matching_attributes(
    cls: [type, object],
    attribute_type: [type, T_Iterable[type], None] = None,
    visibility: [str, None] = None
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
                or (k.startswith('_') and 'protected' not in visibility)):
            continue
        if attribute_type and not (issubclass(v, attribute_type)
                or isinstance(v, attribute_type)):
            continue
        ret.append(k)
    return sorted(ret)
