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
    def __init__(self, nb_bond=1, nb_equity=1, nb_cash=1, \
                 ratio={'Bond':.7, 'Equity':.2, 'Cash':.1},\
                 wealth = 1000, time_horizon=50):
        """
            creates an instance of the Assets class
            
            By default, the portfolio is composed of 1x Bond, 1x Equity and 1x Cash with the following ratio: .7, .2, .1
                and an available wealth of 1000 euros split between these 3 classes of Asset over a 25-year horizon.
                
            :param portfolio: the core of the class
            :param nb_bond: the number of Bond instrument composing the portfolio of Assets
            :param nb_equity: the number of Equity instrument composing the portfolio of Assets
            :param nb_cash: the number of Cash instrument composing the portfolio of Assets
            :param wealth: the amount of wealth to be invested in the portfolio
            :param time_horizon: the projected duration of the simulation
            :type portfolio: List of Asset
            :type nb_bond: Integer
            :type nb_equity: Integer
            :type nb_cash: Integer
            :type wealth: Float
            :type time_horizon: Integer
        """
        self.portfolio = []
        self.ratio = ratio
        self.nb_bond = nb_bond
        self.nb_equity = nb_equity
        self.nb_cash = nb_cash
        self.wealth = wealth
        self.time_horizon = time_horizon
        
        # we create the portfolio according to our specifications (ratio equity classes):
        for _ in range(self.nb_bond):
            self.portfolio.append(Bond(value=self.wealth*ratio['Bond']/self.nb_bond, time_horizon=self.time_horizon))
        for _ in range(self.nb_equity):
            self.portfolio.append(Equity(value=self.wealth*ratio['Equity']/self.nb_equity, time_horizon=self.time_horizon))
        for _ in range(self.nb_cash):
            self.portfolio.append(Cash(value=self.wealth*ratio['Cash']/self.nb_cash, time_horizon=self.time_horizon))
        
    
    def computePortfolioVal(self): 
        """
            returns the value of the portfolio over the duration of the simulation
        """
        value = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1), columns=['Portfolio Value'])
        for asset in self.portfolio:
            if(type(asset).__name__ == 'Bond'):
                value.loc[:, 'Portfolio Value'] += asset.value.loc[:, 'Market Value']
            elif(type(asset).__name__ == 'Equity'):
                value.loc[:, 'Portfolio Value'] += asset.value.loc[:, 'Market Value']
            elif(type(asset).__name__ == 'Cash'):
                value.loc[:, 'Portfolio Value'] += asset.value.loc[:, 'Market Value']
        return value
    
    def computeEQVal(self):
        value = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1), columns=['EQ Total Value'])
        for asset in self.portfolio:
            if(type(asset).__name__ == 'Equity'):
                value.loc[:, 'EQ Total Value'] += asset.value.loc[:, 'Market Value']
        return value
    
    def computeBondVal(self):
        value = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1), columns=['Bond Total Value'])
        for asset in self.portfolio:
            if(type(asset).__name__ == 'Bond'):
                value.loc[:, 'Bond Total Value'] += asset.value.loc[:, 'Face Value']
        return value
    
    def computeCashVal(self):
        value = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1), columns=['Cash Total Value'])
        for asset in self.portfolio:
            if(type(asset).__name__ == 'Cash'):
                value.loc[:, 'Cash Total Value'] += asset.value.loc[:, 'Market Value']
        return value
    
    def computePortfolioPGL(self): 
        """
            returns the value of the potential gains & losses over the duration of the simulation
        """
        value = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1), columns=['Portfolio PGL', 'Portfolio PG', 'Portfolio PL'])
        for asset in self.portfolio:
            if(type(asset).__name__ == 'Bond'):
                value.loc[:, 'Portfolio PGL'] += asset.potential.loc[:, 'Potential Gain']
                value.loc[:, 'Portfolio PG'] += asset.potential.loc[:, 'Potential Gain']
                value.loc[:, 'Portfolio PGL'] += asset.potential.loc[:, 'Potential Loss']
                value.loc[:, 'Portfolio PL'] += asset.potential.loc[:, 'Potential Loss']
            elif(type(asset).__name__ == 'Equity'):
                value.loc[:, 'Portfolio PGL'] += asset.potential.loc[:, 'Potential Gain'] 
                value.loc[:, 'Portfolio PG'] += asset.potential.loc[:, 'Potential Gain'] 
                value.loc[:, 'Portfolio PGL'] += asset.potential.loc[:, 'Potential Loss'] 
                value.loc[:, 'Portfolio PL'] += asset.potential.loc[:, 'Potential Loss'] 
        return value
    
    def computeBondPGL(self):
        """
            returns the value of the potential Bond gains & losses over the duration of the simulation
        """
        value = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1), columns=['Bonds PGL', 'Bonds PG', 'Bonds PL'])
        for asset in self.portfolio:
            if(type(asset).__name__ == 'Bond'):
                value.loc[:, 'Bonds PGL'] += asset.potential.loc[:, 'Potential Gain'] 
                value.loc[:, 'Bonds PG'] += asset.potential.loc[:, 'Potential Gain'] 
                value.loc[:, 'Bonds PGL'] += asset.potential.loc[:, 'Potential Loss'] 
                value.loc[:, 'Bonds PL'] += asset.potential.loc[:, 'Potential Loss']
        return value
    
    def computeEQPGL(self):
        """
            returns the value of the potential Equity gains & losses over the duration of the simulation
        """
        value = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1), columns=['Equities PGL', 'Equities PG', 'Equities PL'])
        for asset in self.portfolio:
            if(type(asset).__name__ == 'Equity'):
                value.loc[:, 'Equities PGL'] += asset.potential.loc[:, 'Potential Gain']
                value.loc[:, 'Equities PG'] += asset.potential.loc[:, 'Potential Gain']
                value.loc[:, 'Equities PGL'] += asset.potential.loc[:, 'Potential Loss']
                value.loc[:, 'Equities PL'] += asset.potential.loc[:, 'Potential Loss']
        return value
    
    def _increase_(self, amount, current_step, asset_type='Equity'):
        if(asset_type == 'Equity'):
            self.portfolio.append(Equity(value=amount,\
                                         time_horizon=self.time_horizon,\
                                         starting_point=current_step))
        if(asset_type == 'Bond'):
            self.portfolio.append(Bond(value=amount,\
                                       time_horizon=self.time_horizon,\
                                       starting_point=current_step))
        if(asset_type == 'Cash'):
            self.portfolio.append(Cash(value=amount,\
                                       time_horizon=self.time_horizon,\
                                       starting_point=current_step))
        
    def _decrease_(self, amount, current_step, asset_type='Equity'):
        tmp = 0
        while(tmp < amount):
            e = self._lookout_(amount=(amount-tmp), current_step=current_step, asset_type=asset_type)
            val = e.value.loc[current_step, 'Market Value']
            if(val > (amount-tmp)):
                flag = e.sell(current_step=current_step, amount=(amount-tmp))
                if(flag < 0):
                    tmp -= flag
                tmp += amount-tmp
            else:
                tmp += (e.cashOut(current_step=current_step-1))['all']
        return tmp 
    
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
        del total
        
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
        selection.sort(key=lambda x:abs(x.value.loc[current_step, 'Market Value']-amount), reverse=False) # l'Asset dont la valeur est la plus proche du 
        # montant souhaite est ordonne en premier dans la liste
        i = 0
        while(selection[i].value.loc[current_step, 'Market Value'] == 0 and i<len(selection)):
            i += 1 # on exclut les assets vendus dont l'ecart absolu serait le minimum
        choice = selection[i]
        return choice 
  
    def update(self, current_step, current_yield, spreads, cash_flows, statement):
        """
            updates the value of the portfolio over a period of time
        """
        for e in self.portfolio:
            tmp = e.update(current_step, current_yield, spreads)
            if(tmp>0):
                cash_flows.loc[current_step, 'CF_in'] += tmp
                statement.loc[current_step, 'financial_income'] += tmp
            else:
                cash_flows.loc[current_step, 'CF_out'] -= tmp
            if(type(e.flag) != int): # on reinvestit automatiquement les nominaux recuperes a l'annee suivante
                self.portfolio.append(Bond(value=e.flag['all'],\
                                 starting_point=current_step+1, time_horizon=self.time_horizon))
#                self.portfolio[-1].value.loc[current_step, 'Market Value'] = 0  # ----------- ATTENTION -------------
#                self.portfolio[-1].value.loc[current_step, 'Book Value'] = 0 
#                self.portfolio[-1].value.loc[current_step, 'Face Value'] = 0 
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

#def main():
#    import gc
#    gc.enable()
#
#    assets = Assets(wealth=100, time_horizon=70) 
##    for e in assets.portfolio:
##        print(e.value)
#     #-------- RAW INPUT --------------
#    noise = np.random.normal(0, .005, size=30)
#    USrate = (np.asarray([1.22,	1.35,	1.51,	1.65,	1.78,	1.89,	1.98,	2.06,	2.13,	2.19,	2.24,	2.29,	2.33,	2.37,	2.41,	2.45,	2.49,	2.53,	2.56,	2.60,	2.63,	2.67,	2.70,	2.73,	2.77,	2.80,	2.83,	2.86,	2.89,	2.91])/100+noise).transpose()
#    yield_curve = pd.DataFrame(data=USrate, index=np.arange(1,assets._lookout_(amount=0, current_step=1, asset_type='Bond').MAX_MATURITY+1), columns=['RRate'])
#    # ---------------------------------
#    cash_flows = pd.DataFrame(data=0, index=np.arange(1,assets.time_horizon+1), columns=['CF_in', 'CF_out'])
#    statement = pd.DataFrame(data=0, index=np.arange(1,assets.time_horizon+1),\
#                                      columns=['financial_income', 'margin', 'benefits', 'tech_income', 'admin_income'])
#    spreads = pd.DataFrame(data=0, index=np.arange(1,len(USrate)+1), columns=['Spreads'])
#    
#    for t in range(1, assets.time_horizon+1):
#        assets.update(current_step=t, current_yield=yield_curve.loc[:, 'RRate'], spreads=spreads.loc[:, 'Spreads'], cash_flows=cash_flows, statement=statement)
#        for e in assets.portfolio:
#            e.computePotential()
##    df = assets.portfolio[0].value.loc[:, 'Face Value'].plot(title='Evolution du portefeuille d\'actifs au cours d\'une simulation', legend=False)     
##    df.axvline(x=31, c="black", linewidth=1, zorder=0, linestyle='--')
##    df.axvline(x=30, c="black", linewidth=1, zorder=0, linestyle='--')
##    df.legend(['Bond #2', 'Bond #1', 'Equity #1', 'Cash #1'], loc='center left', bbox_to_anchor=(1.0, 0.5))
##    df.grid(True)    
#
#    df = assets.portfolio[0].value.plot()
#    for e in assets.portfolio:
#        e.value.plot(ax=df)
#    df.legend(['Bond #2', 'Bond #1', 'Equity #1', 'Cash #1'], loc='center left', bbox_to_anchor=(1.0, 0.5))
#
##    assets.computePortfolioPGL().plot()
#if __name__ == "__main__":
#    main()