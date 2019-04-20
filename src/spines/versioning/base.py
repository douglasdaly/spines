# -*- coding: utf-8 -*-
"""
Base classes for the spines versioning package.
"""
#
#   Imports
#
import hashlib
from types import FunctionType
from typing import Dict

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
        self._version = parver.Version((0, 0, 1), dev=None)
        self._tag = None

    # dunder methods

    def __repr__(self):
        return "<Version name=%s version=%s>" % (self._name, self._version)

    def __str__(self):
        return '%s %s' % (self._name, self._version)

    # Properties

    @property
    def name(self) -> str:
        """str: Name of the object versioned."""
        return self._name

    @property
    def display_name(self) -> str:
        """str: Display name for the object versioned."""
        return self._display_name

    @display_name.setter
    def display_name(self, value) -> None:
        self._display_name = value
        return

    @property
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
    def version(self) -> str:
        """str: Version string for this version object."""
        return str(self._version)

    @property
    def slug(self) -> str:
        """str: Slugified version of this version object"""
        slug_name = slugify(self._name)
        slug_vers = slugify(str(self._version))
        return '%s/%s' % (slug_name, slug_vers)

    # Version actions

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

    def bump_dev(self) -> None:
        """Bumps the dev number for use during iterative work."""
        self._version = self._version.bump_dev()
        return

    def bump(self) -> None:
        """Bumps this version's PATCH number by one."""
        self._version = self._version.bump_release(index=2)
        return

    def bump_minor(self) -> None:
        """Bumps this version's MINOR number by one."""
        self._version = self._version.bump_release(index=1)
        return

    def bump_major(self) -> None:
        """Bumps this version's MAJOR number by one."""
        self._version = self._version.bump_release(index=0)
        return


class Signature(object):
    """
    Signature objects for component change tracking and management
    """

    def __init__(self, obj):
        self._name = obj.__name__
        self._type = 'class' if isinstance(obj, type) else type(obj).__name__
        self._desc = obj.__doc__
        self._hash = self._get_hash(obj)

    def __str__(self):
        return '%s(%s) @ %s' % (self._name, self._type, self.hash[-8:])

    def __repr__(self):
        return '<Signature: type="%s" name="%s" hash="%s">' % (
            self._type, self._name, self.hash[-8:]
        )

    @property
    def name(self):
        """str: The name of the object this signature is for"""
        return self._name

    @property
    def type(self):
        """str: The type of object this signature is for"""
        return self._type

    @property
    def description(self):
        """str: The description (docstring) for this object, if any"""
        return self._desc

    @property
    def hash(self):
        """str: Full hash (in hex string format) for this signature"""
        return self._hash.hex()

    @property
    def hash_bytes(self):
        """bytes: Full hash (in bytes) for this signature"""
        return self._hash

    @classmethod
    def _get_hash(cls, obj) -> [bytes, None]:
        """Gets the hash for the given object"""
        all_bytes = cls._get_bytes_dict(obj)
        if all_bytes:
            m = hashlib.sha256()
            for k in sorted(all_bytes.keys()):
                m.update(all_bytes[k])
            return m.digest()
        return None

    @staticmethod
    def _get_bytes_dict(obj) -> Dict[str, bytes]:
        """Gets an OrderedDictionary of bytes for object components"""
        ret = dict()
        if isinstance(obj, FunctionType):
            ret[obj.__name__] = obj.__code__.co_code
        elif isinstance(obj, (type, object)):
            for k, v in obj.__dict__.items():
                if not isinstance(v, FunctionType):
                    continue
                ret[k] = v.__code__.co_code
        else:
            if hasattr(obj, '__code__'):
                ret['0'] = obj.__code__.co_code
        return ret
