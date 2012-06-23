import unittest
import ccr


class ReturnCorrectccrURL(unittest.TestCase):
    ccrurl_known_values = {
        "cdrtools": "http://chakra-linux.org/ccr/packages.php?ID=2745",
        "ls++-git": "http://chakra-linux.org/ccr/packages.php?ID=3870"
        }

    def testCorrectUrl(self):
        for packagename, url in self.ccrurl_known_values.iteritems():
            result = ccr.getccrurl(packagename)
            self.assertEqual(result, url)

    def testBadPackageName(self):
        pass
