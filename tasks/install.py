# -*- coding: utf-8 -*-
"""
Tasks related to installation.
"""
#
#   Imports
#
import invoke

from .helpers import log as hlog


#
#   Helpers
#

def log(msg, level=None):
    hlog(msg, name='install', level=level)


#
#   Script functions
#

@invoke.task
def ipykernel(ctx, name=None, display_name=None):
    """Installs an IPyKernel for this project"""
    if not name:
        name = 'spines-dev'
    if not display_name:
        display_name = 'Spines Dev'

    log("Installing IPyKernel: %s (%s)" % (name, display_name))
    ctx.run(
        'python -m ipykernel install --user --name %s --display-name "%s"'
        % (name, display_name)
    )
