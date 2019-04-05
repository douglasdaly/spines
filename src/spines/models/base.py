# -*- coding: utf-8 -*-
"""
Base classes for the spines package.
"""
#
#   Imports
#
import os
import pickle
import tarfile
import zipfile
import tempfile
from abc import ABCMeta, abstractmethod

from ..parameters.base import Parameter
from ..parameters.base import ParameterStore


#
#   Class Definitions
#

class Model(object, metaclass=ABCMeta):
    """
    Model class
    """
    _param_store_cls = ParameterStore
    _default_param_cls = Parameter

    def __init__(self, *args, **kwargs):
        self._params = self._param_store_cls()

    # dunder methods

    def __str__(self):
        return self.__class__.__name__

    def __call__(self, *args, **kwargs):
        return self.predict(*args, **kwargs)

    # Properties

    @property
    def parameters(self):
        """ParameterStore: Parameters which are currently set."""
        return self._params

    # Parameter functions

    def set_params(self, **params) -> None:
        """Sets the values for this model's parameters

        Parameters
        ----------
        params
            Parameters and values to set.

        Raises
        ------
        InvalidParameterException
            If the given `name` or `value` are not valid.

        """
        self._params.update(params)
        return

    def get_params(self) -> dict:
        """Gets a copy of this models parameters

        Returns
        -------
        dict
            Copy of currently set parameter names and values.

        """
        return self._params.values

    def set_parameter(self, name: str, value) -> None:
        """Sets a parameter value

        Will add the given `param` and `value` to the parameters if
        they are valid, throws an exception if they are not.

        Parameters
        ----------
        name : str
            Parameter to set the value for.
        value
            Value to set.

        Raises
        ------
        InvalidParameterException
            If the given `name` or `value` are not valid.

        See Also
        --------
        parameters

        """
        self._params[name] = value
        return

    def unset_parameter(self, name: str) -> object:
        """Unsets a parameter value

        Removes the specified parameter's value from the parameter
        values if it is part of the parameter set and returns its
        current value.

        Parameters
        ----------
        name : str
            Name of the parameter whose value needs to be un-set.

        Returns
        -------
        object
            Previously set value of the parameter.

        Raises
        ------
        MissingParameterException
            If the parameter to remove does not exist in the set of
            parameters.

        See Also
        --------
        parameters

        """
        return self._params.pop(name)

    # Save/Load methods

    def save(self, path, fmt=None, overwrite_existing=False) -> str:
        """Saves this model

        Saves this model's `parameters`, `hyper_params` as well as
        any other data required to reconstruct this model.  Saves this
        data with the given unique `tag` name.

        Parameters
        ----------
        path : str
            File path to save the model to.
        fmt : str
            File output format to use.
        overwrite_existing : bool, optional
            Whether to overwrite any existing saved model with the same
            `path` (Default is False).

        Returns
        -------
        str
            The path to the saved file.

        Raises
        ------
        NotImplementedError
            If the specified `fmt` is not supported.

        """
        if not fmt:
            fmt = 'zip'
        else:
            fmt = fmt.lower()

        if not os.path.splitext(path)[1]:
            path += self._get_file_extension(fmt)

        if os.path.exists(path) and not overwrite_existing:
            raise FileExistsError(path)

        with tempfile.TemporaryDirectory(prefix='spines-') as tmp_dir:
            files = self._save_helper(tmp_dir)
            if fmt == 'zip':
                with zipfile.ZipFile(path, 'w') as archive:
                    for file in files:
                        archive.write(file, os.path.basename(file))
            else:
                mode = self._tar_mode_helper('w', fmt)
                with tarfile.open(path, mode) as archive:
                    for file in files:
                        archive.add(file, arcname=os.path.basename(file))
        return path

    def _save_helper(self, dir_path):
        """Helper function to save object to the specified directory

        Parameters
        ----------
        dir_path : str
            Directory to save the model components to.

        Returns
        -------
        list
            List of all the files created.

        """
        ret = list()
        ret.append(self._save_object(dir_path, 'class', self.__class__))
        ret.append(self._save_object(dir_path, 'parameters', self._params))
        return ret

    @classmethod
    def _save_object(cls, dir_path, file, obj):
        """Helper function to save a single object to file

        Parameters
        ----------
        dir_path : str
            Path to the directory to save the files to.
        file : str
            Name to save the file with.
        obj
            Object to save.

        Returns
        -------
        str
            The path of the file created.

        """
        if not file.endswith('.pkl'):
            file += '.pkl'
        obj_file = os.path.join(dir_path, file)
        with open(obj_file, 'wb') as fout:
            pickle.dump(obj, fout)
        return obj_file

    @classmethod
    def load(cls, path, fmt=None, new=False):
        """Loads a saved model instance

        Loads saved model `parameters` and `hyper_params` as well
        as any serialized model-specific objects from a saved version
        with the `tag` specified (from the base `project_dir`).

        Parameters
        ----------
        path : str
            Path to load the model from.
        fmt : :obj:`str` or :obj:`None`
            Format of the file to load (if :obj:`None` it will be inferred).
        new : bool, optional
            Whether to create a new object from this class or use the saved
            object class (default is False).

        Returns
        -------
        Model
            Model loaded from disk.

        """
        if not fmt:
            fmt = cls._infer_file_format(path)
        else:
            fmt = fmt.lower()

        with tempfile.TemporaryDirectory(prefix='spines-') as tmp_dir:
            if fmt == 'zip':
                with zipfile.ZipFile(path, 'r') as archive:
                    archive.extractall(tmp_dir)
            else:
                mode = cls._tar_mode_helper('r', fmt)
                with tarfile.open(path, mode) as archive:
                    archive.extractall(tmp_dir)
            if new:
                instance = cls()
            else:
                klass = cls._load_object(tmp_dir, 'class')
                instance = klass()
            instance = cls._load_helper(tmp_dir, instance)

        return instance

    @classmethod
    def _load_helper(cls, dir_path, instance):
        """Helper function for loading objects from files

        Parameters
        ----------
        dir_path : str
            Path to directory to load files from
        instance : Model
            Model instance to initialize from files

        Returns
        -------
        Model
            The model loaded from file.

        """
        instance._params = cls._load_object(dir_path, 'parameters')
        return instance

    @classmethod
    def _load_object(cls, dir_path, file):
        """Helper function for loading objects from file

        Parameters
        ----------
        dir_path : str
            Directory to load the `file` from.
        file : str
            File to load.

        Returns
        -------
        object
            Object loaded from file.

        """
        if not file.endswith('.pkl'):
            file += '.pkl'
        obj_file = os.path.join(dir_path, file)
        with open(obj_file, 'rb') as fin:
            ret = pickle.load(fin)
        return ret

    @staticmethod
    def _tar_mode_helper(mode, fmt):
        """Helper function for getting tar open mode string"""
        ret = mode
        if fmt == 'lzma':
            return ret + ':xz'
        elif fmt == 'tar':
            return ret
        elif fmt == 'gzip':
            return ret + ':gz'
        elif fmt == 'bzip2':
            return ret + ':bz2'
        raise NotImplementedError('Format: %s' % fmt)

    @staticmethod
    def _infer_file_format(path):
        """Helper function to infer the file format from the path"""
        exts = list()
        tmp_path, tmp_ext = os.path.splitext(path)
        while tmp_ext:
            exts.append(tmp_ext)
            tmp_path, tmp_ext = os.path.splitext(tmp_path)
        exts = tuple(reversed(exts))

        if exts[0] == '.tar':
            if len(exts) == 2:
                compression = exts[1]
                if compression == '.xz':
                    return 'lzma'
                elif compression == '.gz':
                    return 'gzip'
                elif compression == '.bz2':
                    return 'bzip2'
                else:
                    return compression.strip('.').lower()
            else:
                return 'tar'
        elif exts[0] == '.zip':
            return 'zip'

        raise ValueError("Cannot infer file format, please specify")

    @staticmethod
    def _get_file_extension(fmt):
        """Helper function to get file extension based on format"""
        if fmt == 'lzma':
            return '.tar.xz'
        elif fmt == 'bzip2':
            return '.tar.bz2'
        elif fmt == 'gzip':
            return '.tar.gz'
        elif fmt == 'zip':
            return '.zip'
        elif fmt == 'tar':
            return '.tar'
        else:
            return '.%s' % fmt

    # Abstract methods

    def fit(self, *args, **kwargs):
        """Fit the model

        Fits the constructed model using the parameters specified.

        Parameters
        ----------
        args : optional
            Arguments to use in fit call.
        kwargs : optional
            Any additional keyword arguments to use in fit call.

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

    def score(self, *args, **kwargs):
        """Scores the model for the given inputs and outputs

        Parameters
        ----------
        args : optional
            Additional arguments to pass to the score call.
        kwargs : optional
            Additional keyword-arguments to pass to the score call.

        Returns
        -------
        float
            Score for the model on the given inputs and outputs.

        """
        pass


#
#   Exceptions
#

class ModelException(Exception):
    """
    Base class for Model exceptions.
    """
    pass
