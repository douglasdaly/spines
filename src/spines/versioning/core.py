# -*- coding: utf-8 -*-
"""
Core classes for the spines versioning subpackage.
"""
#
#   Imports
#
from collections import OrderedDict
from textwrap import indent
from types import FunctionType
from typing import Any
from typing import Callable
from typing import Dict
from typing import Mapping
from typing import Tuple
from typing import Type

try:
    from typing import OrderedDict as T_OrderedDict
except ImportError:
    T_OrderedDict = Dict

from ..utils.function import get_hash_bytes
from ..utils.function import get_source as get_source_fn
from ..utils.function import get_specification
from ..utils.object import get_doc_string
from ..utils.object import get_new_functions
from ..utils.object import get_new_properties
from ..utils.object import get_overridden_functions
from ..utils.object import get_overridden_properties
from ..utils.property import get_source as get_source_prop
from ..utils.string import INDENT_TAB
from ..utils.string import format_code_style
from .base import Signature


#
#   Classes
#

class FunctionSignature(Signature):
    """
    Signature class for versioning individual functions.
    """

    def __init__(self, obj: FunctionType) -> None:
        self._fn_argspecs, self._fn_rtype = get_specification(obj)
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
        return get_hash_bytes(obj)

    def _get_source(self, obj: FunctionType) -> str:
        """Gets the source code for the function given"""
        return get_source_fn(obj)


class PropertySignature(Signature):
    """
    Signature for properties
    """
    __function_signature__ = FunctionSignature

    def __init__(self, obj: property, name: str) -> None:
        self._fdel = self._get_property_function(obj, 'fdel')
        self._fget = self._get_property_function(obj, 'fget')
        self._fset = self._get_property_function(obj, 'fset')
        return super().__init__(obj, name)

    @property
    def getter(self) -> [Type[FunctionSignature], None]:
        """FunctionSignature: Signature for this property's fget"""
        return self._fget

    @property
    def setter(self) -> [Type[FunctionSignature], None]:
        """FunctionSignature: Signature for this property's fset"""
        return self._fset

    @property
    def deleter(self) -> [Type[FunctionSignature], None]:
        """FunctionSignature: Signature for this property's fdel"""
        return self._fdel

    @classmethod
    def _get_property_function(
        cls,
        obj: [type, object],
        method: str
    ) -> [Type[FunctionSignature], None]:
        """Helper function to get property's various methods"""
        meth = getattr(obj, method)
        if meth is None:
            return None
        return cls.__function_signature__(meth)

    def _get_bytes(self, obj: [type, object]) -> bytes:
        """Gets the hash bytes for the property"""
        ret = self._name.encode()
        if self._fget:
            ret += self._fget.hash_bytes
        if self._fset:
            ret += self._fset.hash_bytes
        if self._fdel:
            ret += self._fdel.hash_bytes
        return ret

    def _get_source(self, obj: property) -> str:
        """Gets the source code for the property given"""
        return get_source_prop(obj)


class ClassSignature(Signature):
    """
    Signature for classes
    """
    __base_cls__ = object
    __function_signature__ = FunctionSignature
    __property_signature__ = PropertySignature

    def __init__(self, obj: [type, object]) -> None:
        if not isinstance(obj, type):
            obj = obj.__class__
        self._functions = self._get_functions(obj)
        self._properties = self._get_properties(obj)
        return super().__init__(obj)

    @property
    def functions(self) -> Dict[str, Type[FunctionSignature]]:
        """dict: Function names and signatures for this class"""
        return self._functions.copy()

    @property
    def properties(self) -> Dict[str, Type[PropertySignature]]:
        """dict: Properties and their signatures for this class"""
        return self._properties.copy()

    def _get_bytes(self, obj: Type[__base_cls__]) -> bytes:
        """Gets the bytes relevant to the hash function"""
        ret = None
        for prop in sorted(self._properties.keys()):
            t_bytes = self._properties[prop].hash_bytes
            if ret is None:
                ret = t_bytes
            else:
                ret += t_bytes
        for fn in sorted(self._functions.keys()):
            t_bytes = self._functions[fn].hash_bytes
            if ret is None:
                ret = t_bytes
            else:
                ret += t_bytes
        return ret

    def _get_source(self, obj) -> str:
        """Gets the source code for the given class"""
        if not isinstance(obj, type):
            obj = obj.__class__

        docstr = get_doc_string(obj)
        prop_source = self._get_signature_dict_sources(
            obj, self._properties, get_source_prop
        )
        func_source = self._get_signature_dict_sources(
            obj, self._functions, get_source_fn
        )

        ret = "class {class_name}({base_classes}):\n".format(
            class_name=obj.__name__,
            base_classes=', '.join([x.__name__ for x in obj.__bases__])
        )
        if docstr:
            ret += indent('"""%s"""\n' % docstr, INDENT_TAB)
        ret += '\n'
        if '__init__' in func_source.keys():
            ret += indent(func_source.pop('__init__') + '\n', INDENT_TAB)
        for prop, src in prop_source.items():
            ret += indent(src + '\n', INDENT_TAB)
        for fn, src in func_source.items():
            ret += indent(src + '\n', INDENT_TAB)

        return format_code_style(ret)

    @classmethod
    def _get_signature_dict_sources(
        cls,
        obj,
        signature_dict: Mapping[str, Type[Signature]],
        source_func: Callable
    ) -> T_OrderedDict[str, str]:
        """Helper to get sources from a dictionary of Signatures"""
        ret = OrderedDict()
        for k in sorted(signature_dict.keys()):
            v = signature_dict[k]
            v_src = getattr(v, 'source', None)
            if v_src:
                ret[k] = v_src
            else:
                ret[k] = source_func(obj.__dict__[k])
        return ret

    @classmethod
    def _get_functions(cls, obj: type) -> Dict[str, Type[FunctionSignature]]:
        """Gets the relevant functions and their signatures"""
        relevant_functions = get_overridden_functions(cls.__base_cls__, obj) \
            + get_new_functions(cls.__base_cls__, obj)
        ret = {}
        for fn in relevant_functions:
            ret[fn] = cls.__function_signature__(getattr(obj, fn))
        return ret

    @classmethod
    def _get_properties(cls, obj: type) -> Dict[str, Type[PropertySignature]]:
        """Gets the relevant properties and their signatures"""
        relevant_properties = (
            get_overridden_properties(cls.__base_cls__, obj)
            + get_new_properties(cls.__base_cls__, obj)
        )
        ret = {}
        for p in relevant_properties:
            ret[p] = cls.__property_signature__(obj.__dict__[p], p)
        return ret
