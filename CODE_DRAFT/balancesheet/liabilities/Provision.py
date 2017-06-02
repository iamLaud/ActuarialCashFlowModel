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
                 duration=20, limit=.2, recovery_frequency=0,\
                 recovery_percentage=0, recovery_mode='percentage'): 
        self.time_horizon = time_horizon
        self.starting_point = starting_point
        self.duration = duration
        
        self.value = value
        self.value = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1), columns=['Value']) 
        self.value.loc[self.starting_point:self.time_horizon, 'Value'] = value

        self.limit = limit
        self.recovery_mode = recovery_mode
        self.recovery_frequency = recovery_frequency
        self.recovery_percentage = recovery_percentage
        
    def computeProvision(self, aWStream, type='PPB'):
        if(type == 'PPB'):
            pass # implementer ici la formule de calcul de la PPB
        elif(type == 'PRE'):
            pass # implementer ici la formule de calcul de la PRE
        elif(type == 'Reserve de cap'):
            pass # implementer ici la formule de la CapRes
        elif('Fonds propres'):
            pass # implementer ici la formule de calcul des FP
        # updates the self.value
     
    def update(self, current_step): # on implemente ici les regles de mise a jour auto
        # on actualise la provision avec les reprises
        if(self.recovery_mode == 'percentage'):
            pass
        elif(self.recovery_mode == 'frequency'):
            pass
    
    def recover(self, amount):
        # we use some or all the provision to feed a Wealthstream
        raise NotImplementedError('Not implemented yet!')

    def allocate(self, amount):
        raise NotImplementedError('Not implemented yet!')
        # we receive some or all the provision to feed a Wealthstream
               
    def __str__(self):
     return "The value of the provision per year of simulation is \n" + (self.get_provision())
    
    
#--------------------------------------------------
#       Start of the testing part of the code
#--------------------------------------------------

#    def main():
#        prov1 = Provision()
#        prov2 = Provision(value=20, starting_point=5)
#        print(prov1.value['Value'] +prov2.value['Value'])
#        
#        
#    if __name__ == "__main__":
#        main()    
