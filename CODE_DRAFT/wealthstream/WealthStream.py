# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 11:10:06 2017

@author: FR015797 (aka Laurent DEBRIL)
"""

#--------------------------------------------------
#           Project packages
#--------------------------------------------------
#from Assets import Assets
#from Liabilities import Liabilities
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
    
    def __init__(self, plus=None, minus=None, value=0, time_horizon=50): 
        self.time_horizon = time_horizon
        """
            minus and plus must be 1-dimensional positive-only DataFrame (aka Series) in order to work properly
        """
        self.time_horizon = time_horizon
        self.pluses = []
        self.minuses = []
        if(plus != None):
            self.pluses.append(plus)
        if(minus != None):
            self.minuses.append(minus)
        self.value = pd.DataFrame(data=value, index=np.arange(1,self.time_horizon+1), columns=['Stream Value']) 
        self.computeWealth()
        
    def _addWealth_(self, amount, current_step): 
        self.value.loc[current_step, 'Stream Value'] += amount
        
    def _reduceWealth_(self, amount, current_step):
        self.value.loc[current_step, 'Stream Value'] -= amount
        
    def add(self, plus): 
        self.pluses.append(plus)    
        self.value.loc[:, 'Stream Value'] += self.pluses[-1].iloc[:]

    def substract(self, minus):
        self.minuses.append(minus)    
        self.value['Stream Value'] -= self.minuses[-1].iloc[:]

    def computeWealth(self):
        for e in self.minuses:
            if(e != None):
                self.value.loc[:, 'Stream Value'] -= e.iloc[:]
        for e in self.pluses:
            if(e != None):
                self.value.loc[:, 'Stream Value'] += e.iloc[:]
        
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
        # e.sort(key=lambda x: (x.value-amount), reverse=True) = celui dont la value est la plus proche du montant visé
        
    def __str__(self):
     return self.value.__str__()
 
#--------------------------------------------------
#       Start of the testing part of the code
#--------------------------------------------------
#
#def main():
#    import copy
#    import gc 
#    gc.enable() # Nettoyage dynamique de la RAM
##    ---------------------------------------------
#    
#    stream1 = WealthStream()
#    stream1.value.loc[:, 'Stream Value'] = 200
#    stream2 = copy.deepcopy(stream1)
#    stream2.value.loc[:, 'Stream Value'] = 400
    
#    mean = 0
#    std = 10
#    noise1 = np.random.normal(mean, std, size=stream1.time_horizon)
#    noise2 = np.random.poisson(size=stream1.time_horizon)
#
#    series1 = pd.Series(data=noise1, index=np.arange(1,stream1.time_horizon+1))
#    series2 = pd.Series(data=noise2, index=np.arange(1,stream1.time_horizon+1))
#    
##    s = series1.plot(title='Evolution des Series - bruit blanc')
##    series2.plot(ax=s)
##    s.legend(['Serie 1', 'Serie 2'], loc='center left', bbox_to_anchor=(1.0, 0.5))
#    
#    stream1.add(series1)
#    stream1._reduceWealth_(amount=1000, current_step=20)
##    stream1.substract(series1)
#    stream2.add(series2)
#    df = stream1.value.plot()
#    stream2.value.plot(ax=df)
#    df.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
#    
#
#if __name__ == "__main__":
#    main()