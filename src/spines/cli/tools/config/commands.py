# -*- coding: utf-8 -*-
"""
Configuration CLI tool.
"""
#
#   Imports
#
import click
from click import pass_context

from ...base import pass_state
from ...settings import SUBCOMMAND_CONTEXT


#
#   Commands
#

@click.group('config', context_settings=SUBCOMMAND_CONTEXT)
@pass_context
@pass_state
def cli(ctx, state, **kwargs):
    """Spines config utility"""
    pass


@cli.command(context_settings=SUBCOMMAND_CONTEXT)
@pass_context
@pass_state
def set(ctx, state, **kwargs):
    """Sets a configuration value."""
    pass
