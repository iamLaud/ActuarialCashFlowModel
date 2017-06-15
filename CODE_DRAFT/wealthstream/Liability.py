# -*- coding: utf-8 -*-
"""
Created on Thu May 18 10:01:38 2017

@author: FR015797
Date of last revision: May 29th 2017
"""


#--------------------------------------------------
#           Project packages
#--------------------------------------------------

#--------------------------------------------------
#           Python packages
#--------------------------------------------------
import pandas as pd
import numpy as np

#--------------------------------------------------
#       Start of the proper code
#--------------------------------------------------

class Liability(object):
    def __init__(self, value=1, time_horizon=50, starting_point=1, time2expiration=20):
        self.time_horizon = time_horizon
        self.starting_point = starting_point
        self.time2expiration = time2expiration
        
        self.value = value
        self.value = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1),\
                                  columns=['Contract Value']) 
        self.value.loc[self.starting_point:self.time_horizon, 'Contract Value'] = value
        self.buy_back_ratio = pd.DataFrame(data=0, \
           index=np.arange(1,self.time_horizon+1), columns=['Contract Value']) 
        
    def buyBack(self, current_step, percentage=1, amount=0):
        flag = percentage * self.value.loc[current_step, 'Contract Value'] + amount
        if(flag <= self.value.loc[current_step, 'Contract Value']):
            if(current_step<self.time_horizon):
                self.value.loc[np.arange(current_step+1,self.time_horizon+1), 'Contract Value'] -= flag
        return flag 
   
    def updateValue(self, current_step): # update auto des contrats (actions de vieillissement only)
#        ----- SIMULATED DATA FOR NOW ---------------
        mean = 0
        std = .05
        noise = float(np.random.normal(mean, std, size=1)*self.value.loc[current_step, 'Contract Value'])
#        ----------------------------------------------
        flag = self.buyBack(current_step, percentage=0, amount=min(noise, self.value.loc[current_step, 'Contract Value']))
        # Implementer les sorties dues aux deces et rachats structurels
        # charger et appliquer ici les formules des tables de morta et rachats
        # 1 mort ou 1 rachat = 1 appel de buyBack()
        return flag 
    
    def update(self, current_step): # update auto des contrats (Actions de vieillissement + application des regles ALM)
        flag = 0
        # si le contrat existe, il vieillit a chaque periode:
        if(self.value.loc[current_step, 'Contract Value'] > 0):
            self.time2expiration -= 1
        # Si le contrat expire, on recupere la somme, sinon on la vieillit:
        if(self.time2expiration == 0):
            flag = self.buyBack(current_step)
        else:
            # on met à jour les valeurs des contrats selon les rachats et deces associes
            flag = self.updateValue(current_step) 
        return flag
    
    def __str__(self):
        return self.value.__str__()
    
    
#--------------------------------------------------
#       Start of the testing part of the code
#--------------------------------------------------

#def main():
#    lia1 = Liability(value=100, time2expiration=20)
#    lia2 = Liability(value=100, starting_point=10, time2expiration=20)
#    lia3 = Liability(value=100, starting_point=25, time2expiration=30)
#    for i in range(1, lia1.time_horizon+1):
#        lia1.update(i)
#        lia2.update(i)
#        lia3.update(i)
#    df = lia1.value.plot(title='Evolution de la valeur des contrats au cours de la simulation')
#    lia2.value.plot(ax=df)
#    lia3.value.plot(ax=df)
#    df.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))


#if __name__ == "__main__":
#    main()