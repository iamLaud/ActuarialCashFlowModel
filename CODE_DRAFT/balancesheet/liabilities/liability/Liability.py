# -*- coding: utf-8 -*-
"""
Created on Thu May 18 10:01:38 2017

@author: FR015797
Date of last revision: May 18th 2017
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
    def __init__(self, value=1, duration=50):
        self.duration = duration
        self.value = pd.DataFrame(data=value, index=np.arange(1,duration+1), columns=['Value'])
    
    def update(self):
        pass
    
    def __str__(self):
        return("value: " + self.value.__str__() + "\n")
    
#--------------------------------------------------
#       Start of the testing part of the code
#--------------------------------------------------

def main():
    test = Liability(value=10, duration=20)        
    #test = Liability()
    #print(test1.__str__())
    print(str(test.duration))
    print(test.value)
    
if __name__ == "__main__":
    main()