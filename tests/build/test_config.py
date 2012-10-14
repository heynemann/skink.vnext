# -*- coding: utf-8 -*-
import __builtin__
try:
        import unittest2 as unittest
except ImportError, e:
        import unittest

from mock import patch, mock_open, ANY

from skink.build.entities import Config


@patch('__builtin__.open')
class ConfigTestCase(unittest.TestCase):

    def setUp(self):
        self.config = Config()

    def test_has_method_create_from_file(self, *args):
        assert Config.create_from_file

    def test_return_new_config_instance(self, *args):
        some_file_path = "tmp/teste.yaml"
        assert isinstance(Config.create_from_file(some_file_path), Config)

    def test_should_open_file_passed(self, open_mock):
        Config.create_from_file('teste.yaml')
        open_mock.assert_called_once_with('teste.yaml')

    @patch('yaml.load')
    def test_should_call_yaml_loader(self, open_mock, yaml_mock):
        Config.create_from_file('teste.yaml')
        yaml_mock.assert_called_once_with(ANY)
