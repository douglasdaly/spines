# -*- coding: utf-8 -*-
"""
Unit tests for the Model class.
"""
#
#   Imports
#
import os
import tempfile

from spines import Model


#
#   Helpers
#

class ModelTestImpl(Model):
    """Test model class"""

    def fit(self):
        return

    def predict(self):
        return

    def score(self):
        return 0.


def model_file_function(fmt, new):
    """Tests the load/save capabilities of the Model class"""
    fmt = fmt.lower()

    test_mod = ModelTestImpl()

    test_mod.add_parameter('test', float)
    test_mod.add_hyper_parameter('test hp', float)

    test_mod.set_parameter('test', 1.0)
    test_mod.set_hyper_parameter('test hp', 2.0)

    file_ext = test_mod._get_file_extension(fmt)
    tmp = tempfile.mktemp(suffix=file_ext)
    try:
        _ = test_mod.save(tmp, fmt=fmt)
        assert os.path.isfile(tmp)

        load_mod = ModelTestImpl.load(tmp, fmt=fmt, new=new)
        for param, value in load_mod.parameters.items():
            assert test_mod.parameters[param] == value
    finally:
        os.remove(tmp)
    return


#
#   Unit tests
#

def test_file_functions():
    """Tests the Model file functions"""
    for fmt in ['zip', 'lzma', 'bzip2', 'gzip']:
        for new in [True, False]:
            model_file_function(fmt, new)
    return
