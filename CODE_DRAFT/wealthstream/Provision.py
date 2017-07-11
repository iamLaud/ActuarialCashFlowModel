# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 10:18:45 2017

@author: FR015797 (aka Laurent DEBRIL)
Date of last revision: May 29th 2017

"""
#--------------------------------------------------
#           Project packages
#--------------------------------------------------
#--------------------------------------------------
#           Python packages
#--------------------------------------------------
import numpy as np
import pandas as pd
#--------------------------------------------------
#       Start of the proper code
#--------------------------------------------------

class Provision(object):
    """A class modeling the structure of a provision as used in the ALM model:

    Attributes:
        value: The value of the Provision over time (DataFrame of Float)
        time_horizon: The time horizon over which the simulation takes place (Integer).
        starting_point: The time step when the Provision is created (Integer)
        duration: The life duration of the Provision (Integer)
        limit_sup: The sup limit percentage of the authorized Provision.
        recovery_frequency: The frequency of recovery of the Provision (Float)
        recovery_percentage: The percentage of recovery at each time step (Float)
        recovery_mode: The mode of recovery of the Provision (percentage or frequency)
    """
    
    def __init__(self, value=0, time_horizon=50, starting_point=1,\
                 duration=10, limit_sup=.2, recovery_frequency=0,\
                 recovery_percentage=0.334, recovery_mode='percentage'): 
        self.time_horizon = time_horizon
        self.starting_point = starting_point
        self.duration = duration
        
        self.value = value
        self.value = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1), columns=['Value']) 
        self.value.loc[self.starting_point:self.time_horizon, 'Value'] = value

        self.limit_sup = limit_sup
        self.recovery_mode = recovery_mode
        self.recovery_frequency = recovery_frequency
        self.recovery_percentage = recovery_percentage
        
    def computeProvision(self, wealth, current_step, type='PPB'):
        """Based on a WealthStream point value (wealth), it computes the theoretical 
            value of the Provision at time current_step of the simulation.
            The default setting is the computation of the value of the
            Profit Sharing Provision (PPB in French).
            
        Parameters:
            wealth: a WealthStream point value (Float)
            current_step: the index of the time step (Integer)
            type: determines the type of computation (String)
                type = {'PPB', 'PRE', 'Reserve de cap', 'Fonds propres'}                     
        """
        # computes the inf limit of the provisions
        if(type == 'PPB'):
            # here wealth = Benefits 
           flag = wealth * 0.2
            # for now: PPB_allocation = 85% of profits
           self.allocate(amount=flag, current_step=current_step)
        elif(type == 'PRE'):
            # here wealth = Potential_Gain&Loss[EQ + Cash]
            if(current_step == 1):
                flag = 1/3 * wealth
                self.allocate(amount=flag, current_step=current_step)
                # for now: we initialize the PRE as a third of the value of the (Cash+EQ) Potential Losses 
            else:
                dot = -min(wealth + self.value.loc[current_step-1, 'Value'], 0)
                rep = min(max(wealth- self.value.loc[current_step-1, 'Value'], 0), self.value.loc[current_step-1, 'Value'])
                flag = self.value.loc[current_step-1, 'Value'] + dot - rep
                self.allocate(amount=flag, current_step=current_step)
                # AXA Formula:
                #        Reprise_PRE = Min(Max(PMVL - PRE, 0), PRE)
                #        Dotation_PRE = -Min(PMVL + PRE, 0)
                #        PRE_{t+1} = PRE_{t} + Dotation_PRE - Reprise_PRE
        elif(type == 'Reserve de cap'):
            # here wealth = Potential_Gain&Loss[Bond]
            if(current_step == 1):
                flag = 1/3 * wealth
                self.allocate(amount=flag, current_step=current_step)
                # for now: we initialize the CapRes as a third of the value of the Bond Potential Losses 
            else:
                flag = max(0, self.value.loc[current_step-1, 'Value'] + wealth)
                self.allocate(amount=flag, current_step=current_step)
                # Formula:
                #        RC(t) = Max(0, RC_{t-1} + PMVR[Bond](t))
        elif(type == 'Fonds propres'):
            flag =  wealth
            self.allocate(amount=flag, current_step=current_step)
            # le calcul des FP se fait ici a l'exterieur dans le WStream: en effet, il s'agit uniquement de la soustraction Actifs - Provisions
            # il est donc plus facile de l'effectuer via les WStream directement et d'uniquement l'affecter ici afin de conserver la méthodologie
            # a voir ulterieurement si on la conserve
        return flag
        # we return the allocated amount in order to send the information upwards to the other WStreams
     
    def update(self, current_step, reference=0): # on implemente ici les regles de mise a jour auto
        # on actualise la provision avec les reprises
        """
            Method used to automatically update the Provision over time.
            Returns the amount of money recovered over the time step.
            
            If the Provision is on 'percentage' mode: it automatically recovers a fixed percentage
            of the Provision at each time step.
            If the Provision is on 'frequency' mode: it automatically recovers an amount of the Provision
            at predetermined time steps. (not implemented yet)
            The wealth is the available_wealth at current_step.
        """
        flag = 0      
        if(self.recovery_mode == 'percentage'):
            flag += self.recovery_percentage * self.value.loc[current_step, 'Value']
            self.recover(amount=min(flag, self.value.loc[current_step, 'Value']), current_step=current_step)           
        elif(self.recovery_mode == 'frequency'):
            pass    
        if(reference != 0 and reference*self.limit_sup < self.value.loc[current_step, 'Value']):
            tmp = self.value.loc[current_step, 'Value'] - reference*self.limit_sup
            self.recover(amount=tmp, current_step=current_step)
            flag += tmp      
        return flag
    
    def recover(self, current_step, amount, percentage=0):
        """
            Method used to recover some or all the money in the Provision
        """
        # we use some or all the provision to feed an outer Wealthstream
        flag = percentage * self.value.loc[current_step, 'Value'] + amount
        if(flag <= self.value.loc[current_step, 'Value']):
            if(current_step <= self.time_horizon):
                self.value.loc[np.arange(current_step,self.time_horizon+1), 'Value'] -= flag
        return flag 
    
    def allocate(self, amount, current_step):
        """
            Method used to allocate new funds to the Provision
        """
        self.value.loc[current_step:self.time_horizon, 'Value'] += amount
        # we receive some or all the provision from a Wealthstream
                   
    
#--------------------------------------------------
#       Start of the testing part of the code
#--------------------------------------------------
#
    def main():
        prov1 = Provision(value=0, time_horizon=50, limit_sup=.2)
        
#        prov1.computeProvision(wealth=1000, current_step=1, type='Fonds propres')
        prov2 = Provision(value=800)
        prov2.allocate(amount=300, current_step=10)
        prov2.recover(current_step=20, amount=500)
        prov2.value.plot()

#        # ------------------- TEST A ENLEVER ------------------
        mean = 0
        std = 100
        # ----------------------------------------------------
        
        for i in range(1,prov1.time_horizon+1):
            noise = abs(np.random.normal(mean, std, size=1))
            prov1.computeProvision(current_step=i, wealth=noise, type='Fonds propres')
            prov1.update(current_step=i, reference=800)
            prov2.value.loc[i, 'Value'] = noise
            
        df = prov1.value.plot(title='Analyse de la corrélation entre performance sur les Bonds et CapRes')
        prov2.value.plot(ax=df)
        df.axhline(y=0, c="red", linewidth=1, zorder=0)
        df.axvline(10, color='k', linewidth=.5, linestyle='--')
        df.axvline(20, color='k', linewidth=.5, linestyle='--')
        df.axvline(30, color='k', linewidth=.5, linestyle='--')
        df.axvline(40, color='k', linewidth=.5, linestyle='--')
        df.legend(["FP", "Flux entrant"], loc='center left', bbox_to_anchor=(1.0, 0.5))

        
        
    if __name__ == "__main__":
        main()    
