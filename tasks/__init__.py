# -*- coding: utf-8 -*-
"""
Invoke commands for common tasks.
"""
#
#   Imports
#
import dotenv
import invoke

from . import develop
from . import docs
from . import install
from . import release
from . import uninstall

dotenv.load_dotenv()

namespace = invoke.Collection(develop, docs, install, release, uninstall)
