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
    def __init__(self, volume=0, return_rate=.01, value=1, time_horizon=50, starting_point=1): # we only consider Asset priced at 1$ each
        self.starting_point = starting_point
        self.time_horizon = time_horizon
        self.flag = 0

        # Initialisation du volume
        self.volume = pd.DataFrame(data=0, index=np.arange(1,time_horizon+1), columns=['Volume'])
        self.volume.loc[self.starting_point:self.time_horizon, 'Volume'] = volume
        # Initialisation du return_rate
        self.return_rate = pd.DataFrame(data=0, index=np.arange(1,time_horizon+1), columns=['RRate'])
        self.return_rate.loc[self.starting_point:self.time_horizon, 'RRate'] = return_rate
        # Initialisation de value
        self.value = pd.DataFrame(data=0, index=np.arange(1,time_horizon+1), columns=['Market Value'])
        self.value.loc[self.starting_point:self.time_horizon, 'Market Value'] = value
        # Initialisation des PGL
        self.potential = pd.DataFrame(data=0, index=np.arange(1,time_horizon+1), columns=['Potential Gain', 'Potential Loss'])
        
    def updateRate(self, rates):
        self.return_rate.loc[:, 'RRate'] = rates.loc[:, 'RRate']
      
    def computePotential(self):
        pass
    
    def updateValue(self):
        raise NotImplementedError("Subclass must implement abstract method")
    
    def update(self, current_step):
        raise NotImplementedError("Subclass must implement abstract method")
    
    def cashOut(self):
        raise NotImplementedError("Subclass must implement abstract method")
        
    def sell(self, amount, current_step):
        assert(amount <= self.volume.loc[current_step, 'Volume'] * self.value.loc[current_step, 'Market Value'])
        self.volume.loc[current_step+1:self.time_horizon, 'Volume'] -= amount/self.value.loc[current_step, 'Market Value']
        return amount*self.value.loc[current_step, 'Market Value']
        #only works for now with value=1 - translates the indivisibility state of the assets
        
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