# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 19:32:36 2021

@author: Rahim Sharifov 
"""
import tkinter as tk
import Sender as s
from tkinter.filedialog import askopenfilename


class MyWindow:
    
    
   def __init__(self,root):
        
        self.root =root
        
        self.messages_frame = tk.Frame(self.root) #Creating messages frame to show the messages 
        
        self.scrolbar = tk.Scrollbar(self.messages_frame) # creating scrolbar and place in right side 
        self.scrolbar.pack(side=tk.RIGHT,fill = tk.Y)
       
        
        self.msg_list = tk.Text(self.messages_frame, height=15, width=50, yscrollcommand=self.scrolbar.set) #Listbox to show the messages
        
        
        self.msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
        self.messages_frame.pack()

        self.entry_field = tk.Entry(self.root)  #Entry widget to get message from keyboard
       
        self.entry_field.pack()
      
        self.menubar = tk.Menu(root)
        self.root.config(menu=self.menubar)
        self.file_menu = tk.Menu(self.menubar)
        self.file_menu.add_command(label='Exit' , command= root.destroy)
      
        self.menubar.add_cascade(label="File" ,menu=self.file_menu)
        
        
        
        self.send_button = tk.Button(self.root, text="Send Picture")
        self.send_button.pack()
        
        
                
       
       
        


   