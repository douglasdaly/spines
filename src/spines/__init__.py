# -*- coding: utf-8 -*-
"""
Spines

Skeletons for parameterized models.
"""
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

from .config import get_config
from .config import load_config
from .config import set_config
from .parameters import Parameter, HyperParameter
from .models import Model
from . import parameters
from . import transforms
from . import utils

__all__ = [
    # Models
    'Model',
    # Parameters
    'Parameter',
    'HyperParameter',
    # Config
    'get_config',
    'load_config',
    'set_config',
    # Submodules
    'parameters',
    'transforms',
    'utils',
]
