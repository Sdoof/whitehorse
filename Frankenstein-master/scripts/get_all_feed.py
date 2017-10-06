import numpy as np
import pandas as pd# -*- coding: utf-8 -*- 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from django.db import models

sys.path.append("../")

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beCOMPANY.settings")
import beCOMPANY
import beCOMPANY.settings as bsettings
from main.models import *
import datetime

import time
import ibfeed.get_feed as feed
import time
import os
import logging
import threading
import sys

"""
Created on Tue Mar 08 20:10:29 2016
3 mins - 2150 dp per request
10 mins - 630 datapoints per request
30 mins - 1025 datapoints per request
1 hour - 500 datapoint per request
@author: Hidemi
"""
""
logging.basicConfig(filename='/logs/get_feed_1m.log',level=logging.DEBUG)

minDataPoints = 10000
durationStr='1 D'
barSizeSetting='1 min'
whatToShow='TRADES'

def get_ibfeed(contract, tickerId):
    feed.get_feed(contract, tickerId)

        
def check_bar(symFilter):
    finished=False
    time.sleep(120)
    while not finished:
        try:
            has_feed=feed.check_bar(barSizeSetting,symFilter)
            if not has_feed:
                logging.error('Feed not being received - restarting')
                feed.reconnect_ib()
                start_feed()
                time.sleep(120)
            time.sleep(30)
        except Exception as e:
            logging.error("check_bar", exc_info=True)
            
def start_feed(symFilter):
    #feed.cache_bar_csv(dataPath, barSizeSetting)
    
    threads = []
    feed_thread = threading.Thread(target=feed.get_bar_feed, args=[whatToShow, barSizeSetting,symFilter])
    feed_thread.daemon=True
    threads.append(feed_thread)
    
    #hist_thread = threading.Thread(target=feed.get_bar_hist, args=[whatToShow, minDataPoints, durationStr, barSizeSetting,symFilter])
    #hist_thread.daemon=True
    #threads.append(hist_thread)
    
    [t.start() for t in threads]
    #[t.join() for t in threads]
contracts=feed.get_contracts()

for contract in contracts:
    symFilter=contract.symbol
    start_feed(symFilter)
    time.sleep(10)

    

