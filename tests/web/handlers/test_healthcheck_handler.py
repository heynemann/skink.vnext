#!/usr/bin/python
# -*- coding: utf-8 -*-

from tornado.testing import AsyncHTTPTestCase

from skink.web.application import Application


class HealthCheckTestCase(AsyncHTTPTestCase):
    def get_app(self):
        self.application = Application(healthcheck_response='testhealth')
        return self.application

    def test_healthcheck(self):
        result = self.fetch("/healthcheck")
        assert result.code == 200
        assert result.body == 'testhealth'
