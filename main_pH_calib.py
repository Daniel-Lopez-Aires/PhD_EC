# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 08:38:52 2022

@author: lopedan

Main script for the pH calibration. You introduce the calibration values, conductivity
and pH, and then introduce the conductivity values of the solutions you want to know their 
pH, and it will compute it.

Need the script Fits to run, so they should be in
the same folder!!! Alternatively, the relevant functions could be copy and pasted here,
but its better to simplify the code and to have different scripts, more handable.

"""


#%%###### 0) General packages useful #################

import matplotlib.pyplot as plt  #for simplicity, to not write matplotlib.pyplot
        #everytime we want to plot something

#from scipy.stats import norm               ##norm.fit() fit to gaussian
import numpy as np
    #np contain linspaces as np.linspace(a,b,N)
import pandas as pd
        
#from plotly.graph_objs import Bar, Layout
#from plotly import offline

#import sys                   #to import functions from other folders!!
#sys.path.insert(0, '/home/dla/Python/Functions_homemade')   #path where I have the functions

import Fits

######3


#%%########## 1) Data load and fit ###################

#First the data for the calibration need to be written:
    
potential_calib = np.array([136.0, -34.0, -164.0, -325.0, -376.0])  
                                #[mV] measured potential of the reference solutions
pH_calib = np.array([4.010, 7.000, 9.210, 12.000, 13.000])         
                                #[pH] pH os the reference solutions, given

#The calibration is, provided that the variable to compute is pH based on conductivity:
Calib = Fits.LinearRegression(potential_calib, pH_calib)    #Fit pH-Conductivity

#The fit eq is: pH = Conductivity*slope + intercept
#Note error are also provided, although not used here (aggh, these chemist)


#%%######## 2) Using the fit #########################

#Now it is easy to use the fit, simply type the measured potential and then compute
#the pH in the standard wat
potential_target = np.array([-105.0, -391-0, 223.0])      #[mV] Measured potential of the solutions to measure
pH_target = Calib['Slope']*potential_target + Calib['Intercept']        #[pH] computed pH of the solution to measure


print()
print('Measured conductivity:')
print(potential_target) 
print()
print('Calculated pH:')
print(pH_target) 