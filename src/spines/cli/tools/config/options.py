# -*- coding: utf-8 -*-
"""
CLI options for the configuration tool.
"""
#
#   Imports
#
import click.types
from click import make_pass_decorator
from click import option


#
#   State object
#

class ConfigState(object):
    """
    State holder object for configuration tool.
    """

    def __init__(self):
        self.use_global = False


pass_config_state = make_pass_decorator(ConfigState, ensure=True)


#
#   Option decorators
#

def global_option(f):
    """Global config: --global"""
    def callback(ctx, param, value):
        state = ctx.ensure_object(ConfigState)
        if value is not None:
            state.use_global = value
        return value
    return option(
        '--global', is_flag=True, default=False,
        help="Use global configuration", callback=callback,
        type=click.types.BOOL, expose_value=False
    )(f)


#
#   Option groups
#

def config_options(f):
    f = global_option(f)
    return f
