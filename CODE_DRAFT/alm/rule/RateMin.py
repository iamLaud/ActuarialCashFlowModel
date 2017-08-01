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
import gc 
#--------------------------------------------------
#       Start of the proper code
#--------------------------------------------------

class RateMin(Rate):
    def __init__(self, time_horizon=50, value=0):
        self.time_horizon = time_horizon
        self.value = pd.DataFrame(data=value, index=np.arange(1,self.time_horizon+1), columns=['RRate'])    
        
    def computeRate(self, current_step=1):
        self.value.iloc[current_step:, 0] = 0.
        # pour le moment on fixe le taux contractuel a une constante i = 2%
    
    def __str__(self):
        pass
    
#--------------------------------------------------
#       Start of the testing part of the code
#--------------------------------------------------

#def main():
#   rate = RateMin()
#   rate.computeRate()
#   print(rate.value)
#
#if __name__ == "__main__":
#    main()
