# -*- coding: utf-8 -*-
import unittest

from mock import patch

from skink.models import Project

class ProjectTestCase(unittest.TestCase):

    def setUp(self):
        self.project = Project(name=u"skink.next", git_repo = 'git@git://github.com/heynemman/skink.next')

    def test_has_clone_method(self):
        assert self.project.clone

    def test_has_fetch_method(self):
        assert self.project.fetch

    def test_has_check_update_method(self):
        assert self.project.check_update

    def test_has_dir_repo(self):
        assert self.project.dir_repo == '/builds/%s' % self.project.name

    @patch('sh.git')
    def test_call_git_clone(self, mock_git_clone):
        self.project.clone()
        expected_params = '%s %s' %('clone', self.project.git_repo)
        mock_git_clone.assert_called_once_with(expected_params)

