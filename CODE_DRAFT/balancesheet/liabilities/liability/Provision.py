# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 10:18:45 2017

@author: FR015797 (aka Laurent DEBRIL)
Date of last revision: May 29th 2017

"""
#--------------------------------------------------
#           Project packages
#--------------------------------------------------
import Liability as Liability
#--------------------------------------------------
#           Project packages
#--------------------------------------------------
import numpy as np
import pandas as pd
#--------------------------------------------------
#       Start of the proper code
#--------------------------------------------------

class Provision(Liability):
    """A class modeling the structure of a provision as used in the ALM model:

    Attributes:
        value: A value of the provision over time (N-array of floats)
        time_horizon: The time horizon over which the simulation takes place (integer).
    """
    
    def __init__(self, volume=0, value=1, time_horizon=50, starting_point=1, duration=20, limit = .2, recovery_frequency = 1/3): 
        self.time_horizon = time_horizon
        self.starting_point = starting_point
        self.duration = duration
        
        self.volume = volume
        self.volume = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1), columns=['Volume']) 
        self.volume.loc[self.starting_point:self.time_horizon, 'Volume'] = volume
        
        self.value = value
        self.value = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1), columns=['Value']) 
        self.value.loc[self.starting_point:self.time_horizon, 'Value'] = value

        self.limit = limit
        self.recovery_frequency = recovery_frequency
        
    def computeProvision(self):
        raise NotImplementedError('You need to define a computation method for the provision!')
     
    def update(self, aProvision = None):
        if aProvision is not None:
            self.value.append(aProvision)  
    
    def recover(self):
        raise NotImplementedError('Not implemented yet!')
    
    def allocate(self):
        raise NotImplementedError('Not implemented yet!')
               
    def __str__(self):
     return "The value of the provision per year of simulation is \n" + (self.get_provision())
    
    
