import sys
import time
import requests
import math
import numpy as np
import pandas as pd
import sqlite3
import talib as ta
import os
import json
from os import listdir
from os.path import isfile, join
import datetime
from datetime import datetime as dt

c2id = "110064634"
c2key = "aQWcUGsCEMPTUjuogyk8G5qb3pk4XM6IG5iRdgCnKdWLxFVjeF"

def get_working_signals(systemid, apikey):
    #logging.info("get_working_signals: " + systemid)
    url = 'https://api.collective2.com/world/apiv3/retrieveSignalsWorking'

    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

    data = {
        "apikey": apikey,  # "tXFaL4E6apdfmLtGasIovtGnUDXH_CQso7uBpOCUDYGVcm1w0w",
        "systemid": systemid
    }

    params = {}

    r = requests.post(url, params=params, json=data);
    time.sleep(1)
    #logging.info(str(r.text))
    return r.text


def cancel_signal(signalid, systemid, apikey):
    #logging.info("cancel_signal: systemid:" + systemid + ', signalid' + signalid)

    url = 'https://api.collective2.com/world/apiv3/cancelSignal'

    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

    data = {
        "apikey": apikey,  # "tXFaL4E6apdfmLtGasIovtGnUDXH_CQso7uBpOCUDYGVcm1w0w",
        "systemid": systemid,
        "signalid": signalid
    }

    params = {}

    r = requests.post(url, params=params, json=data);
    #logging.info(str(r.text))
    return r.text

def clear_signals(systemid, apikey):
    txt=''
    data = get_working_signals(systemid, apikey);
    jsondata = json.loads(data)
    if len(jsondata['response']) > 0:
        dataSet = json_normalize(jsondata['response'])
        for i in dataSet.index:
            row = dataSet.ix[i]
            txt+=cancel_signal(row['signal_id'], systemid, apikey)
    return txt

if __name__ == "__main__":
    start_time = time.time()
    print 'clearing signals.'
    clear_signals(c2id, c2key)
    print 'Elapsed time: ', round(((time.time() - start_time) / 60), 2), ' minutes ', dt.now()
