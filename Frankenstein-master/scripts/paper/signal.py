import numpy as np
import pandas as pd
import time
import os
import json
import logging
from pandas.io.json import json_normalize
from time import gmtime, strftime, time, localtime, sleep

signalPath = './signals/'

def get_model_pos(systems):
    pos=pd.DataFrame({}, columns=['system','action','qty']);
    for system in systems:
        filename=signalPath + system + '.csv'
        if os.path.isfile(filename):
            data = pd.read_csv(filename, index_col='Date').iloc[-1]
            signals=data['Signal'];
            #safef=data['safef'];
           
            signal=signals
            qty=1
            pos=pos.append(pd.DataFrame([[system, signal, qty]], columns=['system','action','qty']))
        else:
            pos=pos.append(pd.DataFrame([[system, 0, 0]], columns=['system','action','qty']))
              
    pos=pos.set_index(['system'])
    pos.to_csv('./data/portfolio/model_pos.csv')
    return pos;

def get_dps_model_pos(systems):
    pos=pd.DataFrame({}, columns=['system','action','qty']);
    for system in systems:
        filename=signalPath + system + '.csv'
        if os.path.isfile(filename):
            try:
                data = pd.read_csv(filename, index_col='dates').iloc[-1]
                signals=data['signals'];
                safef=data['safef'];
                qty=safef*signals
                #signal=signals[-1];
                qty=round(qty)
                signal=qty
                pos=pos.append(pd.DataFrame([[system, signal, qty]], columns=['system','action','qty']))
            except Exception as e:
                print 'Error processing: ', filename
                os.remove(filename);
                logging.error("something bad happened", exc_info=True)
        else:
            pos=pos.append(pd.DataFrame([[system, 0, 0]], columns=['system','action','qty']))
        #pos=pos.append({'sym':system, 'action':signal, 'qty':qty}, ignore_index=True)
            
    pos=pos.set_index(['system'])
    
    pos.to_csv('./data/portfolio/dps_model_pos.csv')
    return pos;

def generate_model_pos(system):
    data = pd.read_csv(signalPath + system + '.csv', index_col='dates').iloc[-1]
    signals=data['signals'];
    safef=data['safef'];
    qty=safef*signals
    #signal=signals[-1];
    qty=round(qty)
    signal=qty
    ###################
    pos=pd.DataFrame([[system, signal, qty]], columns=['system','action','qty'])
    pos=pos.set_index(['system'])
    #pos.to_csv('./data/portfolio/gen_model_pos.csv')
    return pos

def generate_model_sig(system, date, action, qty, comment=''):
    #pos=pd.DataFrame({}, columns=['system','action','qty']);
    pos=pd.DataFrame([[date, action, qty, comment]], columns=['dates','signals','safef','comment'])
    filename=signalPath + system + '.csv'
    if os.path.isfile(filename):
        data=pd.read_csv(filename)
        pos=data.append(pos)
        pos=pos.set_index('dates')
        pos.to_csv(signalPath + system + '.csv')
    else:
        pos=pos.set_index('dates')
        pos.to_csv(signalPath + system + '.csv')
    
    qty=action * qty
    qty=round(qty)
    signal=qty
    ###################
    pos=pd.DataFrame([[system, signal, qty]], columns=['system','action','qty'])
    pos=pos.set_index(['system'])
    return pos

def get_model_sig(system):
    filename=signalPath + system + '.csv'
    if os.path.isfile(filename):
        data=pd.read_csv(filename, index_col='dates')
        return data
    else:
        pos=pd.DataFrame({}, columns=['dates','signals','safef','comment'])
        pos=pos.set_index('dates')
        return pos
        
    
    
def generate_model_manual(system, action, qty):
    pos=pd.DataFrame([[system, action, qty]], columns=['system','action','qty'])
    pos=pos.set_index(['system'])
    #pos.to_csv('./data/portfolio/gen_model_pos.csv')
    return pos
    

def get_signal_list():
    dpsList=dict()
    systemdata=pd.read_csv('./data/systems/system.csv')
    systemdata=systemdata.reset_index()
    for i in systemdata.index:
        system=systemdata.ix[i]
        dpsList[system['System']]=1
    return dpsList.keys()
