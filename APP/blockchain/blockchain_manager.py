import json
import hashlib
import binascii
import pickle
import copy
import threading
from settings import *

class BlockchainManager:

    def __init__(self, genesis_block = None):
        print('Initializing BlockchainManager...')
        self.chain = []
        self.lock = threading.Lock()
        self.__set_my_genesis_block(genesis_block)

    def __set_my_genesis_block(self, block):
        self.genesis_block = block
        self.chain.append(block)

    def set_new_block(self, block):
        with self.lock:
            print("============= set_new_block =============")
            self.chain.append(block)

    def renew_my_blockchain(self, blockchain):
        with self.lock:
            if self.is_valid_chain(blockchain):
                self.chain = blockchain
                latest_block = self.chain[-1]
                return self.get_hash(latest_block)
            else:
                print('invalid chain cannot be set...')
                return None

    def get_my_blockchain(self):
        if len(self.chain) > 1:
            return self.chain
        else:
            return None

    def get_my_chain_length(self):
        return len(self.chain)

    def get_my_Confirmed_block(self):
        if CONFIRMED_BLOCK < len(self.chain):
            print(len(self.chain))
            return self.chain[-CONFIRMED_BLOCK]
        else:
            return self.chain[0]

    def get_transactions_from_orphan_blocks(self, orphan_blocks):
        current_index = 0
        new_transactions = []

        while current_index < len(orphan_blocks):
            block = orphan_blocks[current_index]
            transactions = block['transactions']
            target = self.remove_useless_transaction(transactions)
            current_index += 1
            for t in target:
                new_transactions.append(t)

        return new_transactions


    def remove_useless_transaction(self, transaction_pool):

        if len(transaction_pool) != 0:
            current_index = 1

            while current_index < len(self.chain):
                block = self.chain[current_index]
                transactions = block['transactions']
                for t in transactions:
                    for t2 in transaction_pool:
                        if t == json.dumps(t2, sort_keys=True, ensure_ascii=False):
                            print('already exist in my blockchain :', t2)
                            transaction_pool.remove(t2)

                current_index += 1
            return transaction_pool
        else:
            print('no transaction to be removed...')
            return []

    def resolve_conflicts(self, chain):
        mychain_len = len(self.chain)
        new_chain_len = len(chain)

        pool_4_orphan_blocks = copy.deepcopy(self.chain)
        has_orphan = False

        if new_chain_len > mychain_len:
            for b in pool_4_orphan_blocks:
                for b2 in chain:
                    if b == b2:
                        pool_4_orphan_blocks.remove(b)

            result = self.renew_my_blockchain(chain)
            print(result)
            if result is not None:
                return result, pool_4_orphan_blocks
            else:
                return None, []
        else:
            print('invalid chain cannot be set...')
            return None, []

    def is_valid_block(self, prev_block_hash, block, difficulty=DIF):
        suffix = '0' * difficulty
        block_4_pow = copy.deepcopy(block)
        nonce = block_4_pow['nonce']
        del block_4_pow['nonce']
        print(block_4_pow)

        message = json.dumps(block_4_pow, ensure_ascii=False, sort_keys=True)
        nonce = str(nonce)

        if block['previous_block'] != prev_block_hash:
            print('Invalid block (bad previous_block)')
            print(block['previous_block'])
            print(prev_block_hash)
            return False
        else:
            digest = binascii.hexlify(self._get_double_sha256((message + nonce).encode('utf-8'))).decode('ascii')
            if digest.endswith(suffix):
                print('OK, this seems valid block')
                return True
            else:
                print('Invalid block (bad nonce)')
                print('nonce :' , nonce)
                print('digest :' , digest)
                print('suffix', suffix)
                return False

    def is_valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            if self.is_valid_block(self.get_hash(last_block), block) is not True:
                return False

            last_block = chain[current_index]
            current_index += 1

        return True


    def _get_double_sha256(self,message):
    	return hashlib.sha256(hashlib.sha256(message).digest()).digest()

    def get_hash(self,block):
        print('BlockchainManager: get_hash was called!')
        block_string = json.dumps(block, ensure_ascii=False, sort_keys=True)
        # print("BlockchainManager: block_string", block_string)
        return binascii.hexlify(self._get_double_sha256((block_string).encode('utf-8'))).decode('ascii')
