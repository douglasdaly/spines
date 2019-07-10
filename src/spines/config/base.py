# -*- coding: utf-8 -*-
"""
Base configuration object for spines.
"""
from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping
from collections.abc import MutableMapping
from typing import Any
from typing import Iterator
from typing import List
from typing import Tuple


class BaseConfig(MutableMapping):
    """
    Base configuration object class
    """
    __storage_cls__ = None

    def __init__(self, *args, **kwargs) -> None:
        if self.__storage_cls__ is None:
            self.__storage_cls__ = type(self)
        self._storage = defaultdict(self.__storage_cls__)
        self.update(*args, **kwargs)
        return

    def __repr__(self) -> str:
        return "{%s}" % ', '.join(["%s: %s" % (k, v) for k, v in self.items()])

    def __getitem__(self, item: str) -> Any:
        if item is None:
            return
        key, sub_key = self._key_helper(item)
        if key not in self._storage.keys():
            raise KeyError("Setting not found: %s" % key)
        if sub_key:
            return self._storage[key][sub_key]
        return self._storage[key]

    def __setitem__(self, key: str, value) -> None:
        if key is None:
            return
        key, sub_key = self._key_helper(key)
        if sub_key:
            self._storage[key][sub_key] = value
        else:
            if (key in self._storage and isinstance(value, Mapping)
                    and isinstance(self._storage[key], self.default_cls)):
                self._storage[key].update(value)
            else:
                self._storage[key] = value
        return

    def __delitem__(self, key: str) -> None:
        if key is None:
            return
        key, sub_key = self._key_helper(key)
        if sub_key:
            del self._storage[key][sub_key]
        else:
            del self._storage[key]
        return

    def __iter__(self) -> Iterator:
        return iter(self._storage)

    def __len__(self) -> int:
        return len(self._storage)

    def __contains__(self, item: str) -> bool:
        if item is None:
            return
        key, sub_key = self._key_helper(item)
        if key not in self._storage.keys():
            return False
        tmp_obj = self._storage[key]
        if sub_key is not None and isinstance(tmp_obj, Mapping):
            return sub_key in self._storage[key]
        return True

    def __getattr__(self, name: str) -> Any:
        try:
            return super().__getattribute__(name)
        except AttributeError as ex:
            try:
                return self.__getitem__(name)
            except KeyError:
                raise ex
        return

    def __setattr__(self, name: str, value: Any) -> None:
        if '_storage' not in self.__dict__ or name in self.__dict__:
            return super().__setattr__(name, value)
        return self.__setitem__(name, value)

    @property
    def default_cls(self) -> type:
        """type: Default storage class used for missing items."""
        return self._storage.default_factory

    def copy(self) -> BaseConfig:
        """Creates a copy of this configuration object

        Returns
        -------
        BaseConfig
            Copy of this configuration object.

        """
        new = self.__class__()
        for k, v in self._storage.items():
            if hasattr(v, 'copy'):
                new[k] = v.copy()
            else:
                new[k] = v
        return new

    def keys(self) -> List[str]:
        ret = list()
        for k, v in self._storage.items():
            if isinstance(v, BaseConfig):
                ret.extend(['%s.%s' % (k, x) for x in v.keys()])
            else:
                ret.append(k)
        return sorted(ret)

    def values(self) -> List:
        return [self[k] for k in self.keys()]

    @staticmethod
    def _key_helper(key: str) -> Tuple[str, str]:
        """Helper function to get properly formatted keys"""
        ret = key.lower().split('.', 1)
        if len(ret) == 1:
            return ret[0], None
        return ret[0], ret[1]


class BaseConfigException(Exception):
    """
    Base exception class for configuration subpackage
    """
    pass
