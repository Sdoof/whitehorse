#!/usr/bin/python

import datetime
import numpy as np
import pandas as pd
import pandas.io.data as web
import urllib2
import matplotlib.pyplot as plt

def dd_stats(returns, N=252):
 #initialize
 eSeries = (returns +1).cumprod()
 eHighSeries = pd.expanding_max(eSeries)
 ddSeriesPer = (eSeries - eHighSeries)/eHighSeries
 maxDD = ddSeriesPer.min()
 ddDays = []
 DDs = []
 count = 0
 ddStart= 0

 # calc dd days
 for i,k in enumerate(eHighSeries):
  if i > 0:
   if eHighSeries[i-1]==eHighSeries[i]: # in DD
    if count ==0: #DD Started
     ddStart = i-1
    count +=1
    if i == len(eHighSeries)-1: #still in drawdown at the end of series
     ddDays.append(count)
     DDs.append(min(ddSeriesPer[ddStart:i]))
   else: #new hwm, DDEnded
    if count != 0:
     ddDays.append(count)
     DDs.append(min(ddSeriesPer[ddStart:i]))
     #ddStart =0
    count =0


 # tick[tick.index == datetime.datetime(2008,11,24)]
 # ddStartDate = datetime.datetime.utcfromtimestamp(returns[i-1:i].index.astype(int)*1e-9)
 return np.sqrt(N) * returns.mean()/abs(maxDD), maxDD, max(ddDays), np.mean(ddDays), len(DDs), np.mean(DDs), eSeries, ddSeriesPer, np.log(eSeries[len(eSeries)-1])-np.log(eSeries[1])

def annualised_sharpe(returns, N=252):
 # N = 252 trading days (daily)
 return np.sqrt(N) * returns.mean()/returns.std()

def annualised_sortino(returns, N=252):
 # N = 252 trading days (daily)
 down = []
 for i in returns:
  if i <0:
   down.append(i)
 return np.sqrt(N) * returns.mean()/np.std(down)

def equity_sharpe(pdf):

 
 #use the percent change method to calculate daily returns
 pdf['daily_ret'] = pdf['Close'].pct_change()

 #assume an average annual risk free rate of 5% over the period
 pdf['excess_daily_ret'] = pdf['daily_ret'] - 0.05/252

 #return the annualised sharpe
 return pdf['excess_daily_ret']

def market_neutral_sharpe(tick, bench):
 #calculates sharpe of a market neutral (long/short) strategy
 #long ticker/ short benchmark

 #calc the % returns on each of the time series
 tick['daily_ret'] = tick['Close'].pct_change()
 bench['daily_ret'] = bench['Close'].pct_change()

 #net returns are (long-short)/2 because there is 2x trading capital
 strat = pd.DataFrame(index=tick.index)
 strat['net_ret'] = (tick['daily_ret'] - bench['daily_ret'])/2.0

 return strat['net_ret']

if __name__ == "__main__":
 start = datetime.datetime(2000,1,1)
 end = datetime.datetime(2013,1,1)
 ticker = 'GOOG'
 benchmark = 'SPY'
 #obtain data
 tick = web.DataReader(ticker, 'google', start, end)
 bench = web.DataReader(benchmark, 'google', start,end)
 a = equity_sharpe(tick)
 b = market_neutral_sharpe(tick,bench)
 ddA = dd_stats(a)
 ddB = dd_stats(b)

 print "Equity Sharpe %.3f, Market Neutral Sharpe %.3f" % (annualised_sharpe(a), annualised_sharpe(b))
 print "To Check: Equity Sortino %.3f, Market Neutral Sortino %.3f" % (annualised_sortino(a), annualised_sortino(b))
 print "Equity annual MAR %.3f, CCR MAR %.3f, CCR %.3f" % (ddA[0], ddA[8]/abs(ddA[1]), ddA[8])
 print "Market Neutral annual MAR %.3f, CCR MAR %.3f, CCR %.3f" % (ddB[0], ddB[8]/abs(ddB[1]), ddB[8])
 #plt.plot(ddA[6]); plt.plot(ddA[7])
 print "Equity maxDD(%%):%.2f  maxDD (days):%d avgDD (days):%.1f #DDs:%d avgDD(%%):%.2f" % (ddA[1]*100, ddA[2], ddA[3], ddA[4], ddA[5]*100)
 #plt.plot(ddB[6]); plt.plot(ddB[7])
 print "Mkt Neutral maxDD(%%):%.2f  maxDD (days):%d avgDD (days):%.1f #DDs:%d avgDD(%%):%.2f" % (ddB[1]*100, ddB[2], ddB[3], ddB[4], ddB[5]*100)
 #new_plot = pd.concat([ddA[6],ddA[7],ddB[6],ddB[7]], axis=1)
 #new_plot.columns = ['Equity', 'Eq DD', 'Mkt Neutral', 'MN DD']
 #new_plot.plot()
 fig, newp = plt.subplots()
 newp.plot(ddA[6].index, ddA[6], label='Equity')
 newp.plot(ddA[7].index, ddA[7], label='Eq DD')
 newp.plot(ddB[6].index, ddB[6], label='Mkt Neutral')
 newp.plot(ddB[7].index, ddB[7], label='MN DD')
 plt.legend()
 plt.show()


