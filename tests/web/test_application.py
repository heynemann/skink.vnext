#!/usr/bin/python
# -*- coding: utf-8 -*-

from tornado.testing import AsyncHTTPTestCase
from tornado.httpclient import AsyncHTTPClient

from skink.web.server import Server
from skink.web.application import Application

class ApplicationTestCase(AsyncHTTPTestCase):
    def setUp(self):
        self.server = Server(['--port=8889', '--instances=1'])
        self.server.start()
        self.application = self.server.application
        super(ApplicationTestCase, self).setUp()

    def get_app(self):
        return self.server.application

    def get_http_server(self):
        return self.server.http_server

    def should_be_proper_application(self):
        assert isinstance(self.application, Application)
