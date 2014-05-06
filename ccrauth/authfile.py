import json
import logging
import os
from ccrauth.ccrauth import CCRAuth


class AuthFile(CCRAuth):
    """A class to manage authentication information in a file (ccrauth.txt)"""

    def __init__(self):
        """ define username and password if the file exists
        username and password set to None if the file doesn't exists
        """
        super().__init__()
        self.file_path = os.path.expanduser('~') + "/.config/ccr-tools/ccrauth.txt"

        try:
            with open(self.file_path) as rfile:
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
            "password": password,
        }
        try:
            with open(self.file_path, 'w') as wfile:
                json.dump(data, wfile)
        except IOError:
            raise

        self._set_info(username, password)