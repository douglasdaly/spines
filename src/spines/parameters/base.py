# -*- coding: utf-8 -*-
"""
Base classes for model parameters.
"""
#
#   Imports
#
from abc import ABC
from collections.abc import Iterable
from typing import Type


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
    value_type : :obj:`type` or :obj:`Iterable` of :obj:`type`
        The type(s) of values allowed for this parameter.
    required : bool, optional
        Whether or not this is a required parameter (default is True).
    default : object, optional
        Default value for this parameter (default is None).

    """

    def __init__(self, value_type, required=True, default=None):
        self._name = None
        self.value_type = value_type
        self.required = required
        self.default = default

    # dunder Methods

    def __call__(self, value):
        if self._check_helper(value, raise_exceptions=True):
            return True
        return False

    def __repr__(self) -> str:
        return '<%s %s [type=%s] (%s)>' % (
            self.__class__.__name__,
            self.name,
            ', '.join([x.__name__ for x in self.value_type]),
            ', '.join(self._disp_props())
        )

    def __str__(self) -> str:
        return self._name

    # Descriptor methods

    def __set_name__(self, owner, name: str) -> None:
        self._name = name
        return

    def __set__(self, instance: Type['spines.Model'], value) -> None:
        instance.parameters[self._name] = value
        return

    def __get__(self, instance, owner):
        return instance.parameters.get(self._name, None)

    # Properties

    @property
    def name(self) -> str:
        """str: Name of this parameter"""
        return self._name

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


class HyperParameter(Parameter):
    """
    Hyper-parameter
    """

    def __set__(self, instance: Type['spines.Model'], value) -> None:
        instance.hyper_parameters[self._name] = value
        return

    def __get__(self, instance: Type['spines.Model'], owner):
        return instance.hyper_parameters[self._name]


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

