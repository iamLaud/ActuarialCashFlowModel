# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 11:10:06 2017

@author: FR015797 (aka Laurent DEBRIL)
"""

#--------------------------------------------------
#           Project packages
#--------------------------------------------------
#import Assets as Assets
#import Liabilities as Liabilities
#--------------------------------------------------
#           Python packages
#--------------------------------------------------
import numpy as np
import pandas as pd
#--------------------------------------------------
#       Start of the proper code
#--------------------------------------------------

class WealthStream():
    """A class modeling the structure of a stream of wealth as used in the ALM model:

    Attributes:
        value: A value of the rate over time (N-array of floats)
        time_horizon: The time horizon over which the simulation takes place (integer).
    """
    
    def __init__(self, time_horizon=50, liability_list=[], asset_list=[]): 
        self.time_horizon = time_horizon
        self.liabilities = liability_list
        self.assets = asset_list
        value = 0
        self.value = pd.DataFrame(data=value, index=np.arange(1,self.time_horizon+1), columns=['Value']) 
        
    def addWealth(self, Float, Integer): # méthode la plus technique à implémenter car régit toutes les interactions d'atteinte de taux
        pass
    
    def reduceWealth(self, Float, Integer):
        pass
    
    def addAsset(self, new_asset): 
        self.assets.append(new_asset)    

    def addLiability(self, new_liability):
        self.liabilites.append(new_liability)    
        
    def computeWealth(self):
        for asset in self.assets:
            if(type(asset).__name__ == 'Bond'):
                self.value['Value'] += asset.value['Market Value'] * asset.volume['Volume']
            elif(type(asset).__name__ == 'Equity'):
                self.value['Value'] += asset.value['Market Value'] * asset.volume['Volume']
            elif(type(asset).__name__ == 'Cash'):
                self.value['Value'] += asset.value['Value'] * asset.volume['Volume']
        
        for liability in self.liabilities:
            self.value['Value'] -= liability.value['Value'] * asset.volume['Volume']
        
        
    def transferWealth(self, other_wealthstream): # transfère de la richesse d'un flux à l'autre (ex: PG -> available wealth)
        pass
    
    def __str__(self):
     return "The value of the wealth available per year of simulation is \n" + (self.value)
 


#--------------------------------------------------
#       Start of the testing part of the code
#--------------------------------------------------

def main():
    wealthstream = WealthStream()

    
    
if __name__ == "__main__":
    main()