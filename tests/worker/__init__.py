import unittest

from skink.worker import Build


class BuildTestCase(unittest.TestCase):
    def test_build(self):
        box_type = "python"
        install = "pip install nose"
        script = "nosetests"
        Build(box_type, install, script)
