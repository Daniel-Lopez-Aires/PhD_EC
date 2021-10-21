#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 18:14:52 2021

@author: dla

Testing on my pipeting skills xD

I did 20something pipeting of 1mL, adding the content to a glass, and measuring
the weight. Lets see what we got xD. The measurements were carried out on 6/10/21
Pipet used: P1000 (maximum 1mL)

Stefaan suggests doing the same for other volumes!

"""
#%% ##################0) General packages useful######################

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pipetter_tester  #My function for the tester

#%% 


'''
So, in theory, each increment was 1mL = 1g. I do not know the precision of the
pipet. Seeing my results, the values are about 0.991, which is good, a difference
of .009 with respect to the ideal 1g difference (error bars not appreciable).

It is good enough? Chemist use the standard deviation to compute the systematic error. 
Do not know where the reference value comes from, but it seems like I obtained a higher
systematic error ==> 
'''

mass_1 = [.99053, 1.98296, 2.97654, 3.96811, 4.96, 5.95181, 6.94390,
                 7.93519, 8.92696, 9.9187, 10.91078, 11.90242, 12.89495,
                 13.88744, 14.87711, 15.86630, 16.85694, 17.84955, 18.84175,
                 19.83388, 20.82625, 21.81738, 22.80785, 23.79792, 24.78939]


Resuls_1 = pipetter_tester.Pipetting_tester(1, mass_1)

'''
So, random error good enough, but systematic error bigger than the reference. The
random error is associated to me, while the systematic is to the device, so it may be wrong?
Could redo those measurements again
'''

mass_2 = [1.4382, 1.9336, 2.4282, 2.9238, 3.4198, 3.9164, 4.4132, 4.9091, 5.4048, 5.9013,
              6.3962, 6.8923, 7.3891, 7.8849, 8.3800, 8.8749, 9.3694 ,9.8644, 10.3593,
              10.8548, 11.3495, 11.8443, 12.3397] 
                                            #[g] .5mL volume

Resuls_2 = pipetter_tester.Pipetting_tester(.5, mass_2, bins = 12)

'''
Worse random error, but still good. Same as before, bad systematic error :/
'''

mass_3 = [1.4767, 1.5731, 1.6720, 1.7699, 1.8687, 1.9662, 2.0657, 2.1642, 2.2635, 2.3625,
              2.4613, 2.5595, 2.6584, 2.7579, 2.8566, 2.9542, 3.051, 3.1514, 3.2505, 3.3502,
              3.4490, 3.5484, 3.6471, 3.7464, 3.8460, 3.9455, 4.0444] 
                                            #[g] .1mL volume

Resuls_3 = pipetter_tester.Pipetting_tester(.1, mass_3, bins = 20)

'''
Bad random error, but good systematic error ==> WTF?
'''

mass_4 = [1.4788, 2.4540, 3.4442, 4.4348, 5.4268, 6.4156, 7.4070, 8.3982, 9.3900,
              10.3789, 11.3670, 12.3584, 13.3443, 14.3363, 15.3275, 16.3167, 
              17.3052, 18.2944, 19.2809, 20.2724, 21.2603, 22.2482, 23.2398, 24.2229,
              25.2097] 
                                            #[g] .1mL volume

Resuls_4 = pipetter_tester.Pipetting_tester(1, mass_4, bins = 20)


'''
Bad random error, but good systematic error ==> WTF?


'''

#%% 3/10/21 Redo of everything

"""This time I used deionized water. I did 1st 1mL, then 500uL, then I changed the
plastic thing to do the 100uL.

I have seen:
    .Whatch out, some dropplets may be sucked by the pippete when releasing
    .beware of touching the wall of the vase, if not, dropplets may stay in the plastic
    thing of the pippete
"""
m_1mL = [1.4505, 2.4453, 3.4398, 4.4344, 5.4318, 6.4249, 7.4202, 8.4149,
         9.4094, 10.4049, 11.4013, 12.3936, 13.3858, 14.3764, 15.3644,
         16.3556, 17.3484, 18.3399, 19.3322, 20.3270, 21.3185]
res_1mL_3_10 = pipetter_tester.Pipetting_tester(1, m_1mL, bins = 20)


m_500uL = [1.4814, 1.9729, 2.4649, 2.9575, 3.4504, 3.9446, 4.4390, 4.9315,
           5.4220, 5.9174, 6.4104, 6.9031, 7.3970, 7.8920, 8.3847, 8.8767,
           9.3726, 9.8637, 10.3530, 10.8468, 11.3404, 11.8308, 12.3225, 12.8150]
res_500uL_3_10 = pipetter_tester.Pipetting_tester(.5, m_500uL, bins = 20)


m_100uL = [1.4898, 1.5738, 1.6665, 1.7605,1.8497,1.9398,2.0334, 2.1195, 2.2138, 
           2.3063, 2.3997, 2.4910, 2.5805, 2.6734, 2.7579, 2.8493, 2.9401, 
           3.0289, 3.1223, 3.2113, 3.2953, 3.3762]
res_100uL_3_10 = pipetter_tester.Pipetting_tester(.1, m_100uL, bins = 20)

'''
Random error horrible (on day 4_10 I discovered why)
Systematic error increasing in cronological order, the 2nd measurement has bigger
than the first, etc. So, could this be related to thef act that I did not change
the plastic thing?
'''


#%% 4/10/2021, Redo of 1mL, slowly

'''
This day I see that if you do it slowly, the ast dropplet fell down better.
2 measrements, in cronologic order, using the same plastic thing.
'''

m_1ml_410 = [1.5894, 2.5801, 3.5753, 4.5646, 5.5611, 6.5557, 7.5492, 8.5435, 9.5379,
             10.5297, 11.5278, 12.5233, 13.5218, 14.5178, 15.5131, 16.5081, 
             17.4979, 18.4912, 19.4839, 20.4753, 21.4694, 22.4608]
res_100uL_4_10 = pipetter_tester.Pipetting_tester(1, m_1ml_410, bins = 10)

#The following was done very slowly, ensuring the alst dropplet was out. So, letting
#the liequid go slowly.

m_1ml_410_ = [1.6958, 2.6818, 3.6689, 4.6615, 5.6537, 6.6405, 7.6300, 8.6197,
              9.6105, 10.5993, 11.5888, 12.5794, 13.5664, 14.5576, 15.5463, 
              16.5360, 17.5256, 18.5123, 19.5027, 20.4886, 21.4788, 22.4663,
              23.4509]
res_100uL_4_10_ = pipetter_tester.Pipetting_tester(1, m_1ml_410_, bins = 10)

'''
So, with that last result I got a low random error, whic means that in the previous 
sessions I was doing it wrongly because I was going to fast, fast enough not to take 
care of the last dropplet :)))))
    
That was concerning the unexpected increase in the random error. But,systematic error is 
still on the limit or above. Note that the first measuremnt have better systematic error
than the 2nd one, could this be because of reusing the plastic thing?
'''

#%% 19/10/21, redo of 1mL

'''
" emasurements of 1mL, int he first sometimes I see the droplet, and other not, which tells me
I was not doing it 100% good. In teh 2nd round, I did see the droplet always.
However, I did the sucking once wrong, touching the bottom, so I expell it and then suck it
again, and sometime I touched my coat :)"
        
'''

m_1mL_19_10 = [1.6437, 2.6059, 3.5997, 4.5932, 5.5880, 6.5793, 7.5749, 8.5670, 9.5635, 10.555,
               11.5476, 12.5431, 13.5369, 14.5307, 15.5209, 16.5156, 17.5085, 18.4997, 19.4884,
               20.4816, 21.4741, 22.4700]

res_1mL_19_10 = pipetter_tester.Pipetting_tester(1, m_1mL_19_10, bins = 12)

m_1mL_19_10_ = [1.6935, 2.6898, 3.6845, 4.6779, 5.6722, 6.6635, 7.6525, 8.6440,9.6366,
                10.6265, 11.6203, 12.6112, 13.6010, 14.5925, 15.5830, 16.5740, 17.5669,
                18.5604, 19.5518, 20.5404, 21.5361, 22.5314, 23.5249]

res_1mL_19_10_ = pipetter_tester.Pipetting_tester(1, m_1mL_19_10_, bins = 12)

'''
As expected, the 2nd measure has less random error, at the limit, 0.2%. How in the hell did I
manage on the first day to get 0.1%? because I was nervous because Stefaan was watching me? xD
In any case, systemaic error to high
'''


#%% 21/10/21, redo of .5mL

'''
Measurements of .5mL. 2 emasurements. In thef irst one, always I drop the last dropplet, in the 2nd,
I do sveral mistakes echando el liquido muy rapido, no viendo la goita o succionandola, pq al soltar 
el final, sorbe un poco.
        
'''

m_0_5mL_21_10 = [1.6434, 2.1348, 2.6260, 3.1192, 3.6108, 4.1046, 4.5957, 5.0901, 5.5831, 6.0757,
                 6.5685, 7.0600, 7.5531, 8.0453, 8.5385, 9.0298, 9.5227, 10.0147, 10.5076, 11.0011, 
                 11.4921, 11.9845]

res_0_5mL_21_10 = pipetter_tester.Pipetting_tester(.5, m_0_5mL_21_10, bins = 15)

m_0_5mL_21_10_ = [1.6909, 2.1869, 2.6818, 3.1755, 3.6688, 4.1616, 4.6568, 5.1503, 5.6435, 6.1392,
                  6.6308, 7.1212, 7.6176, 8.1124, 8.6100, 9.1027, 9.5977, 10.0911, 10.5837,
                  11.0759, 11.5688]

res_0_5mL_21_10_ = pipetter_tester.Pipetting_tester(.5, m_0_5mL_21_10_, bins = 12)

'''
As expected, the 2nd measure has less random error, at the limit, 0.2%. How in the hell did I
manage on the first day to get 0.1%? because I was nervous because Stefaan was watching me? xD
In any case, systemaic error to high
'''