from komodo_rpc import KomodoRPC
import komodo.wallet as wallet
class coins():
	def __init__(self,username,password):
		self.username=username
		self.password=password 
		self.komodo_rpc = KomodoRPC(node_addr='127.0.0.1', rpc_port=8790, req_method='POST', rpc_username=self.username,rpc_password=self.password)
	def login(self):
		result = wallet.getwalletinfo()
		print(result)
w=coins("user9032177","passdcbf0f5c7c533db4db2ea33b7fad5deed7e7df026f9e4f7a834add51ec9ee67f08")
w.login()
