#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 18:00:29 2023

@author: alejandro
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as st
import importlib
from fredapi import Fred

fred = Fred(api_key='e9d9693f36697660831d6ff0627029c3')



def load_timeseries(ric, from_date, frequency):
    directory = "/Users/alejandro/Downloads/Documents/Portfolio Management/Trading/Projects/" # hardcoded
    path = directory + ric + '.csv' 
    raw_data = pd.read_csv(path)
    t = pd.DataFrame()
    t['date'] = pd.to_datetime(raw_data['Date'], dayfirst=True) # Aqui se corrige formatos de fechas
    t['close'] = raw_data['Close']
    t = t.sort_values(by='date', ascending=True)
    
    if frequency == "daily":
        t['close_previous_daily'] = t['close'].shift(1)
        t['return_daily'] = t['close']/t['close_previous_daily'] - 1
    elif frequency == "yearly":
        t["close_previous_yearly"] = t['close'].rolling(11, center = True).mean()
        t["close_previous_yearly"] = t['close_previous_yearly'].shift(252)
        t['return_yearly'] = t['close']/t['close_previous_yearly'] - 1
    
    t = t.dropna()
    
    from_date_2 = pd.to_datetime(from_date, dayfirst=True) 
    t = t.loc[t['date'] >= from_date_2]
    
    t = t.reset_index(drop=True)
    return t
    

def fred_timeseries(ric, date_from):
    data = fred.get_series(ric)
    data = pd.DataFrame(data)
    data = data.reset_index()
    data.columns = ["date", ric]
    data = data.sort_values(by='date', ascending=True)
    data = data.dropna()
    date_from = pd.to_datetime(date_from, dayfirst=True) 
    data = data.loc[data['date'] >= date_from]    
    data = data.reset_index(drop=True)
    data = data.sort_values(by='date', ascending=True)

    return data


class distribution:
    
    # constructor
    def __init__(self, ric, from_date, frequency, decimals = 2):
        
        self.ric = ric
        self.from_date = from_date
        self.frequency = frequency
        self.decimals = decimals
        self.timeseries = None
        self.name = None
        self.vector = None
        self.mean = None
        self.volatility = None
        self.sharpe_ratio = None
        self.var_95 = None

        
    def load_timeseries(self):
        self.name = "return_" + self.frequency
        self.timeseries=load_timeseries(self.ric, self.from_date, self.frequency)
        self.vector=self.timeseries[self.name].values
        self.size=len(self.vector)

    def plot_timeseries(self):
        plt.figure(figsize=(12,5))
        plt.title('Time series of close prices and ' + self.frequency + " returns")
        plt.xlabel('Date')
        plt.ylabel('Prices')
        ax = plt.gca()
        ax1 = self.timeseries.plot(kind='line', x='date', y='close', ax=ax, grid=True,\
                                  color='blue', label="Close")
        ax2 = self.timeseries.plot(kind='line', x='date', y=self.name, ax=ax, grid=True,\
                                  color='red', secondary_y=True, label=self.name)
        ax1.legend(loc=2)
        ax2.legend(loc=1)
        plt.show()

        
    def compute_stats(self):
        if self.frequency == "daily":
            factor = 252
        else:
            factor = 1
        self.mean = st.tmean(self.vector)*factor
        self.volatility = st.tstd(self.vector)*np.sqrt(factor)
        self.sharpe_ratio = self.mean / self.volatility
        self.var_95 = np.percentile(self.vector,5)
        
    def plot_histogram(self):
        self.ric += '\n' + 'mean=' + str(np.round(self.mean,self.decimals)) \
            + ' | ' + 'volatility=' + str(np.round(self.volatility,self.decimals)) \
            + '\n' + 'sharpe_ratio=' + str(np.round(self.sharpe_ratio,self.decimals)) \
            + ' | ' + 'var_95=' + str(np.round(self.var_95,self.decimals)) 
        plt.figure()
        plt.hist(self.vector,bins=50)
        plt.title(self.ric)
        plt.show()
    

          

    
    
