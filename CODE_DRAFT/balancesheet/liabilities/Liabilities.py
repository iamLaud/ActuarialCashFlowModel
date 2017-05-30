# -*- coding: utf-8 -*-
"""
Created on May 14th 2017

@author: Laurent DEBRIL
Date of last revision: May 29th 2017

"""

#--------------------------------------------------
#           Project packages
#--------------------------------------------------
import Provision as Provision
import Liability as Liability
#--------------------------------------------------
#           Python packages
#--------------------------------------------------
import numpy as np
import pandas as pd

#--------------------------------------------------
#       Start of the proper code
#--------------------------------------------------

class Liabilities(object):
    def __init__(self, capitalization_reserve, technical_provision, own_fund, PRE, liabilities_data):
        self.portfolio = []
        self.portfolio.append(capitalization_reserve)
        self.portfolio.append(technical_provision)
        self.portfolio.append(own_fund)
        self.portfolio.append(PRE)
        self.portfolio.append(liabilities_data)


    def updatePortfolio(self):
        pass
    
    def computePorfolioVal(self):
        pass
    
    def update(self):
        pass