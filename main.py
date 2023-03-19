# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 00:33:18 2021

@author: Rahim Sharifov
"""
import threading           
import Receiver 
import Sender 
import tkinter as tk 
from MyWindow import MyWindow    
        

if __name__ == "__main__":
       
    root = tk.Tk()
    root.title("Local Network Chat")
    window = MyWindow(root)
        
    Receiver_obj = Receiver.Receiver(window) 
    Sender_obj = Sender.Sender(window)
    
    print(f"Your Local Ip: {Receiver_obj.get_ip()}")
  
    t1 = threading.Thread(target=Receiver_obj.listen )
    t1.start()
    
    
        
  # str1 = input("Which IP you want to connect? ")
  # Sender_obj.connect(str1, 50000)
           
       
    root.mainloop()

    
    Receiver_obj.close()
    Sender_obj.close()
        
  




