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

import tornado.ioloop
import tornado.httpserver

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
        parser.add_argument('-d', '--debug', action="store_true", default=False)

        options = parser.parse_args(self.arguments)

        self.bind = options.bind
        self.port = options.port
        self.instances = options.instances
        self.healthcheck_response = options.healthcheck_response
        self.debug = options.debug

        self.application = Application(
            healthcheck_response=self.healthcheck_response
        )

    def start(self):
        self.http_server = tornado.httpserver.HTTPServer(self.application)
        self.http_server.bind(self.port, self.bind)
        self.http_server.start(self.instances)


def main():
    server = Server(args=sys.argv[1:])
    server.start()
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
