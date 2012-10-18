import unittest

from skink.worker import BoxType


class BoxTypeBaseTestCase(unittest.TestCase):
    def test_base(self):
        name = "python"
        install = "sudo apt-get install python python-pip -y"
        box_type = BoxType(name, install)
        self.assertEqual(name, box_type.name)
        self.assertEqual(install, box_type.install)
