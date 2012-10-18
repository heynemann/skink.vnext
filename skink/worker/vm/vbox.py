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

from skink.worker.vm import base

from sh import VBoxManage


class UbuntuVmManager(base.VmManager):
    snapshot_url = ''
    snapshot_path = 'snapshots/ubuntu.snapshot'

    def create(self, name):
        VBoxManage("createvm", "--name", name, register=True)

    def destroy(self, name):
        VBoxManage("unregistervm", name, delete=True)

    def list(self):
        return VBoxManage("list", "vms")

    def bootstrap(self):
        super(UbuntuVmManager, self).bootstrap()
        self.ensure_snapshot_available()

    def ensure_snapshot_available(self):
        if not self.download_exists(self.snapshot_path):
            self.download(self.snapshot_url, self.snapshot_path)

if __name__ == '__main__':
    vm = UbuntuVmManager()
    vm.bootstrap()

