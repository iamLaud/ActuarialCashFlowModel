# -*- coding: utf-8 -*-
"""
Created on Thu May 18 10:01:38 2017

@author: FR015797
Date of last revision: May 23rd 2017
"""


#--------------------------------------------------
#           Project packages
#--------------------------------------------------
#--------------------------------------------------
#           Python packages
#--------------------------------------------------
import pandas as pd
import numpy as np
#--------------------------------------------------
#       Start of the proper code
#--------------------------------------------------

class Asset(object):
    def __init__(self, return_rate=.005, value=1, time_horizon=50, starting_point=1): # we only consider Asset default value be 1$ each
        self.starting_point = starting_point
        self.time_horizon = time_horizon
        self.flag = 0

        # Initialisation du return_rate
        self.return_rate = pd.DataFrame(data=0, index=np.arange(1,time_horizon+1), columns=['RRate'])
        self.return_rate.loc[self.starting_point:self.time_horizon, 'RRate'] = 0.01 #return_rate
        # Initialisation de value
        self.value = pd.DataFrame(data=value, index=np.arange(1,time_horizon+1), columns=['Market Value', 'Book Value'])
        self.value.loc[:starting_point-1, 'Market Value'] = 0
        # Initialisation des PGL
        self.potential = pd.DataFrame(data=0, index=np.arange(1,time_horizon+1), columns=['Potential Gain', 'Potential Loss'])
        
    def updateRate(self, rates):
        self.return_rate.loc[:, 'RRate'] = rates.loc[:, 'RRate']
      
    def computePotential(self):
        pass
    
    def updateValue(self):
        raise NotImplementedError("Subclass must implement abstract method")
    
    def update(self, current_step, current_yield, spreads):
        raise NotImplementedError("Subclass must implement abstract method")
    
    def cashOut(self):
        raise NotImplementedError("Subclass must implement abstract method")

        
    def sell(self, amount, current_step): # vente spot
        res = 1
        if(amount <= self.value.loc[current_step, 'Market Value']):
            self.value.loc[current_step:self.time_horizon, 'Market Value'] -= amount 
            res = amount
        return res 
      
    def __str__(self):
     return (self.value['Market Value']).__str__()
    
#--------------------------------------------------
#       Start of the testing part of the code
#--------------------------------------------------

#def main():
#    test = Asset(return_rate=.1, value=10, time_horizon=20)        
#    test = Asset()
#    print(test.value)
#    print(test.return_rate)
#    
#if __name__ == "__main__":
#    main()