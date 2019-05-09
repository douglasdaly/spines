# -*- coding: utf-8 -*-
"""
Setup file for Spines library.

Incorporates code from:
    https://github.com/sarugaku/cookiecutter-python-package

"""
#
#   Imports
#
import ast
import os

from setuptools import setup, find_packages


#
#   Configuration
#

ROOT = os.path.dirname(__file__)

PACKAGE_NAME = 'spines'

VERSION = None

with open(os.path.join(ROOT, 'src', PACKAGE_NAME, '__version__.py')) as fin:
    for line in fin:
        if line.startswith('__version__ = '):
            VERSION = ast.literal_eval(line[len('__version__ = '):].strip())
            break

if VERSION is None:
    raise EnvironmentError('Failed to read version')

REQUIRES = [
    'appdirs',
    'click',
    'parver',
    'toml',
    'xxhash',
]


#
#   Setup
#

setup(
    name="spines",
    version=VERSION,
    package_dir={'': 'src'},
    packages=find_packages('src', include=['spines', 'spines.*']),
    entry_points={
        "console_scripts": [
            "spines=spines:cli",
        ]
    },

    include_package_data=True,
    package_data={
        '': ['*LICENSE', 'README*'],
    },

    python_requires=">=3.6",
    install_requires=REQUIRES,
    extras_require={
        "test": [
            "pytest", "pytest-cov", "pytest-timeout", "pytest-xdist"
        ],
    },

    project_urls={
        'Source Code': 'https://www.github.com/douglasdaly/spines',
        'Documentation': 'https://spines.readthedocs.io/',
    }
)
