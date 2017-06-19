# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 10:25:54 2017

@author: Laurent DEBRIL
"""

#--------------------------------------------------
#           Project packages
#--------------------------------------------------

#--------------------------------------------------
#           Python packages
#--------------------------------------------------
#--------------------------------------------------
#       Start of the proper code
#--------------------------------------------------

class OutputData(object):
    def __init__(self, path=r'C:\Users\FR015797\Documents\PyALM_gen\data'):
        self.path = path
    
    def exportCSV(self, ALM, exists=False, var_name=None):
        if(var_name == None):
            var_name = 'available_wealth'
        filename = "".join(['\save_', str(var_name), '.csv'])
        if(not exists):
            getattr(ALM, var_name).value.transpose().to_csv("".join([self.path, filename]), sep=';')
        else:  
            with open(self.path+filename, 'a') as f: # 'a' mode stands for append data at the end of the existing file
                getattr(ALM, var_name).value.transpose().to_csv(f, header=False, sep=';') 
    
    


