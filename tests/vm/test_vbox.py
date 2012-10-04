import unittest
import subprocess

from skink.vm.vbox import VmManager


class VmManagerTestCase(unittest.TestCase):

    def test_vm_manager_start_and_stop(self):
        self.manager = VmManager()
        self.manager.start("myvm")
        vms = subprocess.check_output(["VBoxManage", "list", "vms"])
        self.assertIn("myvm", vms)
        self.manager.stop("myvm")
        vms = subprocess.check_output(["VBoxManage", "list", "vms"])
        self.assertNotIn("myvm", vms)
