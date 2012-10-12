# -*- coding: utf-8 -*-
import unittest

from skink.build.parser import Parser


class ParserTestCase(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()

    def test_has_load_method(self):
        assert self.parser.load_from_file
