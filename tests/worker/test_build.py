import unittest

from skink.worker import Build


class BuildTestCase(unittest.TestCase):
    def test_build(self):
        box_type = "python"
        install = "pip install nose"
        script = "nosetests"
        build = Build(box_type, install, script)
        self.assertEqual(box_type, build.box_type_name)
        self.assertEqual(install, build.install)
        self.assertEqual(script, build.script)
