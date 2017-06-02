# -*- coding: utf-8 -*-
"""
Created on May 14th 2017

@author: Laurent DEBRIL
Date of last revision: May 29th 2017

"""

#--------------------------------------------------
#           Project packages
#--------------------------------------------------
from Provision import Provision
from Liability import Liability
#--------------------------------------------------
#           Python packages
#--------------------------------------------------
import numpy as np
import pandas as pd

#--------------------------------------------------
#       Start of the proper code
#--------------------------------------------------

class Liabilities(object):
    def __init__(self, cap_reserve=None, math_provision=None,\
                 own_funds=None, profit_shar_prov=None, eligib_prov=None, time_horizon=50):
             
        self.math_provision = [] # List des contrats d'assurance
        self.other_provisions = {} # Dict des provisions hors PM
        self.time_horizon = time_horizon
# ---------------------------------------------------------            
        if(math_provision != None):
            self.math_provision.append(math_provision)
        else:
            self.math_provision.append(Liability(value=600))  
            self.math_provision.append(Liability(value=60))          
            self.math_provision.append(Liability(value=6))          

            # parametrer la provision
# ---------------------------------------------------------                   
        if(cap_reserve != None):
            self.other_provisions['Reserve de cap'] = cap_reserve
        else:
            self.other_provisions['Reserve de cap'] = Provision(value=25)
            # parametrer la provision
# ---------------------------------------------------------                        
        if(own_funds != None):
            self.other_provisions['Fonds propres'] = own_funds
        else:
            self.other_provisions['Fonds propres'] = Provision(value=42)
            # parametrer la provision
# ---------------------------------------------------------                        
        if(profit_shar_prov != None):
            self.other_provisions['PPB'] = profit_shar_prov
        else:
            self.other_provisions['PPB'] = Provision(value=933)
            # parametrer la provision
# ---------------------------------------------------------                       
        if(eligib_prov != None):
            self.other_provisions['PRE'] = eligib_prov
        else:
            self.other_provisions['PRE'] = Provision(value=1)
            # parametrer la provision
# ---------------------------------------------------------                       

    def computeProvisions(self, aWStream):
        # on recalcule les valeurs des provisions 
        # en fonction de l'etat de notre portefeuille d'actifs
        for e in self.other_provisions:
            pass
     
    def computeMPVal(self):
        val = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1),\
                           columns=['MP Value'])
        for e in self.math_provision:
            val.loc[:, 'MP Value'] += e.value.loc[:, 'Contract Value']     
        return val
    
    def computeValAll(self):
        val = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1),\
                           columns=['Liabilities Value'])
        for e in self.math_provision:
            val.loc[:, 'Liabilities Value'] += e.value.loc[:, 'Contract Value']     
        for key, value in self.other_provisions.items():            
            val.loc[:, 'Liabilities Value'] += value.value.loc[:, 'Value']
        return val
    
    def update(self, current_step, mode='early'): # on actualise ici les contrats d'assurance
        if(mode == 'early'):
            for e in self.math_provision:
                if(e.update(current_step) != 0):
                    pass #si !=0 on a des sorties de contrats donc on doit vendre des actifs en face
            
            for key, e in self.other_provisions.items():            
                e.update(current_step) 
            
#--------------------------------------------------
#       Start of the testing part of the code
#--------------------------------------------------

def main():
    passif = Liabilities()
    print(passif.computeMPVal())

    
if __name__ == "__main__":
    main()