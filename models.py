"""
	@author ksdme
	the basic linear block chain model
	doesn't support forks or multiple simul
	taneous transactions
"""
import rsa
from utils import *
from wallet import *
from hashlib import sha1
from app_exceptions import *
from json import dumps, loads
from time import time as timeStamp
from binascii import unhexlify

class Block(object):

	@staticmethod
	def load(block):
		loaded = loads(block)
		return Block(
			loaded["prev"],
			loaded["difficulty"],
			loaded["txns"],
			loaded["nonce"],
			loaded["at"])

	def __init__(self, prev, difficulty, txns, nonce=None, time=None):
		assert isinstance(txns, list)
		assert isValidHash(prev)

		self._txns = txns
		self._prev = prev
		self._time = int(timeStamp()*1000)
		self._nonce = ""
		self._difficulty = int(difficulty)

		if nonce is not None:
			self._nonce = str(nonce)

		if time is not None:
			assert isinstance(time, int)
			self._time = int(time)

		try:
			self._txns = map(lambda l: l.json(), self._txns)
		except AttributeError:
			self._txns = map(loads, self._txns)

		self._block = {
			"at": self._time,
			"prev": self._prev,
			"txns": self._txns,
			"difficulty": self._difficulty
		}

		block_hash = sha1(self.json()).hexdigest()
		self._block["hash"] = block_hash
		self._block["nonce"] = self._nonce

	def json(self):
		return dumps(self._block)

	def nonceTest(self, nonce, debug=False):
		loaded_block = Block.load(self.json())
		difficulty = int(self.raw["difficulty"])

		loaded_block.raw["nonce"] = str(nonce)

		loaded_hash = sha1(loaded_block.json()).hexdigest()
		if debug: print loaded_hash, str(loaded_hash)[:difficulty+1]

		return str(loaded_hash[:difficulty]).count("0") == difficulty

	def setNonce(self, nonce):
		self._block["nonce"] = str(nonce)

	raw = property(lambda self: self._block)

class BlockChain(object):

	def __init__(self, blocks):
		assert isinstance(blocks, list)
		assert len(blocks) >= 1

		for block in blocks:
			assert isinstance(block, Block)

		self._blocks = map(lambda l: l.json(), blocks)
		self._contains_gen = False

	"""
		#####################################
		Populate this function asap
		#####################################
	"""
	def validateBlockContents(self, contents):
		return True

	def addBlock(self, block):
		assert isinstance(block, Block)
		nonce = block.raw["nonce"]
		flag = True

		# test the nonce
		flag = flag and block.nonceTest(nonce)

		# test that the difficulty is more than or equal
		# to the last difficulty level
		tip_block = self.tip()
		flag = flag and tip_block.raw["difficulty"] <= block.raw["difficulty"]

		for txn in block.raw["txns"]:
			txn = loads(txn)

			# ensure it contains only one gen txn
			if txn["type"] == "mgo" and not self._contains_gen:
				self._contains_gen = True
			elif txn["type"] == "mgo" and self._contains_gen:
				flag = False
				break

		if flag:
			self._blocks.append(block.json())
		else:
			raise BlockRejected()

	def getBlocks(self, prnt=False):
		blocks = []
		for block in self._blocks:
			blocks.append(Block.load(block))

		if prnt:
			for block in blocks:
				print block.json()

		return blocks

	def getBlock(self, block=None, block_hash=None):
		if block is not None:
			assert block < len(self._blocks)
			return Block.load(self._blocks[block])

		else:
			for block in self.getBlocks(False):
				if block.raw["hash"] == block_hash:
					return block

	def tip(self):
		return self.getBlock(-1)

	def head(self):
		return self.getBlock(0)

	def lastHash(self):
		return self.tip().raw["hash"]

	def lastDifficulty(self):
		return self.tip().raw["difficulty"]

	def calculateBalance(self, of):
		balance = 0.0
		for block in self.getBlocks(False):
			for txn in block.raw["txns"]:

				if txn["type"] not in ["mo", "mgo"]:
					continue

				if txn["type"] == "mgo":
					if txn["to"] == of:
						balance += txn["amount"]
					continue

				if txn["from"] != of:
					frm = txn["from"]
					pubKey = Wallet.reconstructPublicKey(frm)

					decrypted = rsa.decrypt(unhexlify(txn["payload"]), pubKey)
					decrypted = loads(decrypted)

					# Ensure the key matches!
					if of == decrypted["to"]:
						balance += float(decrypted["amount"])
				else:
					pubKey = Wallet.reconstructPublicKey(of)
					decrypted = rsa.decrypt(unhexlify(txn["payload"]), pubKey)
					decrypted = loads(decrypted)

					balance -= float(decrypted["amount"])

		return balance

	def getLoHistory(self, identity_private_key):
		for block in self.getBlocks(False):
			for txn in block.raw["txns"]:
				txn = loads(txn)

				if txn["type"] != "lo":
					continue

				identity = rsa.decrypt(unhexlify(txn["identity"]), identity_private_key)

				try:
					identity = loads(identity)
					if identity["ok"] == 200:
						yield txn["loc"], txn["at"]
				except: continue

	def getAllLoc(self):
		for block in self.getBlocks(False):
			for txn in block.raw["txns"]:
				# txn = loads(txns)

				if txn["type"] != "lo":
					continue

				yield txn["loc"], txn["at"]

if __name__ == "__main__":
	from txns import *
	from miner import *
	from wallet import *

	wallet = Identity.loadWallet("sample.wallet")

	genesis = Block("da4b9237bacccdf19c0760cab7aec4a8359010b0", 1, [])
	blockChain, txnPool = BlockChain([genesis]), TxnPool() 

	loTxn = LoTxn("28.535517,77.391029", 1, wallet)
	Miner.fixLoTxn(loTxn)

	txnPool.addToPool(loTxn)

	loTxn = LoTxn("28.535517,77.391030", 1, wallet)
	Miner.fixLoTxn(loTxn)

	txnPool.addToPool(loTxn)

	moTxn = MoGenTxn("tJiPiyR7ggjQaT0O0hgYijgxLYaatam7AZhjFgMg9hgj4iymJuvaMSiahaagzQahgHaN5nCaUiUoHKihlThLaiaTWvjpgj5QiPha5hgjIgPgELHjzigZAj1aOSuHGjphUxT3mJa2UhgjhlhazlgCKgXgjaaimM3hxghuixEaiJ2KhrIahjhEhhh07SnaaaHiyhHh20jjjgjgiUhh3w2ajhjjiIgIuota4Wxivauh0LkIHj6XSMoaz9EimaumzNmaiiaahgVvCoiXjPiX7igStiPaigg3OjKn9Hjihh5ghO9gH8KgigF4jgTzqZHgPgjRghihPqjZlhaJihjYkGMqFgDWnItjagJxVahJghkGhj9h7BiTiiinFhgiLnYig2kRg1hmOsihZaijgOwOhjMh")
	txnPool.addToPool(moTxn)

	Miner.do(blockChain, txnPool)
	blockChain.getBlocks(True)

	for l in blockChain.getAllLoc():
		print l

	moTxn = MoTxn(blockChain, wallet, "kW3giRjTgjihYqLqajKxBFajaBRagNngi4iQKpiOrg0G3jvAyCihhVj5KE9aahhVJOMAlZiUxaaRB1HyjaBgV1EvJtsDhsjvjiaiojaAwgSjoPtjN2l7a3yYaiqg45iDphQjaoC6NMiqahjhxiBjaihmQ2yQpThGghnhnhagAhOkjMjPDaX8OaaCaiiQhMUhlJgj", 5)
	moTxn.sign()
	txnPool.addToPool(moTxn)

	Miner.do(blockChain, txnPool)

	blockChain.getBlocks(True)

	print blockChain.calculateBalance("kW3giRjTgjihYqLqajKxBFajaBRagNngi4iQKpiOrg0G3jvAyCihhVj5KE9aahhVJOMAlZiUxaaRB1HyjaBgV1EvJtsDhsjvjiaiojaAwgSjoPtjN2l7a3yYaiqg45iDphQjaoC6NMiqahjhxiBjaihmQ2yQpThGghnhnhagAhOkjMjPDaX8OaaCaiiQhMUhlJgj")
