# -*- coding: utf-8 -*-
"""
Unit tests for the parameters module.
"""
#
#   Imports
#
import os
import pickle
import tempfile

from spines.parameters.base import Parameter


#
#   Unit tests
#

def test_required_parameter():
    """Tests the Parameter class"""
    req_param = Parameter('Test Parameter', float, required=True)

    assert req_param.required is True
    assert req_param.check(1.0) is True
    assert req_param.check(1) is False


def test_pickle_parameter():
    """Tests the pickling of the Parameter class"""
    test_param = Parameter('Test Parameter', float, required=True)

    tmp = tempfile.mktemp(suffix='.pkl')
    try:
        with open(tmp, 'wb') as fout:
            pickle.dump(test_param, fout)

        assert os.path.isfile(tmp)

        with open(tmp, 'rb') as fin:
            load_param = pickle.load(fin)

        assert load_param.name == test_param.name
        assert load_param.value_type == test_param.value_type
        assert load_param.required == test_param.required
        assert load_param.default == test_param.default
    finally:
        os.remove(tmp)
