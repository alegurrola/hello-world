#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 12:42:00 2023

@author: alejandro
"""

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
import yfinance as yf

fred = Fred(api_key='e9d9693f36697660831d6ff0627029c3')


def csv_timeseries(ric, from_date):
    directory = "/Users/alejandro/Downloads/Documents/Portfolio Management/Trading/Projects/" # hardcoded
    path = directory + ric + '.csv' 
    raw_data = pd.read_csv(path)
    t = pd.DataFrame()
    t['date'] = pd.to_datetime(raw_data['Date'], dayfirst=True) # Aqui se corrige formatos de fechas
    t['close'] = raw_data['Close']
    t = t.sort_values(by='date', ascending=True)
    t['close_previous_daily'] = t['close'].shift(1)
    t['return_daily'] = t['close']/t['close_previous_daily'] - 1
    
    t["close_previous_yearly"] = t['close'].shift(252)
    t['return_yearly'] = t['close']/t['close_previous_yearly'] - 1
    
    t['close_rolling'] = t['close'].rolling(11, center = True).mean() 
    t['close_previous_yearly_rolling'] = t['close_rolling'].shift(252)
    t['return_yearly_rolling'] = t['close_rolling']/t['close_previous_yearly_rolling'] - 1
    
    t = t.dropna()
    
    t = t.loc[t['date'] >= from_date]
    
    t = t.reset_index(drop=True)
    return t
    

def fred_timeseries(ric, date_from):
    data = fred.get_series(ric)
    data = pd.DataFrame(data)
    data = data.reset_index()
    data.columns = ["date", ric]
    data = data.sort_values(by='date', ascending=True)
    data = data.dropna()
    data = data.loc[data['date'] >= date_from]    
    data = data.reset_index(drop=True)
    data = data.sort_values(by='date', ascending=True)

    return data

def yahoo_timeseries(ric, date_from):
    
    df = yf.download(ric,  start = date_from)
    df = df.reset_index()
    t = pd.DataFrame()
    t['date'] = pd.to_datetime(df['Date'], dayfirst=True) 
    t = t.sort_values(by='date', ascending=True)
    t['close'] = df['Close']
    t['close_rolling'] = t['close'].rolling(11, center = True).mean() 
    
    t['close_previous_daily'] = t['close'].shift(1)
    t['return_daily'] = t['close']/t['close_previous_daily'] - 1
    
    t["close_previous_yearly"] = t['close'].shift(252)
    t['return_yearly'] = t['close']/t['close_previous_yearly'] - 1
    
    t['close_previous_yearly_rolling'] = t['close_rolling'].shift(252)
    t['return_yearly_rolling'] = t['close_rolling']/t['close_previous_yearly_rolling'] - 1

    t = t.reset_index(drop=True)
    
    return t

def load_timeseries(ric, date_from, source):
    if source == 'yahoo':
        df = yahoo_timeseries(ric, date_from)
    elif source == 'fred':
        df = fred_timeseries(ric, date_from)
    else: 
        df = csv_timeseries(ric, date_from)
    return df


    
    