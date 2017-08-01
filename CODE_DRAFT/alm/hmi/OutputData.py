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
import pandas as pd
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
    
    def dataFrame2CSV(self, ALM, exists=False, var_name=None):
        if(var_name == None):
            var_name = 'cash_flows'
        headers = getattr(ALM, var_name).dtypes.index
        for h in headers:
            filename = "".join(['\save_', str(h), '.csv'])
            if(not exists):
                pd.DataFrame(getattr(ALM, var_name).loc[:, h]).T.to_csv("".join([self.path, filename]), sep=';')
            else:  
                with open(self.path+filename, 'a') as f: # 'a' mode stands for append data at the end of the existing file
                    pd.DataFrame(getattr(ALM, var_name).loc[:, h]).T.to_csv(f, header=False, sep=';')

    def dict2CSV(self, ALM, exists=False, var_name1=None, var_name2=None):
        if(var_name1 == None):
            var_name1 = 'liabilities'
        if(var_name2 == None):
            var_name2 = 'other_provisions'
        for key, value in getattr(getattr(ALM, var_name1), var_name2).items():
            filename = "".join(['\save_', str(key), '.csv'])
            if(not exists):
                getattr(getattr(ALM, var_name1), var_name2)[key].value.transpose().to_csv("".join([self.path, filename]), sep=';')
            else:  
                with open(self.path+filename, 'a') as f: # 'a' mode stands for append data at the end of the existing file
                    getattr(getattr(ALM, var_name1), var_name2)[key].value.transpose().to_csv(f, header=False, sep=';') 
