try:
        import unittest2 as unittest
except ImportError, e:
        import unittest

from skink.vm.vbox import VmManager

import sh


@unittest.skipIf(not hasattr(sh, "VBoxManage"), "requires VBoxManage")
class VmManagerTestCase(unittest.TestCase):

    def test_vm_manager_create_and_destroy(self):
        self.manager = VmManager()
        self.manager.create("myvm")
        vms = sh.VBoxManage("list", "vms")
        self.assertIn("myvm", vms)
        self.manager.destroy("myvm")
        vms = sh.VBoxManage("list", "vms")
        self.assertNotIn("myvm", vms)
