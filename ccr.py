#!/usr/bin/python2
# A simple Python lib to access the Chakra Community Repository

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
ARG = "&arg="
SEARCH = "search"
INFO = "info"
MSEARCH = "msearch"


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


def login(username, password, rememberme='off'):
    """log in to the CCR"""
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
    # TODO: Should this call login(), instead of the way ot works now?
    ccrid = info(package).ID
    # FIXME: the ccrid thing below is bad, there has to be a better way
    data = urllib.urlencode({"IDs[%s]" % (ccrid): 1,
                             "ID": ccrid,
                             "do_Vote": 1
                             })
    response = opener.open(CCR_BASE, data)
    return respose.read()



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

