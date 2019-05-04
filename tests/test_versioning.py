# -*- coding: utf-8 -*-
"""
Unit tests for the spines versioning subpackage.
"""
#
#   Imports
#
from spines import versioning


#
#   Unit tests
#

class TestFunctionSignature(object):
    """
    Unit tests for the FunctionSignature object
    """

    def test_compare_simple(self):
        """Test simple comparisons"""
        cls = self.__class__
        sig_a = versioning.FunctionSignature(cls._function_a)
        sig_b = versioning.FunctionSignature(cls._function_b)
        sig_c = versioning.FunctionSignature(cls._function_c)
        sig_d = versioning.FunctionSignature(cls._function_d)

        assert sig_a == sig_a
        assert sig_a != sig_b
        assert sig_c != sig_a
        assert sig_d != sig_a
        assert sig_c != sig_d

    def test_compare_typing(self):
        """Test comparisons with typing"""
        cls = self.__class__
        sig_a = versioning.FunctionSignature(cls._function_a)
        sig_at = versioning.FunctionSignature(cls._function_a_typed)
        sig_ato = versioning.FunctionSignature(cls._function_a_typed_other)
        sig_bt = versioning.FunctionSignature(cls._function_b_typed)
        sig_bto = versioning.FunctionSignature(cls._function_b_typed_other)

        assert sig_at == sig_at
        assert sig_a != sig_at
        assert sig_at != sig_ato
        assert sig_at != sig_bt
        assert sig_ato == sig_bto

    def test_similar(self):
        """Test the similar function"""
        cls = self.__class__
        sig_a = versioning.FunctionSignature(cls._function_a)
        sig_b = versioning.FunctionSignature(cls._function_b)
        sig_c = versioning.FunctionSignature(cls._function_c)
        sig_d = versioning.FunctionSignature(cls._function_d)
        sig_e = versioning.FunctionSignature(cls._function_e)

        assert sig_a.similar(sig_b)
        assert sig_b.similar(sig_a)
        assert not sig_a.similar(sig_c)
        assert not sig_a.similar(sig_e)
        assert not sig_c.similar(sig_d)
        assert not sig_d.similar(sig_c)

    # Helpers

    @staticmethod
    def _function_a(a, b, c):
        """Helper function for unit tests"""
        return a + b - c

    @staticmethod
    def _function_a_typed(a: int, b: int, c: float) -> float:
        """Helper function with typing"""
        return a + b - c

    @staticmethod
    def _function_a_typed_other(a: int, b: float, c: float) -> float:
        """Same as the typed verion but with one different type"""
        return a + b - c

    @staticmethod
    def _function_b(a, b, c):
        """Similar (but not the same) as function_a"""
        return a - b - c

    @staticmethod
    def _function_b_typed(a: int, b: int, c: float) -> float:
        """Similar (but not the same) as function_a_typed"""
        return a - b - c

    @staticmethod
    def _function_b_typed_other(a: int, b: float, c: float) -> float:
        """Same as function_a_typed_other"""
        return a + b - c

    def _function_c(self, a, b, c):
        """Method version of function_a"""
        return a + b - c

    def _function_c_reference(self, a, b, c):
        """Call other method"""
        return self._function_a(a, b, c)

    @classmethod
    def _function_d(cls, d, e, f):
        """Same as function_a but with different variable names"""
        return d + e - f

    @staticmethod
    def _function_e(a, b, c, d):
        """Different # of arguments"""
        return (a - b) + (d - c)
