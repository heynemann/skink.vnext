import unittest

from skink.vm.base import VmManager


class VmManagerTestCase(unittest.TestCase):

    def setUp(self):
        self.manager = VmManager()

    def test_vm_manager_create(self):
        self.assertRaises(NotImplementedError, self.manager.create)

    def test_vm_managet_destroy(self):
        self.assertRaises(NotImplementedError, self.manager.destroy)
