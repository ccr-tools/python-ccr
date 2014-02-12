import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import unittest
import ccr


class TestCCRStatic(unittest.TestCase):

    pkg_list = ["cdrtools", "ls++-git"]
    maintainer = "Guillaume"

    def test_search(self):
        results = ccr.search(self.pkg_list[1])
        self.assertGreaterEqual(len(results), 1)

    def test_info(self):
        results = ccr.info(self.pkg_list[1])
        self.assertEqual(results.Name, self.pkg_list[1])

    def test_msearch(self):
        results = ccr.msearch(self.maintainer)
        self.assertGreaterEqual(len(results), 1)

    def test_list_orphans(self):
        results = ccr.list_orphans()
        self.assertGreaterEqual(len(results), 1)

    # Other
    def test_getlatest(self):
        results = ccr.getlatest()
        self.assertEqual(len(results.results), 10)

    # values in known_values must match pkg_list array.
    def test_geturl(self):
        known_values = ["packages.php?ID=2745", "packages.php?ID=3870"]
        for packagename, value in zip(self.pkg_list, known_values):
            result = ccr.geturl(packagename)
            self.assertEqual(result, ccr.CCR_BASE + value)

    def test_getpkgurl(self):
        known_values = ["packages/cd/cdrtools/cdrtools.tar.gz", "packages/ls/ls++-git/ls++-git.tar.gz"]
        for packagename, value in zip(self.pkg_list, known_values):
            result = ccr.getpkgurl(packagename)
            self.assertEqual(result, ccr.CCR_BASE + value)

    def test_getpkgbuild(self):
        known_values = ["pkgbuild_view.php?p=cdrtools", "pkgbuild_view.php?p=ls++-git"]
        for packagename, value in zip(self.pkg_list, known_values):
            result = ccr.getpkgbuild(packagename)
            self.assertEqual(result, ccr.CCR_BASE + value)

    def test_getpkgbuildraw(self):
        known_values = ["packages/cd/cdrtools/cdrtools/PKGBUILD", "packages/ls/ls++-git/ls++-git/PKGBUILD"]
        for packagename, value in zip(self.pkg_list, known_values):
            result = ccr.getpkgbuildraw(packagename)
            self.assertEqual(result, ccr.CCR_BASE + value)

    def test_getfileraw(self):
        known_values = ["packages/cd/cdrtools/cdrtools/test.raw", "packages/ls/ls++-git/ls++-git/test.raw"]
        for packagename, value in zip(self.pkg_list, known_values):
            result = ccr.getfileraw(packagename, "test.raw")
            self.assertEqual(result, ccr.CCR_BASE + value)


if __name__ == '__main__':
    unittest.main()