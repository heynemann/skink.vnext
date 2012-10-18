#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import argparse
import logging

import redisco

from skink.version import version

class ProjectsMonitor(object):

    def __init__(self, args=[]):
        self.arguments = args
        self.process_arguments()

    def start(self):
        msg = 'skink-monitor started'
        redisco.connection_setup(host=self.redis_host, port=self.redis_port, db=10)
        logging.info(msg)

    def process_arguments(self):
        description = 'Skink v.%s web interface.' % version
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument('-v', '--verbose', action='count', default=0)
        parser.add_argument('--redis-host', default='127.0.0.1')
        parser.add_argument('--redis-port', type=int, default=3218)

        options = parser.parse_args(self.arguments)

        self.redis_port = options.redis_port
        self.redis_host = options.redis_host

        if options.verbose == 0:
            self.log_level = 'warning'
        elif options.verbose == 1:
            self.log_level = 'info'
        else:
            self.log_level = 'debug'

        logging.basicConfig(level=getattr(logging, self.log_level.upper()))

def main():
    ProjectsMonitor(args=sys.argv[1:]).start()
