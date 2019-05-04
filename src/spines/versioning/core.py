# -*- coding: utf-8 -*-
"""
Core classes for the spines versioning subpackage.
"""
#
#   Imports
#
from types import FunctionType
from typing import Any
from typing import Dict
from typing import OrderedDict as T_OrderedDict
from typing import Tuple
from typing import Type

from ..core.base import BaseObject
from ..parameters.base import HyperParameter
from ..parameters.base import Parameter
from ..utils.objects import get_matching_attributes
from ..utils.objects import get_overridden_methods
from .base import BaseSignature
from .base import BaseVersion
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
        return super().__init__(obj)

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

    def _get_bytes(self, obj: FunctionType) -> bytes:
        """Gets the bytes to hash for a Function"""
        return get_function_bytes(obj)


class ClassSignature(BaseSignature):
    """
    Signature object for classes
    """
    __base_cls__ = object

    def __init__(self, obj):
        if not isinstance(obj, type):
            obj = obj.__class__
        self._functions = self._get_functions(obj)
        return super().__init__(obj)

    def _get_bytes(self, obj: Type[__base_cls__]) -> bytes:
        """Gets the bytes relevant to the hash function"""
        ret = None
        for fn in sorted(self._functions.keys()):
            t_bytes = self._functions[fn].hash_bytes
            if ret is None:
                ret = t_bytes
            else:
                ret += t_bytes
        return ret

    @classmethod
    def _get_functions(cls, obj: type) -> Dict[str, Type[BaseSignature]]:
        """Gets the relevant functions and their signatures"""
        ret = {}
        for fn in get_overridden_methods(cls.__base_cls__, obj):
            ret[fn] = FunctionSignature(getattr(obj, fn))
        return ret


class ParameterSignature(ClassSignature):
    """
    Signature for Parameter objects
    """
    __base_cls__ = Parameter

    def __init__(self, obj: Type[__base_cls__]) -> None:
        return super().__init__(obj)


class HyperParameterSignature(ParameterSignature):
    """
    Signature for HyperParameter objects
    """
    __base_cls__ = HyperParameter


class ObjectVersion(BaseVersion, ClassSignature):
    """
    Version object for versioning spines BaseObject objects.
    """
    __base_cls__ = BaseObject

    def __init__(self, obj: Type[__base_cls__]) -> None:
        self._params = self._get_parameters(obj)
        return super().__init__(obj)

    @classmethod
    def _get_parameters(cls, obj: type) -> Dict[str, Type[BaseSignature]]:
        """Gets the relevant parameters and their signatures"""
        ret = {}
        for param in get_matching_attributes(obj, Parameter):
            ret[param] = ParameterSignature(getattr(obj, param))
        return ret
