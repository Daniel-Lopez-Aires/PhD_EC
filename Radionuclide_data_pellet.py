# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 09:50:28 2022

@author: lopedan

Radionuclide inventory of the UO2 fuel pellet (Westinghouse)

	Pellet data		
	Burn-up [GWd/tU]	60	
	Cycles	5	
	Length cycle [d]	352	
	Enrichment [%]	3.95	
Molec mass	U [g/mol]	238.03	
	UO2 [g/mol]	270.03	
    
We start from the ORIGEN code and then compute several derived magnitudes such as:
    .Elemental content per g UO_2
    .Isotopic abundance per chemical element
"""

#%% ################################# 0) Package import######################

import time                                 #to measure the running time
import numpy as np                          #numpy array object, very useful
import pandas as pd                      #dataframe object, extremely useful
import matplotlib.pyplot as plt               #for plotting


#%% ###################################### 1) Import ################

M_U = 238.02891                             #[g/mol] molecular mass of U
M_UO2 = 238.02891 + 2*15.9994          #[g/mol] molecular mass of UO_2

Data=pd.read_excel('Leachates_data_read_version.xlsx','Theoretical inventory')
    #Data from the ORIGEN code
    
Nuclides = Data['Nuclide']               #Nuclides
Con = Data['Content [g/tU]']       #Content, in g/ton of U
Con_UO2 = Con * M_U / M_UO2         #Content, in ug/gUO2
Rel_Con_UO2 = Con_UO2 / sum(Con_UO2) *100           #[%] Relative content 


#%% ########################## 2) Derived calcs ##########################

#We need to get the elements in the pellet. We can write them manually, but they can also
#be extracted from the Nuclides data as follows: you first remove the mass number with an splitter,
#and then get the non-repeated elements:
    
Nuclides_spl = np.array([x.split('-')[0] for x in Nuclides ]) #Nuclides, removing the mass number (splited)
Elements = np.unique(Nuclides_spl)

#Since that output is a bit mixed, to recover the proper order (increasing in Z) we can do:
indexes = np.unique(Nuclides_spl, return_index=True)[1]
Elements = np.array([Nuclides_spl[index] for index in sorted(indexes)])     #Elements, in the right order


#This is nuclide calculation. To do elemental, I should gather the isotopes. How
#can I do that? 
#The nuclides present in the pellet are:
    #H, He, Li, Be, C, Ge, As, Se, Br, Kr, Rb, Se, Sr, Y, Zr, Nb, Mo, Tc, Ru, Rh, Pd,
    #Ag, Cd, In, Sn, Sb, Te, I, Xe, Cs, Ba, La, Ce, Pr, Nd, Pm, Sm, Eu, Gd, Tb, Dy, Ho,
    #Er, Tl, Pb, Bi, Po, Rb, Ra, Ac, Th, Pa, U, Np, Pu, Am, Cm, Bk, Cf 
    
    
# Elements = np.array(['H', 'He', 'Li', 'Be', 'C', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb',
#                      'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag',
#                      'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 
#                      'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tl',
#                      'Pb', 'Bi', 'Po', 'Ra', 'Rn', 'Ac', 'Th', 'Pa', 'U', 'Np',
#                      'Pu', 'Am', 'Cm', 'Bk', 'Cf'])


#You could check if any vowel is in the nuclide dataframe, and if so, start the operations!
#But, you will need to manually exclude the commons; g: H is in H and also He, etc

#But douing this manually will be horrible, think how to do it automatically with a loop.
#For each Element in elements, check which rows in the dataframe (or equivalently data in Nuclides)
#contains the name of the Element, and if so, add ihs content to get elemental content.
#Well, the loop bad idea because of the common things, so will proceed with an actually simpler approach,
#split the names, so that He-4 is splited into [He, 4], and get the first element, and now I
#could do the loop


Nuclides_spl = [x.split('-')[0] for x in Nuclides ] #Nuclides, removing the mass number (splited)

#With that vector now I can do it:

Elem_con = np.array([])         #[ug/gUO2] array that will store elemental concentration
content_iso= np.array([])

for i  in range(len(Elements)):              #loop in the chemical elements
    content_iso= np.array([])               #Initialization/reset of the isotopic content of a given element
    #
    for j in range(len(Nuclides)):          #loop in the nuclides
        if Elements[i] == Nuclides_spl[j]: #If the Nuclide is an isotope of the element, get its content
            content_iso = np.append(content_iso, Con_UO2[j])  #Add the content of the isotopes of the given element
            #
        content=sum(content_iso)        #Total elemental content    
    #
    #Once the elemental content has been computed, store it:
    Elem_con =np.append(Elem_con, content)  #store the content
    
    
#Yas, value double checked with Excel ;)

#Now we can also compute the relative elemental content. Note the gUO2 are not needed for this calc:
    
Elem_con_rel = Elem_con / sum(Elem_con) *100            #[%] Relative elemental content


#To understand this, we could create a datafram with the nuclies, its relative elemental, and sort them
#from max elemental concentration to lower!

df_elements = pd.DataFrame( data = np.array([Elements, Elem_con_rel, Elem_con]).T, columns=['Element', 
                                                                                        'Relative content[%]',
                                                                                        'Concentration[ug/gUO_2]'])

#It is neccessary to convert the numbers to float, to operate with them, since they are strings!

df_elements['Concentration[ug/gUO_2]'] =df_elements['Concentration[ug/gUO_2]'].astype(float)
df_elements['Relative content[%]'] =df_elements['Relative content[%]'].astype(float)

df_elements_sort = df_elements.sort_values(by = 'Relative content[%]', ascending = False)   #TO sort according
    #to the relative concentration, from largest relative concentration to lowest

print()
print('Most abundant elements in the pellet')    
print(df_elements_sort)



#############
#Another thing I could compute here is the relative abundance of each isotope for each element. To do so, we
#can modify the previous loop to store everymass. Actually no, I do not see an evident solution, so will create
#another loop with the elements; for each element check the nuclides data, and if they are similar (same
#element) store the content, and when they are different (next element), copmute the relative content and
#store it:
    
rel_iso_abun = np.array([])              #Initialiyation, relative abundance of each isotope for a certain 
            #element
            
for i in range(len(Elements)):   
    iso_content = np.array([])      #Initialization/reset of variable containnig concentration of isotopes
        #per each element
    aux = np.array([])                              #Initialization/reset of the auxiliar variable
    #
    for j in range(len(rel_iso_abun),len(Nuclides)):
        if Elements[i] == Nuclides_spl[j]:              #If they are isotopes, get the content
            iso_content = np.append(iso_content, Con_UO2[j] )
        #
        elif j == len(Nuclides)-1:      #For a problem with the last iteration, do not compute the aux
            aux= iso_content/sum(iso_content) *100
            #
        else:                               #If they are not isotopes, the following element 
        #(increasing in Z) is the one, so we can compute now the relative abundance and exit
            aux= iso_content/sum(iso_content) *100  #[%] auxiliar variable containing the relative abundance
            break   #We can exit the loop not to compare more isotopes since the elements will be differents
    #
    
        #The next loop is to solve a problem with the last iteration, I have not figured out why in the hell
        #happen but at least I came up with a solution :/
        
    if i == len(Elements)-1 and j == len(Nuclides)-1: #Last iteration loop for problem fixing
        aux= iso_content/sum(iso_content) *100  #[%] auxiliar variable containing the 
        
    rel_iso_abun = np.append(rel_iso_abun, aux)  #Storing of the relative isotopic content per element
            # #       
 

            
##Yas, double checked with excel ;) ==> fuck excel!     Lets create a nuclide df with this info:

df_nuclides = pd.DataFrame( data = np.array([Nuclides, Con_UO2, rel_iso_abun]).T, 
                           columns=['Element','Content [ug/gUO_2]','Relative abundance[%]'])
    
df_nuclides['Content [ug/gUO_2]'] =df_nuclides['Content [ug/gUO_2]'].astype(float)
df_nuclides['Relative abundance[%]'] =df_nuclides['Relative abundance[%]'].astype(float)

df_nuclides_sort = df_nuclides.sort_values(by = 'Content [ug/gUO_2]', ascending = False)   #TO sort according
    #to the relative concentration, from largest relative concentration to lowest
    
print()
print('Most abundant nuclides in the pellet')
print(df_nuclides_sort)




'''
So, from this 2 dataframes sorted we can see:
    
1. More abundant elements: U, Pu, Xe, Nd, Zr, Mo, Cs, Ce, Ru, Ba, Pd, La, Pr,..
2. More abundant isotopes: U238, Pu239, U236, Xe136, U235, Pu240, Xe134, Nd144, Ba138, Ce140,
    La139, Ce142, Xe132, Pr141, Cs137, Cs133, Mo100, Mo98

'''

#%%######################################### 3) Plot ##################

#Lets try a 59 bar plto xDD

plt.figure(figsize=(25,10))  #width, heigh 6.4*4.8 inches by default
plt.bar(Elements, Elem_con_rel, edgecolor="black") 
plt.title("Theoretical elements in UO2 pellet (60GWd/tU, 5 cycles of 352 days each, 3.95% enrichment)", fontsize=20)           #title
plt.xlabel("Element", fontsize=14)                        #xlabel
plt.ylabel("Content [%]", fontsize=14)              #ylabel
plt.yscale('log')                                          #y axis in log scale
# Set size of tick labels.
plt.tick_params(axis='both', labelsize=14)              #size of axis
plt.grid(True) 
plt.savefig('Elements_in_pellet.png', format='png', bbox_inches='tight') 
        #The bbox_inches is to save the figure with less blank space!!






#%% ######## 4) Load leaching results ####################

Data_BIC=pd.read_excel('Leachates_data_read_version.xlsx','Concentration(M) BIC-FULL')
    #Data from the ORIGEN code
    #Note the data from Te from 111days in filtered was wrong, so I set to 0!
t_BIC = Data_BIC['T_run(d)'][0:10]       #[d] Experiment time
Elements_ICPMS = np.array(Data_BIC['Element'])    #Elements measured in ICPMS

Data_YCWCa=pd.read_excel('Leachates_data_read_version.xlsx','Concentration(M) YCWCa-FULL')
t_YCW = Data_YCWCa['T_run(d)'][0:11]       #[d] Experiment time
#Those results can be plotted to be better understood



#%%  ###### 5) plot leaching results ########################

#The simplest thing would be do one loop, and for each loop, plot. The loop will be
#for each experiment time, both plots, filtered and non filtered.s


##########BIC

for i in range(len(t_BIC)):                     #Loop through all the experiments time
    plt.figure(figsize=(24,16))  #width, heigh 6.4*4.8 inches by default
    plt.suptitle("Leachate experiments BIC, running time="+str(t_BIC[i])+'d', fontsize=22, wrap=True)           #title
    #
    plt.subplot(2, 1, 1)
    plt.bar(Elements_ICPMS, Data_BIC['60FULL-F'+str(i+1)], edgecolor="black")     #like that u can iterate 
    plt.title("Filtered leachant", fontsize=22)           #title
    plt.xlabel("Element", fontsize=14)                        #xlabel
    plt.ylabel("Concentration [M]", fontsize=16)              #ylabel
    plt.yscale('log')                                          #y axis in log scale
    # Set size of tick labels.
    plt.tick_params(axis='both', labelsize=16)              #size of axis
    plt.ylim(1e-12,1e-4)                                     #limits of y axis
    plt.grid(True) 
    #
    plt.subplot(2, 1, 2)
    plt.bar(Elements_ICPMS, Data_BIC['60FULL-NF'+str(i+1)], edgecolor="black")     #like that u can iterate 
    plt.title("Non filtered leachant", fontsize=22)           #title
    plt.xlabel("Element", fontsize=14)                        #xlabel
    plt.ylabel("Concentration [M]", fontsize=16)              #ylabel
    plt.yscale('log')                                          #y axis in log scale
    plt.tick_params(axis='both', labelsize=16)              #size of axis
    plt.ylim(1e-12,1e-4)                                     #limits of y axis
    plt.grid(True) 
    #
    plt.savefig('BIC_t_run_'+str(i) +'.png', format='png', bbox_inches='tight') 
    


############# YCWCa


for i in range(len(t_YCW)):                     #Loop through all the experiments time
    plt.figure(figsize=(24,16))  #width, heigh 6.4*4.8 inches by default
    plt.suptitle("Leachate experiments YCW, running time="+str(t_YCW[i])+'d', fontsize=22, wrap=True)           #title
    #
    plt.subplot(2, 1, 1)
    plt.bar(Elements_ICPMS, Data_YCWCa['60 Si F-'+str(i+1)], edgecolor="black")     #like that u can iterate 
    plt.title("Filtered leachant", fontsize=22)           #title
    plt.xlabel("Element", fontsize=14)                        #xlabel
    plt.ylabel("Concentration [M]", fontsize=16)              #ylabel
    plt.yscale('log')                                          #y axis in log scale
    # Set size of tick labels.
    plt.tick_params(axis='both', labelsize=16)              #size of axis
    plt.ylim(1e-12,1e-4)                                     #limits of y axis
    plt.grid(True) 
    #
    plt.subplot(2, 1, 2)
    plt.bar(Elements_ICPMS, Data_YCWCa['60 Si NF-'+str(i+1)], edgecolor="black")     #like that u can iterate 
    plt.title("Non filtered leachant", fontsize=22)           #title
    plt.xlabel("Element", fontsize=14)                        #xlabel
    plt.ylabel("Concentration [M]", fontsize=16)              #ylabel
    plt.yscale('log')                                          #y axis in log scale
    plt.tick_params(axis='both', labelsize=16)              #size of axis
    plt.ylim(1e-12,1e-4)                                     #limits of y axis
    plt.grid(True) 
    #
    plt.savefig('YCW_t_run_'+str(i) +'.png', format='png', bbox_inches='tight') 
    
    
    
'''
Anaylsis ########

OVERAL:
    .BIC have more elements with high concentrations than YCW
    . Pm is the element that dissolve less always, anytime ==> Hard to find
  

######YCW
.We see the larger peaks,Rb, Cs, U, Mo, and as time goes by they increase and the
surrounding elements also!
.Element that dissolve most: Cs and then Mo surpass it

##### BIC
#Rb, Cs, U, Mo dominates, but other elements gets really similar, such as Sr, Cd, Ba
ELement that dissolve most: Cs, and then U surpass it


'''


#%% 6) plot of concentration of each element as a function of experiment time

#Another really interesting thing to plot is the concentration in the leachate as a 
#function of time, per each element. A lot of graphs, but we can make subplots and plot in 1 figure the 4
#subplot of each element (filtered and non filt, BIC and YCW). To get the concentration from a 
#pandas is not difficult:

#1st lets find the index per elements to automatize the process: lets find U index

# a = np.where(Elements_ICPMS=='U')[0][0]         #THis gives the index where U is
# conc_U_BIC= np.array(Data_BIC.iloc[np.where(Elements_ICPMS=='U')[0][0]])
# conc_U_BIC = conc_U_BIC[2:]         #To remove the NaN (or time) and the element
# #That contain all the U concentration, filtered and not filtered. To select one, provided
# #that the order is 1st filter then NF we can do:

# conc_U_BIC_F = conc_U_BIC[0:len(t_BIC)]



#Now the automatization of that thing (commented now) can start:
    
for i in range(len(Elements_ICPMS)):        #loop for each element
    
    #aux_1 = np.where(Elements_ICPMS == Elements_ICPMS[i])[0][0]    #THis gives the index where the
        #desired element is
    conc_BIC= np.array(Data_BIC.iloc[np.where(Elements_ICPMS == Elements_ICPMS[i])[0][0]]) 
                                #[M]Take concentrations for both filtered and non filtered
    conc_BIC = conc_BIC[2:]         #[M] To remove the NaN (or time) and the element name
    
    #To get the filtered and non filtered data we can do:
    conc_BIC_F = conc_BIC[0:len(t_BIC)]         #[M] filtered concentration
    conc_BIC_NF = conc_BIC[len(t_BIC):]         #[M] non filtered concentration
    
    #We need to do essentially the same for YCWCa:
    conc_YCW= np.array(Data_YCWCa.iloc[np.where(Elements_ICPMS == Elements_ICPMS[i])[0][0]]) 
                    #[M]Take concentrations for both filtered and non filtered
    conc_YCW = conc_YCW[2:]         #[M] To remove the NaN (or time) and the element name
    
    #To get the filtered and non filtered data we can do:
    conc_YCW_F = conc_YCW[0:len(t_YCW)]         #[M] filtered concentration
    conc_YCW_NF = conc_YCW[len(t_YCW):]         #[M] non filtered concentration        
    #
    #And now we can plot the 4 of them per figure:
     #   
    plt.figure(figsize=(15,8))  #width, heigh 6.4*4.8 inches by default
    plt.suptitle("Concentration in the leachant of "+Elements_ICPMS[i], fontsize=22, wrap=True)           
                #title
    #
    plt.subplot(1, 2, 1)
    plt.plot( t_BIC, conc_BIC_F, 'bo--', linewidth=2, label= 'Filtered' )    
    plt.plot( t_BIC, conc_BIC_NF, 'ro--', linewidth=2, label = 'Non filtered')    
    plt.title("Leachant with BIC", fontsize=16)           #title
    plt.xlabel("Time [d]", fontsize=14)                        #xlabel
    plt.ylabel("Concentration [M]", fontsize=14)              #ylabel
    # Set size of tick labels.
    plt.tick_params(axis='both', labelsize=14)              #size of axis
    #plt.ylim(1e-12,1e-4)                                     #limits of y axis
    plt.grid(True) 
    plt.legend()
    #
    plt.subplot(1, 2, 2)
    plt.plot( t_YCW, conc_YCW_F, 'bo--', linewidth=2, label= 'Filtered' )    
    plt.plot( t_YCW, conc_YCW_NF, 'ro--', linewidth=2, label = 'Non filtered')      
    plt.title("Leachant with YCW", fontsize=16)           #title
    plt.xlabel("Time [d]", fontsize=14)                        #xlabel
    plt.ylabel("Concentration [M]", fontsize=14)              #ylabel
    # Set size of tick labels.
    plt.tick_params(axis='both', labelsize=14)              #size of axis
    #plt.ylim(1e-12,1e-4)                                     #limits of y axis
    plt.grid(True) 
    plt.legend()
    #
    #
    plt.savefig('Concentration_'+Elements_ICPMS[i] +'_in_leach.png', format='png', bbox_inches='tight') 
    
    
    
    
'''Analysis

.Wow, each element has apparently a different trend ==> :))
.Most of the elements dissolve more in BIC,but not all!
.Note than precipitation can occur once the concentration is too high (saturate), which
could explain some o the graphs, since its common to see initial increase and then decrease

'''


#To understand it better, maybe we can plot the time variation of concentration of all
#elements? lets try. For this we need to plot columns. We will use a loop lop to avoid
#writting a lot of times the same plot xD. But, the plot is not that good because
#there are 10 different colors, so since we have 25 elements, they start repeating, which
#is bad for the interpretation, so should create 3 different line patters to help
#distinguish it. How can we do that? the simplest is 3 loops, 1 of 10, then other 10, then
#the reamining 5 :)


#################BIC

    
    

##### F
    
plt.figure(figsize=(24,16))  #width, heigh 6.4*4.8 inches by default
for i in range(10):     #Loop through first 10 elements
    
    plt.plot(Data_BIC['T_run(d)'][0:10],Data_BIC.iloc[i][2:12], 'o--', linewidth=2, label= Elements_ICPMS[i] )
        #[2:12] to cover all the values of the F (0 is the time, 1 is element)

for i in range(10):     #Loop through second 10 elements
    
    plt.plot(Data_BIC['T_run(d)'][0:10],Data_BIC.iloc[10+i][2:12], 'o-.', linewidth=2, label= Elements_ICPMS[10+i] )
        #[2:12] to cover all the values of the F (0 is the time, 1 is element)

for i in range(5):     #Loop through the reamining 5 elements of eleements ICPMS
    
    plt.plot(Data_BIC['T_run(d)'][0:10],Data_BIC.iloc[20+i][2:12], 'o:', linewidth=2, label= Elements_ICPMS[20+i] )
        #[2:12] to cover all the values of the F (0 is the time, 1 is element)
    
        
# plt.plot(Data_BIC['T_run(d)'][0:10],Data_BIC.iloc[0][0:10], 'bo--', linewidth=2, label= 'Sr' ) 
# plt.plot(Data_BIC['T_run(d)'][0:10],Data_BIC.iloc[0][0:10], 'bo--', linewidth=2, label= 'Y' ) 
# plt.plot(Data_BIC['T_run(d)'][0:10],Data_BIC.iloc[0][0:10], 'bo--', linewidth=2, label= 'Rb' ) 
# plt.plot(Data_BIC['T_run(d)'][0:10],Data_BIC.iloc[0][0:10], 'bo--', linewidth=2, label= 'Rb' ) 
# plt.plot(Data_BIC['T_run(d)'][0:10],Data_BIC.iloc[0][0:10], 'bo--', linewidth=2, label= 'Rb' ) 
# plt.plot(Data_BIC['T_run(d)'][0:10],Data_BIC.iloc[0][0:10], 'bo--', linewidth=2, label= 'Rb' ) 
# plt.plot(Data_BIC['T_run(d)'][0:10],Data_BIC.iloc[0][0:10], 'bo--', linewidth=2, label= 'Rb' ) 
# plt.plot(Data_BIC['T_run(d)'][0:10],Data_BIC.iloc[0][0:10], 'bo--', linewidth=2, label= 'Rb' ) 
# plt.plot(Data_BIC['T_run(d)'][0:10],Data_BIC.iloc[0][0:10], 'bo--', linewidth=2, label= 'Rb' ) 

plt.title("Concentration of every element for the filtered case in BIC", fontsize=20)           #title
plt.xlabel("Time [d]", fontsize=14)                        #xlabel
plt.ylabel("Concentration [M]", fontsize=14)              #ylabel
plt.yscale('log')                                          #y axis in log scale
plt.tick_params(axis='both', labelsize=14)              #size of axis
plt.grid(True) 
plt.legend()
plt.ylim(1e-14,1e-4)                                     #limits of y axis
plt.savefig('Concentration_all_BIC_F.png', format='png', bbox_inches='tight')    


##### NF


plt.figure(figsize=(24,16))  #width, heigh 6.4*4.8 inches by default
for i in range(10):     #Loop through first 10 elements
    
    plt.plot(Data_BIC['T_run(d)'][0:10],Data_BIC.iloc[i][12:], 'o--', linewidth=2, label= Elements_ICPMS[i] )
        #[2:12] to cover all the values of the F (0 is the time, 1 is element)

for i in range(10):     #Loop through second 10 elements
    
    plt.plot(Data_BIC['T_run(d)'][0:10],Data_BIC.iloc[10+i][12:], 'o-.', linewidth=2, label= Elements_ICPMS[10+i] )
        #[2:12] to cover all the values of the F (0 is the time, 1 is element)

for i in range(5):     #Loop through the reamining 5 elements of eleements ICPMS
    
    plt.plot(Data_BIC['T_run(d)'][0:10],Data_BIC.iloc[20+i][12:], 'o:', linewidth=2, label= Elements_ICPMS[20+i] )
        #[2:12] to cover all the values of the F (0 is the time, 1 is element)
    
plt.title("Concentration of every element for the non-filtered case in BIC", fontsize=20)           #title
plt.xlabel("Time [d]", fontsize=14)                        #xlabel
plt.ylabel("Concentration [M]", fontsize=14)              #ylabel
plt.yscale('log')                                          #y axis in log scale
# Set size of tick labels.
plt.tick_params(axis='both', labelsize=14)              #size of axis
plt.grid(True) 
plt.legend()
plt.ylim(1e-14,1e-4)                                     #limits of y axis
plt.savefig('Concentration_all_BIC_NF.png', format='png', bbox_inches='tight')      



#################YCWCa


##### F
    
plt.figure(figsize=(24,16))  #width, heigh 6.4*4.8 inches by default
for i in range(10):     #Loop through first 10 elements
    
    plt.plot(Data_BIC['T_run(d)'][0:11],Data_YCWCa.iloc[i][2:13], 'o--', linewidth=2, label= Elements_ICPMS[i] )
        #[2:12] to cover all the values of the F (0 is the time, 1 is element)

for i in range(10):     #Loop through second 10 elements
    
    plt.plot(Data_BIC['T_run(d)'][0:11],Data_YCWCa.iloc[10+i][2:13], 'o-.', linewidth=2, label= Elements_ICPMS[10+i] )
        #[2:12] to cover all the values of the F (0 is the time, 1 is element)

for i in range(5):     #Loop through the reamining 5 elements of eleements ICPMS
    
    plt.plot(Data_BIC['T_run(d)'][0:11],Data_YCWCa.iloc[20+i][2:13], 'o:', linewidth=2, label= Elements_ICPMS[20+i] )
        #[2:12] to cover all the values of the F (0 is the time, 1 is element)
    
plt.title("Concentration of every element for the filtered case in YCWCa", fontsize=20)           #title
plt.xlabel("Time [d]", fontsize=14)                        #xlabel
plt.ylabel("Concentration [M]", fontsize=14)              #ylabel
plt.yscale('log')                                          #y axis in log scale
# Set size of tick labels.
plt.tick_params(axis='both', labelsize=14)              #size of axis
plt.grid(True) 
plt.legend()
plt.ylim(1e-14,1e-4)                                     #limits of y axis
plt.savefig('Concentration_all_YCWCa_F.png', format='png', bbox_inches='tight')     


##### NF
    
plt.figure(figsize=(24,16))  #width, heigh 6.4*4.8 inches by default
for i in range(10):     #Loop through first 10 elements
    
    plt.plot(Data_BIC['T_run(d)'][0:11],Data_YCWCa.iloc[i][13:], 'o--', linewidth=2, label= Elements_ICPMS[i] )
        #[2:12] to cover all the values of the F (0 is the time, 1 is element)

for i in range(10):     #Loop through second 10 elements
    
    plt.plot(Data_BIC['T_run(d)'][0:11],Data_YCWCa.iloc[10+i][13:], 'o-.', linewidth=2, label= Elements_ICPMS[10+i] )
        #[2:12] to cover all the values of the F (0 is the time, 1 is element)

for i in range(5):     #Loop through the reamining 5 elements of eleements ICPMS
    
    plt.plot(Data_BIC['T_run(d)'][0:11],Data_YCWCa.iloc[20+i][13:], 'o:', linewidth=2, label= Elements_ICPMS[20+i] )
        #[2:12] to cover all the values of the F (0 is the time, 1 is element)
    
plt.title("Concentration of every element for the nono-filtered case in YCWCa", fontsize=20)           #title
plt.xlabel("Time [d]", fontsize=14)                        #xlabel
plt.ylabel("Concentration [M]", fontsize=14)              #ylabel
plt.yscale('log')                                          #y axis in log scale
# Set size of tick labels.
plt.tick_params(axis='both', labelsize=14)              #size of axis
plt.grid(True) 
plt.ylim(1e-14,1e-4)                                     #limits of y axis
plt.legend()
plt.savefig('Concentration_all_YCWCa_NF.png', format='png', bbox_inches='tight')    


''''
Note we omit somethings, the scale to show everything is -4 to -27M! But those exremely
low values I have no clue why they are there. TO ask steff, but to -15M we see the bigger
picture
'''