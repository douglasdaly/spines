# -*- coding: utf-8 -*-
"""
Main click command for spines command line tool.
"""
#
#   Imports
#
from click import group
from click import pass_context
from click import style
from click import version_option

from ..__version__ import __version__
from .base import SpinesCLI
from .options import core_options
from .options import pass_state
from .settings import CONTEXT_SETTINGS
from .settings import STYLIZED_NAME


@group(cls=SpinesCLI, invoke_without_command=True,
       context_settings=CONTEXT_SETTINGS)
@pass_state
@pass_context
@core_options
@version_option(prog_name=style(STYLIZED_NAME, fg='green', bold=True),
                version=__version__, message='%(prog)s %(version)34s\n')
def cli(ctx, state, **kwargs):
    """
    Spines
    """
    pass


if __name__ == "__main__":
    cli()