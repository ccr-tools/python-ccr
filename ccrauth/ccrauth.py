"""An abstract class to manage CCR authentication information"""


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
        reimplemented in AuthFile, AuthSQLite and AuthKWallet classes
        """
        raise NotImplementedError