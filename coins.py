from komodo_rpc import KomodoRPC
import komodo.wallet as wallet
import komodo.address as address
import re
import json
import time
class coins():
	def __init__(self,username,password):
		self.username=username
		self.password=password  
		self.komodo_rpc = KomodoRPC(node_addr='127.0.0.1', rpc_port=8790, req_method='POST', rpc_username=self.username,rpc_password=self.password)
	def login(self): 
		result = wallet.getwalletinfo() 
		if(re.search("^<!>*",str(result))!=None):
			return False
		else:
			return True
	def getbalance(self):
		result=wallet.getwalletinfo()  
		result=result.split(":")[3].split(",")[0]
		return result
	def send(self,address):
		result=wallet.sendtoaddress(address=address, amount=1.0, comment='', comment_to='', subtractFeeFromAmt=False) 
		return result
	def recv(self,address):
		result=wallet.getreceivedbyaddress(address=address, minconf=1)
		print(self.getbalance())
