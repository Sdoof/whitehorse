import sys
import time
import math
import numpy as np
import pandas as pd
import sqlite3
import talib as ta
import os
from os import listdir
from os.path import isfile, join
import datetime
from datetime import datetime as dt

#API
#SYM = FrankiesSystem(symbol, get_hist_func)
#SYM.run() - saves signal transmits to broker

dataPath='./data/'
def getBackendDB():
    dbPath = 'stocks.sqlite3'
    readConn = sqlite3.connect(dbPath)
    return readConn


def getFeed(symbol, lookback, interval):
    global lastDate

    data=dbhist.get_hist(symbol, interval, lookback).sort_index(ascending=True)
    print 'last bar', data.index[-1], 'last processed bar', lastDate
    if data.index[-1] > lastDate:
        lastDate=data.index[-1]
        return data
    else:
        return None

def getFeedHistory(symbol, maxlookback,interval):
    #global lastDate
    historylength=maxlookback*2

    data=dbhist.get_hist(symbol, interval, historylength).sort_index(ascending=True)
    print data
    #if data.index[-1] > lastDate:
    #    lastDate=data.index[-1]
    #return data
    '''
    global dataPath
    #richie you do this
    filename=dataPath+symbol+'.csv'
    data = pd.read_csv(filename)
    data.Date=pd.to_datetime(data.Date)
    data=data.set_index('Date')
    #print data.columns
    data.columns=['Open','High','Low','Close','Volume']
    '''
    #print data.columns
    #for col in data.columns:
    #    data[col]=data[col].astype(float)
    filename = dataPath + symbol + '_signals.csv'
    if isfile(filename):
        os.remove(filename)
        print(filename+" Removed!")
    for i,j in enumerate(range(maxlookback,data.shape[0])):
        yield data.iloc[i:j]

def getHistory(symbol, maxlookback):
    global dataPath
    #richie you do this
    filename=dataPath+symbol+'.csv'
    data = pd.read_csv(filename)
    data.Date=pd.to_datetime(data.Date)
    data=data.set_index('Date')
    #print data.columns
    data.columns=['Open','High','Low','Close','Volume']
    #print data.columns
    for col in data.columns:
        data[col]=data[col].astype(float)
    filename = dataPath + symbol + '_signals.csv'
    if isfile(filename):
        os.remove(filename)
        print(filename+" Removed!")
    for i,j in enumerate(range(maxlookback,data.shape[0])):
        yield data.iloc[i:j]


def place_order(action, quant, sym, type, systemid, apikey, parentsig=None):
    url = 'https://collective2.com/world/apiv2/submitSignal'
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    parentsig = "" if parentsig == None else parentsig
    data = {
        "apikey": apikey,  # "tXFaL4E6apdfmLtGasIovtGnUDXH_CQso7uBpOCUDYGVcm1w0w",
        "systemid": systemid,
        "signal": {
            "action": action,
            "quant": quant,
            "symbol": sym,
            "typeofsymbol": type,
            "market": 1,  # "limit": 31.05,
            "duration": "DAY",
            "signalid": "",
            "conditionalupon": parentsig
        }
    }
    params = {}
    r = requests.post(url, params=params, json=data);
    # sleep(2)
    print r.text
    #logging.info(str(r.text))
    return r.json()['signalid']

class Frankenstein():
    #i'll do this
    global dataPath
    def __init__(self, symbol, feed, ema_lookback=9, vwap_lookback=102):
        self.symbol = symbol
        self.ema_lookback=ema_lookback
        self.vwap_lookback = ema_lookback
        self.maxlookback = max(ema_lookback, vwap_lookback)
        self.feed = feed(symbol, self.maxlookback)
        self.dbConn=getBackendDB()
        self.signal_filename=dataPath+self.symbol+'_signals.csv'

    def check(self):
        #print 'lookback', self.maxlookback
        data=self.feed.next().copy()


        print 'last',data.iloc[-1].name
        #print dir(self)
        if 'signals' in dir(self):
            #later data requests
            data= self.signals.append(data.iloc[-1]).iloc[-self.ema_lookback:].copy()
            #print data.iloc[-self.ema_lookback:]
            #print data

            #data = data.dropna()
            #print data
            self.lastdata=data
            lastbar=self.lastbar=data.iloc[-1]
            #print lastbar
            #print ta.EMA(data.Close.values, timeperiod=self.ema_lookback)
            lastbar['EMA'] = ta.EMA(data.Close.values, timeperiod=self.ema_lookback)[-1]
            if lastbar.name.minute == 35 and lastbar.name.hour ==9:
                #print lastbar
                lastbar['VP'] = (lastbar.High + lastbar.Low + lastbar.Close) / 3 * lastbar.Volume
                lastbar['TotalVP'] = lastbar['VP']
                lastbar['TotalVolume'] =lastbar['Volume']
                lastbar['VWAP'] = lastbar.TotalVP / lastbar.TotalVolume
                lastbar['EMA>VWAP'] = np.where(lastbar.EMA > lastbar.VWAP, 1, -1)
                #print lastbar
            else:

                lastbar['VP'] = (lastbar.High + lastbar.Low + lastbar.Close) / 3 * lastbar.Volume
                lastbar['TotalVP'] = data.iloc[-2].TotalVP+lastbar['VP']
                lastbar['TotalVolume'] = data.iloc[-2].TotalVolume+lastbar['Volume']
                lastbar['VWAP'] = lastbar.TotalVP / lastbar.TotalVolume
                lastbar['EMA>VWAP'] = np.where(lastbar.EMA > lastbar.VWAP, 1, -1)
            #print lastbar
            self.signals=self.signals.append(lastbar)
        else:
            #first data request
            data['EMA'] = ta.EMA(data.Close.values, timeperiod=self.ema_lookback)
            start_idx = [(i, date) for i, date in enumerate(data.index) \
                         if date.minute == 35 and date.hour == 9]
            bars_from_new_day = data.iloc[start_idx[-1][0]:].shape[0]
            #print len(data), start_idx[-1], 'bars from new day', bars_from_new_day

            if len(start_idx) == 0:
                # print data.to_csv(dataPath+'startidx0.csv')
                print 'no start_idx found!'
                sys.exit()

            data = data.iloc[start_idx[-1][0]:]
            #data = data.dropna()
            #self.data=data
            #print data.High.values + data.Low.values + data.Close.values
            data['VP'] = (data.High + data.Low + data.Close) / 3 * data.Volume
            data['TotalVP'] = data.VP.cumsum()
            data['TotalVolume'] = data.Volume.cumsum()
            data['VWAP'] = data.TotalVP / data.TotalVolume
            data['EMA>VWAP'] = np.where(data.EMA > data.VWAP, 1, -1)
            self.signals=data.copy()
            self.lastbar = data.iloc[-1]

        signal_change = False
        if signal_change:
            self.transmit()

    def transmit(self):
        print 'transmitting signal to broker'

    def run(self):
        while True:
            try:
                self.check()
            except StopIteration:
                print 'EOF'
                break
        self.lastdata.to_csv(dataPath + self.symbol + '_last.csv')
        self.signals.to_csv(self.signal_filename, index=True)

if __name__ == "__main__":

    if len(sys.argv) == 1:
        #filename = '5m_#TeslaMotor.csv'
        symbol = 'TSLA'
    else:
        symbol = sys.argv[1]
    start_time = time.time()
    frank = Frankenstein(symbol, getHistory)
    # frank = Frankenstein('TSLA', getFeed)
    frank.run()
    print 'Elapsed time: ', round(((time.time() - start_time) / 60), 2), ' minutes ', dt.now()


