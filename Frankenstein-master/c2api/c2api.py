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
from pandas.io.json import json_normalize

systemid= c2id = "110064634"
apikey=c2key = "aQWcUGsCEMPTUjuogyk8G5qb3pk4XM6IG5iRdgCnKdWLxFVjeF"
import slackweb
fulltimestamp=datetime.datetime.now().strftime('%Y%m%d_%H_%M_%S')
slackhook='https://hooks.slack.com/services/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'
slack = slackweb.Slack(url=slackhook)

def retrieveSystemEquity(c2id, c2key, commission_plan='default'):
    url = 'https://api.collective2.com/world/apiv3/retrieveSystemEquity'
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

    data = {
        "commission_plan": commission_plan,
        "systemid": str(c2id),
        "apikey": str(c2key)
    }

    params = {}

    r = requests.post(url, params=params, json=data);
    # print r.text
    #logging.info(r.text)
    return json_normalize(json.loads(r.text)['equity_data'])

def setDesiredPositions(orders):
    global c2id
    global c2key
    #global type
    global slack
    url = 'https://collective2.com/world/apiv3/setDesiredPositions'
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

    '''
    orders
    [{
        "symbol"		: "@ESM5",
        "typeofsymbol"	: "future",
        "quant"			: "-4"
    },
    {
        "symbol"		: "EURUSD",
        "typeofsymbol"	: "forex",
        "quant"			: "-3"
    },
    {
        "symbol"		: "AAPL",
        "typeofsymbol"	: "stock",
        "quant"			: "211"
    }]
    '''

    data = {
            "apikey":   c2key,
            "systemid": c2id,
            "positions": orders,
            }
    params = {}
    r = requests.post(url, params=params, json=data);
    # sleep(2)
    print r.text
    slack.notify(text=r.text, channel="#logs", username="frankenstein", icon_emoji=":robot_face:")
    # logging.info(str(r.text))
    #return r.json()['signalid']


def get_working_signals(systemid, apikey):
    global slack
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
