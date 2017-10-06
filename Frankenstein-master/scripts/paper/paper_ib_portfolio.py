import numpy as np
import pandas as pd
import time
import os.path

import json
from pandas.io.json import json_normalize
from signal import get_model_pos
from time import gmtime, strftime, localtime, sleep
import pytz
from pytz import timezone
from datetime import datetime as dt
from tzlocal import get_localzone
import bars as bars
from paper_account import get_account_value, update_account_value
from calc import calc_close_pos, calc_closeVWAP, calc_add_pos, calc_pl
import threading
from dateutil.parser import parse
import datetime
import re

debug=False
lock = threading.Lock()
histcache=dict()
histdates=dict()
def get_ib_portfolio(systemname, type, date):
    filename='./data/paper/ib_' + systemname + '_portfolio.csv'
    
    account=get_account_value(systemname, 'ib', date)
    if os.path.isfile(filename):
        with lock:
            dataSet = pd.read_csv(filename, index_col='symbol')
            if 'PurePL' not in dataSet:
                dataSet['PurePL']=0
            if 'unr_pnl' not in dataSet:
                dataSet['unr_pnl']=0
            if 'pure_unr_pnl' not in dataSet:
                dataSet['pure_unr_pnl']=0
            dataSet=dataSet.reset_index()
            dataSet['symbol']=dataSet['sym']
            if type == 'CASH':
                dataSet['symbol']=dataSet['sym'] + dataSet['currency'] 
                
            dataSet=dataSet.set_index('symbol')
        return (account, dataSet)
    else:

        dataSet=pd.DataFrame({}, columns=['sym','exp','qty','openqty','price','openprice','value','avg_cost','unr_pnl','real_pnl','PurePL','accountid','currency'])
        dataSet['symbol']=dataSet['sym']
        if type == 'CASH':
            dataSet['symbol']=dataSet['sym'] + dataSet['currency']        
        dataSet=dataSet.set_index('symbol')
        with lock:
            dataSet.to_csv(filename)
        return (account, dataSet)
   
def get_ib_pos(systemname, symbol, currency, type, date):
    (account_data, portfolio_data)=get_ib_portfolio(systemname, type, date)
    portfolio_data=portfolio_data.reset_index()
    sym_cur=symbol
    if type == 'CASH':
        portfolio_data['symbol']=portfolio_data['sym'] + portfolio_data['currency']
        sym_cur=symbol + currency
    else:
        portfolio_data['symbol']=portfolio_data['sym']
    
    portfolio_data=portfolio_data.set_index('symbol')
    if sym_cur not in portfolio_data.index.values:
       return 0
    else:
        ib_pos=portfolio_data.loc[sym_cur]
        ib_pos_qty=ib_pos['qty']
        return ib_pos_qty

def update_unr_profit(systemname, pricefeed, currency, type, date):
    filename='./data/paper/ib_' + systemname + '_portfolio.csv'
    (account, dataSet)=get_ib_portfolio(systemname, type, date)
    symbols=dataSet.index
    unr_pnl=0
    pure_unr_pnl=0
    for sym in symbols:
        record=dataSet.ix[sym].copy()
        qty=record['qty']
        openVWAP=record['price']
        (bid,ask)=bars.bidask_from_csv(sym).iloc[-1]
        dtimestamp=time.mktime(parse(date).timetuple())
        if not histcache.has_key(sym):
            if re.search(r'BTC',sym):
                histcache[sym]=bars.feed_ohlc_from_csv(sym)
            else:
                histcache[sym]=bars.feed_ohlc_from_csv('1 min_' + sym)
           
            histdates[sym]=time.mktime(parse(histcache[sym].index[-1]).timetuple())
        if histdates[sym] > dtimestamp:
                ldate=parse(date).strftime("%Y%m%d  %H:%M:00")
                if ldate not in histcache[sym].index:
                    histcache[sym].loc[histcache[sym].index <= ldate].iloc[-1]['Close']
                else:
                    bid=histcache[sym].loc[ldate]['Close']
                    ask=histcache[sym].loc[ldate]['Close']
        quant=qty
        price=ask
        if qty < 0:
            quant = abs(qty)
            price = ask
        else:
            quant = -abs(qty)
            price = bid

        (newVWAP, remqty, commission, buy_power, tradepl, ptValue, newside, purepl) =           \
                calc_close_pos(openVWAP, qty, price, quant,                      \
                pricefeed['Commission_Pct'],pricefeed['Commission_Cash'], record['currency'], \
                pricefeed['IBMult'])
        record['unr_pnl']=tradepl
        record['pure_unr_pnl']=purepl
        unr_pnl=unr_pnl + record['unr_pnl']
        pure_unr_pnl=pure_unr_pnl+record['pure_unr_pnl']
        dataSet.ix[sym]=record
    with lock:
        dataSet.to_csv(filename) 
    return (unr_pnl, pure_unr_pnl)  
    
def update_ib_portfolio(systemname, pos, type, date):
    filename='./data/paper/ib_' + systemname + '_portfolio.csv'
   
    (account, dataSet)=get_ib_portfolio(systemname, type, date)
    
    pos=pos.copy()
    if type == 'CASH':
        pos['symbol']=pos['sym'] + pos['currency']
    else:
        pos['symbol']=pos['sym']
    symbol = pos['symbol']
    pos['qty']=pos['openqty']
    pos['price']=pos['openprice']
    
    if debug:
        print "Update Portfolio: " + str(symbol)

    if float(pos['qty']) != 0:
        
        if symbol in dataSet.index.values:
            dataSet = dataSet[dataSet.index != symbol]
            dataSet=dataSet.reset_index()
            dataSet=dataSet.append(pos)
            dataSet=dataSet.set_index('symbol')
        else:
            dataSet=dataSet.reset_index()
            dataSet=dataSet.append(pos)
            dataSet=dataSet.set_index('symbol')
            
    else:
        dataSet = dataSet[dataSet.index != symbol]
        
    if debug:
        print "Update Portfolio " + systemname + " Qty: " + str(pos['qty']) + \
                        ' symbol: ' + symbol
    with lock: 
        dataSet.to_csv(filename)
    
    account=get_account_value(systemname, 'ib', date)
    return (account, dataSet)
# -*- coding: utf-8 -*-

def get_new_ib_pos(systemname, sym, openVWAP, openqty, buy_power, pl, commission, currency, date):
    
    pos=pd.DataFrame([[sym,'',openqty,openVWAP, openVWAP, buy_power, \
                        commission, 0, pl, 'Paper', \
                        currency,openqty,0]], 
                     columns=['sym','exp','qty','price','openprice','value', \
                     'avg_cost','unr_pnl','real_pnl','accountid', \
                     'currency', 'openqty','PurePL']).iloc[-1]
    return pos