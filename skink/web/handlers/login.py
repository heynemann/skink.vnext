#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2012 Bernardo Heynemann

# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
# Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import logging

import tornado.web
import tornado.escape
import tornado.httputil

from skink.web.handlers.base import BaseHandler
from skink.web.handlers.github import GithubMixin

class NotAuthenticatedHandler(BaseHandler):

    def get(self):
        self.render('not_authenticated.html')
 

class LoginHandler(BaseHandler, GithubMixin):

    @tornado.web.asynchronous
    def get(self):
        redirect_url = self.application.github_redirect_url

        # we can append next to the redirect uri, so the user gets the
        # correct URL on login
        redirect_uri = tornado.httputil.url_concat(
            redirect_url,
            {'next': '/'}
        )

        # if we have a code, we have been authorized so we can log in
        if self.get_argument("code", False):
            self.get_authenticated_user(
                redirect_uri=redirect_uri,
                client_id=self.application.github_client_id,
                client_secret=self.application.github_secret,
                code=self.get_argument("code"),
                callback=self.async_callback(self._on_login)
            )
            return

        # otherwise we need to request an authorization code
        self.authorize_redirect(
            redirect_uri=redirect_uri,
            client_id=self.application.github_client_id,
            extra_params={}
        )

    def _on_login(self, user):
        """ This handles the user object from the login request """
        if user:
            logging.info('logged in user from github: ' + str(user))
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
        else:
            self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))


class LogoffHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect('/')

#class GistLister(BaseHandler, github.GithubMixin):

    #@tornado.web.authenticated
    #@tornado.web.asynchronous
    #def get(self):
        #self.github_request(
                #'/gists', self._on_get_gists,
                #access_token=self.current_user['access_token'])

    #def _on_get_gists(self, gists):
        #self.render('gists.jade', gists=gists)
