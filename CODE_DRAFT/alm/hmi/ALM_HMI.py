# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 10:22:39 2017

@author: Laurent DEBRIL
"""

#--------------------------------------------------
#           Project packages
#--------------------------------------------------
from InputData import InputData
from OutputData import OutputData
#--------------------------------------------------
#           Python packages
#--------------------------------------------------

#--------------------------------------------------
#       Start of the proper code
#--------------------------------------------------

class ALM_HMI(object):
    def __init__(self, ALM):
        self.input = InputData()
        self.output = OutputData()
        self.ALM = ALM
    
    def save(self, ALM, exists, var_name):
        self.output.exportCSV(ALM=ALM, exists=exists, var_name=var_name)
    
    def saveDF(self, ALM, exists, var_name):
        self.output.dataFrame2CSV(ALM=ALM, exists=exists, var_name=var_name)
   
    def saveDict(self, ALM, exists, var_name1, var_name2):
        self.output.dict2CSV(ALM=ALM, exists=exists, var_name1=var_name1, var_name2=var_name2)
     
    def load(self):
        pass
    
    def display(self, nb_simulation, time_horizon, duration, BEL=None, VIF=None, SCR=None):
        print('A l\'issue de la simulation sur ' + str(nb_simulation) + ' trajectoires sur ' +\
              str(time_horizon) + ' annees:', end='\n')
        print('Valeur de la BEL: ', BEL, end='\n')
        print('Valeur de la VIF: ', VIF, end='\n')
        print('Valeur du SCR: ', SCR, end='\n')
        print("--- Simulation ran in %s seconds ---" % (duration))

