"""
	@author ksdme
	the various types of coins
"""
import rsa
from utils import *
from wallet import *
from hashlib import sha1
from app_exceptions import *
from json import dumps, loads
from time import time as tyme
from binascii import hexlify

# Simply to keep txns
class Txn(object): pass

class TxnPool(object):
	""" maintainsa a transaction pool """

	def __init__(self, empty=[]):
		assert isinstance(empty, list)
		self._pool = empty

	""" FIFO """
	def select(self):
		for _ in xrange(10):
			try:
				yield self.pool.pop(_)
			except IndexError:
				break
	
	def addToPool(self, txn):
		assert isinstance(txn, Txn)

		if txn.valid():
			self._pool.append(txn)
		else:
			raise BlockRejecetedToPool()

	pool = property(lambda self: self._pool)

class LoTxn(Txn):

	@staticmethod
	def load(txn):
		return LoTxn(
			txn.raw["loc"],
			txn.raw["difficulty"],
			txn.pub,
			txn.raw["at"])

	def __init__(self, lat_long, difficulty, identity, time=None):
		assert isinstance(difficulty, int)
		assert not isinstance(identity, str)

		self._lat_long = lat_long
		self._time = int(tyme()*1000)
		self._difficulty = int(difficulty)
		self._pubKey = Identity.getPublicKey(identity)

		if time is not None:
			self._time = int(time)

		self._lo_txn_partial = {
			"pub": sha1(self._pubKey).hexdigest(),
			"ok": 200
		}

		lo_txn_signed = dumps(self._lo_txn_partial)
		lo_txn_signed = rsa.encrypt(lo_txn_signed, identity[0])
		lo_txn_signed = hexlify(lo_txn_signed)

		self._lo_txn = {
			"type": "lo",
			"at": self._time,
			"loc": self._lat_long,
			"identity": lo_txn_signed,
			"difficulty": self._difficulty
		}

		lo_txn_hash = dumps(self._lo_txn)
		lo_txn_hash = sha1(lo_txn_hash).hexdigest()

		self._lo_txn["hash"] = lo_txn_hash
		self._lo_txn["nonce"] = ""

	def json(self):
		return dumps(self._lo_txn)

	def nonceTest(self, nonce):
		self.raw["nonce"] = str(nonce)

		loTxnStr = self.json()
		loTxnStr = sha1(loTxnStr).hexdigest()
		return str(loTxnStr[:self.raw["difficulty"]]).count("0") == int(self.raw["difficulty"])

	def setNonce(self, nonce):
		self.raw["nonce"] = str(nonce)

	def valid(self):
		return self.nonceTest(self.raw["nonce"])

	raw = property(lambda self: self._lo_txn)
	pub = property(lambda self: self._pubKey)

class MoTxn(Txn):

	def __init__(self, blockChain, frm, to, amount):
		"""
			for reasons, calculate the balances
			beforehand and then validate the amount
		"""

		self._amount = float(amount)
		self._frm = frm
		self._to = to

	def sign(self, priv):
		pass
