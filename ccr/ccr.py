"""A simple Python lib to access the Chakra Community Repository"""

from __future__ import print_function

__all__ = ["search", "info", "msearch", "list_orphans",
           "getlatest", "geturl", "getpkgurl", "getpkgbuild",
           "getpkgbuildraw", "getfileraw",
           "CCR_BASE", "CCR_RPC", "CCR_PKG", "CCR_SUBMIT",
           "PackageNotFound",
           ]

import contextlib
import requests
import urllib.parse
import json
import logging

logging.basicConfig(level=logging.DEBUG, format='>> %(levelname)s - %(message)s')

CCR_BASE = "http://chakra-project.org/ccr/"
CCR_RPC = CCR_BASE + "rpc.php?type="
CCR_PKG = CCR_BASE + "packages.php"
CCR_SUBMIT = CCR_BASE + "pkgsubmit.php"
ARG = "&arg="
SEARCH = "search"
INFO = "info"
MSEARCH = "msearch"
LATEST = "getlatest"


class PackageNotFound(ValueError):
    """Package does not exit"""


class Struct(dict):
    """allows easy access to the parsed json - stolen from Inkane's paste.py"""
    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        del self[name]


#CCR static functions
def _get_ccr_json(method, arg):
    """returns the parsed json - for internal use only"""
    # arg must must be quoted to allow input like 'ls++-git'
    arg = urllib.parse.quote(arg)
    with contextlib.closing(requests.get(CCR_RPC + method + ARG + arg)) as results:
        return json.loads(results.text, object_hook=Struct)


def search(keywords):
    """search for some keywords - returns results as a list"""
    results = _get_ccr_json(SEARCH, keywords)
    try:
        return results.results
    except KeyError:
        logging.debug("Nothing could be found.")
        raise ValueError(results)


def info(package):
    """get information for a specific package - returns results as a list"""
    results = _get_ccr_json(INFO, package)
    try:
        if results.results == u'No result found':
            logging.warning("Package couldn't be found")
            raise PackageNotFound("Package {} couldn't be found".format(package))
        return results.results
    except KeyError:
        logging.warning("Package couldn't be found")
        raise PackageNotFound((package, results))


def msearch(maintainer):
    """search for packages owned by 'maintainer' - returns results as a list"""
    results = _get_ccr_json(MSEARCH, maintainer)
    try:
        return results.results
    except KeyError:
        raise ValueError((maintainer, results))


def list_orphans():
    """search for orphaned packages - returns results as a list"""
    return msearch("0")


def getlatest(num=10):
    """get the info for the latest num CCR packages, returns as a list"""
    return _get_ccr_json(LATEST, str(num))


def geturl(package):
    """get the URL of the package's CCR page"""
    try:
        ccrid = info(package).ID
    except KeyError:
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