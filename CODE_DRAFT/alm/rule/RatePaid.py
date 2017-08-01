# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 18:05:24 2017

@author: FR015797
"""

#--------------------------------------------------
#           Project packages
#--------------------------------------------------
from Rate import Rate
#--------------------------------------------------
#           Python packages
#--------------------------------------------------
import numpy as np
import pandas as pd
#--------------------------------------------------
#       Start of the proper code
#--------------------------------------------------

class RatePaid(Rate):
    def __init__(self, time_horizon=50, value=0):
        self.time_horizon = time_horizon
        self.value = pd.DataFrame(data=value, index=np.arange(1,self.time_horizon+1), columns=['RRate'])
        
    def computeRate(self, current_step=1):
        """
            compute the value of the rate at the current step after comparison with the series containing the available wealth
        """
        self.value.loc[current_step:self.time_horizon, 'RRate'] = 0 #.85 * fin_benefits.loc[current_step]
    
    
#--------------------------------------------------
#       Start of the testing part of the code
#--------------------------------------------------

def main():
   pass

if __name__ == "__main__":
    main()
