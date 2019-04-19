# -*- coding: utf-8 -*-
"""
Invoke commands for common tasks.
"""
#
#   Imports
#
import invoke

from . import install
from . import release
from . import uninstall


namespace = invoke.Collection(install, release, uninstall)

