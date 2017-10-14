"""
	@author ksdme
	miner for clearing the
	blockchain periodically
"""
from models import *
from app_exceptions import *

class Miner(object):

	@staticmethod
	def do(blockChain, txnpool, startfrom=1000, ends=10000000):
		pool = list(txnpool.select())

		for txn in pool:
			if not txn.valid():
				pool.remove(txn)

		# create new block, mine it and do stuff
		block = Block(blockChain.lastHash(), blockChain.lastDifficulty()+1, pool)

		# test all
		for l in xrange(startfrom, ends+1):
			if block.nonceTest(l):
				block.setNonce(l)
				blockChain.addBlock(block)
				print "[!] Added Block: {}".format(block.raw["hash"])
				break

	@staticmethod
	def fixLoTxn(txn, startfrom=1000, ends=10000000):
		for l in xrange(startfrom, ends):
			if txn.nonceTest(l):
				txn.setNonce(l)
				print "[!] Solved LoTxn: {}".format(txn.raw["hash"])
				break
