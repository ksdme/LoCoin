"""
	@author ksdme
	the basic linear block chain model
	doesn't support forks or multiple simul
	taneous transactions
"""
from utils import *
from hashlib import sha1
from app_exceptions import *
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

if __name__ == "__main__":
	genesis = Block("da4b9237bacccdf19c0760cab7aec4a8359010b0", 1, [])
	blockChain = BlockChain([genesis])
	
	firstBlock = Block(blockChain.lastHash(), 4, [])
	#blockChain.addBlock(firstBlock)

	for l in xrange(10000, 1000000):
		if firstBlock.nonceTest(l):
			print "[+] Solved!"
			firstBlock.setNonce(l)
			break
	else:
		print "[+] Not Solved"
		exit()

	blockChain.addBlock(firstBlock)
	blockChain.getBlocks(True)
