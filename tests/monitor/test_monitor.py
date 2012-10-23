# -*- coding: utf-8 -*-
import unittest
from mock import patch, Mock
from contextlib import nested

from skink.monitor import ProjectsMonitor
from skink.models import Project

class MonitorTestCase(unittest.TestCase):

    def test_instance_monitor(self):
        monitor = ProjectsMonitor()
        assert isinstance (monitor, ProjectsMonitor)

    def test_has_defaults(self):
        monitor = ProjectsMonitor()
        assert monitor.redis_port == 3218
        assert monitor.redis_host =='127.0.0.1'
        assert monitor.log_level == 'warning'
        assert monitor.scan_time == 30
        assert monitor.debug  == False

    def test_verbose_level_1(self):
        monitor = ProjectsMonitor(['-v'])
        assert monitor.log_level == 'info'

    def test_verbose_level_2(self):
        monitor = ProjectsMonitor(['-vv'])
        assert monitor.log_level == 'debug'

    def test_has_start_method(self):
        monitor = ProjectsMonitor()
        assert  monitor.start

    def test_has_run_method(self):
        monitor = ProjectsMonitor()
        assert monitor.run

class MonitorStartTestCase(unittest.TestCase):

    def setUp(self):
        self.project = Project()

        with nested(
                patch('redisco.connection_setup'),
                patch('skink.models.Project.objects.all'),
                patch('time.sleep')
            ) as (self.mock_redisco, self.mock_project, self.mock_sleep):

            self.mock_project.return_value = [self.project]
            self.monitor = ProjectsMonitor()
            self.monitor.debug = True
            self.monitor.run = Mock()
            self.monitor.start()

    def test_redisco_connection_setup_has_been_called(self):
        self.mock_redisco.assert_called_once_with(host=self.monitor.redis_host,\
                                                  port=self.monitor.redis_port, \
                                                  db=10)

    def test_get_all_projects(self):
        assert self.monitor.projects == [self.project]

    def test_call_wait(self):
        self.mock_sleep.assert_called_once_with(self.monitor.scan_time)

    def test_call_run(self):
        self.monitor.run.assert_called_once_with()

class MonitorRunTestCase(unittest.TestCase):

    def setUp(self):
        self.project = Project()
        self.project.check_update = Mock(return_value=False)
        self.project.pull = Mock()
        self.monitor = ProjectsMonitor()
        self.monitor.projects = [self.project]
        self.monitor.debug = True

    def test_call_project_check_updates(self):
        self.monitor.run()
        self.project.check_update.assert_called_once_with()

    def test_call_create_build(self):
        self.project.check_update = Mock(return_value=True)
        self.monitor.create_build = Mock()
        self.monitor.run()
        self.monitor.create_build.assert_called_once_with(self.project)

    def test_dont_call_create_build(self):
        self.monitor.create_build = Mock()
        self.monitor.run()
        assert not self.monitor.create_build.called
