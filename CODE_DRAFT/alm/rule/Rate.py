# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 18:05:24 2017

@author: FR015797
"""

#--------------------------------------------------
#           Project packages
#--------------------------------------------------
#--------------------------------------------------
#           Python packages
#--------------------------------------------------
import numpy as np
import pandas as pd
import gc
#--------------------------------------------------
#       Start of the proper code
#--------------------------------------------------

class Rate(object):
    def __init__(self, time_horizon=50, value=0):
        self.time_horizon = time_horizon
        self.value = pd.DataFrame(data=value, index=np.arange(1,self.time_horizon+1), columns=['RRate'])
        
    def computeRate(self):
        raise NotImplementedError("Subclass must implement abstract method")
    
##--------------------------------------------------
##       Start of the testing part of the code
##--------------------------------------------------
#
#def main():
#   pass
#
#if __name__ == "__main__":
#    main()
