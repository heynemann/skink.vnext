# -*- coding: utf-8 -*-
import unittest

from skink.monitor import ProjectsMonitor

class MonitorTestCase(unittest.TestCase):

    def test_instance_monitor(self):
        monitor = ProjectsMonitor()
        assert isinstance (monitor, ProjectsMonitor)

    def test_has_defaults(self):
        monitor = ProjectsMonitor()
        assert monitor.redis_port == 3218
        assert monitor.redis_host =='127.0.0.1'
        assert monitor.log_level == 'warning'

    def test_verbose_level_1(self):
        monitor = ProjectsMonitor(['-v'])
        assert monitor.log_level == 'info'

    def test_verbose_level_2(self):
        monitor = ProjectsMonitor(['-vv'])
        assert monitor.log_level == 'debug'

    def test_has_start_method(self):
        monitor = ProjectsMonitor()
        assert  monitor.start

class MonitorStartTestCase(unittest.TestCase):

    def setUp(self):
        self.monitor = ProjectsMonitor()
