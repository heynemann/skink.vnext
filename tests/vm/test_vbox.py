import unittest

from skink.vm.vbox import VmManager

from sh import VBoxManage


class VmManagerTestCase(unittest.TestCase):

    def test_vm_manager_create_and_destroy(self):
        self.manager = VmManager()
        self.manager.create("myvm")
        vms = VBoxManage("list", "vms")
        self.assertIn("myvm", vms)
        self.manager.destroy("myvm")
        vms = VBoxManage("list", "vms")
        self.assertNotIn("myvm", vms)
