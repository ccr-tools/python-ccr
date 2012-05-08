#!/usr/bin/python
# A simple Python lib to access the Chakra Community Repository
# Should work in python>=2.7, including python3

__all__ = [ "search", "info", "msearch" ]

import json
import contextlib
import urllib2


class Struct(dict):
    """allows easy access to the parsed json - stolen from Inkane's paste.py"""
    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        del self[name]


CCR_RPC = "http://chakra-linux.org/ccr/rpc.php?type="
ARG = "&arg="
SEARCH = "search"
INFO = "info"
MSEARCH = "msearch"


def get_ccr_json(method, arg):
    """
    returns the parsed json - method can be one of: search, info, or msearch.
    """
    with contextlib.closing(urllib2.urlopen(CCR_RPC + method + ARG + arg)) as text:
        return json.loads(text.read(), object_hook=Struct)


def search(keywords):
    """search for some keywords - returns results as a list"""
    results = get_ccr_json(SEARCH, keywords)
    return results.results


def info(package):
    """return information for a specific package - returns results as a list"""
    results = get_ccr_json(INFO, package)
    return results.results


def msearch(maintainer):
    """search for packages owned by 'maintainer' - returns results as a list"""
    results = get_ccr_json(MSEARCH, maintainer)
    return results.results





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


