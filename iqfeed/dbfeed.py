import sys
import pytz
import datetime
from pytz import timezone
from datetime import datetime as dt
from tzlocal import get_localzone

import json
import time
import pandas as pd
import threading
import sys
import logging
import time
#import websocket
import threading
import dateutil 
#lock = threading.Lock()
import socket   
sys.path.append("../../")
sys.path.append("../")

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beCOMPANY.settings")
import beCOMPANY
import beCOMPANY.settings as settings
from scripts.elasticmodel import *
from dateutil.parser import parse
import psycopg2
import threading
from dateutil.relativedelta import relativedelta
import time
from pandas.io.json import json_normalize

eastern=timezone('US/Eastern')
    
logging.basicConfig(stream=sys.stdout,  level=logging.ERROR)
#logging.basicConfig(filename='/logs/get_hist.log',level=logging.DEBUG)

debug=False
last=dict()
feed={}
ohlc={}
hashist={}
model=pd.DataFrame()

'''
[Symbol] - Required - Max Length 30 characters.
[Interval] - Required - The interval in seconds.
[MaxDatapoints] - Required - The maximum number of datapoints to be retrieved.
[DataDirection] - Optional - '0' (default) for "newest to oldest" or '1' for "oldest to newest".
[RequestID] - Optional - Will be sent back at the start of each line of data returned for this request.
[DatapointsPerSend] - Optional - Specifies the number of datapoints that IQConnect.exe will queue before attempting to send across the socket to your app.
[IntervalType] - Optional - 's' (default) for time intervals in seconds, 'v' for volume intervals, 't' for tick intervals
'''
def get_hist(symbol, interval, maxdatapoints,datadirection=0,requestid='',datapointspersend='',intervaltype=''):
    #get_bitstampfeed()
    global feed
    global ohlc
    
    symbol=symbol.upper()
    instrument_list=Instrument.search().filter('term',**{'sym.raw':symbol}).execute()
    if instrument_list and len(instrument_list) > 0:
        instrument=instrument_list[0]
    else:
        instrument=Instrument()
        instrument.sym=symbol
        instrument.save()
    
    from pandas.io.json import json_normalize
    
    feed_list=Feed.search().filter('term',frequency=interval).filter('term',instrument_id=instrument.id).sort('-date')
    feed_list=feed_list[:int(maxdatapoints)]
    res=[]
    for feed in feed_list:
        #feed.date=eastern.localize(feed.date,is_dst=True)
        date=datetime(feed.date.year,feed.date.month,feed.date.day,feed.date.hour,feed.date.minute,feed.date.second)
        quote={ 'Date':datetime(feed.date.year,feed.date.month,feed.date.day,feed.date.hour,feed.date.minute,feed.date.second),
                                'Open':feed.open,
                                'High':feed.high,
                                'Low':feed.low,
                                'Close':feed.close,
                                'Volume':feed.volume
                            }
        if date <= datetime.now():
            res.append(quote)
    data = json_normalize(res)
    data=data.set_index('Date')
    #data.to_csv('test.csv')
    return data


def bg_get_feed(instrument, symbol, interval, maxdatapoints,datadirection=0,requestid='',datapointspersend='',intervaltype=''):
    try:
        # The IP address or hostname of your reader
        READER_HOSTNAME = 'localhost'
        # The TCP port specified in Speedway Connect
        READER_PORT = 5009
        # Define the size of the buffer that is used to receive data.
        BUFFER_SIZE = 1024
         
        # Open a socket connection to the reader
        s = socket.create_connection((READER_HOSTNAME, READER_PORT))
             
        # Set the socket to non-blocking
        #s.setblocking(0)
         
        # Make a file pointer from the socket, so we can read lines
        fs=s.makefile()
        # Receive data in an infinite loop
        cmd="HIX,%s,%s,%s,%s,%s,%s,%s\r\n" % (symbol, interval, maxdatapoints,datadirection,requestid,datapointspersend,intervaltype)
        s.sendall(cmd);
        
        #data = pd.DataFrame({}, columns=['Date','Open','High','Low','Close','Volume','TotalVolume']).set_index('Date')
        i=0
        while 1:
            try:
                line = fs.readline()
                # If data was received, print it
                if (len(line)):
                    #print line
                    fields=line.strip().split(',')
                    '''
                        Format    Notes
                            Request ID    Text    This field will only exist if the request specified a RequestID. If not specified in the request, the first field in each message will be the Timestamp.
                            Time Stamp    CCYY-MM-DD HH:MM:SS    Example: 2008-09-01 16:00:01
                            High    Decimal    Example: 146.2587
                            Low    Decimal    Example: 145.2587
                            Open    Decimal    Example: 146.2587
                            Close    Decimal    Example: 145.2587
                            Total Volume    Integer    Example: 1285001
                            Period Volume    Integer    Example: 1285
                            Number of Trades    Integer    Example: 10000 - Will be zero for all requests other than tick interval requests
                            Example data:    Request: HIX,GOOG,60,10<CR><LF>
                            2013-08-12 13:44:00,886.0680,886.0680,886.0680,886.0680,1010550,200,0,<CR><LF>
                    '''
                    if fields[0] == '!ENDMSG!':
                        s.close()
                        
                        return data
                    else:
                        #print line
                        date=fields[0]
                        high=float(fields[1])
                        low=float(fields[2])
                        open_price=float(fields[3])
                        close_price=float(fields[4])
                        total_volume=float(fields[5])
                        volume=float(fields[6])
                        trades=fields[7]
                        
                        
                       
                        if date:
                            
                            date=dateutil.parser.parse(date)
                            #date=eastern.localize(date,is_dst=True)
                            #print date
                            quote={ 'Date':date,
                                'Open':open_price,
                                'High':high,
                                'Low':low,
                                'Close':close_price,
                                'Volume':volume,
                                'TotalVolume':total_volume,
                               #'wap':WAP,
                            }
                            #print quote
                            saveQuote(symbol, instrument, interval, quote)
                            #self.saveQuote(dbcontract, quote)
                            
                            data.loc[date] = [open_price,high,low,close_price,volume,total_volume]
                            i+=1
                            #print date,high,low,open,close,volume,total_volume,trades
            except Exception as e:
                logging.error("get_btcfeed", exc_info=True)
                    
        return data
    except Exception as e:
        print e

def get_mult_hist(symbols, interval, maxdatapoints,datadirection=0,requestid='',datapointspersend='',intervaltype=''):
    #get_bitstampfeed()
    global feed
    global ohlc
    
    
    
    bg_get_hist_mult(symbols, interval, maxdatapoints,datadirection,requestid,datapointspersend,intervaltype)
    



def bg_get_hist_mult(symbols, interval, maxdatapoints,datadirection=0,requestid='',datapointspersend='',intervaltype=''):
    #try:
        interval=int(interval)
        
        symstate=dict()
        # The IP address or hostname of your reader
        READER_HOSTNAME = 'localhost'
        # The TCP port specified in Speedway Connect
        READER_PORT = 5009
        # Define the size of the buffer that is used to receive data.
        BUFFER_SIZE = 1024
         
        # Open a socket connection to the reader
        s=None
        while s==None:
            try:
                s = socket.create_connection((READER_HOSTNAME, READER_PORT))
            except Exception as e:
                s=None
        cmd = "S,REQUEST ALL UPDATE FIELDNAMES\r\n";
        s.sendall(cmd);

        cmd = "S,SELECT UPDATE FIELDS,Symbol,Ask,Ask Size,Bid,Bid Size,Total Volume,VWAP,Open,High,Low,Close\r\n";
        s.sendall(cmd)
        
        # Make a file pointer from the socket, so we can read lines
        fs=s.makefile()
        instDict=dict()
        for symbol in symbols:
            symbol=symbol.upper()
            #print 'Getting ', symbol
            symbol=symbol.upper()
            instrument_list=Instrument.search().filter('term',**{'sym.raw':symbol}).execute()
            if instrument_list and len(instrument_list) > 0:
                instrument=instrument_list[0]
                print instrument.id, symbol
            else:
                instrument=Instrument()
                instrument.sym=symbol
                instrument.save()
            instDict[symbol]=instrument
            sym=symbol
            if not symstate.has_key(sym):
                symstate[sym]=dict()
                symstate[sym]['ask']=0
                symstate[sym]['bid']=0
                symstate[sym]['asksize']=0
                symstate[sym]['bidsize']=0
                symstate[sym]['last_total_volume']=0
                symstate[sym]['vwap']=0
                symstate[sym]['total_volume']=0
                symstate[sym]['high']=0
                symstate[sym]['low']=0
            
            '''
            feed_list=Feed.search().filter('term',frequency=interval).filter('term',instrument_id=instrument.id).sort('-date').execute()
            feed=feed_list[0]
            symstate[sym]['startdate']=feed.date
            symstate[sym]['enddate']=feed.date
            symstate[sym]['open']=feed.close
            symstate[sym]['high']=feed.close
            symstate[sym]['low']=feed.close
            symstate[sym]['close']=feed.close
            symstate[sym]['total_volume']=feed.volume
            symstate[sym]['last_total_volume']=feed.volume
            '''
            # Receive data in an infinite loop
            cmd="w%s\r\n" % (symbol)
            s.sendall(cmd);
            
            #data = pd.DataFrame({}, columns=['Date','Open','High','Low','Close','Volume','TotalVolume']).set_index('Date')
            i=0

        datenow=datetime.now()
        min_interval=datenow.minute
        diff=(min_interval * 60) % interval

        while 1:
            #try:
                line = fs.readline()
                #print line
                # If data was received, print it
                if (len(line)):
                    #print line
                    fields=line.strip().split(',')
                    '''
                        Format    Notes
                            Request ID    Text    This field will only exist if the request specified a RequestID. If not specified in the request, the first field in each message will be the Timestamp.
                            Time Stamp    CCYY-MM-DD HH:MM:SS    Example: 2008-09-01 16:00:01
                            High    Decimal    Example: 146.2587
                            Low    Decimal    Example: 145.2587
                            Open    Decimal    Example: 146.2587
                            Close    Decimal    Example: 145.2587
                            Total Volume    Integer    Example: 1285001
                            Period Volume    Integer    Example: 1285
                            Number of Trades    Integer    Example: 10000 - Will be zero for all requests other than tick interval requests
                            Example data:    Request: HIX,GOOG,60,10<CR><LF>
                            2013-08-12 13:44:00,886.0680,886.0680,886.0680,886.0680,1010550,200,0,<CR><LF>
                    '''
                    ''
                    if fields[0] == '!ENDMSG!':
                        #s.close()
                        #time.sleep(1)
                        print 'Done',symbol
                        #return data
                    else:
                        #print line
                        '''
                        Symbol,Ask,Ask Size,Bid,Bid Size,Total Volume,VWAP,
                        Open,High,Low,Close,Most Recent Trade,Most Recent Trade Size,Most Recent Trade Time,Most Recent Trade Market Center,Message Contents,Most Recent Trade Conditions
                        '''
                        

                        if fields[0] == 'T':
                            datenow=parse(fields[1])
                            print 'Timestamp: ', datenow
                            min_interval=datenow.minute
                            diff=(min_interval * 60) % interval
                            for sym in symstate.keys():
                                #print diff, sym, ' '
                                if diff == 0:
                                    date=datetime(datenow.year, datenow.month, datenow.day, datenow.hour, datenow.minute)
                                    if symstate.has_key(sym) and symstate[sym].has_key('ask'):
                                        ask=symstate[sym]['ask']
                                        bid=symstate[sym]['bid']
                                        mid=(ask+bid)/2
                                        total_volume=symstate[sym]['total_volume']
                                        vwap=symstate[sym]['vwap']
                                            
                                        if not symstate[sym].has_key('open'):
                                            
                                            symstate[sym]['enddate']=date
                                            symstate[sym]['startdate']=date
                                            symstate[sym]['last_total_volume']=total_volume
                                            symstate[sym]['open']=mid
                                            symstate[sym]['close']=mid
                                        #print date, symstate[sym]['enddate']
                                        if date > symstate[sym]['enddate']:
                                            diff_sec=date - symstate[sym]['enddate']
                                            diff_sec=diff_sec.total_seconds()
                                            #print diff_sec
                                            if diff_sec >= interval:
                                                    symstate[sym]['date']=date
                                                    symstate[sym]['close']=mid
                                                    #print date
                                                    symstate[sym]['volume']=total_volume - symstate[sym]['last_total_volume']
                                                    if symstate[sym]['volume'] < 0:
                                                        symstate[sym]['volume']=total_volume
                                                    quote={ 'Date':date,
                                                        'Open':symstate[sym]['open'],
                                                        'High':symstate[sym]['high'],
                                                        'Low':symstate[sym]['low'],
                                                        'Close':symstate[sym]['close'],
                                                        'Volume':symstate[sym]['volume'],
                                                        'TotalVolume':symstate[sym]['total_volume'],
                                                       #'wap':WAP,
                                                    }
                                                    #print quote
                                                    tradinghour=False
                                                    if datenow.hour >= 8 and datenow.hour <= 20:
                                                        if quote['Open'] > 0 and quote['Close'] > 0 \
                                                        and quote['High'] > 0 and quote['Low'] > 0:
                                                            tradinghour=True
                                                    if tradinghour:    
                                                        saveQuote(sym.upper(), instDict[sym.upper()], interval, quote)
                                                    else:
                                                        print 'Not Saved: ', sym, quote
                                                        
                                                    symstate[sym]['startdate']=symstate[sym]['enddate']
                                                    symstate[sym]['enddate']=date
                                                    symstate[sym]['last_total_volume']=total_volume
                                                    symstate[sym]['asksize']=0
                                                    symstate[sym]['bidsize']=0
                                                    symstate[sym]['open']=symstate[sym]['close']
                                                    symstate[sym]['high']=symstate[sym]['close']
                                                    symstate[sym]['low']=symstate[sym]['close']
                                                    
                                
                        if fields[0] == 'Q':
                            sym=fields[1]
                            ask=0
                            asksize=0
                            bid=0
                            bidsize=0
                            total_volume=0
                            vwap=0
                            open_price=0
                            high=0
                            low=0
                            close_price=0
                            if fields[2]:
                                ask=float(fields[2])
                            if fields[3]:
                                asksize=float(fields[3])
                            if fields[4]:
                                bid=float(fields[4])
                            if fields[5]:
                                bidsize=float(fields[5])
                            if fields[6]:
                                total_volume=float(fields[6])
                            if fields[7]:
                                vwap=float(fields[7])
                            if fields[8]:
                                open_price=float(fields[8])
                            if fields[9]:
                                high=float(fields[9])
                            if fields[10]:
                                low=float(fields[10])
                            if fields[11]:
                                close_price=float(fields[11])

                            
                            if not symstate.has_key(sym):
                                symstate[sym]=dict()
                                symstate[sym]['asksize']=0
                                symstate[sym]['bidsize']=0
                                symstate[sym]['last_total_volume']=total_volume
                                
                            if ask:
                                symstate[sym]['ask']=ask
                            if bid:
                                symstate[sym]['bid']=bid
                            if vwap:
                                symstate[sym]['vwap']=vwap
                            if total_volume:
                                symstate[sym]['total_volume']=total_volume
                                
                            if symstate.has_key(sym):
                                if not ask and symstate[sym].has_key('ask'):
                                    ask=symstate[sym]['ask']
                                if not bid and symstate[sym].has_key('bid'):
                                    bid=symstate[sym]['bid']
                                if ask and bid and ask > 0 and bid > 0:
                                    mid=(ask+bid)/2
                                    if not symstate[sym].has_key('high') or mid > symstate[sym]['high']:
                                        symstate[sym]['high']=mid
                                    if not symstate[sym].has_key('low') or (symstate[sym]['low'] > 0 and mid < symstate[sym]['low']):
                                        symstate[sym]['low']=mid
                                if asksize:
                                    symstate[sym]['asksize']+=asksize
                                if bidsize:
                                    symstate[sym]['bidsize']+=bidsize
                                if vwap:
                                    symstate[sym]['vwap']=vwap
                                if total_volume:
                                    symstate[sym]['total_volume']=total_volume
                                
                                
            #except Exception as e:
            #        logging.error("get_btcfeed", exc_info=True)
                    
    
    #except Exception as e:
    #    print e
def saveQuote(symbol, instrument, interval, quote):
        #if quote.has_key('wap'):
        #    print ' wap:' + str(quote['wap']) 
        
        frequency=interval
        
        
        date=quote['Date'] # .replace(tzinfo=eastern) - relativedelta(minutes=1) 
        #date=eastern.localize(date,is_dst=True)
                                                    
        bar_list=Feed.search().filter('term',date=date).filter('term',instrument_id=instrument.id).filter('term',frequency=frequency).execute()
        #print "close Bar: " + str(dbcontract.id) + " freq ",dbcontract.frequency, " date:" + str(quote['date']) + "date ",date, " open: " + str(quote['open']) + " high:"  + str(quote['high']) + ' low:' + str(quote['low']) + ' close: ' + str(quote['close']) + ' volume:' + str(quote['volume']) 
        print 'New Bar: ', symbol,  quote
        if bar_list and len(bar_list) > 0:
            bar=bar_list[0]
            #print "found bar id",bar.id
        else:
            bar=Feed()
            bar.instrument_id=instrument.id
            bar.frequency=frequency
            bar.date=date
        bar.open= quote['Open']
        bar.high= quote['High']
        bar.low= quote['Low']
        bar.close= quote['Close']
        bar.volume= quote['Volume']
        if quote.has_key('VWAP'):
            bar.wap=quote['VWAP']
        bar.save()
        
        with open('logs\\' + symbol + '_feed.csv', 'a') as outfile:
            log= "%s,%s,%s,%s,%s,%s,%s\r\n" % (date, symbol, str(quote['Open']), str(quote['High']),str(quote['Low']),str(quote['Close']),str(quote['Volume']))
            print 'logging ',symbol
            outfile.write(log)
        outfile.close()

def    main():
    if len(sys.argv) > 3:
        symbol=sys.argv[1]
        interval=sys.argv[2]
        maxdatapoints=sys.argv[3]
        data=get_hist(symbol, interval, maxdatapoints) #,datadirection=0,requestid='',datapointspersend='',intervaltype=''):
    else:
        print "Usage: dbhist.py AAPL 60 100"
        
if    __name__    ==    "__main__":
    try:
        main()
    except    KeyboardInterrupt:
        pass

        
