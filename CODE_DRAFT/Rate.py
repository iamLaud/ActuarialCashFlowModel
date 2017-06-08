# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 10:17:45 2017

@author: FR015797 (aka Laurent DEBRIL)
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

class Rate():
    """A class modeling the structure of a rate as used in the ALM model:

    Attributes:
        value: A value of the rate over time (DataFrame of floats)
        time_horizon: The time horizon over which the simulation takes place (integer).
    """
    
    def __init__(self, time_horizon=50, value=0): 
        self.time_horizon = time_horizon 
        self.value = pd.DataFrame(data=value,\
                                  index=np.arange(1,time_horizon+1),\
                                  columns=['Rate'])
 
    def compute_rate(self):
        raise NotImplementedError('You need to define a computation method for the rate!')
    
    def __str__(self):
     return "The value of the rate per year of simulation is \n" + str(self.value)