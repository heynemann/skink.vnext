#!/usr/bin/python
# -*- coding: utf-8 -*-

from tornado.testing import AsyncHTTPTestCase

from skink.web.application import Application


class IndexTestCase(AsyncHTTPTestCase):
    def get_app(self):
        self.application = Application(healthcheck_response='testhealth')
        return self.application

    def test_index(self):
        result = self.fetch("/")
        assert result.code == 200
