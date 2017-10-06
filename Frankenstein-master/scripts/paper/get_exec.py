import numpy as np
import pandas as pd
import time
import json
from time import gmtime, strftime, time, localtime

from pandas.io.json import json_normalize
from ibapi.get_exec import get_exec as get_ibexec
from c2api.get_exec import get_exec as get_c2exec
import os
import logging

logging.basicConfig(filename='/logs/get_exec.log',level=logging.DEBUG)

def get_c2trades(systemid, name, c2api):
    filename='./data/portfolio/c2_' + name + '_trades.csv'
    
    datestr=strftime("%Y%m%d", localtime())
    data=get_c2exec(systemid,c2api);
    
    jsondata = json.loads(data)
    if len(jsondata['response']) > 1:
        dataSet=json_normalize(jsondata['response'])
        dataSet=dataSet.set_index('trade_id')
        '''
        if os.path.isfile(filename):
            existData = pd.read_csv(filename, index_col='trade_id')
            existData = existData.reset_index()
            dataSet   =   dataSet.reset_index()
            dataSet=existData.append(dataSet)
            dataSet['trade_id'] = dataSet['trade_id'].astype('int')
            dataSet=dataSet.drop_duplicates(subset=['trade_id'],keep='last')
            dataSet=dataSet.set_index('trade_id') 
        '''
        dataSet=dataSet.sort_values(by='closedWhenUnixTimeStamp')
        
        dataSet.to_csv(filename)

def get_ibtrades():
    filename='./data/portfolio/ib_trades' + '.csv'
    
    datestr=strftime("%Y%m%d", localtime())
    data=get_ibexec()
    dataSet=pd.DataFrame(data)
    if len(dataSet.index) > 0:
	dataSet=dataSet.set_index('permid')
    
    	if os.path.isfile(filename):
        	existData = pd.read_csv(filename, index_col='permid')
        	existData =existData.reset_index()
        	dataSet=dataSet.reset_index()
        	dataSet=existData.append(dataSet)
        	dataSet['permid'] = dataSet['permid'].astype('int')
        	dataSet=dataSet.drop_duplicates(subset=['permid'],keep='last')
        	dataSet=dataSet.set_index('permid')
    	dataSet=dataSet.sort_values(by='times')
    	dataSet.to_csv(filename)

def get_executions(data):        
    #data=pd.read_csv('./data/systems/system.csv')
    #data=data.reset_index()

    c2dict={}
    for i in data.index:
        system=data.ix[i]
        print system['Name'] + ' ' + str(system['c2submit'])
        if system['c2submit']:
                c2dict[system['c2id']]=(system['Name'],system['c2api'])

    for c2id in c2dict:
        (stratName,c2api)=c2dict[c2id]
        get_c2trades(c2id, stratName, c2api)


    #get_ibtrades()
