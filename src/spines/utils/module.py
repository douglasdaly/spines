# -*- coding: utf-8 -*-
"""
Utilities for working with modules.
"""
from importlib import import_module
from types import ModuleType
from typing import Dict
from typing import Sequence


def load_modules(
    module: str,
    submodules: [str, Sequence[str], None] = None,
    package: [str, None] = None
) -> Dict[str, ModuleType]:
    """Loads spines CLI commands from the given module

    Parameters
    ----------
    module : str
        Module to load (or load `submodules` from).
    submodules : :obj:`Iterable` of :obj:`str` or :obj:`str`, optional
        Submodule(s) to load from the specified module.
    package : str, optional
        Package where the `module` resides.

    Returns
    -------
    :obj:`dict` of :obj:`str` to command function
        Dictionary of commands and the function objects for them.

    """
    if submodules and not module.endswith('.'):
        module += '.'

    if not submodules:
        submodules = (module,)
        module = ''
    elif isinstance(submodules, str):
        submodules = (submodules,)

    ret = {}
    for submod in submodules:
        try:
            mod = import_module(f'{module}{submod}', package=package)
        except ImportError:
            continue
        ret[submod] = mod
    return ret
