# -*- coding: utf-8 -*-
"""
Utility funtions for the project subpackage.
"""
import os
from pathlib import Path

from .settings import PROJECT_DIRNAME
from .settings import PROJECT_FILE


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


def create_project_dir(path: str) -> str:
    """Creates a new project directory at the given path

    Parameters
    ----------
    path : str
        Path to create a new project directory in.

    Returns
    -------
    str
        Path to the newly created project folder.

    Raises
    ------
    FileExistsError
        If a project directory already exists at the `path` given.

    """
    proj_dir = os.path.join(path, PROJECT_DIRNAME)
    if os.path.exists(proj_dir):
        raise FileExistsError(proj_dir)
    os.mkdir(proj_dir)
    return proj_dir


def create_project_file(path: str) -> str:
    """Creates a new project file at the given path

    Parameters
    ----------
    path : str
        Path to the newly created project file.

    Returns
    -------
    str
        Path to the newly created project file.

    Raises
    ------
    FileExistsError
        If the project file already exists at the `path` given.

    """
    proj_file = os.path.join(path, PROJECT_FILE)
    if os.path.exists(proj_file):
        raise FileExistsError(proj_file)
    new_proj = Project()

    return proj_file
