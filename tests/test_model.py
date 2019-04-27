# -*- coding: utf-8 -*-
"""
Unit tests for the Model class.
"""
#
#   Imports
#
import os
import tempfile

import pytest

from spines import utils

from .helpers import get_line_model


#
#   Unit tests
#

@pytest.mark.usefixtures('class_line_model')
class TestInitialization(object):
    """
    Tests for various model initialization code
    """

    @pytest.mark.parametrize('x, y', [(2.0, 2.5), (0.0, 1.0)])
    def test_auto_score_func(self, x, y):
        err_val = self.line_model.error(x, y)
        assert self.line_model.score(x, y) == -err_val


class TestFitFunctions(object):
    """
    Tests for model fitting functions
    """

    @pytest.mark.parametrize('x, y, intc', [(1.0, 2.0, 0.0), (1.0, 5.0, 1.0)])
    def test_line_model(self, x, y, intc):
        lm = get_line_model(x, y, intercept=intc)
        assert lm.predict(x) == y
        assert lm.error(x, y) == 0.


@pytest.mark.usefixtures('class_line_model')
class TestFileFunctions(object):
    """
    Tests for Model file functions
    """

    def test_zip_file(self):
        self._model_file_function(self.line_model, 'zip')

    def test_lzma_file(self):
        self._model_file_function(self.line_model, 'lzma')

    def test_bzip2_file(self):
        self._model_file_function(self.line_model, 'bzip2')

    def test_gzip_file(self):
        self._model_file_function(self.line_model, 'gzip')

    @staticmethod
    def _model_file_function(model, fmt):
        """Tests the load/save capabilities of the Model class"""
        file_ext = utils.file.get_extension(fmt)
        for new in [False, True]:
            tmp = tempfile.mktemp(suffix=file_ext)
            try:
                tmp = model.save(tmp, fmt=fmt)
                assert os.path.isfile(tmp)

                load_mod = model.__class__.load(tmp, fmt=fmt, new=new)
                for param, value in load_mod.parameters.items():
                    assert model.parameters[param] == value
            except Exception:
                raise
            finally:
                os.remove(tmp)
        return
