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

debug=False

def calc_close_pos(openAt, openqty, closeAt, closeqty, comPct, comCash, currency, mult):
    purepl=0
    side='long'
    if openqty < 0:         
        side='short'
        
    remqty=abs(openqty) - abs(closeqty)
    if remqty < 0:
        closeqty=abs(openqty)
       
    (purepl, value)=calc_pl(openAt, closeAt, closeqty, mult, side)
    commission=abs(comPct * closeAt * closeqty * mult)     
    buy_power=abs(mult * closeAt * closeqty)
    
    if currency != 'USD':
        purepl=purepl * get_USD(currency)
        commission=commission * get_USD(currency)
        buy_power=buy_power * get_USD(currency) 
                   
    commission = max(commission, comCash)
    tradepl = purepl - commission       

    if remqty < 0:
        openAt=closeAt
        remqty = abs(remqty)
        if side == 'long':
            side='short'
            remqty = -abs(remqty)
        else:
            side='long' 
        newpos_buy_power=-abs(mult * openAt * remqty)
        if currency != 'USD':
            newpos_buy_power= newpos_buy_power * get_USD(currency) 
        buy_power=buy_power + newpos_buy_power
    else:
        remqty=openqty + closeqty
    
    if debug:
            print 'Close: PL: ' + side + ' ' + str(tradepl) + ' PurePL: ' + str(purepl) + ' Value: ' + str(value) + ' Open: ' + str(openAt) + ' Close: ' + str(closeAt) + ' Qty' + str(closeqty)
       
    return (openAt, remqty, commission, buy_power, tradepl, mult, side, purepl)

def calc_closeVWAP(closeVWAP, closedqty, addVWAP, addqty):
    if closeVWAP == 0 or closedqty == 0:
        return (addVWAP, addqty)
    else:
        newVWAP = (abs(closeVWAP * closedqty) + abs(addVWAP*addqty)) / (abs(closedqty) + abs(addqty))
        newqty = closedqty + addqty
        return (newVWAP, newqty)
        
                
def calc_add_pos(openVWAP, openqty, addAt, addQty, comPct, comCash, currency, mult):
    newVWAP=(abs(openVWAP * openqty) + abs(addAt * addQty)) / (abs(openqty) + abs(addQty))
    newqty=openqty+addQty
    commission=abs(comPct * addAt * addQty * mult)               
    buy_power=abs(mult * addAt * addQty) * -1
    purepl=0
    if currency != 'USD':
            purepl=purepl * get_USD(currency)
            commission=commission * get_USD(currency)
            buy_power=buy_power * get_USD(currency)
    commission = max(commission, comCash)
    pl =  - commission      
    side='long'
    if newqty < 0:
        side='short'
    if debug:
        print 'Side: ' + side + ' NewVWAP: ' + str(newVWAP) + ' newqty: ' + str(newqty) + ' Open: ' + str(openVWAP) + ' OpenQty: ' + str(openqty) + ' AddAt: ' + str(addAt) + ' addQty: ' + str(addQty) 
    return (newVWAP, newqty, commission, buy_power, pl, mult, side)

def calc_pl(openAt, closeAt, qty, mult, side):
    
    if side == 'short':
        pl=(openAt - closeAt)*abs(qty)*abs(mult)
        value=closeAt*abs(qty)*abs(mult)
        if debug:
            print 'Calc: PL: ' + side + ' ' + str(pl) + ' Value: ' + str(value) + ' Open: ' + str(openAt) + ' Close: ' + str(closeAt) + ' Qty' + str(qty)
        return (pl, value)
        
    if side == 'long':
        pl=(closeAt - openAt)*abs(qty)*abs(mult)
        value=closeAt*abs(qty)*abs(mult)
        if debug:
            print 'Calc: PL: ' + side + ' ' + str(pl) + ' Value: ' + str(value) + ' Open: ' + str(openAt) + ' Close: ' + str(closeAt) + ' Qty' + str(qty)
        return (pl,value)

def get_USD(currency):
    data=pd.read_csv('./data/systems/currency.csv')
    conversion=float(data.loc[data['Symbol']==currency].iloc[-1]['Ask'])
    return float(conversion)