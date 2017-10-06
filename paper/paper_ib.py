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

from paper_account import get_account_value, update_account_value, update_account_pnl
from calc import calc_close_pos, calc_add_pos, calc_pl
from paper_ib_trades import get_ib_trades, update_ib_trades
from paper_ib_portfolio import get_ib_portfolio, update_ib_portfolio, get_ib_pos, get_new_ib_pos, update_unr_profit

debug=False

def place_order(systemname, action, quant, sym, type, currency, exch, pricefeed, date):
        if debug:
            print "Place IB Order " + action + " " + str(quant) + " " + sym + " " + currency 
        (account, portfolio)=get_ib_portfolio(systemname, type, date)
        symbol=sym
        if type == 'CASH':
            symbol=sym+currency
        price=-1
            
        if action == 'SELL':
            price=pricefeed['Bid']
            quant=-abs(quant)
            
        if action == 'BUY':
            price=pricefeed['Ask']
            quant=abs(quant)
            
        if symbol in portfolio.index.values:
            #portfolio=portfolio.reset_index().set_index('symbol')
            pos=portfolio.loc[symbol].copy()
            pos['symbol']=symbol
            openqty=float(pos['openqty'])
            side='long'
            
            if openqty < 0:
                side='short'
                
            if (action == 'BUY' and side == 'long') or (action == 'SELL' and side=='short'):
                exec_open_pos(pos,  systemname, quant, sym, type, currency, exch, price, pricefeed, date)
                
            elif (action == 'BUY' and side=='short') or (action == 'SELL' and side=='long'):
                exec_close_pos(pos, systemname, quant, sym, type, currency, exch, price, pricefeed, date)
            else:
                print action + ' ' + side + ' ILLEGAL OP '
        else:
            exec_open_pos(pd.DataFrame(), systemname, quant, sym, type, currency, exch, price, pricefeed, date)

def exec_open_pos(pos, systemname, quant, sym, type, currency, exch, price, pricefeed, date):
        if debug:
            print "Place Open IB Order " + str(quant) + " " + sym + " " + currency  
        symbol=sym
        if type == 'CASH':
            symbol=sym+currency
        if 'symbol' in pos:
            pos['symbol']=symbol
            openVWAP=float(pos['openprice'])
            openqty=float(pos['openqty'])
            side='long'
            if openqty < 0:
                side='short'
       
            (openVWAP, openqty, commission, buy_power, tradepl, ptValue,side)=calc_add_pos(openVWAP,openqty, \
                price, quant,  \
                pricefeed['Commission_Pct'],pricefeed['Commission_Cash'], currency, \
                pricefeed['IBMult'])
                
            pos['openprice']=openVWAP
            pos['openqty']=openqty
            pos['price']=price
            pos['qty']=quant
            pos['value']=buy_power
            pos['avg_cost']=commission
            pos['real_pnl']=pos['real_pnl'] + tradepl
            pos['unr_pnl']=0
            
            if debug:
                print "IB " + ' ' + str(symbol) + "@" + str(price) + "[" + str(quant) + "] Opened @ " + \
                    str(openVWAP) + "[" + str(openqty) + "]" 
                print "New PL: " + str(pos['real_pnl']) + " Trade PL: " + str(tradepl) + " (Commission: " + str(commission) + ")"   
                print "New VWAP: " + str(openVWAP) + " [" + str(openqty) + "]"
            
            purepl=0
            update_ib_portfolio(systemname, pos, type, date)
            #(unr_pnl, pure_unr_pnl)=update_unr_profit(systemname, pricefeed, currency, type, date)
            unr_pnl=0
            pure_unr_pnl=0
            account=update_account_pnl(systemname, 'ib',tradepl, purepl, buy_power, unr_pnl, pure_unr_pnl, date)
            update_ib_trades(systemname, account, pos, tradepl, purepl, buy_power, exch, date)
            
                

        else:
            
            (openVWAP, openqty, commission, buy_power,tradepl, ptValue,side)=calc_add_pos(0,0,price,quant,
                    pricefeed['Commission_Pct'],pricefeed['Commission_Cash'], currency, 
                    pricefeed['IBMult'])
             
            pos=get_new_ib_pos(systemname, sym, openVWAP, openqty, buy_power, tradepl, commission, currency, date)
            purepl=0
            
            update_ib_portfolio(systemname, pos, type, date)
            #(unr_pnl, pure_unr_pnl)=update_unr_profit(systemname, pricefeed, currency, type, date)
            unr_pnl=0
            pure_unr_pnl=0
            account=update_account_pnl(systemname, 'ib',tradepl, purepl, buy_power, unr_pnl, pure_unr_pnl, date)
            update_ib_trades(systemname, account, pos, tradepl, purepl, buy_power, exch, date)
            
            

def exec_close_pos(pos, systemname, quant, sym, type, currency, exch, price, pricefeed, date):
        symbol=sym
        if type == 'CASH':
            symbol=sym+currency
        if 'symbol' in pos:
            pos['symbol']=symbol
            openVWAP=float(pos['openprice'])
            openqty=float(pos['openqty'])
          
            (openVWAP, openqty, commission, buy_power, tradepl, ptValue,side, purepl) =           \
                calc_close_pos(openVWAP,openqty, price, quant,                      \
                pricefeed['Commission_Pct'],pricefeed['Commission_Cash'], currency, \
                pricefeed['IBMult'])
            
            pos['openprice']=openVWAP
            pos['openqty']=openqty
            pos['price']=price
            pos['qty']=quant
            pos['value']=buy_power
            pos['real_pnl']=pos['real_pnl'] + tradepl
            pos['avg_cost']=commission
            pos['unr_pnl']=0
            pos['PurePL']=pos['PurePL'] + purepl
            
            if debug:
                print "IB " + str(symbol) + "@" + str(price) + "[" + str(quant) + "] Opened @ " + \
                    str(openVWAP) + "[" + str(openqty) + "]" 
                print "Original PL: " + str(pos['real_pnl']) + " New PL: " + str(purepl) + " (Commission: " + str(commission) + ")"
                print "Trade PL: " + str(purepl)
                print "New VWAP: " + str(openVWAP) + " [" + str(openqty) + "]"

            update_ib_portfolio(systemname, pos, type, date)
            #(unr_pnl, pure_unr_pnl)=update_unr_profit(systemname, pricefeed, currency, type, date)
            unr_pnl=0
            pure_unr_pnl=0
            account=update_account_pnl(systemname, 'ib',tradepl, purepl, buy_power, unr_pnl, pure_unr_pnl, date)
            update_ib_trades(systemname, account, pos, tradepl, purepl, buy_power, exch, date)
            
            
                
       