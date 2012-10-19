# -*- coding: utf-8 -*-
import unittest
from mock import patch
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
                patch('skink.models.Project.objects.all')
            ) as (self.mock_redisco, self.mock_project):

            self.mock_project.return_value = [self.project]
            self.monitor = ProjectsMonitor()
            self.monitor.start()

    def test_redisco_connection_setup_has_been_called(self):
        self.mock_redisco.assert_called_once_with(host=self.monitor.redis_host,\
                                                  port=self.monitor.redis_port, \
                                                  db=10)

    def test_get_all_projects(self):
        assert self.monitor.projects == [self.project]

    @patch('time.sleep')
    def test_call_wait(self, sleep_mock):
      self.monitor.run()
      sleep_mock.assert_called_once_with(self.monitor.scan_time)
