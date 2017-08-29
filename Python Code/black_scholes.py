# Importing modules
import smtplib
import pandas as pd
import datetime as dt
import pandas.stats.moments as st
import matplotlib.pyplot as plt
import os
import quandl as qd
import seaborn as sns
from scipy.stats import norm
from math import *
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

""" # The Black Scholes Formula
# CallPutFlag - This is set to 'c' for call option, anything else for put
# S - Stock price
# K - Strike price
# T - Time to maturity (in days)
# r - Riskfree interest rate
# d - Dividend yield
# v - Volatility (in days)
"""
# Function for black scholes option price
# Set for Puts
def BlackScholes(CallPutFlag,S,K,T,r,d,v):
    d1 = (log(float(S)/K)+((r-d)+v*v/2.)*T)/(v*sqrt(T))
    d2 = d1-v*sqrt(T)
    if CallPutFlag=='c':
        return S*exp(-d*T)*norm.cdf(d1)-K*exp(-r*T)*norm.cdf(d2)
    else:
        return K*exp(-r*T)*norm.cdf(-d2)-S*exp(-d*T)*norm.cdf(-d1)
    
# Function for black scholes greeks
# Set for Puts
def BlackScholes_Greeks(CallPutFlag, S, K, r, v, T, d):
    if CallPutFlag == 'c':
        T_sqrt = sqrt(T)
        d1 = (log(float(S)/K)+((r-d)+v*v/2.)*T)/(v*T_sqrt)
        d2 = d1-v*T_sqrt
        Delta = norm.cdf(d1)
        Gamma = norm.pdf(d1)/(S*v*T_sqrt)
        Theta =- (S*v*norm.pdf(d1))/(2*T_sqrt) - r*K*exp( -r*T)*norm.cdf(d2)
        Vega = S * T_sqrt*norm.pdf(d1)
        Rho = K*T*exp(-r*T)*norm.cdf(d2)
    else:
        T_sqrt = sqrt(T)
        d1 = (log(float(S)/K)+r*T)/(v*T_sqrt) + 0.5*v*T_sqrt
        d2 = d1-(v*T_sqrt)
        Delta = -norm.cdf(-d1)
        Gamma = norm.pdf(d1)/(S*v*T_sqrt)
        Theta = -(S*v*norm.pdf(d1)) / (2*T_sqrt)+ r*K * exp(-r*T) * norm.cdf(-d2)
        Vega = S * T_sqrt * norm.pdf(d1)
        Rho = -K*T*exp(-r*T) * norm.cdf(-d2)
    return Delta, Gamma, Theta, Vega, Rho

