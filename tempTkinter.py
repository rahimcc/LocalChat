# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 13:48:50 2021

@author: rahimcc
"""

import tkinter as tk 
from tkinter import ttk 





top = tk.Tk()
top.title("Chatter")

messages_frame = tk.Frame(top)  
my_msg = tk.StringVar()  

scrollbar = tk.Scrollbar(messages_frame)  # Adding scrollbar to message_frame
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


msg_list = tk.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set) #Listbox to show the messages
msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tk.Entry(top, textvariable=my_msg)  #Entry widget to get message from keyboard
#entry_field.bind("<Return>",send) #Binding that widget with enter event 
entry_field.pack()
send_button = tk.Button(top, text="Send")
#send_button.pack()



#Adding a menu 

menubar = tk.Menu(top)

top.config(menu=menubar)


file_menu = tk.Menu(menubar)
file_menu.add_command(label="Exit",command=top.destroy)
    
menubar.add_cascade(label="File",menu=file_menu)

top.mainloop()