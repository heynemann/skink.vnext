import unittest

from skink.vm.base import VmManager


class VmManagerTestCase(unittest.TestCase):

    def setUp(self):
        self.manager = VmManager()

    def test_vm_manager_create(self):
        self.assertRaises(NotImplementedError, self.manager.create)

    def test_vm_manager_destroy(self):
        self.assertRaises(NotImplementedError, self.manager.destroy)

    def test_vm_manager_list(self):
        self.assertRaises(NotImplementedError, self.manager.list)
