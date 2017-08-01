# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 18:02:45 2017

@author: FR015797
"""

#--------------------------------------------------
#           Python packages
#--------------------------------------------------
import pandas as pd
import numpy as np
import sys
MY_PATH = r'C:\Users\FR015797\Documents\PyALM_gen\code\alm'
sys.path.append(MY_PATH + r'\balancesheet\assets') #the directory that contains my classes
sys.path.append(MY_PATH + r'\balancesheet\liabilities') 
sys.path.append(MY_PATH + r'\balancesheet\wealthstream') 
#--------------------------------------------------
#           Project packages
#--------------------------------------------------
from RateMin import RateMin
from RateTarget import RateTarget
from RatePaid import RatePaid
from Assets import Assets
from Liabilities import Liabilities
from WealthStream import WealthStream
#--------------------------------------------------
#       Start of the proper code
#--------------------------------------------------

class Rule(object):
    def __init__(self, time_horizon=50):
        self.time_horizon = time_horizon
        self.paid_rate = RatePaid()
        self.min_rate = RateMin()
        self.target_rate = RateTarget()
        self.priorities = {'first': 'margin', 'second': 'paid_rate', 'third': 'provisions'}
    
    def managePS(self, current_step, assets, liabilities, min_wealth, max_wealth, statement):
        PS_USE_LIMIT = .6 # 1.
        PB_MIN = .85
#       Etape #1: on calcule les differents taux:
        self.min_rate.computeRate(current_step=current_step)
        if(current_step>1):
            self.target_rate.computeRate(current_step=current_step, \
                                         hist_rate=self.paid_rate.value.iloc[current_step-1, 0],\
                                         fin_benefits=statement.loc[current_step, 'financial_income'])
        else:
            self.target_rate.computeRate(current_step=current_step, \
                                         hist_rate=.01, fin_benefits=statement.loc[current_step, 'financial_income'])
        self.paid_rate.computeRate(current_step=current_step)
        print('---------- BEGINNING OF PERIOD --------------------')

#       Etape #2: on utilise les differents leviers:
        isIncreasable = True
        distributed_wealth = max(0, PB_MIN * statement.loc[current_step, 'financial_income']) # l'assureur assume l'integralite des pertes
        statement.loc[current_step, 'benefits'] = statement.loc[current_step, 'financial_income'] - distributed_wealth
        print('MP Value = ', liabilities.computeMPVal().iloc[current_step, 0])
        target_wealth = max(self.target_rate.value.iloc[current_step, 0] * liabilities.computeMPVal().iloc[current_step, 0], \
                            self.min_rate.value.iloc[current_step, 0] * liabilities.computeMPVal().iloc[current_step, 0])
        print('#', current_step)
        print('                       amount available = ', distributed_wealth)
        print('                       amount needed = ', target_wealth)
        if(distributed_wealth > target_wealth):
            print('-----------------------------------------------')
            print('DOTATION PPB')
            gap = .7 * (distributed_wealth - target_wealth)
            liabilities.other_provisions['PPB'].allocate(current_step=current_step+1, amount=statement.loc[current_step, 'financial_income'])
            distributed_wealth -= gap 
        else:
            # calcule le pourcentage de PM en MV que represente les benefices financiers de l'annee en cours
            while(distributed_wealth < target_wealth and isIncreasable):
                regl_wealth = self.min_rate.value.iloc[current_step, 0]* liabilities.computeMPVal().iloc[current_step, 0]
                if(distributed_wealth >= regl_wealth):
                    print('-----------------------------------------------')
                    print('REPRISE PPB')
                    print('PPB = ', liabilities.other_provisions['PPB'].value.iloc[current_step, 0])
                # si on peut verser la PB reglementaire mais pas le taux cible => reprise sur PPB
                    gap = min(PS_USE_LIMIT*liabilities.other_provisions['PPB'].value.iloc[current_step, 0], target_wealth-distributed_wealth)
                    distributed_wealth += liabilities.other_provisions['PPB'].recover(current_step+1, gap)
                    if(distributed_wealth < target_wealth):
                        isIncreasable = False
                else:
                    print('-----------------------------------------------')
                    print('REPRISE FONDS PROPRES')
                # si on ne peut pas servir la PB reglementaire => reprise sur Fonds propres => puis reprise sur PPB si possible pour taux cible
                    gap = min(liabilities.other_provisions['Fonds propres'], regl_wealth-distributed_wealth)
                    distributed_wealth += liabilities.other_provisions['Fonds propres'].recover(current_step+1, gap)
                    if(distributed_wealth < regl_wealth):
                        isIncreasable = False         
                print('-----------------------------------------------')
        print('distributed amount = ', distributed_wealth)
        # revalorisation des PM:
        for e in liabilities.math_provision:
            e.value.iloc[current_step+1:, 0] += distributed_wealth * (e.value.iloc[current_step, 0]/liabilities.computeMPVal().iloc[current_step, 0])
            # repartition de la richesse distribuee au pro rata de la part des PM representees
            
        self.paid_rate.value.iloc[current_step, 0] = distributed_wealth/liabilities.computeMPVal().iloc[current_step, 0]
        print('---------- END OF PERIOD ----------------------')
        print('PAID RATE = ', self.paid_rate.value.iloc[current_step, 0])
        print('PPB = ', liabilities.other_provisions['PPB'].value.iloc[current_step+1, 0])
        print('-----------------------------------------------')
        
        
#--------------------------------------------------
#       Start of the testing part of the code
#--------------------------------------------------

#def main():
#    rule = Rule()
#    
#
#if __name__ == "__main__":
#    main()