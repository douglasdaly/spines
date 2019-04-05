# -*- coding: utf-8 -*-
"""
Unit tests for the Model class.
"""
#
#   Imports
#
import os
import tempfile

from spines import Model, Parameter


#
#   Helpers
#

class LineModel(Model):
    """Test model class"""
    m = Parameter(float)
    b = Parameter(float)

    def fit(self, x, y, intercept=0.):
        self.b = intercept
        self.m = (y-intercept) / x

    def predict(self, x):
        return self.m * x + self.b

    def score(self, x, y):
        pred_y = self.predict(x)
        return (y - pred_y) ** 2


def model_file_function(fmt, new):
    """Tests the load/save capabilities of the Model class"""
    fmt = fmt.lower()

    test_mod = LineModel()

    file_ext = test_mod._get_file_extension(fmt)
    tmp = tempfile.mktemp(suffix=file_ext)
    try:
        _ = test_mod.save(tmp, fmt=fmt)
        assert os.path.isfile(tmp)

        load_mod = LineModel.load(tmp, fmt=fmt, new=new)
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
