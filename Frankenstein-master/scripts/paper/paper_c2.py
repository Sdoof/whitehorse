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
from calc import calc_close_pos, calc_closeVWAP, calc_add_pos, calc_pl
from paper_c2_portfolio import get_c2_portfolio, update_c2_portfolio, get_c2_pos, get_new_c2_pos, update_unr_profit
from paper_c2_trades import get_c2_trades, update_c2_trades

debug=False

def place_order(systemname, action, quant, sym, type, currency, exch, pricefeed, date):
        if debug:
            print "Place C2 Order " + action + " " + str(quant) + " " + sym + " " + currency + " " 
        (account, portfolio)=get_c2_portfolio(systemname, date)
        
        price=pricefeed['Ask']
        if action == 'STO' or action == 'STC':
            quant=-abs(quant)
            price=pricefeed['Bid']
                    
        if sym in portfolio.index.values:
            pos=portfolio.loc[sym].copy()
            pos['symbol']=sym
            pos['currency']=currency
            side=str(pos['long_or_short'])
            if debug:
                print 'Symbol: ' + pos['symbol'] + ' Action: ' + action +' Side: ' + side
                
            if (action == 'BTO' and side=='long') or (action == 'STO' and side=='short'):
               
                exec_pos_open(pos, systemname, quant, sym, type, currency, exch, price, pricefeed, date)

            elif (action == 'BTC' and side=='short') or (action == 'STC' and side=='long'):
                exec_pos_close(pos, systemname, quant, sym, type, currency, exch, price, pricefeed, date)
            else:
                print action + ' ' + side + ' ILLEGAL OP '
        elif action == 'STO' or action == 'BTO':
            
            exec_pos_open(pd.DataFrame(), systemname, quant, sym, type, currency, exch, price, pricefeed, date)
        else:
            print action + ' ' + side + ' ILLEGAL OP '
   

def exec_pos_open(pos, systemname, quant, sym, type, currency, exch, price, pricefeed, date):
        if debug:
            print "Exec C2 Pos Open Order " + str(quant) + " " + sym + " " + currency + " " 
            
        if 'symbol' in pos:
            
            pos['symbol']=sym
            side=str(pos['long_or_short'])
            openVWAP=float(pos['opening_price_VWAP'])
            closeVWAP=float(pos['closing_price_VWAP'])
            openqty=float(pos['quant_opened'])
            closedqty=float(pos['quant_closed'])
            if side == 'short':
                openqty = -abs(openqty)
            elif side == 'long':
                closedqty = -abs(closedqty)
            
            inTradeQty=abs(pos['quant_opened'])-abs(pos['quant_closed'])
            if pos['long_or_short'] == 'short':
                inTradeQty=-abs(inTradeQty)
            
            (openVWAP, openqty, commission, buy_power, tradepl, ptValue, side)=calc_add_pos(openVWAP,inTradeQty,
                price, quant, 
                pricefeed['Commission_Pct'],pricefeed['Commission_Cash'], currency, 
                pricefeed['C2Mult'])
            
            pos['closeVWAP_timestamp']=''
            pos['closedWhen']=''
            pos['closedWhenUnixTimeStamp']=''
            pos['closing_price_VWAP']=''
            pos['quant_closed']=0
            
            pos['openVWAP_timestamp']=date
            pos['opening_price_VWAP']=openVWAP
            pos['quant_opened']=abs(openqty)
            pos['qty']=quant
            pos['commission']=pos['commission'] + commission
            pos['long_or_short']=side
            pos['currency']=currency
            
            if debug:
                print "++++++++++++++++++++"
                print "Trade ID: " + str(pos['trade_id'])
                print "C2 " + str(sym) + "@" + str(price) + "[" + str(quant) + "]"
                print " Total Opened: " + str(openVWAP) + "[" + str(openqty) + "]" 
                print " Total Closed: " + str(closeVWAP) + "[" + str(closedqty) + "]" 
                print "Trade PL: " + str(tradepl) + " Total PL: " + str(pos['PL']) + " (Commission: " + str(commission) + ")"
                print "++++++++++++++++++++"
            purepl=0
            
            update_c2_portfolio(systemname, pos, tradepl, purepl, buy_power, date)
            (unr_pnl, pure_unr_pnl)=update_unr_profit(systemname, pricefeed, currency, date)
            account=update_account_pnl(systemname, 'c2', tradepl, purepl, buy_power, unr_pnl, pure_unr_pnl, date)
            update_c2_trades(systemname, account, pos, tradepl, purepl, buy_power, date)
       
       
        else:
            side='long'
            if quant < 0:
                side='short'
                
            (openVWAP, openqty, commission, buy_power,tradepl, ptValue, side)=calc_add_pos(0,0,
                    price, quant, 
                    pricefeed['Commission_Pct'],pricefeed['Commission_Cash'], currency, 
                    pricefeed['C2Mult'])
            
            pos=get_new_c2_pos(systemname, sym, side, price, quant, tradepl, commission, ptValue, date)
            purepl=0
            pos['currency']=currency
            update_c2_portfolio(systemname, pos, tradepl, purepl, buy_power, date)
            #(unr_pnl, pure_unr_pnl)=update_unr_profit(systemname, pricefeed, currency, date)
            unr_pnl=0
            pure_unr_pnl=0
            account=update_account_pnl(systemname, 'c2', tradepl, purepl, buy_power, unr_pnl, pure_unr_pnl, date)
            update_c2_trades(systemname, account, pos, tradepl, purepl, buy_power, date)
       

def exec_pos_close(pos, systemname, quant, sym, type, currency, exch, price, pricefeed, date):
        if debug:
            print "Exec C2 Pos Close Order " + str(quant) + " " + sym + " " + currency + " " 
    
        if 'symbol' in pos:
            pos['symbol']=sym
            side=str(pos['long_or_short'])
            openVWAP=float(pos['opening_price_VWAP'])
            closeVWAP=float(pos['closing_price_VWAP'])
            openqty=float(pos['quant_opened'])
            closedqty=float(pos['quant_closed'])
            if side == 'short':
                openqty = -abs(openqty)
            elif side == 'long':
                closedqty = -abs(closedqty)
            if abs(openqty) > abs(closedqty):
                qty=abs(abs(openqty)-abs(closedqty))
                if side == 'short':
                    qty=-abs(qty)
                (newVWAP, remqty, commission, buy_power, tradepl, ptValue, newside, purepl) =           \
                    calc_close_pos(openVWAP, qty, price, quant,                      \
                    pricefeed['Commission_Pct'],pricefeed['Commission_Cash'], currency, \
                    pricefeed['C2Mult'])
                (closeVWAP, closedqty)=calc_closeVWAP(closeVWAP, closedqty, price, quant)
                
                #pos['openVWAP_timestamp']=date
                #pos['opening_price_VWAP']=openVWAP
                #pos['quant_opened']=abs(openqty)
                pos['closeVWAP_timestamp']=date
                pos['closedWhen']=date
                pos['closedWhenUnixTimeStamp']=date
                pos['closing_price_VWAP']=closeVWAP
                pos['quant_closed']=abs(closedqty)
                pos['commission']=pos['commission'] + commission
                pos['long_or_short']=side
                pos['qty']=quant
                pos['currency']=currency
                
                if abs(closedqty) >= abs(openqty):
                    pos['open_or_closed']='closed'
                
                if debug:
                    print "--------------------"
                    print "Trade ID: " + str(pos['trade_id'])
                    print "C2 " + ' ' + str(sym) + "@" + str(price) + "[" + str(quant) + "]"
                    print " Total Opened: " + str(openVWAP) + "[" + str(openqty) + "]" 
                    print " Total Closed: " + str(closeVWAP) + "[" + str(closedqty) + "]" 
                    print "Trade PL: " + str(tradepl) + " Total PL: " + str(pos['PL']) + " (Commission: " + str(commission) + ")"
                    print "--------------------"
            else:
                pos['symbol']=sym
                pos['open_or_closed']='closed'
                pos['currency']=currency
                
            update_c2_portfolio(systemname, pos, tradepl, purepl, buy_power, date)
            #(unr_pnl, pure_unr_pnl)=update_unr_profit(systemname, pricefeed, currency, date)
            unr_pnl=0
            pure_unr_pnl=0
            account=update_account_pnl(systemname, 'c2',tradepl, purepl, buy_power, unr_pnl, pure_unr_pnl, date)
            update_c2_trades(systemname, account, pos, tradepl, purepl, buy_power, date)
            

