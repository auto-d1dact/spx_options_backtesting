#%% Importing modules
import smtplib
import pandas as pd
import numpy as np
import datetime as dt
import pandas.stats.moments as st
from pandas import ExcelWriter
import matplotlib.pyplot as plt
import os
import quandl as qd
import seaborn as sns

# Function for saving excel files
def save_xls(list_dfs, xls_path, sheet_names):
    writer = ExcelWriter(xls_path)
    for n, df in enumerate(list_dfs):
        df.to_excel(writer, sheet_names[n])
    writer.save()
    return

#%% Reading in Data
# Reading VIX data from CBOE directly
# VIX is stored as 3 separate files on CBOE's website
#   2004 to present : http://www.cboe.com/publish/scheduledtask/mktdata/datahouse/vixcurrent.csv
#   1990 to 2003    : http://www.cboe.com/publish/scheduledtask/mktdata/datahouse/vixarchive.xls
#   1986 to 2003 VXO: http://www.cboe.com/publish/scheduledtask/mktdata/datahouse/vxoarchive.xls

# First read raw files directly 
vix_present = pd.read_csv('http://www.cboe.com/publish/scheduledtask/mktdata/datahouse/vixcurrent.csv').dropna()
# vix_old = pd.read_excel('http://www.cboe.com/publish/scheduledtask/mktdata/datahouse/vixarchive.xls').dropna()
vxo_old = pd.read_excel('http://www.cboe.com/publish/scheduledtask/mktdata/datahouse/vxoarchive.xls').dropna()

# Function for cleaning CBOE VIX data
def clean_cboe(df):
    df.columns = ['Date','Open','High','Low','Close']
    df = df[1:]
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index(pd.DatetimeIndex(df['Date']))
    return df[['Open','High','Low','Close']]

# Applying clean_cboe to vix data
vix_present = clean_cboe(vix_present)
# vix_old = clean_cboe(vix_old)
vxo_old = clean_cboe(vxo_old)

# Currently the vix_old dataframe doesn't have the Open prices so VXO will be used to proxy VIX prior
# to 2003
vix = pd.concat([vxo_old,vix_present],axis = 0)

#%% Reading SKEW Index data directly from CBOE
skew = pd.read_csv('https://www.cboe.com/publish/scheduledtask/mktdata/datahouse/skewdailyprices.csv')
skew.columns = ['Date','Skew','na1','na2']
skew = skew[1:]
skew['Date'] = pd.to_datetime(skew['Date'])
skew = skew.set_index(pd.DatetimeIndex(skew['Date']))[['Skew']]

#%% Reading in SPX Data
os.chdir('C:\\Users\\Fang\\Desktop\\Python Trading\\SPX Option Backtester\\spx_options_backtesting\\SPX Data')
spx = pd.read_csv('SPX.csv')
spx = spx.set_index(pd.DatetimeIndex(spx['Date']))[['Open','High','Low','Close','Adj Close']]
