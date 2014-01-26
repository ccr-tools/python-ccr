"""A class to manage CCR authentication information"""

__all__ = ["CCRAuthFile", "CCRAuthSQLite", "CCRAuthKWallet"]

import json
import sqlite3
import logging
from PyKDE4.kdeui import KWallet  # TODO PyKDE4 in requirements.txt


class CCRAuth(object):

    def __init__(self):
        self.username = None
        self.password = None

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


class CCRAuthSQLite(CCRAuth):
    """ class to manage authentication information in a database (ccr.db)
    """
    def __init__(self):
        """ define username and password if the table auth exists
        username and password set to None if the table auth doesn't exists
        """
        super().__init__()

        self.conn = sqlite3.connect('ccr.db')
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='auth';")
        if self.cur.fetchone() is not None:
            self.cur.execute("SELECT username, password FROM auth;")
            data = self.cur.fetchone()
            self._set_info(data[0], data[1])
        else:
            logging.debug("Table auth doesn't exists in the database.")

        self.conn.close()

    def store_auth_info(self, username, password):
        """ store/update authentication information in the database
        """
        self.conn = sqlite3.connect('ccr.db')
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS auth (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
        self.cur.execute("INSERT OR REPLACE INTO auth (id, username, password) VALUES (0,?,?)", (username, password))
        self.conn.commit()
        self.conn.close()
        self._set_info(username, password)


class CCRAuthKWallet(CCRAuth):

    def __init__(self):
        """ define username and password if it exists in KWallet
        """
        super().__init__()

        self.wallet = KWallet.Wallet.openWallet(KWallet.Wallet.LocalWallet(), 0)
        if not self.wallet.hasFolder("chakra-ccr"):
            logging.debug("Folder chakra-ccr doesn't exists in KWallet.")
            return

        self.wallet.setFolder("chakra-ccr")
        key, password = self.wallet.readPassword(self.wallet.entryList()[0])
        self._set_info(self.wallet.entryList()[0], password)

    def store_auth_info(self, username, password):
        """ store authentication information in KWallet
        """
        self.wallet.removeFolder("chakra-ccr")
        self.wallet.createFolder("chakra-ccr")
        self.wallet.setFolder("chakra-ccr")
        self.wallet.writePassword(username, password)
        self._set_info(username, password)