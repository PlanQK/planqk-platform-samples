import os
import unittest

from ..program import run

os.environ["DEBUG"] = "true"


class BasicTestSuite(unittest.TestCase):

    def test_should_run_template(self):
        run({"values": [10, 5, 20, 7]}, {})


if __name__ == '__main__':
    unittest.main()
