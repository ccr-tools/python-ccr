import inspect
import unittest
from unittest.mock import *
import requests
from ccr.ccr import *


class TestCCRStatic(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.maintainer = "Guillaume"
        cls.known_values = {
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
        cls.mock_valid_return_values = '{"type":"mock","results":{"ID":"%s","Name":"%s"}}'
        cls.mock_invalid_return_values = ['{"type":"mock"}', '{"type":"mock","results":"No result found"}']
        requests.get = Mock()

    def test_search(self):
        #should pass when a result is returned
        for packagename in self.known_values:
            requests.get.return_value.text = self.mock_valid_return_values
            self.assertGreaterEqual(len(search(packagename)), 1)
        #should raises ValueError if data returned from server are invalid
        for packagename in self.known_values:
            requests.get.return_value.text = self.mock_invalid_return_values[0]
            self.assertRaises(ValueError, search, packagename)

    def test_info(self):
        #should pass when a result is returned
        for packagename in self.known_values:
            requests.get.return_value.text = self.mock_valid_return_values.replace("%s", packagename)
            self.assertEqual(info(packagename).Name, packagename)
        #should raises PackageNotFound if the package couln't be found
        for packagename in self.known_values:
            requests.get.return_value.text = self.mock_invalid_return_values[1]
            self.assertRaises(PackageNotFound, info, packagename)
        #should raises PackageNotFound if data returned from server are invalid
        for packagename in self.known_values:
            requests.get.return_value.text = self.mock_invalid_return_values[0]
            self.assertRaises(PackageNotFound, info, packagename)

    def test_msearch(self):
        #should pass when a result is returned
        requests.get.return_value.text = self.mock_valid_return_values
        self.assertGreaterEqual(len(msearch(self.maintainer)), 1)
        #should raises ValueError if data returned from server are invalid
        requests.get.return_value.text = self.mock_invalid_return_values[0]
        self.assertRaises(ValueError, msearch, self.maintainer)

    def test_geturl(self):
        #should pass when a result is returned
        for packagename in self.known_values:
            requests.get.return_value.text = self.mock_valid_return_values.replace("%s", self.known_values[packagename][inspect.stack()[0][3]][-4:])
            self.assertEqual(geturl(packagename), CCR_BASE + self.known_values[packagename][inspect.stack()[0][3]])
        #should raises ValueError if data returned from server are invalid
        for packagename in self.known_values:
            requests.get.return_value.text = self.mock_invalid_return_values[0]
            self.assertRaises(ValueError, geturl, packagename)

    #should returns a valid url
    def test_getpkgurl(self):
        for packagename in self.known_values:
            self.assertEqual(getpkgurl(packagename), CCR_BASE + self.known_values[packagename][inspect.stack()[0][3]])

    #should returns a valid url
    def test_getpkgbuild(self):
        for packagename in self.known_values:
            self.assertEqual(getpkgbuild(packagename), CCR_BASE + self.known_values[packagename][inspect.stack()[0][3]])

    #should returns a valid url
    def test_getpkgbuildraw(self):
        for packagename in self.known_values:
            self.assertEqual(getpkgbuildraw(packagename), CCR_BASE + self.known_values[packagename][inspect.stack()[0][3]])

    #should returns a valid url
    def test_getfileraw(self):
        for packagename in self.known_values:
            self.assertEqual(getfileraw(packagename, "test.raw"), CCR_BASE + self.known_values[packagename][inspect.stack()[0][3]])