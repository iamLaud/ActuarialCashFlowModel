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
    def __init__(self, volume=0, value=1, time_horizon=50, starting_point=1, duration=20):
        self.time_horizon = time_horizon
        self.starting_point = starting_point
        self.duration = duration
        
        self.volume = volume
        self.volume = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1), columns=['Volume']) 
        self.volume.loc[self.starting_point:self.time_horizon, 'Volume'] = volume
        
        self.value = value
        self.value = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1), columns=['Value']) 
        self.value.loc[self.starting_point:self.time_horizon, 'Value'] = value
        
    def update(self):
        pass
    
    def __str__(self):
        return("value: " + self.value.__str__() + "\n")
    
#--------------------------------------------------
#       Start of the testing part of the code
#--------------------------------------------------
#
#def main():
#
#    
#if __name__ == "__main__":
#    main()