# -*- coding: utf-8 -*-
"""
Project initialization CLI tool.
"""
#
#   Imports
#
from click import command
from click import pass_context

from ...options import pass_state
from ...options import common_options
from ...settings import SUBCOMMAND_CONTEXT
from .options import init_options
from .options import pass_init_state
from .options import path_argument


#
#   Commands
#

@command('init', context_settings=SUBCOMMAND_CONTEXT)
@pass_init_state
@pass_state
@pass_context
@path_argument
@init_options
@common_options
def cli(ctx, state, init_state, path, **kwargs):
    """Project initialization tool."""
    pass
