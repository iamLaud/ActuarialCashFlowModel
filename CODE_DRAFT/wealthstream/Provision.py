# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 10:18:45 2017

@author: FR015797 (aka Laurent DEBRIL)
Date of last revision: May 29th 2017

"""
#--------------------------------------------------
#           Project packages
#--------------------------------------------------
#--------------------------------------------------
#           Python packages
#--------------------------------------------------
import numpy as np
import pandas as pd
#--------------------------------------------------
#       Start of the proper code
#--------------------------------------------------

class Provision(object):
    """A class modeling the structure of a provision as used in the ALM model:

    Attributes:
        value: A value of the provision over time (DataFrame of Float)
        time_horizon: The time horizon over which the simulation takes place (integer).
    """
    
    def __init__(self, value=1, time_horizon=50, starting_point=1,\
                 duration=50, limit_sup=.2, recovery_frequency=0,\
                 recovery_percentage=0.334, recovery_mode='percentage'): 
        self.time_horizon = time_horizon
        self.starting_point = starting_point
        self.duration = duration
        
        self.value = value
        self.value = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1), columns=['Value']) 
        self.value.loc[self.starting_point:self.time_horizon, 'Value'] = value

        self.limit_sup = limit_sup
        self.recovery_mode = recovery_mode
        self.recovery_frequency = recovery_frequency
        self.recovery_percentage = recovery_percentage
        
    def computeProvision(self, WStream_in, current_step, type='PPB'):
        # computes the inf limit of the provisions
        flag = 0
        if(type == 'PPB'):
            pass # implementer ici la formule de calcul de la PPB
        elif(type == 'PRE'):
            pass # implementer ici la formule de calcul de la PRE
        elif(type == 'Reserve de cap'):
            pass # implementer ici la formule de la CapRes
        elif('Fonds propres'):
            pass # implementer ici la formule de calcul des FP
        return flag
        # updates the self.value
     
    def update(self, current_step, amount_wealth): # on implemente ici les regles de mise a jour auto
        # on actualise la provision avec les reprises
        flag = 0
        
        if(self.recovery_mode == 'percentage'):
            flag = self.recovery_percentage * self.value.loc[current_step, 'Value']
            self.recover(amount=min(flag, self.value.loc[current_step, 'Value']), current_step=current_step)           
        elif(self.recovery_mode == 'frequency'):
            pass
        
        if(amount_wealth*self.limit_sup < self.value.loc[current_step, 'Value']):
            tmp = self.value.loc[current_step, 'Value'] - amount_wealth*self.limit_sup
            self.recover(amount=tmp, current_step=current_step)
            flag += tmp
            
        return flag
    
    def recover(self, amount, current_step):
        # we use some or all the provision to feed a Wealthstream
        self.value.loc[current_step:self.time_horizon, 'Value'] -= amount
        
    def allocate(self, amount, current_step):
        self.value.loc[current_step:self.time_horizon, 'Value'] += amount
        # we receive some or all the provision from a Wealthstream
               
      
    
#--------------------------------------------------
#       Start of the testing part of the code
#--------------------------------------------------

#    def main():
#        prov1 = Provision(value=1000)
#        prov2 = Provision(value=800, starting_point=20)
#        for i in range(1, prov1.time_horizon+1):
#            prov1.update(i, amount_wealth=5000)
##            prov1.allocate(amount=2000, current_step=i)
#            prov2.update(i, amount_wealth=5000)
#        df = prov1.value.plot()
#        prov2.value.plot(ax=df)
#        
#        
#    if __name__ == "__main__":
#        main()    
