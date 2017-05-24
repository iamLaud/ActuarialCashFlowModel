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
    def __init__(self, volume=0, return_rate=0, value=1, time_horizon=50):
        self.time_horizon = time_horizon
        self.volume = pd.DataFrame(data=volume, index=np.arange(1,time_horizon+1), columns=['Volume'])
        self.return_rate = pd.DataFrame(data=return_rate, index=np.arange(1,time_horizon+1), columns=['RRate'])
        self.value = pd.DataFrame(data=value, index=np.arange(1,time_horizon+1), columns=['Value'])
        self.potential = pd.DataFrame(data=0, index=np.arange(1,time_horizon+1), columns=['Potential Gain', 'Potential Loss'])
        
    def updateRate(self, rates):
        self.return_rate.loc[:, 'RRate'] = rates.loc[:, 'RRate']
      
    def computePotential(self):
        raise NotImplementedError("Subclass must implement abstract method")
    
    def updateValue(self):
        raise NotImplementedError("Subclass must implement abstract method")
    
    def update(self, current_step):
        raise NotImplementedError("Subclass must implement abstract method")
    
    def cashOut(self):
        raise NotImplementedError("Subclass must implement abstract method")
    
    def __str__(self):
        return("value: " + self.value.__str__() + "\n\nvolume: " + str(self.volume) + "\n\nreturn rate: " + self.return_rate.__str__())
    
    
#--------------------------------------------------
#       Start of the testing part of the code
#--------------------------------------------------

#def main():
#    #test = Asset(volume=5, return_rate=.1, value=10, time_horizon=20)        
#    test = Asset()
#    #print(test1.__str__())
#    print(str(test.volume))
#    print(str(test.time_horizon))
#    print(test.value)
#    print(test.return_rate)
#    
#if __name__ == "__main__":
#    main()