# -*- coding: utf-8 -*-
"""
Utilities for the configuration subpackage.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Dict
from typing import List
from typing import Tuple

import toml

from ..project.settings import PROJECT_DIRNAME
from .core import Config
from .core import PluginConfig
from .settings import CONFIG_FILES


#
#   Functions
#

def find_config_files(path: str) -> List[str]:
    """Find spines configuration files relevant to the given path

    This function will traverse the path tree upwards looking for spines
    configuration files until it reaches the primary project directory
    or the user's home directory.  The order of the returned files is
    the order to be used when creating/updating the configuration: the
    first path in the returned list is the lowest precedence, with each
    successive one taking higher precedence.

    Parameters
    ----------
    path : str
        Path to search for spines configuration files in.

    Returns
    -------
    :obj:`list` of :obj:`str`
        Path(s) to the configuration file(s) found, in the appropriate
        order.

    """
    ret = []
    p = Path(path).resolve()
    usr_home = Path.home()
    while p != p.root:
        for cfg_name in CONFIG_FILES:
            q = p.joinpath(cfg_name)
            if q.exists():
                ret.append(str(q))
                break
        if p == usr_home or p.joinpath(PROJECT_DIRNAME).exists():
            break
        p = p.parent
    if p != usr_home:
        for cfg_name in CONFIG_FILES:
            q = usr_home.joinpath(cfg_name)
            if q.exists():
                ret.append(str(q))
                break
    return reversed(ret)


def save_config(config: Config, *path: Tuple[str]) -> str:
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


def load_config(path: str, config_cls: [Type[Config], None] = None) -> Config:
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
    plugins = data.pop('plugin', [])

    loaded_cfg = config_cls(data)
    for plugin in plugins:
        loaded_cfg.add_plugin(plugin)
    return loaded_cfg


def save_plugin_config(config: PluginConfig, *path: Tuple[str]) -> str:
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
    path: str, config_cls: [Type[Config], None] = None
) -> PluginConfig:
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
    config: BaseConfig, *path: Tuple[str, ...]
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
