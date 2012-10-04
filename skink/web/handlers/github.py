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


import tornado.ioloop
import tornado.web
import tornado.auth
import tornado.httpclient
import tornado.escape
import tornado.httputil
import logging


# found it here: http://casbon.me/connecting-to-githubs-oauth2-api-with-tornado
class GithubMixin(tornado.auth.OAuth2Mixin):
    """
    Github OAuth Mixin, based on FacebookGraphMixin
    """

    _OAUTH_AUTHORIZE_URL = 'https://github.com/login/oauth/authorize'
    _OAUTH_ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token'
    _API_URL = 'https://api.github.com'

    def get_authenticated_user(
            self,
            redirect_uri,
            client_id,
            client_secret,
            code,
            callback,
            extra_fields=None):
        """
        Handles the login for Github, queries /user and returns a user object
        """

        logging.debug('gau ' + redirect_uri)
        http = tornado.httpclient.AsyncHTTPClient()
        args = {
            "redirect_uri": redirect_uri,
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
        }

        oauth_url = self._oauth_request_token_url(**args)
        oauth_callback = self.async_callback(
            self._on_access_token,
            redirect_uri,
            client_id,
            client_secret,
            callback,
            extra_fields
        )

        http.fetch(oauth_url, oauth_callback)

    def _on_access_token(self, redirect_uri, client_id, client_secret,
                         callback, fields, response):
        """ callback for authentication url, if successful get the user details """

        if response.error:
            logging.warning('Github auth error: %s' % str(response))
            callback(None)
            return

        args = tornado.escape.parse_qs_bytes(
            tornado.escape.native_str(response.body)
        )

        if 'error' in args:
            logging.error('oauth error ' + args['error'][-1])
            raise Exception(args['error'][-1])

        session = {
            "access_token": args["access_token"][-1],
        }

        request_callback = self.async_callback(
            self._on_get_user_info,
            callback,
            session
        )

        self.github_request(
            path="/user",
            callback=request_callback,
            access_token=session["access_token"],
        )

    def _on_get_user_info(self, callback, session, user):
        """ callback for github request /user to create a user """

        logging.debug('user data from github ' + str(user))

        if user is None:
            callback(None)
            return

        callback({
            "login": user["login"],
            "name": user["name"],
            "email": user["email"],
            "access_token": session["access_token"],
        })

    def github_request(self, path, callback, access_token=None,
                       method='GET', body=None, **args):
        """ Makes a github API request, hands callback the parsed data """

        args["access_token"] = access_token

        url = tornado.httputil.url_concat(self._API_URL + path, args)

        logging.debug('request to ' + url)
        http = tornado.httpclient.AsyncHTTPClient()

        if body is not None:
            body = tornado.escape.json_encode(body)
            logging.debug('body is' + body)

        fetch_callback = self.async_callback(self._parse_response, callback)
        http.fetch(url, callback=fetch_callback, method=method, body=body)

    def _parse_response(self, callback, response):
        """ Parse the JSON from the API """

        if response.error:
            logging.warning("HTTP error from Github: %s", response.error)
            callback(None)
            return

        try:
            json = tornado.escape.json_decode(response.body)
        except Exception:
            logging.warning("Invalid JSON from Github: %r", response.body)
            callback(None)
            return

        if isinstance(json, dict) and json.get("error_code"):
            logging.warning("Facebook error: %d: %r", json["error_code"],
                            json.get("error_msg"))
            callback(None)
            return

        callback(json)
