import unittest
from unittest.mock import Mock
import requests
from ccr.session import *


class TestSession(unittest.TestCase):

    def setUp(self):
        self.session = Session.__new__(Session)

    def test_init(self):
        self.session._session.post = Mock()
        self.session._session.cookies = "AURSID"
        self.assertRaises(ValueError, self.session.__init__("an0n", "ym0us"))

    def test_checkvote(self):
        requests.get = Mock()
        requests.get.return_value.text = '{"type":"mocked_type","results":{"ID":"mocked_ID"}}'
        self.session._session.get = Mock()
        self.session._session.get.return_value.text = "class='button' name='do_UnVote'"
        self.assertTrue(self.session.check_vote("cdrtools"))