import time
import socket, threading, json
import copy
from time import sleep
import numpy as np
import hashlib
import logging
import datetime
from datetime import datetime, timedelta
import tkinter as tk
from settings import *

from signature.generate_sigunature import DigitalSignature
from signature.generate_sigunature import CheckDigitalSignature
from blockchain.blockchain_manager import BlockchainManager
from window.generate_window import MainWindow
from p2p.connection_manager_4owner import ConnectionManager4Owner
from p2p.my_protocol_message_handler import MyProtocolMessageHandler
from p2p.owner_node_list import OwnerCoreNodeList
from p2p.message_manager import (
	MSG_REQUEST_CROSS_REFERENCE,
	MSG_ACCEPT_CROSS_REFFERENCE,
	LEADER_AGGREGATION_START_CROSS_REFFERENCE,
	MSG_CROSS_REFFERENCE_LEADER_AGGREGATION,
	REQUEST_POW,
	MSG_CROSS_REFFERENCE,
	START_CROSS_REFFERENCE,
	COMPLETE_CROSS_REFERENCE,
	RAFT_CANDIDATE_LEADER,
	U_RAFT_FOLLOWER,
	IM_RAFT_LEADER,
	RAFT_HEARTBEAT
)

from cross_reference.cross_reference_manager import CrossReferenceManager
# from cross_reference.cross_reference_resistance import CrossReferenceResistance

STATE_INIT = 0
STATE_STANDBY = 1
STATE_CONNECTED_TO_NETWORK = 2
STATE_SHUTTING_DOWN = 3

class OwnerCore(object):

	def __init__(self, my_port = 50082, owner_node_host=None, owner_node_port=None  ):
		self.server_state = STATE_INIT
		print('Initializing owner server...')
		self.my_ip = self.__get_myip()
		print('Server IP address is set to ... ', self.my_ip)
		self.my_port = my_port
		self.cm = ConnectionManager4Owner(self.my_ip, self.my_port, self.__handle_message, self )
		self.mpmh = MyProtocolMessageHandler()
		self.owner_node_host = owner_node_host
		self.owner_node_port = owner_node_port
		self.gs = DigitalSignature()
		self.ww = MainWindow(self.my_port)
		self.bmc = BlockchainManager()
		self.create_log()
		self.tkinter_state = tkinter_state #tkinter
		self.Raft_initial()
		self.CR_initial()
		self.Experiment_initial()
		logging.debug('debug_msg : END __init__')

	def CR_initial(self):
		self.CR_Last_stamp = time.time()
		self.AC = 0
		self.Accept_list = [] #Accept Count
		self.Ccount = 0 
		self.Send_list = []
		self.REcount = 0
		self.RE_Send_list = []
		self.check_count = None
		self.previous_cross_sig = []
		self.CR_INTERVAL = CR_INTERVAL
		self.CR_state = CR_STATE
		logging.debug('debug_msg : END CR_initial')

	def Raft_initial(self):
		self.Raft_Voting = 0
		self.Voting_Result = []
		self.Candidate = False
		self.Raft_timer = 0		
		self.CR_count = 0
		self.Raft_Leader_state = None
		self.Raft_Voting_state = False
		self.Leader_C = 0
		self.Lastping_leader = 0 
		self.Last_Heartbeat_time()
		logging.debug('debug_msg : END Raft_initial')

	def Experiment_initial(self):
		self.Phase1_list = []
		self.Phase3_list = []
		self.overtime_c = 0
		self.overtime_flag = False
		logging.debug('debug_msg : END CR_Experiment_initial')

	def start(self, crm = None):
		self.server_state = STATE_STANDBY
		self.cm.start()
		self.crm = crm
		self.Raft_Leader_state = True#if
		self.Raft_Leader_loop()

	def window(self):
		if tkinter_state == True:
			self.ww.generate_genesis_window()

		else:
			logging.debug('debug_msg : Tkinter off')
			pass

	def create_log(self):
		try:
			file_name = "logging/raft_status" + str(self.my_port) + ".log"
			formatter = '%(asctime)s: %(message)s'
			logging.basicConfig(format=formatter, filename= file_name, level = logging.INFO)
			
		except:
			file_name = "APP/logging/raft_status" + str(self.my_port) + ".log"
			formatter = '%(asctime)s: %(message)s'
			logging.basicConfig(format=formatter, filename= file_name, level = logging.INFO)



	def join_DMnetwork(self):
		logging.info('debug_msg : join_DMnetwork')
		if self.owner_node_host != None:
			logging.info('debug_msg : join_DMnetwork')
		
			self.server_state = STATE_CONNECTED_TO_NETWORK
			self.cm.join_DMnetwork(self.owner_node_host, self.owner_node_port)
			self.Raft_Leader_state = False
			logging.debug('Raft_Leader_state:' + str(self.Raft_Leader_state))
			self.Raft_Follower_loop()

		else:
			print('This server is running as Genesis Owner Node...')
			logging.info('This server is running as Genesis Owner Node...')
			self.Raft_Leader_state = True
			self.Raft_Leader_loop()

	def Last_Heartbeat_time(self):
		print("Last_Heartbeat_time")
		self.Last_Heartbeat = time.time()
		print("Last_Heartbeat is ",self.Last_Heartbeat)
		print(datetime.fromtimestamp(self.Last_Heartbeat))

	def Time_judge_is_Follower(self):
		self.Follower_time = time.time()
		if  self.Follower_time < self.Last_Heartbeat + ALLOWABLE_TIME:
			print("Renew_Last_Heartbeat", float(self.Last_Heartbeat + ALLOWABLE_TIME ))
			print("Last_Heartbeat",self.Last_Heartbeat)
			print("self.Raft_Voting_state", self.Raft_Voting_state)
			self.Raft_Follower_side = threading.Timer(LEADER_CHECK_INTERVAL, self.Time_judge_is_Follower)
			self.Raft_Follower_side.start()

		else:
			print("Renew_Last_Heartbeat", float(self.Last_Heartbeat + ALLOWABLE_TIME))
			print("Last_Heartbeat", self.Last_Heartbeat)
			print("Follower_time is ", self.Follower_time)
			logging.info('debug_msg : Candidate')
			print("self.Raft_Voting_state", self.Raft_Voting_state)
			self.Raft_Candidate_Leader()

	def shutdown(self):
		self.server_state = STATE_SHUTTING_DOWN
		print('Shutdown server...')
		self.cm.connection_close()

	def Raft_Follower_loop(self):
		logging.info('debug_msg : Follower_loop')
		print("000000000000000000000000Follower_loop000000000000000000000000")
		self.Time_judge_is_Follower()
		
	def Raft_Leader_loop(self):
		CR_stamp = time.time()
		logging.info('1111111111111111111111111Leader_loop1111111111111111111111111')
		print("1111111111111111111111111Leader_loop1111111111111111111111111")
		if self.ww.Break_state == True:
			self.Leader_broken()

		else:
			self.Leader_loop = threading.Timer(LEADER_UPDATE_INTERVAL, self.Raft_timer_for_Leader)
			self.Leader_loop.start()

		logging.debug("CR_check_stamp" + str(CR_stamp))
		logging.debug("self.CR_Last_stamp" + str(self.CR_Last_stamp))

		if CR_INTERVAL < CR_stamp - self.CR_Last_stamp :
			logging.info("CR_loop")
			self.CR_loop()

		else :
			logging.info("Last consensus is" + str(CR_INTERVAL))

	def Leader_broken(self):
		logging.debug('break down. sleep(10000000)' + str(self.my_port))
		while True:
			sleep(5)
			if self.ww.Break_state == False:
				self.Raft_Leader_state = False
				self.Raft_Follower_loop()

	def Raft_reset(self):
		self.Voting_Result = []
		self.Raft_Voting = 0
		self.Candidate = False
		self.Raft_Voting_state = False
		self.Leader_C = 0
		
	def Send_heartbeat(self):
		logging.info("Send_heartbeat")
		if self.Raft_Leader_state == True:
			self.Lastping_leader = time.time()

		else :
			logging.debug('Not a leader...')

	def Raft_timer_for_Leader(self):
		RenewLastping_Leader = time.time()
		if self.Raft_Leader_state == True:
			if RenewLastping_Leader - self.Lastping_leader > 5:
				new_message = self.cm.get_message_text(RAFT_HEARTBEAT)
				self.cm.send_msg_to_all_owner_peer(new_message)
				logging.info("Continuation of leadership" + str(self.my_ip) + "," + str(self.my_port))
				print("Continuation of leadership")			
				self.Raft_Leader_loop()

			else:
				print("Last ping within 5 s")
				logging.info('Last ping within 5 s')
				self.Raft_Leader_loop()

		else :
			print("Leader rights are gone. Or voting mode")
			logging.debug('Leader rights are gone. Or voting mode')

	def Raft_Candidate_Leader(self):
		logging.debug('candidate for leader' + str(self.my_ip) + "," + str(self.my_port))
		print("candidate for leader")
		if self.Raft_Voting_state == True:
			print("voting mode.")
			self.Candidate = False
			logging('voting mode.')
			print("Follower")
			self.Raft_Follower_loop()

		else:
			self.Raft_Voting_state = True
			print("voting mode.")
			new_message = self.cm.get_message_text(RAFT_CANDIDATE_LEADER)
			self.cm.send_msg_to_all_owner_peer(new_message)
			logging.debug('RAFT_CANDIDATE_LEADER')

	def CR_loop(self):
		logging.info('CR_loop')
		n = self.crm.ref_block_number
		logging.info("block num : " + str(n))
		if self.CR_state == True:
			if self.cm.adding_timer + NEW_CONNECTION < time.time():
				self.CR_Last_stamp = time.time()
				if len(self.cm.owner_node_set.get_list()) > MINIMUM_DOMAIN:
					self.CR_count += 1
					self.request_cross_reference()
					logging.debug(str(self.CR_count))
					
				else:
					logging.debug(str(len(self.cm.owner_node_set.get_list())))
					
			else:
				logging.debug("New connection is" + str(NEW_CONNECTION) + "s") 
				print("")

		else:
			print("Not making an consensus for a reason.")
			logging('Not making an consensus for a reason.')

#-----------------------------------------------------------------------------------------------------------------------------------------
	def request_cross_reference(self):
		self.crm.time_start_phase1()
		self.check_count = 11
		print(" ============= Phase1 start =============")
		self.crm.inc += 1
		print("start_request_cross_reference")
		self.Send_heartbeat()
		if LEADER_AGGREGATION == True:
			self.cross_reference_reset()
		new_message = self.cm.get_message_text(MSG_REQUEST_CROSS_REFERENCE)
		self.cm.send_msg_to_all_owner_peer(new_message)

	def start_cross_reference(self):
		print("start_request_crose_reference")
		block_l = json.dumps(self.crm.block_ref())
		block_msg = self._get_hash_sha256(block_l)
		self.crm.add_cross_reference(block_msg)
		self.crm.myblock_in = True
		new_message = self.cm.get_message_text(MSG_CROSS_REFFERENCE, json.dumps(block_msg, sort_keys = True ,ensure_ascii = False))
		print("============= start_request_crose_reference =============")
		logging.info("============= start_request_crose_reference =============")
		self.Send_heartbeat()
		self.cm.send_msg_to_all_owner_peer(new_message)

	def current_crossref(self, msg):
		self.crm.add_cross_reference(msg)

	def cross_sig(self, cre):
		cross_sig = self.gs.add_public_key(cre)
		return cross_sig

	def _get_hash_sha256(self, message):
		return hashlib.sha256(message.encode()).hexdigest()

	def complete_cross_block(self, msg):
		logging.info("complete_cross_block()")
		if LEADER_AGGREGATION == True:
			new_message = self.cm.get_message_text(COMPLETE_CROSS_REFERENCE, msg)
			self.Send_heartbeat()
			self.cm.send_msg_to_all_owner_peer(new_message)
			
		else:
			self.cross_reference_reset()
			new_message = self.cm.get_message_text(COMPLETE_CROSS_REFERENCE, msg)
			self.Send_heartbeat()
			self.cm.send_msg_to_all_owner_peer(new_message)
		
	def cross_reference_reset(self):
		print("cross_reference_ALL RESET")
		print("refresh crossre ference pool")
		self.crm.clear_cross_reference()
		print( "refresh crossre ference pool")
		logging.debug("clear self.crm.cross_reference is" + str(self.crm.cross_reference))
		self.AC = 0 # Reset
		self.Ccount = 0
		self.REcount = 0
		# self.crm.flag = False
		self.crm.myblock_in = False
		logging.info("cross_reference_reset is ok----Full-Reset")
		print("ok----Full-Reset")


	def myblock_in_check(self):
		logging.debug("myblock_in_check")
		if self.crm.myblock_in == True: 
			msg = self.crm.hysteresis_sig()
			self.crm.set_new_cross_reference(msg)
			print(" ============= Phase2 start =============")
			logging.debug("myblock_in_check")
			if LEADER_AGGREGATION == True:
				self.cross_reference_reset()
				new_message = self.cm.get_message_text(REQUEST_POW, msg)
				self.Send_heartbeat()
				self.cm.send_msg_to_all_owner_peer(new_message)
				
			else:
				complete = threading.Timer(30, self.complete_cross_block(msg))
				complete.start()
				return 0

		else:
			recheck = threading.Timer(REF_RECHECK, self.myblock_in_check)
			recheck.start()	
			return 1

	def __handle_message(self, msg, is_owner, peer=None):
		if self.ww.Break_state == True:
			logging.debug("break down")
			pass

		elif msg[2] == MSG_REQUEST_CROSS_REFERENCE:
			self.crm.time_start_phase1()
			self.cross_reference_reset()
			print("cross_reference_ALL RESET")
			print("refresh crossre ference pool")
			logging.debug('MSG_REQUEST_CROSS_REFERENCE:')
			print("MSG_REQUEST_CROSS_REFERENCE:")
			new_message = self.cm.get_message_text(MSG_ACCEPT_CROSS_REFFERENCE)
			self.cm.send_msg(peer, new_message, delay = False) 

		elif msg[2] == MSG_ACCEPT_CROSS_REFFERENCE: 
			logging.debug('MSG_ACCEPT_CROSS_REFFERENCE')
			print("MSG_ACCEPT_CROSS_REFFERENCE")
			print("self.o_list.get_list = ", self.cm.owner_node_set.get_list())

			if self.AC == 0:
				self.AC = 1
				self.Accept_list = copy.deepcopy(self.cm.owner_node_set.get_list())
				if peer in self.Accept_list:
					self.Accept_list.remove(peer)
			elif self.AC >= 1:
				if peer in self.Accept_list:
					self.Accept_list.remove(peer)
			else:
				pass

			if len(self.Accept_list) == 1: #Accept Count
				print("ok----------------------------ACCEPT_CROSS_REFERENCE")
				print("SEND_START")
				self.check_count = 22

				if LEADER_AGGREGATION == True:
					block_l = json.dumps(self.crm.block_ref())
					block_msg_M = self._get_hash_sha256(block_l)
					c = self.gs.compute_digital_signature(block_msg_M)
					logging.debug('self.gs.get_private_key' + str(c))
					logging.debug('block_msg' + str(block_l))
					msg_d = {
						c + "__PORT(" + str(self.my_port) + ")":block_msg_M + "__(Block_Hash)"
					}
					logging.debug("block_hash" + str(msg_d))
					self.current_crossref(msg_d)
					
					logging.debug("self.crm.cross_reference is :" + str(self.crm.cross_reference))
					
					new_message = self.cm.get_message_text(LEADER_AGGREGATION_START_CROSS_REFFERENCE)
					self.cm.send_msg_to_all_owner_peer(new_message)
					self.Send_heartbeat()
					
				else:
					new_message = self.cm.get_message_text(START_CROSS_REFFERENCE)
					self.cm.send_msg_to_all_owner_peer(new_message)
					self.Send_heartbeat()
					print("accept next")
					self.start_cross_reference()

		elif msg[2] == START_CROSS_REFFERENCE: 
			logging.info(START_CROSS_REFFERENCE)
			print("START_CROSS_REFFERENCE")
			if LEADER_AGGREGATION == False:
				self.start_cross_reference()

			else:
				logging.debug("Modes in which failing leaders aggregate")

		elif msg[2] == MSG_CROSS_REFFERENCE_LEADER_AGGREGATION: 
			logging.info('MSG_CROSS_REFFERENCE_LEADER_AGGREGATION @' + str(peer))

			msg_loads = json.loads(msg[4])

			print("HASH:" ,msg_loads)	

			if self.Ccount == 0:
				self.Ccount = 1
				self.Send_list = copy.deepcopy(self.cm.owner_node_set.get_list())
				logging.debug("sendlist is" + str(self.Send_list))
				
				if peer in self.Send_list:
					self.Send_list.remove(peer)
					self.current_crossref(msg_loads)
					logging.critical("A-1")
				else:
					logging.critical("A-2")
					pass
			elif self.Ccount >= 1:
				if peer in self.Send_list:
					self.Send_list.remove(peer)
					self.current_crossref(msg_loads)
					logging.critical("B-1")
				else:
					logging.critical("B-2")
					pass
			else:
				logging.critical("C")
				pass

			if len(self.Send_list) == 1:
				logging.debug("CROSS_REFERENCE_ACCEPT_ALL_NODE")
				msg = self.crm.hysteresis_sig()
				logging.debug("msg is :" + str(type(msg)))
				self.crm.set_new_cross_reference(msg)
				print("self.reference", self.crm.reference)
				print("============== type ==============" + str(type(self.crm.reference)))
				logging.debug("self.reference" + str(self.crm.reference))
				logging.debug("======= type =======" + str(type(self.crm.reference)))
				block_msg_C = self.crm.get_reference_pool()
				print("block_msg_C", block_msg_C)
				print("block_msg_C", type(block_msg_C))
				logging.debug("block_msg_C" + str(block_msg_C))
				logging.debug("======= type =======" + str(type(block_msg_C)))
				new_message = self.cm.get_message_text(REQUEST_POW, json.dumps(block_msg_C, sort_keys = True ,ensure_ascii = False))
				logging.info("REQUEST_POW")
				self.cm.send_msg_to_all_owner_peer(new_message)
				print("============= self.crm.time_stop_phase1() =============")
				phase1_time = self.crm.time_stop_phase1()
				self.crm.phase1_list.append(phase1_time)
				print("self.crm.Phase1_list", self.crm.phase1_list)
				print(" ============= Phase2 start =============")
				
		elif msg[2] == REQUEST_POW:
			print("REQUEST_POW")
			logging.debug("REQUEST_POW == msg[4] ==" + str(type(msg[4])))
			msg_loads = json.loads(msg[4])
			logging.debug("msg_loads is " + str( msg_loads))
			logging.debug("msg_loads is type is" + str(type(msg_loads)))
			self.crm.cross_reference = eval(msg_loads)
			msg = self.crm.hysteresis_sig()
			logging.debug("=================== msg is =================== 1 : " + str(msg))			
			self.crm.set_new_cross_reference(msg)
			# print("msg is : " + str(type(msg)))
			phase1_time = self.crm.time_stop_phase1()
			self.crm.phase1_list.append(phase1_time)
			print("phase1 time is :", phase1_time)
			logging.debug("=================== msg is =================== 1: " + str(type(msg)))
			print(" ============= Phase2 start ============= ")
			logging.info(" ============= Phase2 start ============= ")

			
		elif msg[2] == LEADER_AGGREGATION_START_CROSS_REFFERENCE:
			logging.debug('LEADER_AGGREGATION_START_CROSS_REFFERENCE @' + str(peer)) # @LEADER
			print("start_crose_reference")
			block_l = json.dumps(self.crm.block_ref())
			block_msg = self._get_hash_sha256(block_l)
			self.crm.myblock_in = True
			c = self.gs.compute_digital_signature(block_msg)
			logging.debug('block_msg' + str(block_l))
			msg_d = {
				c + "__PORT(" + str(self.my_port) + ")":block_msg + "__(Block_Hash)"
			}
			logging.debug("block_hash" + str(msg_d))
			new_message = self.cm.get_message_text(MSG_CROSS_REFFERENCE_LEADER_AGGREGATION, json.dumps(msg_d, sort_keys = True ,ensure_ascii = False))
			print("============= start_cross_reference__Leader_aggregation =============")
			logging.info("============= start_cross_reference__Leader_aggregation =============")
			self.cm.send_msg(peer ,new_message, delay = False)
			logging.info("MSG_CROSS_REFFERENCE_LEADER_AGGREGATION")
			self.Send_heartbeat

		elif msg[2] == MSG_CROSS_REFFERENCE:
			logging.debug('MSG_CROSS_REFFERENCE @' + str(peer))
			print("received : MSG_CROSS_REFFERENCE")
			print("Phase1-1")
			msg_loads = json.loads(msg[4])

			print("HASH:" ,msg_loads)	

			if self.Ccount == 0:
				self.Ccount = 1
				self.Send_list = copy.deepcopy(self.cm.owner_node_set.get_list())
				logging.debug("sendlist is" + str(self.Send_list))
				
				if peer in self.Send_list:
					self.Send_list.remove(peer)
					self.current_crossref(msg_loads)
					logging.critical("A-1")
				else:
					logging.critical("A-2")
					pass
			elif self.Ccount >= 1:
				if peer in self.Send_list:
					self.Send_list.remove(peer)
					self.current_crossref(msg_loads)
					logging.critical("B-1")
				else:
					logging.critical("B-2")
					pass
			else:
				logging.critical("C")
				pass

			if len(self.Send_list) == 1:
				logging.debug("CROSS_REFERENCE_ACCEPT_ALL_NODE")
				check = self.myblock_in_check() 
				logging.debug("block-check-while" + str(check))
				if check == 0:
					logging.debug("block-check" + str(check))
				
				else:
					logging.debug("block-check" + str(check))

		elif msg[2] == COMPLETE_CROSS_REFERENCE:
			print(" ==== OK ==== COMPLETE_CROSS_REFERENCE ==== ")
			logging.debug(" ==== OK ==== COMPLETE_CROSS_REFERENCE ==== ")

#------------------------------ Raft --------------------------------------------------
		elif msg[2] == RAFT_CANDIDATE_LEADER: 
			self.Last_Heartbeat_time() 
			print("msg[2] == Raft_My_Leader")
			logging.debug(str(peer) + "RAFT_CANDIDATE_LEAADER")

			if self.Raft_Voting == 0:
				self.Raft_Voting_state = True
				self.Raft_Voting = +1 
				new_message = self.cm.get_message_text(U_RAFT_FOLLOWER)
				self.cm.send_msg(peer,new_message, delay = False)
			
			else:
				print("Denial")
				logging.debug("")

		elif msg[2] == U_RAFT_FOLLOWER:
			self.Voting_Result.append(peer) 
			B = len(self.Voting_Result)
			A = copy.deepcopy(self.cm.owner_node_set.get_list())
			if len(A)/2 <= B:
				self.Raft_Leader_state = True
	
				new_message = self.cm.get_message_text(IM_RAFT_LEADER) 
				self.cm.send_msg_to_all_owner_peer(new_message) 

				self.Raft_reset_timer = threading.Timer(60, self.Raft_reset)
				self.Raft_reset_timer.start()
				self.Raft_Leader_loop()

			else:
				print(" ")
				logging.debug(" ")

		elif msg[2] == IM_RAFT_LEADER:
			self.Last_Heartbeat_time()
			self.Raft_Leader_state = False
			print("Re new leader is", peer)
			self.Raft_Leader = peer
			logging.debug("IM_RAFT_LEADE :Raft_Voting_state is)" + str(self.Raft_Voting_state))

			self.Raft_Leader_state = False
			self.Raft_reset()
			self.Raft_Follower_loop()
			
		elif msg[2] == RAFT_HEARTBEAT:
			self.Last_Heartbeat_time()

	def __get_myip(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('8.8.8.8', 80))
		return s.getsockname()[0]

