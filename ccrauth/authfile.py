import json
import logging
import os
from ccrauth.ccrauth import CCRAuth

CCRAUTH_FILE = "ccrauth.txt"


class AuthFile(CCRAuth):
    """A class to manage authentication information in a file (ccrauth.txt)"""

    def __init__(self):
        """ define username and password if the file exists
        username and password set to None if the file doesn't exists
        """
        super().__init__()

        try:
            with open(CCRAUTH_FILE) as file:
                data = json.load(file)
        except OSError:
            logging.debug("File ccrauth.txt cannot be opened.")
            return

        self._set_info(data['username'], data['password'])

    def store_auth_info(self, username, password):
        """ store authentication information in the file
        raises IOError if the disk is full
        """
        data = {
            "username": username,
            "password": password,
        }
        try:
            with open(CCRAUTH_FILE, 'w') as file:
                json.dump(data, file)
        except OSError:
            logging.debug("File ccrauth.txt cannot be opened.")
            return

        self._set_info(username, password)

    def delete_auth_info(self):
        try:
            os.remove(CCRAUTH_FILE)
        except OSError:
            logging.debug("File ccrauth.txt cannot be deleted.")
