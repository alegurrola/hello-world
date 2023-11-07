#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 16:11:56 2023

@author: alejandro
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as st
import importlib
from statsmodels.tsa.seasonal import seasonal_decompose
from functools import reduce

import agl_market_data
importlib.reload(agl_market_data)


# JTSJOL: Job Openings: Total Nonfarm (this series is treated as lagged one month,
#         for example, the sep-2023 value corresponds to oct-2023). This is the 
#         newest series beginning in Jan-2001
# CLF16OV: Civilian Labor Force
# UNEMPLOY: Unemployment Level
# UNRATE: Unemployment rate (the unemployment rate data is rounded,
#         thus it is better to calculate it manually as UNEMPLOY/CLF160V)

from_date = "1/12/2020" # dd/mm/yyyy
openings = agl_market_data.fred_timeseries("JTSJOL", from_date)
labor_force = agl_market_data.fred_timeseries("CLF16OV", from_date)
unemployment_level = agl_market_data.fred_timeseries("UNEMPLOY", from_date)

data_frames = [openings, labor_force, unemployment_level]
df = reduce(lambda  left,right: pd.merge(left,right,on=['date'],how='outer'), data_frames)
df = df.sort_values(by='date', ascending=True)

df["unemployment_rate"] = 100*df["UNEMPLOY"]/df["CLF16OV"]
df["JTSJOL"] = df["JTSJOL"].shift(1)

df = df.dropna()


df["vacancy_rate"] = 100*df["JTSJOL"]/df["CLF16OV"]
df["labor_mkt_tightness"] = df["vacancy_rate"]/df["unemployment_rate"]
df["efficient_rate"] = np.sqrt(df["vacancy_rate"]*df["unemployment_rate"])



x = df['unemployment_rate'].values
y = df['vacancy_rate'].values
plt.figure(figsize=(11,7))
plt.title("Beveridge curve")
plt.scatter(x,y)
plt.plot(x, y)
plt.plot(np.linspace(0,10,10) , np.linspace(0,10,10) , color='gray')
plt.ylabel("Vacancy rate (%)")
plt.xlabel("Unemployment rate (%)")
plt.xlim(3, 7)
plt.ylim(3, 8) 
plt.locator_params(axis='x', nbins=5)
plt.locator_params(axis='y', nbins=6) 
plt.grid(linestyle = "dashed")
plt.text(6.4, 4.1, "Jan-2021")
plt.text(4, 5.7, "Oct-2023")
plt.show()



plt.figure()
ax1 = df.plot(x="date", y=["unemployment_rate", "vacancy_rate", "efficient_rate"],\
              figsize=(12, 6))
plt.ylim(3, 8)
plt.locator_params(axis='y', nbins=5)
ax1.set_xlabel('Date')
ax1.set_ylabel('%')
plt.grid(linestyle = "dashed")
ax2 = ax1.twinx()
ax2.set_ylabel('%', rotation = 270)
plt.ylim(3, 8)
plt.show()




plt.figure()
ax1 = df.plot(x="date", y="labor_mkt_tightness",\
              figsize=(12, 6))
plt.ylim(0, 2.5)
plt.locator_params(axis='y', nbins=5)
ax1.set_xlabel('Date')
ax1.set_ylabel('Units')
plt.grid(linestyle = "dashed")
plt.axhline(y = 1, color = 'black') 
ax2 = ax1.twinx()
ax2.set_ylabel('Units', rotation = 270)
plt.ylim(0, 2.5)
plt.show()




