# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 10:17:45 2017

@author: FR015797 (aka Laurent DEBRIL)
"""

#--------------------------------------------------
#           Project packages
#--------------------------------------------------
from Rate import Rate
#--------------------------------------------------
#       Start of the proper code
#--------------------------------------------------

class RateTarget(Rate):
    """A class modeling the structure of the targeted rate as stated in the ALM model:

    Attributes:
        value: A value of the rate over time (N-array of floats)
        time_horizon: The time horizon over which the simulation takes place (integer).
    """
       
    def compute_rate(self):
        raise NotImplementedError('You need to define a computation method for the rate!')


#--------------------------------------------------
#       Start of the testing part of the code
#--------------------------------------------------

def main():
    target_rate = RateTarget()

if __name__ == "__main__":
    main()