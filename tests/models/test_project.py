# -*- coding: utf-8 -*-
import unittest
import os

from mock import patch, Mock

from skink.models import Project


class ProjectTestCase(unittest.TestCase):

    def setUp(self):
        url_git_repo = 'git@git://github.com/heynemman/skink.next'
        self.project = Project(name=u"skink.next",
                               git_repo=url_git_repo)

    def test_has_clone_method(self):
        assert self.project.clone

    def test_has_fetch_method(self):
        assert self.project.fetch

    def test_has_check_update_method(self):
        assert self.project.check_update

    def test_has_dir_repo(self):
        expected = '/tmp/builds/%s' % self.project.name
        assert self.project.dir_repo == expected

    @patch('sh.git')
    def test_call_git_clone(self, mock_git_clone):
        self.project.clone()
        expected_params = '%s %s %s' % ('clone',
                                     self.project.git_repo,
                                     self.project.name )
        mock_git_clone.assert_called_once_with(expected_params)

    @patch('sh.git')
    def test_call_git_fetch(self, mock_git_fetch):
        self.project.fetch()
        mock_git_fetch.assert_called_once_with("fetch --all")

    @patch('os.path.exists')
    def test_has_git_repo_return_false(self, mock):
        mock.return_value = False
        assert not self.project.has_git_repo(), "should be false"
        path = os.path.join(self.project.dir_repo, ".git")
        mock.assert_called_once_with(path)

    @patch('os.path.exists')
    def test_has_git_repo_return_true(self, mock):
        mock.return_value = True
        assert self.project.has_git_repo()

    @patch('os.path.exists')
    def test_has_dir_return_false(self, mock):
        mock.return_value = False
        assert not self.project.has_dir(), "should return false"
        mock.assert_called_once_with(self.project.dir_repo)

    @patch('os.path.exists')
    def test_has_dir_return_true(self, mock):
        mock.return_value = True
        assert self.project.has_dir(), "should return true"

    def test_check_update_return_true_if_dir_not_exists(self):
        self.project._create_git_repo = Mock()
        self.project.has_dir = Mock(return_value = False)
        self.project.has_git_repo = Mock(return_value = True)
        assert self.project.check_update()

    def test_check_update_return_true_if_git_repo_not_exists(self):
        self.project._create_git_repo = Mock()
        self.project.has_dir = Mock(return_value = True)
        self.project.has_git_repo = Mock(return_value= False)
        assert self.project.check_update()

    def test_call_create_repo_if_not_have_dir(self):
        self.project.has_dir = Mock(return_value = False)
        self.project.has_git_repo = Mock(return_value = False)
        self.project._create_git_repo = Mock()
        self.project.check_update()
        self.project._create_git_repo.assert_called_once_with()
