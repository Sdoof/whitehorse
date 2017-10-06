#!/usr/bin/python
# -*- coding: utf-8 -*-

# cont_futures.py
import datetime
import numpy as np
import pandas as pd
import Quandl

def futures_rollover_weights(start_date, expiry_date, contracts, rollover_days=5):
 # start date to date of final contract
 dates = pd.date_range(start_date, expiry_dates[-1], freq='B')
 
 #stores multipliers for each contract (0-1)
 roll_weights = pd.DataFrame(np.zeros((len(dates), len(contracts))), index=dates, columns=contracts)
 prev_date= roll_weights.index[0]
 # Loop through each contract and create weightings
 for i, (item, ex_date) in enumerate(expiry_dates.iteritems()):
  if i < len(expiry_dates) -1 :
   roll_weights.ix[prev_date:ex_date - pd.offsets.BDay(), item] =1
   roll_rng = pd.date_range(end=ex_date - pd.offsets.BDay(), periods=rollover_days +1, freq='B')
   decay_weights = np.linspace(0,1, rollover_days+1)
   roll_weights.ix[roll_rng, item]=1-decay_weights
   roll_weights.ix[roll_rng, expiry_dates.index[i+1]]=decay_weights
  else:
   roll_weights.ix[prev_date:, item] =1
  prev_date=ex_date
#print "Roll Weights", roll_weights
 return roll_weights

if __name__ == "__main__":
 try:
  #download the front and back futures contract
  wti_near = Quandl.get("OFDP/FUTURE_CLF2014")
  wti_far = Quandl.get("OFDP/FUTURE_CLG2014")
  wti = pd.DataFrame({'CLF2014':wti_near['Settle'], 'CLG2014':wti_far['Settle']}, index=wti_far.index)
 
  #create dictionary of expiry dates
  expiry_dates = pd.Series({'CLF2014': datetime.datetime(2013, 12, 19), 'CLG2014': datetime.datetime(2013,  2, 21)}).order()

  # obtain weights
  weights = futures_rollover_weights(wti_near.index[0], expiry_dates, wti.columns)
 
  # Construct the continuous futures
  wti_cts = (wti*weights).sum(1).dropna()

  # Output the merged series of contract settle prices
  print wti_cts.tail(60)
  #wti_cts.to_csv('wti_cts.csv')
 except Exception, e:
  print e
