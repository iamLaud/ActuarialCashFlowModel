# -*- coding: utf-8 -*-
"""
Created on Wed May 31 15:43:33 2017

@author: Laurent DEBRIL
Date of last revision: May 31st 2017

"""

#--------------------------------------------------
#           Project packages
#--------------------------------------------------
#from Rule import Rule
from Assets import Assets, Bond, Equity, Cash 
from Liabilities import Liabilities, Liability
from WealthStream import WealthStream
from ALM_HMI import ALM_HMI
from ESGLinker import ESGLinker
#--------------------------------------------------
#           Python packages
#--------------------------------------------------
import numpy as np
import pandas as pd
import time
import gc 
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
        self.setTraj()
#        self.assets = Assets(nb_bond=1, nb_equity=1, nb_cash=1, \
#                 ratio={'Bond':.7, 'Equity':.2, 'Cash':.1},\
#                 wealth = 1000, time_horizon=time_horizon)
#        self.liabilities = Liabilities(cap_reserve=None, math_provision=None,\
#                 own_funds=None, profit_shar_prov=None,\
#                 eligib_prov=None, time_horizon=time_horizon)
#        self.cash_flows = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1), columns=['CF_in', 'CF_out'])
#        ---------- INITIALIZATION ------------------------       
        self.setWS()        
#        ----------- INDICATORS ----------------------------
        self.bel = 0.        
        self.vif = 0.
        self.scr = 0.
        self.mcr = 0.
        
        self.generator = ESGLinker()
#       ------- INIT NEW YIELD RATE AT EACH NEW TRAJECTORY -----------------------
#        A REMPLACER A TERME PAR LES INPUTS DE L'ESG
#        noise = np.random.normal(0, .02, size=30)
#        USrate = (np.asarray([1.22,	1.35,	1.51,	1.65,	1.78,	1.89,	1.98,	2.06,	2.13,	2.19,	2.24,	2.29,\
#                              3,	2.37,	2.41,	2.45,	2.49,	2.53,	2.56,	2.60,	2.63,	2.67,	2.70,	2.73,	2.77,\
#                              0,	2.83,	2.86,	2.89,	2.91])/100 + noise).transpose()
#        self.bond_info = pd.DataFrame(data=0, index=np.arange(1,self.assets.portfolio[0].MAX_MATURITY+1), columns=['RRate', 'Spreads'])
#        self.bond_info.loc[:, 'RRate'] = USrate
#        self.bond_info.loc[:, 'Spreads'] = 1
##        --------------------------------------------------------------------
#        self.statement = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1),\
#                                      columns=['financial_income', 'margin', 'benefits', 'tech_income', 'admin_income'])
        
    def simulatePeriod(self, current_step):
        self.updateStart(current_step)
        self.updateMid(current_step)
        self.updateEnd(current_step)
        
    def updateStart(self, current_step):
        # ------- ASSETS ------------
        self.assets.update(current_step=current_step,                   \
                           current_yield=self.bond_info.loc[:, 'RRate'],\
                           spreads=self.bond_info.loc[:, 'Spreads'],    \
                           cash_flows=self.cash_flows,                  \
                           statement=self.statement) 
        # on met à jour le bilan Actifs-Passif
        # ------- LIABILITIES -------
        flag = self.liabilities.update(current_step=current_step,       \
                                       cash_flows=self.cash_flows,      \
                                       available_wealth=self.available_wealth.value,\
                                       mode='mid')
        # actualisation de la PM et du portefeuille d'actifs ici (revente en face des sorties de contrats etc)
        self.setWS()
       
    def updateMid(self, current_step):
        # ------- LIABILITIES -------
        flag = self.liabilities.update(current_step=current_step,      \
                                       cash_flows=self.cash_flows,     \
                                       available_wealth=self.available_wealth.value,\
                                       mode='end')
        # on met à jour les jours les passifs
        # on cherche a servir les taux en appelant les differents leviers -- appeler la fonction computeRate de la classe Rate ici
        # toutes les classes de Rate seront appelees ici et interagiront avec les WealthStreams
        self.available_wealth.computeWealth()
        self.setWS()

    def updateEnd(self, current_step):
        # on alloue les provisions et les benefices + marges
        # reallocation et rebalancement
        self.available_wealth.computeWealth()

    def setWS(self):
        self.available_wealth = WealthStream(time_horizon=self.time_horizon)
        for e in self.assets.portfolio:
            self.available_wealth.add(e.value.loc[:, 'Market Value'])
        pgl = self.assets.computePortfolioPGL()  
        self.potential_gain = WealthStream(time_horizon=self.time_horizon)
        self.potential_gain.add(pgl.iloc[:, 1])
        self.potential_loss = WealthStream(time_horizon=self.time_horizon)
        self.potential_loss.substract(abs(pgl.iloc[:, 2]))
        self.net_potential_gain = self.potential_gain + self.potential_loss
        self.net_wealth = self.available_wealth + self.net_potential_gain
        self.max_wealth = self.available_wealth + self.potential_gain
        self.min_wealth = self.available_wealth + self.potential_loss
     
    def setTraj(self):
        self.assets = Assets(nb_bond=1, nb_equity=1, nb_cash=1, \
             ratio={'Bond':.7, 'Equity':.2, 'Cash':.1},\
             wealth = 1000, time_horizon=self.time_horizon)
        self.liabilities = Liabilities(cap_reserve=None, math_provision=None,\
             own_funds=None, profit_shar_prov=None,\
             eligib_prov=None, time_horizon=self.time_horizon)
        self.cash_flows = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1), columns=['CF_in', 'CF_out'])
        noise = np.random.normal(0, .02, size=30)
        USrate = (np.asarray([1.22,	1.35,	1.51,	1.65,	1.78,	1.89,	1.98,	2.06,	2.13,	2.19,	2.24,	2.29,\
                              3,	2.37,	2.41,	2.45,	2.49,	2.53,	2.56,	2.60,	2.63,	2.67,	2.70,	2.73,	2.77,\
                              0,	2.83,	2.86,	2.89,	2.91])/100 + noise).transpose()
        self.bond_info = pd.DataFrame(data=0, index=np.arange(1,self.assets.portfolio[0].MAX_MATURITY+1), columns=['RRate', 'Spreads'])
        self.bond_info.loc[:, 'RRate'] = USrate
        self.bond_info.loc[:, 'Spreads'] = 1
#        --------------------------------------------------------------------
        self.statement = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1),\
                                      columns=['financial_income', 'margin', 'benefits', 'tech_income', 'admin_income'])

# --------------  MAIN OF THE PROGRAM -----------------------
    def main():
#       ------------------- DYNAMIC RAM CLEANING ---------------------
        gc.enable() 
        # --------- TIME STAMPING ------------------------------------
        start_time = time.time()
        # ---------------------------------------------------------

        simulator = ALMComputer(time_horizon=50, nb_simulation=40)
        hmi = ALM_HMI(simulator) # we pair the simulator and the HMI

        for k in range(1, simulator.nb_simulation+1):
            # reinitialiser les variables a chaque nouvelle simulation
            for t in range(1, simulator.time_horizon+1):
                simulator.simulatePeriod(t)
            print("Trajectory #", k)
#           ----------- WE SAVE THE VARIABLES WE WANT AT THE END OF EACH TRAJECTORY PROJECTION     
            if(k == 1):
                hmi.save(ALM=simulator, exists=False, var_name='available_wealth')
                hmi.save(ALM=simulator, exists=False, var_name='potential_gain')
                hmi.save(ALM=simulator, exists=False, var_name='potential_loss')
                hmi.save(ALM=simulator, exists=False, var_name='net_potential_gain')
                hmi.save(ALM=simulator, exists=False, var_name='max_wealth')
                hmi.save(ALM=simulator, exists=False, var_name='min_wealth')
                hmi.save(ALM=simulator, exists=False, var_name='net_wealth')
                hmi.saveDF(ALM=simulator, exists=False, var_name='cash_flows')
                hmi.saveDF(ALM=simulator, exists=False, var_name='statement')

            else:
                hmi.save(ALM=simulator, exists=True, var_name='available_wealth')
                hmi.save(ALM=simulator, exists=True, var_name='potential_gain')
                hmi.save(ALM=simulator, exists=True, var_name='potential_loss')
                hmi.save(ALM=simulator, exists=True, var_name='net_potential_gain')
                hmi.save(ALM=simulator, exists=True, var_name='max_wealth')
                hmi.save(ALM=simulator, exists=True, var_name='min_wealth')
                hmi.save(ALM=simulator, exists=True, var_name='net_wealth')
                hmi.saveDF(ALM=simulator, exists=True, var_name='cash_flows')
                hmi.saveDF(ALM=simulator, exists=True, var_name='statement')
              
            simulator.setTraj()
   
#        actualiser la somme de bel, vif, scr et mcr ici
        simulator.bel /= simulator.nb_simulation
        simulator.vif /= simulator.nb_simulation
        simulator.scr = None
        simulator.mcr = None

#       -------------- INFO SCREEN DISPLAY -----------------
        duration = time.time() - start_time
        hmi.display(nb_simulation=simulator.nb_simulation, time_horizon=simulator.time_horizon, duration=duration)
        # we display some information from the simulation onto the screen 
        gc.enable()
        
    if __name__ == "__main__":
        main()