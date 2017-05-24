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
                 wealth = 1000, time_horizon=50):
        self.portfolio = []
        self.nbBond = nbBond
        self.nbEquity = nbEquity
        self.nbCash = nbCash
        self.wealth = wealth
        self.time_horizon = time_horizon
        
        # we create the portfolio according to our specifications (ratio equity classes):
        for _ in range(self.nbBond):
            self.portfolio.append(Bond(value=1, volume=self.wealth*ratio['Bond']/self.nbBond))
        for _ in range(self.nbEquity):
            self.portfolio.append(Equity(value=1, volume=self.wealth*ratio['Equity']/self.nbEquity))
        for _ in range(self.nbCash):
            self.portfolio.append(Cash(value=1, volume=self.wealth*ratio['Cash']/self.nbCash))
        
    
    def computePortfolioVal(self): 
        value = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1), columns=['Portfolio Value'])
        for asset in self.portfolio:
            if(type(asset).__name__ == 'Bond'):
                value['Portfolio Value'] += asset.value['Market Value'] * asset.volume['Volume']
            elif(type(asset).__name__ == 'Equity'):
                value['Portfolio Value'] += asset.value['Market Value'] * asset.volume['Volume']
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
    
#    def update(self, current_step):
#       for asset in self.portfolio:
#           tmp = asset.update(current_step)
##           if(tmp != 0):
##               self.portfolio.append(Bond(value=tmp)) 
##                on réinvestit automatiquement le nominal
                      
    def clear(self):
       total_amount = 0
       for asset in self.portfolio:
           total_amount += asset.cashOut(self.time_horizon)
       return total_amount

#--------------------------------------------------
#       Start of the testing part of the code
#--------------------------------------------------

def main():
#    step = 1
    portfolio = Assets(wealth=1000) 
    print(portfolio.computePortfolioVal())
    for asset in portfolio.portfolio:
        print(id(asset))
#    print(portfolio.clear())
#    print(portfolio.portfolio[0].volume)
#    portfolio.portfolio[0].cashOut(45)
#    print(portfolio.portfolio[0].volume)
#    for i in range(1,11):
#        for asset in portfolio.portfolio:
#            asset.update(i)
        
#    print(portfolio.computePortfolioVal())    
    print(portfolio.portfolio)
    for asset in portfolio.portfolio:
        print(id(asset))
        
if __name__ == "__main__":
    main()