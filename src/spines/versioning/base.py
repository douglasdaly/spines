# -*- coding: utf-8 -*-
"""
Base classes for the spines versioning functionality.
"""
#
#   Imports
#
from abc import ABC
from abc import abstractmethod
from hashlib import blake2s
from typing import Type

import parver
from xxhash import xxh64

from .. import __version__
from .utils import get_doc_string
from .utils import slugify


#
#   Classes
#

class BaseSignature(ABC):
    """
    Base signature objects for component change tracking and management.

    This object is used for tagging/version-tracking a single component
    of a larger model (e.g. the ``fit`` method).  Collections of these
    objects are used to identify, fully, a particular version of a
    :class:`Model` instance.

    """
    _HASH = xxh64

    def __init__(self, obj):
        self._name = obj.__name__
        self._hash = self._get_hash(obj).digest()

    def __str__(self):
        return '%s @ %s' % (self.name, self.hash[-8:])

    def __repr__(self):
        return '<%s: name="%s" hash="%s">' % (
            self.__class__.__name__, self.name, self.hash[-8:]
        )

    def __eq__(self, value: Type['BaseSignature']) -> bool:
        return self.hash_bytes == value.hash_bytes

    def __ne__(self, value: Type['BaseSignature']) -> bool:
        return not self.__eq__(value)

    @property
    def hash(self) -> str:
        """str: Full hash string for this signature's hash"""
        return self._hash.hex()

    @property
    def hash_bytes(self) -> bytes:
        """bytes: Full hash (in bytes-form) for this signature"""
        return self._hash

    @property
    def name(self) -> str:
        """str: The name of the object this signature is for"""
        return self._name

    @property
    def slug(self) -> str:
        """str: Slug-ified version of this signature"""
        return "%s@%s" % (slugify(self.name), self.hash)

    def _get_hash(self, obj) -> [bytes, None]:
        """Gets the hash for the given object"""
        m = self._HASH()
        m.update(self._get_bytes(obj))
        return m

    @abstractmethod
    def _get_bytes(self, obj) -> bytes:
        """Gets the relevant bytes for a single object"""
        pass


class BaseVersion(BaseSignature):
    """
    Base version object for versioning module.

    Parameters
    ----------
    obj : object
        The object to generate a version object for.

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
        prev_version: [Type['Version'], None]
    ) -> Type[parver.Version]:
        """Determines the next version from the previous"""
        pass

    def _get_desc(self, obj) -> [str, None]:
        """Helper function to get description of this versioned object
        """
        return get_doc_string(obj)
