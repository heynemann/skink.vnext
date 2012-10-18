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

import requests

from skink.worker import BoxType

class UbuntuBoxType(BoxType):
    def bootstrap(self):
        super(UbuntuBoxType, self).bootstrap()
        self.ensure_ubuntu_image()

    def ensure_ubuntu_image(self):
        filename = 'os/ubuntu-12.10-server-amd64.iso'
        if not self.download_exists(filename):
            self.download('http://www.ubuntu.com/start-download?distro=server&bits=64&release=latest', filename)

class PythonBoxType(UbuntuBoxType):
    def __init__(self):
        install = "sudo apt-get install python python-pip -y"
        name = "python"
        super(PythonBoxType, self).__init__(name, install)

    def bootstrap(self):
        super(PythonBoxType, self).bootstrap()

