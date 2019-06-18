# -*- coding: utf-8 -*-
"""
Environment settings/variables used by spines.
"""
import os

from appdirs import user_cache_dir


SPINES_CACHE_DIR = os.environ.get("SPINES_CACHE_DIR", user_cache_dir("spines"))
"""Location for Spines to store cached objects

Defaults to the user's cache directory.
"""

SPINES_DISPLAY_COLOR = os.environ.get("SPINES_DISPLAY_COLOR", True)
"""Whether or not to use color in the command-line interface

Default is :obj:`True`, use color.
"""

SPINES_DISPLAY_EMOJIS = os.environ.get("SPINES_DISPLAY_EMOJIS", True)
"""Whether or not to display emojis in the command-line interface

Default is :obj:`True`, diplay emojis.
"""

SPINES_DISPLAY_SPINNER = os.environ.get("SPINES_DISPLAY_SPINNER", True)
"""Whether or not to use loading spinner animations

Default is :obj:`True`, use spinners.
"""
