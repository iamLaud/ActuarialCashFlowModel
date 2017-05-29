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
    def __init__(self, volume=0, return_rate=.01, value=1, time_horizon=50, starting_point=1):
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
        self.value = pd.DataFrame(data=0, index=np.arange(1,time_horizon+1), columns=['Book Value', 'Market Value'])
        self.value.loc[self.starting_point:self.time_horizon, 'Book Value'] = value
        # Initialisation des PGL
        self.potential = pd.DataFrame(data=0, index=np.arange(1,time_horizon+1), columns=['Potential Gain', 'Potential Loss'])
        self.computePotential()         

    def updateValue(self, current_step):
        self.value.loc[current_step:self.time_horizon, 'Book Value'] = self.value.loc[current_step, 'Book Value'] * (1 + self.return_rate.loc[current_step, 'RRate'])
        
    def cashOut(self, current_step):
#        output = self.value.loc[current_step, 'Market Value'] * self.volume.loc[current_step, 'Volume'] ---------- A MODIFIER PLUS TARD
        output = self.value.loc[current_step, 'Book Value'] * self.volume.loc[current_step, 'Volume']
        if(current_step < self.time_horizon):              
            self.volume.loc[np.arange(current_step+1,self.time_horizon+1), 'Volume'] = 0
#            print("Equity cashout")
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
#        print('Equity updated')

#--------------------------------------------------
#       Start of the testing part of the code
#--------------------------------------------------
#
#def main():
#    equity = Equity(return_rate=.01, volume=100, time_horizon=20)
#    print(equity.volume['Volume'] * equity.value['Book Value'])
#
#    for i in range(1,equity.time_horizon+1):
#        equity.update(i)
#        
#    print(equity.volume['Volume'] * equity.value['Book Value'])
#
#if __name__ == "__main__":
#    main()
#    