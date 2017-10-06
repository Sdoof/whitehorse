#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import numpy as np
import pandas.io.data as web
from scipy.stats import norm
from sharpe import dd_stats
import matplotlib.pyplot as plt

def var_cov_var(P, c, mu, sigma):
 #Value at Risk using Var-Cov
 alpha = norm.ppf(1-c, mu, sigma)
 return P-P*(alpha+1)

if __name__ == "__main__":
 start = datetime.datetime(2010,1,1)
 end = datetime.datetime(2014,1,1)
 symbol = 'C'
 ticker = web.DataReader(symbol, 'yahoo', start, end)
 ticker['rets']=ticker['Adj Close'].pct_change()

 P = 1e6
 c = 0.99
 mu = np.mean(ticker['rets'])
 sigma = np.std(ticker['rets'])

 var = var_cov_var(P, c, mu, sigma)
 dds = dd_stats(ticker['rets'])
 fig, newp = plt.subplots()
 newp.plot(dds[6].index, dds[6], label=symbol)
 newp.plot(dds[7].index, dds[7], label='DD')
 plt.legend()
 plt.show()
 print "maxDD(%%):%.2f  maxDD (days):%d avgDD (days):%.1f #DDs:%d avgDD(%%):%.2f" % (dds[1]*100, dds[2], dds[3], dds[4], dds[5]*100)
 print symbol, "%.2f conf Value-at-Risk: $%0.2f" % (c, var)



