#!/usr/bin/python
# -*- coding: utf-8 -*-

from tornado.testing import AsyncHTTPTestCase
from tornado.httpclient import AsyncHTTPClient

from skink.web.server import Server
from skink.web.application import Application

class ApplicationTestCase(AsyncHTTPTestCase):
    def setUp(self):
        self.server = Server(['--instances=1', '--healthcheck-response=testhealth'])
        self.server.start()
        self.application = self.server.application
        super(ApplicationTestCase, self).setUp()

    def get_app(self):
        return self.server.application

    def test_healthcheck(self):
        result = self.fetch("/healthcheck")
        assert result.code == 200
        assert result.body == 'testhealth'

