# -*- coding: utf-8 -*-
"""
Base classes for the project subpackage.
"""
from typing import Mapping as T_Mapping
from typing import Type

from sortedcontainers import SortedDict
import toml


class Project(object):
    """
    Project class for managing project components.
    """

    def __init__(self) -> None:
        self._sources = SortedDict()
        self._components = SortedDict()
        return

    def __getitem__(self, item) -> T_Mapping[str, str]:
        return self.components[item]

    @property
    def sources(self) -> T_Mapping[str, T_Mapping[str, str]]:
        """dict: Sources used in this project"""
        return self._sources

    @property
    def components(self) -> T_Mapping[str, T_Mapping[str, str]]:
        """dict: Components used in this project"""
        return self._components

    def add_source(self, source: str, **parameters) -> None:
        """Adds a source to this project.

        Parameters
        ----------
        source : str
            Source to add to this project.
        parameters : optional
            Any additional specifications/parameters for this source.

        """
        self._sources[source] = parameters
        return

    def remove_source(self, source: str) -> T_Mapping[str, str]:
        """Removes (and returns) the source specification given.

        Parameters
        ----------
        source : str
            The source to remove the specification for.

        Returns
        -------
        :obj:`dict` of :obj:`str` to :obj:`str`
            The specification for the source removed.

        """
        return self._sources.pop(source)

    def add_component(
        self, name: str, version: str = None, **parameters
    ) -> None:
        """Adds a component to this project.

        Parameters
        ----------
        name : str
            The name of the component to add to this project.
        version : str, optional
            The version of the component to add to this project (the
            default is "*", most recent).
        parameters : optional
            Any additional parameters to specify for this component.

        """
        version = version or "*"
        self._components[name] = {'version': version, **parameters}
        return

    def remove_component(self, name: str) -> T_Mapping[str, str]:
        """Removes (and returns) the component specification.

        Parameters
        ----------
        name : str
            Name of the component to remove the specification for.

        Returns
        -------
        :obj:`dict` of :obj:`str` to :obj:`str`
            The specification(s) that were set for the component
            removed.

        """
        return self._components.pop(name)

    def save(self, path: str) -> None:
        """Saves this project configuration to file.

        Parameters
        ----------
        path : str
            The file to save this project configuration to.

        """
        data = self._to_dict()
        with open(path, 'w') as fout:
            toml.dump(data, fout)
        return path

    @classmethod
    def load(cls, path: str) -> Type['Project']:
        """Loads a new :obj:`Project` object from file.

        Parameters
        ----------
        path : str
            Path to the :obj:`Project` specification to load.

        Returns
        -------
        Project
            A new :obj:`Project` instance loaded from the `path` given.

        """
        with open(path, 'r') as fin:
            data = toml.load(fin)
        return cls._from_dict(data)

    def _to_dict(self) -> T_Mapping:
        data = {}
        data['sources'] = [
            {'name': k, **v} for k, v in self.sources.items()
        ]
        data['components'] = self.components
        return data

    @classmethod
    def _from_dict(cls, data: T_Mapping) -> Type['Project']:
        new_proj = cls()
        for src in data['sources']:
            new_proj.add_source(src.pop('name'), **src)
        for k, v in data['components']:
            new_proj.add_component(k, **v)
        return new_proj
