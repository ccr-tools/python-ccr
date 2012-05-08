#!/usr/bin/python
# A simple Python lib to access the Chakra Community Repository
# Should work in python>=2.7, including python3

__all__ = ["maintainer", "category", "votes"]

import json
import contextlib
import urllib
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



def get_ccr_json(method, arg):
    """
    returns the parsed json - method can be one of: search, info, or msearch.
    """
    with contextlib.closing(urllib2.urlopen(CCR_RPC + method + ARG + arg)) as text:
        return json.loads(text.read(), object_hook=Struct)




if __name__ == "__main__":
    print(maintainer("snort"))
