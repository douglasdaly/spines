# -*- coding: utf-8 -*-
"""
Mixin classes for versioning subpackage.
"""
from abc import ABC
from abc import abstractmethod
from hashlib import blake2s
from typing import Sequence
from typing import Type

import parver

from .. import __version__
from ..utils.object import get_doc_string
from ..utils.string import slugify


class VersionMixin(ABC):
    """
    Version mixin for versioning Signature objects.
    """
    _HASH = blake2s

    def __init__(self, obj) -> None:
        self._spines_version = __version__
        self._desc = self._get_desc(obj)

        super().__init__(obj)

        self._version = self._get_next_version(
            obj.__getattribute__('__version__', None)
        )
        return

    def __call__(self, next_obj) -> Type['VersionMixin']:
        return self.__class__(next_obj)

    def __repr__(self) -> str:
        return '<%s: name="%s" version="%s">' % (
            self.__class__.__name__, self.name, self.version
        )

    @property
    def description(self) -> str:
        """str: Description for the main object versioned."""
        return self._desc

    @property
    def slug(self) -> str:
        """str: Slugified version of this version object"""
        slug_name = slugify(self._name)
        slug_vers = slugify(str(self._version))
        return '%s/%s' % (slug_name, slug_vers)

    @property
    def spines_version(self) -> str:
        """str: Version of spines this version object was created with
        """
        return self._spines_version

    @property
    def version(self) -> str:
        """str: Version string for this version object."""
        return str(self._version)

    def to_release(self) -> None:
        """Switches the version to release"""
        self._version = self._version.clear(dev=False, pre=False, post=False)
        return

    def to_pre(self) -> None:
        """Switches the version to pre-release"""
        self._version = self._version.clear(pre=True)
        return

    def to_post(self) -> None:
        """Switches the version to post-release"""
        self._version = self._version.clear(post=True)
        return

    def to_dev(self) -> None:
        """Switches the version to development"""
        self._version = self._version.clear(dev=True)
        return

    @abstractmethod
    def _get_next_version(
        self,
        prev_version: [Type['VersionMixin'], None]
    ) -> Type[parver.Version]:
        """Determines the next version from the previous"""
        pass

    def _get_desc(self, obj) -> [str, None]:
        """Helper function to get description of this versioned object
        """
        return get_doc_string(obj)


class DependenciesMixin(ABC):
    """
    Mixin for getting dependencies for the Signature's object
    """

    def __init__(self, obj: [type, object]) -> None:
        super().__init__(obj)
        self._dependencies = self._get_dependencies(obj)
        return

    @property
    def dependencies(self) -> Sequence[str]:
        """:obj:`tuple` of :obj:`str`: Dependencies of the object"""
        return self._dependencies

    @abstractmethod
    def _get_dependencies(self, obj: [type, object]) -> Sequence[str]:
        """Gets the dependencies of the signed object"""
        pass


class SourceMixin(ABC):
    """
    Source mixin for storing source code of Signature object's
    """

    def __init__(self, obj: [type, object]) -> None:
        super().__init__(obj)
        self._source = self._get_source(obj)
        return

    @property
    def source(self) -> [str, None]:
        """:obj:`str`: Source code for the signature's object."""
        return self._source
