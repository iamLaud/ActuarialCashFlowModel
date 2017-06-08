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
        assert(amount <= self.value.loc[current_step, 'Contract Value'])
        flag = percentage * self.value.loc[current_step, 'Contract Value'] + amount
        if(current_step<self.time_horizon):
            self.value.loc[np.arange(current_step+1,self.time_horizon+1), 'Contract Value'] -= flag
        return flag 
   
    def updateValue(self, current_step): # update auto des contrats (actions de vieillissement only)
        self.value.loc[current_step:self.time_horizon, 'Contract Value'] -= 0 # Implementer les sorties dues aux deces et rachats structurels
        # charger et appliquer ici les formules des tables de morta et rachats
        # 1 mort ou 1 rachat = 1 appel de buyBack()
        
    def update(self, current_step): # update auto des contrats (Actions de vieillissement + application des regles ALM)
        flag = 0
        self.updateValue(current_step) # on vieillit les contrats avant d'effectuer les sorties
        self.time2expiration -= 1
        if(self.time2expiration == 0):
            flag = self.buyBack(current_step)
        return flag
        # on met à jour le volume selon les rachats et deces associes a ce contrat
    
    def __str__(self):
        return("value: " + self.value.__str__() + "\n")
    
    
#--------------------------------------------------
#       Start of the testing part of the code
#--------------------------------------------------

#def main():
#    liability = Liability()
#    lia2 = Liability(value=2, starting_point=5)
#    print(liability.value['Contract Value'] +lia2.value['Contract Value'])
#    
#    
#if __name__ == "__main__":
#    main()