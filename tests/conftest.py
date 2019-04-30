# -*- coding: utf-8 -*-
"""
PyTest configuration file for the spines unit tests
"""
#
#   Imports
#
import pytest

from .helpers import get_line_model


#
#   Fixtures
#

@pytest.fixture(scope='function')
def line_model():
    yield get_line_model(1.0, 2.0)


@pytest.fixture(scope='class')
def class_line_model(request):
    request.cls.line_model = get_line_model(1.0, 2.0)
    yield


@pytest.fixture(scope='class')
def class_transform(request):
    if hasattr(request.cls, '_init_transform'):
        request.cls.transform = request.cls._init_transform()
    else:
        request.cls.transform = request.cls._TRANSFORM_CLS()
    yield
