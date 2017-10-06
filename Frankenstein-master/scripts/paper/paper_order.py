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
from paper_c2 import place_order as place_c2_order
from paper_ib import place_order as place_ib_order

debug=False

def place_order(systemname, action, quant, sym, type, currency, exch, broker, pricefeed, date):
    if debug:
        print "Place Order " + action + " " + str(quant) + " " + sym + " " + currency + " " + broker 
    pricefeed=pricefeed.iloc[-1]
    
    if broker == 'c2':
        place_c2_order(systemname, action, quant, sym, type, currency, exch, pricefeed, date)
       
    if broker == 'ib':
        place_ib_order(systemname, action, quant, sym, type, currency, exch, pricefeed, date)
       



# -*- coding: utf-8 -*-

