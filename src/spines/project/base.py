# -*- coding: utf-8 -*-
"""
Base classes for the project subpackage.
"""
#
#   Imports
#


#
#   Base classes
#

class Project(object):
    """
    Project class for managing project components
    """

    def __init__(self) -> None:
        self._sources = {}
        self._components = {}
        return

    @property
    def sources(self) -> dict:
        """dict: Sources used in this project"""
        return self._sources.copy()

    @property
    def components(self) -> dict:
        """dict: Components used in this project"""
        return self._components.copy()

