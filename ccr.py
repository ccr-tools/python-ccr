#!/usr/bin/python2
"""A simple Python lib to access the Chakra Community Repository"""

__all__ = [ "search", "info", "msearch", "login", "vote" ]
__version__ = 0.1

import json
import contextlib
import urllib
import urllib2
import cookielib


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
CCR_VOTE = CCR_BASE + "packages.php"
ARG = "&arg="
SEARCH = "search"
INFO = "info"
MSEARCH = "msearch"


# CCR searching and info
def get_ccr_json(method, arg):
    """returns the parsed json"""
    with contextlib.closing(urllib2.urlopen(CCR_RPC + method + ARG + arg)) as text:
        return json.loads(text.read(), object_hook=Struct)


def search(keywords):
    """search for some keywords - returns results as a list"""
    results = get_ccr_json(SEARCH, keywords)
    return results.results


def info(package):
    """get information for a specific package - returns results as a list"""
    results = get_ccr_json(INFO, package)
    return results.results


def msearch(maintainer):
    """search for packages owned by 'maintainer' - returns results as a list"""
    results = get_ccr_json(MSEARCH, maintainer)
    return results.results


# CCR actions
def login(username, password, rememberme='off'):
    """
    log in to the CCR - use like:
    >>> opener = ccr.login(username, password)
    >>> ccr.vote(package, opener)
    """
    data = urllib.urlencode({"user": username,
                             "passwd": password,
                             "remember_me": rememberme
                             })
    cjar = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cjar))
    opener.open(CCR_BASE, data)
    return opener


def vote(package, opener):
    """vote for a package on CCR"""
    ccrid = info(package).ID
    # FIXME: the IDs[%s] thing below is bad, there has to be a better way
    data = urllib.urlencode({"IDs[%s]" % (ccrid): 1,
                             "ID": ccrid,
                             "do_Vote": 1
                             })
    response = opener.open(CCR_VOTE, data)
    return response


def unvote(package, opener):
    """unvote for a package on CCR"""


def check(package, opener):
    """check to see if you have already voted for a package"""


def flag(package, opener):
    """flag a CCR package as out of date"""


def unflag(package, opener):
    """unflag a CCR package as out of date"""


def delete(package, opener):
    """delete a package from CCR"""


def notify(package, opener):
    """set the notify flag on a package"""


def unnotify(package, opener):
    """unset the notify flag on a package"""


def adopt(package, opener):
    """adopt an orphaned CCR package"""


def disown(package, opener):
    """disown a CCR package"""


# Other
def getlatest(num):
    """get the info for the latest num CCR packages, returns as a list"""


def geturl(package):
    """get the URL of the package's CCR page"""




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

