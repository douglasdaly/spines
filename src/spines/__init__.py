# -*- coding: utf-8 -*-
"""
Spines

Skeletons for parameterized models.
"""
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

from .core import Model
from .parameters import Parameter, HyperParameter
from .parameters import Bounded, HyperBounded
from . import transforms
from . import utils

__all__ = [
    # Models
    'Model',
    # Parameters
    'Parameter',
    'HyperParameter',
    'Bounded',
    'HyperBounded',
    # Submodules
    'transforms',
    'utils',
]
