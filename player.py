# Team member1 : Kenilkumar Maheshkumar Patel (1001765579)
# Team member2 : Parth Mukeshbhai Navadia (1001778479)

# ----------------------------------------------------------------------------------------

import socket
import pickle
import re
import threading
import time
from tkinter import *
import sys
import os
from tkinter import font 
from random import randint  
from tkinter import * 
from coins import *
from tkinter import simpledialog
from coins import *
root = None
main = Tk()
server=13
draw=0
client=13
ip=""
name=StringVar()
username=StringVar()
address=StringVar()
password=StringVar()
port=StringVar()
# username.set("user3010723998")
# password.set("pass0d242e88f3a4a7466e08d3d13cc578ece20744a74124c64e9794fce20913fbfeb5")
# address.set("RA3DP2DNgZWoTCoqmn8LgBtZqLorCWrp8b")
# port.set(11060)
balance=0
dealer_address=""
win_loose="" 
nr1=0
nr2=0
warningmsg="Dealer is not available"
w=None
p1=["2C.png","3C.png","4C.png","5C.png","6C.png","7C.png","8C.png","9C.png","10C.png","JC.png","QC.png","KC.png","AC.png","pack.png"]
p2=["2S.png","3S.png","4S.png","5S.png","6S.png","7S.png","8S.png","9S.png","10S.png","JS.png","QS.png","KS.png","AS.png","pack.png"]
p3=["2H.png","3H.png","4H.png","5H.png","6H.png","7H.png","8H.png","9H.png","10H.png","JH.png","QH.png","KH.png","AH.png","pack.png"]
p4=["2D.png","3D.png","4D.png","5D.png","6D.png","7D.png","8D.png","9D.png","10D.png","JD.png","QD.png","KD.png","AD.png","pack.png"]
asl=None
class myThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self) 
		self.s=None
		self.port=7398
		self.conn=0 
		self.status=""
		self.code=0
		self.name_client=""
		self.dealer_num=-1
		self.client_num=-1
	def run(self): 
		global draw
		global server,client
		global dealer_address
		while(True):  
			global warningmsg,balance
			if(self.conn==0): 
				self.conn=1 
				try:
					self.s=socket.socket() 
					self.s.connect((ip,self.port)) 
					self.conn=1
					warningmsg="connected"
				except Exception as e:  
					warningmsg="Dealer is not available"
					self.status="Dealer is not available"
					self.conn=0
					self.code=403
			else: 
				try: 
					msg=pickle.loads(self.s.recv(1024))  
					global draw,nr1,nr2 
					if(draw==1): 
						data = pickle.dumps(700)
						self.s.send(data) 
						draw=0 
					elif(msg==404): 
						self.status="Dealer is full please try after some time"
						self.conn=0
						self.code=404
					elif(re.search("^201:*",str(msg))!=None):  
						x,y=msg.split(":")
						dealer_address=y  
						self.code=201
						self.status="Connected" 
						self.name_client=address.get() 
						data = pickle.dumps(self.name_client)
						self.s.send(data)
						self.conn=1
					elif(msg==400):  
						self.status=""
						self.name=""
						self.conn=0 
						self.code=400
					elif(re.search("^num:*",str(msg))!=None): 
						x,t,nr1=msg.split(":")
						nr1=int(nr1)
						global server,client
						self.status="Connected"
						server=int(t) 
						number=randint(0,12)  
						nr2=randint(0,3)
						client=number 
						d = "number"+":"+str(number)+":"+str(nr2)  
						data = pickle.dumps(d)
						self.dealer_num=int(server)
						self.client_num=int(client)
						if(self.client_num!=-1 and self.dealer_num!=-1):
							if(self.client_num>=self.dealer_num):
								warningmsg="You won 10 chips" 
								w.recv(address.get()) 
							else:
								warningmsg="You lost 10 chips"
								w.send(dealer_address) 
							self.client_num=-1
							self.dealer_num=-1
						self.s.send(data)
						self.conn=1 
						msg=200
					elif(msg==200):
						d=200
						data = pickle.dumps(d)
						self.s.send(data) 
						self.conn=1  
						self.code=200
				except Exception as e: 
					server=13
					client=13 
					self.name_client=""
					warningmsg="Dealer is not available"
					self.status="Dealer is not available"
					self.conn=0
					self.code=403
myFont = font.Font(size=15)
myFont1 = font.Font(size=15)
Label(main).pack() 
warning=Label(main,text="")
warning['font']=myFont 
warning.pack()
Label(main).pack() 
label_add=Label(main,text="Enter your username")
label_add['font']=myFont 
label_add.pack()
Label(main).pack()
user=Entry(main,textvariable=username)
user['font']=myFont
user.pack() 
Label(main).pack()
Label(main).pack() 
label_add=Label(main,text="Enter your password")
label_add['font']=myFont
label_add.pack()
Label(main).pack()
user1=Entry(main,textvariable=password)
user1['font']=myFont
user1.pack()
Label(main).pack() 
label_add=Label(main,text="Enter your address")
label_add['font']=myFont
label_add.pack()
Label(main).pack() 
user2=Entry(main,textvariable=address)
user2['font']=myFont
user2.pack()
Label(main).pack()
label_add=Label(main,text="Enter port number")
label_add['font']=myFont
label_add.pack()
Label(main).pack() 
user3=Entry(main,textvariable=port)
user3['font']=myFont
user3.pack()
Label(main).pack()
def newwindow():
	global root 
	global w,balance
	w=coins(username.get(),password.get(),port.get()) 
	balance=w.getbalance()
	if(w.login()):
		global ip
		ip = simpledialog.askstring("Input", "Enter Ip address of server",parent=root)
		main.withdraw()
		root=Toplevel() 
		t=myThread()
		t.start()
		def close_window(): 
			root.destroy()
			os._exit(0) 
		def retry():  
			if(float(balance)<10):
				print("Insufficient amount of money to play please add some money and then try again")
				global warningmsg
				warningmsg="You do not have enough chips to play"
				os._exit(0)
			global draw  
			draw=1    
		root.geometry("800x910") 
		Label(root).pack() 
		warning=Label(root)
		warning['font']=myFont
		warning.pack()  
		Label(root).pack()
		logo = PhotoImage(file="resources/"+"chip1.png")
		w1 = Label(root, image=logo).pack()
		Label(root).pack()
		dstatus=Label(root)
		dstatus['font']=myFont1
		dstatus.pack()
		Label(root).pack() 
		logo1=PhotoImage(file="resources/"+"play.png")
		submit=Button(root,relief='flat',image=logo1,command=retry)  
		dealer=Label(root,text="Dealer's card")
		dealer['font']=myFont
		dealer.pack()
		Label(root).pack()
		lab = Label(root) 
		lab['font']=myFont1
		photo = PhotoImage(file="resources/"+"pack.png") 
		lab.config(image=photo)
		lab.pack()
		Label(root).pack() 
		player=Label(root,text="Player's card")
		player['font']=myFont
		player.pack() 
		Label(root).pack() 
		lab1 = Label(root) 
		lab1['font']=myFont 
		photo1 = PhotoImage(file="resources/"+"pack.png") 
		lab1.config(image=photo1)
		lab1.pack() 
		Label(root).pack() 
		def update(): 
			warning.config(text=warningmsg) 
			dstatus.config(text="Current balance : $"+w.getbalance())
			if(nr1==0):
				x1=p1
			elif(nr1==1):
				x1=p2
			elif(nr1==2):
				x1=p3
			else:
				x1=p4
			if(nr2==0):
				x2=p1
			elif(nr2==1):
				x2=p2
			elif(nr2==2):
				x2=p3
			else:
				x2=p4
			photo = PhotoImage(file="resources/"+x1[server])
			photo1 = PhotoImage(file="resources/"+x2[client])
			lab.config(image=photo)
			lab1.config(image=photo1)
			lab.image=photo
			lab1.image=photo1
			if(server>=0):     
				submit.pack()
			else:
				lab.config(text=str(0)) 
				submit.pack()
			if(t.code==400): 
				# warning.config(text="Client is already connected")
				submit.pack()
			elif(t.code==404):     
				submit.pack()
			elif(t.code==201): 
				# warning.config(text="")  
				submit.pack() 
			elif(t.code==200):  
				# warning.config(text="")    
				submit.pack() 
			elif(t.code==403):   
				submit.pack()
			root.after(100, update) 
		update()   
		def doSomething(): 
			os._exit(0)
		root.protocol('WM_DELETE_WINDOW', doSomething)
		root.mainloop()
	else:
		warning.config(text="Invalid Credential please try again")
		password.set("")
		address.set("")
		username.set("")
btn=Button(main,text="Login and play",command=newwindow)
btn['font']=myFont
btn.pack()  
main.geometry("600x600") 
def doSomething(): 
	os._exit(0)
main.protocol('WM_DELETE_WINDOW', doSomething)   
main.mainloop()
