# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 11:10:06 2017

@author: FR015797 (aka Laurent DEBRIL)
"""

#--------------------------------------------------
#           Project packages
#--------------------------------------------------
from Assets import Assets
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
    
    def __init__(self, plus=None, minus=None, time_horizon=50): 
        self.time_horizon = time_horizon
        """
            minus and plus must be 1-dimensional positive-only DataFrame (aka Series) in order to work properly
        """
        self.time_horizon = time_horizon
        self.pluses = []
        self.minuses = []
        if(plus):
            self.pluses.append(plus)
        if(minus):
            self.minuses.append(minus)
        self.value = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1), columns=['Stream Value']) 
        self.computeWealth()
        
    def add(self, plus): # define the name of the Series to quickly retrieve the right one
        self.pluses.append(plus)    
        self.value.loc[:, 'Stream Value'] += self.pluses[-1].iloc[:]

    def substract(self, minus):
        self.minuses.append(minus)    
        self.value.loc[:, 'Stream Value'] -= self.minuses[-1].iloc[:]

    def computeWealth(self):
        self.value.loc[:, 'Stream Value'] = 0
        for e in self.minuses:
            if(not e.empty):
                self.value.loc[:, 'Stream Value'] -= e.iloc[:]
        for e in self.pluses:
            if(not e.empty):
                self.value.loc[:, 'Stream Value'] += e.iloc[:]
        
    # OBSOLETE -----------------------------------
    def _addWealth_(self, amount, current_step): 
        self.value.loc[current_step, 'Stream Value'] += amount
        
    def _reduceWealth_(self, amount, current_step):
        self.value.loc[current_step, 'Stream Value'] -= amount
        
    def _transferWealth_(self, other_wealthstream, amount, current_step, direction=1): # transfère de la richesse d'un flux à l'autre (ex: PG -> available wealth)
        """
            principe des vases communiquant
        """
        if(direction == 1):
            assert(other_wealthstream.value.loc[current_step, 'Stream Value'] >= amount)
            self._addWealth_(amount, current_step)
            other_wealthstream._reduceWealth_(amount, current_step)
        elif(direction == -1):
            assert(self.value.loc[current_step, 'Stream Value'] >= amount)
            self._reduceWealth_(amount, current_step)
            other_wealthstream._addWealth_(amount, current_step)
        # on augmente le wealth si direction=1, diminue si =-1
        # on prend le wealthstream du flux1, on l'ajoute au flux 2
        # on diminue en consequence le flux1 (utilisation de la fonction sell, cashout et instanciation d'un nouvel instrument Actif ou versement provision)
        # e.sort(key=lambda x: (x.value-amount), reverse=True) = celui dont la value est la plus proche du montant visé
    # ---------------------------------------------
    
    def __str__(self):
     return self.value.__str__()
 
    def __add__(self, wstream2):
        result = WealthStream(time_horizon=self.time_horizon)
        for e in self.pluses:
            result.pluses.append(e)
        for e in wstream2.pluses:
            result.pluses.append(e)
        for e in self.minuses:
            result.minuses.append(e)
        for e in wstream2.minuses:
            result.minuses.append(e)
        result.computeWealth()
        return result

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
#    stream2 = copy.deepcopy(stream1)
#    a = Assets()
#
#
#    series1 = pd.Series(data=400, index=np.arange(1,stream1.time_horizon+1))
#    series2 = pd.Series(data=200, index=np.arange(1,stream1.time_horizon+1))
#   
#    stream1.add(series1)
#    stream1.add(series2)
#    stream2 = stream1 + stream1
#    
#    print(stream1.pluses)
#    df = stream1.value.plot()
#    stream2.value.plot(ax=df)
#    df.legend(['Stream 1', 'Stream 2'], loc='center left', bbox_to_anchor=(1.0, 0.5))
#    
#
#if __name__ == "__main__":
#    main()