#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 17:58:47 2023

@author: alejandro
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 18:33:11 2023

@author: alejandro
"""



import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as st
import importlib
from statsmodels.tsa.seasonal import seasonal_decompose

import agl_market_data
importlib.reload(agl_market_data)

ric = "AAPL"
from_date = "1/1/2022"

dist = agl_market_data.distribution(ric, from_date, "yearly")
dist.load_timeseries()
dist.plot_timeseries()
dist.compute_stats()
#dist.plot_histogram()

dist2 = agl_market_data.distribution(ric, from_date, "daily")
dist2.load_timeseries()
dist2.plot_timeseries()




