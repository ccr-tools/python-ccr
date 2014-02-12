"""A simple Python lib to access the Chakra Community Repository"""

from __future__ import print_function

__all__ = ["search", "info", "msearch", "list_orphans",
           "getlatest", "geturl", "getpkgurl", "getpkgbuild",
           "getpkgbuildraw", "getfileraw", "CCRSession"]
__version__ = 0.2

import contextlib
import requests
import urllib.parse
import json
import re
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


class InvalidPackage(TypeError):
    """Invalid package or wrong file type"""


class PackageNotFound(ValueError):
    """Package does not exit"""


class CCRWarning(Warning):
    """Base class for all other warnings"""


class _VoteWarning(CCRWarning):
    """Voting didn't work"""


class _FlagWarning(CCRWarning):
    """Flagging as outdated didn't work"""


class _DeleteWarning(CCRWarning):
    """Delete didn't work"""


class _NotifyWarning(CCRWarning):
    """Setting the Notification didn't work"""


class _OwnershipWarning(CCRWarning):
    """Adopting a package failed"""


class _SubmitWarning(CCRWarning):
    """Submitting failed"""


class _CategoryWarning(CCRWarning):
    """Setting the category failed"""


class Struct(dict):
    """allows easy access to the parsed json - stolen from Inkane's paste.py"""

    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        del self[name]


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
        self._username = username
        self._session = requests.session()
        remember_me = "off" if rememberme else "on"
        data = {
            'user': username,
            'passwd': password,
            'remember_me': remember_me
        }

        self._session.post(CCR_BASE, data=data)

        if not ("AURSID" in self._session.cookies):
            logging.debug("There was an error logging in. "
                          "Please check if username and password are correct")
            raise ValueError(username, password)

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.close()

    def close(self):
        """end the session"""
        self._session.close()

    def check_vote(self, package, return_id=False):
        """check to see if you have already voted for a package
        raises a PackageNotFound exception if the package doesn't exist
        raises a ConnectionError if a network error occur
        """
        try:
            ccrid = info(package).ID
        except (ValueError, AttributeError):  # AttributeError shouldn't occur
            raise PackageNotFound(package)

        response = self._session.get(CCR_PKG + "?ID=" + ccrid)

        if "class='button' name='do_UnVote'" in response.text:
            return (True, ccrid) if return_id else True
        else:
            return (False, ccrid) if return_id else False

    def unvote(self, package):
        """unvote a package on CCR
        raises a PackageNotFound exception if the package doesn't exist
        raises a ConnectionError if a network error occur
        raises a _VoteWarning if it is already unvoted or if it couldn't unvote
        """
        # check_vote might raise PackageNotFound
        voted, ccrid = self.check_vote(package, return_id=True)
        if not voted:
            raise _VoteWarning("Already unvoted or never voted!")  # package didn't have a vote or never voted

        data = {
            "IDs[%s]" % ccrid: 1,
            "ID": ccrid,
            "do_UnVote": 1
        }
        self._session.post(CCR_PKG, data=data)

        # check if the package is unvoted now
        if self.check_vote(package):
            raise _VoteWarning("Couldn't unvote {}".format(package))

    def vote(self, package):
        """vote for a package on CCR
        raises a PackageNotFound if the package doesn't exist
        raises a ConnectionError if a network error occur
        raises a _VoteWarning if it is already voted or if it couldn't vote
        """
        # check_vote might raise PackageNotFound
        voted, ccrid = self.check_vote(package, return_id=True)
        if voted:
            raise _VoteWarning("Already voted!")  # package is already voted

        data = {
            "IDs[%s]" % ccrid: 1,
            "ID": ccrid,
            "do_Vote": 1
        }
        self._session.post(CCR_PKG, data=data)

        # check if the package is voted now
        if not self.check_vote(package):
            raise _VoteWarning("Couldn't vote for {}".format(package))

    def flag(self, package):
        """flag a CCR package as out of date
        raises a ValueError if the package doesn't exist
        raises a ConnectionError if a network error occur
        raises a _FlagWarning on failure
        """
        try:
            ccrid = info(package).ID
        except (ValueError, AttributeError):
            raise PackageNotFound(package)

        data = {
            "IDs[%s]" % ccrid: 1,
            "ID": ccrid,
            "do_Flag": 1
        }
        self._session.post(CCR_PKG, data=data)

        if info(package).OutOfDate == "0":
            raise _FlagWarning("Couldn't flag {} as out of date".format(package))

    def unflag(self, package):
        """unflag a CCR package as out of date
        raises a ValueError if the package doesn't exist
        raises a ConnectionError if a network error occur
        raises a _FlagWarning on failure
        """
        try:
            ccrid = info(package).ID
        except (ValueError, AttributeError):
            raise PackageNotFound(package)

        data = {
            "IDs[%s]" % ccrid: 1,
            "ID": ccrid,
            "do_UnFlag": 1
        }
        self._session.post(CCR_PKG, data=data)

        if info(package).OutOfDate == "1":
            raise _FlagWarning("Couldn't remove flag".format(package))

    def delete(self, package):
        """delete a package from CCR
        raises ValueError if the package does not exist
        raises a ConnectionError if a network error occur
        raises a _DeleteWarning on failure
        """
        #FIXME Throw two exceptions if package doesn't exists
        try:
            pkginfo = info(package)
            ccrid = pkginfo.ID
        except (ValueError, AttributeError):
            raise ValueError(package)

        data = {
            "IDs[%s]" % ccrid: 1,
            "ID": ccrid,
            "do_Delete": 1,
            "confirm_Delete": 0
        }
        self._session.post(CCR_PKG, data=data)

        # test if the package still exists <==> delete wasn't succesful
        # FIXME use _getccr for a quicker check, avoiding the need to catch the exception
        try:
            #FIXME Throw WARNING - Package couldn't be found
            info(package)
            raise _DeleteWarning("Couldn't delete {}".format(package))
        except PackageNotFound:
            pass  # everything works

    def notify(self, package):
        """set the notify flag on a package
        raises ValueError if the package does not exist
        raises a ConnectionError if a network error occur
        raises a _NotifyWarning on failure
        """
        try:
            ccrid = info(package).ID
        except (ValueError, AttributeError):
            raise ValueError(package)

        data = {
            "IDs[%s]" % ccrid: 1,
            "ID": ccrid,
            "do_Notify": 1
        }
        response = self._session.post(CCR_PKG, data=data)

        # FIXME use a more stable check
        if "<option value='do_UnNotify'" not in response.text:
            raise _NotifyWarning(response)

    def unnotify(self, package):
        """unset the notify flag on a package
        raises ValueError if the package does not exist
        raises a ConnectionError if a network error occur
        raises a _NotifyWarning on failure
        """
        try:
            ccrid = info(package).ID
        except (ValueError, AttributeError):
            raise ValueError(package)

        data = {
            "IDs[%s]" % ccrid: 1,
            "ID": ccrid,
            "do_UnNotify": 1
        }
        response = self._session.post(CCR_PKG, data=data)

        if "<option value='do_Notify'" not in response.text:
            raise _NotifyWarning(response)

    def adopt(self, package):
        """adopt an orphaned CCR package
        raises ValueError if the package does not exist
        raises a ConnectionError if a network error occur
        raises a _OwnershipWarning if the package is already maintained or if it fails
        """
        try:
            pkginfo = info(package)
            ccrid = pkginfo.ID
        except (ValueError, AttributeError):
            raise ValueError(package)

        if pkginfo.MaintainerUID != "0":
            logging.warning("Warning: Adopting maintained package!")
            raise _OwnershipWarning("Couldn't adopt {} : already maintained.".format(package))

        data = {
            "IDs[%s]" % ccrid: 1,
            "ID": ccrid,
            "do_Adopt": 1
        }
        self._session.post(CCR_PKG, data=data)

        try:
            pkginfo = info(package)
        except ValueError:
            raise ValueError(package)

        if pkginfo.Maintainer != self._username:
            raise _OwnershipWarning("You already own {}".format(package))

    def disown(self, package):
        """disown a CCR package
        raises ValueError if the package does not exist
        raises a ConnectionError if a network error occur
        raises a _OwnershipWarning on failure
        """
        try:
            pkginfo = info(package)
            ccrid = pkginfo.ID
        except (ValueError, AttributeError):
            raise ValueError(package)

        data = {
            "IDs[%s]" % ccrid: 1,
            "ID": ccrid,
            "do_Disown": 1
        }
        self._session.post(CCR_PKG, data=data)

        if info(package).MaintainerUID != "0":
            raise _OwnershipWarning("Couldn't disown {}".format(package))

    def submit(self, f, category):
        """submit a package to CCR
        raises KeyError on bad category
        raises IOError [Errno 2] if 'f' does not exist
        raises a ConnectionError if a network error occur
        """

        error = re.compile(r"<span class='error'>(?P<message>.*)</span>")
        data = {
            "pkgsubmit": 1,
            "category": self._cat2number[category],
        }
        files = {'pfile': open(f, "rb")}
        response = self._session.post(CCR_SUBMIT, data=data, files=files)

        error_message = re.search(error, response.text)
        if error_message:
            raise InvalidPackage(error_message.groupdict()["message"])
        if "pkgbuild_view.php?p=" not in response.text:
            raise _SubmitWarning("Couldn't submit {}".format("package"))

    def setcategory(self, package, category):
        """change/set the category of a package already in the CCR
        raises ValueError if the package does not exist
        raises a requests.ConnectionError if a network error occur
        raises _CategoryWarning for an invalid category or if it fails.
        """
        try:
            pkginfo = info(package)
            ccrid = pkginfo.ID
        except (ValueError, AttributeError):
            raise ValueError(package)

        try:
            data = {
                "action": "do_ChangeCategory",
                "category_id": self._cat2number[category]
            }
        except KeyError:
            raise _CategoryWarning("Invalid category!")

        pkgurl = CCR_PKG + "?ID=" + ccrid
        response = self._session.post(pkgurl, data=data)

        #FIXME find a more stable check
        checkstr = "selected='selected'>" + category + "</option>"
        if checkstr not in response.text:
            raise _CategoryWarning(response.text)


# CCR searching and info
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
    except AttributeError:
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
    except AttributeError:
        logging.warning("Package couldn't be found")
        raise PackageNotFound((package, results))


def msearch(maintainer):
    """search for packages owned by 'maintainer' - returns results as a list"""
    results = _get_ccr_json(MSEARCH, maintainer)
    try:
        return results.results
    except AttributeError:
        raise ValueError((maintainer, results))


def list_orphans():
    """search for orphaned packages - returns results as a list"""
    return msearch("0")


# Other
def getlatest(num=10):
    """get the info for the latest num CCR packages, returns as a list"""
    return _get_ccr_json(LATEST, str(num))


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