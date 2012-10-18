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
import os
import os.path
import urllib
from uuid import uuid4

from abc import ABCMeta, abstractmethod

from skink.worker.box_types import PythonBoxType


class VmManager(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def bootstrap(self):
        pass

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def destroy(self):
        pass

    @abstractmethod
    def list(self):
        pass

    @property
    def skink_files(self):
        if not hasattr(self,  '_skink_files'):
            self._skink_files = os.path.join(os.path.expanduser('~'), '.skinkfiles')
        return self._skink_files

    def ensure_download_dir(self):
        if not os.path.exists(self.skink_files):
            os.makedirs(self.skink_files)

    def download_exists(self, filename):
        return os.path.exists(os.path.join(self.skink_files.rstrip('/'), filename.lstrip('/')))

    def _reporthook(self, numblocks, blocksize, filesize, url=None):
        base = os.path.basename(url)
        try:
            percent = min((float(numblocks) * float(blocksize) * 100) / float(filesize), 100)
        except:
            percent = 100
        if numblocks != 0:
            sys.stdout.write("\b" * 73)
        sys.stdout.write("%-66s%03.02f%%" % (base, percent))

    def download(self, url, filename):
        base = os.path.basename(url)

        print "Getting initial information for %s..." % base

        file_path = os.path.join(self.skink_files.rstrip('/'), filename.lstrip('/'))
        file_dir = os.path.dirname(file_path)
        temp_path = os.path.join(file_dir, str(uuid4()))

        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        if sys.stdout.isatty():
            urllib.urlretrieve(url, temp_path,
                               lambda nb, bs, fs, url=url: self._reporthook(nb,bs,fs,url))
            sys.stdout.write('\n')
        else:
            urllib.urlretrieve(url, downloaded_file.name)

        os.rename(temp_path, file_path)

    def bootstrap(self):
        self.ensure_download_dir()

