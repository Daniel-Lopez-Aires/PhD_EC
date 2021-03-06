# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 14:59:32 2022

@author: lopedan

On the clays selection, SKB analysis. Analized:
        -Posiva
        -ALex´s report, containng the comparisons
        
TO begin with will create plots comparing all the basic stuff from Alex´s report
"""

########## General packages

import matplotlib.pyplot as plt  #for simplicity, to not write matplotlib.pyplot
        #everytime we want to plot something
#from scipy.stats import norm               ##norm.fit() fit to gaussian
import numpy as np
    #np contain linspaces as np.linspace(a,b,N)
import pandas as pd
import sys                   #to import functions from other folders!!
sys.path.insert(0, 'C:/Users/lopedan/Cosas_pc/PhD_Alemania-Sevilla_Residuos_nuclearesMariaVillaAlfageme/Python/Functions')   
                                    #path where I have the functions
import Fits



#%% ###################### 1) Data loading #########################

#For the C and S analysis, since several measurements were taken, I compute the meam
#and associate an error as (max-min)/2
    #Note that sometinmes in the content it is say <.02, I guess this is that the apparatus
        #can not measure it. I will write 0.02, althouhgh that means doing a bit mistake!
    #Bulgarian data unkown to assign, all the samples says bulgaria, without specifying, so will
        #assign it randomly, since the important thing is to plot it, is not a big problem. nevertheless,
        #take it intro account!

Milos = {'name' : "Milos", '%Mont' : 43.6, 'Delta_%Mont' : 1, 
         '%Mica' : 5.6, 'Delta_%Mica' : .5, 
         'CEC_total[cmol/kg]' : 55.6, 'Delta_CEC_total[cmol/kg]' : .6,
         'CEC_clay[cmol/kg]' : 95.7, 'Delta_CEC_clay[cmol/kg]' : .2,
         'EC[cmol/kg]' : 61.2 , 'Delta_EC[cmol/kg]': .5 ,
         'perc_C' : (.23 + .24 + .25)/3, 'Delta_perc_C':(.25 - .23)/2, 
         'perc_S' : (.87 + .79 + .73)/3, 'Delta_perc_S':(.87 - .73)/2, 
         'perc_S_S2-' : (.43 + .36 + .29)/3, 'Delta_perc_S_S2-':(.43 - .29)/2, 
         'rho_grain[kg/m3]' :2606, 'Delta_rho_grain[kg/m3]' : 13,
         'rho_min[kg/m3]' : 1440, 'rho_max[kg/m3]': 1530,
         'Geo_H2O' : 17.9, 'Gen_H2O' : 15.1,
         #
         'MnO' : .03, 'Delta_MnO' : .02, 'Fe2O3' : 3.04, 'Delta_Fe2O3' : .21,
         'Na2O' : .36, 'Delta_Na2O' : .04, 'MgO' : 2.56, 'Delta_MgO' : .09,
         'Al2O3' : 18.35, 'Delta_Al2O3' : .46, 'SiO2' : 67.9, 'Delta_SiO2' : 1.01,         
         'P2O5' : .01, 'Delta_P2O5' : .0, 'SO3' : 2.50, 'Delta_SO3' : .22,
         'Cl' : .03, 'Delta_Cl' : .01, 'K2O' : 1.29, 'Delta_K2O' : .15,
         'CaO' : 3.39, 'Delta_CaO' : 1, 'TiO2' : .56, 'Delta_TiO2' : .06,
         }  #All the data from the Milos bentonite. Note this is low content on
            #purpose. Could find higher content. Delta is the standard deviation
            
        #cmol is charge*mass, yes, equivalente en espanol

Morocco = {'name' : "Morocco", '%Mont' : 84.8, 'Delta_%Mont' : 1.48, 
         '%Mica' : 1.7, 'Delta_%Mica' : 2.33, 
         'CEC_total[cmol/kg]' : 80.6, 'Delta_CEC_total[cmol/kg]' : .9,
         'CEC_clay[cmol/kg]' : 104.3, 'Delta_CEC_clay[cmol/kg]' : 0,
         'EC[cmol/kg]' : 82.3 , 'Delta_EC[cmol/kg]': 1.5 ,
         'perc_C' : (.06 + .03 + .03)/3, 'Delta_perc_C':(.06 - .03)/2, 
         'perc_S' : (.03 + .05 + .03)/3, 'Delta_perc_S':(.05 - .03)/2, 
         'perc_S_S2-' : (.02 + .02 + .02)/3, 'Delta_perc_S_S2-':(.02 - .02)/2,
         'rho_grain[kg/m3]' :2737, 'Delta_rho_grain[kg/m3]' : 16,
         'rho_min[kg/m3]' : 1440, 'rho_max[kg/m3]': 1550,
         'Geo_H2O' : 17.7, 'Gen_H2O' : 15,
         #Morocco data
         'MnO' : .01, 'Delta_MnO' : 0, 'Fe2O3' : 2.71, 'Delta_Fe2O3' : .02,
         'Na2O' : 1.42, 'Delta_Na2O' : .03, 'MgO' : 2.07, 'Delta_MgO' : .01,
         'Al2O3' : 28.87, 'Delta_Al2O3' : .07, 'SiO2' : 61.82, 'Delta_SiO2' : .05,         
         'P2O5' : .01, 'Delta_P2O5' : .00, 'SO3' : .07, 'Delta_SO3' : .0,
         'Cl' : .12, 'Delta_Cl' : .00, 'K2O' : 1.08, 'Delta_K2O' : .02,
         'CaO' : 1.53, 'Delta_CaO' : .03, 'TiO2' : .31, 'Delta_TiO2' : .0,
         }  #Moroco bentonite. CEC_clay is marked with a * in the report

Turkish = {'name' : "Turkey", '%Mont' : 72.43, 'Delta_%Mont' : 1.39, 
         '%Mica' : 7.03, 'Delta_%Mica' : 0, 
         'CEC_total[cmol/kg]' : 68.6, 'Delta_CEC_total[cmol/kg]' : .5,
         'CEC_clay[cmol/kg]' : 86, 'Delta_CEC_clay[cmol/kg]' : 1.3,
         'EC[cmol/kg]' : 93.3 , 'Delta_EC[cmol/kg]': .9 ,
         'perc_C' : (.61 + .62 + .64)/3, 'Delta_perc_C':(.64 - .61)/2, 
         'perc_S' : (.02 + .02 + .02)/3, 'Delta_perc_S':(.87 - .73)/2, 
         'perc_S_S2-' : (.02 + .02 + .02)/3, 'Delta_perc_S_S2-':(.02 - .02)/2,
         'rho_grain[kg/m3]' :2605, 'Delta_rho_grain[kg/m3]' : 83,
         'rho_min[kg/m3]' : 1485, 'rho_max[kg/m3]': 1580,
         'Geo_H2O' : 9.3, 'Gen_H2O' : 8.5,
         #Since only 3 results are included, but each one was measured several
         #times, will take that into account by doing number of times*value
         'MnO' : (6*.1 + 3*.09 + 3*.11 + 20*.11)/(6+3+3+20), 'Delta_MnO' : (.11-.09)/2, 
         'Fe2O3' : (6*4.76 + 3*4.53 + 3*4.58 + 20*4.79)/(6+3+3+20), 'Delta_Fe2O3' : (4.79-4.53)/2,
         'Na2O' : (6*2.05 + 3*2.01 + 3*2.21 + 20*+2.14)/(6+3+3+20), 'Delta_Na2O' : (2.21-2.01)/2, 
         'MgO' : (6*1.98 + 3*2.12 + 3*1.89 + 20*2.04)/(6+3+3+20), 'Delta_MgO' : (2.12-1.89)/2,
         'Al2O3' : (6*19.23 + 3*19.52 + 3*19.44 + 20*19.31)/(6+3+3+20), 'Delta_Al2O3' : (19.52-19.23)/2, 
         'SiO2' : (6*66.62 + 3*66.76 + 3*66.3 + 20*66.12)/(6+3+3+20), 'Delta_SiO2' : (66.76-66.12)/2,      
         'P2O5' : (6*.02 + 3*.03 + 3*.04 + 20*.03)/(6+3+3+20), 'Delta_P2O5' : (.04-.02)/2, 
         'SO3' : (6*.06 + 3*.03 + 3*.04 + 20*.04)/(6+3+3+20), 'Delta_SO3' : (.06-.03)/2, 
         'Cl' : (6*.01 + 3*.01 + 3*0 + 20*.01)/(6+3+3+20), 'Delta_Cl' : (.01-0)/2, 
         'K2O' : (6*1.23 + 3*.94 + 3*1.29 + 20*1.35)/(6+3+3+20), 'Delta_K2O' : (1.35-.94)/2, 
         'CaO' : (6*3.52 + 3*3.56 + 3*3.69 + 20*3.64)/(6+3+3+20), 'Delta_CaO' : (3.69-3.52)/2, 
         'TiO2' : (6*.41 + 3*.41 + 3*.42 + 20*.43)/(6+3+3+20), 'Delta_TiO2' : (.43-.41)/2, 
         }  #Turkish bentonite. The 200kg version, not small batches.

Wyoming = {'name' : "Bara-Kade", '%Mont' : 85.3, 'Delta_%Mont' : 1.5, 
         '%Mica' : 4.97, 'Delta_%Mica' : .74, 
         'CEC_total[cmol/kg]' : 84, 'Delta_CEC_total[cmol/kg]' : .6,
         'CEC_clay[cmol/kg]' : 1e10, 'Delta_CEC_clay[cmol/kg]' : 0, #Instead of = in CEC clay I write 1e10!
         'EC[cmol/kg]' : 87.7 , 'Delta_EC[cmol/kg]': .3 ,
         'perc_C' : (.44 + .42 + .42)/3, 'Delta_perc_C':(.44 - .42)/2, 
         'perc_S' : (.21 + .21 + .21)/3, 'Delta_perc_S':(.21 - .21)/2, 
         'perc_S_S2-' : (.03 + .04 + .04)/3, 'Delta_perc_S_S2-':(.04 - .03)/2,
         'rho_grain[kg/m3]' :2769, 'Delta_rho_grain[kg/m3]' : 6,
         'rho_min[kg/m3]' : 1480, 'rho_max[kg/m3]': 1585,
         'Geo_H2O' : 11.4, 'Gen_H2O' : 10.2,
         #
         'MnO' : .04, 'Delta_MnO' : .0, 'Fe2O3' : 5.00, 'Delta_Fe2O3' : .02,
         'Na2O' : 1.71, 'Delta_Na2O' : .03, 'MgO' : 2.49, 'Delta_MgO' : .01,
         'Al2O3' : 21.63, 'Delta_Al2O3' : .02, 'SiO2' : 66.44, 'Delta_SiO2' : .02,         
         'P2O5' : .0, 'Delta_P2O5' : .00, 'SO3' : .37, 'Delta_SO3' : .02,
         'Cl' : .0, 'Delta_Cl' : .00, 'K2O' : .61, 'Delta_K2O' : .0,
         'CaO' : 1.52, 'Delta_CaO' : .06, 'TiO2' : .18, 'Delta_TiO2' : .0,
         }  #Wyoming Bara Kade bentonite (not MX80, but similar). CEC_clay not measured.

Sardinian = {'name' : "Sardinia", '%Mont' : 85.2, 'Delta_%Mont' : .14, 
         '%Mica' : 8, 'Delta_%Mica' : .42, 
         'CEC_total[cmol/kg]' : 108.6, 'Delta_CEC_total[cmol/kg]' : 1.6,
         'CEC_clay[cmol/kg]' : 1e10, 'Delta_CEC_clay[cmol/kg]' : 0,
         'EC[cmol/kg]' : 122.7 , 'Delta_EC[cmol/kg]': 2.1 ,
         'perc_C' : (.18 + .19 + .18)/3, 'Delta_perc_C':(.19 - .18)/2, 
         'perc_S' : (.03 + .03 + .03)/3, 'Delta_perc_S':(.03 - .03)/2, 
         'perc_S_S2-' : (.02 + .02 + .02)/3, 'Delta_perc_S_S2-':(.02 - .02)/2,
         'rho_grain[kg/m3]' :2812, 'Delta_rho_grain[kg/m3]' : 10,
         'rho_min[kg/m3]' : 1430, 'rho_max[kg/m3]': 1510,
         'Geo_H2O' : 19.4, 'Gen_H2O' : 16.3,
         #
         'MnO' : .09, 'Delta_MnO' : .01, 'Fe2O3' : 7.37, 'Delta_Fe2O3' : .03,
         'Na2O' : 1.12, 'Delta_Na2O' : .02, 'MgO' : 5.57, 'Delta_MgO' : .02,
         'Al2O3' : 18.93, 'Delta_Al2O3' : .01, 'SiO2' : 62.66, 'Delta_SiO2' : .03,         
         'P2O5' : .05, 'Delta_P2O5' : .00, 'SO3' : .04, 'Delta_SO3' : .0,
         'Cl' : .05, 'Delta_Cl' : .00, 'K2O' : 1.58, 'Delta_K2O' : .01,
         'CaO' : 1.80, 'Delta_CaO' : .01, 'TiO2' : .75, 'Delta_TiO2' : .0,
         }  #Sardinian bentonite. CEC_clay not measured.

Indian = {'name' : "India", '%Mont' : 77.2, 'Delta_%Mont' : .71, 
         '%Mica' : 0, 'Delta_%Mica' : 0, 
         'CEC_total[cmol/kg]' : 79.8, 'Delta_CEC_total[cmol/kg]' : .05,
         'CEC_clay[cmol/kg]' : 89.4, 'Delta_CEC_clay[cmol/kg]' : .05,
         'EC[cmol/kg]' : 92.1 , 'Delta_EC[cmol/kg]': 5.1 ,
         'perc_C' : (.14 + .14 + .15)/3, 'Delta_perc_C':(.15 - .14)/2, 
         'perc_S' : (.14 + .15 + .15)/3, 'Delta_perc_S':(.15 - .14)/2, 
         'perc_S_S2-' : (.02 + .02 + .02)/3, 'Delta_perc_S_S2-':(.02 - .02)/2,
         'rho_grain[kg/m3]' :2931, 'Delta_rho_grain[kg/m3]' : 19,
         'rho_min[kg/m3]' : 1420, 'rho_max[kg/m3]': 1540,
         'Geo_H2O' : 14.4, 'Gen_H2O' : 12.6,
         #
         'MnO' : .11, 'Delta_MnO' : .01, 'Fe2O3' : 21.13, 'Delta_Fe2O3' : .10,
         'Na2O' : 1.58, 'Delta_Na2O' : .02, 'MgO' : 1.89, 'Delta_MgO' : .03,
         'Al2O3' : 21.17, 'Delta_Al2O3' : .06, 'SiO2' : 48.55, 'Delta_SiO2' : .11,         
         'P2O5' : .02, 'Delta_P2O5' : .00, 'SO3' : .63, 'Delta_SO3' : .02,
         'Cl' : .68, 'Delta_Cl' : .05, 'K2O' : .13, 'Delta_K2O' : .0,
         'CaO' : 1.26, 'Delta_CaO' : .03, 'TiO2' : 2.40, 'Delta_TiO2' : .03,
         }  #Indian bentonite. CEC_clay not measured.

Bulgarian_1 = {'name' : "Bulgaria$_{20kg}$", '%Mont' : 73.8, 'Delta_%Mont' : 1.7, 
         '%Mica' : 8.2, 'Delta_%Mica' : .2, 
         'CEC_total[cmol/kg]' : 73.1, 'Delta_CEC_total[cmol/kg]' : 1.1,
         'CEC_clay[cmol/kg]' : 85.3, 'Delta_CEC_clay[cmol/kg]' : 0,
         'EC[cmol/kg]' : 81.8 , 'Delta_EC[cmol/kg]': .3 ,
         'perc_C' : (.82 + .78 + .89)/3, 'Delta_perc_C':(.89 - .78)/2, 
         'perc_S' : (.05 + .05 + .06)/3, 'Delta_perc_S':(.06 - .05)/2, 
         'perc_S_S2-' : (.02 + .02 + .02)/3, 'Delta_perc_S_S2-':(.02 - .02)/2,
         'rho_grain[kg/m3]' :2757, 'Delta_rho_grain[kg/m3]' : 7,
         'rho_min[kg/m3]' : 1280, 'rho_max[kg/m3]': 1400,
         'Geo_H2O' : 20.1, 'Gen_H2O' : 16.7,
         #
         'MnO' : .061, 'Delta_MnO' : 0, 'Fe2O3' : 6.301, 'Delta_Fe2O3' : .0,
         'Na2O' : .481, 'Delta_Na2O' : .0, 'MgO' : 3.581, 'Delta_MgO' : .0,
         'Al2O3' : 16.974, 'Delta_Al2O3' : .0, 'SiO2' : 64.877, 'Delta_SiO2' : .0,         
         'P2O5' : .182, 'Delta_P2O5' : .00, 'SO3' : .038, 'Delta_SO3' : .0,
         'Cl' : .005, 'Delta_Cl' : .00, 'K2O' : 1.838, 'Delta_K2O' : .0,
         'CaO' : 4.548, 'Delta_CaO' : .0, 'TiO2' : 1.113, 'Delta_TiO2' : .0,
         }  #Bulgarian bentonite, 20kg (2017). 

Bulgarian_2 = {'name' : "Bulgaria$_{20ton}$", '%Mont' : 82.6, 'Delta_%Mont' : .5, 
         '%Mica' : 6.3, 'Delta_%Mica' : .3, 
         'CEC_total[cmol/kg]' : 79.4, 'Delta_CEC_total[cmol/kg]' : .4,
         'CEC_clay[cmol/kg]' : 1e10, 'Delta_CEC_clay[cmol/kg]' : 0,
         'EC[cmol/kg]' : 0 , 'Delta_EC[cmol/kg]': 0 ,
         'perc_C' : (.58 + .86 + .59)/3, 'Delta_perc_C':(.86 - .58)/2, 
         'perc_S' : (.03 + .04 + .03)/3, 'Delta_perc_S':(.04 - .03)/2, 
         'perc_S_S2-' : (.02 + .02 + .02)/3, 'Delta_perc_S_S2-':(.02 - .02)/2,
         'rho_grain[kg/m3]' :2770, 'Delta_rho_grain[kg/m3]' : 6,
         'rho_min[kg/m3]' : 0, 'rho_max[kg/m3]': 0,
         'Geo_H2O' : 19.6, 'Gen_H2O' : 16.4,
         #
         'MnO' : (.068+.067+.067)/3, 'Delta_MnO' : (.068-.067)/2, 
         'Fe2O3' : (6.775+6.655+6.679)/3, 'Delta_Fe2O3' : (6.79-6.655)/2,
         'Na2O' : (.557+.567+.562)/3, 'Delta_Na2O' : (.567-.557)/2, 
         'MgO' : (3.494+3.479+3.484)/3, 'Delta_MgO' : (3.494-3.484)/2,
         'Al2O3' : (16.946+16.937+16.895)/3, 'Delta_Al2O3' : (16.946-16.895)/2, 
         'SiO2' : (64.561+64.699+64.653)/3, 'Delta_SiO2' : (64.699-64.561)/2,      
         'P2O5' : (.156+.169+.171)/3, 'Delta_P2O5' : (.171-.156)/2, 
         'SO3' : (.041+.054+.042)/3, 'Delta_SO3' : (.054-.041)/2, 
         'Cl' : (.002+.003+.002)/3, 'Delta_Cl' : (.003-.002)/2, 
         'K2O' : (1.593+1.574+1.575)/3, 'Delta_K2O' : (1.593-1.574)/2, 
         'CaO' : (4.621+4.626+4.698)/3, 'Delta_CaO' : (4.698-4.621)/2, 
         'TiO2' : (1.188+1.171+1.174)/3, 'Delta_TiO2' : (1.188-1.171)/2, 
         }  #Bulgarian bentonite, 20 ton (2018).Data from grain infered from typing error
            #on report

Bulgarian_3 = {'name' : "Bulgaria$_F$", '%Mont' : 79.2, 'Delta_%Mont' : 1.7, 
         '%Mica' : 5.3, 'Delta_%Mica' : .2, 
         'CEC_total[cmol/kg]' : 76.2, 'Delta_CEC_total[cmol/kg]' : .6,
         'CEC_clay[cmol/kg]' : 89.9, 'Delta_CEC_clay[cmol/kg]' : 0,
         'EC[cmol/kg]' : 83.5 , 'Delta_EC[cmol/kg]': .2 ,
         'perc_C' : (.74 + .72 + .73)/3, 'Delta_perc_C':(.74 - .72)/2, 
         'perc_S' : (.05 + .04 + .05)/3, 'Delta_perc_S':(.05 - .04)/2, 
         'perc_S_S2-' : (.02 + .02 + .02)/3, 'Delta_perc_S_S2-':(.02 - .02)/2,
         'rho_grain[kg/m3]' :2758, 'Delta_rho_grain[kg/m3]' : 5,
         'rho_min[kg/m3]' : 1315, 'rho_max[kg/m3]': 1425,
         'Geo_H2O' : 18.8, 'Gen_H2O' : 15.9,
                    #
         'MnO' : .083, 'Delta_MnO' : 0, 'Fe2O3' : 6.344, 'Delta_Fe2O3' : .0,
         'Na2O' : .651, 'Delta_Na2O' : .0, 'MgO' : 3.629, 'Delta_MgO' : .0,
         'Al2O3' : 17.189, 'Delta_Al2O3' : .0, 'SiO2' : 64.222, 'Delta_SiO2' : .0,         
         'P2O5' : .176, 'Delta_P2O5' : .00, 'SO3' : .064, 'Delta_SO3' : .0,
         'Cl' : .003, 'Delta_Cl' : .00, 'K2O' : 1.502, 'Delta_K2O' : .0,
         'CaO' : 5.016, 'Delta_CaO' : .0, 'TiO2' : 1.123, 'Delta_TiO2' : .0,
         }

#0 means not measured!!! 


#%% ############################# 2) Data obtaining ###########################
#Now lets obtain the data in arrays for simpler managemente (the dicitonary is for easier error seeking). Creating a list
#with the dictionaries makes everything easier.

#Note that for extracting the XRF data, 24 variables needed for value and errors!

Bentonites = np.array( [Milos, Morocco, Indian, Sardinian, Turkish, Wyoming, Bulgarian_1, Bulgarian_2, Bulgarian_3] )
        #Gathering of all the bentonites
        
names = np.array([])
CEC_total = np.array([])                        #storing of the CEC_toal [cmol/kg]
Delta_CEC_total = np.array([])          #storing of the error of CEC_toal [cmol/kg]
CEC_clay = np.array([])                        #storing of the CEC_toal [cmol/kg]
Delta_CEC_clay = np.array([])        #storing of the error of CEC_toal [cmol/kg]
EC = np.array([])                        #storing of the EC [cmol/kg]
Delta_EC = np.array([])                 #storing of the error of EC [cmol/kg]
mineral_wt = np.array([])                   #content of that mineral
Delta_mineral_wt = np.array([])             #error of the mineral content
perc_C = np.array([])                               #%C
perc_S = np.array([])                               #%S
perc_S_S2 = np.array([])                            #%S/S2-
Delta_perc_C = np.array([])                         #error of %C
Delta_perc_S = np.array([])                         #error of %S
Delta_perc_S_S2 = np.array([])                      #error of %S/S2-
#XRF data:
MnO = np.array([])
Delta_MnO = np.array([])
Fe2O3 = np.array([])
Delta_Fe2O3 = np.array([])
Na2O = np.array([])
Delta_Na2O = np.array([])
MgO = np.array([])
Delta_Na2O = np.array([])
MgO = np.array([])
Delta_MgO = np.array([])
Al2O3 = np.array([])
Delta_Al2O3 = np.array([])
SiO2 = np.array([])
Delta_SiO2 = np.array([])
P2O5 = np.array([])
Delta_P2O5 = np.array([])
SO3 = np.array([])
Delta_SO3 = np.array([])
Cl = np.array([])
Delta_Cl = np.array([])
K2O = np.array([])
Delta_K2O = np.array([])
CaO = np.array([])
Delta_CaO = np.array([])
TiO2 = np.array([])
Delta_TiO2 = np.array([])
#
rho_grain = np.array([])            #grain density [kg/m3]
Delta_rho_grain = np.array([])#error of the grain density
rho_min = np.array([])              #Lower limit of rho [kg/m3]
rho_max = np.array([])              #Upper limit of rho [kg/m3]
Geo_H2O = np.array([])          #Water content, geological data (water/dry mass)
Gen_H2O = np.array([])          #Water content, general data (water/total mass)
#
Mont_CEC = np.array([])     #Mont content stimation from CEC total/CEC clay
Delta_Mont_CEC = np.array([])

for i in range(0, len(Bentonites)):
    names = np.append(names, Bentonites[i]['name'])
    CEC_total = np.append(CEC_total, Bentonites[i]['CEC_total[cmol/kg]'])
    Delta_CEC_total = np.append(Delta_CEC_total, Bentonites[i]['Delta_CEC_total[cmol/kg]'])
    CEC_clay = np.append(CEC_clay, Bentonites[i]['CEC_clay[cmol/kg]'])
    Delta_CEC_clay = np.append(Delta_CEC_clay, Bentonites[i]['Delta_CEC_clay[cmol/kg]'])
    EC = np.append(EC, Bentonites[i]['EC[cmol/kg]'])
    Delta_EC = np.append(Delta_EC, Bentonites[i]['Delta_EC[cmol/kg]'])
    #
    perc_C = np.append(perc_C, Bentonites[i]['perc_C'])
    perc_S = np.append(perc_S, Bentonites[i]['perc_S'])
    perc_S_S2 = np.append(perc_S_S2, Bentonites[i]['perc_S_S2-'])
    Delta_perc_C = np.append(Delta_perc_C, Bentonites[i]['Delta_perc_C'])
    Delta_perc_S = np.append(Delta_perc_S, Bentonites[i]['Delta_perc_S'])
    Delta_perc_S_S2 = np.append(Delta_perc_S_S2, Bentonites[i]['Delta_perc_S_S2-'])
    #
    rho_grain = np.append(rho_grain, Bentonites[i]['rho_grain[kg/m3]'])
    Delta_rho_grain = np.append(Delta_rho_grain, Bentonites[i]['Delta_rho_grain[kg/m3]'])
    rho_min = np.append(rho_min, Bentonites[i]['rho_min[kg/m3]'])
    rho_max = np.append(rho_max, Bentonites[i]['rho_max[kg/m3]'])
    Gen_H2O = np.append(Gen_H2O, Bentonites[i]['Gen_H2O'])
    Geo_H2O = np.append(Geo_H2O, Bentonites[i]['Geo_H2O'])
    #
    mineral_wt = np.append(mineral_wt,Bentonites[i]['%Mont'] )
    Delta_mineral_wt = np.append(Delta_mineral_wt, Bentonites[i]['Delta_%Mont'])     
    #
    MnO = np.append(MnO, Bentonites[i]['MnO'])
    Delta_MnO = np.append(Delta_MnO, Bentonites[i]['Delta_MnO'])
    Fe2O3 = np.append(Fe2O3, Bentonites[i]['Fe2O3'])
    Delta_Fe2O3 = np.append(Delta_Fe2O3, Bentonites[i]['Delta_Fe2O3'])
    Na2O = np.append(Na2O, Bentonites[i]['Na2O'])
    Delta_Na2O = np.append(Delta_Na2O, Bentonites[i]['Delta_Na2O'])
    MgO = np.append(MgO, Bentonites[i]['MgO'])
    Delta_MgO = np.append(Delta_MgO, Bentonites[i]['Delta_MgO'])
    Al2O3 = np.append(Al2O3, Bentonites[i]['Al2O3'])
    Delta_Al2O3 = np.append(Delta_Al2O3, Bentonites[i]['Delta_Al2O3'])
    SiO2 = np.append(SiO2, Bentonites[i]['SiO2'])
    Delta_SiO2 = np.append(Delta_SiO2, Bentonites[i]['Delta_SiO2'])
    P2O5 = np.append(P2O5, Bentonites[i]['P2O5'])
    Delta_P2O5 = np.append(Delta_P2O5, Bentonites[i]['Delta_P2O5'])
    SO3 = np.append(SO3, Bentonites[i]['SO3'])
    Delta_SO3 = np.append(Delta_SO3, Bentonites[i]['Delta_SO3'])
    Cl = np.append(Cl, Bentonites[i]['Cl'])
    Delta_Cl = np.append(Delta_Cl, Bentonites[i]['Delta_Cl'])
    K2O = np.append(K2O, Bentonites[i]['K2O'])
    Delta_K2O = np.append(Delta_K2O, Bentonites[i]['Delta_K2O'])
    CaO = np.append(CaO, Bentonites[i]['CaO'])
    Delta_CaO = np.append(Delta_CaO, Bentonites[i]['Delta_CaO'])
    TiO2 = np.append(TiO2, Bentonites[i]['TiO2'])
    Delta_TiO2 = np.append(Delta_TiO2, Bentonites[i]['Delta_TiO2'])
    #
    Mont_CEC = np.append(Mont_CEC,  
                         Bentonites[i]['CEC_total[cmol/kg]'] / Bentonites[i]['CEC_clay[cmol/kg]'])
    Delta_Mont_CEC = np.append(Delta_Mont_CEC, 
                               Bentonites[i]['CEC_total[cmol/kg]'] / Bentonites[i]['CEC_clay[cmol/kg]'] * np.sqrt(
                             (Bentonites[i]['Delta_CEC_total[cmol/kg]'] / Bentonites[i]['CEC_total[cmol/kg]'])**2 + 
                             (Bentonites[i]['Delta_CEC_clay[cmol/kg]'] /Bentonites[i]['CEC_clay[cmol/kg]'])**2) 
                                )    
    
#%% ################################ 3) Data plotting #######################


####################### Chemical properties ##########


###CEC total
plt.figure(figsize=(10,8))  #width, heigh 6.4*4.8 inches by default
plt.title("Cation Exchange Capacity (CEC)", fontsize=22, wrap=True)           #title
plt.bar(names, CEC_total, yerr = Delta_CEC_total, edgecolor="black") 
plt.ylabel("$CEC_{total}$ [cmol/kg]", fontsize=14)              #ylabel
plt.xlabel('Bentonite', fontsize = 14)
plt.tick_params(axis='both', labelsize=14)              #size of axis
plt.grid(True)
plt.xticks(rotation=30) #rotation = 'vertical', 40 for 40 degress
plt.savefig('CEC_total_vs_bentonite.png', format='png')

###CEC clay
plt.figure(figsize=(10,8))  #width, heigh 6.4*4.8 inches by default
plt.title("CEC of the clay mineral", fontsize=22, wrap=True)           #title
plt.bar(names, CEC_clay, yerr = Delta_CEC_clay, edgecolor="black") 
plt.ylabel("$CEC_{clay}$ [cmol/kg]", fontsize=14)              #ylabel
plt.xlabel('Bentonite', fontsize = 14)
plt.tick_params(axis='both', labelsize=14)              #size of axis
plt.grid(True)
plt.xticks(rotation=30) #rotation = 'vertical', 40 for 40 degress
plt.savefig('CEC_clay_vs_bentonite.png', format='png')

###EC
plt.figure(figsize=(10,8))  #width, heigh 6.4*4.8 inches by default
plt.title("Exchange cation sum", fontsize=22, wrap=True)           #title
plt.bar(names, EC, yerr = Delta_EC, edgecolor="black") 
plt.ylabel("EC [cmol/kg]", fontsize=14)              #ylabel
plt.xlabel('Bentonite', fontsize = 14)
plt.tick_params(axis='both', labelsize=14)              #size of axis
plt.grid(True)
plt.xticks(rotation=30) #rotation = 'vertical', 40 for 40 degress
plt.savefig('EC_vs_bentonite.png', format='png')


### %mineral

plt.figure(figsize=(10,8))  #width, heigh 6.4*4.8 inches by default
plt.title("% Montmorillonite", fontsize=22, wrap=True)           #title
plt.bar(names, mineral_wt, yerr = Delta_mineral_wt, edgecolor="black") 
plt.ylabel("% Montmorillonite [%]", fontsize=14)              #ylabel
plt.xlabel('Bentonite', fontsize = 14)
plt.tick_params(axis='both', labelsize=14)              #size of axis
plt.grid(True)
plt.xticks(rotation=30) #rotation = 'vertical', 40 for 40 degress
plt.savefig('Mont_content_vs_bentonite.png', format='png')

### %mineral stimation from CEC
#This gives higher values from the other stimation (XRD

plt.figure(figsize=(10,8))  #width, heigh 6.4*4.8 inches by default
plt.title("% Montmorillonite from CEC total/CEC clay", fontsize=22, wrap=True)           #title
plt.bar(names, Mont_CEC*100, yerr = Delta_Mont_CEC, edgecolor="black") 
plt.ylabel("% Montmorillonite [%]", fontsize=14)              #ylabel
plt.xlabel('Bentonite', fontsize = 14)
plt.tick_params(axis='both', labelsize=14)              #size of axis
plt.grid(True)
plt.xticks(rotation=30) #rotation = 'vertical', 40 for 40 degress
plt.savefig('Mont_content_vs_bentonite_CEC.png', format='png')

### C and S content

X_axis = np.arange(len(names))                 #To do the 2 bar plot
w = .3          #bar width

plt.figure(figsize=(10,8))  #width, heigh 6.4*4.8 inches by default
plt.title("Organic C and S content", fontsize=22, wrap=True)           #title
plt.bar(X_axis - w, perc_C, yerr = Delta_perc_C, width = 1*w, edgecolor="black", label = '%C', align='center') 
plt.bar(X_axis , perc_S, yerr = Delta_perc_S, width = 1*w, edgecolor="black", label = '%S', align='center') 
plt.bar(X_axis + w, perc_S_S2, yerr = Delta_perc_S_S2,  width = 1*w, edgecolor="black", label = '%S/S$^{2-}$', align='center') 
plt.ylabel("Impurity content", fontsize=14)              #ylabel
plt.xlabel('Bentonite', fontsize = 14)
plt.tick_params(axis='both', labelsize=14)              #size of axis
plt.grid(True)
plt.legend()
plt.xticks(X_axis, names, rotation=30) #rotation = 'vertical', 40 for 40 degress
plt.savefig('C_S_content_vs_bentonite.png', format='png')


###XRF data
#So, 12 values, with their 12 errors. Could try a massive bar plot? Could. If not, single plots and
#thats it.

X_axis = np.arange(len(names))                 #To do the 2 bar plot
w = .5/6          #bar width

plt.figure(figsize=(16,12))  #width, heigh 6.4*4.8 inches by default
plt.title("XRF", fontsize=22, wrap=True)           #title
plt.bar(X_axis - w, MnO, yerr = Delta_MnO, width = .5/6, edgecolor="black", label = '%MnO', align='center') 
plt.bar(X_axis - 2*w , Fe2O3, yerr = Delta_Fe2O3, width = 1/12, edgecolor="black", label = '%Fe_2O_3', align='center') 
plt.bar(X_axis - 3*w, Na2O, yerr = Delta_Na2O,  width = 1/12, edgecolor="black", label = '%Na_2O', align='center') 
plt.bar(X_axis - 4*w, MgO, yerr = Delta_MnO, width = 1/12, edgecolor="black", label = '%MgO', align='center') 
plt.bar(X_axis - 5*w, Al2O3, yerr = Delta_Al2O3, width = 1/12, edgecolor="black", label = '%Al2O3', align='center') 
plt.bar(X_axis - 6*w, SiO2, yerr = Delta_SiO2, width = 1/12, edgecolor="black", label = '%SiO2', align='center') 
#Central position
plt.bar(X_axis + w, P2O5, yerr = Delta_P2O5, width = 1/12, edgecolor="black", label = '%P2O5', align='center') 
plt.bar(X_axis + 2*w, SO3, yerr = Delta_SO3, width = 1/12, edgecolor="black", label = '%SO3', align='center') 
plt.bar(X_axis + 3*w, Cl, yerr = Delta_Cl, width = 1/12, edgecolor="black", label = '%Cl', align='center') 
plt.bar(X_axis + 4*w, K2O, yerr = Delta_K2O, width = 1/12, edgecolor="black", label = '%K2O', align='center') 
plt.bar(X_axis + 5*w, CaO, yerr = Delta_CaO, width = 1/12, edgecolor="black", label = '%CaO', align='center') 
plt.bar(X_axis + 6*w, TiO2, yerr = Delta_TiO2, width = 1/12, edgecolor="black", label = '%TiO', align='center') 
plt.ylabel("%", fontsize=14)              #ylabel
plt.xlabel('Bentonite', fontsize = 14)
plt.tick_params(axis='both', labelsize=14)              #size of axis
plt.grid(True)
plt.legend()
plt.xticks(X_axis, names, rotation=30) #rotation = 'vertical', 40 for 40 degress
plt.savefig('XRF.png', format='png')
#No, this plot (which is not completely well done), its pointless, which that amount of bars its pointless to do it, to
#difficult to read it. Will do a table instead

################ Physical properties ###########


### rho limits

X_axis = np.arange(len(names))                 #To do the 2 bar plot
w = .2          #bar width

plt.figure(figsize=(10,8))  #width, heigh 6.4*4.8 inches by default
plt.title("Density limits to satisfy $P_{swell}$ limits", fontsize=22, wrap=True)           #title
plt.bar(X_axis - w, rho_min, width = 2*w, edgecolor="black", label = 'Min', align='center') 
plt.bar(X_axis + w, rho_max, width = 2*w, edgecolor="black", label = 'Max', align='center') 
plt.ylabel(r"$\rho_{grain}$ [kg/m3]", fontsize=14)              #ylabel
plt.xlabel('Bentonite', fontsize = 14)
plt.tick_params(axis='both', labelsize=14)              #size of axis
plt.grid(True)
plt.legend()
plt.xticks(X_axis, names, rotation=30) #rotation = 'vertical', 40 for 40 degress
plt.savefig('rho_limits_vs_bentonite.png', format='png')


### rho_grain
plt.figure(figsize=(10,8))  #width, heigh 6.4*4.8 inches by default
plt.title("Grain density", fontsize=22, wrap=True)           #title
plt.bar(names, rho_grain, yerr = Delta_rho_grain, edgecolor="black") 
plt.ylabel(r"$\rho_{grain}$ [kg/m3]", fontsize=14)              #ylabel
plt.xlabel('Bentonite', fontsize = 14)
plt.tick_params(axis='both', labelsize=14)              #size of axis
plt.grid(True)
plt.xticks(rotation=30) #rotation = 'vertical', 40 for 40 degress
plt.savefig('grain_density_vs_bentonite.png', format='png')

plt.figure(figsize=(10,8))  #width, heigh 6.4*4.8 inches by default
plt.title("Water content, geological (water/dry mass)", fontsize=22, wrap=True)           #title
plt.bar(names, Geo_H2O, edgecolor="black") 
plt.ylabel('H$_2$O [%]', fontsize=14)              #ylabel
plt.xlabel('Bentonite', fontsize = 14)
plt.tick_params(axis='both', labelsize=14)              #size of axis
plt.grid(True)
plt.xticks(rotation=30) #rotation = 'vertical', 40 for 40 degress
plt.savefig('H2O_geo_vs_bentonite.png', format='png')

plt.figure(figsize=(10,8))  #width, heigh 6.4*4.8 inches by default
plt.title("Water content, general (water/total mass)", fontsize=22, wrap=True)           #title
plt.bar(names, Gen_H2O, edgecolor="black") 
plt.ylabel('H$_2$O [%]', fontsize=14)              #ylabel
plt.xlabel('Bentonite', fontsize = 14)
plt.tick_params(axis='both', labelsize=14)              #size of axis
plt.grid(True)
plt.xticks(rotation=30) #rotation = 'vertical', 40 for 40 degress
plt.savefig('H2O_gen_vs_bentonite.png', format='png')



#%% ############### 4) Discussion ############################

'''

'''