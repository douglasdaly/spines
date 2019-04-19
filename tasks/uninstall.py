# -*- coding: utf-8 -*-
"""
Uninstall tasks
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
    hlog(msg, name='uninstall', level=level)


#
#   Tasks
#

@invoke.task
def ipykernel(ctx, name=None):
    """Uninstalls the previously installed IPyKernel"""
    if not name:
        name = "spines-dev"

    log("Removing IPyKernel: %s" % name)
    ctx.run("jupyter kernelspec remove -f %s" % name)
