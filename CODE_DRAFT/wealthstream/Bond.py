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
        represents Bond-like instruments. 
        
        This class inherited from the *Asset* class
        
        :param value: Time serie of the value of the Equity over time
        :param time_horizon: Duration of the simulation
        :param starting_point: Point of time in the simulation when the instrument is emitted
        :param flag: hidden variables equal to 0 by default
        :param book_yield: Time serie of the value of the interest rate of the Equity over time
        :param potential: Time serie of the potential gain & loss on the Equity
        :param rating: Moody's credit rating
        :param default_proba: default's probability
        :param currency: currency of the bond emission
        :param coupon: number of coupons offered by the bond
        :type value: DataFrame of Float
        :type time_horizon: Integer
        :type starting_point: Integer
        :type flag: Float
        :type book_yield: DataFrame of Float
        :type potential: DataFrame of Float
        :param rating: String
        :param default_proba: float
        :param currency: String
        :param coupon: Integer
        :return: An instance of the Equity class
        :rtype: Equity object
    """
    def __init__(self, face_value=1, value=1, time_horizon=20,\
                 starting_point=1, coupon=0, MAX_MATURITY=10, \
                 rating="AAA", default_proba=0, \
                 currency="Euro", book_yield=0): 
        self.starting_point = starting_point
        self.time_horizon = time_horizon
        self.flag = 0
        
        self.MAX_MATURITY = MAX_MATURITY # in years
        self.maturity = self.MAX_MATURITY # decrease each year until expiring at 0 thus delivering back the face value
        
        # Initialisation du book_yield
        self.book_yield = pd.DataFrame(data=0, index=np.arange(1,time_horizon+1), columns=['RRate'])
        self.book_yield.loc[starting_point:self.time_horizon, 'RRate'] = book_yield
        # Initialisation de value
        self.value = pd.DataFrame(data=face_value, index=np.arange(1,time_horizon+1), columns=['Market Value', 'Book Value', 'Face Value'])
        self.value.loc[:starting_point-1, 'Book Value'] = 0
        self.value.loc[:starting_point-1, 'Face Value'] = 0
        self.value.loc[:starting_point-1, 'Market Value'] = 0

        # Initialisation des deflators
        self.deflators = pd.DataFrame(data=1, index=np.arange(1,time_horizon+1), columns=['Deflators'])

        # Initialisation des PGL
        self.potential = pd.DataFrame(data=0, index=np.arange(1,time_horizon+1), columns=['Potential Gain', 'Potential Loss'])
        self.computePotential()   

        self.rating = rating
        self.default_proba = default_proba
        self.currency = currency
        self.coupon = coupon # number of coupons    

    def cashOut(self, current_step):
        output = {}
        output['all'] = self.value.loc[current_step, 'Market Value']
        if(current_step<self.time_horizon):
            output['pnl'] = output['all'] - self.value.loc[current_step, 'Book Value']
            self.value.loc[np.arange(current_step+1,self.time_horizon+1), 'Market Value'] = 0
            self.value.loc[np.arange(current_step+1,self.time_horizon+1), 'Book Value'] = 0
            self.value.loc[np.arange(current_step+1,self.time_horizon+1), 'Face Value'] = 0
        return output
   
    def sell(self, amount, current_step):
        res = 0
        if(amount <= self.value.loc[current_step, 'Market Value']):
            self.value.loc[current_step+1:self.time_horizon, 'Market Value'] -= amount 
            self.value.loc[current_step+1:self.time_horizon, 'Face Value'] -= amount
            self.value.loc[current_step+1:self.time_horizon, 'Book Value'] -= amount
            if(self.value.loc[current_step+1, 'Book Value'] < 0):
                res = -self.value.loc[current_step+1:self.time_horizon, 'Book Value'] # s'il renvoit une valeur>0 = Plus Value, <0 = Moins Value
                self.value.loc[current_step+1:self.time_horizon, 'Book Value'] = 0
        return res

    def updateValue(self, current_step, current_yield, spreads): 
        # zero-coupon hypothesis
        # Book Value amortization
        denom1 = np.power((1 + self.book_yield.loc[self.maturity, 'RRate']), (self.MAX_MATURITY - self.maturity))
        self.value.loc[current_step:self.time_horizon, 'Book Value'] = self.value.loc[self.starting_point, 'Face Value'] / denom1
#        # Market Value updating
        denom2 = np.power((1 + current_yield.loc[self.maturity, 'RRate'] + spreads.loc[self.maturity, 'Spreads']), (self.MAX_MATURITY - self.maturity))
        self.value.loc[current_step:self.time_horizon, 'Market Value'] = self.value.loc[self.starting_point, 'Face Value'] / denom2
        
    def update(self, current_step, current_yield, spreads):
        if(current_step >= self.starting_point):
            if(self.maturity == 0):
                self.flag = self.cashOut(current_step)
            elif(self.maturity > 0):
                self.updateValue(current_step, current_yield, spreads)
            self.maturity -= 1

    def getWealth(self, current_step):
        return (self.value.loc[current_step, 'Market Value'])

    def getWealthPlus(self, current_step):
        self.computePotential()   
        return self.getWealth(current_step) + self.potential.loc[current_step, 'Potential Gain']
        
    def getWealthMinus(self, current_step):
        self.computePotential()   
        return self.getWealth(current_step) + self.potential.loc[current_step, 'Potential Loss']
   
    def computePotential(self):
        self.potential["Potential Gain"] = np.where(self.value.loc[:, 'Market Value'] - self.value.loc[:, 'Book Value'] >0, (self.value.loc[:, 'Market Value'] - self.value.loc[:, 'Book Value']), 0)
        self.potential["Potential Loss"] = np.where(self.value.loc[:, 'Market Value'] - self.value.loc[:, 'Book Value'] <0, (self.value.loc[:, 'Market Value'] - self.value.loc[:, 'Book Value']), 0)

    def __str__(self):
     return (self.value['Market Value']).__str__()

#--------------------------------------------------
#       Start of the testing part of the code
#--------------------------------------------------

#def main():
#    import gc
#    gc.enable()
#    bond = Bond(starting_point=10, face_value=100)
#    yield_curve = pd.DataFrame(data=abs(np.random.normal(20,5, size=bond.time_horizon)), index=np.arange(1,bond.time_horizon+1), columns=['RRate'])
#    bond.book_yield = pd.DataFrame(data=np.log(np.arange(101, 121, 1)), index=np.arange(1,bond.time_horizon+1), columns=['RRate'])
#
#    for i in range(1, 51):
#        bond.update(i, yield_curve, pd.DataFrame(data=0, index=np.arange(1,bond.time_horizon+1), columns=['Spreads']))
#    bond.value.plot()
#    bond.computePotential()
#    bond.potential.plot()
#
#if __name__ == "__main__":
#    main()