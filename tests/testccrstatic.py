import inspect
import unittest
from unittest.mock import *
import requests
from ccr.ccr import *

MAINTAINER = "Guillaume"
KNOWN_VALUES = {
    "cdrtools": {
        "test_geturl": "packages.php?ID=2745",
        "test_getpkgurl": "packages/cd/cdrtools/cdrtools.tar.gz",
        "test_getpkgbuild": "pkgbuild_view.php?p=cdrtools",
        "test_getpkgbuildraw": "packages/cd/cdrtools/cdrtools/PKGBUILD",
        "test_getfileraw": "packages/cd/cdrtools/cdrtools/test.raw",
    },
    "ls++-git": {
        "test_geturl": "packages.php?ID=3870",
        "test_getpkgurl": "packages/ls/ls++-git/ls++-git.tar.gz",
        "test_getpkgbuild": "pkgbuild_view.php?p=ls++-git",
        "test_getpkgbuildraw": "packages/ls/ls++-git/ls++-git/PKGBUILD",
        "test_getfileraw": "packages/ls/ls++-git/ls++-git/test.raw",
    },
}
MOCK_CCRRPC_VALID_VALUES = {
    "test_search": '{"type":"mock","results":{"ID":"mock"}}',
    "test_info": '{"type":"mock","results":{"ID":"","Name":"%s"}}',
    "test_msearch": '{"type":"mock","results":{"ID":"mock"}}',
    "test_geturl": '{"type":"mock","results":{"ID":"%s"}}',
}
MOCK_CCRRPC_INVALID_VALUES = '{"type":"mock"}'


class TestCCRStatic(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        requests.get = Mock()
    
    def test_search(self):
        #should pass when a result is returned
        for packagename in KNOWN_VALUES:
            requests.get.return_value.text = MOCK_CCRRPC_VALID_VALUES[inspect.stack()[0][3]]
            self.assertGreaterEqual(len(search(packagename)), 1)
        #should raise ValueError if data returned from server are malformed
        for packagename in KNOWN_VALUES:
            requests.get.return_value.text = MOCK_CCRRPC_INVALID_VALUES
            self.assertRaises(ValueError, search, packagename)

    def test_info(self):
        #should pass when a result is returned
        for packagename in KNOWN_VALUES:
            requests.get.return_value.text = MOCK_CCRRPC_VALID_VALUES[inspect.stack()[0][3]].replace("%s", packagename)
            self.assertEqual(info(packagename).Name, packagename)
        #should raise PackageNotFound when no result is returned
        for packagename in KNOWN_VALUES:
            requests.get.return_value.text = MOCK_CCRRPC_INVALID_VALUES
            self.assertRaises(PackageNotFound, info, packagename)

    def test_msearch(self):
        requests.get.return_value.text = MOCK_CCRRPC_VALID_VALUES[inspect.stack()[0][3]]
        self.assertGreaterEqual(len(msearch(MAINTAINER)), 1)
        requests.get.return_value.text = MOCK_CCRRPC_INVALID_VALUES
        self.assertRaises(ValueError, msearch, MAINTAINER)

    def test_geturl(self):
        for packagename in KNOWN_VALUES:
            requests.get.return_value.text = MOCK_CCRRPC_VALID_VALUES[inspect.stack()[0][3]].replace("%s", KNOWN_VALUES[packagename][inspect.stack()[0][3]][-4:])
            self.assertEqual(geturl(packagename), CCR_BASE + KNOWN_VALUES[packagename][inspect.stack()[0][3]])
        for packagename in KNOWN_VALUES:
            requests.get.return_value.text = MOCK_CCRRPC_INVALID_VALUES
            self.assertRaises(ValueError, geturl, packagename)

    def test_getpkgurl(self):
        for packagename in KNOWN_VALUES:
            self.assertEqual(getpkgurl(packagename), CCR_BASE + KNOWN_VALUES[packagename][inspect.stack()[0][3]])

    def test_getpkgbuild(self):
        for packagename in KNOWN_VALUES:
            self.assertEqual(getpkgbuild(packagename), CCR_BASE + KNOWN_VALUES[packagename][inspect.stack()[0][3]])

    def test_getpkgbuildraw(self):
        for packagename in KNOWN_VALUES:
            self.assertEqual(getpkgbuildraw(packagename), CCR_BASE + KNOWN_VALUES[packagename][inspect.stack()[0][3]])

    def test_getfileraw(self):
        for packagename in KNOWN_VALUES:
            self.assertEqual(getfileraw(packagename, "test.raw"), CCR_BASE + KNOWN_VALUES[packagename][inspect.stack()[0][3]])