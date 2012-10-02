#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

from tornado.testing import AsyncHTTPTestCase
from tornado.httpclient import AsyncHTTPClient

from skink.web.server import Server

class ServerTestCase(unittest.TestCase):

    def test_server_instance(self):
        server = Server()
        assert isinstance(server, Server), "Should have returned a server instance"

    def test_server_has_defaults(self):
        server = Server()
        assert server.port == 8888
        assert server.instances == 0
        assert server.healthcheck_response == 'WORKING'

    def test_should_receive_port(self):
        server = Server(['--port=10'])
        assert server.port == 10

    def test_should_receive_instance(self):
        server = Server(['--instances=11'])
        assert server.instances == 11

    def test_should_receive_healthcheck_response(self):
        server = Server(['--healthcheck-response=OK'])
        assert server.healthcheck_response == 'OK'


class ServerStartTestCase(AsyncHTTPTestCase):

    def get_http_server(self):
        self.server = Server(['--port=8889', '--instances=1'])
        self.server.start()
        return self.server.http_server

    def test_healthcheck(self):
        client = AsyncHTTPClient(self.io_loop)
        client.fetch("http://localhost:8889/healtcheck", self.handle_fetch)
        result = self.wait()
        assert result == 'WORKING'

