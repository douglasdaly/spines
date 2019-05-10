# -*- coding: utf-8 -*-
"""
Primary configuration interface
"""
#
#   Imports
#
from typing import Tuple
from typing import Type

from .._vendored.boltons.typeutils import make_sentinel

from . import utils
from .core import Config


#
#   Constants
#

_MISSING = make_sentinel(var_name='_MISSING')


#
#   Variables
#

_GLOBAL_CONFIG = None


#
#   Functions
#

def get_config(setting: str = _MISSING, default=_MISSING) -> Type[Config]:
    """Get the global spines configuration

    Parameters
    ----------
    setting : str, optional
        Setting(s) to get from the global configuration.
    default : optional
        Value to return if setting is not set (if not given an error
        will occur if accessing a non-existant setting).

    Returns
    -------
    :obj:`Config` or :obj:`dict`
        The global configuration settings for the current spines
        project or the values for the `settings` given.

    Raises
    ------
    ValueError
        If the given setting(s) doesn't exist and no `default` value is
        provided.

    """
    if _GLOBAL_CONFIG is None:
        load_config()

    if setting is _MISSING:
        return _GLOBAL_CONFIG.copy()

    if default is _MISSING:
        return _GLOBAL_CONFIG[setting]
    return _GLOBAL_CONFIG.get(setting, default)


def set_config(**settings) -> None:
    """Sets global configuration setting(s)

    Parameters
    ----------
    settings
        The setting(s) in the global configuration to update.

    """
    global _GLOBAL_CONFIG
    _GLOBAL_CONFIG = _update_config(_GLOBAL_CONFIG, **settings)
    return


def load_config(*path: Tuple[str], update: bool = False) -> None:
    """Loads the global spines configuration

    Parameters
    ----------
    path : :obj:`str` (or multiple), optional
        File(s) to load the configuration from (defaults to the correct
        spines hierarchy for configuration files).
    update : bool, optional
        Update the current configuration as opposed to replacing it with
        the newly loaded on (default is :obj:`False`, replace it).

    """
    global _GLOBAL_CONFIG

    if not path:
        path = utils.find_config_files('.')

    if update:
        config = _GLOBAL_CONFIG
    else:
        config = Config()

    for p in path:
        config = _update_config(config, utils.load_config(p))

    _GLOBAL_CONFIG = config
    return


def _update_config(
    config: Type[Config],
    *other: Tuple[Type[Config]],
    **settings
) -> Type[Config]:
    """Updates the given configuration object"""
    updated = config.copy()
    for other_cfg in other:
        updated.update(other_cfg)

    if settings:
        updated.update(**settings)

    return updated
