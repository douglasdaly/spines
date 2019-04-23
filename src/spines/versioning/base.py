# -*- coding: utf-8 -*-
"""
Base classes for the spines versioning package.
"""
#
#   Imports
#
import hashlib
import inspect
from types import FunctionType
from typing import Dict

import parver

from .. import __version__
from ..parameters.base import Parameter
from .core import slugify
from .core import get_function_source


#
#   Classes
#

class Version(object):
    """
    Version object for versioning of spines models.
    """

    def __init__(self, obj, display_name=None, desc=None):
        if not isinstance(obj, type):
            obj = obj.__class__

        self._name = obj.__name__
        self._display_name = display_name if display_name else self._name
        self._desc = desc if desc else obj.__doc__
        self._functions = self._get_functions(obj)
        self._parameters = self._get_parameters(obj)
        self._spines_version = __version__
        self._tag = None
        self._version = parver.Version((0, 0, 1), dev=None)

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
    def functions(self) -> Dict[str, 'Signature']:
        """dict: Functions in this version"""
        return self._functions.copy()

    @property
    def parameters(self) -> Dict[str, Parameter]:
        """dict: Parameters in this version"""
        return self._parameters.copy()

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

    def bump_params(self) -> None:
        """Bumps this version's MINOR number by one."""
        self._version = self._version.bump_release(index=1)
        return

    def bump_code(self) -> None:
        """Bumps this version's MAJOR number by one."""
        self._version = self._version.bump_release(index=0)
        return

    # Component signatures

    @classmethod
    def _get_functions(cls, obj):
        """Helper function to get individual model function signatures
        """
        ret = {}
        for k, v in obj.__dict__.items():
            if isinstance(v, FunctionType):
                ret[k] = Signature(v)
        return ret

    @classmethod
    def _get_parameters(cls, obj):
        """Helper function to get individual model parameters"""
        ret = {}
        for k, v in obj.__dict__.items():
            if isinstance(v, Parameter):
                ret[k] = v
        return ret


class Signature(object):
    """
    Signature objects for component change tracking and management.

    This object is used for tagging/version-tracking a single component
    of a larger model (e.g. the ``fit`` method).  Collections of these
    objects are used to identify, fully, a particular version of a
    :class:`Model` instance.

    """

    def __init__(self, obj):
        self._name = obj.__name__
        self._desc = obj.__doc__
        self._code = self._get_code(obj)
        self._parameters = self._get_parameters(obj)
        self._hash = self._get_hash(obj)

    def __str__(self):
        return '%s @ %s' % (self.name, self.hash[-8:])

    def __repr__(self):
        return '<Signature: name="%s" hash="%s">' % (
            self.name, self.hash[-8:]
        )

    @property
    def code(self):
        """str: The code for the function"""
        return self._code

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

    @property
    def name(self):
        """str: The name of the object this signature is for"""
        return self._name

    @property
    def parameters(self):
        """dict: Parameters used in the function signature"""
        return self._parameters

    @classmethod
    def _get_hash(cls, obj) -> [bytes, None]:
        """Gets the hash for the given object"""
        all_bytes = cls._get_bytes(obj)
        if all_bytes:
            m = hashlib.sha256()
            m.update(all_bytes)
            return m.digest()
        return

    @classmethod
    def _get_bytes(cls, obj: FunctionType) -> [bytes, None]:
        """Gets the relevant bytes for a single function object"""
        if not hasattr(obj, '__code__'):
            return None
        bytecode = obj.__code__.co_code
        consts = obj.__code__.co_consts[1:]
        dep_objs = obj.__code__.co_names
        all_vars = obj.__code__.co_varnames

        ret = []
        for v in (consts, dep_objs, all_vars):
            for i_v in v:
                ret.append('str:%s' % i_v)
        return bytecode + ','.join(ret).encode()

    @classmethod
    def _get_code(cls, obj: FunctionType) -> str:
        """Gets the code for the given function object"""
        return get_function_source(obj)

    @classmethod
    def _get_parameters(cls, obj) -> Dict[str, object]:
        """Gets the parameters for a function object"""
        fn_sig = inspect.signature(obj)
        return {k: None if v.default is fn_sig.empty else v.default
                for k, v in fn_sig.parameters.items()}
