#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import pandas.io.data as web
import pprint
import statsmodels.tsa.stattools as ts
from pandas.stats.api import ols
from numpy import cumsum, log, polyfit, sqrt, std, subtract
from numpy.random import randn

def hurst(ts):
 #create range of lag values
 lags = range(2,100)
 #calculate the array of the variances of the lagged differences
 tau = [sqrt(std(subtract(ts[lag:], ts[:-lag]))) for lag in lags]
 #use a linear fit to estimate the hurt exponent
 poly = polyfit(log(lags), log(tau),1)
 #return the hurst exponent from the polyfit output
 return poly[0]*2.0

def plot_price_series(df, ts1, ts2, start, end):
 months = mdates.MonthLocator() # every month
 fig, ax = plt.subplots()
 ax.plot(df.index, df[ts1], label=ts1)
 ax.plot(df.index, df[ts2], label=ts2)
 ax.xaxis.set_major_locator(months)
 ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
 ax.set_xlim(start, end)
 ax.grid(True)
 fig.autofmt_xdate()

 plt.xlabel('Month/Year')
 plt.ylabel('Price ($)')
 plt.title('%s and %s Daily Prices' % (ts1, ts2))
 plt.legend()
 plt.show()

def plot_scatter_series(df, ts1, ts2):
 plt.xlabel('%s Price ($)' % ts1)
 plt.ylabel('%s Price ($)' % ts2)
 plt.title('%s and %s Price Scatterplot' % (ts1, ts2))
 plt.scatter(df[ts1], df[ts2])
 plt.show()

def plot_residuals(df,start,end):
 months = mdates.MonthLocator()
 fig, ax = plt.subplots()
 ax.plot(df.index, df["res"], label='Residuals')
 ax.xaxis.set_major_locator(months)
 ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
 ax.set_xlim(start,end)
 ax.grid(True)
 fig.autofmt_xdate()

 plt.xlabel('Month/Year')
 plt.ylabel('Price ($)')
 plt.title('Residual Plot')
 plt.legend()
 plt.plot(df['res'])
 plt.show()

def print_coint(adf, hurst):
 #create a GBM, MR, Trending series
 #gbm = log(cumsum(randn(100000))+1000)
 #mr = log(randn(100000)+1000)
 #tr = log(cumsum(randn(100000)+1)+1000)

 print ""
 print "ADF test for mean reversion"
 print "Datapoints", adf[3]
 print "p-value", adf[1]
 print "Test-Stat", adf[0]
 for key in adf[4]:
  print adf[0]<adf[4][key],"Critical Values:",key, adf[4][key],"Test-stat: ",adf[0]
 print ""
 print "Hurst Exponent"
 print "Hurst(GBM): %s Hurst(MR): %s Hurst(TREND): %s" % (.50,0,1)
 print "Hurst(Resid): %s" % (hurst)



if __name__ == "__main__":
 start = raw_input("Enter Start_date: ")
 end = raw_input("Enter End_date: ")
 if start =="":
  start = datetime.datetime(2012,1,1)
  print start
 if end =="":
  end = datetime.date.today()
  print end

 symbol1 = raw_input("Enter Ticker1: ")
 symbol2 = raw_input("Enter Ticker2: ")
 if symbol1 == "":
  symbol1 = "AREX"
  print symbol1
 if symbol2 =="":
  symbol2 ="WLL"
  print symbol2

 ticker1 = web.DataReader(symbol1, "yahoo", start, end)
 ticker2 = web.DataReader(symbol2, "yahoo", start, end)

 df = pd.DataFrame(index=ticker1.index)
 df[symbol1] = ticker1["Adj Close"]
 df[symbol2] = ticker2["Adj Close"]

 #plot the two time series
 plot_price_series(df, symbol1, symbol2, start, end)

 #display scatterplot
 plot_scatter_series(df, symbol1, symbol2)

 #calculate optimal hedge ratio "beta"
 res = ols(y=df[symbol2], x=df[symbol1])
 beta_hr = res.beta.x

 #calc resid of linear combo
 df['res']=df[symbol2]-beta_hr*df[symbol1]

 #plot residuals
 plot_residuals(df,start,end)

 #calc and output the coint ADF test on the resids
 cadf = ts.adfuller(df['res'])
 churst = hurst(df['res'])
 print_coint(cadf,churst)
