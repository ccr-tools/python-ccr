#!/usr/bin/python2
"""A simple Python lib to access the Chakra Community Repository"""
from __future__ import print_function

__all__ = ["getfileraw", "getpkgbuild",
        "getpkgbuildraw", "getpkgurl", "geturl", "info",
        "msearch", "search",
        ]
__version__ = 0.2


import json
import contextlib
import urllib
import urllib2
import cookielib
import poster
import logging
import re

logging.basicConfig(level=logging.DEBUG, format='>> %(levelname)s - %(message)s')


class InvalidPackage(TypeError):
    """Invalid package or wrong file type"""


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
#E_ALLOK = 0
#E_GENER = 1
#E_NETWK = 2
#E_NOPKG = 3
#E_NOFIL = 4
#E_NOUSR = 5
#E_LOGIN = 6


# CCR searching and info
def _get_ccr_json(method, arg):
    """returns the parsed json - for internal use only"""
    try:
        with contextlib.closing(urllib2.urlopen(CCR_RPC + method + ARG + arg)) as text:
            return json.loads(text.read(), object_hook=Struct)
    except urllib2.HTTPError:
        raise


def search(keywords):
    """search for some keywords - returns results as a list"""
    results = _get_ccr_json(SEARCH, keywords)
    try:
        return results.results
    except AttributeError:
        raise AttributeError(results)


def info(package):
    """get information for a specific package - returns results as a list"""
    results = _get_ccr_json(INFO, package)
    try:
        return results.results
    except AttributeError:
        raise ValueError((package, results))


def msearch(maintainer):
    """search for packages owned by 'maintainer' - returns results as a list"""
    results = _get_ccr_json(MSEARCH, maintainer)
    try:
        return results.results
    except AttributeError:
        raise ValueError((maintainer, results))


def orphan():
    """search for orphaned packages - returns results as a list"""
    return msearch("0")


# CCR actions
class CCRSession(object):
    """class for all CCR actions """

    def __init__(self, username, password, rememberme=False):
        self._cat2number = {
                "none": 1,
                "daemons": 2,
                "devel": 3,
                "editors": 4,
                "emulators": 5,
                "games": 6,
                "gnome": 7,
                "i18n": 8,
                "kde": 9,
                "lib": 10,
                "modules": 11,
                "multimedia": 12,
                "network": 13,
                "office": 14,
                "educational": 15,
                "system": 16,
                "x11": 17,
                "utils": 18,
                "lib32": 19,
                }
        self.username = username
        remember_me = 'off' if rememberme else "on"
        data = urllib.urlencode({"user": username,
            "passwd": password,
            "remember_me": remember_me
            })
        self._opener = poster.streaminghttp.register_openers()
        self._opener.add_handler(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
        # do a check if the login did work
        try:
            self._opener.open(CCR_BASE, data)
        except urllib2.HTTPError:
            # Network error occured
            # TODO: some error handling stuff
            logging.debug("A network error occured")
            raise
        checkstr = "packages.php?SeB=m&K=" + username
        response = self._opener.open(CCR_BASE).read()
        if not (checkstr in response):
            logging.debug("There was an error logging in")
            logging.debug("Please check if username and password are correct")
            raise ValueError(username, password)

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self._opener.close()

    def check_vote(self, package, return_id=False):
        """check to see if you have already voted for a package"""
        try:
            ccrid = info(package).ID
        except (ValueError, AttributeError):
            logging.debug("{} does not exist".format(package))
            # package does not exist
            # maybe add error message here?
            raise ValueError(package)
        response = self._opener.open(CCR_PKG + "?ID=" + ccrid)
        if "class='button' name='do_UnVote'" in response.read():
            return ((True, ccrid) if return_id else True)
        else:
            return ((False, ccrid) if return_id else False)

    def unvote(self, package):
        """unvote for a package on CCR
           returns False if the package didn't have a vote
           returns True on success
           raises an ValueError if the package doesn't exist
        """
        try:
            voted, id = self.check_vote(package, True)
            if not voted:
                return True  # package didn't have a vote
            data = urllib.urlencode({"IDs[%s]" % (id): 1,
                "ID": id,
                "do_UnVote": 1
                })
            self._opener.open(CCR_PKG, data)
            # check if the package is unvoted now
            return not self.check_vote(package)
        except ValueError:
            logging.warn("Package doesn't exist!")
            raise

    def vote(self, package):
        """vote for a package on CCR
           returns False if  already voted
           returns True on success
           raises a ValueError if the package doesn't exist
        """
        try:
            voted, id = self.check_vote(package, True)
            if voted:
                return True  # package  is already voted
            data = urllib.urlencode({"IDs[%s]" % (id): 1,
                "ID": id,
                "do_Vote": 1
                })
            self._opener.open(CCR_PKG, data)
            # check if the package is unvoted now
            return self.check_vote(package)
        except ValueError:
            logging.warn("Package doesn't exist!")
            raise

    def flag(self, package):
        """flag a CCR package as out of date"""
        try:
            ccrid = info(package).ID
        except (ValueError, AttributeError):
            raise ValueError(package)
        data = urllib.urlencode({"IDs[%s]" % (ccrid): 1,
            "ID": ccrid,
            "do_Flag": 1
            })
        self._opener.open(CCR_PKG, data)
        return False if (info(package).OutOfDate == 0) else True

    def unflag(self, package):
        """unflag a CCR package as out of date"""
        try:
            ccrid = info(package).ID
        except (ValueError, AttributeError):
            raise ValueError(package)
        data = urllib.urlencode({"IDs[%s]" % (ccrid): 1,
            "ID": ccrid,
            "do_UnFlag": 1
            })
        self._opener.open(CCR_PKG, data)
        return True if (info(package).OutOfDate == 0) else False

    def delete(self, package):
        """delete a package from CCR
           Raises ValueError if the package does not exist
        """
        try:
            ccrid = info(package).ID
        except (ValueError, AttributeError):
            raise ValueError(package)
        data = urllib.urlencode({"IDs[%s]" % (ccrid): 1,
            "ID": ccrid,
            "do_Delete": 1,
            "confirm_Delete": 0
            })
        self._opener.open(CCR_PKG, data).read()
        # test if the package still exists <==> delete wasn't succesful
        if info(package) == u"No result found":
            return True  # package deleted
        else:
            return False  # pacage still exists

    def notify(self, package):
        """set the notify flag on a package"""
        try:
            ccrid = info(package).ID
        except (ValueError, AttributeError):
            raise ValueError(package)
        data = urllib.urlencode({"IDs[%s]" % (ccrid): 1,
            "ID": ccrid,
            "do_Notify": 1
            })
        response = self._opener.open(CCR_PKG, data).read()
        if "<option value='do_UnNotify'" in response:
            return True
        else:
                return response
                #return False

    def unnotify(self, package):
        """unset the notify flag on a package"""
        try:
            ccrid = info(package).ID
        except (ValueError, AttributeError):
            raise ValueError(package)
        data = urllib.urlencode({"IDs[%s]" % (ccrid): 1,
            "ID": ccrid,
            "do_UnNotify": 1
            })
        response = self._opener.open(CCR_PKG, data).read()
        if "<option value='do_Notify'" in response:
            return True
        else:
            return False

    def adopt(self, package):
        """adopt an orphaned CCR package"""
        try:
            package_info = info(package)
            ccrid = package_info.ID
            # TODO don't only warn but do somethnig
            if package_info.Maintainer != u'[PKGBUILD error: non-UTF8 character]':
                logging.warn("Warning: Adopting maintained package!")
        except (ValueError, AttributeError):
            raise ValueError(package)
        data = urllib.urlencode({"IDs[%s]" % (ccrid): 1,
            "ID": ccrid,
            "do_Adopt": 1
            })
        response = self._opener.open(CCR_PKG, data).read()
        # FIXME: This returns True if the pacage was adopted, and True
        # if a non-privileged user attempted to adopt a non-orphaned
        # package. The delete() workaround does not work here.
        if "<option value='do_Disown'" in response:
            return True
        else:
            return False

    def disown(self, package):
        """disown a CCR package"""
        try:
            ccrid = info(package).ID
        except (ValueError, AttributeError):
            raise ValueError(package)
        data = urllib.urlencode({"IDs[%s]" % (ccrid): 1,
            "ID": ccrid,
            "do_Disown": 1
            })
        response = self._opener.open(CCR_PKG, data).read()
        if "href='packages.php?O=2275&amp;PP=25&amp;SO=a'" in response:
                return False
        elif "<option value='do_Adopt'" in response:
            return True
        else:
            return False

    def submit(self, f, category):
        """submit a package to CCR
           Raises KeyError on bad category, IOError [Errno 2] if 'f'
           does not exist, and urllib2.HTTPError if there are network
           problems. Returns True if successful, and False if not.
        """
        error = re.compile(r"<span class='error'>(?P<message>.*)</span>")
        params = {"pkgsubmit": 1,
                "category": self._cat2number[category],
                "pfile": open(f, "rb")
                }
        datagen, headers = poster.encode.multipart_encode(params)
        request = urllib2.Request(CCR_SUBMIT, datagen, headers)
        response = urllib2.urlopen(request).read()

        error_message = re.search(error, response)
        if error_message:
            raise InvalidPackage(error_message.groupdict()["message"])
        if "pkgbuild_view.php?p=" in response:
            return True
        else:
            return False

    def setcategory(self, package, category):
        """change/set the category of a package already in the CCR
           Raises KeyError for an invalid category, or urllib2.HTTPError
           if there are network problems. Returns True if successful, and
           False if not.
        """
        try:
            ccrid = info(package).ID
        except (ValueError, AttributeError):
            raise ValueError(package)
        data = urllib.urlencode({"action": "do_ChangeCategory",
            "category_id": self._cat2number[category]
            })
        try:
            pkgurl = CCR_PKG + "?ID=" + ccrid
            response = self._opener.open(pkgurl, data).read()
            checkstr = "selected='selected'>" + category + "</option>"
            if checkstr in response:
                return True
            else:
                return response  # return False
        except urllib2.HTTPError:
            raise


# Other
def getlatest(num):
    """get the info for the latest num CCR packages, returns as a list"""


def geturl(package):
    """get the URL of the package's CCR page"""
    try:
        ccrid = info(package).ID
    except AttributeError:
        raise ValueError(package)
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
    """get the url to an arbitrary file f, like a .install"""
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
