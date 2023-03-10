import logging
import time
import threading, json
import hashlib

from signature.generate_sigunature import DigitalSignature
from signature.generate_sigunature import CheckDigitalSignature
from p2p.connection_manager_4owner import ConnectionManager4Owner
from p2p.my_protocol_message_handler import MyProtocolMessageHandler
from blockchain.blockchain_manager import BlockchainManager
# from p2p.owner_node_list import OwnerCoreNodeList



class CrossReferenceManager:

	def __init__(self):
		self.gs = DigitalSignature()
		self.cross_reference = []
		self.previous_cross_sig = []
		self.reference = []
		self.lock1 = threading.Lock()
		self.lock2 = threading.Lock()
		self.lock3 = threading.Lock()
		self.lock4 = threading.Lock()
		self.timer1 = 0
		self.flag1 = False
		self.timer2 = 0
		self.flag2 = False
		self.timer3 = 0
		self.flag3 = False
		self.cross_reference_flag = False
		self.inc = 0
		self.ref_block_num = 999
		self.Block_confirmed = None
		self.myblock_in = False
		self.phase1_list = []

	def set_new_cross_reference(self, cross):
		logging.debug("rq == self.lock1-1")
		with self.lock1: 
			logging.debug("self.lock1_ON-set_new_cross_reference ")
			self.reference.append(cross)
			print("======= set_new_cross_ref =======")
		logging.debug("self.lock1_OFF-set_new_cross_reference ==")

	def store_cross_reference(self):
		logging.debug("rq == self.lock1-2")
		with self.lock1:
			logging.debug("self.lock1_ON-store_cross_reference ==")
			print("store_cross_reference")
			self.set_new_cross_reference(self.cross_reference)
		logging.debug("self.lock1_OFF-store_cross_reference ==")

	def clear_my_reference(self):
		with self.lock3:
			self.reference.clear()
			print('reference is now ALL CLEAR ... ', self.reference)

		
	def add_cross_reference(self, cross): 
		logging.debug("rq == self.lock1-3")
		with self.lock1:
			logging.debug("self.lock1_ON-add_cross_reference ==")
			print("add_cross_reference")
			self.cross_reference.append(cross)
		logging.debug("self.lock1_OFF-add_cross_reference ==")
			

	def clear_cross_reference(self):
		logging.debug("rq == self.lock1-4")
		with self.lock1:
			logging.debug("self.lock1_ON-clear_cross_reference ==")
			self.cross_reference.clear()
		print(" ======== reference part clear ======== ",self.cross_reference)
		logging.debug("self.lock1_ON-clear_cross_reference == ")
	
	def get_reference_pool(self):
		logging.debug("rq == self.lock3")
		with self.lock3:
			logging.debug("self.lock3_ON-get_reference_pool")
			if len(self.reference) == 1:
				logging.debug("len(self.reference) == 1")
				return self.reference[0]
				
			elif len(self.reference) > 1:
				logging.debug("len(self.reference) > 1")
				return self.reference[:]
				
			else:
				logging.debug("Currently, it seems cross pool is empty...")
				print("Currently, it seems cross pool is empty...")
				return []
		
	def hysteresis_sig(self):
		logging.debug("rq == self.lock1-5")
		with self.lock1:
			logging.debug("self.lock1_ON-hysteresis_sig")
			Current_C = self.cross_reference
			print("hysteresis_sig is1:",Current_C)
			Current_C.append(self.get_previous_cross_ref())
			print("hysteresis_sig is 2",Current_C)
		msg = Current_C[:]
		# logging.debug(msg)
		msg_pub = self.gs.add_public_key(json.dumps(msg[:]))
		self.store_previous_cross_ref(msg_pub)
		return msg_pub

	def store_previous_cross_ref(self, msg_sig):
		with self.lock2:
			self.previous_cross_sig.clear()
		
		print("clear", len(self.previous_cross_sig))

		msg_hash = self._get_hash_sha256(msg_sig)
		print("store_previous_crossref_hash")
		d = {
			'previous_crossref_hash' : msg_hash
		}
		self.previous_cross_sig.append(d)
		# r = self.previous_cross_sig[0] # .get('previous_crossref_hash')
		print("======= renew prev_crossref_hash  ... ======= ",self.previous_cross_sig)

		if len(self.previous_cross_sig) == 1:
			print("store_previous_cross_ref")
		
		elif len(self.previous_cross_sig) > 1 :
			print("ERR")

		else :
			print("ERR")
			pass


	def _get_hash_sha256(self, message):
		return hashlib.sha256(message.encode()).hexdigest()

	def get_previous_cross_ref(self):
		print("get_previous_cross_sig")
		if len(self.previous_cross_sig) == 1:
			msg_sig = self.previous_cross_sig[0]
			return msg_sig
		else:
			print("Currently, it seems previous_cross_sig is empty or ERR...")
			d = {
				'previous_crossref_hash' : {}
			}
			return d

	def time_start_phase1(self):
		print("================= time_start_phase1 =================")
		self.flag1 = True
		self.timer1 =  time.perf_counter()
	
	def time_stop_phase1(self):
		if self.flag1:
			t = time.perf_counter()- self.timer1
			self.flag1 = False
			return t
		else:
			return None

	def time_start_phase2(self):
		self.flag2 = True
		self.timer2 =  time.perf_counter()
	
	def time_stop_phase2(self):
		if self.flag2:
			t = time.perf_counter()- self.timer2
			self.flag2 = False
			return t
		else:
			return None


	def ref_block_number(self,num):
		self.ref_block_num = num + 2
		print("##########################",self.ref_block_num)

	def check_ref_block_num(self):
		return self.ref_block_num

	def block_cheek(self):
		self.cross_reference_flag = False

	def block_ref(self): #
		return self.Block_confirmed

	def renew_block_ref(self,block):
		self.Block_confirmed = block
