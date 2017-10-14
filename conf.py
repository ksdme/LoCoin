"""
    @author ksdme
"""
from toyutils import enum

class WalletConf(enum):
    """
        handles conf stuff for the wallet,
        such as key sizes and stuff
    """

    # bits, 40 Bytes
    KEY_PAIR_SIZE = 2048

    # file names
    WALLET_FILE_EXTENSION = ".wallet"
    PUBLIC_KEY_FILE_NAME = "wallet_pub.pem"
    PRIVATE_KEY_FILE_NAME = "wallet_priv.pem"

    # keys configuration
    KEY_PAIR_E_VALUE = 65537
