#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 23:17:57 2023

@author: alejandro
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as st
import importlib


par_rates = [.02,.03]
periods = [1,2]
n = len(periods)
n=2


df=pd.DataFrame()
df["period"]=periods
df["par_rates"]=par_rates


# for i in periods:
#     if i == 1:
#         spot_rates = [df.iloc[i-1]['par_rates']]
#     else:
#         par = par_rates[i-1]
#         y = 1-par*(1+spot_rates[i-2])**(-(i-1))
#         temp_spot_rates = [((1+par)*y**(-1))**(1/i)-1]
#         spot_rates = spot_rates + temp_spot_rates
                           
   
    
for i in periods:
    if i == 1:
        spot_rates = [df.iloc[i-1]['par_rates']]
    else:
        par = par_rates[i-1]
        y = 1-par*np.su
        temp_spot_rates = [((1+par)*y**(-1))**(1/i)-1]
        spot_rates = spot_rates + temp_spot_rates   
    
   
    
   
