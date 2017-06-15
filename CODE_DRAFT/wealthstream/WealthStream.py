# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 11:10:06 2017

@author: FR015797 (aka Laurent DEBRIL)
"""

#--------------------------------------------------
#           Project packages
#--------------------------------------------------
from Assets import Assets
from Liabilities import Liabilities
from Bond import Bond
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
    
    def __init__(self, asset1, liability1, value=0, time_horizon=50): 
        self.time_horizon = time_horizon
        
        self.liabilities = [liability1]
        self.assets = [asset1]
        self.value = pd.DataFrame(data=value, index=np.arange(1,self.time_horizon+1), columns=['Stream Value']) 
        for e in self.liabilities:
            self.value.loc[:, 'Stream Value'] -= e.value.loc[:, 'Contract Value']
        for e in self.assets:
            if(type(e).__name__ == 'Bond'):
                self.value.loc[:, 'Stream Value'] += e.value.loc[:, 'Market Value']*e.volume.loc[:, 'Volume']
            elif(type(e).__name__ == 'Equity'):
                self.value.loc[:, 'Stream Value'] += e.value.loc[:, 'Market Value']*e.volume.loc[:, 'Volume']
            elif(type(e).__name__ == 'Cash'):
                self.value.loc[:, 'Stream Value'] += e.value.loc[:, 'Market Value']*e.volume.loc[:, 'Volume']
        
    def _addWealth_(self, amount, current_step): # METHODE QUI EVOLUERA PAR LA SUITE: V1 (TRES) SIMPLIFIEE
        self.value.loc[current_step, 'Stream Value'] += amount
        # IDEE DE LA METHODE:
        # augmenter le flux = effectuer PVL ou vendre assets les plus proches de la maturité
        # diminuer les assets
        # e.sort(key=lambda x: x.maturity, reverse=True) on trie selon l'expiration à maturité
        
    def _reduceWealth_(self, amount, current_step):
        self.value.loc[current_step, 'Stream Value'] -= amount
        # IDEE DE LA METHODE: List(source) en entree
        # diminuer le flux
        # reduire l'actif = effectuer des MVL
        # e.sort(key=lambda x: x.maturity, reverse=True)
        
    def add(self, new_asset, mode='Market Value'): 
        self.assets.append(new_asset)    
        if(type(self.assets[-1]).__name__ == 'Bond'):
            self.value.loc[:, 'Stream Value'] += self.assets[-1].value.loc[:, mode] * self.assets[-1].volume.loc[:, 'Volume']
        elif(type(self.assets[-1]).__name__ == 'Equity'):
            self.value.loc[:, 'Stream Value'] += self.assets[-1].value.loc[:, mode] * self.assets[-1].volume.loc[:, 'Volume']
        elif(type(self.assets[-1]).__name__ == 'Cash'):
            self.value.loc[:, 'Stream Value'] += self.assets[-1].value.loc[:, mode] * self.assets[-1].volume.loc[:, 'Volume']
        
    def substract(self, new_liability):
        self.liabilites.append(new_liability)    
        self.value['Stream Value'] -= self.assets[-1].value['Value']

    def computeWealth(self):
        for asset in self.assets:
            if(type(asset).__name__ == 'Bond'):
                self.value.loc[:, 'Stream Value'] += asset.value.loc[:, 'Market Value'] * asset.volume.loc[:, 'Volume']
            elif(type(asset).__name__ == 'Equity'):
                self.value.loc[:, 'Stream Value'] += asset.value.loc[:, 'Market Value'] * asset.volume.loc[:, 'Volume']
            elif(type(asset).__name__ == 'Cash'):
                self.value.loc[:, 'Stream Value'] += asset.value.loc[:, 'Market Value'] * asset.volume.loc[:, 'Volume']
        
        for liability in self.liabilities:
            self.value.loc[:, 'Stream Value'] -= liability.value.loc[:, 'Value'] * asset.volume.loc[:, 'Volume']
        
        
    def transferWealth(self, other_wealthstream, amount, current_step, direction=1): # transfère de la richesse d'un flux à l'autre (ex: PG -> available wealth)
        """
            principe des vases communiquant
        """
        if(direction == 1):
            assert(other_wealthstream.value.loc[current_step, 'Stream Value'] >= amount)
            self.value.loc[current_step, 'Stream Value'] += amount
            other_wealthstream.value.loc[current_step, 'Stream Value'] -= amount
        elif(direction == -1):
            assert(self.value.loc[current_step, 'Stream Value'] >= amount)
            self.value.loc[current_step, 'Stream Value'] -= amount
            other_wealthstream.value.loc[current_step, 'Stream Value'] += amount
        # on augmente le wealth si direction=1, diminue si =-1
        # on prend le wealthstream du flux1, on l'ajoute au flux 2
        # on diminue en consequence le flux1 (utilisation de la fonction sell, cashout et instanciation d'un nouvel instrument Actif ou versement provision)
        #e.sort(key=lambda x: (x.value-amount), reverse=True) = celui dont la value est la plus proche du montant visé
        
    def __str__(self):
     return self.value.__str__()
 
#--------------------------------------------------
#       Start of the testing part of the code
#--------------------------------------------------
#
#def main():
#    import copy
#    assets = Assets()
#    myAsset = assets.portfolio[0]
#    myAsset.value.loc[:, 'Market Value'] = 1
#    myAsset.volume.loc[:, 'Volume'] = 1000
#    
#    liabilities = Liabilities()
#    myLiability = liabilities.math_provision[0]
#    myLiability.value.loc[:, 'Contract Value'] = 500 
#    
#    stream1 = WealthStream(asset1=myAsset, liability1=myLiability)
#    stream2 = copy.deepcopy(stream1)
#    stream2.value.loc[:, 'Stream Value'] = 400
##    stream._addWealth_(500, 20)
##    stream._reduceWealth_(400, 30)
#    
#    df = stream1.value.plot()
#    stream2.value.plot(ax=df)
#    df.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
#    
#    mean = 200
#    std = 50
#    i=20
##    for i in range(20, 41):
#    noise = np.random.normal(mean, std, size=1)
#    stream1.transferWealth(other_wealthstream=stream2, amount=noise, current_step=i, direction=-1)
#    
#    df = stream1.value.plot(title= 'Test de la méthode transferWealth()')
#    stream2.value.plot(ax=df)
#    df.legend(["WStream 1", "WStream 2"], loc='center left', bbox_to_anchor=(1.0, 0.5))
##    import gc 
##    gc.enable() # Nettoyage dynamique de la RAM
#
#if __name__ == "__main__":
#    main()