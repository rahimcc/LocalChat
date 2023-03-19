# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 23:28:19 2021

@author: Rahim Sharifov
"""
import threading
import socket
import tkinter as tk
from tkinter.filedialog import askopenfilename
from PIL import Image,ImageTk
import os

class Sender:
    
    
    def __init__(self,window):
        
        self.Sender_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM )
        self.port=60000
        self.ip = self.get_ip()
        self.window = window
        self.window.file_menu.add_command(label='Connect', command = self.pop_up)
        self.count=0
        
    
    def pop_up(self):
       self.new_win= tk.Toplevel(self.window.root)
       self.new_entry= tk.Entry(self.new_win)
       self.new_entry.pack()
       self.new_win.geometry("200x50")
       self.new_entry.bind("<Return>" , self.window_connect)
        
    def window_connect(self,event):
        ip_str = self.new_entry.get()
        self.new_win.destroy() 
        self.connect(ip_str,50000)
    
    
    def window_send(self,event):
        msg = self.window.entry_field.get()
        self.send_message(msg)
        self.window.msg_list.insert(tk.END,"\n->>"+msg + " \n")
        self.window.msg_list.see(tk.END)
        print("returned")
        self.window.entry_field.delete(0,tk.END)
        
    
    
    def send_picture(self,event):
        pct = askopenfilename()
        f=open(pct, "rb" )
        file_size = str(os.path.getsize(pct))
        
        file_size = file_size + " "*(20-len(file_size))
        
        self.Sender_socket.send("img".encode('utf-8'))
        
        
        self.Sender_socket.send(str(file_size).encode('utf-8'))

        
        l = f.read(1024)
        
        
        while l:
            self.Sender_socket.send(l)
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
        self.window.msg_list.see(tk.END)
        
        
        
    
    def send_message(self,msg):
        
            try:
                #self.Sender_socket.send("img".encode('utf-8'))
                #self.send_picture('C:\\Users\shari\OneDrive\Documents\Projects\LocalChat\Peyvend.jpg')
                self.Sender_socket.send("msg".encode('utf-8'))
                
                self.Sender_socket.send(msg.encode('utf-8'))
            except KeyboardInterrupt:
                return
            except :
                print("Error in sending")
                return 
                
    def recv_message (self,client,address):
            
        while True:
          test = client.recv(3).decode('utf-8')
          if test== 'msg':  
            try:
                msg = client.recv(1024).decode("utf-8")
                
                self.window.msg_list.insert(tk.END, self.name +":  "+msg+"\n")
                self.window.msg_list.see(tk.END)
            
            except KeyboardInterrupt:
                break
            except:
                break
                print("Something went wrong in receiving")
                
          elif test== 'img':
             
             file_size = client.recv(20).decode("utf-8")
             print(file_size + str(type(file_size)))
              
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
             self.window.msg_list.insert(tk.END, self.name +" \n")
             self.window.msg_list.image_create(tk.END, image=img)
             self.window.msg_list.see(tk.END)
            
    def connect(self,IP, port ):
        try:
            self.Sender_socket.connect((IP,port))
            self.name = self.Sender_socket.recv(30).decode('utf-8').strip()
            name = "Rahim's PC" 
            name = name + " "*(30-len(name))
            self.Sender_socket.send(name.encode('utf-8'))
        
            self.window.msg_list.insert(tk.END,f"Connected to {self.name}\n")
            self.window.entry_field.bind("<Return>" , self.window_send)
            self.window.send_button.bind("<Button-1>" , self.send_picture)
            
            t1 =threading.Thread(target= self.recv_message, args=(self.Sender_socket,IP),daemon=True) 
          #  t2 =threading.Thread(target= self.send_message,daemon=True)
            
            t1.start()
          #  t2.start()
            
            
        except TimeoutError:
            print("No Response")
            
            
            
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
        self.Sender_socket.close()
        