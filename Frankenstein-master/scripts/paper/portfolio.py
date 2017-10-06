import numpy as np
import pandas as pd
import time
import os
import json
from pandas.io.json import json_normalize
from time import gmtime, strftime, time, localtime, sleep
from paper_ib_portfolio import get_ib_portfolio, update_ib_portfolio, get_ib_pos, get_new_ib_pos
from paper_c2_portfolio import get_c2_portfolio, update_c2_portfolio, get_c2_pos, get_new_c2_pos
#from ibapi.get_exec import get_ibpos, get_iblivepos, get_exec_open as get_ibexec_open, get_ibpos_from_csv
#from c2api.get_exec import get_c2pos, get_c2livepos, get_exec_open as get_c2exec_open, get_c2pos_from_csv


def get_portfolio(systemname, broker, date, isLive=False):
    if not isLive:
        if broker == 'c2':
            (account, portfolio)=get_c2_portfolio(systemname, date)
            return portfolio
        elif broker == 'ib':
            (account, portfolio)=get_ib_portfolio(systemname, date)
            return portfolio
    else:
        if broker == 'c2':
            c2_pos=get_c2pos_from_csv()
            return c2_pos
        elif broker == 'ib':
            ib_pos=get_ibpos_from_csv()
            return ib_pos
        
def get_pos(portfolio, broker, symbol, currency, date):
    if broker == 'ib':
        portfolio_data=portfolio.reset_index().copy()
        portfolio_data['symbol']=portfolio_data['sym'] + portfolio_data['currency']
        sym_cur=symbol + currency
        portfolio_data=portfolio_data.set_index('symbol')
        if sym_cur not in portfolio_data.index.values:
           return 0
        else:
            ib_pos=portfolio_data.loc[sym_cur]
            ib_pos_qty=ib_pos['qty']
            return ib_pos_qty
    elif broker == 'c2':
        portfolio_data=portfolio_data.reset_index().copy()
        sym_cur=symbol
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

def update_portfolio_data(broker, systemname, systemid='c2sysid',apikey='c2api'):
    if broker == 'ib':
        get_iblivepos()
    elif broker == 'c2':
        get_c2livepos(systemid, apikey, systemname)