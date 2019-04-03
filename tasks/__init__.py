# -*- coding: utf-8 -*-
"""
Invoke commands for common tasks.
"""
#
#   Imports
#
import invoke

from . import release


namespace = invoke.Collection(release)

