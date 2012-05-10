#!/usr/bin/python2
"""A simple Python lib to access the Chakra Community Repository"""

__all__ = [ "adopt", "disown", "flag", "geturl", "info", "login",
            "msearch", "notify", "search", "unflag", "unnotify",
            "unvote", "vote" ]
__version__ = 0.2

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
CCR_PKG = CCR_BASE + "packages.php"
CCR_SUBMIT = CCR_BASE + "pkgsubmit.php"
ARG = "&arg="
SEARCH = "search"
INFO = "info"
MSEARCH = "msearch"


# Custom error codes
E_GENER = 0
E_ALLOK = 1
E_NOPKG = 2
E_NOFIL = 2
E_NOUSR = 2
E_LOGIN = 2
E_NETWK = 3


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
    try: 
        opener.open(CCR_BASE, data)
    except urllib2.HTTPError:
        return E_NETWK
    checkstr = "Logged-in as: <b>" + username
    if checkstr in opener.open(CCR_BASE).read():
        return opener
    else:
        return E_LOGIN


def vote(package, opener):
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
        response = opener.open(CCR_PKG, data)
        return check(package, opener)
    except urllib2.HTTPError:
        return E_NETWK


def unvote(package, opener):
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
        response = opener.open(CCR_PKG, data)
        if check(package, opener) == E_GENER:
            return E_ALLOK
        else:
            return E_GENER
    except urllib2.HTTPError:
        return E_NETWK


def check(package, opener):
    """check to see if you have already voted for a package"""
    try:
        ccrid = info(package).ID
    except AttributeError:
        return E_NOPKG
    try:
        response = opener.open(CCR_PKG + "?ID=" + ccrid)
        if "class='button' name='do_UnVote' value='UnVote'" in response.read():
            return E_ALLOK
        else:
            return E_GENER
    except urllib2.HTTPError:
        return E_NETWK


def flag(package, opener):
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
        response = opener.open(CCR_PKG, data)
        if "class='button' name='do_UnFlag' value=" in response.read():
            return E_ALLOK
        else:
            return E_GENER
    except urllib2.HTTPError:
        return E_NETWK


def unflag(package, opener):
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
        response = opener.open(CCR_PKG, data)
        if "class='button' name='do_Flag' value=" in response.read():
            return E_ALLOK
        else:
            return E_GENER
    except urllib2.HTTPError:
        return E_NETWK


def delete(package, opener):
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
        response = opener.open(CCR_PKG, data)
        if "WHAT GOES HERE?" in response.read():
            return E_ALLOK
        else:
            return E_GENER
    except urllib2.HTTPError:
        return E_NETWK


def notify(package, opener):
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
        response = opener.open(CCR_PKG, data)
        if "class='button' name='do_UnNotify' value=" in response.read():
            return E_ALLOK
        else:
            return E_GENER
    except urllib2.HTTPError:
        return E_NETWK


def unnotify(package, opener):
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
        response = opener.open(CCR_PKG, data)
        if "class='button' name='do_Notify' value=" in response.read():
            return E_ALLOK
        else:
            return E_GENER
    except urllib2.HTTPError:
        return E_NETWK


def adopt(package, opener):
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
        response = opener.open(CCR_PKG, data)
        if "class='button' name='do_Disown' value=" in response.read():
            return E_ALLOK
        else:
            return E_GENER
    except urllib2.HTTPError:
        return E_NETWK


def disown(package, opener):
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
        response = opener.open(CCR_PKG, data)
        if "class='button' name='do_Adopt' value=" in response.read():
            return E_ALLOK
        else:
            return E_GENER
    except urllib2.HTTPError:
        return E_NETWK


def submit(file, category, opener):
    """submit a package to CCR"""
    data = urllib.urlencode({"pkgsubmit": 1,
                             "category": category,
                             "pfile": "@%s" % (file)
                             })
    try: 
        response = opener.open(CCR_SUBMIT, data)
        if "WHAT GOES HERE?" in response.read():
            return E_ALLOK
        else:
            return response.read()
    except urllib2.HTTPError:
        return E_NETWK


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

