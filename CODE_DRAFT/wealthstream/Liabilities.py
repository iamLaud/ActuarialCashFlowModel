# -*- coding: utf-8 -*-
"""
Created on May 14th 2017

@author: Laurent DEBRIL
Date of last revision: May 29th 2017

"""

#--------------------------------------------------
#           Project packages
#--------------------------------------------------
from Provision import Provision
from Liability import Liability
#--------------------------------------------------
#           Python packages
#--------------------------------------------------
import numpy as np
import pandas as pd

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
            self.math_provision.append(Liability(value=6, starting_point=1))          
            self.math_provision.append(Liability(value=600, time2expiration=15))  
            self.math_provision.append(Liability(value=60, starting_point=20))          


            # parametrer la provision
# ---------------------------------------------------------                   
        if(cap_reserve != None):
            self.other_provisions['Reserve de cap'] = cap_reserve
        else:
            self.other_provisions['Reserve de cap'] = Provision(value=25)
            # parametrer la provision
# ---------------------------------------------------------                        
        if(own_funds != None):
            self.other_provisions['Fonds propres'] = own_funds
        else:
            self.other_provisions['Fonds propres'] = Provision(value=42)
            # parametrer la provision
# ---------------------------------------------------------                        
        if(profit_shar_prov != None):
            self.other_provisions['PPB'] = profit_shar_prov
        else:
            self.other_provisions['PPB'] = Provision(value=933)
            # parametrer la provision
# ---------------------------------------------------------                       
        if(eligib_prov != None):
            self.other_provisions['PRE'] = eligib_prov
        else:
            self.other_provisions['PRE'] = Provision(value=1)
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
        selection.sort(key=lambda x:x.time2expiration, reverse=False)
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
                                   amount=amount, percentage=0)
            else:
                tmp += e.buyBack(current_step=current_step,\
                                   percentage=1)
#                e.time2expiration = 999999 # +infty
                
    def _increase_(self, amount, current_step): # to increase the amount of Liabilities
        self.math_provision.append(Liability(value=amount, time_horizon=50,\
                                             starting_point=current_step,\
                                             time2expiration=20))    
    
    def update(self, current_step, cash_flow_in=None, cash_flow_out=None, available_wealth=None, mode='mid'):
        # on actualise ici les contrats d'assurance contenus dans math_provision
        if(mode == 'mid'): # anciennete et age
            for e in self.math_provision:
                tmp = e.update(current_step)
#                if(tmp != 0):
#                    cash_flow_out.value.loc[current_step, 'Stream Value'] = tmp
                    #si !=0 on a des sorties de contrats donc on MaJ la WStream des CF_out
#            for key, e in self.other_provisions.items():            
#                tmp = e.update(current_step)
#                if(tmp != 0):
#                    cash_flow_in.value.loc[current_step, 'Stream Value'] = tmp
                    #si !=0 on a des reprises sur dotation on MaJ le CF_in 
                    
        if(mode == 'early'): # rachats, deces, entrees, sorties, taux
            pass # pour l'instant on fusionne l'etape 'early' et 'mid'
        
        if(mode == 'late'): #actualisation PM et repartition provisions APRES SERVICE DES TAUX
            tmp = available_wealth.loc[current_step, 'Stream Value']    
            if(tmp>0):
                self.other_provisions['PPB'].value.loc[current_step, 'Value'] = tmp
                available_wealth.value.loc[current_step, 'Stream Value'] -= tmp
            # si available_wealth > 0 apres service des taux, il reste de l'argent a doter quelques part (marge ou provisions)    
            
    def _clear_(self):
        flag = 0
        for e in self.math_provision:
            flag += e.buyBack(current_step=self.time_horizon)
        for e in self.other_provisions:
            flag += e.recover(current_step=self.time_horizon, percentage=1, amount=0)
        return flag
#--------------------------------------------------
#       Start of the testing part of the code
#--------------------------------------------------

def main():
    passif = Liabilities()
    for i in range(1, passif.time_horizon):
        passif.update(i)
        if(i == 5 or i==11 or i==21):
            passif._lookout_(i).value.plot()


        
        
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
##    df.axvline(11, color='k', linewidth=.5, linestyle='--')
##    df.axvline(12, color='k', linewidth=.5, linestyle='--')
##    df.axhline(y=1500,c="blue", linewidth=.5, zorder=0)
#    df.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))


if __name__ == "__main__":
    main()