import unittest
from unittest.mock import Mock
import requests
from ccr.session import *
from ccr.session import _VoteWarning, _FlagWarning, _DeleteWarning, _NotifyWarning, _OwnershipWarning, _SubmitWarning, _CategoryWarning


class TestSession(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        requests.get = Mock()
        cls.username = "an0n"
        cls.password = "ym0us"
        cls.package = "pyccr-testing"

    def setUp(self):
        self.session = Session()
        self.session._session.get = Mock()
        self.session._session.post = Mock()

    def test_authenticate(self):
        # should pass if a cookie is created after a successful login
        self.session._session.cookies = "AURSID"
        self.session.authenticate(self.username, self.password)
        # should raises ValueError if the login failed and if no cookie is created
        self.session._session.cookies = "None"
        self.assertRaises(ValueError, self.session.authenticate, self.username, self.password)

    def test_checkvote(self):
        # should pass if True or False is returned
        requests.get.return_value.text = '{"type":"mock","results":{"ID":"mock"}}'
        self.session._session.get.return_value.text = "class='button' name='do_UnVote'"
        if self.session.check_vote(self.package) is not True or False:
            self.fail()
        # should raises PackageNotFound if the package doesn't exists
        requests.get.return_value.text = '{"type":"mock"}'
        self.assertRaises(PackageNotFound, self.session.check_vote, self.package)

    def test_vote(self):
        # should pass if package is not already voted and vote confirmed
        self.session.check_vote = Mock(side_effect=[(False, 0), True])
        self.session.vote(self.package)
        # should failed if package is already voted
        self.session.check_vote = Mock(return_value=(True, 0))
        self.assertRaises(_VoteWarning, self.session.vote, self.package)

    def tearDown(self):
        self.session.close()