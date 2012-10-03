import unittest

from skink.vm.base import VmManager


class VmManagerTestCase(unittest.TestCase):

    def setUp(self):
        self.manager = VmManager()

    def test_vm_manager_start(self):
        self.manager.start()

    def test_vm_managet_stop(self):
        self.manager.stop()
