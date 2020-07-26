# Team member1 : Kenilkumar Maheshkumar Patel (1001765579)
# Team member2 : Parth Mukeshbhai Navadia (1001778479)

# ----------------------------------------------------------------------------------------

from komodo_rpc import KomodoRPC
import komodo.wallet as wallet
import komodo.address as address
import re
import json
import time
class coins():
	def __init__(self,username,password,port):
		self.username=username
		self.password=password  
		self.port=port
		self.komodo_rpc = KomodoRPC(node_addr='127.0.0.1', rpc_port=port, req_method='POST', rpc_username=self.username,rpc_password=self.password)
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
		result=wallet.sendtoaddress(address=address, amount=10.0, comment='', comment_to='', subtractFeeFromAmt=False)  
		result=result[1:].split(",")[0].split(":")[1] 
		if(result!="500"):
			print("Transaction id is:"+result[1:len(result)-1])
		else:
			print("Transaction rejected")
	def recv(self,address):
		result=wallet.getreceivedbyaddress(address=address, minconf=1) 
