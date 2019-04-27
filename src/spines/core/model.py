# -*- coding: utf-8 -*-
"""
Model class for the spines package.
"""
#
#   Imports
#
from abc import abstractmethod
from typing import Dict
from typing import List
from typing import Type

from ..parameters.base import HyperParameter
from ..parameters.store import ParameterStore
from ..utils.file import load_pickle
from ..utils.file import save_pickle
from . import decorators
from .base import BaseObject


#
#   Class Definitions
#

class Model(BaseObject):
    """
    Base Model class
    """
    __hyperparam_store__ = ParameterStore

    def __init__(self, *args, **kwargs):
        super(Model, self).__init__(*args, **kwargs)

        self._hyper_params = self._create_store(
            self.__hyperparam_store__, HyperParameter
        )

        self._modify_methods()

    def __str__(self):
        return self.__class__.__name__

    def __call__(self, *args, **kwargs):
        return self.predict(*args, **kwargs)

    @property
    def hyper_parameters(self) -> Type[ParameterStore]:
        """ParameterStore: Hyper-parameters which are currently set."""
        return self._hyper_params

    def construct(self, *args, **kwargs) -> None:
        """Constructs the model

        Parameters
        ----------
        args : optional
            Arguments to use in constructing the model.
        kwargs : optional
            Keyword arguments to use in constructing the model.

        """
        return

    def fit(self, *args, **kwargs) -> [None, Dict]:
        """Fits the model

        Generally this method is used for a single iteration of model
        fitting (and for simple models this may be the only call
        which is required).  The :obj:`train` method can call this
        function multiple times and update the model iteratively (where
        that approach is appropriate).

        Parameters
        ----------
        args : optional
            Arguments to use in fit call.
        kwargs : optional
            Any additional keyword arguments to use in fit call.

        Returns
        -------
        :obj:`None` or :obj:`dict`
            Either returns `None` if adjustments to the model's
            parameters happen internally, otherwise returns the
            dictionary of updated parameters to apply.

        See Also
        --------
        train

        """
        return

    def train(self, *args, **kwargs) -> None:
        """Trains the model, iteratively

        This is the main training routine method for the model class.
        It's generally used for training models such as neural networks
        where you'll want to iteratively update the model (via ``fit``
        calls), potentially based on different hyper-parameter settings.

        Parameters
        ----------
        args : optional
            Arguments to use in train call.
        kwargs : optional
            Any additional keyword arguments to use in the train call.

        See Also
        --------
        fit

        """
        return

    @abstractmethod
    def predict(self, *args, **kwargs):
        """Predict outputs for the given inputs

        Parameters
        ----------
        args : optional
            Additional arguments to pass to predict call.
        kwargs : optional
            Additional keyword arguments to pass to predict call.

        Returns
        -------
        object
            Predictions from the given data.

        """
        pass

    def score(self, *args, **kwargs) -> float:
        """Returns the score measure of the model for the given data

        Parameters
        ----------
        args : optional
            Arguments (data inputs and outputs) to pass to the score
            call.
        kwargs : optional
            Additional keyword-arguements to pass to the score call.

        Returns
        -------
        float
            Score for the model on the given inputs and outputs.

        """
        return

    def error(self, *args, **kwargs) -> float:
        """Returns the error measure of the model for the given data

        Parameters
        ----------
        args : optional
            Additional arguments to pass to the error call.
        kwargs : optional
            Additional keyword-arguments to pass to the error call.

        Returns
        -------
        float
            Error for the model on the given inputs and outputs.

        """
        return

    # Hyper-parameters

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

    def get_hyper_params(self) -> Dict[str, object]:
        """Gets the current hyper-parameter values

        Returns
        -------
        dict
            Copy of the currently set hyper-parameter values.

        See Also
        --------
        hyper_parameters, set_hyper_params

        """
        return self._hyper_params.values

    def set_hyper_parameter(self, name: str, value) -> None:
        """Sets a hyper-parameter value

        Sets a hyper-parameter's value if the given `hyper_param` and
        `value` are valid.

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
        hyper_parameters, set_hyper_params

        """
        self._hyper_parameters[name] = value
        return

    def unset_hyper_parameter(self, name: str):
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
        hyper_parameters, set_hyper_params

        """
        return self._hyper_parameters.pop(name)

    def _save_helper(self, dir_path: str) -> List[str]:
        """Saves Model objects to the specified directory"""
        ret = super(Model, self)._save_helper(dir_path)
        ret.append(
            save_pickle(self._hyper_params, dir_path, 'hyperparameters')
        )
        return ret

    @classmethod
    def _load_helper(cls, dir_path: str, new: bool) -> Type['Model']:
        """Helper function for loading a Model from file"""
        instance = super(Model, cls)._load_helper(dir_path, new)
        instance._hyper_params = load_pickle(dir_path, 'hyperparameters')
        return instance

    def _modify_methods(self, *args, **kwargs):
        """Modifies the model's functions in-place on object creation"""
        super(Model, self)._modify_methods(*args, **kwargs)

        self.fit = decorators.finalize_pre(self.fit, self._hyper_params)
        self.fit = decorators.finalize_post(self.fit, self._params)

        if (hasattr(self.error, '__is_overridden')
                and not hasattr(self.score, '__is_overridden')):
            self.score = decorators.inverse_from_func(self.score, self.error)
        elif (hasattr(self.score, '__is_overridden')
                and not hasattr(self.error, '__is_overridden')):
            self.error = decorators.inverse_from_func(self.error, self.score)

        return
