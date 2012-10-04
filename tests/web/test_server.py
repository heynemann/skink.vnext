#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

from tornado.testing import AsyncHTTPTestCase

from skink.web.server import Server


class ServerTestCase(unittest.TestCase):

    def test_server_instance(self):
        server = Server()
        assert isinstance(
            server,
            Server
        ), "Should have returned a server instance"

    def test_server_has_defaults(self):
        server = Server()
        assert server.port == 8888
        assert server.instances == 0
        assert server.healthcheck_response == 'WORKING'
        assert not server.debug

    def test_should_receive_port(self):
        server = Server(['--port=10'])
        assert server.port == 10

    def test_should_receive_instance(self):
        server = Server(['--instances=11'])
        assert server.instances == 11

    def test_should_receive_healthcheck_response(self):
        server = Server(['--healthcheck-response=OK'])
        assert server.healthcheck_response == 'OK'

    def test_should_receive_debug_mode(self):
        server = Server(['--debug'])
        assert server.debug

    def test_should_receive_github_id(self):
        server = Server(['--github-id=testid'])
        assert server.application.github_id == 'testid'

    def test_should_receive_github_secret(self):
        server = Server(['--github-secret=testsecret'])
        assert server.application.github_secret == 'testsecret'


class ServerStartTestCase(AsyncHTTPTestCase):
    def setUp(self):
        self.server = Server(['--port=8889', '--instances=1'])
        self.server.start()
        super(ServerStartTestCase, self).setUp()

    def get_app(self):
        return self.server.application

    def test_healthcheck(self):
        result = self.fetch("/healthcheck")
        assert result.code == 200
        assert result.body == 'WORKING'
