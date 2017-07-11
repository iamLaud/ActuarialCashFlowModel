# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 18:02:45 2017

@author: FR015797
"""

#--------------------------------------------------
#           Project packages
#--------------------------------------------------
from MinRate import MinRate
from TargetRate import TargetRate
from PaidRate import PaidRate
#--------------------------------------------------
#           Python packages
#--------------------------------------------------
import numpy as np
import gc 
#--------------------------------------------------
#       Start of the proper code
#--------------------------------------------------

class Rule(object):
    def __init__(self, time_horizon=50):
        self.paid_rate = PaidRate()
        self.min_rate = MinRate()
        self.target_rate = TargetRate()
        
    def createStrategy(self):
        pass
#--------------------------------------------------
#       Start of the testing part of the code
#--------------------------------------------------

def main():
   pass

if __name__ == "__main__":
    main()