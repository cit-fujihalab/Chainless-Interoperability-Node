import plyvel
from glob import glob
import json
import binascii
import hashlib
import os

from settings import DIF


def valid_all(ldb_p):
    db_list = list(glob(ldb_p + "block*.ldb"))
    re_s = []
    for db_name in sorted(db_list):
        db = plyvel.DB(str(db_name), create_if_missing=False)
        for k, v in db:
            val = json.loads(v.decode())
            re_s.append(val)
        if not is_valid_chain(re_s):
            return None
        re_s = re_s[-1:]
    if not re_s:
        return None
    return re_s


# -------------------------------------------------------------------------------------------------------------------------

def is_valid_block(prev_block_hash, block, difficulty=DIF):
    suffix = '0' * difficulty
    nonce = block['nonce']
    del block['nonce']

    message = json.dumps(block, sort_keys=True)
    nonce = str(nonce)

    if block['previous_block'] != prev_block_hash:
        return False
    else:
        digest = binascii.hexlify(_get_double_sha256((message + nonce).encode('utf-8'))).decode('ascii')
        if digest.endswith(suffix):
            # print('OK, this seems valid block')
            block['nonce'] = nonce
            return True
        else:
            return False


def is_valid_chain(chain):
    last_block = chain[0]
    current_index = 1

    while current_index < len(chain):
        block = chain[current_index]
        if not is_valid_block(get_hash(last_block), block):
            return False

        last_block = chain[current_index]
        current_index += 1

    return True


def _get_double_sha256(message):
    return hashlib.sha256(hashlib.sha256(message).digest()).digest()


def get_hash(block):
    block_string = json.dumps(block, sort_keys=True)
    # print("BlockchainManager: block_string", block_string)
    return binascii.hexlify(_get_double_sha256((block_string).encode('utf-8'))).decode('ascii')


if __name__ == "__main__":
    dirname = os.path.dirnama(__file__)
    P = dirname+"/DB/ldb/"


    if valid_all(P):
        print("\nOK ALL !!")
