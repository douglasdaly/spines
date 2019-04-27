# -*- coding: utf-8 -*-
"""
Primary configuration interface
"""
#
#   Imports
#
from typing import Tuple
from typing import Type

from . import utils
from .core import Config


#
#   Variables
#

_GLOBAL_CONFIG = None


#
#   Functions
#

def get_config() -> Type[Config]:
    """Get the global spines configuration

    Returns
    -------
    Config
        The global configuration settings for the current spines
        project.

    """
    if _GLOBAL_CONFIG is None:
        load_config()
    return _GLOBAL_CONFIG.copy()


def set_config(*config: Tuple[Config], **settings) -> None:
    """Sets/updates the global spines configuration

    Parameters
    ----------
    config : Config, optional
        The new configuration object to use for the global
        configuration.
    settings : optional
        The settings in the global configuration file to update.

    """
    global _GLOBAL_CONFIG

    if config:
        config = config[0]
    else:
        config = _GLOBAL_CONFIG

    if settings:
        config.update(**settings)

    _GLOBAL_CONFIG = config
    return


# TODO: Finish implementing

def load_config(*path: Tuple[str]) -> Type[Config]:
    """Loads the global spines configuration

    Parameters
    ----------
    path : :obj:`str` (or multiple), optional
        File(s) to load the configuration from (defaults to the correct
        spines hierarchy for configuration files).

    Returns
    -------
    Config
        New global configuration object loaded.

    """
    if not path:
        path = utils.get_default_config_paths()

    for p in path:
        t_config = utils.load_config(p)

    pass
