import sys
import iqfeed.dbhist as dbhist
import time as tt
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beCOMPANY.settings")
import beCOMPANY
import beCOMPANY.settings as settings
from main.models import *
import datetime
import psycopg2
import csv
import threading

"""
Created on Tue Mar 08 20:10:29 2016
3 mins - 2150 dp per request
10 mins - 630 datapoints per request
30 mins - 1025 datapoints per request
1 hour - 500 datapoint per request
@author: Hidemi
"""


def    main():
    if len(sys.argv) > 2:
        symbols=[]
        threads = []
        interval=sys.argv[1]
        maxdatapoints=sys.argv[2]
        loop=False
        if len(sys.argv) > 3:
            if sys.argv[3]:
                loop=True
        i=0
        seen=dict()
        with open("../stocks.csv", 'rb') as f:
            reader = csv.reader(f)
            rownum=0
            for row in reader:
                rownum+=1
                i+=1
                if rownum > 1:
                    (symbol,qty,exch)=row
                    seen[symbol]=qty
                    symbols.append(symbol)
                if i > 25:
                    i=0
                    feed_thread = threading.Thread(target=dbhist.get_mult_hist, args=[symbols, interval, maxdatapoints,0,'','','', loop])
                    feed_thread.daemon=True
                    threads.append(feed_thread)
                    symbols=[]
        
        if len(symbols) > 0:
            feed_thread = threading.Thread(target=dbhist.get_mult_hist, args=[symbols, interval, maxdatapoints,0,'','','', loop])
            feed_thread.daemon=True
            threads.append(feed_thread)
        [t.start() for t in threads]
        while 1:
            threads=[]
            try:
                with open("../stocks.csv", 'rb') as f:
                    reader = csv.reader(f)
                    rownum=0
                    symbols=[]
                    for row in reader:
                        rownum+=1
                        i+=1
                        if rownum > 1:
                            (symbol,qty,exch)=row
                            if not seen.has_key(symbol):
                                print 'Found New Symbol, ', symbol
                                seen[symbol]=qty
                                symbols.append(symbol)
                    if len(symbols) > 0:
                        #feed_thread = threading.Thread(target=dbhist.get_mult_hist, args=[symbols, interval, 10000, 0,'','','', False])
                        #feed_thread.daemon=True
                        #threads.append(feed_thread)

                        feed_thread = threading.Thread(target=dbhist.get_mult_hist, args=[symbols, interval, maxdatapoints,0,'','','', loop])
                        feed_thread.daemon=True
                        threads.append(feed_thread)
                [t.start() for t in threads]
                        
                tt.sleep(5)
                print 'History Running',datetime.datetime.now()
            except Exception as e:
                print e
    else:
        print "Usage: get_iqhist.py 300 100"
        
if    __name__    ==    "__main__":
    try:
        main()
    except    KeyboardInterrupt:
        pass
