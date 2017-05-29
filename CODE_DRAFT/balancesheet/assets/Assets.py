# -*- coding: utf-8 -*-
"""
Created on Thu May 18 10:01:38 2017

@author: Laurent DEBRIL
Date of last revision: May 23rd 2017

"""

#--------------------------------------------------
#           Project packages
#--------------------------------------------------
from Bond import Bond
from Equity import Equity
from Cash import Cash
#--------------------------------------------------
#           Python packages
#--------------------------------------------------
import numpy as np
import pandas as pd
#--------------------------------------------------
#       Start of the proper code
#--------------------------------------------------

class Assets(object):
    def __init__(self, nbBond=1, nbEquity=1, nbCash=1, \
                 ratio={'Bond':.7, 'Equity':.2, 'Cash':.1},\
                 wealth = 1000, time_horizon=25):
        self.portfolio = []
        self.nbBond = nbBond
        self.nbEquity = nbEquity
        self.nbCash = nbCash
        self.wealth = wealth
        self.time_horizon = time_horizon
        
        # we create the portfolio according to our specifications (ratio equity classes):
        for _ in range(self.nbBond):
            self.portfolio.append(Bond(value=1, volume=self.wealth*ratio['Bond']/self.nbBond, time_horizon=self.time_horizon))
        for _ in range(self.nbEquity):
            self.portfolio.append(Equity(value=1, volume=self.wealth*ratio['Equity']/self.nbEquity, time_horizon=self.time_horizon))
        for _ in range(self.nbCash):
            self.portfolio.append(Cash(value=1, volume=self.wealth*ratio['Cash']/self.nbCash, time_horizon=self.time_horizon))
        
    
    def computePortfolioVal(self): 
        value = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1), columns=['Portfolio Value'])
        for asset in self.portfolio:
            if(type(asset).__name__ == 'Bond'):
                value['Portfolio Value'] += asset.value['Book Value'] * asset.volume['Volume']
            elif(type(asset).__name__ == 'Equity'):
                value['Portfolio Value'] += asset.value['Book Value'] * asset.volume['Volume']
            elif(type(asset).__name__ == 'Cash'):
                value['Portfolio Value'] += asset.value['Value'] * asset.volume['Volume']
        return value
    
    def computePortfolioPGL(self): 
        value = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1), columns=['Portfolio PGL'])
        for asset in self.portfolio:
            if(type(asset).__name__ == 'Bond'):
                value['Portfolio PGL'] += asset.potential['Potential Gain'] * asset.volume['Volume']
                value['Portfolio PGL'] += asset.potential['Potential Loss'] * asset.volume['Volume']
            elif(type(asset).__name__ == 'Equity'):
                value['Portfolio PGL'] += asset.potential['Potential Gain'] * asset.volume['Volume']
                value['Portfolio PGL'] += asset.potential['Potential Loss'] * asset.volume['Volume']
        return value
    
    def computeBondPGL(self):
        value = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1), columns=['Bonds PGL'])
        for asset in self.portfolio:
            if(type(asset).__name__ == 'Bond'):
                value['Bonds PGL'] += asset.potential['Potential Gain'] * asset.volume['Volume']
                value['Bonds PGL'] += asset.potential['Potential Loss'] * asset.volume['Volume']
        return value
    
    def computeEQPGL(self):
        value = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1), columns=['Equities PGL'])
        for asset in self.portfolio:
            if(type(asset).__name__ == 'Equity'):
                value['Equities PGL'] += asset.potential['Potential Gain'] * asset.volume['Volume']
                value['Equities PGL'] += asset.potential['Potential Loss'] * asset.volume['Volume']
        return value
    
    def update(self, current_step):
        for e in self.portfolio:
            e.update(current_step)
            if(e.flag != 0):
                self.portfolio.append(Bond(value=1, volume=e.flag,\
                                 starting_point=current_step, time_horizon=self.time_horizon))
                self.portfolio[-1].volume.loc[current_step, 'Volume'] = 0  # ----------- ATTENTION -------------
                e.flag = 0 
                # on réinvestit automatiquement le nominal

    def clear(self):
       total_amount = 0
       for asset in self.portfolio:
           total_amount += asset.cashOut(self.time_horizon)
       return total_amount

#--------------------------------------------------
#       Start of the testing part of the code
#--------------------------------------------------
#
def main():
    step = 1
    assets = Assets(wealth=100, time_horizon=50) 
    for i in range(step,assets.time_horizon):
        assets.update(i)
    assets.clear()
    
    for asset in assets.portfolio:
        if(type(asset).__name__=='Cash'):
            print(asset.value['Value'] * asset.volume['Volume'])
        else:
            print(asset.value['Book Value'] * asset.volume['Volume'])
    assets.computePortfolioVal().plot()

##    
##    ------------ Save option -----------------
#    path = r'C:\Users\FR015797\Documents\PyALM_gen\code\alm\balancesheet\assets'
#    filename = '\save1.csv'
#    new_file = check.to_csv(path+filename, sep=';')
#

if __name__ == "__main__":
    main()