# -*- coding: utf-8 -*-
"""
Helper functions and classes for unit tests.
"""
#
#   Imports
#
import os

from spines import Model
from spines import Parameter


#
#   Constants
#

TESTS_ROOT = os.path.abspath(os.path.dirname(__file__))
RESOURCE_DIR = os.path.join(TESTS_ROOT, 'resources')


#
#   Model
#

class LineModel(Model):
    """
    Test model class for simple line
    """
    m = Parameter(float)
    b = Parameter(float)

    def fit(self, x, y, intercept=0.):
        """Fits the model"""
        self.b = intercept
        self.m = (y-intercept) / x

    def predict(self, x):
        """Get single prediction from fitted model"""
        return self.m * x + self.b

    def error(self, x, y):
        """Mean squared error"""
        pred_y = self.predict(x)
        return (y - pred_y) ** 2


#
#   Factory functions
#

def get_line_model(x, y, intercept=0.):
    """Gets a fitted LineModel instance"""
    ret = LineModel()
    ret.fit(x, y, intercept=intercept)
    return ret
