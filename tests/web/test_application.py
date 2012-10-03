#!/usr/bin/python
# -*- coding: utf-8 -*-

from tornado.testing import AsyncHTTPTestCase

from skink.web.application import Application
from skink.web.handlers import HealthCheckHandler


class ApplicationTestCase(AsyncHTTPTestCase):
    def get_app(self):
        self.application = Application()
        return self.application

    def test_proper_application(self):
        assert isinstance(self.application, Application)

    def test_has_healthcheck_route(self):
        assert (
            r"/healthcheck/?",
            HealthCheckHandler
        ) in self.application.routes
