# -*- coding: utf-8 -*-
"""
Uninstall tasks
"""
#
#   Imports
#
import invoke


#
#   Helpers
#

def log(msg, level=None):
    prt_msg = '[uninstall] '
    if level:
        prt_msg += '(%s) ' % (prt_msg, level)
    print(prt_msg + msg)


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

