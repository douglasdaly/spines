# -*- coding: utf-8 -*-
"""
Common options for click commands.
"""
#
#   Imports
#
import click.types
from click import option


#
#   State object
#

class State(object):
    """
    Primary state object for common CLI options
    """

    def __init__(self):
        self.verbose = False


#
#   Option decorators
#

def verbose_option(f):
    """Verbosity option: --verbose -v"""
    def callback(ctx, param, value):
        state = ctx.ensure_object(State)
        if value is not None:
            state.verbose = value
        return value
    return option(
        '--verbose', '-v', is_flag=True, default=False, help="Verbose output",
        callback=callback, type=click.types.BOOL, expose_value=False,
        show_envvar=True
    )(f)


#
#   Option groups
#

def core_options(f):
    f = verbose_option(f)
    return f
