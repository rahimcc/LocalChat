# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 10:59:21 2021

@author: rahimcc
"""

import unittest
from Receiver import Receiver


class Testing(unittest.TestCase):
    
    def setUp(self):
        R= Receiver()
        
    def test_get_ip(self):
        self.assertAlmostEqual(self.R.get_ip(), "192.168.1.7")
        
   
        
        
        

if __name__ == "__main__":
    t = unittest.TestLoader().loadTestsFromTestCase(TestReceiver)
    unittest.TextTestRunner(verbosity=2).run(t)       

