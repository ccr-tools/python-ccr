import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import unittest
import ccr


class TestCCRStatic(unittest.TestCase):

    MAINTAINER = "Guillaume"
    KNOWN_VALUES = {
        "cdrtools": {
            "test_geturl": "packages.php?ID=2745",
            "test_getpkgurl": "packages/cd/cdrtools/cdrtools.tar.gz",
            "test_getpkgbuild": "pkgbuild_view.php?p=cdrtools",
            "test_getpkgbuildraw": "packages/cd/cdrtools/cdrtools/PKGBUILD",
            "test_getfileraw": "packages/cd/cdrtools/cdrtools/test.raw"
        },
        "ls++-git": {
            "test_geturl": "packages.php?ID=3870",
            "test_getpkgurl": "packages/ls/ls++-git/ls++-git.tar.gz",
            "test_getpkgbuild": "pkgbuild_view.php?p=ls++-git",
            "test_getpkgbuildraw": "packages/ls/ls++-git/ls++-git/PKGBUILD",
            "test_getfileraw": "packages/ls/ls++-git/ls++-git/test.raw"
        }
    }

    def test_search(self):
        for packagename in self.KNOWN_VALUES:
            results = ccr.search(packagename)
            self.assertGreaterEqual(len(results), 1)

    def test_info(self):
        for packagename in self.KNOWN_VALUES:
            results = ccr.info(packagename)
            self.assertEqual(results.Name, packagename)

    def test_msearch(self):
        results = ccr.msearch(self.MAINTAINER)
        self.assertGreaterEqual(len(results), 1)

    def test_list_orphans(self):
        results = ccr.list_orphans()
        self.assertGreaterEqual(len(results), 1)

    # Other
    def test_getlatest(self):
        results = ccr.getlatest()
        self.assertEqual(len(results.results), 10)

    def test_geturl(self):
        for packagename in self.KNOWN_VALUES:
            result = ccr.geturl(packagename)
            self.assertEqual(result, ccr.CCR_BASE + self.KNOWN_VALUES[packagename][inspect.stack()[0][3]])

    def test_getpkgurl(self):
        for packagename in self.KNOWN_VALUES:
            result = ccr.getpkgurl(packagename)
            self.assertEqual(result, ccr.CCR_BASE + self.KNOWN_VALUES[packagename][inspect.stack()[0][3]])

    def test_getpkgbuild(self):
        for packagename in self.KNOWN_VALUES:
            result = ccr.getpkgbuild(packagename)
            self.assertEqual(result, ccr.CCR_BASE + self.KNOWN_VALUES[packagename][inspect.stack()[0][3]])

    def test_getpkgbuildraw(self):
        for packagename in self.KNOWN_VALUES:
            result = ccr.getpkgbuildraw(packagename)
            self.assertEqual(result, ccr.CCR_BASE + self.KNOWN_VALUES[packagename][inspect.stack()[0][3]])

    def test_getfileraw(self):
        for packagename in self.KNOWN_VALUES:
            result = ccr.getfileraw(packagename, "test.raw")
            self.assertEqual(result, ccr.CCR_BASE + self.KNOWN_VALUES[packagename][inspect.stack()[0][3]])


if __name__ == '__main__':
    unittest.main()