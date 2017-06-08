# -*- coding: utf-8 -*-
"""
Created on Thu May 18 10:01:38 2017

@author: FR015797
Date of last revision: May 18th 2017
"""


#--------------------------------------------------
#           Project packages
#--------------------------------------------------
from RatePaid import RatePaid
from RateTarget import RateTarget
from RateCustomer import RateCustomer
#--------------------------------------------------
#           Python packages
#--------------------------------------------------
import numpy as np
import pandas as pd
#--------------------------------------------------
#       Start of the proper code
#--------------------------------------------------

class Rule(object):
    """
        Rule va directement avoir acces a Liabilities et Assets et controler les limites, ainsi que controler l'etat des WStream
    """
    def __init__(self, time_horizon=50):
        self.rates = {'Paid Rate': RatePaid(), 'Customer Rate': RateCustomer(), 'Target Rate': RateTarget()}
        self.time_horizon = time_horizon
        self.priorities = {1:'Marge', 2:'Customer Rate', 3:'Provisions'}
        self.RATIO1 = .85
        self.RATIO2 = .90
        
    def computePBMin(self, x, y):
        return self.RATIO1*x + self.RATIO2*y        
    
    def updateRates(self):
        pass
    
    def checkPRE(self, wealthstream, provision):
        pass
    
    def checkRC(self, wealthstream, provision):
        pass
    
    def checkPPB(self):
        pass
    
    def checkPGL(self, category='All', wealthstream):
        if(category == 'All'):
            pass
        elif(category == 'Bond'):
            pass
        elif(category == 'Equity'):
            pass
     
    def checkPBMin(self):
         pass
    
    def changePriorities(self, first='Marge', second='Customer Rate', third='Provisions'):
        self.priorities[1] = first
        self.priorities[2] = second
        self.priorities[3] = third

    
#--------------------------------------------------
#       Start of the testing part of the code
#--------------------------------------------------

def main():
    rule = Rule()

if __name__ == "__main__":
    main()