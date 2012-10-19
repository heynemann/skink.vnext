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

import os.path
import tempfile
from shutil import rmtree

from sh import vagrant

from skink.models.config import Config


class VagrantManager:
    vagrant_box_id = 'precise64'
    vagrant_box_url = 'http://files.vagrantup.com/precise64.box'
    vagrant_root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'vagrant'))

    def __init__(self, ip):
        self.clean_output()
        self.ip = ip
        self.vagrant_file_dir = tempfile.mkdtemp()
        self.vagrant_file_path = None
        self.write_vagrant_file()

    def log(self, message, message_type="text"):
        self.output.append({
            'type': message_type,
            'message': message
        })
        print "[%s] %s" % (message_type, message)

    def cmd(self, message):
        self.log(message, message_type='cmd')

    def out(self, message):
        self.log(message, message_type='out')

    def br(self):
        self.log('', message_type='br')

    def clean_output(self):
        self.output = []

    def cleanup(self):
        self.destroy()
        if os.path.exists(self.vagrant_file_dir):
            rmtree(self.vagrant_file_dir)

    @property
    def vagrant_template(self):
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'vagrantfile_template.txt')), 'r') as t:
            return t.read()

    def write_vagrant_file(self):
        self.vagrant_file_path = os.path.join(self.vagrant_file_dir, 'VagrantFile')
        self.cmd('Vagrant file written at %s' % self.vagrant_file_path)
        self.cmd('    Arguments:')
        self.cmd('    * box_id: %s' % self.vagrant_box_id)
        self.cmd('    * box_url: %s' % self.vagrant_box_url)
        self.cmd('    * box_ip: %s' % self.ip)

        with open(self.vagrant_file_path, 'w') as f:
            f.write(self.vagrant_template % {
                'box_id': self.vagrant_box_id,
                'box_url': self.vagrant_box_url,
                'box_ip': self.ip
            })

    @property
    def vagrant(self):
        return vagrant.bake(_cwd=self.vagrant_file_dir, _tty_in=True, _tty_out=True, _err_to_out=True, _iter=True)

    def create(self):
        self.destroy()
        self.cmd('vagrant up')
        for line in self.vagrant.up():
            self.out(line)

    def suspend(self):
        self.cmd('vagrant suspend')
        for line in self.vagrant.suspend():
            self.out(line)

    def resume(self):
        self.cmd('vagrant resume')
        for line in self.vagrant.resume():
            self.out(line)

    def destroy(self):
        self.cmd('vagrant destroy --force')
        for line in self.vagrant.destroy(force=True):
            self.out(line)

    @property
    def config(self):
        return Config.create_from_file(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../.skink.yml')))

    def run_command_in_vm(self, command, cwd=True):
        if cwd:
            command = 'cd ~/skink-build && %s' % command

        self.cmd(command)
        for line in self.vagrant.ssh(command=command):
            self.out(line)

    def clone_repository(self):
        self.cmd('Cloning repository...')
        self.run_command_in_vm('sudo aptitude install -y git-core', cwd=False)
        self.run_command_in_vm('git clone https://github.com/heynemann/skink.vnext.git ~/skink-build', cwd=False)

    def provision(self):
        self.br()
        self.cmd('Provisioning...')

        self.clone_repository()

        for command in self.config.install:
            self.run_command_in_vm(command)

    def build(self):
        self.br()
        self.cmd('Building...')

        for command in self.config.script:
            self.run_command_in_vm(command)

    def bootstrap(self):
        self.ensure_vagrant_vm_available()

    def ensure_vagrant_vm_available(self):
        self.cmd('vagrant box list')
        boxes = self.vagrant.box.list()
        self.out('\n\t'.join(boxes))

        self.cmd('Retrieving %s box from %s' % (self.vagrant_box_id, self.vagrant_box_url))

        if self.vagrant_box_id in boxes:
            self.out('%s box already downloaded.' % self.vagrant_box_id)
        else:
            self.cmd('vagrant box ad %s %s' % (self.vagrant_box_id, self.vagrant_box_url))
            for line in self.vagrant.box.add(self.vagrant_box_id, self.vagrant_box_url, _iter=True):
                self.out(line)

if __name__ == '__main__':
    vm = VagrantManager(ip='33.66.33.01')
    try:
        vm.bootstrap()
        vm.create()
        #vm.suspend()
        #vm.resume()
        vm.provision()
        vm.build()
    finally:
        vm.cleanup()

