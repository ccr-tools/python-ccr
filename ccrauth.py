"""A class to manage CCR authentication"""

__all__ = ["CCRAuthFile", "CCRAuthSQLite", "CCRAuthKWallet"]

import json


class CCRAuth(object):

    _username = None
    _password = None

    def get_username(self):
        """ get the username
        """
        return self._username

    def get_password(self):
        """ get the password
        """
        return self._password

    def store_auth_info(self, username, password):
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
                self._username = data['username']
                self._password = data['password']
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
        except IOError:
            raise


class CCRAuthSQLite(CCRAuth):
    pass


class CCRAuthKWallet(CCRAuth):
    pass