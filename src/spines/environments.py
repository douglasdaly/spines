# -*- coding: utf-8 -*-
"""
Environment settings/variables used by spines.
"""
#
#   Imports
#
import os
import sys

from appdirs import user_cache_dir


#
#   Helpers
#

def _is_env_truthy(name):
    """An environment variable is truthy if it exists and isn't one of
    (0, false, no, off)
    """
    if name not in os.environ:
        return False
    return os.environ.get(name).lower() not in ("0", "false", "no", "off")


#
#   Environment variables
#

SPINES_CACHE_DIR = os.environ.get("SPINES_CACHE_DIR", user_cache_dir("spines"))
"""Location for Spines to store cached objects

Defaults to the user's cache directory.
"""

SPINES_DISPLAY_COLOR = os.environ.get("SPINES_DISPLAY_COLOR", True)
"""Whether or not to use color in the command-line interface

Default is :obj:`True`, use color.
"""

SPINES_DISPLAY_SPINNER = os.environ.get("SPINES_DISPLAY_SPINNER", False)
"""Whether or not to use loading spinner animations

Default is :obj:`True`, use spinners.
"""
