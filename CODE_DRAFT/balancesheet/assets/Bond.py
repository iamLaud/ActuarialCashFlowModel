# -*- coding: utf-8 -*-
"""
Created on Thu May 18 10:01:38 2017

@author: Laurent DEBRIL
Date of last revision: April 26th 2017

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

class Bond(Asset):
    """
        This class is meant to model the simplest kind of bonds
    """
    def __init__(self, face_value=1, coupon=0, MAX_MATURITY=10, \
                 rating="AAA", default_proba=0, \
                 currency="Euro", value=1, return_rate=.01, volume=0,\
                 time_horizon=25, starting_point=1): 
        self.starting_point = starting_point
        self.time_horizon = time_horizon
        self.flag = 0
        
        self.MAX_MATURITY = MAX_MATURITY # in years
        self.maturity = self.MAX_MATURITY # decrease each year until expiring at 0 thus delivering back the face value
        
        # Initialisation du volume
        self.volume = pd.DataFrame(data=0, index=np.arange(1,time_horizon+1), columns=['Volume'])
        self.volume.loc[starting_point:self.time_horizon, 'Volume'] = volume
        # Initialisation du return_rate
        self.return_rate = pd.DataFrame(data=0, index=np.arange(1,time_horizon+1), columns=['RRate'])
        self.return_rate.loc[starting_point:self.time_horizon, 'RRate'] = return_rate
        # Initialisation de value
        self.value = pd.DataFrame(data=value, index=np.arange(1,time_horizon+1), columns=['Book Value', 'Market Value', 'Face Value'])
        self.value.loc[:starting_point-1, 'Book Value'] = 0
        self.value.loc[:starting_point-1, 'Face Value'] = 0
        self.value.loc[:, 'Market Value'] = 0

        # Initialisation des PGL
        self.potential = pd.DataFrame(data=0, index=np.arange(1,time_horizon+1), columns=['Potential Gain', 'Potential Loss'])
        self.computePotential()   

        self.rating = rating
        self.default_proba = default_proba
        self.currency = currency
        self.coupon = coupon # number of coupons    

    def updateValue(self, current_step):
#        coupon_value = self.return_rate.loc[current_step, 'RRate'] * self.value.loc[1, 'Face Value']
        self.value.loc[current_step:self.time_horizon, 'Book Value'] = self.value.loc[current_step, 'Book Value'] * (1 + self.return_rate.loc[current_step, 'RRate'])
        self.value.loc[current_step:self.time_horizon, 'Face Value'] = self.value.loc[current_step, 'Face Value'] * (1 + self.return_rate.loc[current_step, 'RRate']) 
        
    def cashOut(self, current_step):
        output = self.value.loc[current_step, 'Book Value'] * self.volume.loc[current_step, 'Volume']
        if(current_step<self.time_horizon):
            self.volume.loc[np.arange(current_step+1,self.time_horizon+1), 'Volume'] = 0
        return(output) 
     
    def update(self, current_step):
        self.maturity -= 1
        if(self.maturity == 0):
            self.flag = self.cashOut(current_step)
        self.updateValue(current_step)

    def getWealth(self, current_step):
        return (self.value.loc[current_step, 'Market Value'] * self.volume.loc[current_step, 'Volume'])

    def getWealthPlus(self, current_step):
        self.computePotential()   
        return self.getWealth(current_step) + self.potential.loc[current_step, 'Potential Gain']
        
    def getWealthMinus(self, current_step):
        self.computePotential()   
        return self.getWealth(current_step) + self.potential.loc[current_step, 'Potential Loss']
   
    def computePotential(self):
        self.potential["Potential Gain"] = np.where(self.value.loc[:, 'Market Value'] - self.value.loc[:, 'Book Value'] >0, (self.value.loc[:, 'Market Value'] - self.value.loc[:, 'Book Value']), 0)
        self.potential["Potential Loss"] = np.where(self.value.loc[:, 'Market Value'] - self.value.loc[:, 'Book Value'] <0, (self.value.loc[:, 'Market Value'] - self.value.loc[:, 'Book Value']), 0)



#--------------------------------------------------
#       Start of the testing part of the code
#--------------------------------------------------

def main():
    bond = Bond(value=1, volume=100, starting_point=5)
    print(bond)
  
if __name__ == "__main__":
    main()
    

##--------------------------------------------------
#class CP_Bond(Bond):
#    """
#        This class is meant to model coupon-paying bonds
#    """
#    def __init__(self): 
#        self.coupon = self.time_horizon
#    
##--------------------------------------------------              
#class FR_Bond(CP_Bond):
#    """
#        This class is meant to model floating rates bonds
#    """
