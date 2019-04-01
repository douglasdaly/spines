# -*- coding: utf-8 -*-
"""
Unit tests for the ParameterStore class.
"""
#
#   Imports
#
import os
import pickle
import tempfile

from spines.parameters.base import ParameterStore, Parameter


#
#   Helpers
#


#
#   Unit test
#

def test_pickle_parameter_store():
    """Tests the pickling of a ParameterStore object"""
    pstore = ParameterStore()
    pstore.add(Parameter('test', float))
    pstore.add(Parameter('other', int))

    tmp = tempfile.mktemp(suffix='.pkl')
    try:
        with open(tmp, 'wb') as fout:
            pickle.dump(pstore, fout)

        assert os.path.isfile(tmp)

        with open(tmp, 'rb') as fin:
            load_pstore = pickle.load(fin)

        for name, option in load_pstore.options.items():
            assert option.name == pstore.options[name].name
            assert option.value_type == pstore.options[name].value_type
            assert option.required == pstore.options[name].required
            assert option.default == pstore.options[name].default
    finally:
        os.remove(tmp)
