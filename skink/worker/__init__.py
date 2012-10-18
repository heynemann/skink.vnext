# -*- coding: utf-8 -*-

# Copyright (c) 2012 Bernardo Heynemann

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is furnished
# to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import os.path
from tempfile import NamedTemporaryFile
import uuid

import requests


class Build(object):
    def __init__(self, box_type_name, install, script):
        self.uuid = uuid.uuid4().hex
        self.box_type = self.get_box_type_by_name(box_type_name)
        self.install = install
        self.script = script

    def get_box_type_by_name(self, name):
        from skink.worker import box_types
        box_type_name = "{0}BoxType".format(name.title())
        return getattr(box_types, box_type_name)()

    def create_vm(self):
        from skink.worker.vm.vbox import VmManager
        VmManager().create(self.uuid)


class BoxType(object):
    def __init__(self, name, install):
        self.name = name
        self.install = install

    @property
    def skink_files(self):
        if not hasattr(self,  '_skink_files'):
            self._skink_files = os.path.join(os.path.expanduser('~'), '.skinkfiles')
        return self._skink_files

    def ensure_download_dir(self):
        if not os.path.exists(self.skink_files):
            os.makedirs(self.skink_files)

    def download_exists(filename):
        return os.path.exists(os.path.join(self.skink_files.rstrip('/'), filename.lstrip('/')))

    def download(self, url, filename):
        f = NamedTemporaryFile(mode='wb')
        r = requests.get(url)
        f.write(r.content)

        os.rename(f.name, os.path.join(self.skink_files.rstrip('/'), filename.lstrip('/')))

    def bootstrap(self):
        self.ensure_download_dir()

