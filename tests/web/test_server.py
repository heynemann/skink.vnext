#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

from skink.web.server import Server

class ServerTestCase(unittest.TestCase):

    def test_server_instance(self):
        server = Server()
        assert isinstance(server, Server), "Should have returned a server instance"

    def test_server_has_defaults(self):
        server = Server()
        assert server.port == 8888
        assert server.bind == '0.0.0.0'

    def test_should_receive_port(self):
        server = Server(['--port=10'])
        assert server.port == 10

