# -*- coding: utf-8 -*-
"""
Created on Thu May 18 10:01:38 2017

@author: FR015797
Date of last revision: May 18th 2017
"""


#--------------------------------------------------
#           Project packages
#--------------------------------------------------
from Asset import Asset

#--------------------------------------------------
#           Python packages
#--------------------------------------------------
import numpy as np
import pandas as pd
#--------------------------------------------------
#       Start of the proper code
#--------------------------------------------------

class Cash(Asset):        
    def updateValue(self, current_step):
        self.value.loc[current_step:self.time_horizon, 'Value'] = self.value.loc[current_step, 'Value'] * (1 + self.return_rate.loc[current_step, 'RRate'])
        
    def cashOut(self, current_step):
        output = self.value.loc[current_step, 'Value'] * self.volume.loc[current_step, 'Volume']
        if(current_step < self.time_horizon):
            self.volume.loc[np.arange(current_step+1,self.time_horizon+1), 'Volume'] = 0
            print("Cash cashout")
        return output    
    
    def getWealth(self, current_step):
        return (self.value.loc[current_step, 'Value'] * self.volume.loc[current_step, 'Volume'])

    def update(self, current_step):
        self.updateValue(current_step)
        return(0)
    
#--------------------------------------------------
#       Start of the testing part of the code
#--------------------------------------------------

#def main():
#    cash = Cash(value=1, volume=100)

  
#if __name__ == "__main__":
#    main()