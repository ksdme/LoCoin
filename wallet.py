"""
	@author ksmde
	the wallet keys generator for the
	given app kind of stuff!
"""

# the siginging mechanism 
from codecs import encode
from binascii import unhexlify
from ecdsa import SigningKey, VerifyingKey, SECP256k1

class Wallet(object):

	@staticmethod
	def new():
		publicKey = SigningKey.generate(curve=SECP256k1)
		privateKey = publicKey.get_verifying_key()

		publicKey = encode(publicKey.to_string(), "hex").decode("utf-8")
		privateKey = encode(privateKey.to_string(), "hex").decode("utf-8")
		return str(publicKey), str(privateKey)

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
