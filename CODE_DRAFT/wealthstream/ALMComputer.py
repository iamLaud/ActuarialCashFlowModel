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
from ALM_HMI import ALM_HMI
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
        This class is the core of the simulator and builds the bridge
        between the different parts of the code.
    """
    def __init__(self, time_horizon=50, nb_simulation=1000):
#        --------- SIMULATION PARAMETERS -------------------
        self.nb_simulation = nb_simulation
        self.time_step = 0 # on initialise l'horloge de la trajectoire
        self.time_horizon = time_horizon
#        self.rules = Rule() # Management rules
        self.assets = Assets(nb_bond=1, nb_equity=1, nb_cash=1, \
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
#       ---
        self.potential_gain = WealthStream()
        self.potential_gain.add(pgl.iloc[:, 1])
#       ---
        self.potential_loss = WealthStream()
        self.potential_loss.substract(pgl.iloc[:, 2])
#       ---
        self.net_potential_gain = self.potential_gain + self.potential_loss
        self.net_wealth = self.available_wealth + self.net_potential_gain
#       ---------------------------------------------------   
        self.max_wealth = self.available_wealth + self.potential_gain
        self.min_wealth = self.available_wealth + self.potential_loss
        
#       ---------------------------------------------------   
        self.total_asset_wealth = self.available_wealth + self.net_potential_gain
        self.financial_income = WealthStream()
#        self.technical_income = WealthStream() # set to 0 for Life
#        self.admin_income = WealthStream() # not modeled yet
        
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


# --------------  MAIN OF THE PROGRAM -----------------------
    def main():
        gc.enable() # Nettoyage dynamique de la RAM
        # --------- TIME STAMPING ------------------------------------
        start_time = time.time()
        # ---------------------------------------------------------

        simulator = ALMComputer(time_horizon=50, nb_simulation=1000)
        hmi = ALM_HMI(simulator)
        for k in range(1, simulator.nb_simulation+1):
            # reinitialiser les variables a chaque nouvelle simulation
            for t in range(1, simulator.time_horizon+1):
                simulator.simulatePeriod()    
#           ----------- WE SAVE AT THE END OF EACH TRAJECTORY PROJECTION     
            if(k == 1):
                hmi.save(ALM=simulator, exists=False, var_name='available_wealth')
                hmi.save(ALM=simulator, exists=False, var_name='potential_gain')
                hmi.save(ALM=simulator, exists=False, var_name='potential_loss')
                hmi.save(ALM=simulator, exists=False, var_name='net_potential_gain')
                hmi.save(ALM=simulator, exists=False, var_name='max_wealth')
                hmi.save(ALM=simulator, exists=False, var_name='min_wealth')
                hmi.save(ALM=simulator, exists=False, var_name='net_wealth')
                hmi.save(ALM=simulator, exists=False, var_name='margin')
                hmi.save(ALM=simulator, exists=False, var_name='benefits')
                hmi.save(ALM=simulator, exists=False, var_name='cash_flow_in')
                hmi.save(ALM=simulator, exists=False, var_name='cash_flow_out')
            else:
                hmi.save(ALM=simulator, exists=True, var_name='available_wealth')
                hmi.save(ALM=simulator, exists=True, var_name='potential_gain')
                hmi.save(ALM=simulator, exists=True, var_name='potential_loss')
                hmi.save(ALM=simulator, exists=True, var_name='net_potential_gain')
                hmi.save(ALM=simulator, exists=True, var_name='max_wealth')
                hmi.save(ALM=simulator, exists=True, var_name='min_wealth')
                hmi.save(ALM=simulator, exists=True, var_name='net_wealth')
                hmi.save(ALM=simulator, exists=True, var_name='margin')
                hmi.save(ALM=simulator, exists=True, var_name='benefits')
                hmi.save(ALM=simulator, exists=True, var_name='cash_flow_in')
                hmi.save(ALM=simulator, exists=True, var_name='cash_flow_out')
                
#        actualiser la somme de bel, vif, scr et mcr ici
        simulator.bel /= simulator.nb_simulation
        simulator.vif /= simulator.nb_simulation
        simulator.scr = None
        simulator.mcr = None
        
#       -------------- INFO SCREEN DISPLAY -----------------
        duration = time.time() - start_time
        hmi.display(nb_simulation=simulator.nb_simulation, time_horizon=simulator.time_horizon, duration=duration)
        
    if __name__ == "__main__":
        main()