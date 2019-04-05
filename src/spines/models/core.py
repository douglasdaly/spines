# -*- coding: utf-8 -*-
"""
Core model classes.
"""
#
#   Imports
#
from abc import ABCMeta

from .base import Model
from ..parameters.base import Parameter
from ..parameters.base import ParameterStore


#
#   Models
#

class HyperModel(Model, metaclass=ABCMeta):
    """
    Hyper-parameterized model class
    """
    _hyper_param_store_cls = ParameterStore
    _default_hyper_param_cls = Parameter

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._hyper_params = self._hyper_param_store_cls()

    @property
    def hyper_parameters(self):
        """ParameterStore: Hyper-parameters which are currently set."""
        return self._hyper_params

    def set_hyper_params(self, **hyper_params) -> None:
        """Sets the values of this model's hyper-parameters

        Parameters
        ----------
        hyper_params
            Hyper-parameter values to set.

        Raises
        ------
        InvalidParameterException
            If one of the given hyper-parameter values is not valid.

        """
        self._hyper_params.update(hyper_params)
        return

    def get_hyper_params(self) -> dict:
        """Gets the current hyper-parameter values

        Returns
        -------
        dict
            Copy of the currently set hyper-parameter values.

        """
        return self._hyper_params.values

    def set_hyper_parameter(self, name, value):
        """Sets a hyper-parameter value

        Sets a hyper-parameter's value if the given `hyper_param` and `value`
        are valid.

        Parameters
        ----------
        name : str
            Hyper-parameter to set value for.
        value
            Value to set.

        Raises
        ------
        MissingParameterException
            If the given `name` hyper-parameter does not exist.
        InvalidParameterException
            If the given `value` is not valid for the specified
            hyper-parameter.

        See Also
        --------
        hyper_parameters

        """
        self._hyper_parameters[name] = s
        return

    def unset_hyper_parameter(self, name):
        """Un-sets a hyper-parameter

        Un-sets the specified hyper-parameter's value from the set of
        hyper-parameters and returns the previously set value.

        Parameters
        ----------
        name : str
            Name of the hyper-parameter to clear the value for.

        Returns
        -------
        object
            Previously set value of the hyper-parameter.

        Raises
        ------
        MissingParameterException
            If the given `name` hyper-parameter does not exist.

        See Also
        --------
        hyper_parameters

        """
        return self._hyper_parameters.pop(s)
