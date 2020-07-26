
import socket
import pickle
import threading
import re
from random import randint
import time
from tkinter import *
from tkinter import font
import os
from tkinter import messagebox
from coins import *
clients=[]
name=[]
client_id=-1
timer=-1
server=13
draw=0
client=13
root = None
main = Tk()
nr1=0
w=None
nr2=0
balance=0
abort=0
p1=["2C.png","3C.png","4C.png","5C.png","6C.png","7C.png","8C.png","9C.png","10C.png","JC.png","QC.png","KC.png","AC.png","pack.png"]
p2=["2S.png","3S.png","4S.png","5S.png","6S.png","7S.png","8S.png","9S.png","10S.png","JS.png","QS.png","KS.png","AS.png","pack.png"]
p3=["2H.png","3H.png","4H.png","5H.png","6H.png","7H.png","8H.png","9H.png","10H.png","JH.png","QH.png","KH.png","AH.png","pack.png"]
p4=["2D.png","3D.png","4D.png","5D.png","6D.png","7D.png","8D.png","9D.png","10D.png","JD.png","QD.png","KD.png","AD.png","pack.png"]
signal=""
signal_disconnected=""
win_loose=""
username=StringVar()
address=StringVar()
password=StringVar()
port=StringVar()
# username.set("user3070554556")
# password.set("pass6e261696532cd591acf639b17af3c17b1dd3fc09af4b609863d6698590b1555299")
# address.set("RGwNq9jdiD3B9WcjY14SkPawb8iVhXPQwT")
# port.set(11060)
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
        self.client_num=13
        self.dealer_num=13
        self.caddress=""
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
            global timer,server,client,nr1,nr2,win_loose,balance,w
            send_num=-1
            while (True):
                if(abort==1):
                    break
                try:
                    if(self.msg==100):
                        self.msg="201"+":"+address.get()
                    elif(send_num==0):
                        num=randint(0,12)
                        self.dealer_num=num
                        server=num
                        nr1=randint(0,3)
                        self.msg="num:"+str(num)+":"+str(nr1)
                    else:
                        self.msg=200
                    data = pickle.dumps(self.msg)
                    self.c.send(data)
                    rdata = pickle.loads(self.c.recv(1024))
                    if(send_num==0):
                        display=rdata
                        dummy,x,y=rdata.split(":")
                        x=int(x)
                        y=int(y)
                        self.client_num=x
                        client=x
                        nr2=y
                        send_num=1
                    if(rdata==700):
                        send_num=0
                    if(re.search("^201:*",str(self.msg))!=None):
                        self.caddress=rdata
                        if(rdata in name):
                            self.msg=400
                            data = pickle.dumps(self.msg)
                            self.c.send(data)
                            raise("Client is already connected")
                        else:
                            self.n=rdata
                            name.append(self.n)
                            self.msg=200
                    if(re.search("^num:*",str(rdata))!=None):
                        display=rdata
                        dummy,x,y=rdata.split(":")
                        x=int(x)
                        y=int(y)
                        self.client_num=x
                        client=x
                        nr2=y
                    if(self.client_num!=13 and self.dealer_num!=13):
                            if(self.client_num>=self.dealer_num):
                                win_loose="You lost 10 chips"
                                w.send(self.n)
                            else:
                                win_loose="You won 10 chips"
                                w.recv(address.get())
                            self.client_num=13
                            self.dealer_num=13
                except Exception as e:
                    err=1
                    if(self.n!=""):
                        signal_disconnected=str(self.n)+" disconnected"
                    clients.remove(self.id)
                    if(self.n!=""):
                        name.remove(self.n)
                    break
myFont = font.Font(size=15)
myFont1 = font.Font(size=15)
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
    global root,w
    w=coins(username.get(),password.get(),port.get())
    balance=w.getbalance()
    if(w.login()):
        main.withdraw()
        root=Toplevel()
        def close_window():
            root.destroy()
            os._exit(0)
        def retry():
             global draw
             draw=1
        root.geometry("800x900")
        Label(root).pack()
        hc=handle_client()
        hc.start()
        Label(main).pack()
        warning=Label(main,text="")
        warning['font']=myFont
        warning.pack()
        Label(main).pack()
        logo = PhotoImage(file="resources/"+"chip1.png")
        w1 = Label(root, image=logo).pack()
        Label(root).pack()
        dstatus=Label(root)
        dstatus['font']=myFont1
        dstatus.pack()
        Label(root).pack()
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
        warning=Label(root)
        warning['font']=myFont
        warning.pack()
        def update():
            dstatus.config(text="Current balance : $"+w.getbalance())
            warning.config(text=win_loose)
            if(float(balance)<10):
                print("Insufficient amount of money to play please add some money and then try again")
                os._exit(0)
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
            photo = PhotoImage(file="resources/"+x1[int(server)])
            photo1 = PhotoImage(file="resources/"+x2[int(client)])
            lab.config(image=photo)
            lab1.config(image=photo1)
            lab.image=photo
            lab1.image=photo1
            root.after(100, update)
        update()
        Label(root).pack()
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