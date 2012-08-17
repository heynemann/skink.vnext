import unittest

from skink.vm.base import VmManager


class VmManagerTestCase(unittest.TestCase):

    def test_vm_manager_start(self):
        manager = VmManager()
        manager.start()
