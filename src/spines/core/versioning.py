# -*- coding: utf-8 -*-
"""
Versioning objects for core classes.
"""
#
#   Imports
#
from typing import Dict
from typing import Type

from ..parameters.base import Parameter
from ..parameters.versioning import ParameterSignature
from ..utils.object import get_matching_attributes
from ..versioning.base import Signature
from ..versioning.core import ClassSignature
from .base import BaseObject


#
#   Signatures
#

class BaseObjectSignature(ClassSignature):
    """
    Signature object for spines BaseObject objects.
    """
    __base_cls__ = BaseObject

    def __init__(self, obj: Type[__base_cls__]) -> None:
        self._params = self._get_parameters(obj)
        return super().__init__(obj)

    @classmethod
    def _get_parameters(cls, obj: type) -> Dict[str, Type[Signature]]:
        """Gets the relevant parameters and their signatures"""
        if not isinstance(obj, type):
            obj = obj.__class__
        ret = {}
        for param in get_matching_attributes(obj, Parameter):
            ret[param] = ParameterSignature(getattr(obj, param))
        return ret
