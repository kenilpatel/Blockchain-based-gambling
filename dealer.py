import socket
import pickle
import threading
import re 
from random import randint
import time
from tkinter import * 
from tkinter import font
import os
clients=[] 
name=[]
client_id=-1
timer=-1
root = Tk()
signal=""
signal_disconnected=""
class random_select(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self) 
    def run(self):
        x=10
        global client_id
        global timer
        while(True): 
            if(len(name)!=0):
                x=x-1
                if(x==0): 
                    if(len(clients)==0):
                        index=0
                    else:
                        index=randint(0,len(clients)-1)
                        client_id=clients[index]
                        timer=randint(3,9)
                    global signal
                    # signal="Wait signal sent to "+str(name[index])+" to wait for "+str(timer)
                    # print("Wait signal sent to ",name[index]," to wait for ",timer)
                    x=10
                # print("Next wait signal in",x)
                time.sleep(1)
class handle_client(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        s=socket.socket()
        port=7398
        s.bind(('',port))
        s.listen(5)
        flag=0
        count=0
        while(True):  
            c, addr = s.accept()
            if(len(clients)==0):
                count=1
            else:   
                x=sorted(clients)
                count=int(x[len(clients)-1])+1
            t=myThread(c,count)
            t.start() 
class myThread(threading.Thread):
    def __init__(self,c,id):
        threading.Thread.__init__(self)
        self.c=c
        self.id=id
        self.n="" 
        self.msg=100
    def run(self): 
        err=0  
        clients.append(self.id) 
        global signal_disconnected
        if(len(clients)==4):
            clients.remove(self.id)
            self.msg = 404
            data = pickle.dumps(self.msg)
            self.c.send(data)   
        else:
            global timer  
            send_num=-1
            while (True):    
                try:
                    if(self.msg==100): 
                        signal_disconnected=""
                        self.msg=201  
                    elif(send_num==0):
                        num=randint(0,12)
                        self.msg="num:"+str(num)   
                        send_num=-1
                    else:
                        self.msg=200
                    data = pickle.dumps(self.msg)
                    self.c.send(data)
                    rdata = pickle.loads(self.c.recv(1024))
                    if(rdata==700):
                        send_num=0
                    elif(rdata!=200 and self.msg!=201):
                        display=rdata
                        global signal
                        signal=rdata
                        print("from client number is")
                        print(display)
                    if(self.msg==201): 
                        if(rdata in name):
                            self.msg=400
                            data = pickle.dumps(self.msg)
                            self.c.send(data)
                            raise("Client is already connected")
                        else: 
                            self.n=rdata 
                            name.append(self.n)
                            self.msg=200
                except Exception as e: 
                    err=1 
                    if(self.n!=""): 
                        signal_disconnected=self.n+" disconnected"
                        print(self.n," disconnected")
                    clients.remove(self.id) 
                    if(self.n!=""):
                        name.remove(self.n)
                    break  
t1=random_select()
t1.start()
def close_window(): 
    root.destroy()
    os._exit(0)
myFont = font.Font(size=20)
myFont1 = font.Font(size=25)
Label(root).pack()
Label(root).pack()
logo1=PhotoImage(file="close.png")
btn=Button(root,image=logo1,relief='flat',command=close_window).pack()
root.geometry("600x800")   
cstatus=Label(root)
cstatus['font']=myFont
cstatus.pack()
Label(root).pack()
Label(root).pack()
logo = PhotoImage(file="chip.png")
w1 = Label(root, image=logo).pack()
Label(root).pack()
Label(root).pack()
dstatus=Label(root)
dstatus['font']=myFont1
dstatus.pack()
Label(root).pack()
Label(root).pack() 
def update():  
    dstatus.config(text="Current balance : $"+"10000")
    root.after(100, update)
update()  
main_t=handle_client()
main_t.start()
root.mainloop()

