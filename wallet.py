"""
    @author ksmde
    the wallet keys generator for the
    given app kind of stuff!
"""

# the siginging mechanism
from utils import *
from conf import *
from toyutils import *
from binascii import unhexlify

from StringIO import StringIO
from os.path import isdir, join
from zipfile import ZipFile, ZIP_STORED
from rsa import newkeys, PublicKey, PrivateKey

class Wallet(object):

    @staticmethod
    def new():
        return newkeys(WalletConf.KEY_PAIR_SIZE, poolsize=2)

    @staticmethod
    def getPublicKey(wallet):
        """
            takes a wallet and generates your
            public alphanumeric key
        """

        pub_key = str(wallet[0].n)
        return transform_pub_key_to_alpha(pub_key)

    @staticmethod
    def reconstructPublicKey(key):
        return PublicKey(int(transform_alpha_to_pub_key(key)), 65537)

    @staticmethod
    def loadWallet(uri):
        """
            loads a wallet from a public key file
            and a private key file
        """
        assert not isdir(uri)

        with ZipFile(uri, "r") as walletfile:
            pub_key = (PublicKey.load_pkcs1(walletfile.read(
                WalletConf.PUBLIC_KEY_FILE_NAME)))

            priv_key = PrivateKey.load_pkcs1(walletfile.read(
                WalletConf.PRIVATE_KEY_FILE_NAME))

        return pub_key, priv_key

    @staticmethod
    def saveWallet(key_pair, save_to):
        """
            saves a given wallet key pair to
            a given directory, in pem format
        """
        if isdir(save_to):
            save_to = join(save_to, "toycoin")

        pub_key, priv_key = key_pair
        save_to = save_to+WalletConf.WALLET_FILE_EXTENSION
        with ZipFile(save_to, "w", ZIP_STORED) as walletfile:

            binary_data = StringIO(pub_key.save_pkcs1(format="PEM")).getvalue()
            walletfile.writestr(WalletConf.PUBLIC_KEY_FILE_NAME, binary_data)

            binary_data = StringIO(priv_key.save_pkcs1(format="PEM")).getvalue()
            walletfile.writestr(WalletConf.PRIVATE_KEY_FILE_NAME, binary_data)

class Identity(Wallet):
    """
        simple namespace duplication,
        I think it would be neat to have
        different classes for different roles
    """
    pass

if __name__ == "__main__":
    newWallet = Wallet.new()
    Wallet.saveWallet(newWallet, "sample")
    loaded = Wallet.loadWallet("sample.wallet")
    print Wallet.getPublicKey(loaded)
    print loaded
