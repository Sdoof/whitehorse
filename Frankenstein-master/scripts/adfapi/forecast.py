#!/usr/bin/python
#-*- coding: utf-8 -*-

import datetime
import numpy as np
import pandas as pd
import sklearn

from pandas.io.data import DataReader
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.lda import LDA
from sklearn.metrics import confusion_matrix
from sklearn.qda import QDA
from sklearn.svm import LinearSVC, SVC

def create_lagged_series(symbol, start_date, end_date, lags=5):
 """stores % returns of adj_close with a number of lagged returns (5 days). Trading volume, as well as Direction from previous day are included"""
 
 #get info from yahoo
 ts = DataReader(symbol, 'yahoo', start_date-datetime.timedelta(days=365),end_date)
 
 #Create the new lagged DataFrame
 tslag = pd.DataFrame(index=ts.index)
 tslag["Today"] = ts["Adj Close"]
 tslag["Volume"] = ts["Volume"]

 # Create the shifted lag series
 for i in xrange(0, lags):
  tslag["Lag%s" % str(i+1)] = ts["Adj Close"].shift(i+1)

 #Create the returns DataFrame
 tsret = pd.DataFrame(index=tslag.index)
 tsret["Volume"] = tslag["Volume"]
 tsret["Today"] = tslag["Today"].pct_change()*100.0

 #sets any of the zero values to a small number for issues with QDA model
 for i,x in enumerate(tsret["Today"]):
  if (abs(x) < 0.0001):
   tsret["Today"][i] = 0.0001

 #create lagged percentage returns columns
 for i in xrange(0,lags):
  tsret["Lag%s" % str(i+1)] = tslag["Lag%s" % str(i+1)].pct_change()*100.0
 
 #create direction column (+1/-1)
 tsret["Direction"] = np.sign(tsret["Today"])
 tsret = tsret[tsret.index >= start_date]

 return tsret

if __name__ == "__main__":
 #Create lagged series
 snpret = create_lagged_series("^GSPC", datetime.datetime(2001,1,10), datetime.datetime(2005,12,31), lags=5)
 
 #use prior two days of returns as predictor
 X = snpret[["Lag1", "Lag2"]]
 # direction as response
 y = snpret["Direction"]

 # test data is split into two parts, before and after start date
 start_test = datetime.datetime(2005,1,1)

 #create training and test sets
 X_train = X[X.index < start_test]
 X_test = X[X.index >= start_test]
 y_train = y[y.index < start_test]
 y_test = y[y.index >= start_test]

 #create parametrised models
 print "Hit Rates/Confusion Matrices:\n"
 models = [("LR", LogisticRegression()), ("LDA", LDA()), ("QDA", QDA()), ("LSVC", LinearSVC()), ("RSVM", SVC(C=1000000.0, cache_size=200, class_weight=None, coef0=0.0, degree=3, gamma=0.0001, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False)), ("RF", RandomForestClassifier(n_estimators=1000, criterion='gini',max_depth=None, min_samples_split=2, min_samples_leaf=1, max_features='auto', bootstrap=True, oob_score=False, n_jobs=1, random_state=None, verbose=0))]

 #iterate through the models
 for m in models:
  #train each of the models 
  m[1].fit(X_train, y_train)

  #make an array of predictions on test set
  pred = m[1].predict(X_test)

  #output the hit-rate and confusion matrix for each model
  print "%s:\n%0.3f" % (m[0], m[1].score(X_test, y_test))
  print "%s\n" % confusion_matrix(pred, y_test)

