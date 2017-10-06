#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 17:54:31 2017

@author: hidemiasakura
"""

import os
import sys
import datetime
from datetime import datetime as dt
import pandas as pd
import json
from os import listdir, remove
from os.path import isfile, join
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import time
from slackclient import SlackClient
from c2api.c2api import setDesiredPositions, get_working_signals, clear_signals,\
                        retrieveSystemEquity

c2id = "110064634"
c2key = "aQWcUGsCEMPTUjuogyk8G5qb3pk4XM6IG5iRdgCnKdWLxFVjeF"
BOT_NAME = 'frankenstein'

#slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
SLACK_BOT_TOKEN='xoxb-156360318612-rOsZj0PhdcnBozPfHWBHJiGS'
BOT_ID='U4LAL9CJ0'
slack_client = SlackClient(SLACK_BOT_TOKEN)

fulltimestamp=datetime.datetime.now().strftime('%Y%m%d_%H_%M_%S')
dataPath = './data/'
portfolioPath=dataPath+c2id+'/'
closed_dir=portfolioPath+fulltimestamp[:8]+'/'
check_dir=dataPath+'check/'
def handle_command(command, channel):
    print command
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean."
    #response += " Use the *" + EXAMPLE_COMMAND + "* command for help."
    if command.startswith('ping'):
        response = "<@"+command.split()[1]+"> yo yo yo"
    if command.startswith('help'):
        response = "*commands:*\n"
        response += "BUY AAPL 100\n"
        response += "SELL AAPL 100\n"
        response += "CLOSE AAPL\n"
        #response += "CLEAR ORDERS\n"
        response += "GET OPEN ORDERS\n"
        response += "RESULTS\n"
        response += "WHERE MY BABY DOLLS FRANK? :dancers:"

    if command.startswith('buy'):
        symbol=command.split()[1]
        qty = command.split()[2]
        response = "BOUGHT " + str(qty) + " " + symbol
        orders = [{
                "symbol"		: symbol,
                "typeofsymbol"	: "stock",
                "quant"			: qty
             }]
        setDesiredPositions(orders)

    if command.startswith('sell'):
        symbol=command.split()[1]
        qty = int(command.split()[2])
        response = "SOLD " + str(qty) + " " + symbol
        orders = [{
                "symbol"		: symbol,
                "typeofsymbol"	: "stock",
                "quant"			: '-'+qty
             }]
        setDesiredPositions(orders)

    if command.startswith('close'):
        symbol=command.split()[1]
        #qty = int(command.split()[2])
        response = "CLOSED " + symbol
        orders = [{
                "symbol"		: symbol,
                "typeofsymbol"	: "stock",
                "quant"			: '0'
             }]
        setDesiredPositions(orders)

    #if command.startswith('clear orders'):
    #    response = "<@" + command.split()[1] + "> CLEARING ORDERS...\n"
    #    response += clear_signals(c2id, c2key)

    if command.startswith('get open orders'):
        response = "GETTING OPEN ORDERS...\n"
        response += get_working_signals(c2id, c2key)
        
    if command.startswith('results'):
        response = "RESULTS...\n"
        df = retrieveSystemEquity(c2id, c2key).groupby(['YYYYMMDD']).last()
        pc=round(df.strategy_with_cost.astype(float).pct_change()[-1]*100,2)
        benchmark_pc=round(df.index_price.astype(float).pct_change()[-1]*100)
        var_pc = pc-benchmark_pc
        itd = round(df.strategy_with_cost.astype(float).pct_change(periods=df.shape[0]-1)[-1]*100)
        benchmark_itd = round(df.index_price.astype(float).pct_change(periods=df.shape[0]-1)[-1]*100)
        var_itd=itd-benchmark_itd
        response+="Last Day: Frank: {}%   S&P500: {}%  VS: {}%\n".format(pc, benchmark_pc, var_pc)
        response+="ITD: Frank: {}%   S&P500: {}%  VS: {}%\n".format(itd, benchmark_itd, var_itd)
        
        positions = [x for x in listdir(closed_dir) if x[-4:]=='json']
        checks = [x for x in listdir(check_dir) if x[-8:]=='last.csv']
        response +='\nChecking {} symbols in frankenstein.csv..\n'.format(len(checks))
        errors=0
        for i,check in enumerate(checks):
            sym=check.split('_')[0]
            df = pd.read_csv(check_dir+check, index_col='Date')
            df.index=pd.to_datetime(df.index)
            df=df.ix[[x for x in df.index if x.time()<datetime.time(16,0)]]
            if df.iloc[-1].state != 0:
                #check closed trades
                if sym+'.json' in positions:
                    position = sym+'.json'

                    filename = closed_dir + position
                    with open(filename, 'r') as f:
                        order = json.load(f)
                    response += '\n'+sym+' Signal '
                    response += str(df[df.state ==1].iloc[0].name)
                    response += '\nOrder '
                    response += 'Timestamp '+dt.fromtimestamp(int(os.path.getctime(filename))).strftime('%Y-%m-%d %H:%M:%S')
                    response += ' '+str(order)+'\n'                    
                else:
                    errors +=1
                    bar=df.ix[df[df.state ==1].index[0]]
                    print type(bar)
                    if type(bar)==type(pd.Series()):
                        bartime=str(bar.name)
                    else:
                        print bar
                        bartime=str(bar.iloc[-1].name)

                    response += '{}. #{}. {} triggered {} but not transmitted to c2. Check what happened frank.\n'.format(errors, i+1, sym, bartime )
                    
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']\
                    and output['user'] in operators:
                print output_list
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "help"

if __name__ == "__main__":
    api_call = slack_client.api_call("users.list")
    members = api_call.get('members')
    users=[(x.get('name'), x.get('id')) for x in members if 'name' in x] 
    print users
    operators=['U3ZQ523QT','U3Z56KPU0']
    
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print(BOT_NAME+" connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                print channel, command
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
        
'''
if __name__ == "__main__":
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
    else:
        print("could not find bot user with the name " + BOT_NAME)
'''