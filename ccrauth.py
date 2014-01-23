"""A class to manage CCR authentication information"""

__all__ = ["CCRAuthFile", "CCRAuthSQLite", "CCRAuthKWallet"]

import json
import sqlite3
import os.path


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
            reimplemented in child classes
        """
        pass


class CCRAuthFile(CCRAuth):
    """ class to manage authentication information in a file (ccrauth.txt)
    """

    def __init__(self):
        """ define username and password if the file crauth.txt exists
        raises IOError if the file ccrauth.txt doesn't exists
        raises ValueError if the data in file are malformed
        """
        try:
            with open('ccrauth.txt') as rfile:
                data = json.load(rfile)
        except IOError:
            raise

        try:
            self._set_info(data['username'], data['password'])
        except ValueError:
            raise

    def store_auth_info(self, username, password):
        """ store authentication information in a file
        raises IOError if the disk is full
        raises ValueError if the data in file are malformed
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

        try:
            self._set_info(username, password)
        except ValueError:
            raise


class CCRAuthSQLite(CCRAuth):
    """ class to manage authentication information in a sqlite database (ccr.db)
    """

    def __init__(self):
        """ define username and password if the table auth exists
        """
        #  TODO exceptions
        if os.path.exists('ccr.db') is False:
            return

        conn = sqlite3.connect('ccr.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='auth';")

        if cur.fetchone()[1] == "auth":
            cur.execute("SELECT username, password FROM auth;")
            data = cur.fetchone()
            self._set_info(data[0], data[1])

        conn.close()

    def store_auth_info(self, username, password):
        """ store authentication information in the database
        """
        #  TODO exceptions
        #  TODO modify data instead of inserting new row
        conn = sqlite3.connect('ccr.db')
        cur = conn.cursor()
        cur.execute("CREATE TABLE auth(username TEXT, password TEXT)")
        cur.execute("INSERT INTO auth VALUES (?,?)", (username, password))
        conn.commit()
        conn.close()

        try:
            self._set_info(username, password)
        except ValueError:
            raise


class CCRAuthKWallet(CCRAuth):
    pass