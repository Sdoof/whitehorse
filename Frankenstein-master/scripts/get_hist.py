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
import ibfeed.get_feed as ibfeed
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
logging.basicConfig(filename='/logs/get_hist.log',level=logging.DEBUG)


def start_feed(symFilter, durationStr, barSizeSetting, whatToShow, minDataPoints):
    
    if durationStr == '1 min':
        threads = []
        feed_thread = threading.Thread(target=ibfeed.get_bar_realtime, args=[ whatToShow, barSizeSetting, symFilter])
        feed_thread.daemon=True
        threads.append(feed_thread)
        [t.start() for t in threads]
    data=ibfeed.get_bar_hist(whatToShow, minDataPoints, durationStr, barSizeSetting, symFilter)
    #[t.join() for t in threads]

if len(sys.argv) > 3:
    symFilter=sys.argv[1]
    interval=sys.argv[2]
    minDataPoints = int(sys.argv[3])
    (durationStr, barSizeSetting,whatToShow)=ibfeed.interval_to_ibhist_duration(interval)
    start_feed(symFilter, durationStr, barSizeSetting, whatToShow, minDataPoints)
else:
    print 'The syntax is: get_hist.py EURAUD 30m 10000'
    exit()
    

