import json
from time import time
import hashlib
import binascii
from settings import *
from datetime import datetime

from cross_reference.cross_reference_manager import CrossReferenceManager


class Block:
	def __init__(self, transactions, previous_block_hash, cross_reference, block_num):
		snap_tr = json.dumps(transactions, sort_keys=True, ensure_ascii=False) 

		self.timestamp = time()
		self.transactions = json.loads(snap_tr)
		self.previous_block = previous_block_hash
		self.cross_reference = cross_reference
		self.block_num = block_num

		if self.cross_reference != []:
			print("============= get_cross_reference_pool =============")		
		else:
			print("============= cross_reference_pool_empty =============")

		current = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
		print(current)

		json_block = json.dumps(self.to_dict(include_nonce=False) , sort_keys=True, ensure_ascii=False)
		print('json_block :', json_block)
		self.nonce = self._compute_nonce_for_pow(json_block)

		current2 = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
		print(current2)

	def to_dict(self,include_nonce= True):
		d = {
			'block_num' : self.block_num,
			'timestamp' : self.timestamp,
			'transactions' : [json.dumps(self.transactions[i], sort_keys=True, ensure_ascii=False) for i in range(len(self.transactions))],
			'cross-ref' : self.cross_reference,
			'previous_block': self.previous_block
			# 'previous_cross_ref' : 
		}

		if include_nonce:
			d['nonce'] = self.nonce
		else:
			pass

		return d

	def _compute_nonce_for_pow(self, message, difficulty = DIF):
		i = 0
		suffix = '0' * difficulty
		while True:
			nonce = str(i)
			digest = binascii.hexlify(self._get_double_sha256((message + nonce).encode('utf-8'))).decode('ascii')
			if digest.endswith(suffix):
				return nonce
			i += 1

	def _get_double_sha256(self, message):
		return hashlib.sha256(hashlib.sha256(message).digest()).digest()


class GenesisBlock(Block):

	def __init__(self):
		super().__init__(transactions='AD9B477B42B22CDF18B1335603D07378ACE83561D8398FBFC8DE94196C65D806',
                         previous_block_hash=None, cross_reference = None, block_num = 0 )

	def to_dict(self, include_nonce=True, cross_reference = [], block_num = 0):
		d = {
			'block_num': self.block_num,
			'transactions': self.transactions,
			'genesis_block': True,
			'cross-ref' : cross_reference,
			}
		if include_nonce:
			d['nonce'] = self.nonce
			return d
