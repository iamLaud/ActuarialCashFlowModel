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
                 wealth = 1000, time_horizon=50):
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
        value = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1), columns=['Portfolio PGL', 'Portfolio PG', 'Portfolio PL'])
        for asset in self.portfolio:
            if(type(asset).__name__ == 'Bond'):
                value['Portfolio PGL'] += asset.potential['Potential Gain'] * asset.volume['Volume']
                value['Portfolio PG'] += asset.potential['Potential Gain'] * asset.volume['Volume']
                value['Portfolio PGL'] += asset.potential['Potential Loss'] * asset.volume['Volume']
                value['Portfolio PL'] += asset.potential['Potential Loss'] * asset.volume['Volume']
            elif(type(asset).__name__ == 'Equity'):
                value['Portfolio PGL'] += asset.potential['Potential Gain'] * asset.volume['Volume']
                value['Portfolio PG'] += asset.potential['Potential Gain'] * asset.volume['Volume']
                value['Portfolio PGL'] += asset.potential['Potential Loss'] * asset.volume['Volume']
                value['Portfolio PL'] += asset.potential['Potential Loss'] * asset.volume['Volume']
        return value
    
    def computeBondPGL(self):
        """
            returns the value of the potential Bond gains & losses over the duration of the simulation
        """
        value = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1), columns=['Bonds PGL', 'Bonds PG', 'Bonds PL'])
        for asset in self.portfolio:
            if(type(asset).__name__ == 'Bond'):
                value['Bonds PGL'] += asset.potential['Potential Gain'] * asset.volume['Volume']
                value['Bonds PG'] += asset.potential['Potential Gain'] * asset.volume['Volume']
                value['Bonds PGL'] += asset.potential['Potential Loss'] * asset.volume['Volume']
                value['Bonds PL'] += asset.potential['Potential Loss'] * asset.volume['Volume']
        return value
    
    def computeEQPGL(self):
        """
            returns the value of the potential Equity gains & losses over the duration of the simulation
        """
        value = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1), columns=['Equities PGL', 'Equities PG', 'Equities PL'])
        for asset in self.portfolio:
            if(type(asset).__name__ == 'Equity'):
                value['Equities PGL'] += asset.potential['Potential Gain'] * asset.volume['Volume']
                value['Equities PG'] += asset.potential['Potential Gain'] * asset.volume['Volume']
                value['Equities PGL'] += asset.potential['Potential Loss'] * asset.volume['Volume']
                value['Equities PL'] += asset.potential['Potential Loss'] * asset.volume['Volume']
        return value
    
    def _increase_(self, amount, current_step, asset_type='Equity'):
        if(asset_type == 'Equity'):
            self.portfolio.append(Equity(value=1, volume=amount,\
                                         time_horizon=self.time_horizon,\
                                         starting_point=current_step+1))
        if(asset_type == 'Bond'):
            self.portfolio.append(Bond(value=1, volume=amount,\
                                       time_horizon=self.time_horizon,\
                                       starting_point=current_step+1))
        if(asset_type == 'Cash'):
            self.portfolio.append(Cash(value=1, volume=amount,\
                                       time_horizon=self.time_horizon,\
                                       starting_point=current_step+1))
        
    def _decrease_(self, amount, current_step, asset_type='Equity'):
        tmp = 0
        while(tmp < amount):
            e = self._lookout_(amount=(amount-tmp), current_step=current_step+1, asset_type=asset_type)
            val = e.value.loc[current_step, 'Market Value'] * e.volume.loc[current_step, 'Volume']
            if(val > (amount-tmp)):
                tmp += e.sell(current_step=current_step, amount=(amount-tmp))
            else:
                tmp += e.cashOut(current_step=current_step)

    def _rebalance_(self, current_step):
        """
            will rebalance the current composition of the portfolio in compliance with the theoretical ratios
        """
        total = self.computePortfolioVal()
        err = 0.025
        EQ_theory = total * self.ratio['Equity']
        bond_theory = total * self.ratio['Bond']
        cash_theory = total * self.ratio['Cash']
#       ------------- CHECK THE BOND COMPOSITION -------------------
        tmp = bond_theory.loc[current_step, 'Portfolio Value'] - self.computeBondVal().loc[current_step, 'Bond Total Value']
        if(abs(tmp)>err):
            if(tmp>err):
                self._increase_(amount=abs(tmp), current_step=current_step, asset_type='Bond')
            if(tmp<err):
                self._decrease_(amount=abs(tmp), current_step=current_step, asset_type='Bond')
#       ------------- CHECK THE EQUITY COMPOSITION -------------------        
        tmp = EQ_theory.loc[current_step, 'Portfolio Value'] - self.computeEQVal().loc[current_step, 'EQ Total Value']
        if(abs(tmp)>err):
            if(tmp>err):
                self._increase_(amount=abs(tmp), current_step=current_step, asset_type='Equity')
            if(tmp<err):
                self._decrease_(amount=abs(tmp), current_step=current_step, asset_type='Equity')
#       ------------- CHECK THE CASH COMPOSITION -------------------
        tmp = cash_theory.loc[current_step, 'Portfolio Value'] - self.computeCashVal().loc[current_step, 'Cash Total Value']
        if(abs(tmp)>err):
            if(tmp>err):
                self._increase_(amount=abs(tmp), current_step=current_step, asset_type='Cash')
            if(tmp<err):
                self._decrease_(amount=abs(tmp), current_step=current_step, asset_type='Cash')
    
    def _lookout_(self, amount, current_step, asset_type='Equity'):
        """
            returns the Asset(s) whose value at a given step of time is the closest to the desired amount 
        """
        choice = 0
        selection = []
        if(asset_type == 'All'):
            selection = self.portfolio
        else:
            for e in self.portfolio:
                if(type(e).__name__ == asset_type):
                    selection.append(e)
        selection.sort(key=lambda x:abs(x.value.loc[current_step, 'Market Value']*x.volume.loc[current_step, 'Volume']-amount), reverse=False)
        i = 0
        while(selection[i].value.loc[current_step, 'Market Value']*selection[i].volume.loc[current_step, 'Volume'] == 0 and i<len(selection)):
            i += 1 # on exclut les assets vendus dont l'ecart absolu serait le minimum
        choice = selection[i]
        return choice 
  
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
            e.computePotential()
                # on réinvestit automatiquement le nominal
                
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
    assets = Assets(wealth=1000, time_horizon=50) 
    for i in range(1, assets.time_horizon):
        assets.update(i)
#        if(i==15):
#            assets._decrease_(amount=400, current_step=i, asset_type='Bond')
#        if(i == 40):
#            assets._rebalance_(current_step=i)
#        if(i%10 == 0):
#           assets._increase_(amount=100, current_step=i, asset_type='Cash')
#           assets._increase_(amount=100, current_step=i, asset_type='Equity') 
#        if(i%10 == 0):
#    for asset in assets.portfolio:
#        if(type(asset).__name__ == 'Equity'):
#            asset.potential.plot()

#    ------------- PLOT RESULTS ---------------------------------
#    df = assets.computePortfolioVal().plot(title="Evolution de la composition du portefeuille au cours de la simulation")
#    assets.computePortfolioVal().plot(ax=df)
#    assets.computeBondVal().plot(ax=df)
#    assets.computeEQVal().plot(ax=df)
#    assets.computeCashVal().plot(ax=df)
#    
#    for k in range(1, assets.time_horizon):
#        if(k%5 == 0):
#            df.axvline(k, color='k', linewidth=.5, linestyle='--')
#            df.axvline(k+1, color='r', linewidth=.5, linestyle='--')
#        if(k%10 == 0):
#            df.axvline(k, color='r', linewidth=.5, linestyle='--')
#            
#    df.axvline(11, color='k', linewidth=.5, linestyle='--')
#    df.axvline(12, color='k', linewidth=.5, linestyle='--')
#    df.axhline(y=1500,c="blue", linewidth=.5, zorder=0)
#    df.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))

if __name__ == "__main__":
    main()