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
        requests.get = Mock()
        cls.req_get_return_values = {
            "test_search": '{"type":"mocked_type","results":{"ID":"mocked_ID"}}',
            "test_info": '{"type":"mocked_type","results":{"ID":"mocked_ID","Name":"%s"}}',
            "test_msearch": '{"type":"mocked_type","results":{"ID":"mocked_ID"}}',
            "test_list_orphans": '{"type":"mocked_type","results":{"ID":"mocked_ID"}}',
            "test_getlatest": '{"type":"mocked_type","results":[{"ID":"mocked_ID"},{"ID":"mocked_ID"},'
                              '{"ID":"mocked_ID"},{"ID":"mocked_ID"},{"ID":"mocked_ID"},{"ID":"mocked_ID"},'
                              '{"ID":"mocked_ID"},{"ID":"mocked_ID"},{"ID":"mocked_ID"},{"ID":"mocked_ID"}]}',
            "test_geturl": '{"type":"mocked_type","results":{"ID":"%s"}}',
        }

    def test_search(self):
        for packagename in self.known_values:
            requests.get.return_value.text = self.req_get_return_values[inspect.stack()[0][3]]
            results = search(packagename)
        self.assertGreaterEqual(len(results), 1)

    def test_info(self):
        for packagename in self.known_values:
            requests.get.return_value.text = self.req_get_return_values[inspect.stack()[0][3]].replace("%s", packagename)
            results = info(packagename)
            self.assertEqual(results.Name, packagename)

    def test_msearch(self):
        requests.get.return_value.text = self.req_get_return_values[inspect.stack()[0][3]]
        results = msearch(self.maintainer)
        self.assertGreaterEqual(len(results), 1)

    def test_list_orphans(self):
        requests.get.return_value.text = self.req_get_return_values[inspect.stack()[0][3]]
        results = list_orphans()
        self.assertGreaterEqual(len(results), 1)

    def test_getlatest(self):
        requests.get.return_value.text = self.req_get_return_values[inspect.stack()[0][3]]
        results = getlatest()
        self.assertEqual(len(results.results), 10)

    def test_geturl(self):
        for packagename in self.known_values:
            requests.get.return_value.text = self.req_get_return_values[inspect.stack()[0][3]].replace\
                    ("%s", self.known_values[packagename][inspect.stack()[0][3]][-4:])
            result = geturl(packagename)
            self.assertEqual(result, CCR_BASE + self.known_values[packagename][inspect.stack()[0][3]])

    def test_getpkgurl(self):
        for packagename in self.known_values:
            result = getpkgurl(packagename)
            self.assertEqual(result, CCR_BASE + self.known_values[packagename][inspect.stack()[0][3]])

    def test_getpkgbuild(self):
        for packagename in self.known_values:
            result = getpkgbuild(packagename)
            self.assertEqual(result, CCR_BASE + self.known_values[packagename][inspect.stack()[0][3]])

    def test_getpkgbuildraw(self):
        for packagename in self.known_values:
            result = getpkgbuildraw(packagename)
            self.assertEqual(result, CCR_BASE + self.known_values[packagename][inspect.stack()[0][3]])

    def test_getfileraw(self):
        for packagename in self.known_values:
            result = getfileraw(packagename, "test.raw")
            self.assertEqual(result, CCR_BASE + self.known_values[packagename][inspect.stack()[0][3]])