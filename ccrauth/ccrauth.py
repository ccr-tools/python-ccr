import abc


class CCRAuth(object):
    """An abstract class to manage CCR authentication information"""
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.username = None
        self.password = None

    def _set_info(self, username, password):
        """ set the username and password
        """
        self.username = username
        self.password = password

    @abc.abstractmethod
    def store_auth_info(self, username, password):
        """ store authentication information
        reimplemented in AuthFile, AuthDB and AuthKWallet classes
        """

    @abc.abstractmethod
    def delete_auth_info(self):
        """ remove authentication information
        reimplemented in AuthFile, AuthDB and AuthKWallet classes
        """