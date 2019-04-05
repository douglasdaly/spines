# -*- coding: utf-8 -*-
"""
Spines

Backbones for parameterized models.
"""
from .models import Model
from .models import HyperModel
from .parameters import Parameter
from .parameters import BoundedParameter

__all__ = [
    # Models
    'Model',
    'HyperModel',
    # Parameters
    'Parameter',
    'BoundedParameter',
]

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
