# -*- coding: utf-8 -*-
"""
Base classes for the spines versioning functionality.
"""
#
#   Imports
#
from abc import ABC
from abc import abstractmethod
from sys import maxsize as _OS_MAXSIZE
from typing import Type

if _OS_MAXSIZE > 2**32:
    from xxhash import xxh64 as xxh
else:
    from xxhash import xxh32 as xxh

from ..utils.string import slugify


#
#   Base class
#

class Signature(ABC):
    """
    Signature objects for component change tracking and management.

    This object is used for tagging/version-tracking a single component
    of a larger model (e.g. the ``fit`` method).  Collections of these
    objects are used to identify, for example, a particular version of a
    :class:`Model` instance.

    """
    _HASH = xxh

    def __init__(self, obj: [type, object], name: str = None):
        if not name:
            self._name = obj.__name__
        else:
            self._name = name
        self._hash = self._get_hash(obj).digest()

    def __str__(self):
        return '%s @ %s' % (self.name, self.hash[-8:])

    def __repr__(self):
        return '<%s: name="%s" hash="%s">' % (
            self.__class__.__name__, self.name, self.hash[-8:]
        )

    def __eq__(self, value: Type['Signature']) -> bool:
        return self.hash_bytes == value.hash_bytes

    def __ne__(self, value: Type['Signature']) -> bool:
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

    def _get_source(self, obj) -> str:
        """Gets the source code for the given object"""
        return
