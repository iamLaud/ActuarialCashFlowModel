# -*- coding: utf-8 -*-
"""
Created on Thu May 18 10:01:38 2017

@author: Laurent DEBRIL
Date of last revision: August 1st 2017

"""

#--------------------------------------------------
#           Python packages
#--------------------------------------------------
import numpy as np
import pandas as pd
import sys
MY_PATH = r'C:\Users\FR015797\Documents\PyALM_gen\code\alm'
sys.path.append(MY_PATH + r'\balancesheet\assets\asset') #the directory that contains my classes
#--------------------------------------------------
#           Project packages
#--------------------------------------------------
from Bond import Bond
from Equity import Equity
from Cash import Cash
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
        value = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1), columns=['Portfolio Market Value', 'Portfolio Book Value'])
        for asset in self.portfolio:
            if(type(asset).__name__ == 'Bond'):
                value.loc[:, 'Portfolio Market Value'] += asset.value.loc[:, 'Market Value']
                value.loc[:, 'Portfolio Book Value'] += asset.value.loc[:, 'Book Value']
            elif(type(asset).__name__ == 'Equity'):
                value.loc[:, 'Portfolio Market Value'] += asset.value.loc[:, 'Market Value']
                value.loc[:, 'Portfolio Book Value'] += asset.value.loc[:, 'Book Value']
            elif(type(asset).__name__ == 'Cash'):
                value.loc[:, 'Portfolio Market Value'] += asset.value.loc[:, 'Market Value']
                value.loc[:, 'Portfolio Book Value'] += asset.value.loc[:, 'Market Value']
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

    def computeEQVal(self):
        value = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1), columns=['EQ Market Value', 'EQ Book Value'])
        for asset in self.portfolio:
            if(type(asset).__name__ == 'Equity'):
                value.loc[:, 'EQ Market Value'] += asset.value.loc[:, 'Market Value']
                value.loc[:, 'EQ Book Value'] += asset.value.loc[:, 'Book Value']
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

    def computeBondVal(self):
        value = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1), columns=['Bond Market Value', 'Bond Book Value'])
        for asset in self.portfolio:
            if(type(asset).__name__ == 'Bond'):
                value.loc[:, 'Bond Market Value'] += asset.value.loc[:, 'Market Value']
                value.loc[:, 'Bond Book Value'] += asset.value.loc[:, 'Book Value']
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

    def computeCashVal(self):
        value = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1), columns=['Cash Total Value'])
        for asset in self.portfolio:
            if(type(asset).__name__ == 'Cash'):
                value.loc[:, 'Cash Total Value'] += asset.value.loc[:, 'Market Value']
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

    def _lookout_(self, amount, current_step, asset_type='Equity'):
        """
            returns the Asset whose net value at a given step of time is the closest to the desired amount
        """
        choice = 0
        selection = []
        if(asset_type == 'All'):
            selection = self.portfolio
        else:
            for e in self.portfolio:
                if(type(e).__name__ == asset_type):
                    selection.append(e)

        selection.sort(key=lambda x:abs(x.value.loc[current_step, 'Market Value'] \
                                        + x.potential.loc[current_step, 'Potential Gain'] \
                                        + x.potential.loc[current_step, 'Potential Loss'] - amount), reverse=False)
#        selection.sort(key=lambda x:abs(x.value.loc[current_step, 'Book Value'] \
#                                        - amount), reverse=False)
        # l'Asset dont la valeur est la plus proche du montant souhaite est ordonne en premier dans la liste
        pos = 0
        while(selection[pos].value.loc[current_step, 'Market Value'] == 0 and pos<len(selection)-1):
            pos += 1 # on exclut les assets vendus dont l'ecart absolu serait le minimum
        choice = selection[pos]
        return choice

    def _decrease_(self, amount, current_step, asset_type='Equity'):
        if(asset_type == 'Equity'):
            threshhold = self.computeEQVal().loc[current_step, 'EQ Market Value'] \
                        + self.computeEQPGL().loc[current_step, 'Equities PGL']
        elif(asset_type == 'Bond'):
            threshhold = self.computeBondVal().loc[current_step, 'Bond Market Value'] \
                        + self.computeBondPGL().loc[current_step, 'Bonds PGL']
        elif(asset_type == 'Cash'):
            threshhold = self.computeCashVal().loc[current_step, 'Cash Total Value']
        else:
            threshhold = self.computePortfolioVal().loc[current_step, 'Portfolio Value'] \
                        + self.computePortfolioPGL().loc[current_step, 'Portfolio PGL']

        amount = min(amount, threshhold)
        buffer = 0
        while(buffer < amount):
            e = self._lookout_(amount=(amount-buffer), current_step=current_step, asset_type=asset_type)
            e.computePotential()
            val = e.value.loc[current_step, 'Market Value'] + e.potential.loc[current_step, 'Potential Gain'] \
                    + e.potential.loc[current_step, 'Potential Loss']
            if(val > (amount-buffer)):
                buffer += e.sell(current_step=current_step, amount=(amount-buffer))
            else:
                buffer += (e.cashOut(current_step=current_step-1))['all']
        return buffer

    def _rebalance_(self, current_step):
        """
            will rebalance the current composition of the portfolio in compliance with the theoretical ratios
        """
        total = self.computePortfolioVal().loc[current_step, 'Portfolio Market Value']
        err = .0
        EQ_theory = total * self.ratio['Equity']
        bond_theory = total * self.ratio['Bond']
        cash_theory = total * self.ratio['Cash']
#       ------------- CHECK THE BOND COMPOSITION -------------------
        tmp = bond_theory - self.computeBondVal().loc[current_step, 'Bond Market Value']
        errEmp = tmp/bond_theory*100
        if(abs(errEmp)>err):
            if(tmp>0):
                self._increase_(amount=abs(tmp), current_step=current_step, asset_type='Bond')
            if(tmp<0):
                self._decrease_(amount=abs(tmp), current_step=current_step, asset_type='Bond')
#       ------------- CHECK THE EQUITY COMPOSITION -------------------
        tmp = EQ_theory - self.computeEQVal().loc[current_step, 'EQ Market Value']
        errEmp = tmp/EQ_theory*100
        if(abs(errEmp)>err):
            if(tmp>0):
                self._increase_(amount=abs(tmp), current_step=current_step, asset_type='Equity')
            if(tmp<0):
                self._decrease_(amount=abs(tmp), current_step=current_step, asset_type='Equity')
#       ------------- CHECK THE CASH COMPOSITION -------------------
        tmp = cash_theory - self.computeCashVal().loc[current_step, 'Cash Total Value']
        errEmp = tmp/cash_theory*100
        if(abs(errEmp)>err):
            if(tmp>0):
                self._increase_(amount=abs(tmp), current_step=current_step, asset_type='Cash')
            if(tmp<0):
                self._decrease_(amount=abs(tmp), current_step=current_step, asset_type='Cash')
        del total

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
            if(type(e.flag).__name__ == 'dict'): # on reinvestit automatiquement les nominaux recuperes a l'annee suivante
                self.portfolio.append(Bond(value=e.flag['all']+e.flag['pnl'],\
                                 starting_point=current_step+1, time_horizon=self.time_horizon, MAX_MATURITY=e.MAX_MATURITY))
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
#    assets = Assets(wealth=1000, time_horizon=50)
##     -------- RAW INPUT --------------
#    noise = np.random.normal(0, .001, size=30)
#    USrate = (np.asarray([1.22,	1.35,	1.51,	1.65,	1.78,	1.89,	1.98,	2.06,	2.13,	2.19,	2.24,	2.29,	2.33,	2.37,	2.41,	2.45,	2.49,	2.53,	2.56,	2.60,	2.63,	2.67,	2.70,	2.73,	2.77,	2.80,	2.83,	2.86,	2.89,	2.91])/100+noise).transpose()
#    yield_curve = pd.DataFrame(data=USrate, index=np.arange(1,len(USrate)+1), columns=['RRate'])
#    cash_flows = pd.DataFrame(data=0, index=np.arange(1,assets.time_horizon+1), columns=['CF_in', 'CF_out'])
#    statement = pd.DataFrame(data=0, index=np.arange(1,assets.time_horizon+1),\
#                                      columns=['financial_income', 'margin', 'benefits', 'tech_income', 'admin_income'])
#    spreads = pd.DataFrame(data=0, index=np.arange(1,len(USrate)+1), columns=['Spreads'])
#    # ---------------------------------
#
#    for t in range(1, assets.time_horizon+1):
#        assets.update(current_step=t, current_yield=yield_curve.loc[:, 'RRate'], spreads=spreads.loc[:, 'Spreads'], cash_flows=cash_flows, statement=statement)
#        assets._rebalance_(t)
#        
#    df=assets.computeBondVal().loc[:, 'Bond Market Value'].plot(title='Valeur des différentes classes d\'actifs au cours de la simulation')
#    assets.computeEQVal().loc[:, 'EQ Market Value'].plot(ax=df)
#    assets.computeCashVal().plot(ax=df)
#    df.legend(['Bond Value', 'Equity Value', 'Cash Value'], loc='center left', bbox_to_anchor=(1, 0.5))
#    df.grid(True)
#
#    print("Number of items in portfolio = ", len(assets.portfolio))
#    
#    df2 = assets.computePortfolioVal().plot(title='Valeur du portefeuille d\'actifs au cours de la simulation')
#    df2.legend(loc='center left', bbox_to_anchor=(1, 0.5))
#    df2.grid(True)
#    print(cash_flows)
#    
#    
#if __name__ == "__main__":
#    main()
