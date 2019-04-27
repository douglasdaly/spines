# -*- coding: utf-8 -*-
"""
Unit tests for the transforms subpackage.
"""
#
#   Imports
#
import pytest

from spines import transforms


#
#   Unit tests
#

@pytest.mark.usefixtures('class_transform')
class TestPassSimple(object):
    """
    Tests for the Pass transform object
    """
    _TRANSFORM_CLS = transforms.Pass

    @pytest.mark.parametrize('data_in, data_out', [
        (5, 5), (10., 10.), ('Hello', 'Hello'), ((1, 2), (1, 2))
    ])
    def test_transform(self, data_in, data_out):
        assert self.transform.transform(data_in) == data_out
