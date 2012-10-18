# -*- coding: utf-8 -*-
import unittest

from skink.models import Project

class ProjectTestCase(unittest.TestCase):

    def setUp(self):
        self.project = Project(git_repo = 'git@git://github.com/heynemman/skink.next')

    def test_has_clone_method(self):
        assert self.project.clone

    def test_has_fetch_method(self):
        assert self.project.fetch

    def test_has_check_update_method(self):
        assert self.project.check_update

