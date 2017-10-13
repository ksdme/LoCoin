"""
	@author ksdme
	the basic linear block chain model
	doesn't support forks or multiple simul
	taneous transactions
"""
from utils import *
from hashlib import md5
from exceptions import *
from json import dumps, loads
from time import time as timeStamp

class Block(object):

	@staticmethod
	def load(block):
		loaded = loads(block)
		return Block(
			loaded["prev"],
			loaded["difficulty"],
			loaded["txns"],
			loaded["nonce"],
			loaded["time"])

	def __init__(self, prev, difficulty, txns, nonce=None, time=None):
		assert isinstance(txns, list)
		assert isValidHash(prev)

		self._txns = txns
		self._prev = prev
		self._time = int(timeStamp())
		self._nonce = ""
		self._difficulty = int(difficulty)

		if nonce is not None:
			self._nonce = str(nonce)

		if time is not None:
			assert isinstance(time, int)
			self._time = int(time)

		self._block = {
			"at": self._time,
			"prev": self._prev,
			"txns": self._txns,
			"difficulty": self._difficulty
		}

		block_hash = md5(self.json()).hexdigest()
		self._block["hash"] = block_hash
		self._block["nonce"] = self._nonce

	def json(self):
		return dumps(self._block)

	def nonceTest(self, nonce):
		loaded_block = Block.load(self.json())
		difficulty = int(self.raw["difficulty"])

		loaded_block.raw["nonce"] = str(nonce)

		loaded_hash = md5(loaded_block.json()).hexdigest()
		loaded_hash = toString(loaded_hash)

		return str(loaded_hash[:difficulty]).count("0") == difficulty

	raw = property(lambda self: self._block)

class BlockChain(object):

	def __init__(self, blocks):
		assert isinstance(blocks, list)
		assert len(blocks) >= 1

		for block in blocks:
			assert isinstance(block, Block)

		self._blocks = blocks

	def addBlock(self, block):
		assert isinstance(block, Block)

		nonce = block.raw["nonce"]
		if block.nonceTest(nonce):
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

if __name__ == "__main__":
	print Block("d0eedb799584d850fdd802fd3c27ae34", 1, []).json()
