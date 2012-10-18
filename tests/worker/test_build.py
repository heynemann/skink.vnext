try:
        import unittest2 as unittest
except ImportError, e:
        import unittest

from skink.worker import Build, BoxType


class BuildTestCase(unittest.TestCase):
    def test_build(self):
        box_type = "python"
        install = "pip install nose"
        script = "nosetests"

        build = Build(box_type, install, script)

        self.assertEqual(install, build.install)
        self.assertEqual(script, build.script)

    def test_box_type(self):
        box_type_name = "python"
        install = "pip install nose"
        script = "nosetests"

        build = Build(box_type_name, install, script)
        box_type = build.box_type

        self.assertIsInstance(box_type, BoxType)
        self.assertEqual(box_type_name, box_type.name)
