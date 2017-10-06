import numpy as np
import pandas as pd
import time
from os import listdir
from os.path import isfile, join
from swigibpy import EPosixClientSocket, ExecutionFilter, CommissionReport, Execution, Contract
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 08 20:10:29 2016
3 mins - 2150 dp per request
10 mins - 630 datapoints per request
30 mins - 1025 datapoints per request
1 hour - 500 datapoint per request
@author: Hidemi
"""
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
import datetime
import sys
import random
import copy
import pytz
from pytz import timezone
from datetime import datetime as dt
from tzlocal import get_localzone
from sklearn.feature_selection import SelectKBest, chi2, f_regression, RFECV
import os
from dateutil.parser import parse
import logging
import re

sys.path.append("../../")
sys.path.append("../")

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beCOMPANY.settings")
import beCOMPANY
import beCOMPANY.settings as settings
from main.models import *
import datetime

import csv

rtbar={}
rtdict={}
rthist={}
rtfile={}
rtreqid={}
lastdate={}
contract_to_dbcontract_dict=dict()
tickerId=1
systemfile='../data/systems/system_consolidated.csv'
import psycopg2

try:
    dbstr="dbname=" + settings.DATABASES['default']['NAME'] + \
          " user=" + settings.DATABASES['default']['USER'] + \
          " password=" + settings.DATABASES['default']['PASSWORD'] + \
          " host=" + settings.DATABASES['default']['HOST'] + \
          " port=" + settings.DATABASES['default']['PORT']
          
    c=psycopg2.connect(dbstr)
except:
    print "I am unable to connect to the database."
    
    
def get_bidask_list():
    bidask_list=BidAsk.objects.filter(date__gt=datetime.datetime.now()- datetime.timedelta(seconds=60)).order_by('-date')
    seen=dict()
    result=[]
    for bidask in bidask_list:
        if not seen.has_key(str(bidask.instrument_id)):
            seen[bidask.instrument_id]=1
            result.append(bidask.instrument_id)
    return result

    
def get_currencies():
    return get_symbols()




def dbcontract_to_ibcontract(dbcontract):
        symbol=str(dbcontract.sym)
        localSym=str(dbcontract.local_sym)
        if str(dbcontract.secType)=='CASH':
            symbol=str(dbcontract.sym) + str(dbcontract.cur)

        if str(dbcontract.secType)=='FUT':
            year=str(dbcontract.contractMonth)[0:4]
            mon=str(dbcontract.contractMonth)[4:6]
            addSym=''
            print symbol,year,int(mon)
            
            if int(mon) == 1:
                addSym='F'
                print addSym
            if int(mon) == 2:
                addSym='G'
            if int(mon) == 3:
                addSym='H'
            if int(mon) == 4:
                addSym='J'
            if int(mon) == 5:
                addSym='K'
            if int(mon) == 6:
                addSym='M'
            if int(mon) == 7:
                addSym='N'
            if int(mon) == 8:
                addSym='Q'
            if int(mon) == 9:
                addSym='U'
            if int(mon) == 10:
                addSym='V'
            if int(mon) == 11:
                addSym='X'
            if int(mon) == 12:
                addSym='Z'
            addSym+=year[3:4]
            print addSym
            localSym+=addSym
        print 'Found',localSym
        contract=Contract()
        contract.symbol = str(symbol) 
        contract.secType = str(dbcontract.secType)
        contract.exchange = str(dbcontract.exch)
        contract.primaryExchange=str(dbcontract.exch)
        contract.currency = str(dbcontract.cur)
        contract.expiry=str(dbcontract.expiry)
        #contract.strike= # Strike Price
        contract.localSymbol= localSym
        return contract
 
def contract_to_dbcontract(contract):
    return contract_to_dbcontract_dict[contract.localSymbol]
   
def get_contracts():
    symList=dict()
    contract_list=Instrument.objects.filter(broker='ib').order_by('-sym')
    print 'Getting Contracts'
    for dbcontract in contract_list:
        contract=dbcontract_to_ibcontract(dbcontract)
        contract_to_dbcontract_dict[contract.localSymbol]=dbcontract
        symList[contract.localSymbol]=contract
          
    return symList.values()  

def get_contract(sym):
    symList=dict()
    contract_list=Instrument.objects.filter(broker='ib').filter(sym=sym)
    print 'Getting Contract', sym
    for dbcontract in contract_list:
        contract=dbcontract_to_ibcontract(dbcontract)
        contract_to_dbcontract_dict[contract.localSymbol]=dbcontract
        symList[contract.localSymbol]=contract
          
    return symList.values()  

def lookup_contract(symbol):
    contract_list=Instrument.objects.filter(broker='ib').filter(sym=symbol)
    if contract_list and len(contract_list) > 0:
        dbcontract=contract_list[0]
        contract=dbcontract_to_ibcontract(dbcontract)
        contract_to_dbcontract_dict[contract.localSymbol]=dbcontract
        return contract
    else:
        return None
    

def get_cash_contracts():
    symList=dict()
    contract_list=Instrument.objects.filter(broker='ib').filter(secType='CASH')
    for dbcontract in contract_list:
        contract=dbcontract_to_ibcontract(dbcontract)
        symList[contract.localSymbol]=contract
        contract_to_dbcontract_dict[contract.localSymbol]=dbcontract
          
    return symList.values()  

def get_symbols():
    symList=dict()
    contract_list=Instrument.objects.filter(broker='ib')
    for dbcontract in contract_list:
        contract=dbcontract_to_ibcontract(dbcontract)
        symList[contract.localSymbol]=contract
        contract_to_dbcontract_dict[contract.localSymbol]=dbcontract
    return symList.keys()


def create_bars(instrument_ids, frequency):
    try:
        global tickerId
        
        for instrument_id in instrument_ids:
            sql = ' SELECT date, open, high, low, close, volume '
            sql +=' FROM main_feed '
            sql +=' WHERE frequency=%s AND instrument_id=%s ' % (frequency, instrument_id)
            sql +=' ORDER by date DESC '
            data = pd.read_sql(sql, c, index_col='date')
            for i in data.index:
                quote=data.ix[i]
                compress_min_bar(instrument_id, quote, frequency)
    except Exception as e:
        logging.error("create_bars", exc_info=True)

def cache_bar_csv(instrument_id,  frequency):
    global rtbar
    global rtdict
    global rtfile
    global rtreqid
    global tickerId
    if not rtreqid.has_key(instrument_id):
            tickerId=tickerId+1
            reqId=tickerId
            rtdict[reqId]=instrument_id
            rtreqid[instrument_id]=reqId
            
            print 'Caching: ' + instrument_id
    else:
            reqId=rtreqid[instrument_id]
            
    if not rtbar.has_key(reqId):
        
        sql = ' SELECT date, open, high, low, close, volume '
        sql +=' FROM main_feed '
        sql +=' WHERE frequency=%s AND instrument_id=%s ' % (frequency, instrument_id)
        sql +=' ORDER by date DESC limit 1000'
        data = pd.read_sql(sql, c, index_col='date')
            
        rtbar[reqId]=data
    return rtbar[reqId]

def is_bar_date(dateStr, frequency):
        if frequency == '30m':
            if re.search(r'\d\d\d\d\d\d  \d\d:[03]0:00', dateStr):
                return True
        elif frequency == '10m':
            if re.search(r'\d\d\d\d\d\d  \d\d:[012345]0:00', dateStr):
                return True
        elif frequency == '1h':
            if re.search(r'\d\d\d\d\d\d  \d\d:00:00', dateStr):
                return True
        else:
            return True
        return False
        

def compress_min_bar(instrument_id, histData, frequency='30m'):
    try:
        global pricevalue
        global finished
        global rtbar
        global rtdict
        global rtfile
        global rtreqid
        global tickerId
        
        data=cache_bar_csv(instrument_id, frequency)
        reqId=rtreqid[instrument_id]
        
        date=histData['date']
        open=histData['open']
        high=histData['high']
        low=histData['low']
        close=histData['close']
        volume=histData['volume']
        
        eastern=timezone('US/Eastern')
        #timestamp
        date=parse(date).replace(tzinfo=eastern)
        timestamp = time.mktime(date.timetuple())
        if frequency == '30m':
            mins=int(datetime.datetime.fromtimestamp(
                        int(timestamp)
                    ).strftime('%M'))
            if mins < 30:
                #time
                date=datetime.datetime.fromtimestamp(
                            int(timestamp)
                        ).strftime('%Y%m%d  %H:00:00') 
            else:
                 date=datetime.datetime.fromtimestamp(
                            int(timestamp)
                        ).strftime('%Y%m%d  %H:30:00') 
        elif frequency == '10m':
            mins=int(datetime.datetime.fromtimestamp(
                        int(timestamp)
                    ).strftime('%M'))
            if mins < 10:
                #time
                date=datetime.datetime.fromtimestamp(
                            int(timestamp)
                        ).strftime('%Y%m%d  %H:00:00') 
            elif mins < 20:
                #time
                date=datetime.datetime.fromtimestamp(
                            int(timestamp)
                        ).strftime('%Y%m%d  %H:10:00') 
            elif mins < 30:
                #time
                date=datetime.datetime.fromtimestamp(
                            int(timestamp)
                        ).strftime('%Y%m%d  %H:20:00') 
            elif mins < 40:
                #time
                date=datetime.datetime.fromtimestamp(
                            int(timestamp)
                        ).strftime('%Y%m%d  %H:30:00') 
            elif mins < 50:
                #time
                date=datetime.datetime.fromtimestamp(
                            int(timestamp)
                        ).strftime('%Y%m%d  %H:40:00') 
            else:
                 date=datetime.datetime.fromtimestamp(
                            int(timestamp)
                        ).strftime('%Y%m%d  %H:50:00') 
        elif frequency == '1h':
            date=datetime.datetime.fromtimestamp(
                    int(timestamp)
                ).strftime('%Y%m%d  %H:00:00') 
        #time=time.astimezone(eastern).strftime('%Y-%m-%d %H:%M:00') 
        wap=0
        count=data.shape[0]
        if date in data.index:
               
            quote=data.loc[date].copy()
            if high > quote['high']:
                quote['high']=high
            if low < quote['low']:
                quote['low']=low
            quote['close']=close
            quote['volume']=quote['volume'] + volume
            if quote['volume'] < 0:
                quote['volume'] = 0 
            data.loc[date]=quote
            #print "Update Bar: bar: sym: " + sym + " date:" + str(date) + "open: " + str(quote['open']) + " high:"  + str(quote['high']) + ' low:' + str(quote['low']) + ' close: ' + str(quote['close']) + ' volume:' + str(quote['volume']) 
                    
        else:
            if len(data.index) > 1:
                data=data.sort_index()
                quote=data.reset_index().iloc[-1]
                print "close Bar: " + instrument_id + " date:" + str(quote['date']) + " open: " + str(quote['open']) + " high:"  + str(quote['high']) + ' low:' + str(quote['low']) + ' close: ' + str(quote['close']) + ' volume:' + str(quote['volume']) + ' wap:' + str(wap) 
                bar_list=Feed.objects.filter(date=quote['date']).filter(instrument_id=instrument_id).filter(frequency=frequency)
                if bar_list and len(bar_list) > 0:
                    bar=bar_list[0]
                else:
                    bar=Feed()
                    bar.instrument_id=instrument_id
                    bar.frequency=frequency
                    bar.date=quote['date']
                bar.open= quote['open']
                bar.high= quote['high']
                bar.low= quote['low']
                bar.close= quote['close']
                bar.volume= quote['volume']
                bar.save()
                
            print "New Bar:   " + instrument_id + " date:" + str(date) + " open: " + str(open) + " high:"  + str(high) + ' low:' + str(low) + ' close: ' + str(close) + ' volume:' + str(volume) 
            data=data.reset_index().append(pd.DataFrame([[date, open, high, low, close, volume]], columns=['date','open','high','low','close','volume'])).set_index('date')
            
        rtbar[reqId]=data
    except Exception as e:
        logging.error("compress_min_bars", exc_info=True)
        
def get_last_bars(instrument_ids, ylabel, callback):
    global tickerId
    global lastdate
    while 1:
        try:
            
            SST=pd.DataFrame()
            symbols=list()
            returnData=False
            for ticker in instrument_ids:
                instrument_id=ticker
                minFile='../data/bars/'+instrument_id+'.csv'
                symbol = instrument_id
                date=''
                
                if os.path.isfile(minFile):
                    dta=pd.read_csv(minFile)
                    date=dta.iloc[-1]['date']
                    
                    eastern=timezone('US/Eastern')
                    date=parse(date).replace(tzinfo=eastern)
                    timestamp = time.mktime(date.timetuple())
                    #print 'loading',minFile,date,dta[ylabel],'\n'
                    data=pd.DataFrame()
                    data['date']=dta['date']
                    data[symbol]=dta[ylabel]
                    data=data.set_index('date') 
                    
                    
                    
                    if data.shape[0] > 0:
                        if SST.shape[0] < 1:
                            SST=data
                        else:
                            SST = SST.combine_first(data).sort_index()
                            #SST=SST.join(data)
                        
                        if not lastdate.has_key(symbol):
                            returnData=True
                            lastdate[symbol]=timestamp
                            symbols.append(symbol)
                                                   
                        if lastdate[symbol] < timestamp:
                            returnData=True
                            lastdate[symbol]=timestamp
                            symbols.append(symbol)
                        #print 'Shape: ' + str(len(SST.index)) 
                        
            if returnData:
                data=SST.copy()
                data=data.reset_index() #.set_index('date')
                data=data.fillna(method='pad')
                callback(data, symbols)
            time.sleep(20)
        except Exception as e:
            logging.error("get_last_bar", exc_info=True)
            
def get_bar_history(datas, ylabel):
    try:
        SST=pd.DataFrame()
        
        for (filename, ticker, qty) in datas:
            dta=pd.read_csv(filename)
            #symbol=ticker[0:3]
            #currency=ticker[3:6]
            #print 'plot for ticker: ' + currency
            #if ylabel == 'close':
            #    diviser=dta.iloc[0][ylabel]
            #    dta[ylabel]=dta[ylabel] /diviser
                
            #dta[ylabel].plot(label=ticker)   
            data=pd.DataFrame()
            
            data['date']=pd.to_datetime(dta[dta.columns[0]])
            
            data[ticker]=dta[ylabel]
            data=data.set_index('date') 
            if len(SST.index.values) < 2:
                SST=data
            else:
                SST = SST.combine_first(data).sort_index()
        colnames=list()
        for col in SST.columns:
            if col != 'date' and col != 0:
                colnames.append(col)
        data=SST
        data=data.reset_index()        
        data['timestamp']= data['date']
        
        data=data.set_index('date')
        data=data.fillna(method='pad')
        return data
        
    except Exception as e:
        logging.error("something bad happened", exc_info=True)
    return SST
    

def get_bar_start_date(dbcontract, frequency):
    feed_list=Feed.objects.filter(instrument_id=dbcontract.id).filter(frequency=frequency).order_by('date')[:1]
    if feed_list and len(feed_list) > 0:
        return feed_list[0].date
    
def get_bar_end_date(dbcontract, frequency):
    feed_list=Feed.objects.filter(instrument_id=dbcontract.id).filter(frequency=frequency).order_by('-date')[:1]
    if feed_list and len(feed_list > 0):
        return feed_list[0].date

def get_bar_count(dbcontract, frequency, date):
    eastern=timezone('US/Eastern')
    
    date=parse(date).replace(tzinfo=eastern)  
    
    feed_list=Feed.objects.filter(instrument_id=dbcontract.id).filter(frequency=frequency).filter(date__lte=date)
    if feed_list:
        print 'get bar count ',dbcontract.local_sym, ' freq ', frequency, ' date ', date, ' found ', len(feed_list)
        return feed_list.count()
    else:
        return 0
    
def get_bar(dbcontract):
    try:
        global tickerId
        
        sql = ' SELECT date, open, high, low, close, volume, wap '
        sql +=' FROM main_feed '
        sql +=' WHERE frequency=%s AND instrument_id=%s ' % (60, dbcontract.id)
        sql +=' ORDER by date DESC '
        data = pd.read_sql(sql, c, index_col='date')
        return data
    
    except Exception as e:
        logging.error("create_bars", exc_info=True)
        

def feed_ohlc_from_csv(ticker):
    dataSet=pd.read_csv('../data/from_IB/' + ticker  + '.csv', index_col='date')
    return dataSet

def bar_ohlc_from_csv(ticker):
    dataSet=pd.read_csv('../data/bars/' + ticker + '.csv', index_col='date')
    return dataSet

def bidask_to_csv(ticker, date, bid, ask):
    data=pd.DataFrame([[date, bid, ask]], columns=['date','Bid','Ask'])
    data=data.set_index('date')
    data.to_csv('../data/bidask/' + ticker + '.csv')
    return data

def get_ask(ticker):
    data=bidask_from_csv(ticker).iloc[-1]
    return data['Ask']

def get_bid(ticker):
    data=bidask_from_csv(ticker).iloc[-1]
    return data['Bid']
    
def bidask_from_csv(ticker):
    if os.path.isfile('../data/bidask/' + ticker + '.csv'):
        dataSet=pd.read_csv('../data/bidask/' + ticker + '.csv', index_col='date')
        return dataSet
    else:
        return pd.DataFrame([['20160101 01:01:01',-1,-1]], columns=['date','Bid','Ask']).set_index('date')