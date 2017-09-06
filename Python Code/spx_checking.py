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
from scipy.stats import skewnorm as skn
from scipy.stats import norm

# Function for saving excel files
def save_xls(list_dfs, xls_path, sheet_names):
    writer = ExcelWriter(xls_path)
    for n, df in enumerate(list_dfs):
        df.to_excel(writer, sheet_names[n])
    writer.save()
    return

# Reading in Data
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

# Reading SKEW Index data directly from CBOE
skew = pd.read_csv('https://www.cboe.com/publish/scheduledtask/mktdata/datahouse/skewdailyprices.csv')
skew.columns = ['Date','Skew','na1','na2']
skew = skew[1:]
skew['Date'] = pd.to_datetime(skew['Date'])
skew = skew.set_index(pd.DatetimeIndex(skew['Date']))[['Skew']]
skew['skew'] = -(pd.to_numeric(skew['Skew'], downcast='float') - 100)/10
del skew['Skew']

# Reading in SPX Data
os.chdir('C:\\Users\\Fang\\Desktop\\Python Trading\\SPX Option Backtester\\spx_options_backtesting\\SPX Data')
spx = pd.read_csv('SPX.csv')
spx = spx.set_index(pd.DatetimeIndex(spx['Date']))[['Open','High','Low','Close','Adj Close']]


# Joining all index together to one dataframe
spx = spx[['Open','Close']]
spx.columns = ['SPX ' + s for s in spx.columns.tolist()]

vix = vix[['Open','Close']]
vix.columns = ['VIX ' + s for s in vix.columns.tolist()]

#
df = pd.concat([spx,vix,skew],axis = 1).dropna()

# An error in data: 2000-10-18 VIX Close value is a string, converting to float
df['VIX Close'][2714] = 32.5

# Fixing VIX values so that they are floats
df['VIX Close'] = df['VIX Close'].astype('float')
df['VIX Open'] = df['VIX Open'].astype('float')

# Adjusting VIX so that it's on 252 trading days
df['Daily VIX Open'] = np.sqrt(((df['VIX Open']*df['VIX Open'])/365)*1.5)/100
df['Daily VIX Close'] = np.sqrt(((df['VIX Close']*df['VIX Close'])/365)*1.5)/100

# Cleaning up unused dataframes
del skew, spx, vix, vix_present, vxo_old


#%% Creating function to produce the daily x% VaR of SPX

# spx_implied_var: rolling_window, var_pct, mkt_time --> dataframe
#   Function consumes an int, rolling_window, a float,
#   var_pct, and a string, mkt_time, and determines the worst 
#   case return using the skewnorm function and applying
#   VIX as the scaling parameter and SKEW as the shape parameter

def spx_implied_var(rolling_window, var_pct, mkt_time = 'Close'):
        
    if mkt_time == 'Open':
        temp_df = df[['SPX Open','SPX Close','skew',
                      'Daily VIX Open','Daily VIX Close']]
        temp_df['spx_shift'] = temp_df['SPX Close'].shift(-rolling_window)
        temp_df['vix_shift'] = temp_df['Daily VIX Close'].shift(-rolling_window)
        del temp_df['SPX Close'], temp_df['Daily VIX Close']
        temp_df.columns = ['spx','skew','vix','spx_shift','vix_shift']
    else:
        temp_df = df[['SPX Close','skew','Daily VIX Close']]
        temp_df.columns = ['spx','skew','vix']
        temp_df['spx_shift'] = temp_df['spx'].shift(-rolling_window)
        temp_df['vix_shift'] = temp_df['vix'].shift(-rolling_window)
    
    temp_df['period_vix'] = temp_df['vix']*np.sqrt(rolling_window)
    temp_df['var_pct'] = skn.ppf(var_pct, temp_df['skew'], 0, temp_df['period_vix'])
    
    temp_df['var_spx_lvl'] = temp_df['spx']*(1 + temp_df['var_pct'])
    
    return temp_df[['spx','spx_shift','var_pct','var_spx_lvl']]



