# -*- coding: utf-8 -*-
"""
Created on May 14th 2017

@author: Laurent DEBRIL
Date of last revision: August 1st 2017

"""

#--------------------------------------------------
#           Python packages
#--------------------------------------------------
import numpy as np
import pandas as pd
import sys
sys.path.append(r'C:\Users\FR015797\Documents\PyALM_gen\code\alm\balancesheet\liabilities\liability') #the directory that contains my classes
#--------------------------------------------------
#           Project packages
#--------------------------------------------------
from Liability import Liability
from Provision import Provision
#--------------------------------------------------
#       Start of the proper code
#--------------------------------------------------

class Liabilities(object):
    def __init__(self, cap_reserve=None, math_provision=None,\
                 own_funds=None, profit_shar_prov=None,\
                 eligib_prov=None, time_horizon=50):

        self.math_provision = [] # List des contrats d'assurance
        self.other_provisions = {} # Dict des provisions hors PM
        self.time_horizon = time_horizon
# ---------------------------------------------------------
        if(math_provision != None):
            self.math_provision.append(math_provision)
        else:
            self.math_provision.append(Liability(value=500, starting_point=1, age=40, lifespan=30))
            self.math_provision.append(Liability(value=200, starting_point=1, age=30, lifespan=30))
            self.math_provision.append(Liability(value=300, starting_point=1, age=50, lifespan=30))
            # parametrer la provision
# ---------------------------------------------------------
        if(cap_reserve != None):
            self.other_provisions['Reserve de cap'] = cap_reserve
        else:
            self.other_provisions['Reserve de cap'] = Provision(value=500)
            # parametrer la provision
# ---------------------------------------------------------
        if(own_funds != None):
            self.other_provisions['Fonds propres'] = own_funds
        else:
            self.other_provisions['Fonds propres'] = Provision(value=2000)
            # parametrer la provision
# ---------------------------------------------------------
        if(profit_shar_prov != None):
            self.other_provisions['PPB'] = profit_shar_prov
        else:
            self.other_provisions['PPB'] = Provision(value=0)
            # parametrer la provision
# ---------------------------------------------------------
        if(eligib_prov != None):
            self.other_provisions['PRE'] = eligib_prov
        else:
            self.other_provisions['PRE'] = Provision(value=0)
            # parametrer la provision
# ---------------------------------------------------------

    def computeMPVal(self):
        val = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1),\
                           columns=['MP Value'])
        for e in self.math_provision:
            val.loc[:, 'MP Value'] += e.value.loc[:, 'Contract Value']
        return val

    def computeValAll(self):
        val = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1),\
                           columns=['Liabilities Value'])
        for e in self.math_provision:
            val.loc[:, 'Liabilities Value'] += e.value.loc[:, 'Contract Value']
        for key, value in self.other_provisions.items():
            val.loc[:, 'Liabilities Value'] += value.value.loc[:, 'Value']
        return val

    def _lookout_(self, current_step):
        """
            returns the Liability whose time2expiry at a given step of time is the shortest
        """
        selection = self.math_provision
        selection.sort(key=lambda x:x.contract_age, reverse=False)
        i = 0
        while(selection[i].value.loc[current_step, 'Contract Value'] == 0 and i<len(selection)):
            i += 1 # on exclut les assets vendus dont l'ecart absolu serait le minimum
        choice = selection[i]
        return choice

    def _decrease_(self, amount, current_step):
        tmp = 0
        while(tmp < amount):
            e = self._lookout_(current_step)
            if(e.value.loc[current_step, 'Contract Value'] >= amount):
                tmp += e.buyBack(current_step=current_step,\
                                   amount=amount-tmp, percentage=0)
            else:
                tmp += e.buyBack(current_step=current_step,\
                                   percentage=1)
#                e.time2expiration = 999999 # +infty

    def _increase_(self, amount, current_step): # to increase the amount of Liabilities
        self.math_provision.append(Liability(value=amount, time_horizon=self.time_horizon,\
                                             starting_point=current_step,\
                                             lifespan=20, age=40))

    def update(self, current_step, cash_flows=None, available_wealth=None, mode='mid'):
        flag = None
#        --------------- DEFAULT CASE -----------------------
#        if(cash_flows == None):
#            cash_flows = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1), columns=['CF_in', 'CF_out'])
#        if(available_wealth == None):
#            available_wealth = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1), columns=['Stream Value'])
#        -----------------------------------------------------

        # on actualise ici les contrats d'assurance contenus dans math_provision
        if(mode == 'end'): # anciennete et age
            flag = 0
            for e in self.math_provision:
                flag  += e.update(current_step, mode='end')
            if(flag != 0):
            # i.e. if a contract expired, we immediatly create a new one with the same value
                NB_CONTRACT = 3
                for i in range(1, NB_CONTRACT+1):
                    self._increase_(amount=flag*i/(2*NB_CONTRACT), current_step=current_step+1)
                flag = 0

        elif(mode == 'mid'): # rachats, deces, entrees, sorties, taux
            for e in self.math_provision:
                flag = e.update(current_step, mode='mid')
                if(type(flag).__name__ == 'tuple'):
                    cash_flows.loc[current_step, 'CF_in'] += flag[0]
                    cash_flows.loc[current_step, 'CF_out'] += abs(flag[1])
        elif(mode == 'early'):
            for e in self.other_provisions:
                flag = e.update(current_step=current_step)
#                cash_flows.loc[current_step, 'CF_in'] += flag
        return flag

    def _clear_(self, current_step):
        flag = 0
        for e in self.math_provision:
            flag += e.buyBack(current_step=current_step)
        for key, value in self.other_provisions.items():
            flag += self.other_provisions[key].recover(current_step=self.time_horizon, percentage=1, amount=0)
        return flag

#--------------------------------------------------
#       Start of the testing part of the code
#--------------------------------------------------

#def main():
#    passif = Liabilities()
#    for t in range(1, passif.time_horizon+1):
#        passif.update(current_step=t, mode='mid')
#        passif.update(current_step=t, mode='end')
#
#    df = passif.math_provision[0].value.plot(title='Simulation d\'un portefeuille auto-géré de contrats d\'assurance')
#    for e in passif.math_provision:
#        e.value.plot(ax =df)
#    df.axvline(30, color='black', linewidth=.5, linestyle='--')
#    df.axvline(31, color='black', linewidth=.5, linestyle='--')
#    passif.computeMPVal().plot()
#
#
#if __name__ == "__main__":
#    main()
