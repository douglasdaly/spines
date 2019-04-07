# -*- coding: utf-8 -*-
"""
Base classes for the spines versioning package.
"""
#
#   Imports
#
import parver

from .core import slugify


#
#   Classes
#

class Version(object):
    """
    Version objects for versioning of spines components
    """

    def __init__(self, name, display_name=None, desc=None):
        self._name = name
        self._display_name = display_name
        self._desc = desc
        self._version = parver.Version((0, 0, 1), dev=None, epoch=0)
        self._tag = None

    # dunder methods

    def __str__(self):
        return '%s %s' % (self._name, self._version)

    # Properties

    @property
    def name(self) -> str:
        """str: Name of the object versioned."""
        return self._name

    def display_name(self) -> str:
        """str: Display name for the object versioned."""
        return self._display_name

    @display_name.setter
    def display_name(self, value) -> None:
        self._display_name = value
        return

    def description(self) -> str:
        """str: Description for the object versioned."""
        return self._desc

    @description.setter
    def description(self, value) -> None:
        self._desc = value
        return

    @property
    def tag(self) -> str:
        """str: Tag (if any) for this version."""
        return self._tag

    @tag.setter
    def tag(self, value) -> None:
        self._tag = value
        return

    @property
    def slug(self) -> str:
        """str: Slugified version of this version object"""
        slug_name = slugify(self._name)
        slug_vers = slugify(str(self._version))
        return '%s/%s' % (slug_name, slug_vers)

