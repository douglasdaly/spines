# -*- coding: utf-8 -*-
"""
Base objects and settings for CLI interface.
"""
#
#   Imports
#
import os

from click import make_pass_decorator
from click import Group

from ..utils.module import load_modules
from .options import State
from .settings import TOOLS_FOLDER


#
#   Click stuff
#

pass_state = make_pass_decorator(State, ensure=True)


#
#   Spines CLI
#

class SpinesCLI(Group):
    """
    Customized click group class for Spines CLI
    """

    def __init__(self, name=None, commands=None, **attrs):
        super().__init__(name, commands, **attrs)
        self._load_tools()
        return

    def _load_tools(self):
        tools = [
            x for x in os.listdir(TOOLS_FOLDER)
            if os.path.isdir(os.path.join(TOOLS_FOLDER, x))
        ]
        return self._load_commands(tools, '.tools.', 'spines.cli')

    def _load_commands(self, commands, module, package):
        loaded_cmds = load_modules(module, submodules=commands,
                                   package=package)
        for cmd, mod in loaded_cmds.items():
            self.add_command(mod.cli, cmd)
        return
