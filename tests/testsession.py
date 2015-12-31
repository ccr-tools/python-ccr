import unittest
from unittest.mock import Mock, PropertyMock, mock_open, patch
import requests
from ccr.session import *
from ccr.session import _VoteWarning, _FlagWarning, _DeleteWarning, _NotifyWarning, _OwnershipWarning, _SubmitWarning, _CategoryWarning


class TestSession(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.username = "an0n"
        cls.password = "ym0us"
        cls.package = "pyccr-testing"
        cls.category = "none"
        cls.mock_valid_return_values = '{"type":"mock","results":{"ID":"mock","Name":"mock", "OutOfDate":"%s", "MaintainerUID":"%s", "Maintainer":"%s"}}'
        cls.mock_invalid_return_values = '{"type":"mock"}'

    def setUp(self):
        self.session = Session()
        self.session._session.get = Mock()
        self.session._session.post = Mock()
        requests.get = Mock()

    def test_authenticate(self):
        # should pass if a cookie is created after a successful login
        self.session._session.cookies = "AURSID"
        self.session.authenticate(self.username, self.password)
        # should raises ValueError if the login failed and if no cookie is created
        self.session._session.cookies = "None"
        self.assertRaises(ValueError, self.session.authenticate, self.username, self.password)

    def test_checkvote(self):
        # should pass if the package exists and True or False is returned
        requests.get.return_value.text = self.mock_valid_return_values
        self.session._session.get.return_value.text = "class='button' name='do_UnVote'"
        if self.session.check_vote(self.package) is not True or False:
            self.fail()
        # should raises PackageNotFound if the package doesn't exists
        requests.get.return_value.text = self.mock_invalid_return_values
        self.assertRaises(PackageNotFound, self.session.check_vote, self.package)

    def test_vote(self):
        # should pass if the package is not already voted and the server confirmation succeed
        self.session.check_vote = Mock(side_effect=[(False, 0), True])
        self.session.vote(self.package)
        # should raises _VoteWarning if the package is already voted
        self.session.check_vote = Mock(return_value=(True, 0))
        self.assertRaises(_VoteWarning, self.session.vote, self.package)
        # should fails if the server confirmation fails
        self.session.check_vote = Mock(side_effect=[(False, 0), False])
        self.assertRaises(_VoteWarning, self.session.vote, self.package)

    def test_unvote(self):
        # should pass if the package is already voted and the server confirmation succeed
        self.session.check_vote = Mock(side_effect=[(True, 0), False])
        self.session.unvote(self.package)
        # should raises _VoteWarning if the package already or never voted
        self.session.check_vote = Mock(return_value=(False, 0))
        self.assertRaises(_VoteWarning, self.session.unvote, self.package)
        # should raises _VoteWarning if the server confirmation fails
        self.session.check_vote = Mock(side_effect=[(True, 0), True])
        self.assertRaises(_VoteWarning, self.session.unvote, self.package)

    def test_flag(self):
        # should pass if the package exists and the server confirmation succeed
        type(requests.get.return_value).text = PropertyMock(side_effect=[self.mock_valid_return_values,
                                                                         self.mock_valid_return_values.replace("%s", "1")])
        self.session.flag(self.package)
        # should raises PackageNotFound if the package doesn't exists
        type(requests.get.return_value).text = PropertyMock(side_effect=self.mock_invalid_return_values)
        self.assertRaises(PackageNotFound, self.session.flag, self.package)
        # should raises _FlagWarning if the server confirmation fails
        type(requests.get.return_value).text = PropertyMock(side_effect=[self.mock_valid_return_values,
                                                                         self.mock_valid_return_values.replace("%s", "0")])
        self.assertRaises(_FlagWarning, self.session.flag, self.package)

    def test_unflag(self):
        # should pass if the package exists and the server confirmation succeed
        type(requests.get.return_value).text = PropertyMock(side_effect=[self.mock_valid_return_values,
                                                                         self.mock_valid_return_values.replace("%s", "0")])
        self.session.unflag(self.package)
        # should raises PackageNotFound if the package doesn't exists
        type(requests.get.return_value).text = PropertyMock(side_effect=self.mock_invalid_return_values)
        self.assertRaises(PackageNotFound, self.session.unflag, self.package)
        # should raises _FlagWarning if the server confirmation fails
        type(requests.get.return_value).text = PropertyMock(side_effect=[self.mock_valid_return_values,
                                                                         self.mock_valid_return_values.replace("%s", "1")])
        self.assertRaises(_FlagWarning, self.session.unflag, self.package)

    def test_notify(self):
        # should pass if the package exists and the server confirmation succeed
        requests.get.return_value.text = self.mock_valid_return_values
        self.session._session.post.return_value.text = "<option value='do_UnNotify'"
        self.session.notify(self.package)
        # should raises PackageNotFound if the package doesn't exists
        requests.get.return_value.text = self.mock_invalid_return_values
        self.assertRaises(PackageNotFound, self.session.notify, self.package)
        # should raises _NotifyWarning if the server confirmation fails
        requests.get.return_value.text = self.mock_valid_return_values
        self.session._session.post.return_value.text = "mock"
        self.assertRaises(_NotifyWarning, self.session.notify, self.package)

    def test_unnotify(self):
        # should pass if the package exists and the server confirmation succeed
        requests.get.return_value.text = self.mock_valid_return_values
        self.session._session.post.return_value.text = "<option value='do_Notify'"
        self.session.unnotify(self.package)
        # should raises PackageNotFound if the package doesn't exists
        requests.get.return_value.text = self.mock_invalid_return_values
        self.assertRaises(PackageNotFound, self.session.unnotify, self.package)
        # should raises _NotifyWarning if the server confirmation fails
        requests.get.return_value.text = self.mock_valid_return_values
        self.session._session.post.return_value.text = "mock"
        self.assertRaises(_NotifyWarning, self.session.unnotify, self.package)

    def test_adopt(self):
        self.session._username = self.username
        # should pass if the package exists and the server confirmation succeed
        type(requests.get.return_value).text = PropertyMock(side_effect=[self.mock_valid_return_values.replace("%s", "0"),
                                                                         self.mock_valid_return_values.replace("%s", self.username)])
        self.session.adopt(self.package)
        # should raises PackageNotFound if the package doesn't exists
        type(requests.get.return_value).text = PropertyMock(side_effect=self.mock_invalid_return_values)
        self.assertRaises(PackageNotFound, self.session.adopt, self.package)
        # should raises _OwnershipWarning if the package is already maintained
        type(requests.get.return_value).text = PropertyMock(side_effect=[self.mock_valid_return_values.replace("%s", "1")])
        self.assertRaises(_OwnershipWarning, self.session.adopt, self.package)
        # should raises _OwnershipWarning if the package can't be adopted.
        type(requests.get.return_value).text = PropertyMock(side_effect=[self.mock_valid_return_values.replace("%s", "0"),
                                                                         self.mock_valid_return_values.replace("%s", "mock")])
        self.assertRaises(_OwnershipWarning, self.session.adopt, self.package)

    @patch('builtins.open', mock_open())
    def test_submit(self):
        # should pass if the file exists and the server accepts it
        self.session._session.post.return_value.text = "pkgbuild_view.php?p="
        self.session.submit("mock", self.category)
        # should fails if the package is invalid
        self.session._session.post.return_value.text = "<span class='error'>(?P<message>.*)</span>"
        self.assertRaises(InvalidPackage, self.session.submit, "mock", self.category)
        # should raises _SubmitWarning if the server confirmation fails
        self.session._session.post.return_value.text = "mock"
        self.assertRaises(_SubmitWarning, self.session.submit, "mock", self.category)

    def test_delete(self):
        # TODO Fix ccr.delete() method before writing the test
        pass

    def test_setcategory(self):
        # should pass if the category is valid and the server confirmation succeed
        requests.get.return_value.text = self.mock_valid_return_values
        self.session._session.post.return_value.text = "selected='selected'>" + self.category + "</option>"
        self.session.setcategory(self.package, self.category)
        # should raises PackageNotFound if the package doesn't exists
        requests.get.return_value.text = self.mock_invalid_return_values
        self.assertRaises(PackageNotFound, self.session.setcategory, self.package, self.category)
        # should raises _CategoryWarning if the category is invalid
        requests.get.return_value.text = self.mock_valid_return_values
        self.assertRaises(_CategoryWarning, self.session.setcategory, self.package, "mock")
        # should raises _CategoryWarning if the server confirmation fails
        requests.get.return_value.text = self.mock_valid_return_values
        self.session._session.post.return_value.text = "mock"
        self.assertRaises(_CategoryWarning, self.session.setcategory, self.package, self.category)

    def tearDown(self):
        self.session.close()
