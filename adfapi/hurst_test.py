#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
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

#create a GBM, MR, Trending series
gbm = log(cumsum(randn(100000))+1000)
mr = log(randn(100000)+1000)
tr = log(cumsum(randn(100000)+1)+1000)

print "Hurst(GBM): %s" % hurst(gbm)
print "Hurst(MR): %s" % hurst(mr)
print "Hurst(TR): %s" %hurst(tr)

wti = pd.io.parsers.read_csv('./wti_cts.csv')
print "Hurst(WTI): %s" % hurst(wti['81.71'])
#print "Hurst(GOOG): %s" % hurst(goog['Adj Close'])

