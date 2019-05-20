# -*- coding: utf-8 -*-
"""
Unit tests for the project module.
"""
#
#   Imports
#
import os

from spines.project import utils

from .helpers import RESOURCE_DIR


#
#   Constants
#

PROJECT_RESOURCES = os.path.join(RESOURCE_DIR, 'project')


#
#   Unit tests
#

class TestUtils(object):
    """
    Tests for the project utilities module.
    """

    def test_find_project_dir(self):
        test_a = utils.find_project_dir(
            os.path.join(PROJECT_RESOURCES, 'test_project')
        )
        assert test_a == os.path.join(PROJECT_RESOURCES, 'test_project')

        test_b = utils.find_project_dir(
            os.path.join(PROJECT_RESOURCES, 'test_project', 'subdir')
        )
        assert test_b == test_a

        test_d = utils.find_project_dir(
            os.path.join(PROJECT_RESOURCES, 'test_no_project')
        )
        assert test_d is None
