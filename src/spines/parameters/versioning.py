# -*- coding: utf-8 -*-
"""
Versioning objects for Parameters.
"""
#
#   Imports
#
from typing import Type

from ..versioning.core import ClassSignature
from .base import Parameter
from .base import HyperParameter


#
#   Signatures
#

class ParameterSignature(ClassSignature):
    """
    Signature for Parameter objects
    """
    __base_cls__ = Parameter

    def __init__(self, obj: Type[__base_cls__]) -> None:
        self._
        return super().__init__(obj)


class HyperParameterSignature(ParameterSignature):
    """
    Signature for HyperParameter objects
    """
    __base_cls__ = HyperParameter