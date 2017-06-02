# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 11:10:06 2017

@author: FR015797 (aka Laurent DEBRIL)
"""

#--------------------------------------------------
#           Project packages
#--------------------------------------------------
import Assets as Assets
import Liabilities as Liabilities
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
        value: A value of the rate over time (DataFrame of Float)
        time_horizon: The time horizon over which the simulation takes place (integer).
    """
    
    def __init__(self, time_horizon=50, asset1, liability1, value=0): 
        self.time_horizon = time_horizon
        
        self.liabilities = liability1
        self.assets = asset1
        self.value = pd.DataFrame(data=value, index=np.arange(1,self.time_horizon+1), columns=['Stream Value']) 
        for e in self.liabilities:
            self.value['Stream Value'] -= e.value['Value']
        for e in self.assets:
            if(type(e).__name__ == 'Bond'):
                self.value['Stream Value'] += e.value['Book Value']
            elif(type(e).__name__ == 'Equity'):
                self.value['Stream Value'] += e.value['Book Value'] # a modifier par Market Value plus tard
            elif(type(e).__name__ == 'Cash'):
                self.value['Stream Value'] += e.value['Value']
            
        
    def addWealth(self, Float, Integer): # méthode la plus technique à implémenter car régit toutes les interactions d'atteinte de taux
        pass
        # augmenter le flux = effectuer PVL ou vendre assets les plus proches de la maturité
        # diminuer les assets
        #e.sort(key=lambda x: x.maturity, reverse=True) on trie selon l'expiration à maturité
        
    def reduceWealth(self, Float, Integer):
        pass
        #diminuer le flux
        # reduire l'actif = effectuer des MVL
        #e.sort(key=lambda x: x.maturity, reverse=True)
        
    def addAsset(self, new_asset): 
        self.assets.append(new_asset)    
        if(type(self.assets[-1]).__name__ == 'Bond'):
            self.value['Stream Value'] += self.assets[-1].value['Book Value']
        elif(type(self.assets[-1]).__name__ == 'Equity'):
            self.value['Stream Value'] += self.assets[-1].value['Book Value'] # a modifier par Market Value plus tard
        elif(type(self.assets[-1]).__name__ == 'Cash'):
            self.value['Stream Value'] += self.assets[-1].value['Value']
        
    def addLiability(self, new_liability):
        self.liabilites.append(new_liability)    
        self.value['Stream Value'] -= self.assets[-1].value['Value']

    def computeWealth(self):
        for asset in self.assets:
            if(type(asset).__name__ == 'Bond'):
                self.value['Stream Value'] += asset.value['Market Value'] * asset.volume['Volume']
            elif(type(asset).__name__ == 'Equity'):
                self.value['Stream Value'] += asset.value['Market Value'] * asset.volume['Volume']
            elif(type(asset).__name__ == 'Cash'):
                self.value['Stream Value'] += asset.value['Value'] * asset.volume['Volume']
        
        for liability in self.liabilities:
            self.value['Stream Value'] -= liability.value['Value'] * asset.volume['Volume']
        
        
    def transferWealth(self, other_wealthstream, amount, direction=1): # transfère de la richesse d'un flux à l'autre (ex: PG -> available wealth)
        pass
        # on augmente le wealth si direction=1, diminue si =-1
        # on prend le wealthstream du flux1, on l'ajoute au flux 2
        # on diminue en consequence le flux1 (utilisation de la fonction sell, cashout et instanciation d'un nouvel instrument Actif ou versement provision)
        #e.sort(key=lambda x: (x.value-amount), reverse=True) = celui dont la value est la plus proche du montant visé
        
    def __str__(self):
     return "The value of the wealth available per year of simulation is \n" + (self.value.__str__())
 
#--------------------------------------------------
#       Start of the testing part of the code
#--------------------------------------------------

def main():
    wealthstream = WealthStream()
    print(wealthstream.__str__())
    
    
if __name__ == "__main__":
    main()