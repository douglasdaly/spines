# -*- coding: utf-8 -*-
"""
Core classes for the spines versioning subpackage.
"""
#
#   Imports
#
from types import FunctionType
from typing import Any
from typing import OrderedDict as T_OrderedDict
from typing import Tuple
from typing import Type

from .base import BaseSignature
from .utils import get_function_bytes
from .utils import get_function_spec


#
#   Classes
#

class FunctionSignature(BaseSignature):
    """
    Signature class for versioning individual functions.
    """

    def __init__(self, obj: FunctionType) -> None:
        self._fn_argspecs, self._fn_rtype = get_function_spec(obj)
        super().__init__(obj)

    @property
    def arguments(self) -> T_OrderedDict[str, Tuple[type, Any]]:
        """OrderedDict: The signature function's argument specifications
        """
        return self._fn_argspecs.copy()

    @property
    def return_type(self) -> [type, None]:
        """type: The function's return type specification (if any)"""
        return self._fn_rtype

    def similar(
        self,
        other: Type['FunctionSignature'],
        strict: bool = False
    ) -> bool:
        """Compares this FunctionSignature to another for similarity

        Similarity is defined as having the same number and types of
        parameters and the same return type, regardless of the naming
        conventions used for each.

        Parameters
        ----------
        other : FunctionSignature
            The other function signature to compare with.
        strict : bool, optional
            Whether or not the types must be the same or if subclasses
            are permittable (the default is :obj:`False`, subclasses are
            also acceptable).

        Returns
        -------
        bool
            Whether or not the two functions are similar (as defined
            above).

        """
        if self._fn_rtype != other.return_type:
            return False
        if len(self._fn_argspecs) != len(other.arguments):
            return False

        s_values = [x[0] for x in self._fn_argspecs.values()]
        o_values = [x[0] for x in other.arguments.values()]
        if strict:
            for i, s_v in enumerate(s_values):
                if s_v != o_values[i]:
                    return False
        else:
            s_values = [x if x is not None else object for x in s_values]
            o_values = [x if x is not None else object for x in o_values]
            for i, s_v in enumerate(s_values):
                o_v = o_values[i]
                if not (issubclass(s_v, o_v) or issubclass(o_v, s_v)):
                    return False
        return True

    @classmethod
    def _get_bytes(cls, obj: FunctionType) -> bytes:
        """Gets the bytes to hash for a Function"""
        return get_function_bytes(obj)
