# SPX Option Backtestings Using CBOE Data
Python Scripts for Backtesting SPX Put Strategies Using Black-Scholes Proxies

The code here will be used to run through historical backtests based on SPX,
VIX, and SKEW index Open and Close prices to proxy a short put strategy.
The goal of this is to test the following questions:
1. When is it better to sell daily, weekly, monthly, or quarterly options?
2. What is an optimal risk-management system, e.g.,
  - Stoploss based on option price
  - Stoploss based on spot index price distance to strike
  - Stoploss based on implied volatility
  - Stoploss based on historical volatility
  - Stoploss based on ratio of IV/HV

*Note that data prior to 1996 for VIX will be proxied by VXO

## Useful links from the CBOE website
http://www.cboe.com/products/vix-index-volatility/vix-options-and-futures/vix-index/vix-historical-data
https://www.cboe.com/products/vix-index-volatility/volatility-indicators/skew
