from wrapper_v4 import IBWrapper, IBclient
from swigibpy import Contract 
import time
import pandas as pd
from time import gmtime, strftime, localtime, sleep
import json
import datetime
from pandas.io.json import json_normalize
from pytz import timezone
from datetime import datetime as dt
from tzlocal import get_localzone
import logging
from swigibpy import EPosixClientSocket, ExecutionFilter, CommissionReport, Execution, Contract
import bars
from dateutil.parser import parse
import os
import random
from scripts.ibfeed.bars import contract_to_dbcontract_dict,\
    dbcontract_to_ibcontract

currencyPairsDict=dict()
tickerId=random.randint(100,9999)

callback = IBWrapper()
client=IBclient(callback)

def reconnect_ib():
    global callback
    global client
    client.tws.eDisconnect()
    callback = IBWrapper()
    client=IBclient(callback)

def get_bar(symbol):
    return client.get_bar(str(symbol))
    
def get_ask(symbol):
    global client
    ask=client.get_IBAsk(str(symbol))
    return ask
    
def get_bid(symbol):
    global client
    return client.get_IBBid(str(symbol))
   

def get_contracts():
   return bars.get_contracts()


def get_history(date, contract, whatToShow, dbcontract, tickerId, minDataPoints, durationStr, barSizeSetting):
    symbol= contract.symbol
    currency=contract.currency
    ticker=symbol        
    if contract.secType == 'CASH':
        ticker=symbol+currency
    interval=duration_to_interval(barSizeSetting)
    frequency=interval_to_sec(interval)
    start_date=date
    datacount=bars.get_bar_count(dbcontract, frequency, start_date)
    print 'get_history data count',datacount, ' requesting ', minDataPoints
    if datacount < minDataPoints:
        count=0
        finished=False
        while not finished:    
            dbcontract.frequency=interval_to_sec(interval)
            data = client.get_history(date, contract, whatToShow, dbcontract,tickerId, minDataPoints, durationStr, barSizeSetting)
            datacount=bars.get_bar_count(dbcontract, frequency, start_date)
            if datacount > 0:
                logging.info("Received date: " + str(datacount) + " records out of " + str(minDataPoints) )
                
                date = bars.get_bar_start_date(dbcontract, frequency)
                date=date.strftime("%Y%m%d %H:%M:%S EST")
                time.sleep(30)
                if datacount > int(minDataPoints):
                    finished=True
            else:
                count=count + 1
                if count > 10:
                    finished=True
    else:

        dbcontract.frequency=interval_to_sec(interval)

        data = client.get_history(date, contract, whatToShow, dbcontract,tickerId, minDataPoints, durationStr, barSizeSetting)
        datacount=bars.get_bar_count(dbcontract, frequency, start_date)
        logging.info("Total of " + str(datacount) + " Records")
        date = bars.get_bar_start_date(dbcontract, frequency)
        date=date.strftime("%Y%m%d %H:%M:%S EST")
            
        time.sleep(30)
            
        #set date as last index for next request

    return data
        
def get_TickerId(symbol):
    global tickerId
    global currencyPairsDict
    if not currencyPairsDict.has_key(symbol):
            tickerId=tickerId+1
            currencyPairsDict[symbol] = tickerId
    return currencyPairsDict[symbol]

def get_TickerDict():
    global currencyPairsDict
    return currencyPairsDict
    
def get_bar_bidask(symfilter = ''):
    global tickerId
    if symfilter:
        symbols=bars.get_contract(symfilter)
    else:
        symbols=bars.get_contracts()
    for contract in symbols:
        pair=contract.symbol
        if contract.secType == 'CASH':
            pair=contract.symbol + contract.currency 
        #if len(symfilter) == 0 or pair == symfilter:
        logging.info(  'Subscribing Bid/Ask to ' + pair  )
        eastern=timezone('US/Eastern')
        enddateTime=dt.now(get_localzone())
        date=enddateTime.astimezone(eastern)
        date=date.strftime("%Y%m%d %H:%M:%S EST")
        tickerId=get_TickerId(pair)
        
        global tickerid, client, callback
        dbcontract=bars.contract_to_dbcontract(contract)
        #dbcontract.frequency=frequency
        client.get_IB_market_data(contract, tickerId, dbcontract)
        
        logging.info( 'Done Subscribing to ' + pair  )
    
def get_bar_feed( whatToShow, barSizeSetting, symfilter=''):
    if symfilter:
        symbols=bars.get_contract(symfilter)
    else:
        symbols=bars.get_contracts()
    for contract in symbols:
        pair=contract.symbol
        if contract.secType == 'CASH':
            pair = contract.symbol + contract.currency
        #if len(symfilter) == 0 or pair == symfilter:
        logging.info(  'Subscribing Feed to ' + pair  )
        interval=duration_to_interval(barSizeSetting)
        frequency=interval_to_sec(interval)
        
        tickerId=get_TickerId(pair)          
        
        global tickerid, client, callback
        dbcontract=bars.contract_to_dbcontract(contract)
        dbcontract.frequency=frequency

        client.get_IB_market_data(contract, tickerId,dbcontract)

        logging.info( 'Done Subscribing to ' + pair  )

def get_bar_realtime(whatToShow, barSizeSetting, symfilter=''):
    if symfilter:
        contracts=bars.get_contract(symfilter)
    else:
        contracts=bars.get_contracts()
    
    for contract in contracts:
        pair=contract.localSymbol
        if contract.secType == 'CASH':
            pair = contract.symbol + contract.currency
        #if len(symfilter) == 0 or pair == symfilter:
        logging.info(  'Subscribing Realtime Bar to ' + pair  )
        interval=duration_to_interval(barSizeSetting)
        tickerId=get_TickerId(pair)          
        secs=interval_to_sec(interval)
        dbcontract=bars.contract_to_dbcontract(contract)
        

        global client, callback
        dbcontract.frequency=interval_to_sec(interval)

        client.get_realtimebar(contract, tickerId, whatToShow, dbcontract, secs)


        logging.info( 'Done Subscribing to ' + pair  )

def interval_to_sec(interval):
    if interval== '1 min':
        return 60
    
    elif interval== '30m':
        return 1800
    
    elif interval=='10m':
        return 600
    
    elif interval=='1h':
        return 3600
    
    elif interval=='1d':
        return 86400           
                       
def duration_to_interval(duration):
    if duration == '1 min':
        return '1 min'
    elif duration == '30 mins':
        return '30m'
    elif duration == '10 mins':
        return '10m'
    elif duration == '1 hour':
        return '1h'
    elif duration == '1 day':
        return '1d'
        
def interval_to_ibhist_duration(interval):
    durationStr='1 D'
    barSizeSetting='1 min'
    if interval == '1m':
        durationStr='1 D'
        barSizeSetting='1 min'
    elif interval == '30m':
        durationStr='30 D'
        barSizeSetting='30 mins'
    elif interval == '10m':
        durationStr='10 D'
        barSizeSetting='10 mins'
    elif interval == '1h':
        durationStr='30 D'
        barSizeSetting='1 hour'
    elif interval == '1d':
        durationStr='30 D'
        barSizeSetting='1 hour'
    whatToShow='TRADES'
    return (durationStr, barSizeSetting, whatToShow)


        
def get_bar_date(barSizeSetting, date):
    interval=duration_to_interval(barSizeSetting)
    timestamp = time.mktime(date.timetuple())
    if interval == '1 min':
        date=datetime.datetime.fromtimestamp(
                        int(timestamp)
                    ).strftime('%Y%m%d  %H:%M:00') 
                    
    elif interval == '30m':
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
    elif interval == '10m':
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
    elif interval == '1h':
        date=datetime.datetime.fromtimestamp(
                int(timestamp)
            ).strftime('%Y%m%d  %H:00:00') 
    return date


def get_bar_hist(whatToShow, minDataPoints, durationStr, barSizeSetting, symfilter=''):
    global tickerId
    global currencyPairsDict
    if symfilter:
        symbols=bars.get_contract(symfilter)
    else:
        symbols=bars.get_contracts()
    for contract in symbols:
        print 'Looking up ',symfilter, ' found:',contract.localSymbol
        pair=contract.symbol
        if contract.secType == 'CASH':
            pair = contract.symbol + contract.currency
        #if len(symfilter) == 0 or pair == symfilter:
        logging.info(  'Getting History for ' + pair  )
        interval=duration_to_interval(barSizeSetting)
        
        
        eastern=timezone('US/Eastern')
        enddateTime=dt.now(get_localzone())
        date=enddateTime.astimezone(eastern)
        #date=date.strftime("%Y%m%d %H:%M:%S EST")
        date=get_bar_date(barSizeSetting, date) + ' EST'
        tickerId=get_TickerId(pair)
        
        dbcontract=bars.contract_to_dbcontract(contract)
        dbcontract.frequency=interval_to_sec(interval)

        data=get_history(date, contract, whatToShow, dbcontract, tickerId, minDataPoints, durationStr, barSizeSetting)

        logging.info( 'Done Getting History for ' + pair  )
        if len(symfilter) > 0:
            return data
                
def get_bar_hist_date(date, whatToShow, minDataPoints, durationStr, barSizeSetting, symfilter=''):
    global tickerId
    global currencyPairsDict
    if symfilter:
        symbols=bars.get_contract(symfilter)
    else:
        symbols=bars.get_contracts()
    for contract in symbols:
        pair=contract.symbol
        if contract.secType == 'CASH':
            pair = contract.symbol + contract.currency
        #if len(symfilter) == 0 or pair == symfilter:
        logging.info(  'Getting History for ' + pair  )
        interval=duration_to_interval(barSizeSetting)
        dbcontract=bars.contract_to_dbcontract(contract)
        date=get_bar_date(barSizeSetting, date) + ' EST'
        tickerId=get_TickerId(pair)
        data=get_history(date, contract, whatToShow, dbcontract, tickerId, minDataPoints, durationStr, barSizeSetting)
        logging.info( 'Done Getting History for ' + pair  )
        if len(symfilter) > 0:
            return data
            
def check_bar(barSizeSetting, symfilter=''):
    
    interval=duration_to_interval(barSizeSetting)
    frequency=interval_to_sec(interval)
    try:
        count=0
        if symfilter:
            contracts=bars.get_contract(symfilter)
        else:
            contracts=bars.get_contracts()
        for contract in contracts:
            pair=contract.symbol
            if contract.secType == 'CASH':
                pair = contract.symbol + contract.currency
            #if len(symfilter) == 0 or pair == symfilter:
            dbcontract=bars.contract_to_dbcontract(contract)
            eastern=timezone('US/Eastern')
            nowdate=datetime.datetime.now()
            bardate=bars.get_bar_end_date(dbcontract, frequency)
            if bardate:
                bardate=parse(bardate).replace(tzinfo=eastern)         
            else:
                bardate=datetime.date(2000,1,1)
            #dtimestamp = time.mktime(datadate.timetuple())
            btimestamp = time.mktime(bardate.timetuple())
            timestamp=time.mktime(nowdate.timetuple()) + 3600
            checktime = 3
                
            checktime = checktime * 60
            logging.info(pair + ' Feed Last Received ' + str(round((timestamp - btimestamp)/60, 2)) + ' mins ago')
                
            if timestamp - btimestamp > checktime:
                logging.error(pair + ' Feed not being received for ' + str(round((timestamp - btimestamp)/60, 2))) + ' mins'
                if len(symfilter) > 0:
                    return False
                count = count + 1
        if count > 5:
                return False
        else:
                return True
    except Exception as e:
            logging.error("check_bar", exc_info=True)