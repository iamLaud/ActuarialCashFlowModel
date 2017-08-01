# -*- coding: utf-8 -*-
"""
Created on Thu May 18 10:01:38 2017

@author: FR015797
Date of last revision: May 29th 2017
"""


#--------------------------------------------------
#           Project packages
#--------------------------------------------------

#--------------------------------------------------
#           Python packages
#--------------------------------------------------
import pandas as pd
import numpy as np
#--------------------------------------------------
#       Start of the proper code
#--------------------------------------------------

class Liability(object):
    def __init__(self, value=1, time_horizon=50, starting_point=1, lifespan=30, age=40):
        self.name = 'Model point #'+(str(id(self)))
        self.age = age
        self.time_horizon = time_horizon # horizon of the simulation
        self.starting_point = starting_point # start date of the contract
        self.lifespan = lifespan # duration of the contract
        self.contract_age = 0
        
        self.value = pd.DataFrame(data=0, index=np.arange(1,self.time_horizon+1),\
                                  columns=['Contract Value']) 
        self.value.loc[self.starting_point:self.time_horizon, 'Contract Value'] = value
        # Definition of the lapse rate table
        self.buy_back_ratio = pd.DataFrame(data=0, \
           index=np.arange(1,self.lifespan+1), columns=['Lapse rate']) 
        self.buy_back_ratio.iloc[1:4, 0] = .01
        self.buy_back_ratio.iloc[5:9, 0] = .02
        self.buy_back_ratio.iloc[8, 0] = .1
        self.buy_back_ratio.iloc[10:15, 0] = .03
        self.buy_back_ratio.iloc[16:, 0] = .05

        # Definition of the mortality table
        VAL = [0.00384,0.000331272084805654,0.000210879366960224,0.000170747875695546,0.00014063991159777,0.000120565451969738,\
               0.000110531657271476,0.000100494432608433,0.000100504532754427,0.000100514634930846,0.000110577213052132,\
               0.000110589441724391,0.000120656370656371,0.000130726841237279,0.000160915609819875,0.000201176884775939,\
               0.000241460838070325,0.00029183564621469,0.000332185782448511,0.00035243532811729,0.000352559582569454,\
               0.000342607241104808,0.00034272466105539,0.000342842161518992,0.000342959742578452,0.000353167916208389,\
               0.000353292687850769,0.000363515191905728,0.000373748699455539,0.000394098625707356,0.000424581231487753,\
               0.000465215060831926,0.000516021976465351,0.00057702820351886,0.000638136237022031,0.000699357402039286,\
               0.000760703092511639,0.000842485637142451,0.000934626911159649,0.00102701768300743,0.00114004193725698,\
               0.00125343931519413,0.00137745263093453,0.00151217917279712,0.00164749703245876,0.00180396256777672,0.00195097908345056,\
               0.00209883021080898,0.00223727485488644,0.00237662230305034,0.00250657717564684,0.00264786509386941,0.00282147653801705,\
               0.00301739439119631,0.00323597482432532,0.00345660853120403,0.00368999799685823,0.0039153024835716,0.00414316218886446,\
               0.0043950885951718,0.00468236025244029,0.00502734358179391,0.00543143088991074,0.00588536057352349,0.00640169836510473,\
               0.00697159597784068,0.00763053990506189,0.00838213599177433,0.00923066519396795,0.0102039655545065,0.0113320308010574,\
               0.0125895099042128,0.0140097243969343,0.0156296641234135,0.0175153441207152,0.0197041902269192,0.0222790357925493,\
               0.0252727577190112,0.0287428473259241,0.0327636878197453,0.0374887463425613,0.0430410826768777,0.0495586303796695,\
               0.0570918965821992,0.0656441717791411,0.0751805646749836,0.0856703348716128,0.0969328329235149,0.108650998375848,\
               0.12052841716016,0.132598031747966,0.14545646141417,0.15965143045051,0.175308158873019,0.192289442467378,0.210603612865325,\
               0.230046511627907,0.250453062703878,0.272082527401676,0.294729849424269,0.318367346938775,0.343159834177798,0.368863955119215,\
               0.395555555555556,0.422794117647059,0.452229299363057,0.482558139534884,0.50561797752809,0.545454545454545,0.55,\
               0.555555555555556,0.75,1,00000]
        # to be later accessed via csv file reading
        self.mortality_rate = pd.DataFrame(data=VAL, \
           index=np.arange(0,114), columns=['Mortality table']) 
        # Definition of the periodic premium table
        self.premium = pd.DataFrame(data=0.1*value, \
           index=np.arange(1,self.lifespan+1), columns=['Periodic premium']) # we set the periodic premium to 10% of the initial MP
        
    def buyBack(self, current_step, percentage=1, amount=0):
        flag = percentage * self.value.loc[current_step, 'Contract Value'] + amount
        if(flag <= self.value.loc[current_step, 'Contract Value']):
            if(current_step<self.time_horizon):
                self.value.loc[current_step:self.time_horizon, 'Contract Value'] -= flag
        return flag 
     
    def updateValue(self, current_step): # update auto des Model Points
        flagPlus = 0
        flagMinus = 0
        if(current_step > 1):
            self.premium.loc[current_step, 'Periodic premium'] = .1 * self.value.loc[current_step-1, 'Contract Value']
        if(self.value.loc[current_step, 'Contract Value'] > 0 and current_step>self.starting_point):
            # update periodic premium
            self.value.loc[current_step:self.time_horizon, 'Contract Value'] += self.premium.iloc[self.contract_age, 0]
            flagPlus += self.premium.iloc[self.contract_age, 0]
            # update rachats
            basis = self.value.loc[current_step-1, 'Contract Value']
            flagMinus = -self.buyBack(current_step, percentage=0, \
                               amount=min(basis * self.buy_back_ratio.iloc[self.contract_age, 0]\
                               , self.value.loc[current_step-1, 'Contract Value']))
            # update deces
            flagMinus -= self.buyBack(current_step=current_step, percentage=0, \
                         amount=min(basis * self.mortality_rate.iloc[self.age, 0], self.value.loc[current_step-1, 'Contract Value']))  
        return flagPlus, flagMinus 
    
    def update(self, current_step, mode='mid'): # update auto des contrats (Actions de vieillissement + application des regles ALM)
        flag = 0
        if(current_step >= self.starting_point):
            if(current_step<self.time_horizon):
                if(mode == 'end'):
                    # si le contrat existe, il vieillit a chaque periode:
                    if(self.contract_age < self.lifespan):
                        self.contract_age += 1 # age du contrat
                        self.age += 1 # age des assures
                    # Si le contrat expire, on recupere la somme, sinon on la vieillit:
                    if(self.contract_age == self.lifespan):
                        flag = self.buyBack(current_step+1) # here, flag is a float <> 0
                    
            if(mode == 'mid' and self.contract_age<self.lifespan):
                # on met à jour les valeurs des contrats si le contrat est encore existant
                flag = self.updateValue(current_step) # here, flag is a tuple (flag+, flag-)
        return flag
    
    def __str__(self):
        return self.value.__str__()
    
    
#--------------------------------------------------
#       Start of the testing part of the code
#--------------------------------------------------

def main():
    import gc
    gc.enable()
    lia = Liability(value=100, starting_point=10, lifespan=20, age=60)
    for t in range(1, lia.time_horizon+1):
        lia.update(current_step=t, mode='mid')
        lia.update(current_step=t, mode='end')
    df = lia.value['Contract Value'].plot(title='Sensibilité de la valeur du contrat en fonction de l\'âge de l\'assuré', legend=False)
    for age in [20, 30, 40, 50, 60]:
        lia = Liability(value=100, starting_point=10, lifespan=20, age=age)
        for t in range(1, lia.time_horizon+1):
            lia.update(current_step=t, mode='mid')
            lia.update(current_step=t, mode='end')
        lia.value['Contract Value'].plot(title='Sensibilité de la valeur du contrat en fonction de l\'âge de l\'assuré', ax=df, legend=False)
    df.axvline(13, color='black', linewidth=.5, linestyle='--')
    df.axvline(14, color='black', linewidth=.5, linestyle='--')
    df.axvline(17, color='black', linewidth=.5, linestyle='--')
    df.axvline(39, color='black', linewidth=.5, linestyle='--')

#    df.grid(True)

if __name__ == "__main__":
    main()