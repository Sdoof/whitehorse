#!/usr/bin/python
# -*- coding: utf-8 -*-

import statsmodels.tsa.stattools as ts
from datetime import datetime
from pandas.io.data import DataReader
import pandas as pd
import pandas.io.sql as psql
import MySQLdb as mdb
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



symbol = raw_input("Enter Ticker: ")

#Connect to MySQL
db_host = 'localhost'
db_user = 'sec_user'
db_pass = 'password'
db_name = 'securities_master'
con = mdb.connect(db_host, db_user, db_pass, db_name)

#select all of the historic Google adj close data
sql = "SELECT dp.price_date, dp.adj_close_price FROM symbol AS sym INNER JOIN daily_prices AS dp ON dp.symbol_id = sym.id WHERE sym.ticker = '%s' ORDER BY dp.price_date ASC;" % symbol

ticker = psql.read_sql(sql, con=con, index_col='price_date')
print ticker.head()
print ticker.tail()

#ticker = DataReader(symbol, "yahoo", datetime(2000,1,1), datetime(2013,1,1))


adf = ts.adfuller(ticker['adj_close_price'],1)
#create a GBM, MR, Trending series
gbm = log(cumsum(randn(100000))+1000)
mr = log(randn(100000)+1000)
tr = log(cumsum(randn(100000)+1)+1000)

print ""
print "ADF test for mean reversion"
print "Datapoints", adf[3]
print "p-value", adf[1]
print "Test-Stat", adf[0]
for key in adf[4]:
 print adf[0]<adf[4][key],"Critical Values:",key, adf[4][key],"Test-stat: ",adf[0]
print ""
print "Hurst Exponent"
print "Hurst(GBM): %s" % hurst(gbm)
print "Hurst(MR): %s" % hurst(mr)
print "Hurst(TR): %s" %hurst(tr)

print "Hurst(%s): %s" % (symbol,hurst(ticker['adj_close_price']))

