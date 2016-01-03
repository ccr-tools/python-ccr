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
                "test_url": "packages.php?ID=2745",
                "test_pkgurl": "packages/cd/cdrtools/cdrtools.tar.gz",
                "test_pkgbuild": "pkgbuild_view.php?p=cdrtools",
                "test_pkgbuildraw": "packages/cd/cdrtools/cdrtools/PKGBUILD",
                "test_fileraw": "packages/cd/cdrtools/cdrtools/test.raw",
            },
            "ls++-git": {
                "test_url": "packages.php?ID=3870",
                "test_pkgurl": "packages/ls/ls++-git/ls++-git.tar.gz",
                "test_pkgbuild": "pkgbuild_view.php?p=ls++-git",
                "test_pkgbuildraw": "packages/ls/ls++-git/ls++-git/PKGBUILD",
                "test_fileraw": "packages/ls/ls++-git/ls++-git/test.raw",
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

    def test_url(self):
        #should pass when a result is returned
        for packagename in self.known_values:
            requests.get.return_value.text = self.mock_valid_return_values.replace("%s", self.known_values[packagename][inspect.stack()[0][3]][-4:])
            self.assertEqual(url(packagename), CCR_BASE + self.known_values[packagename][inspect.stack()[0][3]])
        #should raises ValueError if data returned from server are invalid
        for packagename in self.known_values:
            requests.get.return_value.text = self.mock_invalid_return_values[0]
            self.assertRaises(ValueError, url, packagename)

    #should returns a valid url
    def test_pkgurl(self):
        for packagename in self.known_values:
            self.assertEqual(pkg_url(packagename), CCR_BASE + self.known_values[packagename][inspect.stack()[0][3]])

    #should returns a valid url
    def test_pkgbuild(self):
        for packagename in self.known_values:
            self.assertEqual(pkgbuild_url(packagename), CCR_BASE + self.known_values[packagename][inspect.stack()[0][3]])

    #should returns a valid url
    def test_pkgbuildraw(self):
        for packagename in self.known_values:
            self.assertEqual(pkgbuild_raw_url(packagename), CCR_BASE + self.known_values[packagename][inspect.stack()[0][3]])

    #should returns a valid url
    def test_fileraw(self):
        for packagename in self.known_values:
            self.assertEqual(file_raw_url(packagename, "test.raw"), CCR_BASE + self.known_values[packagename][inspect.stack()[0][3]])
