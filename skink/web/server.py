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

import sys
import argparse
import logging

import tornado.ioloop
import tornado.httpserver
import redisco

from skink.version import version
from skink.web.application import Application


class Server:
    def __init__(self, args=[]):
        self.arguments = args

        self.process_arguments()

    def process_arguments(self):
        description = 'Skink v.%s web interface.' % version
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument('-b', '--bind', default='127.0.0.1')
        parser.add_argument('-p', '--port', type=int, default=8888)
        parser.add_argument('-i', '--instances', type=int, default=0)
        parser.add_argument('-r', '--healthcheck-response', default="WORKING")

        parser.add_argument('-d',
                            '--debug',
                            action="store_true",
                            default=False
                            )

        parser.add_argument('--redis-host', default='127.0.0.1')
        parser.add_argument('--redis-port', type=int, default=3218)

        parser.add_argument('-v', '--verbose', action='count', default=0)
        parser.add_argument(
            '--github-client-id',
            default="165b0d755a7432301dd4"
        )
        parser.add_argument('--github-secret', default="15c3838dc34bb63efa152e96f40bbfea8c8b49c6")
        parser.add_argument('--github-redirect-url',
                            default="http://localhost:8888/auth/github")

        options = parser.parse_args(self.arguments)

        self.bind = options.bind
        self.port = options.port
        self.instances = options.instances
        self.healthcheck_response = options.healthcheck_response
        self.debug = options.debug

        if self.debug:
            self.instances = 1

        if options.verbose == 0:
            self.log_level = 'warning'
        elif options.verbose == 1:
            self.log_level = 'info'
        else:
            self.log_level = 'debug'

        logging.basicConfig(level=getattr(logging, self.log_level.upper()))

        logging.debug('Connecting at redis %s:%d...' % (options.redis_host, options.redis_port))
        redisco.connection_setup(host=options.redis_host, port=options.redis_port, db=10)

        self.application = Application(
            healthcheck_response=self.healthcheck_response,
            debug=self.debug,
            github_client_id=options.github_client_id,
            github_secret=options.github_secret,
            github_redirect_url=options.github_redirect_url
        )

    def start(self):
        msg = 'skink-web started at http://%s:%s' % (self.bind, self.port)
        logging.info(msg)
        self.http_server = tornado.httpserver.HTTPServer(self.application)
        self.http_server.bind(self.port, self.bind)
        self.http_server.start(self.instances)


def main():
    Server(args=sys.argv[1:]).start()
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
