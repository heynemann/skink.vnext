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


class VagrantManager:
    vagrant_box_id = 'precise64'
    vagrant_box_url = 'http://files.vagrantup.com/precise64.box'
    vagrant_root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'vagrant'))

    def __init__(self, ip):
        self.ip = ip
        self.vagrant_file_dir = tempfile.mkdtemp()
        self.vagrant_file_path = None
        self.write_vagrant_file()

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
        for line in self.vagrant.up():
            print line

    def destroy(self):
        for line in self.vagrant.destroy(force=True):
            print line

    def bootstrap(self):
        self.ensure_vagrant_vm_available()

    def ensure_vagrant_vm_available(self):
        boxes = self.vagrant.box.list()

        print 'Provisioning VagrantVM Manager'
        print
        print 'Retrieving %s box from %s' % (self.vagrant_box_id, self.vagrant_box_url)

        if self.vagrant_box_id in boxes:
            print '%s box already downloaded.' % self.vagrant_box_id
        else:
            for line in self.vagrant.box.add(self.vagrant_box_id, self.vagrant_box_url, _iter=True):
                print line

if __name__ == '__main__':
    vm = VagrantManager(ip='33.66.33.01')
    vm.bootstrap()
    vm.create()
    vm.cleanup()

