# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 23:28:07 2021

@author: Rahim Sharifov , Sevinj Yadigarova
"""

import threading 
import socket
import tkinter as tk 
from PIL import Image,ImageTk
from tkinter.filedialog import askopenfilename
import os 



class Receiver:

    def __init__ (self,window):
        self.receiver_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 50000 
        self.ip = self.get_ip()
        self.receiver_socket.bind((self.ip,self.port))
        self.window= window
        self.count= 1
   
    def listen(self):
        
        self.receiver_socket.listen()    
        self.client,address = self.receiver_socket.accept()
        name = "Rahim's PC" 
        name = name + " "*(30-len(name))
        self.client.send(name.encode('utf-8'))
        self.name = self.client.recv(30).decode('utf-8').strip()
        
        self.window.msg_list.insert(tk.END, "connected to " + self.name+" \n")
        
        self.window.entry_field.bind("<Return>",self.window_send)
        self.window.send_button.bind("<Button-1>" , self.send_picture)
        
        t1 = threading.Thread(target= self.recv_message, args=(self.client,address),daemon=True)
        #t2 = threading.Thread(target=self.send_message, args=(client,window),daemon=True)
        t1.start()
        #t2.start()
   
        
        

    
    def send_picture(self,event):
        pct = askopenfilename()
        f=open(pct, "rb" )
       
        self.client.send("img".encode('utf-8'))
        
        file_size = str(os.path.getsize(pct))
        
        file_size = file_size + " "*(20-len(file_size))
        
        
        self.client.send(str(file_size).encode('utf-8'))
        
        
        
        l = f.read(1024)
        while l:
            self.client.send(l)
            l = f.read(1024)
        f.close()
    
        global img
        image = Image.open(pct)
             
        resize_img= image.resize((250,200))
        img = ImageTk.PhotoImage(resize_img)
             #img = tk.Label(self.window.msg_list, image=render)
             #img.pack()
             
        self.window.msg_list.insert(tk.END,"->>\n")
        self.window.msg_list.image_create(tk.END, image=img)
        self.window.msg_list.insert(tk.END,"\n")
        self.window.msg_list.see(tk.END)
        
    
        
    def recv_message (self,client,address):
        
      while True:
          test = client.recv(3).decode('utf-8')
          if test== 'msg':  
            try:
                msg = client.recv(1024).decode("utf-8")
                
                self.window.msg_list.insert(tk.END,self.name+": "+msg+"\n")
                self.window.msg_list.see(tk.END)
            
            except KeyboardInterrupt:
                break
            except:
                break
                print("Something went wrong in receiving")
          elif test== 'img':
             file_size = client.recv(20).decode("utf-8")
              
           
             
             file_size = int(file_size)
             
             
             new_pic="C:/Users/shari/OneDrive/Documents/Projects/LocalChat/received/pict" +str(self.count)+ ".jpg"
             self.count= self.count+1 
             
             
             with open(new_pic, "wb") as f:
                 l = client.recv(1024)
                 total = len(l) 
                 f.write(l)
                 while l:
                     if total != file_size:    
                         
                         l= client.recv(1024)
                         f.write(l) 
                         total = total + len(l) 
                     else:
                         break
             
             image = Image.open(new_pic)
             
             resize_img= image.resize((250,200))
             img = ImageTk.PhotoImage(resize_img)
             #img = tk.Label(self.window.msg_list, image=render)
             #img.pack()
             print('B')
             self.window.msg_list.insert(tk.END, self.name +": \n")
             self.window.msg_list.image_create(tk.END, image=img)
             self.window.msg_list.see(tk.END)
             
    
    def window_send(self,event):
        
        self.send_message(self.client,self.window.entry_field.get())
        self.window.msg_list.insert(tk.END, "->>" +self.window.entry_field.get() +"\n")
        self.window.entry_field.delete(0,tk.END)
        self.window.msg_list.see(tk.END)
    
    
    def send_message(self,client,msg):
       
        try:
             #message= "Hello"
             client.send("msg".encode('utf-8'))
            
             client.send(msg.encode('utf-8'))
 
        except KeyboardInterrupt:
             return
        except:
             print("Error in sending")
             return 
      
    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
                IP = '127.0.0.1'
        finally:
                s.close()
                return IP
            
            
    def close(self):
        self.receiver_socket.close()