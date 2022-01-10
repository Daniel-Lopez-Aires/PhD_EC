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


Milos = {'name' : "Milos", '%Mont' : 43.6, 'Delta_%Mont' : 1, 
         '%Mica' : 5.6, 'Delta_%Mica' : .5, 
         'CEC_total[cmol/kg]' : 55.6, 'Delta_CEC_total[cmol/kg]' : .6,
         'CEC_clay[cmol/kg]' : 95.7, 'Delta_CEC_clay[cmol/kg]' : .2,
         'rho_grain[kg/m3]' :2606, 'Delta_rho_grain[kg/m3]' : 13,
         'Geo_H2O' : 17.9, 'Gen_H2O' : 15.1,
         }  #All the data from the Milos bentonite. Note this is low content on
            #purpose. Could find higher content. Delta is the standard deviation
            
        #cmol is charge*mass, yes, equivalente en espanol

Morocco = {'name' : "Morocco", '%Mont' : 84.8, 'Delta_%Mont' : 1.48, 
         '%Mica' : 1.7, 'Delta_%Mica' : 2.33, 
         'CEC_total[cmol/kg]' : 80.6, 'Delta_CEC_total[cmol/kg]' : .9,
         'CEC_clay[cmol/kg]' : 104.3, 'Delta_CEC_clay[cmol/kg]' : 0,
         'rho_grain[kg/m3]' :2737, 'Delta_rho_grain[kg/m3]' : 16,
         'Geo_H2O' : 17.7, 'Gen_H2O' : 15,
         }  #Moroco bentonite. CEC_clay is marked with a * in the report

Turkish = {'name' : "Turkish", '%Mont' : 72.43, 'Delta_%Mont' : 1.39, 
         '%Mica' : 7.03, 'Delta_%Mica' : 0, 
         'CEC_total[cmol/kg]' : 68.6, 'Delta_CEC_total[cmol/kg]' : .5,
         'CEC_clay[cmol/kg]' : 86, 'Delta_CEC_clay[cmol/kg]' : 1.3,
         'rho_grain[kg/m3]' :2605, 'Delta_rho_grain[kg/m3]' : 83,
         'Geo_H2O' : 9.3, 'Gen_H2O' : 8.5,
         }  #Turkish bentonite. The 200kg version, not small batches.

Wyoming = {'name' : "MX-80", '%Mont' : 85.3, 'Delta_%Mont' : 1.5, 
         '%Mica' : 4.97, 'Delta_%Mica' : .74, 
         'CEC_total[cmol/kg]' : 84, 'Delta_CEC_total[cmol/kg]' : .6,
         'CEC_clay[cmol/kg]' : 0, 'Delta_CEC_clay[cmol/kg]' : 0,
         'rho_grain[kg/m3]' :2769, 'Delta_rho_grain[kg/m3]' : 6,
         'Geo_H2O' : 11.4, 'Gen_H2O' : 10.2,
         }  #Wyoming MX-80 bentonite. CEC_clay not measured.

Sardinian = {'name' : "Sardinian", '%Mont' : 85.2, 'Delta_%Mont' : .14, 
         '%Mica' : 8, 'Delta_%Mica' : .42, 
         'CEC_total[cmol/kg]' : 108.6, 'Delta_CEC_total[cmol/kg]' : 1.6,
         'CEC_clay[cmol/kg]' : 0, 'Delta_CEC_clay[cmol/kg]' : 0,
         'rho_grain[kg/m3]' :2812, 'Delta_rho_grain[kg/m3]' : 10,
         'Geo_H2O' : 19.4, 'Gen_H2O' : 16.3,
         }  #Sardinian bentonite. CEC_clay not measured.

Indian = {'name' : "Indian", '%Mont' : 77.2, 'Delta_%Mont' : .71, 
         '%Mica' : 0, 'Delta_%Mica' : 0, 
         'CEC_total[cmol/kg]' : 79.8, 'Delta_CEC_total[cmol/kg]' : .05,
         'CEC_clay[cmol/kg]' : 89.4, 'Delta_CEC_clay[cmol/kg]' : .05,
         'rho_grain[kg/m3]' :2931, 'Delta_rho_grain[kg/m3]' : 19,
         'Geo_H2O' : 14.4, 'Gen_H2O' : 12.6,
         }  #Indian bentonite. CEC_clay not measured.

Bulgarian_1 = {'name' : "Bulgarian$_{20kg}$", '%Mont' : 73.8, 'Delta_%Mont' : 1.7, 
         '%Mica' : 8.2, 'Delta_%Mica' : .2, 
         'CEC_total[cmol/kg]' : 73.1, 'Delta_CEC_total[cmol/kg]' : 1.1,
         'CEC_clay[cmol/kg]' : 85.3, 'Delta_CEC_clay[cmol/kg]' : 0,
         'rho_grain[kg/m3]' :2757, 'Delta_rho_grain[kg/m3]' : 7,
          'Geo_H2O' : 20.1, 'Gen_H2O' : 16.7,
          }  #Bulgarian bentonite, 20kg (2017). 

Bulgarian_2 = {'name' : "Bulgarian$_{20ton}$", '%Mont' : 82.6, 'Delta_%Mont' : .5, 
         '%Mica' : 6.3, 'Delta_%Mica' : .3, 
         'CEC_total[cmol/kg]' : 79.4, 'Delta_CEC_total[cmol/kg]' : .4,
         'CEC_clay[cmol/kg]' : 0, 'Delta_CEC_clay[cmol/kg]' : 0,
         'rho_grain[kg/m3]' :2770, 'Delta_rho_grain[kg/m3]' : 6,
         'Geo_H2O' : 19.6, 'Gen_H2O' : 16.4,
         }  #Bulgarian bentonite, 20 ton (2018).Data from grain infered from typing error
            #on report

Bulgarian_3 = {'name' : "Bulgarian$_F$", '%Mont' : 79.2, 'Delta_%Mont' : 1.7, 
         '%Mica' : 5.3, 'Delta_%Mica' : .2, 
         'CEC_total[cmol/kg]' : 76.2, 'Delta_CEC_total[cmol/kg]' : .6,
         'CEC_clay[cmol/kg]' : 89.9, 'Delta_CEC_clay[cmol/kg]' : 0,
         'rho_grain[kg/m3]' :2758, 'Delta_rho_grain[kg/m3]' : 5,
           'Geo_H2O' : 18.8, 'Gen_H2O' : 15.9,
           }  #Bulgarian bentonite, F. 


#0 means not measured!!! 


#%% ############################# 2) Data obtaining ###########################
#Now lets obtain the data in arrays for simpler managemente (the dicitonary is for easier error seeking). Creating a list
#with the dictionaries makes everything easier.

Bentonites = np.array( [Milos, Morocco, Indian, Sardinian, Turkish, Wyoming, Bulgarian_1, Bulgarian_2, Bulgarian_3] )
        #Gathering of all the bentonites
        
names = np.array([])
CEC_total = np.array([])                        #storing of the CEC_toal [cmol/kg]
Delta_CEC_total = np.array([])      #storing of the error of CEC_toal [cmol/kg]
CEC_clay = np.array([])                        #storing of the CEC_toal [cmol/kg]
Delta_CEC_clay = np.array([])      #storing of the error of CEC_toal [cmol/kg]
mineral_type = np.array([])         #type of mineral, smectite or montmorillonite'
mineral_wt = np.array([])           #content of that mineral
Delta_mineral_wt = np.array([])           #error of the mineral content
rho_grain = np.array([])            #grain density [kg/m3]
Delta_rho_grain = np.array([])#error of the grain density
Geo_H2O = np.array([])          #Water content, geological data (water/dry mass)
Gen_H2O = np.array([])          #Water content, general data (water/total mass)


for i in range(0, len(Bentonites)):
    names = np.append(names, Bentonites[i]['name'])
    CEC_total = np.append(CEC_total, Bentonites[i]['CEC_total[cmol/kg]'])
    Delta_CEC_total = np.append(Delta_CEC_total, Bentonites[i]['Delta_CEC_total[cmol/kg]'])
    CEC_clay = np.append(CEC_clay, Bentonites[i]['CEC_clay[cmol/kg]'])
    Delta_CEC_clay = np.append(Delta_CEC_clay, Bentonites[i]['Delta_CEC_clay[cmol/kg]'])
    rho_grain = np.append(rho_grain, Bentonites[i]['rho_grain[kg/m3]'])
    Delta_rho_grain = np.append(Delta_rho_grain, Bentonites[i]['Delta_rho_grain[kg/m3]'])
    Gen_H2O = np.append(Gen_H2O, Bentonites[i]['Gen_H2O'])
    Geo_H2O = np.append(Geo_H2O, Bentonites[i]['Geo_H2O'])
    
    try: #If the mineral is montorillonite
        mineral_wt = np.append(mineral_wt,Bentonites[i]['%Mont'] )
        Delta_mineral_wt = np.append(Delta_mineral_wt, Bentonites[i]['Delta_%Mont'])     
        mineral_type = np.append(mineral_type, 'Mont')
  
    except: #the mineral is smectite (No longer used, since is Montmorillonite always!)
        mineral_wt = np.append(mineral_wt,Bentonites[i]['%Smec'] )
        Delta_mineral_wt = np.append(Delta_mineral_wt, Bentonites[i]['Delta_%Smec'])    
        mineral_type = np.append(Delta_mineral_wt, 'Smectite')
        
        
        
#%% ################################ 3) Data plotting #######################

#### Chemical properties ###

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
plt.title("CEC of the clay mineral (Mont/Smec)", fontsize=22, wrap=True)           #title
plt.bar(names, CEC_clay, yerr = Delta_CEC_clay, edgecolor="black") 
plt.ylabel("$CEC_{clay}$ [cmol/kg]", fontsize=14)              #ylabel
plt.xlabel('Bentonite', fontsize = 14)
plt.tick_params(axis='both', labelsize=14)              #size of axis
plt.grid(True)
plt.xticks(rotation=30) #rotation = 'vertical', 40 for 40 degress
plt.savefig('CEC_clay_vs_bentonite.png', format='png')


### %mineral

plt.figure(figsize=(10,8))  #width, heigh 6.4*4.8 inches by default
plt.title("% Montmorillonite", fontsize=22, wrap=True)           #title
plt.bar(names, mineral_wt, yerr = Delta_CEC_clay, edgecolor="black") 
plt.ylabel("% Montmorillonite [%]", fontsize=14)              #ylabel
plt.xlabel('Bentonite', fontsize = 14)
plt.tick_params(axis='both', labelsize=14)              #size of axis
plt.grid(True)
plt.xticks(rotation=30) #rotation = 'vertical', 40 for 40 degress
plt.savefig('Mont_content_vs_bentonite.png', format='png')

### Physical properties ###

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
No big differences in the self made plots. Neither in the created y the author.

TO plot:
    .Limits in density fulfilling Pswell 
    .extract graphs from te report and make slides
'''