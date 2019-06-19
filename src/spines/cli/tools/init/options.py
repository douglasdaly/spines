# -*- coding: utf-8 -*-
"""
Options for the initialization tool.
"""
import os

import click.types
from click import argument
from click import make_pass_decorator
from click import option

from ....project.settings import PROJECT_DIRNAME
from ....project.settings import PROJECT_FILE


#
#   State
#

class InitState(object):
    """
    State holder for init tool
    """

    def __init__(self):
        self.project_dir = os.path.abspath(os.curdir)
        self.force = False

    @property
    def file_exists(self) -> bool:
        """bool: Whether or not the project file exists"""
        return os.path.exists(
            os.path.join(self.project_dir, PROJECT_FILE)
        )

    @property
    def folder_exists(self) -> bool:
        """bool: Whether or not the project folder exists"""
        return os.path.exists(
            os.path.join(self.project_dir, PROJECT_DIRNAME)
        )


pass_init_state = make_pass_decorator(InitState, ensure=True)


#
#   Arguments
#

def path_argument(f):
    """Argument: PATH (optional)"""
    def callback(ctx, param, value):
        state = ctx.ensure_object(InitState)
        if value:
            state.project_dir = value
        return value
    return argument(
        'path', required=False, type=click.types.STRING, default='.',
        callback=callback
    )(f)


#
#   Options
#

def force_option(f):
    """Option: --force, -f"""
    def callback(ctx, param, value):
        state = ctx.ensure_object(InitState)
        if value:
            state.force = value
        return value
    return option(
        '--force', '-f', is_flag=True, default=False, type=click.types.BOOL,
        help="Don't prompt for confirmations", expose_value=False
    )(f)


#
#   Option groups
#

def init_options(f):
    f = force_option(f)
    return f
