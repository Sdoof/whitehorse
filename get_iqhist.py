import sys
import iqfeed.dbhist as dbhist
import time
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beCOMPANY.settings")
import beCOMPANY
import beCOMPANY.settings as settings
from elasticmodel import *
from dateutil.parser import parse
import psycopg2
import threading
from dateutil.relativedelta import relativedelta
import time
"""
Created on Tue Mar 08 20:10:29 2016
3 mins - 2150 dp per request
10 mins - 630 datapoints per request
30 mins - 1025 datapoints per request
1 hour - 500 datapoint per request
@author: Hidemi
"""

def    main():
    if len(sys.argv) > 3:
        symbol=sys.argv[1]
        interval=sys.argv[2]
        maxdatapoints=sys.argv[3]
        #while 1:
        symbol=symbol.upper()
        instrument_list=Instrument.search().filter('match_phrase',sym=symbol).execute()
        if instrument_list and len(instrument_list) > 0:
            instrument=instrument_list[0]
        else:
            instrument=Instrument()
            instrument.sym=symbol
            instrument.save()
        data=dbhist.get_realtime_hist(symbol, interval, maxdatapoints)
        #data=dbhist.get_hist(symbol, interval, maxdatapoints) #,datadirection=0,requestid='',datapointspersend='',intervaltype=''):
        #time.sleep(5)
    else:
        print "Usage: get_iqhist.py AAPL 60 100"
        
if    __name__    ==    "__main__":
    try:
        main()
    except    KeyboardInterrupt:
        pass
