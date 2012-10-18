import unittest

from skink.worker import BoxType
from skink.worker.box_types import PythonBoxType



class PythonBoxTypeTestCase(unittest.TestCase):
    def test_is_a_box_type(self):
        self.assertTrue(issubclass(PythonBoxType, BoxType))

    def test_name(self):
        self.assertEqual("python", PythonBoxType().name)

    def test_install(self):
        install = "sudo apt-get install python python-pip -y"
        self.assertEqual(install, PythonBoxType().install)
