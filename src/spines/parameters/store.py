# -*- coding: utf-8 -*-
"""
Parameter storage module.
"""
#
#   Imports
#
from collections.abc import MutableMapping
from typing import Iterator

from .base import Parameter


#
#   Classes
#

class ParameterStore(MutableMapping):
    """
    Helper class for managing collections of Parameters.
    """

    def __init__(self):
        self._params = dict()
        self._values = dict()

    # dunder methods

    def __setitem__(self, k: str, v) -> None:
        if self._params[k](v):
            self._values[k] = v
        return

    def __delitem__(self, v: str) -> None:
        del self._values[v]

    def __getitem__(self, k: str):
        return self._values[k]

    def __len__(self) -> int:
        return len(self._values)

    def __iter__(self) -> Iterator[str]:
        return iter(self._values)

    # Properties

    @property
    def parameters(self) -> dict:
        """dict: Copy of the current set of parameters."""
        return self._params.copy()

    @property
    def values(self) -> dict:
        """dict: Copy of the current set of parameter values."""
        return self._values.copy()

    @property
    def valid(self) -> bool:
        """bool: Whether or not this is a fully valid set of parameters."""
        return self._validate_helper(raise_exceptions=False)

    # Helper methods

    def copy(self, deep=False):
        """Returns a copy of this parameter store object.

        Parameters
        ----------
        deep : bool, optional
            Whether or not to do deep-copying of this stores contents.

        Returns
        -------
        ParameterStore
            Copied parameter store object.

        """
        new_obj = self.__class__()
        for k, v in self._params:
            new_obj.add(v)
        for k, v in self._values:
            new_obj[k] = v
        return new_obj

    def reset(self) -> None:
        """Clears all of the parameters and options stored."""
        self._values.clear()
        self._params.clear()

    # Option methods

    def add(self, parameter: Parameter) -> None:
        """Add a :class:`Parameter` specification to this store

        Parameters
        ----------
        option : Parameter
            :class:`Parameter` specification to add to this parameter
            store.

        Raises
        ------
        ParameterExistsError
            If a parameter option with the same name already exists.

        """
        self._params[parameter.name] = parameter
        return

    def remove(self, name: str) -> Parameter:
        """Removes a :class:`Parameter` specification

        Parameters
        ----------
        name : str
            Name of the :class:`Parameter` to remove.

        Returns
        -------
        Parameter
            The removed :class:`Parameter` specified.

        Raises
        ------
        KeyError
            If the given `name` does not exist.

        """
        if name in self._values.keys():
            del self._values[name]
        return self._params.pop(name)

    def _validate_helper(self, raise_exceptions=False) -> bool:
        """Helper to check if this set of parameters is valid"""
        for k, v in self._params.items():
            if v.required and k not in self._values.keys():
                if raise_exceptions:
                    raise MissingParameterException(k)
                return False
        return True
