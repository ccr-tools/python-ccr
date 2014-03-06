import unittest
from unittest.mock import Mock
from ccr.session import *


class TestSession(unittest.TestCase):

    def test_authenticate(self):
        self.session = Session()
        self.session._session.post = Mock()
        self.session._session.cookies = "AURSID"
        self.assertRaises(ValueError, self.session.authenticate("an0n", "ym0us"))


if __name__ == "__main__":
    unittest.main()