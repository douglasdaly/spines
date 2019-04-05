# -*- coding: utf-8 -*-
"""
Base classes for model parameters.
"""
#
#   Imports
#
from abc import ABC
from collections.abc import MutableMapping, Iterable
from typing import Iterator


#
#   Base classes
#

class Parameter(object):
    """
    Parameter class

    Attributes
    ----------
    name : str
        Name of the Parameter.
    value_type : :obj:`Iterable` of :obj:`type`
        The type(s) of values allowed for this parameter.
    required : bool
        Whether or not this is a required parameter.
    default : object
        Default value for this parameter.

    Parameters
    ----------
    name : str
        Name of the Parameter these options are for.
    value_type : :obj:`type` or :obj:`Iterable` of :obj:`type`
        The type(s) of values allowed for this parameter.
    required : bool, optional
        Whether or not this is a required parameter (default is True).
    default : object, optional
        Default value for this parameter (default is None).

    """

    def __init__(self, name, value_type, required=True, default=None):
        self.name = name
        self.value_type = value_type
        self.required = required
        self.default = default

    # dunder Methods

    def __call__(self, value):
        """Checks the given value, raising exceptions if it isn't valid"""
        if self._check_helper(value, raise_exceptions=True):
            return value
        return

    def __repr__(self):
        return '<%s %s [type=%s] (%s)>' % (
            self.__class__.__name__,
            self.name,
            ', '.join([x.__name__ for x in self.value_type]),
            ', '.join(self._disp_props())
        )

    def __str__(self):
        return self.name

    # Properties

    @property
    def value_type(self) -> tuple:
        """tuple: The types of values allowed for this option."""
        return self._value_types

    @value_type.setter
    def value_type(self, value):
        """Sets the value type(s) allowed

        Parameters
        ----------
        value : :obj:`type` or :obj:`Iterable` of :obj:`type`
            Value type(s) allowed for this option.

        """
        if not isinstance(value, Iterable):
            value = (value,)
        else:
            value = tuple(value)
        if not all([isinstance(x, type) for x in value]):
            raise TypeError('Must use types when setting this value')
        self._value_types = value

    @property
    def default(self):
        """object: Default value to use for this parameter."""
        return self._default

    @default.setter
    def default(self, value):
        """Sets the default value for this parameter

        Parameters
        ----------
        value
            Default value to use for this parameter.

        Raises
        ------
        InvalidParameterException
            If the type of the given `value` is not a valid parameter
            `value_type`.

        """
        if value is not None and not isinstance(value, self.value_type):
            raise TypeError('Value type must be one of: %s' % self.value_type)
        self._default = value

    # Check methods

    def check(self, value) -> bool:
        """Checks the given `value` for validity

        Parameters
        ----------
        value
            Parameter value to check validity of.

        Returns
        -------
        bool
            Whether or not the value is valid for the parameter.

        """
        return self._check_helper(value, raise_exceptions=False)

    # Helper functions

    def _check_helper(self, value, raise_exceptions=True) -> bool:
        """Helper function for checking if a value is valid"""
        if not isinstance(value, self.value_type):
            if raise_exceptions:
                raise InvalidParameterException(
                    '%s: invalid type given: %s (required %s)' % (
                        self.name, type(value),
                        ', '.join([str(x) for x in self.value_type])
                    )
                )
            return False

        return True

    def _disp_props(self):
        """Helper function to get properties to display in name string"""
        ret = list()
        if self.required:
            ret.append('required')
        if self.default:
            ret.append('default=%s' % self.default)
        return ret


class ParameterStore(MutableMapping):
    """
    Helper class for managing collections of Parameters.
    """

    def __init__(self):
        self._params = dict()
        self._values = dict()

    # dunder methods

    def __setitem__(self, k: str, v: Parameter) -> None:
        self._values[k] = self._params[k](v)

    def __delitem__(self, v: str) -> None:
        del self._values[v]

    def __getitem__(self, k: str) -> Parameter:
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


class ParameterMixin(ABC):
    """
    Base mixin class for parameters
    """

    def _check_helper(self, value, raise_exceptions=True):
        """Helper function to check if the given value is valid."""
        return super(ParameterMixin, self)._check_helper(
            value, raise_exceptions=raise_exceptions
        )


#
#   Exceptions
#

class ParameterException(Exception):
    """
    Base class for Model parameter exceptions.
    """
    pass


class MissingParameterException(ParameterException):
    """
    Thrown when a required parameter is missing.
    """
    pass


class InvalidParameterException(ParameterException):
    """
    Thrown when an invalid parameter is given.
    """
    pass

