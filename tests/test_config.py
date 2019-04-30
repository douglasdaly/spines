# -*- coding: utf-8 -*-
"""
Unit tests for the config subpackage.
"""
#
#   Imports
#
from spines.config.base import BaseConfig


#
#   Unit tests
#

class TestBaseConfig(object):
    """
    Tests for the BaseConfig object
    """

    def test_init(self):
        cfg = BaseConfig({'a': 5, 'b': '10'})

        assert cfg['a'] == 5
        assert cfg['b'] == '10'

    def test_getattr(self):
        cfg = BaseConfig({'a': 5, 'b': '10'})
        cfg['c.d.e'] = 100

        assert cfg.a == 5
        assert cfg.b == '10'
        assert cfg.c.d.e == 100

    def test_get_set(self):
        cfg = BaseConfig()
        cfg['key'] = 'value'
        cfg['other.key'] = 'other_value'

        assert cfg['key'] == 'value'
        assert cfg['other.key'] == 'other_value'
        assert cfg['other']['key'] == 'other_value'
        assert cfg['OTHER.KEY'] == cfg['OTHER']['KEY']

    def test_copy(self):
        cfg = BaseConfig()
        cfg['a.a'] = 1
        cfg['a.b'] = 'Hello'

        assert cfg == cfg.copy()

    def test_update_dict(self):
        cfg = BaseConfig()
        cfg['a.a'] = 1
        cfg['a.b'] = 2
        cfg['a.c'] = 'Hello'

        cfg.update({'a.a': 2, 'a': {'b': 3, 'c': 'World'}})

        assert cfg['a.a'] == 2
        assert cfg['a.b'] == 3
        assert cfg['a.c'] == 'World'

    def test_update_other_config(self):
        cfg_a = BaseConfig()
        cfg_a['a.a'] = 1
        cfg_a['a.b'] = 2
        cfg_a['a.c'] = 'Hello'

        cfg_b = BaseConfig()
        cfg_b['a.a'] = 2
        cfg_b['a.b'] = 3
        cfg_b['a.c'] = 'World'
        cfg_b['b'] = 'Added'

        cfg_a2b = cfg_a.copy()
        cfg_a2b.update(cfg_b)

        cfg_b2a = cfg_b.copy()
        cfg_b2a.update(cfg_a)

        for k in cfg_a.keys():
            assert cfg_a2b[k] == cfg_b[k]
            assert cfg_b2a[k] == cfg_a[k]

        assert cfg_a2b['b'] == cfg_b['b']
        assert cfg_b2a['b'] == cfg_b['b']
