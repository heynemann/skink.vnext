import unittest

from skink.vm.base import VmManager


class VmManagerTestCase(unittest.TestCase):

    def setUp(self):
        self.manager = VmManager

    def test_vm_manager_create(self):
        self.assertTrue(self.manager.create.im_func.func_dict['__isabstractmethod__'])

    def test_vm_manager_destroy(self):
        self.assertTrue(self.manager.destroy.im_func.func_dict['__isabstractmethod__'])

    def test_vm_manager_list(self):
        self.assertTrue(self.manager.list.im_func.func_dict['__isabstractmethod__'])
