# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 15:36:21 2016

@author: Jun JING
"""

## Progam packages
#from ...asset.Asset_data import Asset_data

## Python packages
from abc import ABCMeta, abstractmethod

class credit_model_base:
    """
        This is purely abstract class for all credit models we will implement in the future
    """

    __metaclass__=ABCMeta

    @abstractmethod
    def add_time_horizon(self, time_horizon):
        """This method add time horizon """
        return

    @abstractmethod
    def get_spread(self):
        """This method get the market spread"""
        return

    @abstractmethod
    def get_RN_transition_matrix(self):
        """This method get the historical transition matrix"""
        return
        

    @abstractmethod
    def calibrate_spread(self):
        """Calibrate the credit model onto the market environment"""
        return


    @abstractmethod
    def generate_spreads_and_matrix(self):
        """generate the spreads"""
        return