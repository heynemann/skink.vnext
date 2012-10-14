# -*- coding: utf-8 -*-
import __builtin__
try:
        import unittest2 as unittest
except ImportError, e:
        import unittest

from mock import patch, ANY
from contextlib import nested

from skink.build.entities import Config


class ConfigTestCase(unittest.TestCase):

    def setUp(self):
        with nested(
            patch('__builtin__.file'),
            patch('yaml.load')
        ) as (self.file_mock, self.yaml_load_mock):
            self.config = Config.create_from_file("teste.yaml")

    def test_return_new_config_instance(self):
        assert isinstance(self.config, Config)

    def test_should_open_file_passed(self):
        self.file_mock.assert_called_once_with('teste.yaml', 'r')

    def test_should_call_yaml_loader(self):
        self.yaml_load_mock.assert_called_once_with(ANY)
