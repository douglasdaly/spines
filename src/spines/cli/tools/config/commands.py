# -*- coding: utf-8 -*-
"""
Configuration CLI tool.
"""
from click import group
from click import pass_context

from ....config import get_config
from ...options import common_options
from ...options import pass_state
from ...settings import SUBCOMMAND_CONTEXT
from .arguments import name_argument
from .arguments import set_arguments
from .options import config_options
from .options import pass_config_state


@group('config', context_settings=SUBCOMMAND_CONTEXT)
@pass_config_state
@pass_state
@pass_context
@config_options
@common_options
def cli(ctx, state, cfg_state, **kwargs):
    """Configuration utility for Spines."""
    pass


@cli.command(context_settings=SUBCOMMAND_CONTEXT)
@pass_config_state
@pass_state
@pass_context
@config_options
@common_options
def init(ctx, state, cfg_state, **kwargs):
    """Initializes a new Spines config file."""
    pass


@cli.command(context_settings=SUBCOMMAND_CONTEXT)
@pass_config_state
@pass_state
@pass_context
@config_options
@common_options
def list(ctx, state, cfg_state, **kwargs):
    """Lists configuration settings."""
    cfg = get_config()
    for k, v in cfg.items():
        if k.startswith('_'):
            continue
        print("%-20s  %s" % (k, v))
    return


@cli.command(context_settings=SUBCOMMAND_CONTEXT)
@pass_config_state
@pass_state
@pass_context
@set_arguments
@config_options
@common_options
def set(ctx, state, cfg_state, name, value, **kwargs):
    """Set a configuration setting."""
    pass


@cli.command(context_settings=SUBCOMMAND_CONTEXT)
@pass_config_state
@pass_state
@pass_context
@name_argument
@config_options
@common_options
def unset(ctx, state, cfg_state, name, **kwargs):
    """Unset a configuration setting."""
    pass


@cli.group('plugin', context_settings=SUBCOMMAND_CONTEXT)
@pass_config_state
@pass_state
@pass_context
@config_options
@common_options
def plugin(ctx, state, cfg_state, **kwargs):
    """Plugin configuration tools."""
    pass
