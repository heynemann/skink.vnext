#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time
import logging
import argparse

import redisco
from deego import VM

from skink.version import version
from skink.worker.box_types import PythonBoxType

class Worker:
    def __init__(self, args=[]):
        self.arguments = args

        self.process_arguments()

    def process_arguments(self):
        description = 'Skink v.%s worker' % version
        parser = argparse.ArgumentParser(description=description)

        parser.add_argument('--redis-host', default='127.0.0.1')
        parser.add_argument('--redis-port', type=int, default=3218)

        parser.add_argument('-v', '--verbose', action='count', default=0)

        options = parser.parse_args(self.arguments)

        if options.verbose == 0:
            self.log_level = 'warning'
        elif options.verbose == 1:
            self.log_level = 'info'
        else:
            self.log_level = 'debug'

        logging.basicConfig(level=getattr(logging, self.log_level.upper()))

        logging.debug('Connecting at redis %s:%d...' % (options.redis_host, options.redis_port))
        redisco.connection_setup(host=options.redis_host, port=options.redis_port, db=10)

    def start(self):
        msg = 'skink-worker started'
        logging.info(msg)

        build_item = {
            'box_type': 'python',
            'repo': 'https://github.com/globocom/tapioca.git',
            'install': [
                'sudo pip install -r requirements.txt --use-mirrors'
            ],
            'script': [
                'make test'
            ]
        }

        vm = None
        try:
            vm = VM.create()
            vm.start()
            PythonBoxType().provision(vm.run_command)
            vm.snapshot()

            while True:
                logging.info('Building...')

                vm.run_command('git clone {0} ~/skink-build'.format(build_item['repo']))

                for command in build_item['install']:
                    result = vm.run_command(command, cwd="~/skink-build")
                    if result['status'] != 0:
                        logging.info("================ BUILD FAILED ==================")

                for command in build_item['script']:
                    result = vm.run_command(command, cwd="~/skink-build")
                    if result['status'] != 0:
                        logging.info("================ BUILD FAILED ==================")
                    else:
                        logging.info("================ BUILD SUCCESSFUL ==================")

                vm.revert()
                time.sleep(1)
        except Exception, err:
            import ipdb;ipdb.set_trace()
            if vm is not None:
                vm.destroy()
            raise err


def main():
    Worker(args=sys.argv[1:]).start()

if __name__ == '__main__':
    main()
