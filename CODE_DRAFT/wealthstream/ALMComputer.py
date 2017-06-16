# -*- coding: utf-8 -*-
"""
Created on Wed May 31 15:43:33 2017

@author: Laurent DEBRIL
Date of last revision: May 31st 2017

"""

#--------------------------------------------------
#           Project packages
#--------------------------------------------------
#from Rule import *
from Assets import Assets, Bond, Equity, Cash 
from Liabilities import Liabilities, Liability
from WealthStream import WealthStream
#--------------------------------------------------
#           Python packages
#--------------------------------------------------
import numpy as np
import pandas as pd
import time
import gc 
import copy
#--------------------------------------------------
#       Start of the proper code
#--------------------------------------------------

class ALMComputer(object):
    """
        This class is the core of the simulator and builds the bridge between the different
        parts of the code.
    """
    def __init__(self, time_horizon=50, nb_simulation=1000):
#        --------- SIMULATION PARAMETERS -------------------
        self.nb_simulation = nb_simulation
        self.time_step = 0 # on initialise l'horloge de la trajectoire
        self.time_horizon = time_horizon
#        self.rules = Rule()
        self.assets = Assets(nbBond=1, nbEquity=1, nbCash=1, \
                 ratio={'Bond':.7, 'Equity':.2, 'Cash':.1},\
                 wealth = 1000, time_horizon=50)
        self.liabilities = Liabilities(cap_reserve=None, math_provision=None,\
                 own_funds=None, profit_shar_prov=None,\
                 eligib_prov=None, time_horizon=50)
        
#        ---------- INITIALIZATION ------------------------       
        self.available_wealth = WealthStream()
        for e in self.assets.portfolio:
            self.available_wealth.add(e.value.iloc[:, 0]*e.volume.iloc[:, 0])
            # initialization by Market Cap (=unit value(column 0) x volume)
#       ---------------------------------------------------
        pgl = self.assets.computePortfolioPGL()  
        mean = 0
        std = 50
        noise1 = np.random.normal(mean, std, size=self.time_horizon)
        noise2 = np.random.normal(mean, std, size=self.time_horizon)
        pgl.iloc[:, 1] = abs(noise1)
        pgl.iloc[:, 2] = abs(noise2)
        a=pgl.iloc[:, 1].plot()
        pgl.iloc[:, 2].plot(ax=a)
#       ---
        self.potential_gain = WealthStream()
        self.potential_gain.add(pgl.iloc[:, 1])
#       ---
        self.potential_loss = WealthStream()
        self.potential_gain.substract(pgl.iloc[:, 2])
#       ---
        self.net_potential_gain = WealthStream()
        self.net_potential_gain.add(pgl.iloc[:, 1])
        self.net_potential_gain.substract(pgl.iloc[:, 2])
#       ---------------------------------------------------   
        self.max_wealth = WealthStream()
        self.min_wealth = WealthStream()
        
#       ---------------------------------------------------   
        self.total_asset_wealth = WealthStream()
        self.financial_income = WealthStream()
        self.technical_income = WealthStream()
#        self.admin_income = WealthStream()
        
        self.margin = WealthStream()
        self.benefits = WealthStream()
        self.cash_flow_in = WealthStream()
        self.cash_flow_out = WealthStream()
        
#        ----------- INDICATORS ----------------------------
        self.bel = 0.        
        self.vif = 0.
        self.scr = 0.
        self.mcr = 0.
    
    def simulatePeriod(self):
        self.updateStart()
        self.updateMid()
        self.updateEnd()
    
    def updateStart(self):
        pass # on met à jour les actifs
    
    def updateMid(self):
        pass # on met à jour les jours les passifs
        # on cherche a servir les taux en appelant les differents leviers -- appeler la fonction computeRate de la classe Rate ici
        # toutes les classes de Rate seront appelees ici et interagiront avec les WealthStreams
    
    def updateEnd(self):
        pass # on alloue les provisions et les benefices + marges
        # reallocation et rebalancement

#%%    
# --------------  MAIN OF THE PROGRAM -----------------------
    def main():
        gc.enable() # Nettoyage dynamique de la RAM
        # --------- TIME STAMP ------------------------------------
        start_time = time.time()
        # ---------------------------------------------------------

        simulator = ALMComputer(time_horizon=50, nb_simulation=1000)
        for k in range(1, simulator.nb_simulation+1):
            for t in range(1, simulator.time_horizon+1):
                simulator.simulatePeriod()    
                
        #------------ Save option -----------------
#            path = r'C:\Users\FR015797\Documents\PyALM_gen\data' # write here the absolute path to the data directory of the project
#            filename = '\save_trajectory'+str(k)+'.csv'
#            simulator.available_wealth.to_csv(path+filename, sep=';')
#            with open(path+filename, 'a') as f: # 'a' mode stands for append data at the end of the existing file
#                simulator.max_wealth.to_csv(f, header=True)
#                simulator.min_wealth.to_csv(f, header=True)
#                simulator.net_potential_gain.to_csv(f, header=True)
#                simulator.potential_gain.to_csv(f, header=True)
#                simulator.potential_loss.to_csv(f, header=True)
#                simulator.margin.to_csv(f, header=True)
#                simulator.benefits.to_csv(f, header=True)
#            # actualiser la somme de bel, vif, scr et mcr ici
#        simulator.bel /= simulator.nb_simulation
#        simulator.vif /= simulator.nb_simulation
#        simulator.scr = None
#        simulator.mcr = None
        #------------ calcul du SCR et du MCR ici ---------
        print('A l\'issue de la simulation sur ' + str(simulator.nb_simulation) + ' trajectoires sur ' + str(simulator.time_horizon) + ' annees:', end='\n')
        print('Valeur de la BEL: ', end='\n')
        print('Valeur de la VIF: ', end='\n')
        print('Valeur du SCR: ',end='\n')
        print("--- Simulation ran in %s seconds ---" % (time.time() - start_time))
#        df= simulator.available_wealth.value.plot()
        df = simulator.potential_gain.value.plot()
        simulator.potential_loss.value.plot(ax=df)
#        simulator.net_potential_gain.value.plot(ax=df)
    if __name__ == "__main__":
        main()