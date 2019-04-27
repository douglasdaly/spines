# -*- coding: utf-8 -*-
"""
Utilities for the configuration subpackage.
"""
#
#   Imports
#
import os
from typing import Dict
from typing import Tuple
from typing import Type

import toml

from .core import Config
from .core import PluginConfig


#
#   Functions
#

def save_config(config: Type[Config], *path: Tuple[str]) -> str:
    """Saves a configuration object to file

    Parameters
    ----------
    config : BaseConfig
        Configuration object to save to file.
    path : str
        Path name(s) to save the configuration to.

    Returns
    -------
    str
        Path to the saved file.

    """
    return _save_config_contents(config, *path)


def load_config(path: str, config_cls: [Type, None] = None) -> Type[Config]:
    """Loads a configuration from file

    Parameters
    ----------
    path : str
        Path to the file to load.
    config_cls : Config
        Configuration class to load data into.

    Returns
    -------
    Config
        Configuration object loaded from the file.
    """
    if config_cls is None:
        config_cls = Config
    data = _load_config_contents(path)
    plugins = data.pop('plugin')

    loaded_cfg = config_cls(data)
    for plugin in plugins:
        loaded_cfg.add_plugin(plugin)
    return loaded_cfg


def save_plugin_config(config: Type[PluginConfig], *path: Tuple[str]) -> str:
    """Saves a plugin configuration to file

    Parameters
    ----------
    config : PluginConfig
        Configuration object to save to file.
    path : str
        Path name(s) to save the configuration file to.

    Returns
    -------
    str
        Path to the saved file.

    """
    return _save_config_contents(config, *path)


def load_plugin_config(
    path: str, config_cls: [Type, None] = None
) -> Type[PluginConfig]:
    """Loads a plugin configuration from file

    Parameters
    ----------
    path : str
        Path to the file to load.
    config_cls : Config
        Configuration class to load data into.

    Returns
    -------
    PluginConfig
        The plugin configuration loaded.

    """
    if config_cls is None:
        config_cls = PluginConfig
    data = _load_plugin_config_contents(path)
    return config_cls(data)


def _save_config_contents(
    config: Type['BaseConfig'], *path: Tuple[str]
) -> str:
    """Saves the given configuration to file"""
    path = os.path.join(path)
    with open(path, 'w') as fout:
        toml.dump(config, fout)
    return path


def _load_config_contents(path: str) -> Dict:
    """Loads the contents of a configuration file"""
    with open(path, 'r') as fin:
        data = toml.load(fin)
    return data


def _load_plugin_config_contents(path: str) -> Dict:
    """Loads the contents of a plugin configuration file"""
    data = _load_config_contents(path)
    return data.get('plugin', data)
