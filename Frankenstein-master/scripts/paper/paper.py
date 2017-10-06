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
from paper_c2_portfolio import get_c2_pos
from paper_ib_portfolio import get_ib_pos
from paper_order import place_order

debug=True

def adj_size(model_pos, system, system_name, pricefeed, c2systemid, c2apikey, c2quant, c2sym, c2type, c2submit, ibquant, ibsym, ibcurrency, ibexch, ibtype, ibsubmit, date):
    system_pos=model_pos.loc[system]
   
    c2submit=True
    ibsubmit=True
                
    if c2submit:
        c2_pos_qty=get_c2_pos(system_name, c2sym, date)           
        system_c2pos_qty=round(system_pos['action']) * c2quant
        
        if system_c2pos_qty != c2_pos_qty:
            if debug:
                print "!!!C2!!!"
                print "system: " + system_name + " symbol: " + c2sym
                print "system_c2_pos: " + str(system_c2pos_qty)
                print "c2_pos: " + str(c2_pos_qty)
                print "!!!C2!!!"
        else:
            if debug:
                print "===C2==="
                print "system: " + system_name + " symbol: " + c2sym
                print "system_c2_pos: " + str(system_c2pos_qty)
                print "c2_pos: " + str(c2_pos_qty)
                print "===C2==="
        if system_c2pos_qty > c2_pos_qty:
            c2quant=system_c2pos_qty - c2_pos_qty
            if c2_pos_qty < 0:        
                qty=min(abs(c2_pos_qty), abs(c2_pos_qty - system_c2pos_qty))
                if debug:
                    print 'BTC: ' + str(qty)
                place_order(system_name, 'BTC', qty, c2sym, c2type, ibcurrency, ibexch, 'c2', pricefeed,date)
                                
                c2quant = c2quant - qty
            
            if c2quant > 0:
                if debug:
                    print 'BTO: ' + str(c2quant)
                place_order(system_name, 'BTO', c2quant, c2sym, c2type, ibcurrency, ibexch, 'c2', pricefeed,date)
                
        if system_c2pos_qty < c2_pos_qty:
            c2quant=c2_pos_qty - system_c2pos_qty   
            
            if c2_pos_qty > 0:        
                qty=min(abs(c2_pos_qty), abs(c2_pos_qty - system_c2pos_qty))
                if debug:
                    print 'STC: ' + str(qty)
                place_order(system_name, 'STC', qty, c2sym, c2type, ibcurrency, ibexch, 'c2', pricefeed,date)
                
                c2quant = c2quant - qty

            if c2quant > 0:
                if debug:
                    print 'STO: ' + str(c2quant)
                place_order(system_name, 'STO', c2quant, c2sym, c2type, ibcurrency, ibexch, 'c2', pricefeed,date)
                
    if ibsubmit:
        symbol=ibsym
        if ibtype == 'CASH':
            symbol=ibsym+ibcurrency
        ib_pos_qty=get_ib_pos(system_name, ibsym, ibcurrency, ibtype, date)
        system_ibpos_qty=round(system_pos['action']) * ibquant
        
        if system_ibpos_qty != ib_pos_qty:
            if debug:
                print "!!!IB!!!"
                print "system: " + system_name + " symbol: " +symbol
                print "system_ib_pos: " + str(system_ibpos_qty)
                print "ib_pos: " + str(ib_pos_qty)
                print "!!!IB!!!"
        else:
            if debug:
                print "===IB==="
                print "system: " + system_name + " symbol: " +symbol
                print "system_ib_pos: " + str(system_ibpos_qty)
                print "ib_pos: " + str(ib_pos_qty)
                print "===IB==="
        if system_ibpos_qty > ib_pos_qty:
            ibquant=float(system_ibpos_qty - ib_pos_qty)
            if debug:
                print 'BUY: ' + str(ibquant)
            place_order(system_name, 'BUY', ibquant, ibsym, ibtype, ibcurrency, ibexch, 'ib', pricefeed,date);
        if system_ibpos_qty < ib_pos_qty:
            ibquant=float(ib_pos_qty - system_ibpos_qty)
            if debug:
                print 'SELL: ' + str(ibquant)
            place_order(system_name, 'SELL', ibquant, ibsym, ibtype, ibcurrency, ibexch, 'ib', pricefeed,date)



