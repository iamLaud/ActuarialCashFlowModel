# -*- coding: utf-8 -*-
"""
Created on Wed May 31 15:43:33 2017

@author: Laurent DEBRIL
Date of last revision: May 31st 2017

"""

#--------------------------------------------------
#           Project packages
#--------------------------------------------------
from Rule import Rule
from Assets import Assets
from Liabilities import Liabilities
from WealthStream import WealthStream
#--------------------------------------------------
#           Python packages
#--------------------------------------------------
import numpy as np
import pandas as pd
#--------------------------------------------------
#       Start of the proper code
#--------------------------------------------------

class ALMComputer(object):
    def __init__(self, time_horizon=50, nb_simulation=1000):
#        --------- SIMULATION PARAMETERS -------------------
        self.nb_simulation = nb_simulation
        self.time_step = 0 # on initialise l'horloge de la trajectoire
        self.time_horizon = time_horizon
        self.rules = Rule()
        self.assets = Assets()
        self.liabilities = Liabilities()
        
#        ---------- INITIALIZATION ------------------------       
        self.available_wealth = WealthStream()
        self.max_wealth = WealthStream()
        self.min_wealth = WealthStream()
        self.net_potential_gain = WealthStream()
        self.potential_gain = WealthStream()
        self.potential_loss = WealthStream()
        self.margin = WealthStream()
        self.benefits = WealthStream()
        self.cash_flow_in = WealthStream()
        self.cash_flow_out = WealthStream()
        
#        ----------- INDICATORS ----------------------------
        self.bel = 0        
        self.vif = 0
        self.scr = 0
        self.mcr = 0
    
    def simulatePeriod(self):
        self.updateStart()
        self.updateMid()
        self.updateEnd()
    
    def updateStart(self):
        pass
    
    def updateMid(self):
        pass
    
    def updateEnd(self):
        pass
    
# --------------  MAIN OF THE PROGRAM -----------------------
    def main():
        simulator = ALMComputer(time_horizon=50, nb_simulation=1000)
        for k in range(1, simulator.nb_simulation+1):
            for t in range(1, simulator.time_horizon+1):
                simulator.simulatePeriod()    
            #------------ Save option -----------------
            path = r'C:\Users\FR015797\Documents\PyALM_gen\data' # write here the absolute path to the data directory of the project
            filename = '\save_trajectory'+str(k)+'.csv'
            simulator.available_wealth.to_csv(path+filename, sep=';')
            with open(path+filename, 'a') as f: # 'a' mode stands for append data at the end of the existing file
                simulator.max_wealth.to_csv(f, header=True)
                simulator.min_wealth.to_csv(f, header=True)
                simulator.net_potential_gain.to_csv(f, header=True)
                simulator.potential_gain.to_csv(f, header=True)
                simulator.potential_loss.to_csv(f, header=True)
                simulator.margin.to_csv(f, header=True)
                simulator.benefits.to_csv(f, header=True)
            # actualiser la somme de bel, vif, scr et mcr ici
        simulator.bel /= simulator.nb_simulation
        simulator.vif /= simulator.nb_simulation
#        simulator.scr = 
#        simulator.mcr = 
        #------------ calcul du SCR et du MCR ici ---------
        print('A l''issue de la simulation sur ' + simulator.nb_simulation + ' trajectoires sur ' + simulator.time_horizon + ' annees:', end='\n')
        print('Valeur de la BEL: ', end='\n')
        print('Valeur de la VIF: ', end='\n')
        print('Valeur du SCR: ',end='\n')
        
    if __name__ == "__main__":
        main()