# -*- coding: utf-8 -*-
"""
Click settings and constants for the CLI interface.
"""
import os
import textwrap


STYLIZED_NAME = textwrap.indent(textwrap.dedent(
    """     __   __          ___  __
    /__` |__) | |\ | |__  /__`
    .__/ |    | | \| |___ .__/
    """), '  ')

TOOLS_FOLDER = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'tools')
)

CONTEXT_SETTINGS = {
    "help_option_names": ["-h", "--help"],
    "auto_envvar_prefix": "SPINES",
}

SUBCOMMAND_CONTEXT = CONTEXT_SETTINGS.copy()
SUBCOMMAND_CONTEXT.update({
    'ignore_unknown_options': True,
    'allow_extra_args': True,
})
