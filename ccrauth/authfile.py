"""A class to manage authentication information in a file (ccrauth.txt)"""

import json
import logging
from ccrauth.ccrauth import CCRAuth


class AuthFile(CCRAuth):

    def __init__(self):
        """ define username and password if the file exists
        username and password set to None if the file doesn't exists
        """
        super().__init__()

        try:
            with open('ccrauth.txt') as rfile:
                data = json.load(rfile)
        except IOError:
            logging.debug("File ccrauth.txt doesn't exists.")
            return

        self._set_info(data['username'], data['password'])

    def store_auth_info(self, username, password):
        """ store authentication information in the file
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

        self._set_info(username, password)