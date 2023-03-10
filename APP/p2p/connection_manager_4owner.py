import socket
import threading
import pickle

from concurrent.futures import ThreadPoolExecutor
from websocket_server import WebsocketServer
from websocket import create_connection
import time
import sys

from .owner_node_list import OwnerCoreNodeList
from .message_manager import (
	MessageManager,
	MSG_ADD_AS_OWNER,
	MSG_REMOVE_AS_OWNER,
	MSG_OWNER_LIST,
	MSG_REQUEST_OWNER_LIST,
	MSG_PING,
	ERR_PROTOCOL_UNMATCH,
	ERR_VERSION_UNMATCH,
	OK_WITH_PAYLOAD,
	OK_WITHOUT_PAYLOAD,

)
from time import sleep

PING_INTERVAL = 10
TIME_OUT = 60


class ConnectionManager4Owner:

	def __init__(self, host,  my_port, callback, sc_self=None ):
		print('Initializing ConnectionManager...')#####
		self.host = host
		self.port = my_port
		self.my_o_host = None
		self.my_o_port = None
		self.owner_node_set = OwnerCoreNodeList()
		self.last_ping = {}	##
		self.__add_peer((host, my_port))
		self.mm = MessageManager()
		self.callback = callback
		self.my_host = self.__get_myip()##
		self.ws = WebsocketServer(port = my_port, host = self.my_host)##
		
		self.sc_self = sc_self ##
		self.flag = 0 ##
		self.adding_timer = 0## 

		#---------------------------------------------------50050
		if 50050 <= self.port:
			print("This Domain in Barcelona" , self.port)
			bpsBarcelona = { # 50050
				50050 : 100, 
				50052 : 100, 
				50054 : 100, 
				50056 : 100, 
				50058 : 100, 
				#--------------------------------------------
				50060 : 2779.949613413, # Byte for Paris
				50062 : 2779.949613413, # Byte for Paris
				50064 : 2779.949613413, # Byte for Paris
				50066 : 2779.949613413, # Byte for Paris
				50068 : 2779.949613413, # Byte for Paris
				#--------------------------------------------
				50070 : 265.143198041, # Byte for Tokyo
				50072 : 265.143198041, # Byte for Tokyo
				50074 : 265.143198041, # Byte for Tokyo
				50076 : 265.143198041, # Byte for Tokyo
				50078 : 265.143198041, # Byte for Tokyo
				#--------------------------------------------
				50080 : 542.713226939, # Byte for Toronto
				50082 : 542.713226939, # Byte for Toronto
				50084 : 542.713226939, # Byte for Toronto
				50086 : 542.713226939, # Byte for Toronto
				50088 : 542.713226939, # Byte for Toronto
				#--------------------------------------------
				50090 : 669.876491522, # Byte for Washinton
				50092 : 669.876491522, # Byte for Washinton
				50094 : 669.876491522, # Byte for Washinton
				50096 : 669.876491522, # Byte for Washinton
				50098 : 669.876491522, # Byte for Washinton
				#--------------------------------------------
				50100 : 100, 
				50102 : 100, 
				50104 : 100, 
				50106 : 100, 
				50108 : 100, 
				#--------------------------------------------
				50110 : 2779.949613413, # Byte for Paris
				50112 : 2779.949613413, # Byte for Paris
				50114 : 2779.949613413, # Byte for Paris
				50116 : 2779.949613413, # Byte for Paris
				50118 : 2779.949613413, # Byte for Paris
				#--------------------------------------------
				50120 : 265.143198041, # Byte for Tokyo
				50122 : 265.143198041, # Byte for Tokyo
				50124 : 265.143198041, # Byte for Tokyo
				50126 : 265.143198041, # Byte for Tokyo
				50128 : 265.143198041, # Byte for Tokyo
				#--------------------------------------------
				50130 : 542.713226939, # Byte for Toronto
				50132 : 542.713226939, # Byte for Toronto
				50134 : 542.713226939, # Byte for Toronto
				50136 : 542.713226939, # Byte for Toronto
				50138 : 542.713226939, # Byte for Toronto
				#--------------------------------------------
				50130 : 669.876491522, # Byte for Washinton
				50132 : 669.876491522, # Byte for Washinton
				50134 : 669.876491522, # Byte for Washinton
				50136 : 669.876491522, # Byte for Washinton
				50138 : 669.876491522, # Byte for Washinton
				#--------------------------------------------
				50140 : 100, 
				50142 : 100, 
				50144 : 100, 
				50146 : 100, 
				50148 : 100, 
				#--------------------------------------------
				50150 : 2779.949613413, # Byte for Paris
				50152 : 2779.949613413, # Byte for Paris
				50154 : 2779.949613413, # Byte for Paris
				50156 : 2779.949613413, # Byte for Paris
				50158 : 2779.949613413, # Byte for Paris
				#--------------------------------------------
				50160 : 265.143198041, # Byte for Tokyo
				50162 : 265.143198041, # Byte for Tokyo
				50164 : 265.143198041, # Byte for Tokyo
				50166 : 265.143198041, # Byte for Tokyo
				50168 : 265.143198041, # Byte for Tokyo
				#--------------------------------------------
				50170 : 542.713226939, # Byte for Toronto
				50172 : 542.713226939, # Byte for Toronto
				50174 : 542.713226939, # Byte for Toronto
				50176 : 542.713226939, # Byte for Toronto
				50178 : 542.713226939, # Byte for Toronto
				#--------------------------------------------
				50180 : 669.876491522, # Byte for Washinton
				50182 : 669.876491522, # Byte for Washinton
				50184 : 669.876491522, # Byte for Washinton
				50186 : 669.876491522, # Byte for Washinton
				50188 : 669.876491522, # Byte for Washinton
				#--------------------------------------------
				50190 : 669.876491522, # Byte for Washinton
				50192 : 669.876491522, # Byte for Washinton
				50194 : 669.876491522, # Byte for Washinton
				50196 : 669.876491522, # Byte for Washinton
				50198 : 669.876491522, # Byte for Washinton
				#--------------------------------------------
				50200 : 669.876491522, # Byte for Washinton
				50202 : 669.876491522, # Byte for Washinton
				50204 : 669.876491522, # Byte for Washinton
				50206 : 669.876491522, # Byte for Washinton
				50208 : 669.876491522, # Byte for Washinton
				#--------------------------------------------
				50210 : 669.876491522, # Byte for Washinton
				50212 : 669.876491522, # Byte for Washinton
				50214 : 669.876491522, # Byte for Washinton
				50216 : 669.876491522, # Byte for Washinton
				50218 : 669.876491522, # Byte for Washinton
				#--------------------------------------------
				50220 : 669.876491522, # Byte for Washinton
				50222 : 669.876491522, # Byte for Washinton
				50224 : 669.876491522, # Byte for Washinton
				50226 : 669.876491522, # Byte for Washinton
				50228 : 669.876491522, # Byte for Washinton
				#--------------------------------------------
				50230 : 669.876491522, # Byte for Washinton
				50232 : 669.876491522, # Byte for Washinton
				50234 : 669.876491522, # Byte for Washinton
				50236 : 669.876491522, # Byte for Washinton
				50238 : 669.876491522, # Byte for Washinton
				#--------------------------------------------
				50240 : 669.876491522, # Byte for Washinton
				50242 : 669.876491522, # Byte for Washinton
				50244 : 669.876491522, # Byte for Washinton
				50246 : 669.876491522, # Byte for Washinton
				50248 : 669.876491522, # Byte for Washinton
				#--------------------------------------------
				50250 : 669.876491522, # Byte for Washinton
				50252 : 669.876491522, # Byte for Washinton
				50254 : 669.876491522, # Byte for Washinton
				50256 : 669.876491522, # Byte for Washinton
				50258 : 669.876491522, # Byte for Washinton
				#--------------------------------------------
				50260 : 669.876491522, # Byte for Washinton
				50262 : 669.876491522, # Byte for Washinton
				50264 : 669.876491522, # Byte for Washinton
				50266 : 669.876491522, # Byte for Washinton
				50268 : 669.876491522, # Byte for Washinton
				#--------------------------------------------
				50270 : 669.876491522, # Byte for Washinton
				50272 : 669.876491522, # Byte for Washinton
				50274 : 669.876491522, # Byte for Washinton
				50276 : 669.876491522, # Byte for Washinton
				50278 : 669.876491522, # Byte for Washinton
				#--------------------------------------------
				50280 : 669.876491522, # Byte for Washinton
				50282 : 669.876491522, # Byte for Washinton
				50284 : 669.876491522, # Byte for Washinton
				50286 : 669.876491522, # Byte for Washinton
				50288 : 669.876491522, # Byte for Washinton
				#--------------------------------------------
				50290 : 669.876491522, # Byte for Washinton
				50292 : 669.876491522, # Byte for Washinton
				50294 : 669.876491522, # Byte for Washinton
				50296 : 669.876491522, # Byte for Washinton
				50298 : 669.876491522, # Byte for Washinton
				#--------------------------------------------
				50300 : 669.876491522, # Byte for Washinton
				50302 : 669.876491522, # Byte for Washinton
				50304 : 669.876491522, # Byte for Washinton
				50306 : 669.876491522, # Byte for Washinton
				50308 : 669.876491522, # Byte for Washinton
				#--------------------------------------------
				50310 : 669.876491522, # Byte for Washinton
				50312 : 669.876491522, # Byte for Washinton
				50314 : 669.876491522, # Byte for Washinton
				50316 : 669.876491522, # Byte for Washinton
				50318 : 669.876491522, # Byte for Washinton
				#--------------------------------------------
				50320 : 669.876491522, # Byte for Washinton
				50322 : 669.876491522, # Byte for Washinton
				50324 : 669.876491522, # Byte for Washinton
				50326 : 669.876491522, # Byte for Washinton
				50328 : 669.876491522, # Byte for Washinton
				#--------------------------------------------
				50330 : 669.876491522, # Byte for Washinton
				50332 : 669.876491522, # Byte for Washinton
				50334 : 669.876491522, # Byte for Washinton
				50336 : 669.876491522, # Byte for Washinton
				50338 : 669.876491522, # Byte for Washinton
				#--------------------------------------------
				50340 : 669.876491522, # Byte for Washinton
				50342 : 669.876491522, # Byte for Washinton
				50344 : 669.876491522, # Byte for Washinton
				50346 : 669.876491522, # Byte for Washinton
				50348 : 669.876491522, # Byte for Washinton
				#--------------------------------------------
				50350 : 669.876491522, # Byte for Washinton
				50352 : 669.876491522, # Byte for Washinton
				50354 : 669.876491522, # Byte for Washinton
				50356 : 669.876491522, # Byte for Washinton
				50358 : 669.876491522, # Byte for Washinton
				#--------------------------------------------
				50360 : 669.876491522, # Byte for Washinton
				50362 : 669.876491522, # Byte for Washinton
				50364 : 669.876491522, # Byte for Washinton
				50366 : 669.876491522, # Byte for Washinton
				50368 : 669.876491522, # Byte for Washinton
				#--------------------------------------------
				50370 : 669.876491522, # Byte for Washinton
				50372 : 669.876491522, # Byte for Washinton
				50374 : 669.876491522, # Byte for Washinton
				50376 : 669.876491522, # Byte for Washinton
				50378 : 669.876491522, # Byte for Washinton
				#--------------------------------------------
				50380 : 669.876491522, # Byte for Washinton
				50382 : 669.876491522, # Byte for Washinton
				50384 : 669.876491522, # Byte for Washinton
				50386 : 669.876491522, # Byte for Washinton
				50388 : 669.876491522, # Byte for Washinton
				#--------------------------------------------
				50390 : 669.876491522, # Byte for Washinton
				50392 : 669.876491522, # Byte for Washinton
				50394 : 669.876491522, # Byte for Washinton
				50396 : 669.876491522, # Byte for Washinton
				50398 : 669.876491522, # Byte for Washinton
				50400 : 1,
				50402 : 1,
				50404 : 1,
				50406 : 1,
				50408 : 1,
				50410 : 1,
				50412 : 1,
				50414 : 1,
				50416 : 1,
				50418 : 1,
				50420 : 1,
				50422 : 1,
				50424 : 1,
				50426 : 1,
				50428 : 1,
				50430 : 1,
				50432 : 1,
				50434 : 1,
				50436 : 1,
				50438 : 1,
				50440 : 1,
				50442 : 1,
				50444 : 1,
				50446 : 1,
				50448 : 1,
				50450 : 1,
				50452 : 1,
				50454 : 1,
				50456 : 1,
				50458 : 1,
				50460 : 1,
				50462 : 1,
				50464 : 1,
				50466 : 1,
				50468 : 1,
				50470 : 1,
				50472 : 1,
				50474 : 1,
				50476 : 1,
				50478 : 1,
				50480 : 1,
				50482 : 1,
				50484 : 1,
				50486 : 1,
				50488 : 1,
				50490 : 1,
				50492 : 1,
				50494 : 1,
				50496 : 1,
				50498 : 1,
				50500 : 1,
				50502 : 1,
				50504 : 1,
				50506 : 1,
				50508 : 1,
				50510 : 1,
				50512 : 1,
				50514 : 1,
				50516 : 1,
				50518 : 1,
				50520 : 1,
				50522 : 1,
				50524 : 1,
				50526 : 1,
				50528 : 1,
				50530 : 1,
				50532 : 1,
				50534 : 1,
				50536 : 1,
				50538 : 1,
				50540 : 1,
				50542 : 1,
				50544 : 1,
				50546 : 1,
				50548 : 1,
				50550 : 1,
				50552 : 1,
				50554 : 1,
				50556 : 1,
				50558 : 1,
				50560 : 1,
				50562 : 1,
				50564 : 1,
				50566 : 1,
				50568 : 1,
				50570 : 1,
				50572 : 1,
				50574 : 1,
				50576 : 1,
				50578 : 1,
				50580 : 1,
				50582 : 1,
				50584 : 1,
				50586 : 1,
				50588 : 1,
				50590 : 1,
				50592 : 1,
				50594 : 1,
				50596 : 1,
				50598 : 1
			}
			self.bps = bpsBarcelona


		elif self.port == 50052:
			print("This Domain in Barcelona" , self.port)
			bpsBarcelona = { # 50050
				50050 : 100, 
				50052 : 100, 
				50054 : 100, 
				50056 : 100, 
				50058 : 100, 
				#--------------------------------------------
				50060 : 2779.949613413, # Byte for Paris
				50062 : 2779.949613413, # Byte for Paris
				50064 : 2779.949613413, # Byte for Paris
				50066 : 2779.949613413, # Byte for Paris
				50068 : 2779.949613413, # Byte for Paris
				#--------------------------------------------
				50070 : 265.143198041, # Byte for Tokyo
				50072 : 265.143198041, # Byte for Tokyo
				50074 : 265.143198041, # Byte for Tokyo
				50076 : 265.143198041, # Byte for Tokyo
				50078 : 265.143198041, # Byte for Tokyo
				#--------------------------------------------
				50080 : 542.713226939, # Byte for Toronto
				50082 : 542.713226939, # Byte for Toronto
				50084 : 542.713226939, # Byte for Toronto
				50086 : 542.713226939, # Byte for Toronto
				50088 : 542.713226939, # Byte for Toronto
				#--------------------------------------------
				50090 : 669.876491522, # Byte for Washinton
				50092 : 669.876491522, # Byte for Washinton
				50094 : 669.876491522, # Byte for Washinton
				50096 : 669.876491522, # Byte for Washinton
				50098 : 669.876491522 # Byte for Washinton
			}
			self.bps = bpsBarcelona

		elif self.port == 50054:
			print("This Domain in Barcelona" , self.port)
			bpsBarcelona = { # 50050
				50050 : 100, 
				50052 : 100, 
				50054 : 100, 
				50056 : 100, 
				50058 : 100, 
				#--------------------------------------------
				50060 : 2779.949613413, # Byte for Paris
				50062 : 2779.949613413, # Byte for Paris
				50064 : 2779.949613413, # Byte for Paris
				50066 : 2779.949613413, # Byte for Paris
				50068 : 2779.949613413, # Byte for Paris
				#--------------------------------------------
				50070 : 265.143198041, # Byte for Tokyo
				50072 : 265.143198041, # Byte for Tokyo
				50074 : 265.143198041, # Byte for Tokyo
				50076 : 265.143198041, # Byte for Tokyo
				50078 : 265.143198041, # Byte for Tokyo
				#--------------------------------------------
				50080 : 542.713226939, # Byte for Toronto
				50082 : 542.713226939, # Byte for Toronto
				50084 : 542.713226939, # Byte for Toronto
				50086 : 542.713226939, # Byte for Toronto
				50088 : 542.713226939, # Byte for Toronto
				#--------------------------------------------
				50090 : 669.876491522, # Byte for Washinton
				50092 : 669.876491522, # Byte for Washinton
				50094 : 669.876491522, # Byte for Washinton
				50096 : 669.876491522, # Byte for Washinton
				50098 : 669.876491522 # Byte for Washinton
			}
			self.bps = bpsBarcelona

		elif self.port == 50056:
			print("This Domain in Barcelona" , self.port)
			bpsBarcelona = { # 50050
				50050 : 100, 
				50052 : 100, 
				50054 : 100, 
				50056 : 100, 
				50058 : 100, 
				#--------------------------------------------
				50060 : 2779.949613413, # Byte for Paris
				50062 : 2779.949613413, # Byte for Paris
				50064 : 2779.949613413, # Byte for Paris
				50066 : 2779.949613413, # Byte for Paris
				50068 : 2779.949613413, # Byte for Paris
				#--------------------------------------------
				50070 : 265.143198041, # Byte for Tokyo
				50072 : 265.143198041, # Byte for Tokyo
				50074 : 265.143198041, # Byte for Tokyo
				50076 : 265.143198041, # Byte for Tokyo
				50078 : 265.143198041, # Byte for Tokyo
				#--------------------------------------------
				50080 : 542.713226939, # Byte for Toronto
				50082 : 542.713226939, # Byte for Toronto
				50084 : 542.713226939, # Byte for Toronto
				50086 : 542.713226939, # Byte for Toronto
				50088 : 542.713226939, # Byte for Toronto
				#--------------------------------------------
				50090 : 669.876491522, # Byte for Washinton
				50092 : 669.876491522, # Byte for Washinton
				50094 : 669.876491522, # Byte for Washinton
				50096 : 669.876491522, # Byte for Washinton
				50098 : 669.876491522 # Byte for Washinton
			}
			self.bps = bpsBarcelona

		elif self.port == 50058:
			print("This Domain in Barcelona" , self.port)
			bpsBarcelona = { # 50050
				50050 : 100, 
				50052 : 100, 
				50054 : 100, 
				50056 : 100, 
				50058 : 100, 
				#--------------------------------------------
				50060 : 2779.949613413, # Byte for Paris
				50062 : 2779.949613413, # Byte for Paris
				50064 : 2779.949613413, # Byte for Paris
				50066 : 2779.949613413, # Byte for Paris
				50068 : 2779.949613413, # Byte for Paris
				#--------------------------------------------
				50070 : 265.143198041, # Byte for Tokyo
				50072 : 265.143198041, # Byte for Tokyo
				50074 : 265.143198041, # Byte for Tokyo
				50076 : 265.143198041, # Byte for Tokyo
				50078 : 265.143198041, # Byte for Tokyo
				#--------------------------------------------
				50080 : 542.713226939, # Byte for Toronto
				50082 : 542.713226939, # Byte for Toronto
				50084 : 542.713226939, # Byte for Toronto
				50086 : 542.713226939, # Byte for Toronto
				50088 : 542.713226939, # Byte for Toronto
				#--------------------------------------------
				50090 : 669.876491522, # Byte for Washinton
				50092 : 669.876491522, # Byte for Washinton
				50094 : 669.876491522, # Byte for Washinton
				50096 : 669.876491522, # Byte for Washinton
				50098 : 669.876491522 # Byte for Washinton
			}
			self.bps = bpsBarcelona

		#---------------------------------------------------50060
		elif self.port == 50060:
			print("This Domain in Paris" , self.port)
			bpsParis = { # 50060
				50050 : 2775.48963095, # Byte  for Barcelona
				50052 : 2775.48963095, # Byte  for Barcelona
				50054 : 2775.48963095, # Byte  for Barcelona
				50056 : 2775.48963095, # Byte  for Barcelona
				50058 : 2775.48963095, # Byte  for Barcelona
				#--------------------------------------------
				50060 : 100, 
				50062 : 100, 
				50064 : 100, 
				50066 : 100, 
				50068 : 100, 
				#--------------------------------------------
				50070 : 274.323727717, # Byte for Tokyo
				50072 : 274.323727717, # Byte for Tokyo
				50074 : 274.323727717, # Byte for Tokyo
				50076 : 274.323727717, # Byte for Tokyo
				50078 : 274.323727717, # Byte for Tokyo
				#--------------------------------------------
				50080 : 696.007743086, # Byte for Toronto
				50082 : 696.007743086, # Byte for Toronto
				50084 : 696.007743086, # Byte for Toronto
				50086 : 696.007743086, # Byte for Toronto
				50088 : 696.007743086, # Byte for Toronto
				#--------------------------------------------
				50090 : 724.941381693, # Byte for Washinton
				50092 : 724.941381693, # Byte for Washinton
				50094 : 724.941381693, # Byte for Washinton
				50096 : 724.941381693, # Byte for Washinton
				50098 : 724.941381693 # Byte for Washinton
			}
			self.bps = bpsParis

		elif self.port == 50062:
			print("This Domain in Paris" , self.port)
			bpsParis = { # 50060
				50050 : 2775.48963095, # Byte  for Barcelona
				50052 : 2775.48963095, # Byte  for Barcelona
				50054 : 2775.48963095, # Byte  for Barcelona
				50056 : 2775.48963095, # Byte  for Barcelona
				50058 : 2775.48963095, # Byte  for Barcelona
				#--------------------------------------------
				50060 : 100, 
				50062 : 100, 
				50064 : 100, 
				50066 : 100, 
				50068 : 100, 
				#--------------------------------------------
				50070 : 274.323727717, # Byte for Tokyo
				50072 : 274.323727717, # Byte for Tokyo
				50074 : 274.323727717, # Byte for Tokyo
				50076 : 274.323727717, # Byte for Tokyo
				50078 : 274.323727717, # Byte for Tokyo
				#--------------------------------------------
				50080 : 696.007743086, # Byte for Toronto
				50082 : 696.007743086, # Byte for Toronto
				50084 : 696.007743086, # Byte for Toronto
				50086 : 696.007743086, # Byte for Toronto
				50088 : 696.007743086, # Byte for Toronto
				#--------------------------------------------
				50090 : 724.941381693, # Byte for Washinton
				50092 : 724.941381693, # Byte for Washinton
				50094 : 724.941381693, # Byte for Washinton
				50096 : 724.941381693, # Byte for Washinton
				50098 : 724.941381693 # Byte for Washinton
			}
			self.bps = bpsParis

		elif self.port == 50064:
			print("This Domain in Paris" , self.port)
			bpsParis = { # 50060
				50050 : 2775.48963095, # Byte  for Barcelona
				50052 : 2775.48963095, # Byte  for Barcelona
				50054 : 2775.48963095, # Byte  for Barcelona
				50056 : 2775.48963095, # Byte  for Barcelona
				50058 : 2775.48963095, # Byte  for Barcelona
				#--------------------------------------------
				50060 : 100, 
				50062 : 100, 
				50064 : 100, 
				50066 : 100, 
				50068 : 100, 
				#--------------------------------------------
				50070 : 274.323727717, # Byte for Tokyo
				50072 : 274.323727717, # Byte for Tokyo
				50074 : 274.323727717, # Byte for Tokyo
				50076 : 274.323727717, # Byte for Tokyo
				50078 : 274.323727717, # Byte for Tokyo
				#--------------------------------------------
				50080 : 696.007743086, # Byte for Toronto
				50082 : 696.007743086, # Byte for Toronto
				50084 : 696.007743086, # Byte for Toronto
				50086 : 696.007743086, # Byte for Toronto
				50088 : 696.007743086, # Byte for Toronto
				#--------------------------------------------
				50090 : 724.941381693, # Byte for Washinton
				50092 : 724.941381693, # Byte for Washinton
				50094 : 724.941381693, # Byte for Washinton
				50096 : 724.941381693, # Byte for Washinton
				50098 : 724.941381693 # Byte for Washinton
			}
			self.bps = bpsParis

		elif self.port == 50066:
			print("This Domain in Paris" , self.port)
			bpsParis = { # 50060
				50050 : 2775.48963095, # Byte  for Barcelona
				50052 : 2775.48963095, # Byte  for Barcelona
				50054 : 2775.48963095, # Byte  for Barcelona
				50056 : 2775.48963095, # Byte  for Barcelona
				50058 : 2775.48963095, # Byte  for Barcelona
				#--------------------------------------------
				50060 : 100, 
				50062 : 100, 
				50064 : 100, 
				50066 : 100, 
				50068 : 100, 
				#--------------------------------------------
				50070 : 274.323727717, # Byte for Tokyo
				50072 : 274.323727717, # Byte for Tokyo
				50074 : 274.323727717, # Byte for Tokyo
				50076 : 274.323727717, # Byte for Tokyo
				50078 : 274.323727717, # Byte for Tokyo
				#--------------------------------------------
				50080 : 696.007743086, # Byte for Toronto
				50082 : 696.007743086, # Byte for Toronto
				50084 : 696.007743086, # Byte for Toronto
				50086 : 696.007743086, # Byte for Toronto
				50088 : 696.007743086, # Byte for Toronto
				#--------------------------------------------
				50090 : 724.941381693, # Byte for Washinton
				50092 : 724.941381693, # Byte for Washinton
				50094 : 724.941381693, # Byte for Washinton
				50096 : 724.941381693, # Byte for Washinton
				50098 : 724.941381693 # Byte for Washinton
			}
			self.bps = bpsParis

		elif self.port == 50068:
			print("This Domain in Paris" , self.port)
			bpsParis = { # 50060
				50050 : 2775.48963095, # Byte  for Barcelona
				50052 : 2775.48963095, # Byte  for Barcelona
				50054 : 2775.48963095, # Byte  for Barcelona
				50056 : 2775.48963095, # Byte  for Barcelona
				50058 : 2775.48963095, # Byte  for Barcelona
				#--------------------------------------------
				50060 : 100, 
				50062 : 100, 
				50064 : 100, 
				50066 : 100, 
				50068 : 100, 
				#--------------------------------------------
				50070 : 274.323727717, # Byte for Tokyo
				50072 : 274.323727717, # Byte for Tokyo
				50074 : 274.323727717, # Byte for Tokyo
				50076 : 274.323727717, # Byte for Tokyo
				50078 : 274.323727717, # Byte for Tokyo
				#--------------------------------------------
				50080 : 696.007743086, # Byte for Toronto
				50082 : 696.007743086, # Byte for Toronto
				50084 : 696.007743086, # Byte for Toronto
				50086 : 696.007743086, # Byte for Toronto
				50088 : 696.007743086, # Byte for Toronto
				#--------------------------------------------
				50090 : 724.941381693, # Byte for Washinton
				50092 : 724.941381693, # Byte for Washinton
				50094 : 724.941381693, # Byte for Washinton
				50096 : 724.941381693, # Byte for Washinton
				50098 : 724.941381693 # Byte for Washinton
			}
			self.bps = bpsParis

		#---------------------------------------------------50070

		elif self.port == 50070:
			print("This Domain in Tokyo" , self.port)
			bpsTokyo = { # Tokyo 50070
				50050 : 265.054259292, # Byte  for Barcelona
				50052 : 265.054259292, # Byte  for Barcelona
				50054 : 265.054259292, # Byte  for Barcelona
				50056 : 265.054259292, # Byte  for Barcelona
				50058 : 265.054259292, # Byte  for Barcelona
				#--------------------------------------------
				50060 : 274.350774612, # Byte for Paris
				50062 : 274.350774612, # Byte for Paris
				50064 : 274.350774612, # Byte for Paris
				50066 : 274.350774612, # Byte for Paris
				50068 : 274.350774612, # Byte for Paris
				#--------------------------------------------
				50070 : 100, 
				50072 : 100, 
				50074 : 100, 
				50076 : 100, 
				50078 : 100, 
				#--------------------------------------------
				50080 : 395.14220329, # Byte for Toronto
				50082 : 395.14220329, # Byte for Toronto
				50084 : 395.14220329, # Byte for Toronto
				50086 : 395.14220329, # Byte for Toronto
				50088 : 395.14220329, # Byte for Toronto
				#--------------------------------------------
				50090 : 384.971668491, # Byte for Washinton
				50092 : 384.971668491, # Byte for Washinton
				50094 : 384.971668491, # Byte for Washinton
				50096 : 384.971668491, # Byte for Washinton
				50098 : 384.971668491, # Byte for Washinton
			}
			self.bps = bpsTokyo
			
		elif self.port == 50072:
			print("This Domain in Tokyo" , self.port)
			bpsTokyo = { # Tokyo 50070
				50050 : 265.054259292, # Byte  for Barcelona
				50052 : 265.054259292, # Byte  for Barcelona
				50054 : 265.054259292, # Byte  for Barcelona
				50056 : 265.054259292, # Byte  for Barcelona
				50058 : 265.054259292, # Byte  for Barcelona
				#--------------------------------------------
				50060 : 274.350774612, # Byte for Paris
				50062 : 274.350774612, # Byte for Paris
				50064 : 274.350774612, # Byte for Paris
				50066 : 274.350774612, # Byte for Paris
				50068 : 274.350774612, # Byte for Paris
				#--------------------------------------------
				50070 : 100, 
				50072 : 100, 
				50074 : 100, 
				50076 : 100, 
				50078 : 100, 
				#--------------------------------------------
				50080 : 395.14220329, # Byte for Toronto
				50082 : 395.14220329, # Byte for Toronto
				50084 : 395.14220329, # Byte for Toronto
				50086 : 395.14220329, # Byte for Toronto
				50088 : 395.14220329, # Byte for Toronto
				#--------------------------------------------
				50090 : 384.971668491, # Byte for Washinton
				50092 : 384.971668491, # Byte for Washinton
				50094 : 384.971668491, # Byte for Washinton
				50096 : 384.971668491, # Byte for Washinton
				50098 : 384.971668491, # Byte for Washinton
			}
			self.bps = bpsTokyo

		elif self.port == 50074:
			print("This Domain in Tokyo" , self.port)
			bpsTokyo = { # Tokyo 50070
				50050 : 265.054259292, # Byte  for Barcelona
				50052 : 265.054259292, # Byte  for Barcelona
				50054 : 265.054259292, # Byte  for Barcelona
				50056 : 265.054259292, # Byte  for Barcelona
				50058 : 265.054259292, # Byte  for Barcelona
				#--------------------------------------------
				50060 : 274.350774612, # Byte for Paris
				50062 : 274.350774612, # Byte for Paris
				50064 : 274.350774612, # Byte for Paris
				50066 : 274.350774612, # Byte for Paris
				50068 : 274.350774612, # Byte for Paris
				#--------------------------------------------
				50070 : 100, 
				50072 : 100, 
				50074 : 100, 
				50076 : 100, 
				50078 : 100, 
				#--------------------------------------------
				50080 : 395.14220329, # Byte for Toronto
				50082 : 395.14220329, # Byte for Toronto
				50084 : 395.14220329, # Byte for Toronto
				50086 : 395.14220329, # Byte for Toronto
				50088 : 395.14220329, # Byte for Toronto
				#--------------------------------------------
				50090 : 384.971668491, # Byte for Washinton
				50092 : 384.971668491, # Byte for Washinton
				50094 : 384.971668491, # Byte for Washinton
				50096 : 384.971668491, # Byte for Washinton
				50098 : 384.971668491, # Byte for Washinton
			}
			self.bps = bpsTokyo

		elif self.port == 50076:
			print("This Domain in Tokyo" , self.port)
			bpsTokyo = { # Tokyo 50070
				50050 : 265.054259292, # Byte  for Barcelona
				50052 : 265.054259292, # Byte  for Barcelona
				50054 : 265.054259292, # Byte  for Barcelona
				50056 : 265.054259292, # Byte  for Barcelona
				50058 : 265.054259292, # Byte  for Barcelona
				#--------------------------------------------
				50060 : 274.350774612, # Byte for Paris
				50062 : 274.350774612, # Byte for Paris
				50064 : 274.350774612, # Byte for Paris
				50066 : 274.350774612, # Byte for Paris
				50068 : 274.350774612, # Byte for Paris
				#--------------------------------------------
				50070 : 100, 
				50072 : 100, 
				50074 : 100, 
				50076 : 100, 
				50078 : 100, 
				#--------------------------------------------
				50080 : 395.14220329, # Byte for Toronto
				50082 : 395.14220329, # Byte for Toronto
				50084 : 395.14220329, # Byte for Toronto
				50086 : 395.14220329, # Byte for Toronto
				50088 : 395.14220329, # Byte for Toronto
				#--------------------------------------------
				50090 : 384.971668491, # Byte for Washinton
				50092 : 384.971668491, # Byte for Washinton
				50094 : 384.971668491, # Byte for Washinton
				50096 : 384.971668491, # Byte for Washinton
				50098 : 384.971668491, # Byte for Washinton
			}
			self.bps = bpsTokyo

		elif self.port == 50078:
			print("This Domain in Tokyo" , self.port)
			bpsTokyo = { # Tokyo 50070
				50050 : 265.054259292, # Byte  for Barcelona
				50052 : 265.054259292, # Byte  for Barcelona
				50054 : 265.054259292, # Byte  for Barcelona
				50056 : 265.054259292, # Byte  for Barcelona
				50058 : 265.054259292, # Byte  for Barcelona
				#--------------------------------------------
				50060 : 274.350774612, # Byte for Paris
				50062 : 274.350774612, # Byte for Paris
				50064 : 274.350774612, # Byte for Paris
				50066 : 274.350774612, # Byte for Paris
				50068 : 274.350774612, # Byte for Paris
				#--------------------------------------------
				50070 : 100, 
				50072 : 100, 
				50074 : 100, 
				50076 : 100, 
				50078 : 100, 
				#--------------------------------------------
				50080 : 395.14220329, # Byte for Toronto
				50082 : 395.14220329, # Byte for Toronto
				50084 : 395.14220329, # Byte for Toronto
				50086 : 395.14220329, # Byte for Toronto
				50088 : 395.14220329, # Byte for Toronto
				#--------------------------------------------
				50090 : 384.971668491, # Byte for Washinton
				50092 : 384.971668491, # Byte for Washinton
				50094 : 384.971668491, # Byte for Washinton
				50096 : 384.971668491, # Byte for Washinton
				50098 : 384.971668491, # Byte for Washinton
			}
			self.bps = bpsTokyo

		#---------------------------------------------------50080

		elif self.port == 50080:
			print("This Domain in Toronto" , self.port)
			bpsToronto = { # 50080
				50050 : 542.920402779, # Byte  for Barcelona
				50052 : 542.920402779, # Byte  for Barcelona
				50054 : 542.920402779, # Byte  for Barcelona
				50056 : 542.920402779, # Byte  for Barcelona
				50058 : 542.920402779, # Byte  for Barcelona
				#--------------------------------------------
				50060 : 695.856392637, # Byte for Paris
				50062 : 695.856392637, # Byte for Paris
				50064 : 695.856392637, # Byte for Paris
				50066 : 695.856392637, # Byte for Paris
				50068 : 695.856392637, # Byte for Paris
				#--------------------------------------------
				50070 : 395.122704121, # Byte for Tokyo
				50072 : 395.122704121, # Byte for Tokyo
				50074 : 395.122704121, # Byte for Tokyo
				50076 : 395.122704121, # Byte for Tokyo
				50078 : 395.122704121, # Byte for Tokyo
				#--------------------------------------------
				50080 : 100, 
				50082 : 100, 
				50084 : 100, 
				50086 : 100, 
				50088 : 100, 
				#--------------------------------------------
				50090 : 4266.666666667, # Byte for Washinton
				50092 : 4266.666666667, # Byte for Washinton
				50094 : 4266.666666667, # Byte for Washinton
				50096 : 4266.666666667, # Byte for Washinton
				50098 : 4266.666666667 # Byte for Washinton
			}
			self.bps = bpsToronto

		elif self.port == 50082:
			print("This Domain in Toronto" , self.port)
			bpsToronto = { # 50080
				50050 : 542.920402779, # Byte  for Barcelona
				50052 : 542.920402779, # Byte  for Barcelona
				50054 : 542.920402779, # Byte  for Barcelona
				50056 : 542.920402779, # Byte  for Barcelona
				50058 : 542.920402779, # Byte  for Barcelona
				#--------------------------------------------
				50060 : 695.856392637, # Byte for Paris
				50062 : 695.856392637, # Byte for Paris
				50064 : 695.856392637, # Byte for Paris
				50066 : 695.856392637, # Byte for Paris
				50068 : 695.856392637, # Byte for Paris
				#--------------------------------------------
				50070 : 395.122704121, # Byte for Tokyo
				50072 : 395.122704121, # Byte for Tokyo
				50074 : 395.122704121, # Byte for Tokyo
				50076 : 395.122704121, # Byte for Tokyo
				50078 : 395.122704121, # Byte for Tokyo
				#--------------------------------------------
				50080 : 100, 
				50082 : 100, 
				50084 : 100, 
				50086 : 100, 
				50088 : 100, 
				#--------------------------------------------
				50090 : 4266.666666667, # Byte for Washinton
				50092 : 4266.666666667, # Byte for Washinton
				50094 : 4266.666666667, # Byte for Washinton
				50096 : 4266.666666667, # Byte for Washinton
				50098 : 4266.666666667 # Byte for Washinton
			}
			self.bps = bpsToronto

		elif self.port == 50084:
			print("This Domain in Toronto" , self.port)
			bpsToronto = { # 50080
				50050 : 542.920402779, # Byte  for Barcelona
				50052 : 542.920402779, # Byte  for Barcelona
				50054 : 542.920402779, # Byte  for Barcelona
				50056 : 542.920402779, # Byte  for Barcelona
				50058 : 542.920402779, # Byte  for Barcelona
				#--------------------------------------------
				50060 : 695.856392637, # Byte for Paris
				50062 : 695.856392637, # Byte for Paris
				50064 : 695.856392637, # Byte for Paris
				50066 : 695.856392637, # Byte for Paris
				50068 : 695.856392637, # Byte for Paris
				#--------------------------------------------
				50070 : 395.122704121, # Byte for Tokyo
				50072 : 395.122704121, # Byte for Tokyo
				50074 : 395.122704121, # Byte for Tokyo
				50076 : 395.122704121, # Byte for Tokyo
				50078 : 395.122704121, # Byte for Tokyo
				#--------------------------------------------
				50080 : 100, 
				50082 : 100, 
				50084 : 100, 
				50086 : 100, 
				50088 : 100, 
				#--------------------------------------------
				50090 : 4266.666666667, # Byte for Washinton
				50092 : 4266.666666667, # Byte for Washinton
				50094 : 4266.666666667, # Byte for Washinton
				50096 : 4266.666666667, # Byte for Washinton
				50098 : 4266.666666667 # Byte for Washinton
			}
			self.bps = bpsToronto

		elif self.port == 50086:
			print("This Domain in Toronto" , self.port)
			bpsToronto = { # 50080
				50050 : 542.920402779, # Byte  for Barcelona
				50052 : 542.920402779, # Byte  for Barcelona
				50054 : 542.920402779, # Byte  for Barcelona
				50056 : 542.920402779, # Byte  for Barcelona
				50058 : 542.920402779, # Byte  for Barcelona
				#--------------------------------------------
				50060 : 695.856392637, # Byte for Paris
				50062 : 695.856392637, # Byte for Paris
				50064 : 695.856392637, # Byte for Paris
				50066 : 695.856392637, # Byte for Paris
				50068 : 695.856392637, # Byte for Paris
				#--------------------------------------------
				50070 : 395.122704121, # Byte for Tokyo
				50072 : 395.122704121, # Byte for Tokyo
				50074 : 395.122704121, # Byte for Tokyo
				50076 : 395.122704121, # Byte for Tokyo
				50078 : 395.122704121, # Byte for Tokyo
				#--------------------------------------------
				50080 : 100, 
				50082 : 100, 
				50084 : 100, 
				50086 : 100, 
				50088 : 100, 
				#--------------------------------------------
				50090 : 4266.666666667, # Byte for Washinton
				50092 : 4266.666666667, # Byte for Washinton
				50094 : 4266.666666667, # Byte for Washinton
				50096 : 4266.666666667, # Byte for Washinton
				50098 : 4266.666666667 # Byte for Washinton
			}
			self.bps = bpsToronto

		elif self.port == 50088:
			print("This Domain in Toronto" , self.port)
			bpsToronto = { # 50080
				50050 : 542.920402779, # Byte  for Barcelona
				50052 : 542.920402779, # Byte  for Barcelona
				50054 : 542.920402779, # Byte  for Barcelona
				50056 : 542.920402779, # Byte  for Barcelona
				50058 : 542.920402779, # Byte  for Barcelona
				#--------------------------------------------
				50060 : 695.856392637, # Byte for Paris
				50062 : 695.856392637, # Byte for Paris
				50064 : 695.856392637, # Byte for Paris
				50066 : 695.856392637, # Byte for Paris
				50068 : 695.856392637, # Byte for Paris
				#--------------------------------------------
				50070 : 395.122704121, # Byte for Tokyo
				50072 : 395.122704121, # Byte for Tokyo
				50074 : 395.122704121, # Byte for Tokyo
				50076 : 395.122704121, # Byte for Tokyo
				50078 : 395.122704121, # Byte for Tokyo
				#--------------------------------------------
				50080 : 100, 
				50082 : 100, 
				50084 : 100, 
				50086 : 100, 
				50088 : 100, 
				#--------------------------------------------
				50090 : 4266.666666667, # Byte for Washinton
				50092 : 4266.666666667, # Byte for Washinton
				50094 : 4266.666666667, # Byte for Washinton
				50096 : 4266.666666667, # Byte for Washinton
				50098 : 4266.666666667 # Byte for Washinton
			}
			self.bps = bpsToronto

		#---------------------------------------------------50090

		elif self.port == 50090:
			bpsWashinton = { # 50090
				50050 : 672.198298498, # Byte  for Barcelona
				50052 : 672.198298498, # Byte  for Barcelona
				50054 : 672.198298498, # Byte  for Barcelona
				50056 : 672.198298498, # Byte  for Barcelona
				50058 : 672.198298498, # Byte  for Barcelona
				#--------------------------------------------
				50060 : 726.504943639, # Byte for Paris
				50062 : 726.504943639, # Byte for Paris
				50064 : 726.504943639, # Byte for Paris
				50066 : 726.504943639, # Byte for Paris
				50068 : 726.504943639, # Byte for Paris
				#--------------------------------------------
				50070 : 367.51827542, # Byte for Tokyo
				50072 : 367.51827542, # Byte for Tokyo
				50074 : 367.51827542, # Byte for Tokyo
				50076 : 367.51827542, # Byte for Tokyo
				50078 : 367.51827542, # Byte for Tokyo
				#--------------------------------------------
				50080 : 4229.447528417, # Byte for Toronto
				50082 : 4229.447528417, # Byte for Toronto
				50084 : 4229.447528417, # Byte for Toronto
				50086 : 4229.447528417, # Byte for Toronto
				50088 : 4229.447528417, # Byte for Toronto
				#--------------------------------------------
				50090 : 100,  # Byte for Washinton
				50092 : 100, 
				50094 : 100, 
				50096 : 100, 
				50098 : 100, 
			}
			self.bps = bpsWashinton

		elif self.port == 50092:
			bpsWashinton = { # 50090
				50050 : 672.198298498, # Byte  for Barcelona
				50052 : 672.198298498, # Byte  for Barcelona
				50054 : 672.198298498, # Byte  for Barcelona
				50056 : 672.198298498, # Byte  for Barcelona
				50058 : 672.198298498, # Byte  for Barcelona
				#--------------------------------------------
				50060 : 726.504943639, # Byte for Paris
				50062 : 726.504943639, # Byte for Paris
				50064 : 726.504943639, # Byte for Paris
				50066 : 726.504943639, # Byte for Paris
				50068 : 726.504943639, # Byte for Paris
				#--------------------------------------------
				50070 : 367.51827542, # Byte for Tokyo
				50072 : 367.51827542, # Byte for Tokyo
				50074 : 367.51827542, # Byte for Tokyo
				50076 : 367.51827542, # Byte for Tokyo
				50078 : 367.51827542, # Byte for Tokyo
				#--------------------------------------------
				50080 : 4229.447528417, # Byte for Toronto
				50082 : 4229.447528417, # Byte for Toronto
				50084 : 4229.447528417, # Byte for Toronto
				50086 : 4229.447528417, # Byte for Toronto
				50088 : 4229.447528417, # Byte for Toronto
				#--------------------------------------------
				50090 : 100,  # Byte for Washinton
				50090 : 100, 
				50092 : 100, 
				50094 : 100, 
				50096 : 100, 
				50098 : 100, 
			}
			self.bps = bpsWashinton

		elif self.port == 50094:
			bpsWashinton = { # 50090
				50050 : 672.198298498, # Byte  for Barcelona
				50052 : 672.198298498, # Byte  for Barcelona
				50054 : 672.198298498, # Byte  for Barcelona
				50056 : 672.198298498, # Byte  for Barcelona
				50058 : 672.198298498, # Byte  for Barcelona
				#--------------------------------------------
				50060 : 726.504943639, # Byte for Paris
				50062 : 726.504943639, # Byte for Paris
				50064 : 726.504943639, # Byte for Paris
				50066 : 726.504943639, # Byte for Paris
				50068 : 726.504943639, # Byte for Paris
				#--------------------------------------------
				50070 : 367.51827542, # Byte for Tokyo
				50072 : 367.51827542, # Byte for Tokyo
				50074 : 367.51827542, # Byte for Tokyo
				50076 : 367.51827542, # Byte for Tokyo
				50078 : 367.51827542, # Byte for Tokyo
				#--------------------------------------------
				50080 : 4229.447528417, # Byte for Toronto
				50082 : 4229.447528417, # Byte for Toronto
				50084 : 4229.447528417, # Byte for Toronto
				50086 : 4229.447528417, # Byte for Toronto
				50088 : 4229.447528417, # Byte for Toronto
				#--------------------------------------------
				50090 : 100,  # Byte for Washinton
				50090 : 100, 
				50092 : 100, 
				50094 : 100, 
				50096 : 100, 
				50098 : 100, 
			}
			self.bps = bpsWashinton

		elif self.port == 50096:
			bpsWashinton = { # 50090
				50050 : 672.198298498, # Byte  for Barcelona
				50052 : 672.198298498, # Byte  for Barcelona
				50054 : 672.198298498, # Byte  for Barcelona
				50056 : 672.198298498, # Byte  for Barcelona
				50058 : 672.198298498, # Byte  for Barcelona
				#--------------------------------------------
				50060 : 726.504943639, # Byte for Paris
				50062 : 726.504943639, # Byte for Paris
				50064 : 726.504943639, # Byte for Paris
				50066 : 726.504943639, # Byte for Paris
				50068 : 726.504943639, # Byte for Paris
				#--------------------------------------------
				50070 : 367.51827542, # Byte for Tokyo
				50072 : 367.51827542, # Byte for Tokyo
				50074 : 367.51827542, # Byte for Tokyo
				50076 : 367.51827542, # Byte for Tokyo
				50078 : 367.51827542, # Byte for Tokyo
				#--------------------------------------------
				50080 : 4229.447528417, # Byte for Toronto
				50082 : 4229.447528417, # Byte for Toronto
				50084 : 4229.447528417, # Byte for Toronto
				50086 : 4229.447528417, # Byte for Toronto
				50088 : 4229.447528417, # Byte for Toronto
				#--------------------------------------------
				50090 : 100,  # Byte for Washinton
				50090 : 100, 
				50092 : 100, 
				50094 : 100, 
				50096 : 100, 
				50098 : 100, 
			}
			self.bps = bpsWashinton

		elif self.port == 50098:
			bpsWashinton = { # 50090
				50050 : 672.198298498, # Byte  for Barcelona
				50052 : 672.198298498, # Byte  for Barcelona
				50054 : 672.198298498, # Byte  for Barcelona
				50056 : 672.198298498, # Byte  for Barcelona
				50058 : 672.198298498, # Byte  for Barcelona
				#--------------------------------------------
				50060 : 726.504943639, # Byte for Paris
				50062 : 726.504943639, # Byte for Paris
				50064 : 726.504943639, # Byte for Paris
				50066 : 726.504943639, # Byte for Paris
				50068 : 726.504943639, # Byte for Paris
				#--------------------------------------------
				50070 : 367.51827542, # Byte for Tokyo
				50072 : 367.51827542, # Byte for Tokyo
				50074 : 367.51827542, # Byte for Tokyo
				50076 : 367.51827542, # Byte for Tokyo
				50078 : 367.51827542, # Byte for Tokyo
				#--------------------------------------------
				50080 : 4229.447528417, # Byte for Toronto
				50082 : 4229.447528417, # Byte for Toronto
				50084 : 4229.447528417, # Byte for Toronto
				50086 : 4229.447528417, # Byte for Toronto
				50088 : 4229.447528417, # Byte for Toronto
				#--------------------------------------------
				50090 : 100,  # Byte for Washinton
				50090 : 100, 
				50092 : 100, 
				50094 : 100, 
				50096 : 100, 
				50098 : 100, 
			}
			self.bps = bpsWashinton

		else:
			print("Not setting Domain delay ")


	def start(self):

		self.ping_timer_p = threading.Timer(PING_INTERVAL, self.__check_owner_peers_connection)
		self.ping_timer_p.start()

		self.ws.set_fn_new_client(self.__new_client)##
		self.ws.set_fn_message_received(self.__ws_handle)##

		t = threading.Thread(target=self.ws.run_forever)
		t.start()

	def __ws_handle(self, client, server, message):##
		self.__handle_message((client, client['address'], message), server)
		return
	
	def __new_client(self, client, server):##
		print("%s is connected" %(client))
	
	def join_DMnetwork(self, host, port):
		self.my_o_host = host
		self.my_o_port = port
		self.__connect_to_CROSSP2PNW(host, port)

	def get_message_text(self, msg_type, payload = None):
		msgtxt = self.mm.build(msg_type, self.port, payload)
		print('generated_msg:', msgtxt)
		print("msgtxt_type",type(msgtxt))
		return msgtxt

	def send_msg(self, peer, msg, delay):
		if not delay:
			try:
				ws4edge = create_connection("ws://" + str(peer[0]) + ":" + str(peer[1]))
				ws4edge.send(msg.encode())
				ws4edge.close()

			except OSError:
				print('Connection failed for peer : ', peer)
				self.__remove_peer(peer)

		else:
			bps = self.bps.get(peer[1])
			print("delay bps",bps)
			getsize = sys.getsizeof(msg)
			print(getsize)
			sec = getsize/bps
			print(sec)
			wait_sec =  sec
			t = time.perf_counter()
			until = time.perf_counter() + wait_sec
			while time.perf_counter() < until:
				pass
			end_time = time.perf_counter() - t
			try:
				ws4edge = create_connection("ws://" + str(peer[0]) + ":" + str(peer[1]))
				ws4edge.send(msg.encode())
				ws4edge.close()

			except OSError:
				print('Connection failed for peer : ', peer)
				self.__remove_peer(peer)


	def send_msg_to_all_owner_peer(self, msg):
		print('send_msg_to_all_owner_peer was called!')
		current_list = sorted(self.owner_node_set.get_list(),reverse=True, key = lambda x: self.bps[x[1]])
		current_list.remove((self.host, self.port))
		for peer in current_list:
			print("message will be sent to ... ", peer)
			self.send_msg(peer, msg, delay = None )
			# p_wait_sec = sec

	def connection_close(self):
		pass
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((self.host, self.port))
		self.socket.close()
		s.close()
		self.ping_timer_p.cancel()
		if self.my_o_host is not None:
			msg = self.mm.build(MSG_REMOVE_AS_OWNER, self.port)
			self.send_msg((self.my_o_host, self.my_o_port), msg, False)

	def __connect_to_CROSSP2PNW(self, host, port):
		msg = self.mm.build(MSG_ADD_AS_OWNER, self.port)
		self.send_msg((host, port), msg, False) 

	def __wait_for_access(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((self.host, self.port))
		self.socket.listen(0)

		executor = ThreadPoolExecutor(max_workers=10)

		while True:

			print('Waiting for the connection ...')
			soc, addr = self.socket.accept()
			print('Connected by .. ', addr)
			data_sum = ''

			params = (soc, addr, data_sum)
			executor.submit(self.__handle_message, params)

	def __is_in_owner_set(self, peer):
		return self.owner_node_set.has_this_peer(peer)


	def __handle_message(self, params ,server):#

		soc, addr, data_sum = params

		#Parse
		result, reason, cmd, peer_port, payload = self.mm.parse(data_sum)
		print("result, reason, cmd, peer_port, payload")

		status = (result, reason)

		if status == ('error', ERR_PROTOCOL_UNMATCH):
			print('Error: Protocol name is not matched')
			return
		elif status == ('error', ERR_VERSION_UNMATCH):
			print('Error: Protocol version is not matched')
			return

		elif status == ('ok', OK_WITHOUT_PAYLOAD):
			if cmd == MSG_ADD_AS_OWNER:
				print('ADD node request was received!!')
				self.__add_peer((addr[0], peer_port))
				print("New Domain connection")
				self.adding_timer = time.time()
	
				if(addr[0], peer_port) == (self.host, self.port):
					return
				else:
					cl = pickle.dumps(self.owner_node_set.get_list(), 0).decode()
					msg = self.mm.build(MSG_OWNER_LIST, self.port, cl)
					self.send_msg_to_all_owner_peer(msg)

			elif cmd == MSG_REMOVE_AS_OWNER:
				print('REMOVE request was received!! from', addr[0], peer_port)
				self.__remove_peer((addr[0], peer_port))
				cl = pickle.dumps(self.owner_node_set.get_list(), 0).decode()
				msg = self.mm.build(MSG_OWNER_LIST, self.port, cl)
				self.send_msg_to_all_owner_peer(msg)

			elif cmd == MSG_PING:##
				peer = (addr[0], peer_port)
				if ( self.__is_in_edge_set(peer) ):
					self.edge_node_set.ping_recv(peer)
				print('----------------PING receive!!------------')
				cl = pickle.dumps(self.core_node_set.get_list(), 0).decode()
				msg = self.mm.build(MSG_OWNER_LIST, self.port, cl)
				server.send_message(soc, msg.encode('utf-8'))
				print("core node list sent")
				return

			elif cmd == MSG_REQUEST_OWNER_LIST:
				print('List for Core nodes was requested!!')
				cl = pickle.dumps(self.owner_node_set.get_list(), 0).decode()
				msg = self.mm.build(MSG_OWNER_LIST, self.port, cl)
				self.send_msg((addr[0], peer_port), msg, delay = False)


			else:
				is_owner = self.__is_in_owner_set((addr[0], peer_port))
				self.callback((result, reason, cmd, peer_port, payload), is_owner, (addr[0], peer_port))
				return


		elif status == ('ok', OK_WITH_PAYLOAD):
			if cmd == MSG_OWNER_LIST:
					print('Refresh the owner node list...')
					new_owner_set = pickle.loads(payload.encode('utf8'))
					print('latest owner node list: ', new_owner_set)
					self.owner_node_set.overwrite(new_owner_set)

			else:
				is_owner = self.__is_in_owner_set((addr[0], peer_port))
				self.callback((result, reason, cmd, peer_port, payload), is_owner, (addr[0], peer_port))
				return
		else:
			print('Unexpected status', status)

	def __add_peer(self, peer):
		self.owner_node_set.add((peer))

	def __remove_peer(self, peer):
		self.owner_node_set.remove(peer)


	def __check_owner_peers_connection(self):
		print('check_owner_peers_connection was called')
		current_owner_list = self.owner_node_set.get_list()
		changed = False
		dead_o_node_set = list(filter(lambda p: not self.__is_alive(p), current_owner_list))
		if dead_o_node_set:
			changed = True
			print('Removing owner peer', dead_o_node_set)
			current_owner_list = current_owner_list - set(dead_o_node_set)

		current_owner_list = self.owner_node_set.get_list()
		print('current owner node list:', current_owner_list)
		if changed:
			cl = pickle.dumps(current_owner_list, 0).decode()
			msg = self.mm.build(MSG_OWNER_LIST, self.port, cl)
			self.send_msg_to_all_owner_peer(msg)
		self.ping_timer_p = threading.Timer(PING_INTERVAL, self.__check_owner_peers_connection)
		self.ping_timer_p.start()



	def __is_alive(self, target):
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((target))
			msg_type = MSG_PING
			msg = self.mm.build(msg_type)
			s.sendall(msg.encode('utf-8'))
			s.close()
			return True
		except OSError:
			return False

	def __get_myip(self):
	##
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('8.8.8.8', 80))
		return s.getsockname()[0]

