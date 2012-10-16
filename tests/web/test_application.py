#!/usr/bin/python
# -*- coding: utf-8 -*-

from tornado.testing import AsyncHTTPTestCase

from skink.web.application import Application
from skink.web.handlers import HealthCheckHandler, IndexHandler


class ApplicationTestCase(AsyncHTTPTestCase):
    def get_app(self):
        self.application = Application()
        return self.application

    def test_proper_application(self):
        assert isinstance(self.application, Application)

    def test_default_github_info(self):
        assert self.application.github_client_id is None
        assert self.application.github_secret is None
        assert self.application.github_redirect_url == 'http://localhost:8888/auth/github'

    def test_has_default_settings(self):
        assert self.application.default_settings['login_url'] == '/auth/login'
        assert not self.application.default_settings['debug']
        cookie_secret = self.application.default_settings['cookie_secret']
        assert cookie_secret == '61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo='

    def test_has_healthcheck_route(self):
        assert (
            r"/healthcheck/?",
            HealthCheckHandler
        ) in self.application.routes

    def test_has_index_route(self):
        assert (
            r"/?",
            IndexHandler
        ) in self.application.routes
