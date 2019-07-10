# -*- coding: utf-8 -*-
"""
Versioning objects for core classes.
"""
from __future__ import annotations

from typing import Mapping
from typing import Type
from typing import Union

import parver

from ..parameters.base import Parameter
from ..parameters.versioning import ParameterSignature
from ..utils.object import get_matching_attributes
from ..versioning.base import Signature
from ..versioning.core import ClassSignature
from ..versioning.mixins import VersionMixin
from .base import BaseObject


class BaseObjectSignature(ClassSignature):
    """
    Signature object for spines BaseObject objects.
    """
    __base_cls__: Type[BaseObject] = BaseObject

    def __init__(self, obj: Union[BaseObject, Type[BaseObject]]) -> None:
        self._params = self._get_parameters(obj)
        return super().__init__(obj)

    @classmethod
    def _get_parameters(
        cls, obj: Union[BaseObject, Type[BaseObject]]
    ) -> Mapping[str, Signature]:
        """Gets the relevant parameters and their signatures"""
        if not isinstance(obj, type):
            obj = obj.__class__
        ret = {}
        for param in get_matching_attributes(obj, Parameter):
            ret[param] = ParameterSignature(getattr(obj, param))
        return ret
