# -*- coding: utf-8 -*-
"""
Main click command for spines command line tool.
"""
#
#   Imports
#
from click import group
from click import pass_context
from click import version_option

import crayons

from ..__version__ import __version__
from .base import SpinesCLI
from .base import pass_state
from .settings import CONTEXT_SETTINGS


#
#   Commands
#

@group(cls=SpinesCLI, invoke_without_command=True,
       context_settings=CONTEXT_SETTINGS)
@pass_context
@pass_state
@version_option(prog_name=crayons.normal("spines", bold=True),
                version=__version__)
def cli(ctx, state, **kwargs):
    """Spines"""
    pass


#
#   Entry-point
#

if __name__ == "__main__":
    cli()
