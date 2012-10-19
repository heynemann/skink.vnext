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
import sh
import os

from redisco import models


class Project(models.Model):
    name = models.Attribute(required=True)
    git_repo = models.Attribute(required=True)
    created_by = models.Attribute(required=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_build_number = models.IntegerField(default=0)

    def clone(self):
        command = '%s %s %s' % ('clone', self.git_repo, self.name)
        sh.git(command)

    def fetch(self):
        sh.git("fetch --all", _cwd=self.dir_repo)

    def has_git_repo(self):
        path = os.path.join(self.dir_repo, ".git")
        return os.path.exists(path)

    def has_dir(self):
        return os.path.exists(self.dir_repo)

    def _create_git_repo(self):
        self.clone()

    def check_update(self):
        if not self.has_dir() or not self.has_git_repo():
            self._create_git_repo()
            return True

        return False

    @property
    def dir_repo(self):
        if not hasattr(self, '_dir_repo'):
            self._dir_repo = "/tmp/builds/%s" % self.name

        return self._dir_repo

    @property
    def next_build(self):
        return self.last_build_number + 1

#class Build(models.Model):
    #project = models.ReferenceField(Project, required=True)
    #number = models.IntegerField(required=True)
    #log = models.Attribute()


