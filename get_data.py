#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 07:19:01 2017

@author: hidemiasakura
"""

import sys
import time
import requests
import math
import numpy as np
import pandas as pd
import sqlite3
import talib as ta
import os
import json
from pytz import timezone
from os import listdir
from os.path import isfile, join
import datetime
from datetime import datetime as dt
import scripts.iqfeed.dbhist as dbhist
import slackweb
fulltimestamp=datetime.datetime.now().strftime('%Y%m%d_%H_%M_%S')
slackhook='https://hooks.slack.com/services/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'
slack = slackweb.Slack(url=slackhook)
slack_channel="#logs"
# API
# SYM = FrankiesSystem(symbol, get_hist_func)
# SYM.run() - saves signal transmits to broker
c2id = "110064634"
c2key = "aQWcUGsCEMPTUjuogyk8G5qb3pk4XM6IG5iRdgCnKdWLxFVjeF"
typeofsymbol = "stock"
duration = "DAY"
dataPath = './data/'
portfolioPath=dataPath+c2id+'/'
lastDate = datetime.datetime(1000, 1, 1)


def getFeed(symbol, lookback, interval):
    global lastDate
    eastern = timezone('EST5EDT')
    try:
        data = dbhist.get_hist(symbol, interval, lookback).sort_index(ascending=True)
        #data.index=[x.replace(tzinfo=None) for x in data.index.to_pydatetime()]
        data.index=[x.astimezone(eastern) for x in data.index]
        data.index=[x.replace(tzinfo=None) for x in data.index]
        filename=dataPath+symbol+'_hist.csv'
        data.to_csv(filename)
        print 'wrote to', filename
        #print data
        if data.shape[0]<1:
            #print 'return None: last bar', data.index[-1], 'last processed bar', lastDate
            return None
        else:
            #print 'return data: last bar', data.index[-1], 'last processed bar', lastDate
            lastDate = data.index[-1]
            return data
        
    except Exception as e:
        print e
        txt="Feed error: "+str(e)+"\n"
        txt+=symbol+" lb"+str(lookback)+" i"+str(interval)
        slack.notify(text=txt, channel=slack_channel, username="frankenstein", icon_emoji=":rage:")
    


if __name__ == "__main__":
    start_time = time.time()

    mode = 'live'
    symbol = sys.argv[1]
    lookback = int(sys.argv[2])
    interval= int(sys.argv[3])
    data=getFeed(symbol, lookback, interval)
    if data is not None:
        print 'Success!', data.shape[0], 'bars returned'
    # frank.run()
    print 'Elapsed time: ', round(((time.time() - start_time) / 60), 2), ' minutes ', dt.now()
