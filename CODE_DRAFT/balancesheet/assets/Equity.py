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
    """
        represents Equity-like instruments. 
        
        This class inherited from the *Asset* class
        
        :param volume: Time serie of the volume of Equities over time
        :param value: Time serie of the value of the Equity over time
        :param time_horizon: Duration of the simulation
        :param starting_point: Point of time in the simulation when the instrument is emitted
        :param flag: hidden variables equal to 0 by default
        :param return_rate: Time serie of the value of the interest rate of the Equity over time
        :param potential: Time serie of the potential gain & loss on the Equity
        :type volume: DataFrame of Integer
        :type value: DataFrame of Float
        :type time_horizon: Integer
        :type starting_point: Integer
        :type flag: Float
        :type return_rate: DataFrame of Float
        :type potential: DataFrame of Float
        :return: An instance of the Equity class
        :rtype: Equity object
    """
    def __init__(self, value=1, volume=0, return_rate=.01, time_horizon=50, starting_point=1):
        """
            creates an Equity object
        """
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
        self.value = pd.DataFrame(data=value, index=np.arange(1,time_horizon+1), columns=['Book Value', 'Market Value'])
        self.value.loc[:starting_point-1, 'Book Value'] = 0
        self.value.loc[:starting_point-1, 'Market Value'] = 0
#        self.value.loc[:, 'Market Value'] = 0
        # Initialisation des PGL
        self.potential = pd.DataFrame(data=0, index=np.arange(1,time_horizon+1), columns=['Potential Gain', 'Potential Loss'])
        self.computePotential()         

    def updateValue(self, current_step):
        """
            capitalizes the Equity over a period of time
        """
       # ------------------- TEST A ENLEVER ------------------
        mean = 0
        std = .05
        noise = np.random.normal(mean, std, size=1)
#        noise = 0
        # ----------------------------------------------------
        self.value.loc[current_step:self.time_horizon, 'Book Value'] = noise + self.value.loc[current_step, 'Book Value'] * (1 + self.return_rate.loc[current_step, 'RRate'])
        # integrer le versement des dividendes 
        
    def cashOut(self, current_step):
        """
            cashes out the amount of money generated by the Equity
        """
#        output = self.value.loc[current_step, 'Market Value'] * self.volume.loc[current_step, 'Volume'] ---------- A MODIFIER PLUS TARD
        output = self.value.loc[current_step, 'Book Value'] * self.volume.loc[current_step, 'Volume']
        if(current_step < self.time_horizon):              
            self.volume.loc[np.arange(current_step+1,self.time_horizon+1), 'Volume'] = 0
#            print("Equity cashout")
        return output    
   
    def sell(self, amount, current_step):
        assert(amount <= self.volume.loc[current_step, 'Volume'] * self.value.loc[current_step, 'Market Value'])
        self.volume.loc[current_step:self.time_horizon, 'Volume'] -= amount/self.value.loc[current_step, 'Market Value'] 
        return amount*self.value.loc[current_step, 'Market Value']
        #only works for now with value=1 - translates the indivisibility state of the assets
        
    def getWealth(self, current_step):
        """
            returns the amount of money represented by the Equity at a certain point in time
        """
        return (self.value.loc[current_step, 'Market Value'] * self.volume.loc[current_step, 'Volume'])

    def getWealthPlus(self, current_step):
        """
            returns the wealth returned by the selling of the Equity increased by the potential gain on it
        """
        return self.getWealth(current_step) + self.potential.loc[current_step, 'Potential Gain']
        
    def getWealthMinus(self, current_step):
        """
            returns the wealth returned by the selling of the Equity decreased by the potential loss on it
        """
        return self.getWealth(current_step) + self.potential.loc[current_step, 'Potential Loss']
#   
    def computePotential(self):
        """
            updates the potential gains & losses on this Equity
        """
        self.potential["Potential Gain"] = np.where(self.value.loc[:, 'Market Value'] - self.value.loc[:, 'Book Value'] >0, (self.value.loc[:, 'Market Value'] - self.value.loc[:, 'Book Value']), 0)
        self.potential["Potential Loss"] = np.where(self.value.loc[:, 'Market Value'] - self.value.loc[:, 'Book Value'] <0, (self.value.loc[:, 'Market Value'] - self.value.loc[:, 'Book Value']), 0)

    def update(self, current_step):
        """
            updates the Equity over a period of time
        """
        self.updateValue(current_step)
#        print('Equity updated')

#--------------------------------------------------
#       Start of the testing part of the code
#--------------------------------------------------

#def main():
#    equity = Equity(return_rate=.01, volume=100, time_horizon=20)
#    print(equity.volume)
#    
#    equity.sell(25, 15)
#    print(equity.volume)
#    
#if __name__ == "__main__":
#    main()
    