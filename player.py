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

root = None
main = Tk()
timer=13
draw=0
client=13
name=StringVar()
address=StringVar()
password=StringVar()
AS = PhotoImage(file="AS.png")
nr1=0
nr2=0
p1=["2C.png","3C.png","4C.png","5C.png","6C.png","7C.png","8C.png","9C.png","10C.png","JC.png","QC.png","KC.png","AC.png","pack.png"]
p2=["2S.png","3S.png","4S.png","5S.png","6S.png","7S.png","8S.png","9S.png","10S.png","JS.png","QS.png","KS.png","AS.png","pack.png"]
p3=["2H.png","3H.png","4H.png","5H.png","6H.png","7H.png","8H.png","9H.png","10H.png","JH.png","QH.png","KH.png","AH.png","pack.png"]
p4=["2D.png","3D.png","4D.png","5D.png","6D.png","7D.png","8D.png","9D.png","10D.png","JD.png","QD.png","KD.png","AD.png","pack.png"]
asl=None
class timer_display(threading.Thread):
    def __init__(self,t):
        threading.Thread.__init__(self) 
        self.t=t 
    def run(self):
        global timer
        while(True):
            if(timer>0):
                while(timer>=0):  
                    timer=timer-1
                    time.sleep(1) 
                timer=0 
class myThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self) 
        self.s=None
        self.port=7398
        self.conn=0 
        self.status=""
        self.code=0
        self.name_client=""
    def run(self): 
        global draw
        global timer,client
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
                    elif(msg==201):
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
                        global timer,client
                        self.status="Connected"
                        timer=int(t)
                        print("number from server",timer)
                        number=randint(0,12)
                        global nr1,nr2
                        nr1=randint(0,3)
                        nr2=randint(0,3)
                        client=number
                        print("number from client",client)
                        d = str(number) 
                        data = pickle.dumps(d)
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
                    timer=13
                    client=13
                    self.name_client=""
                    self.status="Dealer is not available"
                    self.conn=0
                    self.code=403
myFont = font.Font(size=15)
myFont1 = font.Font(size=25)
def newwindow():
    global root
    main.withdraw()
    root=Toplevel() 
    t=myThread()
    t.start()
    def close_window(): 
        root.destroy()
        os._exit(0) 
    def retry(): 
         global draw 
         print(draw)
         draw=1  
         print(draw) 
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
        photo = PhotoImage(file=x1[timer])
        photo1 = PhotoImage(file=x2[client])
        lab.config(image=photo)
        lab1.config(image=photo1)
        lab.image=photo
        lab1.image=photo1
        if(timer>=0):     
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
Label(main).pack()
Label(main).pack()
label_add=Label(main,text="Enter your username")
label_add['font']=myFont 
label_add.pack()
Label(main).pack()
user=Entry(main,textvariable=address)
user['font']=myFont
user.pack() 
Label(main).pack()
Label(main).pack() 
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
Label(main).pack()
btn=Button(main,text="Login and play",command=newwindow)
btn['font']=myFont
btn.pack() 
print("login and play",address.get(),password.get())
main.geometry("600x500")  
main.mainloop()