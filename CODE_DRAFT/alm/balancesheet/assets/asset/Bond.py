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
    def __init__(self, face_value=1, value=1, time_horizon=50,\
                 starting_point=1, coupon=0, MAX_MATURITY=30, \
                 rating="AAA", default_proba=0, \
                 currency="Euro", book_yield=0): 
        self.starting_point = starting_point
        self.time_horizon = time_horizon
        self.flag = 0
        
        self.MAX_MATURITY = MAX_MATURITY # in years
        self.maturity = self.MAX_MATURITY # decrease each year until expiring at 0 thus delivering back the face value
        
        # Initialisation du book_yield
        USrate = (np.asarray([1.22,	1.35,	1.51,	1.65,	1.78,	1.89,	1.98,	2.06,	2.13,	2.19,	2.24,	2.29,	2.33,\
                              2.37,	2.41,	2.45,	2.49,	2.53,	2.56,	2.60,	2.63,	2.67,	2.70,	2.73,	2.77,	2.80,\
                              2.83,	2.86,	2.89,	2.91])/100).transpose()
        self.book_yield = pd.DataFrame(data=USrate, index=np.arange(1,MAX_MATURITY+1), columns=['RRate'])
        # Initialisation de value
        self.value = pd.DataFrame(data=value, index=np.arange(1,time_horizon+1), columns=['Market Value', 'Face Value', 'Book Value']) #interversion face et book
        self.value.loc[:starting_point-1, 'Book Value'] = 0
        self.value.loc[:starting_point-1, 'Market Value'] = 0
        self.value.loc[:starting_point-1, 'Face Value'] = 0
        self.value.loc[self.starting_point:self.time_horizon, 'Face Value'] = value * \
                    np.power((1 + self.book_yield.loc[self.MAX_MATURITY, 'RRate']), self.MAX_MATURITY)

        # Initialisation des deflators
        self.deflators = pd.DataFrame(data=1, index=np.arange(1,time_horizon+1), columns=['Deflators'])

        # Initialisation des PGL
        self.potential = pd.DataFrame(data=0, index=np.arange(1,time_horizon+1), columns=['Potential Gain', 'Potential Loss'])
        self.computePotential()   

        self.rating = rating
        self.default_proba = default_proba
        self.currency = currency
        self.coupon = coupon # number of coupons    

    def cashOut(self, current_step): # on n'appelle la methode cashOut qu'a maturite i.e. on recupere le nominal (Face Value) et non revente a la Market Value
        output = {}
        
        if(self.maturity > 0):
            output['all'] = self.value.loc[self.starting_point, 'Market Value']
            output['pnl'] = output['all'] - self.value.loc[current_step, 'Book Value']
            self.value.loc[np.arange(current_step+1,self.time_horizon+1), 'Market Value'] = 0
            self.value.loc[np.arange(current_step+1,self.time_horizon+1), 'Book Value'] = 0
            self.value.loc[np.arange(current_step+1,self.time_horizon+1), 'Face Value'] = 0
        else:
            output['all'] = self.value.loc[self.starting_point, 'Face Value']
            output['pnl'] = 0
            self.value.loc[np.arange(current_step+1,self.time_horizon+1), 'Market Value'] = 0
            self.value.loc[np.arange(current_step+1,self.time_horizon+1), 'Book Value'] = 0
            self.value.loc[np.arange(current_step+1,self.time_horizon+1), 'Face Value'] = 0
        return output

   
    def sell(self, amount, current_step): # on vend avant maturite donc on recupere la somme en Market Value et non en nominal (Face Value)
        self.computePotential()
        denom = 1 + (self.potential.loc[current_step, 'Potential Gain'] \
                     + self.potential.loc[current_step, 'Potential Loss']) * 1/self.value.loc[current_step, 'Market Value']
        real_amount = amount/denom
        ratio = real_amount/self.value.loc[current_step, 'Market Value']
        if(ratio <= 1):
            self.value.loc[current_step:self.time_horizon, 'Market Value'] -= ratio \
                * self.value.loc[current_step, 'Market Value'] 
            self.value.loc[current_step:self.time_horizon, 'Book Value'] -= ratio \
                * self.value.loc[current_step, 'Book Value']
            self.value.loc[current_step:self.time_horizon, 'Face Value'] -= ratio \
                * self.value.loc[current_step, 'Face Value']           
        self.computePotential()
        return amount

    def updateValue(self, current_step, current_yield, spreads): # assertion: self.maturity > 0
        # zero-coupon hypothesis
        # Book Value amortization
        res = self.value.loc[current_step, 'Market Value']
        denom1 = np.power((1 + self.book_yield.loc[self.maturity, 'RRate']), (self.maturity-1))
        self.value.loc[current_step:self.time_horizon, 'Book Value'] = self.value.loc[max(self.starting_point, current_step-1), 'Face Value'] / denom1
#        # Market Value updating
        denom2 = np.power((1 + current_yield.loc[self.maturity] + spreads.loc[self.maturity]), (self.maturity-1))
        self.value.loc[current_step:self.time_horizon, 'Market Value'] = self.value.loc[max(self.starting_point, current_step-1), 'Face Value'] / denom2
        if(current_step > self.starting_point):
            res = self.value.loc[current_step, 'Market Value'] - res
        else: 
            res = 0
        return res # valeur apres actualisation - valeur avant actualisation = benefices financiers de l'annee
    
    def update(self, current_step, current_yield, spreads):
        res= 0
        if(current_step>=self.starting_point):
            if(self.maturity>0 and current_step>=self.starting_point):
                res = self.updateValue(current_step, current_yield, spreads)
            self.maturity -= 1
            if(self.maturity==0 and self.value.loc[current_step, 'Market Value']>0):
                self.flag = self.cashOut(current_step)
        return res 
    
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
#
#def main():
#    import gc
#    gc.enable()
#    
#    bond = Bond(value=100, starting_point=10, MAX_MATURITY=30)
#    # ---------------------------------
#    noise = 0#np.random.normal(0, .01, size=30)
#    USrate = (np.asarray([1.22,	1.35,	1.51,	1.65,	1.78,	1.89,	1.98,	2.06,	2.13,	2.19,	2.24,	2.29,	2.33,	2.37,	2.41,	2.45,	2.49,	2.53,	2.56,	2.60,	2.63,	2.67,	2.70,	2.73,	2.77,	2.80,	2.83,	2.86,	2.89,	2.91])/100+noise).transpose()
#    yield_curve = pd.DataFrame(data=USrate, index=np.arange(1,len(USrate)+1), columns=['RRate'])
#    spreads = pd.DataFrame(data=0, index=np.arange(1,len(USrate)+1), columns=['Spreads'])
#    # ---------------------------------
#    test = pd.DataFrame(data=0, index=np.arange(1,bond.time_horizon+1), columns=['Test Value'])
#    for i in range(1, bond.time_horizon+1):
#        tmp = bond.update(i, yield_curve.loc[:, 'RRate'], spreads.loc[:, 'Spreads'])
#        test.loc[i, 'Test Value'] = tmp
##        if(i==20):
##            bond.sell(75, i)
##    df= test.plot()
##    df.grid(True)
#    bond.value.plot()
#    print(bond.value)
#
#if __name__ == "__main__":
#    main()