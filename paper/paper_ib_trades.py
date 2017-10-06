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
import threading

debug=True
debug2=False
lock = threading.Lock()

def get_ib_trades(systemname, date):
    filename='./data/paper/ib_' + systemname + '_trades.csv'
    
    if os.path.isfile(filename):
        with lock:
            dataSet = pd.read_csv(filename, index_col='permid')
            if 'PurePL' not in dataSet:
                dataSet['PurePL']=0
            return dataSet
    else:
        dataSet=pd.DataFrame({}, columns=['permid','account','clientid','commission','commission_currency',\
                            'exchange','execid','expiry','level_0','orderid','price','qty','openqty', \
                            'realized_PnL','side',\
                            'symbol','symbol_currency','times','yield_redemption_date','PurePL'])
        dataSet=dataSet.set_index('permid')
        with lock:
            dataSet.to_csv(filename)
        return dataSet
    
    
def update_ib_trades(systemname, account, pos, tradepl, purepl, buypower, ibexch, date):
    
    filename='./data/paper/ib_' + systemname + '_trades.csv'
   
    dataSet = get_ib_trades(systemname, date)
    #pos=pos.iloc[-1]
    pos=pos.copy()
    trade_id=0
    dataSet=dataSet.reset_index()
    if len(dataSet['permid'].values) > 0:
        trade_id=int(max(dataSet['permid'].values))
    trade_id=int(trade_id) + 1
    side='BOT'
    if pos['qty'] < 0:
        side='SLD'
    
    
    pos=pd.DataFrame([[trade_id, 'Paper', 'Paper', pos['avg_cost'], 'USD', \
                               ibexch, trade_id, '','',1,pos['price'],abs(pos['qty']),pos['openqty'],pos['openprice'], \
                               tradepl,purepl,side, \
                               pos['sym'], pos['currency'], date, '' \
                            ]], columns=['permid','account','clientid','commission','commission_currency',\
                            'exchange','execid','expiry','level_0','orderid','price','qty','openqty','openprice', \
                            'realized_PnL','PurePL','side',\
                            'symbol','symbol_currency','times','yield_redemption_date']).iloc[-1]
                            
    tradeid=int(pos['permid'])
    
    dataSet['permid'] = dataSet['permid'].astype('int')
    pos['permid'] = pos['permid'].astype('int')
    pos['balance']=account['balance'] 
    pos['purebalance']=account['purebalance']
    pos['mark_to_mkt']=account['mark_to_mkt']    
    pos['pure_mark_to_mkt']=account['pure_mark_to_mkt']
    pos['margin_available']=account['buy_power']
    pos['PurePL']=purepl
    pos['real_pnl']=tradepl
    
    if debug2:
        print 'IB Symbol: ' + pos['symbol'] + pos['symbol_currency'] + ' PL: ' + str(pos['real_pnl']) + ' Pure PL:' + str(pos['PurePL'])
    
    if tradeid in dataSet['permid'].values:
        dataSet = dataSet[dataSet['permid'] != tradeid]
        dataSet=dataSet.append(pos)
         
    else:
        dataSet=dataSet.append(pos)
    
    if debug:
        longshort='long'
        qty=abs(pos['qty'])
        if pos['openqty'] < 0:
            longshort='short'
        if pos['openqty'] == 0:
            if side=='SLD':
                longshort='long'
            else:
                longshort='short'
        if side == 'SLD':
            qty=-abs(qty)
        openorclosed='open'
        if pos['openqty'] == 0:
            openorclosed='closed'
        if debug:
            print "Update IB Balance: " + str(account['balance'])  + " PB: " +  str(account['purebalance']) + " PurePL: " + str(account['PurePL']) + ' ' + \
                    systemname + " " + longshort + \
                    ' symbol: ' + (pos['symbol']) + ' currency: ' + pos['symbol_currency'] + ' qty: ' + str(qty) + \
                    ' openqty: ' + str(pos['openqty']) + ' open_or_closed ' + openorclosed + ' Buy_Power: ' + str(account['buy_power'])
    #print filename
    dataSet['permid'] = dataSet['permid'].astype('int')
    dataSet=dataSet.set_index('permid')   
    with lock:
        dataSet.to_csv(filename)
    

    return (account, dataSet)



# -*- coding: utf-8 -*-

