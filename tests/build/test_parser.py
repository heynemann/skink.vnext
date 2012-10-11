# -*- coding: utf-8 -*-
import unittest

from skink.build.parser import Parser


class ParserTestCase(unittest.TestCase):

    def setUp(self):
        self.path = "qualquer"
        self.parser = Parser(self.path)

    def test_tem_metodo_load(self):
        assert self.parser.load

    def test_iniciar_parser_com_path(self):
        self.assertEqual(self.path, self.parser._file_path)
