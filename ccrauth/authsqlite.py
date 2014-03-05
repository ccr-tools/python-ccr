import sqlite3
import logging
from ccrauth.ccrauth import CCRAuth


class AuthSQLite(CCRAuth):
    """A class to manage authentication information in a database (ccr.db)"""

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