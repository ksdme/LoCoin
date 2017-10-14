"""
	@author ksmde
	the wallet keys generator for the
	given app kind of stuff!
"""

# the siginging mechanism
from rsa import *
from utils import *
from binascii import unhexlify

# required constant, helps during translation
# of the public key from a number to string
_MAP_GEN_TUPLE = ([(str(l), chr(l+97)) for l in xrange(0, 26)] +
                  [(str(l), chr(l+39)) for l in xrange(26, 52)] +
                  [(str(l), chr(l-4))  for l in xrange(52, 62)])

# useful when translating from pub key to alpha
_KEY_TRANSLATE_MAP_FORWARD = dict(_MAP_GEN_TUPLE)

# used when translating from alpha to pub key
_KEY_TRANSLATE_MAP_BACKWARD = dict(map(
    lambda elm: (elm[1], elm[0]), _MAP_GEN_TUPLE))

def transform_pub_key_to_alpha(key):
    """
        transforms a given pub key into
        an alphanumeric key used for txn
    """
    key, transformed = str(key), ""
    current, key_len = 0, len(key)

    while current < key_len:
        partial = key[current]
        try:
            transformed += _KEY_TRANSLATE_MAP_FORWARD[partial+key[current+1]]
            current += 2
        except (KeyError, IndexError):
            transformed += _KEY_TRANSLATE_MAP_FORWARD[partial]
            current += 1

    return transformed

def transform_alpha_to_pub_key(key):
    """
        transforms a given alpha numeric
        key into its pub key form
    """
    transformed, key = "", str(key)
    for elm in key:
        transformed += _KEY_TRANSLATE_MAP_BACKWARD[elm]

    return transformed

class Wallet(object):

	@staticmethod
	def new():
		keys = newkeys(4096, poolsize=2)

	@staticmethod
    def getPublicKey(wallet):
        """
            takes a wallet and generates your
            public alphanumeric key
        """

        pub_key = str(wallet[0].n)
        return transform_pub_key_to_alpha(pub_key)

	@staticmethod
	def loadPublic(publicKey):
		publicKey = unhexlify(publicKey)
		return SigningKey.from_string(publicKey, curve=SECP256k1)

	@staticmethod
	def loadPrivate(privateKey):
		privateKey = unhexlify(privateKey, curve=SECP256k1)
		return VerifyingKey.from_string(privateKey, curve=SECP256k1)

	@staticmethod
	def load(publicKey, privateKey):
		return Wallet.loadPublic(publicKey), Wallet.loadPrivate(privateKey)

class Identity(Wallet):
	"""
		simple namespace duplication,
		I think it would be neat to have
		different classes for different roles
	"""
	pass
