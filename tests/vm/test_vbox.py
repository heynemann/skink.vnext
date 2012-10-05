import unittest
import subprocess

from skink.vm.vbox import VmManager


class VmManagerTestCase(unittest.TestCase):

    def test_vm_manager_create_and_destroy(self):
        self.manager = VmManager()
        self.manager.create("myvm")
        vms = subprocess.check_output(["VBoxManage", "list", "vms"])
        self.assertIn("myvm", vms)
        self.manager.destroy("myvm")
        vms = subprocess.check_output(["VBoxManage", "list", "vms"])
        self.assertNotIn("myvm", vms)
