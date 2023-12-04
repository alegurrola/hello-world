#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 13:03:09 2023

@author: alejandro
"""



import datetime as dt
import pandas as pd
import yfinance as yf
import importlib
import numpy as np
import matplotlib.pyplot as plt
from datetime import date
import scipy.stats as st


import agl_market_data
importlib.reload(agl_market_data)

import load_market_data
importlib.reload(load_market_data)



ric = 'PCE' # AAPL # ^GSPC
source = "fred" # yahoo  fred  csv
date_from = "2010-12-31" # yyyy-mm-dd
date_from = pd.to_datetime(date_from) 

df = load_market_data.load_timeseries(ric, date_from, source)

# PCEPI: PCE Inflation
# PCEPILFE: PCE Core Inflation
# PCETRIM12M159SFRBDAL: Trimmed Mean PCE Inflation Rate
# GDPC1: Real GDP
# GDP: Nominal GDP







