import numpy as np
import pandas as pd
import time

import json
from pandas.io.json import json_normalize
from ibapi.place_order import place_order as place_iborder
from c2api.place_order import place_order as place_c2order
from ibapi.get_exec import get_ib_pos, get_exec_open as get_ibexec_open, get_ib_sym_pos
from c2api.get_exec import get_c2_pos
from signal import get_model_pos
from time import gmtime, strftime, time, localtime, sleep
import logging

def adj_size(model_pos, system, systemname, systemid, c2apikey, c2quant,\
                    c2sym, c2type, c2submit, ibquant, ibsym, ibcurrency, ibexch, ibtype,\
                    ibsubmit, iblocalsym=''):
    system_pos=model_pos.loc[system]
   
    logging.info('==============')
    logging.info('Strategy:' + systemname)
    #logging.info('system_pos:' +str(system_pos))
    logging.info("  Signal Name: " + system)
    logging.info("  C2ID: " + systemid + "  C2Key: " + c2apikey)
    logging.info("  C2Sym: " + c2sym + " IBSym: " + ibsym)
    if c2submit == 'TRUE':
        c2submit=True
    elif c2submit == 'FALSE':
        c2submit=False
        
    if ibsubmit == 'TRUE':
        ibsubmit=True
    elif ibsubmit == 'FALSE':
        ibsubmit=False
    #print str(system_pos['action'])
    #print "c2: " 
    #print c2_pos
    if c2submit:
        c2_pos_qty=get_c2_pos(systemname, c2sym)           
        system_c2pos_qty=round(system_pos['action']) * c2quant
        logging.info( "system_c2_pos: " + str(system_c2pos_qty) )
        logging.info( "c2_pos: " + str(c2_pos_qty) )
        
        if system_c2pos_qty > c2_pos_qty:
            c2quant=system_c2pos_qty - c2_pos_qty
            isrev=False
            psigid=0
            if c2_pos_qty < 0:        
                qty=min(abs(c2_pos_qty), abs(c2_pos_qty - system_c2pos_qty))
                logging.info( 'BTC: ' + str(qty) )
                psigid=place_c2order('BTC', qty, c2sym, c2type, systemid, c2submit, c2apikey)
                isrev=True                
                c2quant = c2quant - qty
                
            if c2quant > 0:
                logging.info( 'BTO: ' + str(c2quant) )
                if isrev:
                    place_c2order('BTO', c2quant, c2sym, c2type, systemid, c2submit, c2apikey, psigid)
                else:
                    place_c2order('BTO', c2quant, c2sym, c2type, systemid, c2submit, c2apikey)
        if system_c2pos_qty < c2_pos_qty:
            c2quant=c2_pos_qty - system_c2pos_qty   
            isrev=False
            psigid=0
            if c2_pos_qty > 0:        
                qty=min(abs(c2_pos_qty), abs(c2_pos_qty - system_c2pos_qty))
                logging.info( 'STC: ' + str(qty) )
                psigid=place_c2order('STC', qty, c2sym, c2type, systemid, c2submit, c2apikey)
                isrev=True 
                c2quant = c2quant - qty

            if c2quant > 0:
                logging.info( 'STO: ' + str(c2quant) )
                if isrev:
                    place_c2order('STO', c2quant, c2sym, c2type, systemid, c2submit, c2apikey, psigid)
                else:
                    place_c2order('STO', c2quant, c2sym, c2type, systemid, c2submit, c2apikey)
   
    if ibsubmit:
        ib_pos_qty=get_ib_pos(ibsym, ibcurrency)
        system_ibpos_qty=round(system_pos['action']) * ibquant
        
        logging.info( "system_ib_pos: " + str(system_ibpos_qty) )
        logging.info( "ib_pos: " + str(ib_pos_qty) )
        if system_ibpos_qty > ib_pos_qty:
            ibquant=int(system_ibpos_qty - ib_pos_qty)
            logging.info( 'BUY: ' + str(ibquant) )
            place_iborder('BUY', ibquant, ibsym, ibtype, ibcurrency, ibexch, ibsubmit, iblocalsym);
        if system_ibpos_qty < ib_pos_qty:
            ibquant=int(ib_pos_qty - system_ibpos_qty)
            logging.info( 'SELL: ' + str(ibquant) )
            place_iborder('SELL', ibquant, ibsym, ibtype, ibcurrency, ibexch, ibsubmit, iblocalsym);
    #
    #place_iborder(ibaction, ibquant, ibsym, ibtype, ibcurrency, ibexch, ibsubmit);
