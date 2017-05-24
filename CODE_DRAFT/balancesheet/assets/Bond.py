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
    def __init__(self, face_value=.95, coupon=0, MAX_MATURITY=10, \
                 date_of_issue=1, rating="AAA", default_proba=0, \
                 currency="Euro", value=1, return_rate=.01, volume=0, time_horizon=50): 
        self.time_horizon = time_horizon
        self.MAX_MATURITY = MAX_MATURITY # in years
        self.maturity = self.MAX_MATURITY # decrease each year until expiring at 0 thus delivering back the face value
        
        self.value = pd.DataFrame(data=value, index=np.arange(1,self.time_horizon+1), columns=['Book Value', 'Market Value'])
        self.value.loc[:, 'Face Value'] = pd.Series(data=face_value, index=np.arange(1,self.time_horizon+1))
        
        self.volume = pd.DataFrame(data=volume, index=np.arange(1,self.time_horizon+1), columns=['Volume'])
        self.return_rate = pd.DataFrame(data=return_rate, index=np.arange(1,self.time_horizon+1), columns=['RRate'])
        self.potential = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1), columns=['Potential Gain', 'Potential Loss'])
        self.coupon = coupon # number of coupons    

        self.rating = rating
        self.default_proba = default_proba
        self.currency = currency
        self.computePotential()
        
    def updateValue(self, current_step):
        coupon_value = self.return_rate.loc[current_step, 'RRate'] * self.value.loc[1, 'Face Value']
        self.value.loc[current_step:self.time_horizon, 'Book Value'] = self.value.loc[current_step, 'Book Value'] * (1 + self.return_rate.loc[current_step, 'RRate']) - coupon_value
        self.value.loc[current_step:self.time_horizon, 'Face Value'] = self.value.loc[current_step, 'Face Value'] * (1 + self.return_rate.loc[current_step, 'RRate']) - coupon_value
    
    def cashOut(self, current_step):
        output = self.value.loc[current_step, 'Market Value'] * self.volume.loc[current_step, 'Volume']
        if(current_step<self.time_horizon):
            self.volume.loc[np.arange(current_step+1,self.time_horizon+1), 'Volume'] = 0
        return(output) 
     
    def update(self, current_step):
        self.updateValue(current_step)
        self.maturity -= 1
        if(self.maturity == 0):
            tmp = self.cashOut(current_step)
            return(tmp)
        else:
            return(0)
        
    def getWealth(self, current_step):
        return (self.value.loc[current_step, 'Market Value'] * self.volume.loc[current_step, 'Volume'])

    def getWealthPlus(self, current_step):
        return self.getWealth(current_step) + self.potential.loc[current_step, 'Potential Gain']
        
    def getWealthMinus(self, current_step):
        return self.getWealth(current_step) + self.potential.loc[current_step, 'Potential Loss']
   
    def computePotential(self):
        self.potential["Potential Gain"] = np.where(self.value.loc[:, 'Market Value'] - self.value.loc[:, 'Book Value'] >0, (self.value.loc[:, 'Market Value'] - self.value.loc[:, 'Book Value']), 0)
        self.potential["Potential Loss"] = np.where(self.value.loc[:, 'Market Value'] - self.value.loc[:, 'Book Value'] <0, (self.value.loc[:, 'Market Value'] - self.value.loc[:, 'Book Value']), 0)



#--------------------------------------------------
#       Start of the testing part of the code
#--------------------------------------------------
#
#def main():
#    bond = Bond(value=50, volume=100)
#    print(bond.update(5))
#
#    
#if __name__ == "__main__":
#    main()
#    

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
