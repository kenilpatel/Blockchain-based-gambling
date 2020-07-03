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
root = None
main = Tk()
server=13
draw=0
client=13
name=StringVar()
username=StringVar()
address=StringVar()
password=StringVar()
username.set("user59240048")
password.set("passaa94230c68d9bdfc0c5fbd08cb3b734e56dae6f5fb153959a8a3093daef8a7db89")
address.set("RErdj8npUaL35jdcAa7Hixp724Hvc1Ajtp")
dealer_address=""
AS = PhotoImage(file="AS.png")
nr1=0
nr2=0
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
            if(self.conn==0): 
                self.conn=1
                # print("connecting again")
                try:
                    self.s=socket.socket()
                    self.s.connect(('127.0.0.1',self.port)) 
                    self.conn=1
                except Exception as e: 
                    print(e)
                    self.status="Dealer is not available"
                    self.conn=0
                    self.code=403
            else:
                try: 
                    msg=pickle.loads(self.s.recv(1024))  
                    global draw 
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
                        x,t=msg.split(":")
                        global server,client
                        self.status="Connected"
                        server=int(t) 
                        number=randint(0,12)
                        global nr1,nr2
                        nr1=randint(0,3)
                        nr2=randint(0,3)
                        client=number 
                        d = str(number) 
                        data = pickle.dumps(d)
                        self.dealer_num=int(server)
                        self.client_num=int(client)
                        if(self.client_num!=-1 and self.dealer_num!=-1):
                            if(self.client_num>=self.dealer_num):
                                print("win")
                            else:
                                print("loose")
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
                        self.status="Connected" 
                        self.code=200
                except Exception as e:  
                    print(e) 
                    server=13
                    client=13
                    self.name_client=""
                    self.status="Dealer is not available"
                    self.conn=0
                    self.code=403
myFont = font.Font(size=15)
myFont1 = font.Font(size=25)
Label(main).pack() 
warning=Label(main,text="")
warning['font']=myFont 
warning.pack()
Label(main).pack()
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
user=Entry(main,textvariable=password)
user['font']=myFont
user.pack()
Label(main).pack() 
label_add=Label(main,text="Enter your address")
label_add['font']=myFont
label_add.pack()
Label(main).pack() 
user=Entry(main,textvariable=address)
user['font']=myFont
user.pack()
Label(main).pack()
Label(main).pack()
def newwindow():
    global root
    # print(username.get(),address.get(),password.get())
    w=coins(username.get(),password.get())
    print(w.login())
    if(w.login()):
        main.withdraw()
        root=Toplevel() 
        t=myThread()
        t.start()
        def close_window(): 
            root.destroy()
            os._exit(0) 
        def retry(): 
             global draw  
             draw=1    
        root.geometry("800x910") 
        Label(root).pack()  
        player=Label(root,text="Welcome to casino")
        player['font']=myFont1
        player.pack() 
        Label(root).pack()
        logo = PhotoImage(file="chip1.png")
        w1 = Label(root, image=logo).pack()
        Label(root).pack()
        dstatus=Label(root)
        dstatus['font']=myFont1
        dstatus.pack()
        Label(root).pack()
        Label(root).pack() 
        logo1=PhotoImage(file="play.png")
        submit=Button(root,relief='flat',image=logo1,command=retry)  
        dealer=Label(root,text="Dealer's card")
        dealer['font']=myFont
        dealer.pack()
        Label(root).pack()
        lab = Label(root) 
        lab['font']=myFont1
        photo = PhotoImage(file="pack.png") 
        lab.config(image=photo)
        lab.pack()
        Label(root).pack() 
        player=Label(root,text="Player's card")
        player['font']=myFont
        player.pack() 
        Label(root).pack() 
        lab1 = Label(root) 
        lab1['font']=myFont 
        photo1 = PhotoImage(file="pack.png") 
        lab1.config(image=photo1)
        lab1.pack() 
        Label(root).pack() 
        def update():  
            dstatus.config(text="Current balance : $"+"10000")
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
            photo = PhotoImage(file=x1[server])
            photo1 = PhotoImage(file=x2[client])
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
        Label(root).pack()
        root.mainloop()
    else:
        warning.config(text="Invalid Credential please try again")
        password.set("")
        address.set("")
        username.set("")
btn=Button(main,text="Login and play",command=newwindow)
btn['font']=myFont
btn.pack()  
main.geometry("600x500")  
main.mainloop()

'''rpcuser=user59240048
rpcpassword=passaa94230c68d9bdfc0c5fbd08cb3b734e56dae6f5fb153959a8a3093daef8a7db89'''