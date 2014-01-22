"""A class to manage CCR authentication"""

__all__ = ["CCRAuthFile", "CCRAuthSQLite", "CCRAuthKWallet"]

import json


class CCRAuth(object):

    username = None
    password = None

    def _set_info(self, username, password):
        """ set the username and password
        """
        self.username = username
        self.password = password

    def store_auth_info(self, username, password):
        """ store authentication information
            reimplmented in child classes
        """
        pass


class CCRAuthFile(CCRAuth):
    """ class to manage authentication information in a file
    """

    def __init__(self):
        """ define username and password if the file ccrauth.txt exists
        raises IOError if the file ccrauth.txt doesn't exists
        """
        try:
            with open('ccrauth.txt') as rfile:
                data = json.load(rfile)
            self._set_info(data['username'], data['password'])
        except IOError:
            pass

    def store_auth_info(self, username, password):
        """ store authentication information in the file ccrauth.txt
        raises IOError if the disk is full
        """
        data = {
            "username": username,
            "password": password
        }

        try:
            with open('ccrauth.txt', 'w') as wfile:
                json.dump(data, wfile)
            self._set_info(data['username'], data['password'])
        except IOError:
            raise


class CCRAuthSQLite(CCRAuth):
    pass


class CCRAuthKWallet(CCRAuth):
    pass