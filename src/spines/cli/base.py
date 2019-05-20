# -*- coding: utf-8 -*-
"""
Base objects and settings for CLI interface.
"""
#
#   Imports
#
import os
from typing import Dict
from typing import List

from click import Group

from ..utils.crypto import verify_hashes
from ..utils.environment import is_truthy
from ..utils.module import load_modules
from .settings import TOOLS_FOLDER


#
#   Click customizations
#

class SpinesCLI(Group):
    """
    Customized click group class for Spines CLI
    """

    def __init__(self, name=None, commands=None, **attrs):
        super().__init__(name=name, commands=commands, **attrs)
        self._tools = self._get_tools()
        self._loaded = None
        return

    @property
    def tools(self) -> Dict[str, bool]:
        """dict: Mapping of available tools to verified status"""
        return self._tools.copy()

    @property
    def loaded(self) -> List[str]:
        """list: Listing of the loaded tools/plugins"""
        if self._loaded is not None:
            return self._loaded.copy()
        return []

    def parse_args(self, ctx, args):
        ctx.meta['develop'] = self._set_develop(ctx, args)
        if self._loaded is None:
            self._loaded = self._initialize(ctx)
        return super().parse_args(ctx, args)

    def _set_develop(self, ctx, args):
        """Determine if we're in develop mode or not"""
        if 'develop' in ctx.meta:
            return ctx.meta['develop']
        if '--develop' in args:
            return True
        if is_truthy('SPINES_DEVELOP'):
            return True
        return False

    def _initialize(self, ctx) -> List[str]:
        """Initializes the primary command to load extra components"""
        if ctx.meta.get('develop', False):
            tools_to_load = [x for x in self._tools.keys()]
        else:
            tools_to_load = [k for k, v in self._tools.items() if v]
        if tools_to_load:
            self._load_commands(tools_to_load, '.tools.', 'spines.cli')

        return tools_to_load

    def _get_tools(self):
        """Gets a mapping of installed tools to verified status"""
        tools = [
            x for x in os.listdir(TOOLS_FOLDER)
            if os.path.isdir(os.path.join(TOOLS_FOLDER, x))
        ]
        tools.sort()

        ret = {}
        for tool_dir in tools:
            try:
                f_res = verify_hashes(tool_dir)
                v_res = True
                for k, v in f_res.items():
                    v_res &= v
            except FileNotFoundError:
                v_res = False
            ret[tool_dir] = v_res
        return ret

    def _load_commands(self, commands, module, package) -> None:
        """Loads the given command modules from the given locations"""
        loaded_cmds = load_modules(module, submodules=commands,
                                   package=package)
        for cmd, mod in loaded_cmds.items():
            self.add_command(mod.cli, cmd)
        return
