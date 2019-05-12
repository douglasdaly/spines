# -*- coding: utf-8 -*-
"""
Tests for the spines crypto utilities.
"""
#
#   Imports
#
import os

from spines.utils import crypto

from ..helpers import RESOURCE_DIR


#
#   Constants
#

HASHING_DIR = os.path.join(RESOURCE_DIR, 'hashing')


#
#   Unit tests
#

class TestHashing(object):
    """
    Tests for the hash-related functions in the crypto utilities
    """

    def test_load_hashes(self):
        test_a = crypto.load_hashes(HASHING_DIR, 'test.txt.sha256')
        test_b = crypto.load_hashes(HASHING_DIR, 'test2.txt.sha256')

        assert 'test.txt' in test_a.keys()
        assert 'test.txt' in test_b.keys()

        ta_val = test_a['test.txt']
        tb_val = test_b['test.txt']

        assert ta_val[0] is False
        assert ta_val[1] == \
            'f29bc64a9d3732b4b9035125fdb3285f5b6455778edca72414671e0ca3b2e0de'

        assert tb_val[0] is True
        assert tb_val[1] == \
            'f29bc64a9d3732b4b9035125fdb3285f5b6455778edca72414671e0ca3b2e0de'

        test_d = crypto.load_hashes(HASHING_DIR, 'test_dir')
        d_dict = dict(zip(('test%s.txt' % x for x in (1, 2)), (
            'fdbbb3e0171fe6128fd3351fe6e48a698b74096d88a1dd746f44b43df823975d',
            '948dbc0200407c063f3e4bbf2d4f43ab84c53e6a7cf3709cb8bb703f78ccfe9d'
        )))

        for fname, fhash in d_dict.items():
            assert fname in test_d.keys()
            td_val = test_d[fname]
            assert td_val[0] is False
            assert td_val[1] == fhash

        return

    def test_file_hash(self):
        test_a = crypto.load_hashes(HASHING_DIR, 'test.txt.sha256')
        test_b = crypto.load_hashes(HASHING_DIR, 'test2.txt.sha256')

        for k, v in test_a.items():
            t_h = crypto.hash_file(HASHING_DIR, k, binary_mode=v[0])
            assert t_h == v[1]

        for k, v in test_b.items():
            t_h = crypto.hash_file(HASHING_DIR, k, binary_mode=v[0])
            assert t_h == v[1]

        return

    def test_find_hash_file(self):
        test_a = crypto.find_hash_file(HASHING_DIR, 'test_dir')
        assert test_a == os.path.join(
            HASHING_DIR, 'test_dir', 'test_dir' + crypto.HASH_EXTENSION
        )

    def test_verify_hashes(self):
        test_a = crypto.verify_hashes(HASHING_DIR, 'test.txt')
        assert all(test_a.values())

        test_b = crypto.verify_hashes(
            HASHING_DIR, 'test.txt',
            hash_path=os.path.join(HASHING_DIR, 'test2.txt.sha256')
        )
        assert all(test_b.values())

        test_c = crypto.verify_hashes(HASHING_DIR, 'test_dir')
        assert all(test_c.values())

        test_d = crypto.verify_hashes(HASHING_DIR, 'test_subdir')
        assert all(test_d.values())

        test_e = crypto.verify_hashes(HASHING_DIR, 'test_dir_fail')
        for k, v in test_e.items():
            if k in ('test3.txt', 'subdir/test_sub2.txt'):
                assert v is False
            else:
                assert v
