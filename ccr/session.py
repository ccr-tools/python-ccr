import re
import logging
import requests
from ccr.ccr import *

__all__ = ["Session", "PackageNotFound", "InvalidPackage", "CCRWarning"]

logging.basicConfig(level=logging.DEBUG, format='>> %(levelname)s - %(message)s')


class PackageNotFound(ValueError):
    """Package does not exit"""


class InvalidPackage(TypeError):
    """Invalid package or wrong file type"""


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


class Session(object):
    """class for all CCR actions """

    def __init__(self, username=None, password=None, rememberme=False):
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
        self._session = requests.session()
        if username and password is not None:
            self._username = username
            self.authenticate(username, password, rememberme)

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.close()

    def close(self):
        """end the session"""
        self._session.close()

    def authenticate(self, username, password, rememberme=False):
        """authenticate on CCR
        raises a ConnectionError if a network error occur
        raises a ValueError if login fails
        """
        remember_me = "on" if rememberme else "off"
        data = {
            'user': username,
            'passwd': password,
            'remember_me': remember_me,
        }

        self._session.post(CCR_BASE, data)

        if not ("AURSID" in self._session.cookies):
            logging.debug("There was an error logging in. "
                          "Please check if username and password are correct")
            raise ValueError(username, password)

    def check_vote(self, package, return_id=False):
        """check to see if you have already voted for a package
        raises a PackageNotFound exception if the package doesn't exist
        raises a ConnectionError if a network error occur
        """
        try:
            ccrid = info(package).ID
        except (ValueError, KeyError):
            raise PackageNotFound(package)

        response = self._session.get(CCR_PKG + "?ID=" + ccrid).text

        if "class='button' name='do_UnVote'" in response:
            return (True, ccrid) if return_id else True
        else:
            return (False, ccrid) if return_id else False

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
            "do_Vote": 1,
        }
        self._session.post(CCR_PKG, data=data)

        # check if the package is voted now
        if not self.check_vote(package):
            raise _VoteWarning("Couldn't vote for {}".format(package))

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
            "do_UnVote": 1,
        }
        self._session.post(CCR_PKG, data=data)

        # check if the package is unvoted now
        if self.check_vote(package):
            raise _VoteWarning("Couldn't unvote {}".format(package))

    def flag(self, package):
        """flag a CCR package as out of date
        raises a PackageNotFound exception if the package doesn't exist
        raises a ConnectionError if a network error occur
        raises a _FlagWarning on failure
        """
        try:
            ccrid = info(package).ID
        except (ValueError, KeyError):
            raise PackageNotFound(package)

        data = {
            "IDs[%s]" % ccrid: 1,
            "ID": ccrid,
            "do_Flag": 1,
        }
        self._session.post(CCR_PKG, data=data)

        if info(package).OutOfDate == "0":
            raise _FlagWarning("Couldn't flag {} as out of date".format(package))

    def unflag(self, package):
        """unflag a CCR package as out of date
        raises a PackageNotFound exception if the package doesn't exist
        raises a ConnectionError if a network error occur
        raises a _FlagWarning on failure
        """
        try:
            ccrid = info(package).ID
        except (ValueError, KeyError):
            raise PackageNotFound(package)

        data = {
            "IDs[%s]" % ccrid: 1,
            "ID": ccrid,
            "do_UnFlag": 1,
        }
        self._session.post(CCR_PKG, data=data)

        if info(package).OutOfDate == "1":
            raise _FlagWarning("Couldn't remove flag".format(package))

    def notify(self, package):
        """set the notify flag on a package
        raises a PackageNotFound exception if the package doesn't exist
        raises a ConnectionError if a network error occur
        raises a _NotifyWarning on failure
        """
        try:
            ccrid = info(package).ID
        except (ValueError, KeyError):
            raise PackageNotFound(package)

        data = {
            "IDs[%s]" % ccrid: 1,
            "ID": ccrid,
            "do_Notify": 1,
        }
        response = self._session.post(CCR_PKG, data=data).text

        # FIXME use a more stable check
        if "<option value='do_UnNotify'" not in response:
            raise _NotifyWarning(response)

    def unnotify(self, package):
        """unset the notify flag on a package
        raises a PackageNotFound exception if the package doesn't exist
        raises a ConnectionError if a network error occur
        raises a _NotifyWarning on failure
        """
        try:
            ccrid = info(package).ID
        except (ValueError, KeyError):
            raise PackageNotFound(package)

        data = {
            "IDs[%s]" % ccrid: 1,
            "ID": ccrid,
            "do_UnNotify": 1,
        }
        response = self._session.post(CCR_PKG, data=data)

        if "<option value='do_Notify'" not in response.text:
            raise _NotifyWarning(response)

    def adopt(self, package):
        """adopt an orphaned CCR package
        raises a PackageNotFound exception if the package doesn't exist
        raises a ConnectionError if a network error occur
        raises a _OwnershipWarning if the package is already maintained or if it fails
        """
        try:
            pkginfo = info(package)
            ccrid = pkginfo.ID
        except (ValueError, KeyError):
            raise PackageNotFound(package)

        if pkginfo.MaintainerUID != "0":
            logging.warning("Warning: Adopting maintained package!")
            raise _OwnershipWarning("Couldn't adopt {} : already maintained.".format(package))

        data = {
            "IDs[%s]" % ccrid: 1,
            "ID": ccrid,
            "do_Adopt": 1,
        }
        self._session.post(CCR_PKG, data=data)
        try:
            pkginfo = info(package)
        except (ValueError, KeyError):
            raise PackageNotFound(package)

        if pkginfo.Maintainer != self._username:
            raise _OwnershipWarning("Couldn't adopt {}".format(package))

    def disown(self, package):
        """disown a CCR package
        raises a PackageNotFound exception if the package doesn't exist
        raises a ConnectionError if a network error occur
        raises a _OwnershipWarning on failure
        """
        try:
            pkginfo = info(package)
            ccrid = pkginfo.ID
        except (ValueError, KeyError):
            raise PackageNotFound(package)

        data = {
            "IDs[%s]" % ccrid: 1,
            "ID": ccrid,
            "do_Disown": 1,
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
            raise _SubmitWarning("Couldn't submit {}".format(f))

    def delete(self, package):
        """delete a package from CCR
        raises a PackageNotFound exception if the package doesn't exist
        raises a ConnectionError if a network error occur
        raises a _DeleteWarning on failure
        """
        #FIXME Throw two exceptions if package doesn't exists
        try:
            pkginfo = info(package)
            ccrid = pkginfo.ID
        except (ValueError, KeyError):
            raise PackageNotFound(package)

        data = {
            "IDs[%s]" % ccrid: 1,
            "ID": ccrid,
            "do_Delete": 1,
            "confirm_Delete": 0,
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

    def setcategory(self, package, category):
        """change/set the category of a package already in the CCR
        raises a PackageNotFound exception if the package doesn't exist
        raises a requests.ConnectionError if a network error occur
        raises _CategoryWarning for an invalid category or if it fails.
        """
        try:
            pkginfo = info(package)
            ccrid = pkginfo.ID
        except (ValueError, KeyError):
            raise PackageNotFound(package)

        try:
            data = {
                "action": "do_ChangeCategory",
                "category_id": self._cat2number[category],
            }
        except KeyError:
            raise _CategoryWarning("Invalid category!")

        pkgurl = CCR_PKG + "?ID=" + ccrid
        response = self._session.post(pkgurl, data=data)

        #FIXME find a more stable check
        checkstr = "selected='selected'>" + category + "</option>"
        if checkstr not in response.text:
            raise _CategoryWarning(response.text)