# -*- coding: utf-8 -*-
"""
Created on Thu May 18 10:01:38 2017

@author: FR015797
Date of last revision: August 1st 2017
"""


#--------------------------------------------------
#           Project packages
#--------------------------------------------------
from Asset import Asset
#--------------------------------------------------
#           Python packages
#--------------------------------------------------
import numpy as np
import pandas as pd
#--------------------------------------------------
#       Start of the proper code
#--------------------------------------------------

class Cash(Asset):   
    """
        represents Cash-like instruments. 
        
        This class inherited from the *Asset* class
        
        :param value: Time serie of the value of the Equity over time
        :param time_horizon: Duration of the simulation
        :param starting_point: Point of time in the simulation when the instrument is emitted
        :param flag: hidden variables equal to 0 by default
        :param return_rate: Time serie of the value of the interest rate of the Equity over time
        :param potential: Time serie of the potential gain & loss on the Equity
        :type value: DataFrame of Float
        :type time_horizon: Integer
        :type starting_point: Integer
        :type flag: Float
        :type return_rate: DataFrame of Float
        :type potential: DataFrame of Float
        :return: An instance of the Cash class
        :rtype: Cash object
    """     
    def cashOut(self, current_step):
        """
            cashes out the amount of money generated by the Equity
        """
        output = {}
        if(current_step < self.time_horizon):
            output['all'] = self.value.loc[current_step, 'Market Value']
            self.value.loc[current_step+1:self.time_horizon, 'Market Value'] = 0
            output['pnl'] = 0
        return output    
    
    def getWealth(self, current_step):
        """
            returns the amount of money represented by the Equity at a certain point in time
        """
        return self.value.loc[current_step, 'Market Value']

    def updateValue(self, current_step): # actualisation debut de periode
        """
            capitalizes the Equity over a period of time
        """
        res = self.value.loc[current_step, 'Market Value'] * self.return_rate.loc[current_step, 'RRate']
        self.value.loc[current_step:self.time_horizon, 'Market Value'] = self.value.loc[current_step, 'Market Value'] + res
        return res
    
    def update(self, current_step, current_yield=None, spreads=None):
        """
            updates the Equity over a period of time
        """
        res = 0
        if(current_step>=self.starting_point):
            res = self.updateValue(current_step)
        self.value.loc[:, 'Book Value'] = self.value.loc[:, 'Market Value']
        return res
    
#--------------------------------------------------
#       Start of the testing part of the code
#--------------------------------------------------
#
#def main():
#    import gc
#    gc.enable()
#    
#    cash = Cash(value=100)
#    for i in range(1,cash.time_horizon+1):
#        cash.update(i)
#        if(i==10):
#            print(cash.sell(amount=cash.value.loc[i, 'Market Value'], current_step=i))
#    df = cash.value.plot(title='Evolution de la valeur du Cash au cours de simulation')
#    print(cash.value)
##    df.axvline(21, color='k', linewidth=1, linestyle='--')
#
##    df.grid(True)
#    
#if __name__ == "__main__":
#    main()