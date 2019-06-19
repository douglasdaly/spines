# -*- coding: utf-8 -*-
"""
Arguments and argument groups for the config tool.
"""
import click.types
from click import argument


#
#   Arguments
#

def name_argument(f):
    """Argument: NAME"""
    return argument(
        'name', required=True, type=click.types.STRING
    )(f)


def value_argument(f):
    """Argument: VALUE"""
    return argument(
        'value', required=True, type=click.types.STRING
    )(f)


#
#   Argument groups
#

def set_arguments(f):
    f = value_argument(f)
    f = name_argument(f)
    return f
