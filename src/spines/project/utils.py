# -*- coding: utf-8 -*-
"""
Utility funtions for the project subpackage.
"""
#
#   Imports
#
from pathlib import Path

from .settings import PROJECT_DIRNAME


#
#   Functions
#

def find_project_dir(path: str = None) -> str:
    """Finds the project's base directory

    Parameters
    ----------
    path : str, optional
        Initial path to start searching from, if not given it will start
        from the current working directory.

    Returns
    -------
    str
        Path to the found project directory, or :obj:`None` if not
        found.

    """
    path = path or Path.cwd()
    c_path = Path(path).resolve()
    usr_home = Path.home()
    while c_path != c_path.root:
        if c_path == usr_home:
            return None
        elif c_path.joinpath(PROJECT_DIRNAME).exists():
            return str(c_path)
        c_path = c_path.parent
    return None
