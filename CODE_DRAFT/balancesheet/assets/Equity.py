# -*- coding: utf-8 -*-
"""
Created on Thu May 18 10:01:38 2017

@author: FR015797
Date of last revision: May 18th 2017
"""


#--------------------------------------------------
#           Project packages
#--------------------------------------------------
from Asset import Asset

#--------------------------------------------------
#           Python packages
#--------------------------------------------------
import pandas as pd
import numpy as np
#--------------------------------------------------
#       Start of the proper code
#--------------------------------------------------

class Equity(Asset):
    def __init__(self, volume=0, return_rate=0, value=1, time_horizon=50):
        self.time_horizon = time_horizon
        self.volume = pd.DataFrame(data=volume, index=np.arange(1,time_horizon+1), columns=['Volume'])
        self.return_rate = pd.DataFrame(data=return_rate, index=np.arange(1,time_horizon+1), columns=['RRate'])
        self.value = pd.DataFrame(data=value, index=np.arange(1,time_horizon+1), columns=['Book Value', 'Market Value'])
        self.potential = pd.DataFrame(data=0, index=np.arange(1,time_horizon+1), columns=['Potential Gain', 'Potential Loss'])
        self.computePotential()
        
    def updateValue(self, current_step):
        self.value.loc[current_step:self.time_horizon, 'Book Value'] = self.value.loc[current_step, 'Book Value'] * (1 + self.return_rate.loc[current_step, 'RRate'])
        
    def cashOut(self, current_step):
        output = self.value.loc[current_step, 'Market Value'] * self.volume.loc[current_step, 'Volume']
        if(current_step < self.time_horizon):              
#            self.volume.loc[np.arange(current_step+1,self.time_horizon+1), 'Volume'] = 0
            print("Equity cashout")
        return output    
    
    def getWealth(self, current_step):
        return (self.value.loc[current_step, 'Market Value'] * self.volume.loc[current_step, 'Volume'])

    def getWealthPlus(self, current_step):
        return self.getWealth(current_step) + self.potential.loc[current_step, 'Potential Gain']
        
    def getWealthMinus(self, current_step):
        return self.getWealth(current_step) + self.potential.loc[current_step, 'Potential Loss']
   
    def computePotential(self):
        self.potential["Potential Gain"] = np.where(self.value.loc[:, 'Market Value'] - self.value.loc[:, 'Book Value'] >0, (self.value.loc[:, 'Market Value'] - self.value.loc[:, 'Book Value']), 0)
        self.potential["Potential Loss"] = np.where(self.value.loc[:, 'Market Value'] - self.value.loc[:, 'Book Value'] <0, (self.value.loc[:, 'Market Value'] - self.value.loc[:, 'Book Value']), 0)

    def update(self, current_step):
        self.updateValue(current_step)
        return(0)

#--------------------------------------------------
#       Start of the testing part of the code
#--------------------------------------------------

#def main():
#    equity = Equity(value=100, return_rate=.1, volume=100)


#if __name__ == "__main__":
#    main()
    