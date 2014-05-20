import logging
try:
    from PyKDE4.kdeui import KWallet
except ImportError as e:
    KWallet = e
    # Handle below
from ccrauth.ccrauth import CCRAuth


class AuthKWallet(CCRAuth):
    """ A class to manage authentication information in KWallet"""

    def __init__(self):
        """ define username and password if it exists in KWallet
        """
        super().__init__()

        # Handling this in __init__ means the library can still be
        # imported, even without the pykde4 bindings installed.
        if type(KWallet) == type(ImportError()):
            raise KWallet

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
