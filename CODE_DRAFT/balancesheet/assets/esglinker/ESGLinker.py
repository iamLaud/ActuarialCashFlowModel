# -*- coding: utf-8 -*-
"""
Created on Thu May 18 10:01:38 2017

@author: FR015797 (aka Laurent DEBRIL)
Date of last revision: May 18th 2017
"""


#--------------------------------------------------
#           Project packages
#--------------------------------------------------
#from esg.ESG_RN import ESG_RN
#--------------------------------------------------
#           Python packages
#--------------------------------------------------
import numpy as np
import pandas as pd

#import os
#--------------------------------------------------
#       Start of the proper code
#--------------------------------------------------
class ESGLinker(object):
    def __init__(self):
        self.prices_EQ = None
        self.rates_EQ = None
        self.rates_bond = None
        self.deflators_bond = None
        self.rates_cash = None 
        
    def importScenarios(self):
#        ESG = ESG_RN()
#        return ESG.scenarios
        scenarios = {}
        scenarios['1'] = {'EQ_prices': [1, 2, 3, 4, 5], 'EQ_return_rates': [.1, .2, .3, .4, .5], 'IR_curves': [1, 2, 3, 4, 5], 'Deflators': [.1, .2, .3, .4, .5], 'Short_rates': [.011, .235, .813, .213, .455]} 
        scenarios['2'] = {'EQ_prices': [6, 7, 8, 9, 10], 'EQ_return_rates': [.6, .7, .8, .9, .10], 'IR_curves': [1, 2, 3, 4, 5], 'Deflators': [.1, .2, .3, .4, .5], 'Short_rates': [.011, .235, .813, .213, .455]}    
        scenarios['3'] = {'EQ_prices': [11, 12, 13, 14, 15], 'EQ_return_rates': [.11, .12, .13, .14, .15], 'IR_curves': [1, 2, 3, 4, 5], 'Deflators': [.1, .2, .3, .4, .5], 'Short_rates': [.011, .235, .813, .213, .455]}
        return(scenarios)
    
    def acquireData(self):
        tmp = self.importScenarios()
        
        #---Pour des besoins de test:
#        Structure des données
#        ti = {'EQ_prices':EQ_prices, 'EQ_total_returns':EQ_total_returns, 'EQ_return_rates':EQ_return_rates, 
#              'IR_curves':IR_curves, 'Deflators':IR_deflators, 'Short_rates':IR_trajectory,
#              'RN_migration_matrix':RN_migration_matrix, 'spreads':actuarial_spreads, 'spreads_spot':spreads,
#              'rating_based_deflators':rating_based_deflators}
#        self.scenarios[traj_i] = ti

        #Equity Vect generator
        time_horizon = len(tmp['1']['EQ_prices'])
        self.prices_EQ = pd.DataFrame(index=np.arange(1,time_horizon+1))
        for key, value in tmp.items():
            self.prices_EQ['Scenario #'+str(key)] = tmp[key]['EQ_prices']
            
        time_horizon = len(tmp['1']['EQ_return_rates'])
        self.rates_EQ = pd.DataFrame(index=np.arange(1,time_horizon+1))
        for key, value in tmp.items():
            self.rates_EQ['Scenario #'+str(key)] = tmp[key]['EQ_return_rates']

#            
#        #Bond Vect generator
        time_horizon = len(tmp['1']['IR_curves'])
        self.rates_bond = pd.DataFrame(index=np.arange(1,time_horizon+1))
        for key, value in tmp.items():
            self.rates_bond['Scenario #'+str(key)] = tmp[key]['IR_curves']
            
        time_horizon = len(tmp['1']['Deflators'])
        self.deflators_bond = pd.DataFrame(index=np.arange(1,time_horizon+1))
        for key, value in tmp.items():
            self.deflators_bond['Scenario #'+str(key)] = tmp[key]['Deflators']
            
        #Cash Vect generator
        time_horizon = len(tmp['1']['Short_rates'])
        self.rates_cash = pd.DataFrame(index=np.arange(1,time_horizon+1))
        for key, value in tmp.items():
            self.rates_cash['Scenario #'+str(key)] = tmp[key]['Short_rates']
        
#--------------------------------------------------
#       Start of the testing part of the code
#--------------------------------------------------

def main():
    link = ESGLinker()
    link.acquireData()
#    print(link.prices_EQ)
#    print(link.rates_EQ)
#    print(link.rates_bond)
#    print(link.deflators_bond)
    print(link.rates_cash)
    
if __name__ == "__main__":
    main()