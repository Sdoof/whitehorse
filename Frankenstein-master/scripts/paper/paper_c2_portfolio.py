import numpy as np
import pandas as pd
import time
import os.path
from dateutil.parser import parse
import json
from pandas.io.json import json_normalize
from signal import get_model_pos
from time import gmtime, strftime, localtime, sleep
import pytz
from pytz import timezone
from datetime import datetime as dt
from tzlocal import get_localzone
import bars as bars
import datetime
from paper_account import get_account_value, update_account_value
from calc import calc_close_pos, calc_closeVWAP, calc_add_pos, calc_pl
from paper_c2_trades import get_c2_trades
import threading
import logging
import re

debug=False
debug2=False
lock = threading.Lock()
histcache=dict()
histdates=dict()
def get_c2_portfolio(systemname, date):
    filename='./data/paper/c2_' + systemname + '_portfolio.csv'
    
    account=get_account_value(systemname, 'c2', date)
    
    if os.path.isfile(filename):
        with lock:
            dataSet = pd.read_csv(filename, index_col='symbol')
            if 'PurePL' not in dataSet:
                dataSet['PurePL']=0
            if 'unr_pnl' not in dataSet:
                dataSet['unr_pnl']=0
            if 'pure_unr_pnl' not in dataSet:
                dataSet['pure_unr_pnl']=0
        return (account, dataSet)
        
    else:
        dataSet=pd.DataFrame({},columns=['symbol','open_or_closed','long_or_short','quant_opened', 'quant_closed', \
                     'opening_price_VWAP', 'closing_price_VWAP', 'PL', 'PurePL', 'commission', \
                     'trade_id','closeVWAP_timestamp','closedWhen','closedWhenUnixTimeStamp', \
                     'expir','instrument',\
                     'markToMarket_time','openVWAP_timestamp','openedWhen','qty','currency'])
        dataSet = dataSet.set_index('symbol')
        with lock:
            dataSet.to_csv(filename)
        return (account, dataSet)

    
def get_c2_pos(systemname, c2sym, date):
    
    (account_data, portfolio_data)=get_c2_portfolio(systemname, date)
    portfolio_data=portfolio_data.reset_index()
    sym_cur=c2sym
    portfolio_data=portfolio_data.set_index('symbol')
    if sym_cur not in portfolio_data.index.values:
       return 0
    else:
        c2_pos=portfolio_data.loc[sym_cur]
        c2_pos_qty=float(c2_pos['quant_opened']) - float(c2_pos['quant_closed'])
        c2_pos_side=str(c2_pos['long_or_short'])
        if c2_pos_side == 'short':
            c2_pos_qty=-abs(c2_pos_qty)
        return c2_pos_qty

def get_new_c2_pos(systemname, sym, side, openVWAP, openqty, pl, commission, ptValue, date):
    trade_id=0
    trades=get_c2_trades(systemname, date)
    if len(trades.index.values) > 0:
        trade_id=int(max(trades.index.values))
    trade_id=int(trade_id) + 1
    
    if debug:
        print "Trade ID:" + str(trade_id)
            
    pos=pd.DataFrame([[sym, 'open',side, abs(openqty), 0, \
                        openVWAP, 0, 0, 0, commission, \
                        trade_id, '','','', \
                        '',sym, \
                        '',date,date,openqty]]
            ,columns=['symbol','open_or_closed','long_or_short','quant_opened', 'quant_closed', \
                     'opening_price_VWAP', 'closing_price_VWAP', 'PL', 'PurePL', 'commission', \
                     'trade_id','closeVWAP_timestamp','closedWhen','closedWhenUnixTimeStamp', \
                     'expir','instrument',\
                     'markToMarket_time','openVWAP_timestamp','openedWhen','qty']).iloc[-1]
    return pos

def update_unr_profit(systemname, pricefeed, currency, date):
    print pricefeed
    filename='./data/paper/c2_' + systemname + '_portfolio.csv'
    (account, dataSet)=get_c2_portfolio(systemname, date)
    symbols=dataSet.index
    unr_pnl=0
    pure_unr_pnl=0
    for sym in symbols:
        record=dataSet.ix[sym].copy()
        qty=record['quant_opened'] - record['quant_closed']
        openVWAP=record['opening_price_VWAP']
        (bid,ask)=bars.bidask_from_csv(sym).iloc[-1]
        dtimestamp=time.mktime(parse(date).timetuple())
        if not histcache.has_key(sym):
            if re.search(r'BTC',sym):
                histcache[sym]=bars.feed_ohlc_from_csv(sym)
            else:
                histcache[sym]=bars.feed_ohlc_from_csv('1 min_' + sym)
            histdates[sym]=time.mktime(parse(histcache[sym].index[-1]).timetuple())
        if histdates[sym] > dtimestamp:
                #logging.info('unr profit using hist: ' + sym)
                ldate=parse(date).strftime("%Y%m%d  %H:%M:00")
                if ldate not in histcache[sym].index:
                    histcache[sym].loc[histcache[sym].index <= ldate].iloc[-1]['Close']
                else:
                    bid=histcache[sym].loc[ldate]['Close']
                    ask=histcache[sym].loc[ldate]['Close']
        quant=qty
        price=ask
        if record['long_or_short'] == 'short':
            quant = abs(qty)
            price = ask
        else:
            quant = -abs(qty)
            price = bid

        (newVWAP, remqty, commission, buy_power, tradepl, ptValue, newside, purepl) =           \
                calc_close_pos(openVWAP, qty, price, quant,                      \
                pricefeed['Commission_Pct'],pricefeed['Commission_Cash'], record['currency'], \
                pricefeed['C2Mult'])
        record['unr_pnl']=tradepl
        record['pure_unr_pnl']=purepl
        unr_pnl=unr_pnl + record['unr_pnl']
        pure_unr_pnl=pure_unr_pnl+record['pure_unr_pnl']
        dataSet.ix[sym]=record
    with lock:
        dataSet.to_csv(filename) 
    return (unr_pnl, pure_unr_pnl)        
          
def update_c2_portfolio(systemname, pos, tradepl, purepl, buy_power, date):
    filename='./data/paper/c2_' + systemname + '_portfolio.csv'
    (account, dataSet)=get_c2_portfolio(systemname, date)

    pos=pos.copy()
    symbol=pos['symbol']
    
    pos['balance']=account['balance'] + tradepl
    pos['purebalance']=account['purebalance'] + purepl
    pos['margin_available']=account['buy_power'] + buy_power
    pos['PurePL']=float(pos['PurePL']) + purepl
    pos['PL']=float(pos['PL']) + float(tradepl)
    
    if debug2:
         print 'C2 Symbol: ' + pos['symbol'] + ' PurePL: ' + str(pos['PurePL']) + ' From Portfolio'
         
    if debug:
        print "Update Portfolio: " + str(symbol)
        
    if abs(pos['quant_opened']) > abs(pos['quant_closed']):
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
        print "Update Portfolio " + systemname + " " + pos['long_or_short'] + \
                        ' symbol: ' + pos['symbol'] + ' open_or_closed ' + pos['open_or_closed'] + \
                        ' opened: ' + str(pos['quant_opened']) + ' closed: ' + str(pos['quant_closed'])
    with lock:
        dataSet.to_csv(filename)
    return dataSet