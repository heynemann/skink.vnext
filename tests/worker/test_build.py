try:
        import unittest2 as unittest
except ImportError, e:
        import unittest

from skink.worker import Build
from skink.worker.box_types import PythonBoxType

import mock


class BuildTestCase(unittest.TestCase):
    def setUp(self):
        self.box_type_name = "python"
        self.install = "pip install nose"
        self.script = "nosetests"

        with mock.patch("uuid.uuid4") as uuid4:
            uuid4.return_value = mock.Mock(hex="uuid")
            self.build = Build(
                self.box_type_name,
                self.install,
                self.script
            )

    def test_build(self):
        self.assertEqual(self.install, self.build.install)
        self.assertEqual(self.script, self.build.script)

    def test_box_type(self):
        box_type = self.build.box_type

        self.assertIsInstance(box_type, PythonBoxType)
        self.assertEqual(self.box_type_name, box_type.name)

    def test_uuid(self):
        self.assertEqual("uuid", self.build.uuid)

