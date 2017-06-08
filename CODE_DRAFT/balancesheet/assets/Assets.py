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
    """
        represents of portfolio of Assets composed of Bonds, Equities and Cash
        
        Assets is basically a List of Asset
    """
    def __init__(self, nbBond=1, nbEquity=1, nbCash=1, \
                 ratio={'Bond':.7, 'Equity':.2, 'Cash':.1},\
                 wealth = 1000, time_horizon=25):
        """
            creates an instance of the Assets class
            
            By default, the portfolio is composed of 1x Bond, 1x Equity and 1x Cash with the following ratio: .7, .2, .1
                and an available wealth of 1000 euros split between these 3 classes of Asset over a 25-year horizon.
                
            :param portfolio: the core of the class
            :param nbBond: the number of Bond instrument composing the portfolio of Assets
            :param nbEquity: the number of Equity instrument composing the portfolio of Assets
            :param nbCash: the number of Cash instrument composing the portfolio of Assets
            :param wealth: the amount of wealth to be invested in the portfolio
            :param time_horizon: the projected duration of the simulation
            :type portfolio: List of Asset
            :type nbBond: Integer
            :type nbEquity: Integer
            :type nbCash: Integer
            :type wealth: Float
            :type time_horizon: Integer
        """
        self.portfolio = []
        self.ratio = ratio
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
        """
            returns the value of the portfolio over the duration of the simulation
        """
        value = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1), columns=['Portfolio Value'])
        for asset in self.portfolio:
            if(type(asset).__name__ == 'Bond'):
                value['Portfolio Value'] += asset.value['Market Value'] * asset.volume['Volume']
            elif(type(asset).__name__ == 'Equity'):
                value['Portfolio Value'] += asset.value['Market Value'] * asset.volume['Volume']
            elif(type(asset).__name__ == 'Cash'):
                value['Portfolio Value'] += asset.value['Market Value'] * asset.volume['Volume']
        return value
    
    def computeEQVal(self):
        value = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1), columns=['EQ Total Value'])
        for asset in self.portfolio:
            if(type(asset).__name__ == 'Equity'):
                value['EQ Total Value'] += asset.value['Market Value'] * asset.volume['Volume']
        return value
    
    def computeBondVal(self):
        value = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1), columns=['Bond Total Value'])
        for asset in self.portfolio:
            if(type(asset).__name__ == 'Bond'):
                value['Bond Total Value'] += asset.value['Market Value'] * asset.volume['Volume']
        return value
    
    def computeCashVal(self):
        value = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1), columns=['Cash Total Value'])
        for asset in self.portfolio:
            if(type(asset).__name__ == 'Cash'):
                value['Cash Total Value'] += asset.value['Market Value'] * asset.volume['Volume']
        return value
    
    def computePortfolioPGL(self): 
        """
            returns the value of the potential gains & losses over the duration of the simulation
        """
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
        """
            returns the value of the potential Bond gains & losses over the duration of the simulation
        """
        value = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1), columns=['Bonds PGL'])
        for asset in self.portfolio:
            if(type(asset).__name__ == 'Bond'):
                value['Bonds PGL'] += asset.potential['Potential Gain'] * asset.volume['Volume']
                value['Bonds PGL'] += asset.potential['Potential Loss'] * asset.volume['Volume']
        return value
    
    def computeEQPGL(self):
        """
            returns the value of the potential Equity gains & losses over the duration of the simulation
        """
        value = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1), columns=['Equities PGL'])
        for asset in self.portfolio:
            if(type(asset).__name__ == 'Equity'):
                value['Equities PGL'] += asset.potential['Potential Gain'] * asset.volume['Volume']
                value['Equities PGL'] += asset.potential['Potential Loss'] * asset.volume['Volume']
        return value
    
    def update(self, current_step):
        """
            updates the value of the portfolio over a period of time
        """
        for e in self.portfolio:
            e.update(current_step)
            if(e.flag != 0):
                self.portfolio.append(Bond(value=1, volume=e.flag,\
                                 starting_point=current_step, time_horizon=self.time_horizon))
                self.portfolio[-1].volume.loc[current_step, 'Volume'] = 0  # ----------- ATTENTION -------------
                e.flag = 0 
                # on réinvestit automatiquement le nominal
    
    def _increase_(self, amount, current_step, asset_type='Equity'):
        if(asset_type == 'Equity'):
            self.portfolio.append(Equity(value=1, volume=amount,\
                                         time_horizon=self.time_horizon,\
                                         starting_point=current_step))
        if(asset_type == 'Bond'):
            self.portfolio.append(Bond(value=1, volume=amount,\
                                       time_horizon=self.time_horizon,\
                                       starting_point=current_step))
        if(asset_type == 'Cash'):
            self.portfolio.append(Cash(value=1, volume=amount,\
                                       time_horizon=self.time_horizon,\
                                       starting_point=current_step))
        
    def _decrease_(self, amount, current_step, asset_type='Equity'):
        tmp = 0
        while(tmp < amount):
            e = self._lookout_(amount=amount, current_step=current_step, asset_type=asset_type)
            val = e.value.loc[current_step, 'Market Value'] * e.volume.loc[current_step, 'Volume']
            if(val >= amount):
                tmp += e.sell(current_step=current_step, amount=amount)
            else:
                tmp += e.cashOut(current_step=current_step)
    
    def _rebalance_(self):
        total = self.computePortfolioVal()
        err = .025
        bond_theory = total * self.ratio['Bond']
        if(abs(bond_theory - self.computeBondVal())>err):
            pass
        EQ_theory = total * self.ratio['Equity']
        if(abs(EQ_theory - self.computeEQVal())>err):
            pass
        cash_theory = total * self.ratio['Cash']
        if(abs(cash_theory - self.computeCashVal())>err):
            pass
        # implementer le rebalancement du portfolio selon le self.ratio
        # on calcule la balance theorique a atteindre
        # SI ratio > ratio_theorique:
        #   (lookout(assets)).sell() tant que > ()
        #   et acheter autre classe d'Asset ?
    
    def _lookout_(self, amount, current_step, asset_type='Equity'):
        """
            returns the Asset(s) whose value at a given step of time is the closest to the desired amount 
        """
        choice = 0
        selection = []
        if(type == 'All'):
            selection = self.portfolio
        else:
            for e in self.portfolio:
                if(type(e).__name__ == asset_type):
                    selection.append(e)
        selection.sort(key=lambda x:(x.value.loc[current_step, 'Market Value']*x.volume.loc[current_step, 'Volume']-amount), reverse=False)
        choice = selection[0]
        return choice 
    
    def clear(self):
        """
            clears the portfolio and returns the amount of money invested in it.
        """
        flag = 0
        for asset in self.portfolio:
            flag += asset.cashOut(self.time_horizon)
        return flag

#--------------------------------------------------
#       Start of the testing part of the code
#--------------------------------------------------
#
def main():
    step = 1
    assets = Assets(wealth=100, time_horizon=50) 
#    print(assets.computeCashVal)
#    print(assets.computeEQVal)
    
#    for asset in assets.portfolio:
#        if(type(asset).__name__=='Cash'):
#            print(asset.value['Market Value'] * asset.volume['Volume'])
#        else:
#            print(asset.value['Book Value'] * asset.volume['Volume'])
#    assets.computePortfolioVal().plot()


if __name__ == "__main__":
    main()