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

from paper_account import get_account_value, update_account_value
from calc import calc_close_pos, calc_closeVWAP, calc_add_pos, calc_pl

debug=True
debug2=False
cumpl=dict()

def get_c2_trades(systemname, date):
    filename='./data/paper/c2_' + systemname + '_trades.csv'
    
    if os.path.isfile(filename):
        dataSet = pd.read_csv(filename, index_col='trade_id')
        if 'PurePL' not in dataSet:
            dataSet['PurePL']=0
        return dataSet
    else:
        dataSet=pd.DataFrame({},columns=['trade_id','PL','closeVWAP_timestamp','closedWhen',\
        'closedWhenUnixTimeStamp','closing_price_VWAP','expir','instrument','long_or_short',\
        'markToMarket_time','openVWAP_timestamp','open_or_closed','openedWhen','opening_price_VWAP',\
        'ptValue','putcall','quant_closed','quant_opened','strike','symbol','symbol_description','PurePL','qty','currency'])
        dataSet = dataSet.set_index('trade_id')
        dataSet.to_csv(filename)
        return dataSet
  
    return dataSet


def update_c2_trades(systemname, account, pos, tradepl, purepl, buypower, date):

    filename='./data/paper/c2_' + systemname + '_trades.csv'
    dataSet = get_c2_trades(systemname, date)
    
    pos=pos.copy()
    tradeid=int(pos['trade_id'])
    pos['balance']=account['balance'] 
    pos['purebalance']=account['purebalance']
    pos['mark_to_mkt']=account['mark_to_mkt']    
    pos['pure_mark_to_mkt']=account['pure_mark_to_mkt']
    pos['margin_available']=account['buy_power']
    pos['PurePL']=float(pos['PurePL']) + purepl
    pos['PL']=float(pos['PL']) + float(tradepl)
    
    if debug2:
        if cumpl.has_key(pos['symbol']):
            cumpl[pos['symbol']]=cumpl[pos['symbol']] +float(tradepl)
        else:
            cumpl[pos['symbol']]=float(tradepl)
        print 'C2 Symbol: ' + pos['symbol'] + ' PL: ' + str(pos['PL']) + ' Comp:' + str(cumpl[pos['symbol']])
        print 'C2 Symbol: ' + pos['symbol'] + ' Co: ' + str(pos['commission']) + ' Comp:' + str(pos['PL']-pos['PurePL'])
        if pos['quant_opened']-pos['quant_closed']==0:
            cumpl[pos['symbol']]=0
            
    if tradeid in dataSet.index.values:
        dataSet = dataSet[dataSet.index != tradeid]
        dataSet=dataSet.reset_index()
        dataSet=dataSet.append(pos)
        dataSet=dataSet.set_index('trade_id')   
    
    else:
        dataSet=dataSet.reset_index()
        dataSet=dataSet.append(pos)
        dataSet=dataSet.set_index('trade_id')   
        
    if debug:
        openqty=pos['quant_opened']-pos['quant_closed']
        if pos['long_or_short'] == 'short':
            openqty=-abs(openqty)
        print "Update C2 Trade Balance: " + str(account['balance'])  + " PB: " +  str(account['purebalance']) + " PurePL: " + str(account['PurePL']) + ' ' + \
                    systemname + " " + pos['long_or_short'] + \
                    ' symbol: ' + pos['symbol'] + ' qty: ' + str(pos['qty']) + \
                    ' openqty: ' + str(openqty) + \
                    ' open_or_closed ' + pos['open_or_closed'] + ' Buy_Power: ' + str(account['buy_power'])
             
    dataSet.to_csv(filename)
    
    return (account, dataSet)
    
