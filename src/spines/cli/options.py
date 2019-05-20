# -*- coding: utf-8 -*-
"""
Common options for click commands.
"""
#
#   Imports
#
import os

import click.types
from click import echo
from click import make_pass_decorator
from click import option
from click import style

from ..project.utils import find_project_dir


#
#   State object
#

class State(object):
    """
    Primary state object for common CLI options and functions
    """

    def __init__(self):
        self.colors = True
        self.develop = False
        self.verbose = False
        self.project_dir = self._get_project_dir()

    def log(self, msg: str, component: str = None, level: str = None) -> None:
        """Displays a log message"""
        if not level:
            level = ''
        else:
            level = f'[{level}] '
        if not component:
            component = ''
        else:
            component = '({}) '.format(style(component, fg='yellow'))
        ret = f"{level}{component}{msg}"
        echo(ret)
        return

    def debug(self, msg: str, component: str = None) -> None:
        """Displays a debug message"""
        if self.develop:
            lvl = style('DEBUG', fg='blue', bold=True)
            return self.log(msg, component=component, level=lvl)
        return

    def info(self, msg: str, component: str = None) -> None:
        """Displays an info message"""
        if self.verbose:
            lvl = style('INFO', fg='green', bold=True)
            return self.log(msg, component=component, level=lvl)
        return

    def warn(self, msg: str, component: str = None) -> None:
        """Displays a warning message"""
        lvl = style('WARNING', fg='magenta', bold=True)
        return self.log(msg, component=component, level=lvl)

    def error(self, msg: str, component: str = None) -> None:
        """Displays an error message"""
        lvl = style('ERROR', fg='red', bold=True)
        return self.log(msg, component=component, level=lvl)

    def _get_project_dir(self) -> str:
        ret = os.path.abspath(os.curdir)
        ret = find_project_dir(ret) or ret
        return ret


pass_state = make_pass_decorator(State, ensure=True)


#
#   Options
#

def colors_option(f):
    """Color option: --colors"""
    def callback(ctx, param, value):
        state = ctx.ensure_object(State)
        if value is not None:
            state.colors = not value
        return value
    return option(
        '--no-colors', is_flag=True, default=False, help="Don't use colors",
        callback=callback, type=click.types.BOOL, expose_value=False,
        show_default=True, show_envvar=True
    )(f)


def develop_option(f):
    """Development option: --develop"""
    def callback(ctx, param, value):
        state = ctx.ensure_object(State)
        if value is not None:
            state.develop = value
        ctx.meta['develop'] = state.develop
        return value
    return option(
        '--develop', is_flag=True, default=False, help="Development mode",
        callback=callback, type=click.types.BOOL, expose_value=False,
        show_default=True, show_envvar=True
    )(f)


def project_dir_option(f):
    """Project home folder option: --project-dir"""
    def callback(ctx, param, value):
        state = ctx.ensure_object(State)
        if value is not None:
            state.project_dir = value
        return value
    return option(
        '--project-dir', default=None, help='Project directory',
        callback=callback, type=click.types.STRING, expose_value=False,
        show_default=False, show_envvar=True
    )(f)


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

def common_options(f):
    f = colors_option(f)
    f = develop_option(f)
    f = verbose_option(f)
    return f


def core_options(f):
    f = common_options(f)
    f = project_dir_option(f)
    return f
