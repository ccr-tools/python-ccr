#!/usr/bin/python2
"""A simple Python lib to access the Chakra Community Repository"""

#__all__ = ["adopt", "disown", "flag", "getfileraw", "getpkgbuild",
        #"getpkgbuildraw", "getpkgurl", "geturl", "info", "login",
        #"msearch", "notify", "search", "unflag", "unnotify",
        #"unvote", "vote"]
__version__ = 0.2

import json
import contextlib
import urllib
import urllib2
import cookielib
import poster


class Struct(dict):
    """allows easy access to the parsed json - stolen from Inkane's paste.py"""
    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        del self[name]


CCR_BASE = "http://chakra-linux.org/ccr/"
CCR_RPC = CCR_BASE + "rpc.php?type="
CCR_PKG = CCR_BASE + "packages.php"
CCR_SUBMIT = CCR_BASE + "pkgsubmit.php"
ARG = "&arg="
SEARCH = "search"
INFO = "info"
MSEARCH = "msearch"


# Custom error codes
E_ALLOK = 0
E_GENER = 1
E_NETWK = 2
E_NOPKG = 3
E_NOFIL = 4
E_NOUSR = 5
E_LOGIN = 6


# CCR searching and info
def get_ccr_json(method, arg):
    """returns the parsed json"""
    try:
        with contextlib.closing(urllib2.urlopen(CCR_RPC + method + ARG + arg)) as text:
            return json.loads(text.read(), object_hook=Struct)
    except urllib2.HTTPError:
        return E_NETWK


def search(keywords):
    """search for some keywords - returns results as a list"""
    results = get_ccr_json(SEARCH, keywords)
    try:
        return results.results
    except AttributeError:
        return results


def info(package):
    """get information for a specific package - returns results as a list"""
    results = get_ccr_json(INFO, package)
    try:
        return results.results
    except AttributeError:
        return results


def msearch(maintainer):
    """search for packages owned by 'maintainer' - returns results as a list"""
    results = get_ccr_json(MSEARCH, maintainer)
    try:
        return results.results
    except AttributeError:
        return results


# CCR actions
class CCRUserActions(object):
    """class for all CCR actions """

    def __init__(self, username, password, rememberme='off'):
        data = urllib.urlencode({"user": username,
            "passwd": password,
            "remember_me": rememberme
            })
        self.opener = poster.streaminghttp.register_openers()
        self.opener.add_handler(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
        #opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cjar)) REMOVE
        # do a check if the login did work
        try:
            self.opener.open(CCR_BASE, data)
        except urllib2.HTTPError:
            # Network error occured
            # TODO: some error handling stuff
            raise
        checkstr = "packages.php?SeB=m&K=" + username
        if checkstr in self.opener.open(CCR_BASE).read():
            pass
        else:
            # TODO print an error message
            raise Exception

    def check(self, package):
        """check to see if you have already voted for a package"""
        try:
            ccrid = info(package).ID
        except AttributeError:
            return E_NOPKG
        try:
            response = self.opener.open(CCR_PKG + "?ID=" + ccrid)
            # TODO: value is not reliable (translated)
            if "class='button' name='do_UnVote'" in response.read():
                "works"
                return E_ALLOK
            else:
                return E_GENER
        except urllib2.HTTPError:
            # TODO: Might be better to reraise the exception
            return E_NETWK

    def unvote(self, package):
        """unvote for a package on CCR"""
        try:
            ccrid = info(package).ID
        except AttributeError:
            return E_NOPKG
        data = urllib.urlencode({"IDs[%s]" % (ccrid): 1,
            "ID": ccrid,
            "do_UnVote": 1
            })
        try:
            response = self.opener.open(CCR_PKG, data)
            if self.check(package) == E_GENER:
                return E_ALLOK
            else:
                return E_GENER
        except urllib2.HTTPError:
            return E_NETWK

    def vote(self, package):
        """vote for a package in the CCR"""
        try:
            ccrid = info(package).ID
        except AttributeError:
            return E_NOPKG
        # FIXME: the IDs[%s] thing below is bad, there has to be a better way
        data = urllib.urlencode({"IDs[%s]" % (ccrid): 1,
            "ID": ccrid,
            "do_Vote": 1
            })
        try:
            response = self.opener.open(CCR_PKG, data)
            return self.check(package)
        except urllib2.HTTPError:
            return E_NETWK

    def flag(self, package):
        """flag a CCR package as out of date"""
        try:
            ccrid = info(package).ID
        except AttributeError:
            return E_NOPKG
        data = urllib.urlencode({"IDs[%s]" % (ccrid): 1,
            "ID": ccrid,
            "do_Flag": 1
            })
        try:
            response = self.opener.open(CCR_PKG, data)
            if "class='button' name='do_UnFlag' value=" in response.read():
                return E_ALLOK
            else:
                return E_GENER
        except urllib2.HTTPError:
            return E_NETWK

    def unflag(self, package):
        """unflag a CCR package as out of date"""
        try:
            ccrid = info(package).ID
        except AttributeError:
            return E_NOPKG
        data = urllib.urlencode({"IDs[%s]" % (ccrid): 1,
            "ID": ccrid,
            "do_UnFlag": 1
            })
        try:
            response = self.opener.open(CCR_PKG, data)
            if "class='button' name='do_Flag' value=" in response.read():
                return E_ALLOK
            else:
                return E_GENER
        except urllib2.HTTPError:
            return E_NETWK

    def delete(self, package):
        """delete a package from CCR"""
        try:
            ccrid = info(package).ID
        except AttributeError:
            return E_NOPKG
        data = urllib.urlencode({"IDs[%s]" % (ccrid): 1,
            "ID": ccrid,
            "do_Delete": 1
            })
        try:
            response = self.opener.open(CCR_PKG, data)
            if "WHAT GOES HERE?" in response.read():
                return E_ALLOK
            else:
                return E_GENER
        except urllib2.HTTPError:
            return E_NETWK

    def notify(self, package):
        """set the notify flag on a package"""
        try:
            ccrid = info(package).ID
        except AttributeError:
            return E_NOPKG
        data = urllib.urlencode({"IDs[%s]" % (ccrid): 1,
            "ID": ccrid,
            "do_Notify": 1
            })
        try:
            response = self.opener.open(CCR_PKG, data)
            if "class='button' name='do_UnNotify' value=" in response.read():
                return E_ALLOK
            else:
                return E_GENER
        except urllib2.HTTPError:
            return E_NETWK

    def unnotify(self, package):
        """unset the notify flag on a package"""
        try:
            ccrid = info(package).ID
        except AttributeError:
            return E_NOPKG
        data = urllib.urlencode({"IDs[%s]" % (ccrid): 1,
            "ID": ccrid,
            "do_UnNotify": 1
            })
        try:
            response = self.opener.open(CCR_PKG, data)
            if "class='button' name='do_Notify' value=" in response.read():
                return E_ALLOK
            else:
                return E_GENER
        except urllib2.HTTPError:
            return E_NETWK

    def adopt(self, package):
        """adopt an orphaned CCR package"""
        try:
            ccrid = info(package).ID
        except AttributeError:
            return E_NOPKG
        data = urllib.urlencode({"IDs[%s]" % (ccrid): 1,
            "ID": ccrid,
            "do_Adopt": 1
            })
        try:
            response = self.opener.open(CCR_PKG, data)
            if "class='button' name='do_Disown' value=" in response.read():
                return E_ALLOK
            else:
                return E_GENER
        except urllib2.HTTPError:
            return E_NETWK

    def disown(self, package):
        """disown a CCR package"""
        try:
            ccrid = info(package).ID
        except AttributeError:
            return E_NOPKG
        data = urllib.urlencode({"IDs[%s]" % (ccrid): 1,
            "ID": ccrid,
            "do_Disown": 1
            })
        try:
            response = self.opener.open(CCR_PKG, data)
            if "class='button' name='do_Adopt' value=" in response.read():
                return E_ALLOK
            else:
                return E_GENER
        except urllib2.HTTPError:
            return E_NETWK

    def submit(self, f, category):
        """submit a package to CCR"""
        #catID = "set this with some sort of array"
        params = {"pkgsubmit": 1,
                "category": category,
                "pfile": open(f, "rb")
                }
        datagen, headers = poster.encode.multipart_encode(params)
        try:
            request = urllib2.Request(CCR_SUBMIT, datagen, headers)
            response = urllib2.urlopen(request)
            return response
            # TODO: fix the stuff beneath
            #if "WHAT GOES HERE?" in response.read():
                #return E_ALLOK
            #else:
                #return response.read()
        except urllib2.HTTPError:
            # TODO better rereaise the exception
            # raise
            return E_NETWK

    def setcategory(self, package, category):
        """change/set the category of a package already in CCR"""


# Other
def getlatest(num):
    """get the info for the latest num CCR packages, returns as a list"""


def geturl(package):
    """get the URL of the package's CCR page"""
    try:
        ccrid = info(package).ID
    except AttributeError:
        return E_NOPKG
    url = CCR_PKG + "?ID=" + ccrid
    return url


def getpkgurl(package):
    """get the url to the source package"""
    path = "packages/" + package[:2] + "/" + package + "/"
    url = CCR_BASE + path + package + ".tar.gz"
    return url


def getpkgbuild(package):
    """get the url to the online PKGBUILD viewer"""
    url = CCR_BASE + "pkgbuild_view.php?p=" + package
    return url


def getpkgbuildraw(package):
    """get the url to the actual PKGBUILD"""
    path = "packages/" + package[:2] + "/" + package + "/" + package + "/"
    url = CCR_BASE + path + "PKGBUILD"
    return url


def getfileraw(package, f):
    """get the url to an arbitrary f, like a .install"""
    path = "packages/" + package[:2] + "/" + package + "/" + package + "/"
    url = CCR_BASE + path + f
    return url


if __name__ == "__main__":
    r = info("snort")
    print("Name           : %s" % r.Name)
    print("Version        : %s" % r.Version)
    print("URL            : %s" % r.URL)
    print("License        : %s" % r.License)
    print("Category       : %s" % r.Category)
    print("Maintainer     : %s" % r.Maintainer)
    print("Description    : %s" % r.Description)
    print("OutOfDate      : %s" % r.OutOfDate)
    print("Votes          : %s" % r.NumVotes)
