# -*- coding: utf-8 -*-
try:
        import unittest2 as unittest
except ImportError, e:
        import unittest

from skink.build.entities import Config


class ConfigTestCase(unittest.TestCase):

    def setUp(self):
        self.config = Config()

    def test_has_method_create_from_file(self):
        assert Config.create_from_file

    def test_return_new_config_instance(self):
        some_file_path = "tmp/teste.yaml"
        assert isinstance(Config.create_from_file(some_file_path), Config)
