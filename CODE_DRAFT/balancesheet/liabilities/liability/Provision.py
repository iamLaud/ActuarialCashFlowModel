# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 10:18:45 2017

@author: FR015797 (aka Laurent DEBRIL)
"""

#--------------------------------------------------
#           Project packages
#--------------------------------------------------

#--------------------------------------------------
#       Start of the proper code
#--------------------------------------------------

class Provision():
    """A class modeling the structure of a provision as used in the ALM model:

    Attributes:
        value: A value of the provision over time (N-array of floats)
        time_horizon: The time horizon over which the simulation takes place (integer).
    """
    
    def __init__(self): 
        self.time_horizon = 50 # default time_horizon setting is 50 years 
        self.value = [None] * self.time_horizon 
      
    def compute_provision(self):
        raise NotImplementedError('You need to define a computation method for the provision!')
     
    def step(self, aProvision = None):
        if aProvision is not None:
            self.value.append(aProvision)  
    
    def recover(self):
        raise NotImplementedError('Not implemented yet!')
    
    def allocate(self):
        raise NotImplementedError('Not implemented yet!')
               
    def __str__(self):
     return "The value of the provision per year of simulation is \n" + (self.get_provision())
    
    
#--------------------------------------------------
#       Inherited classes
#--------------------------------------------------


class MathProvision(Provision): #PM
    """A class modeling the structure of a provision as used in the ALM model:

    Attributes:
        value: A value of the provision over time (N-array of floats)
        time_horizon: The time horizon over which the simulation takes place (integer).
    """
    def __init__(self): 
        self.time_horizon = 50 # default time_horizon setting is 50 years 
        self.value = [None] * self.time_horizon 

    
    
    
class ProfitSharingProvision(Provision): #PPB
    """A class modeling the structure of a provision as used in the ALM model:

    Attributes:
        value: A value of the provision over time (N-array of floats)
        time_horizon: The time horizon over which the simulation takes place (integer).
        upper_bound: The upward limit of the provision in percentage of MP
        lower_bound: the downward limit of the provision in percentage of MP
    """
    def __init__(self): 
        self.time_horizon = 50 # default time_horizon setting is 50 years 
        self.value = [None] * self.time_horizon 
        self.RECOVERY_FREQUENCY = 8 # recovery: every 3, 6 or 8 years e.g
        self.upper_bound = .08
        self.lower_bound = .01



class LiquidityRiskProvision(Provision): #PRE
    """A class modeling the structure of a provision as used in the ALM model:

    Attributes:
        value: A value of the provision over time (N-array of floats)
        time_horizon: The time horizon over which the simulation takes place (integer).
        upper_bound: The upward limit of the provision in percentage of MP
        lower_bound: the downward limit of the provision in percentage of MP
    """
    def __init__(self): 
        self.time_horizon = 50 # default time_horizon setting is 50 years 
        self.value = [None] * self.time_horizon 
        self.POTENTIAL_LOSS_RATIO = .08 # PRE should cover for x% of the total unrealized losses and be inferior to the total


    def check_reg_compliance(self, aList):
        return (((self.get_provision() >= aList * self.POTENTIAL_LOSS_RATIO).all()) and ((self.get_provision() < aList).all())) # to be tested