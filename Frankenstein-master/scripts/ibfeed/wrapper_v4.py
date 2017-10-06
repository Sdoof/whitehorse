from swigibpy import EWrapper
import time
import datetime
import numpy as np
import pandas as pd
import random
from swigibpy import EPosixClientSocket, ExecutionFilter, CommissionReport, Execution, Contract
from swigibpy import Order as IBOrder
from IButils import bs_resolve, action_ib_fill
from pytz import timezone
from threading import Event
import logging
from pytz import timezone
from datetime import datetime as dt
from tzlocal import get_localzone
import re
import psycopg2
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import random
import copy
import pytz
from pytz import timezone
from datetime import datetime as dt
from tzlocal import get_localzone
from sklearn.feature_selection import SelectKBest, chi2, f_regression, RFECV
import os
from dateutil.parser import parse
import logging
import re

sys.path.append("../../")
sys.path.append("../")

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tsdp.settings")
import tsdp
import tsdp.settings as settings
from feed.models import *
import datetime
import time

import csv

try:
    dbstr="dbname=" + settings.DATABASES['default']['NAME'] + \
          " user=" + settings.DATABASES['default']['USER'] + \
          " password=" + settings.DATABASES['default']['PASSWORD'] + \
          " host=" + settings.DATABASES['default']['HOST'] + \
          " port=" + settings.DATABASES['default']['PORT']
          
    c=psycopg2.connect(dbstr)
except:
    print "I am unable to connect to the database."
    
    
MAX_WAIT_SECONDS=10
MEANINGLESS_NUMBER=1729

## This is the reqId IB API sends when a fill is received
FILL_CODE=-1
rtbar={}
rtdict={}
rthist={}
rtfile={}
rtreqid={}
rtbarsize={}
fask={}
fasksize={}
fbid={}
fbidsize={}
fdict={}

bidaskSavedate=dict()

def return_IB_connection_info():
    """
    Returns the tuple host, port, clientID required by eConnect
   
    """
   
    host=""
   
    port=7496
    clientid=random.randint(100,9999)
    
    return (host, port, clientid)

class IBWrapper(EWrapper):
    """
    Callback object passed to TWS, these functions will be called directly by the TWS or Gateway.
    """
    global rtbar
    global rtdict
    
    def init_error(self):
        setattr(self, "flag_iserror", False)
        setattr(self, "error_msg", "")

    def error(self, id, errorCode, errorString):
        """
        error handling, simple for now
       
        Here are some typical IB errors
        INFO: 2107, 2106
        WARNING 326 - can't connect as already connected
        CRITICAL: 502, 504 can't connect to TWS.
            200 no security definition found
            162 no trades
        """
        ## Any errors not on this list we just treat as information
        ERRORS_TO_TRIGGER=[201, 103, 502, 504, 509, 200, 162, 420, 2105, 1100, 478, 201, 399]
       
        if errorCode in ERRORS_TO_TRIGGER:
            errormsg="IB error id %d errorcode %d string %s" %(id, errorCode, errorString)
            print errormsg
            setattr(self, "flag_iserror", True)
            setattr(self, "error_msg", True)
           
        ## Wrapper functions don't have to return anything
       
    """
    Following methods will be called, but we don't use them
    """
       
    def managedAccounts(self, openOrderEnd):
        pass

    def orderStatus(self, reqid, status, filled, remaining, avgFillPrice, permId,
            parentId, lastFilledPrice, clientId, whyHeld):
        pass

    def commissionReport(self, commission):
        print 'Commission %s %s P&L: %s' % (commission.currency,
                                            commission.commission,
                                            commission.realizedPNL)
        filldata=self.data_fill_data
        
        #if reqId not in filldata.keys():
        #    filldata[reqId]={}
            
        execid=commission.execId
        
        execdetails=filldata[execid]
        execdetails['commission']=commission.commission
        execdetails['commission_currency']=commission.currency
        execdetails['realized_PnL']=commission.realizedPNL
        execdetails['yield_redemption_date']=commission.yieldRedemptiondate
        filldata[execid]=execdetails
        self.data_fill_data=filldata
        

    """
    get stuff
    """

    def init_fill_data(self):
        setattr(self, "data_fill_data", {})
        setattr(self, "flag_fill_data_finished", False)

    def add_fill_data(self, reqId, execdetails):
        #if "data_fill_data" not in dir(self):
        #    filldata=execdetails
        #else:
        filldata=self.data_fill_data

        #if reqId not in filldata.keys():
        #    filldata[reqId]={}
            
        #execid=execdetails['execid']
        
        filldata[execdetails['execid']]=execdetails
                        
        setattr(self, "data_fill_data", filldata)


    def execDetails(self, reqId, contract, execution):
        try:
            """
            This is called if 
            
            a) we have submitted an order and a fill has come back
            b) We have asked for recent fills to be given to us 
            
            We populate the filldata object and also call action_ib_fill in case we need to do something with the 
              fill data 
            
            See API docs, C++, SocketClient Properties, Contract and Execution for more details 
            """
            reqId=int(reqId)
           
            execid=execution.execId
            exectime=execution.time
            thisorderid=int(execution.orderId)
            account=execution.acctNumber
            exchange=execution.exchange
            permid=execution.permId
            avgprice=execution.price
            cumQty=execution.cumQty
            clientid=execution.clientId
            symbol=contract.localSymbol
            expiry=contract.expiry
            side=execution.side
            #commission=execution.commission
            currency=contract.currency
            
            
            execdetails=dict( symbol_currency=str(currency), side=str(side), times=str(exectime), orderid=str(thisorderid), qty=int(cumQty), price=float(avgprice), symbol=str(symbol), expiry=str(expiry), clientid=str(clientid), execid=str(execid), account=str(account), exchange=str(exchange), permid=int(permid))
            
            if reqId==FILL_CODE:
                ## This is a fill from a trade we've just done
                action_ib_fill(execdetails)
                
            else:
                ## This is just execution data we've asked for
                self.add_fill_data(reqId, execdetails)
        except Exception as e:
            logging.error("execDetails", exc_info=True)
            
    def execDetailsEnd(self, reqId):
        """
        No more orders to look at if execution details requested
        """

        setattr(self, "flag_fill_data_finished", True)
            

    def init_openorders(self):
        setattr(self, "data_order_structure", {})
        setattr(self, "flag_order_structure_finished", False)

    def add_order_data(self, orderdetails):
        if "data_order_structure" not in dir(self):
            orderdata={}
        else:
            orderdata=self.data_order_structure

        orderid=orderdetails['orderid']
        orderdata[orderid]=orderdetails
                        
        setattr(self, "data_order_structure", orderdata)


    def openOrder(self, orderID, contract, order, orderState):
        """
        Tells us about any orders we are working now
        
        Note these objects are not persistent or interesting so we have to extract what we want
        
        
        """
        
        ## Get a selection of interesting things about the order
        orderdetails=dict(symbol=contract.localSymbol , expiry=contract.expiry,  qty=int(order.totalQuantity) , 
                       side=order.action , orderid=int(orderID), clientid=order.clientId ) 
        
        self.add_order_data(orderdetails)

    def openOrderEnd(self):
        """
        Finished getting open orders
        """
        setattr(self, "flag_order_structure_finished", True)


    def init_nextvalidid(self):
        setattr(self, "data_brokerorderid", None)


    def nextValidId(self, orderId):
        """
        Give the next valid order id 
        
        Note this doesn't 'burn' the ID; if you call again without executing the next ID will be the same
        """
        
        self.data_brokerorderid=orderId


    def init_contractdetails(self, reqId):
        if "data_contractdetails" not in dir(self):
            dict_contractdetails=dict()
        else:
            dict_contractdetails=self.data_contractdetails
        
        dict_contractdetails[reqId]={}
        setattr(self, "flag_finished_contractdetails", False)
        setattr(self, "data_contractdetails", dict_contractdetails)
        

    def contractDetails(self, reqId, contractDetails):
        """
        Return contract details
        
        If you submit more than one request watch out to match up with reqId
        """
        
        contract_details=self.data_contractdetails[reqId]

        contract_details["contractMonth"]=contractDetails.contractMonth
        contract_details["liquidHours"]=contractDetails.liquidHours
        contract_details["longName"]=contractDetails.longName
        contract_details["minTick"]=contractDetails.minTick
        contract_details["tradingHours"]=contractDetails.tradingHours
        contract_details["timeZoneId"]=contractDetails.timeZoneId
        contract_details["underConId"]=contractDetails.underConId
        contract_details["evRule"]=contractDetails.evRule
        contract_details["evMultiplier"]=contractDetails.evMultiplier

        contract2 = contractDetails.summary

        contract_details["expiry"]=contract2.expiry

        contract_details["exchange"]=contract2.exchange
        contract_details["symbol"]=contract2.symbol
        contract_details["secType"]=contract2.secType
        contract_details["currency"]=contract2.currency

    def contractDetailsEnd(self, reqId):
        """
        Finished getting contract details
        """
        
        setattr(self, "flag_finished_contractdetails", True)



    ## portfolio

    def init_portfolio_data(self):
        if "data_portfoliodata" not in dir(self):
            setattr(self, "data_portfoliodata", [])
        if "data_accountvalue" not in dir(self):
            setattr(self, "data_accountvalue", [])
            
        
        setattr(self, "flag_finished_portfolio", False)
        

    def updatePortfolio(self, contract, position, marketPrice, marketValue, averageCost, unrealizedPNL, realizedPNL, accountName):
        """
        Add a row to the portfolio structure
        """

        portfolio_structure=self.data_portfoliodata
                
        portfolio_structure.append((contract.localSymbol, contract.expiry, position, marketPrice, marketValue, averageCost, 
                                    unrealizedPNL, realizedPNL, accountName, contract.currency))

    ## account value
    
    def updateAccountValue(self, key, value, currency, accountName):
        """
        Populates account value dictionary
        """
        account_value=self.data_accountvalue
        
        account_value.append((key, value, currency, accountName))
        

    def accountDownloadEnd(self, accountName):
        """
        Finished can look at portfolio_structure and account_value
        """
        setattr(self, "flag_finished_portfolio", True)

    def is_bar_date(self, dateStr, barSizeSetting):
        if barSizeSetting == '30 mins':
            if re.search(r'\d\d\d\d\d\d  \d\d:[03]0:00', dateStr):
                return True
        elif barSizeSetting == '10 mins':
            if re.search(r'\d\d\d\d\d\d  \d\d:[012345]0:00', dateStr):
                return True
        elif barSizeSetting == '1 hour':
            if re.search(r'\d\d\d\d\d\d  \d\d:00:00', dateStr):
                return True
        else:
            return True
        return False
    def historicalData(self, reqId, date, open, high,
                       low, close, volume,
                       barCount, WAP, hasGaps):
        try:
            global rtbar
            global rtdict
            global rthist
            global rtbarsize
            global rtfile
            
            dbcontract=rtfile[reqId]
            barSizeSetting=rtbarsize[reqId]
            sym=rtdict[reqId]
            data=rtbar[reqId]
            if date[:8] == 'finished':
                logging.info("Req ID: " + str(reqId) + " History request complete " + str(data.shape[0]) + " Records")
                rthist[reqId].set()
                data=data.sort_index()
            else:
                if self.is_bar_date(str(date), barSizeSetting):
                    quote={ 'date':date,
                           'open':open,
                           'high':high,
                           'low':low,
                           'close':close,
                           'volume':volume,
                           'wap':WAP,
                        }
                    self.saveQuote(dbcontract, quote)
                        
                    data.loc[date] = [open,high,low,close,volume,WAP]
                else:  
                    print "Skipping Off date History %s - open: %s, high: %s, low: %s, close: %s, volume: %d"\
                              % (date, open, high, low, close, volume)
            rtbar[reqId]=data
        
        except Exception as e:
            logging.error("historicalData", exc_info=True)
            
    def saveQuote(self, dbcontract, quote):
        #if quote.has_key('wap'):
        #    print ' wap:' + str(quote['wap']) 
        
        eastern=timezone('US/Eastern')
        date=parse(quote['date']).replace(tzinfo=eastern)   
        bar_list=Feed.objects.filter(date=date).filter(instrument_id=dbcontract.id).filter(frequency=dbcontract.frequency)
        #print "close Bar: " + str(dbcontract.id) + " freq ",dbcontract.frequency, " date:" + str(quote['date']) + "date ",date, " open: " + str(quote['open']) + " high:"  + str(quote['high']) + ' low:' + str(quote['low']) + ' close: ' + str(quote['close']) + ' volume:' + str(quote['volume']) 
        if bar_list and len(bar_list) > 0:
            bar=bar_list[0]
            print "found bar id",bar.id
        else:
            bar=Feed()
            bar.instrument_id=dbcontract.id
            bar.frequency=dbcontract.frequency
            bar.date=date
        bar.open= quote['open']
        bar.high= quote['high']
        bar.low= quote['low']
        bar.close= quote['close']
        bar.volume= quote['volume']
        if quote.has_key('wap'):
            bar.wap=quote['wap']
        bar.save()
        #print "saving bar id",bar.id
        
    def realtimeBar(self, reqId, time, open, high, low, close, volume, wap, count):
        try:
            """
            Note we don't use all the information here
            
            Just append close prices. 
            """
           
            global pricevalue
            global finished
            global rtbar
            global rtdict
            global rtfile
            sym=rtdict[reqId]
            data=rtbar[reqId]
            dbcontract=rtfile[reqId]
            
            eastern=timezone('US/Eastern')
            
            time=datetime.datetime.fromtimestamp(
                        int(time), eastern
                    ).strftime('%Y%m%d  %H:%M:00') 
            #time=time.astimezone(eastern).strftime('%Y-%m-%d %H:%M:00') 
            
            if time in data.index:
                   
                quote=data.loc[time].copy()
                if high > quote['high']:
                    quote['high']=high
                if low < quote['low']:
                    quote['low']=low
                quote['close']=close
                quote['volume']=quote['volume'] + volume
                if quote['volume'] < 0:
                    quote['volume'] = 0 
                if wap:
                    quote['wap']=wap
                else:
                    quote['wap']=0
                data.loc[time]=quote
                #print "Update Bar: " + sym + " date:" + str(time) + "open: " + str(quote['open']) + " high:"  + str(quote['high']) + ' low:' + str(quote['low']) + ' close: ' + str(quote['close']) + ' volume:' + str(quote['volume']) + ' wap:' + str(wap) + ' count:' + str(data.shape[0])
                
            else:
                if len(data.index) > 1:
                    
                    data=data.sort_index()          
                    
                    quote=data.reset_index().iloc[-1].copy()
                    self.saveQuote(dbcontract, quote)
                    print "close Bar: " + sym + " date:" + str(quote['date']) + " open: " + str(quote['open']) + " high:"  + str(quote['high']) + ' low:' + str(quote['low']) + ' close: ' + str(quote['close']) + ' volume:' + str(quote['volume']) + ' wap:' + str(wap) + ' count:' + str(data.shape[0])
                    
                    #gotbar=pd.DataFrame([[quote['date'], quote['open'], quote['high'], quote['low'], quote['close'], quote['volume'], sym]], columns=['date','open','high','low','close','volume','Symbol']).set_index('date')
                    #gotbar.to_csv('./data/bars/' + sym + '.csv')
                print "New Bar:   " + sym + " date:" + str(time) + " open: " + str(open) + " high:"  + str(high) + ' low:' + str(low) + ' close: ' + str(close) + ' volume:' + str(volume) + ' wap:' + str(wap) + ' count:' + str(data.shape[0])
                data=data.reset_index().append(pd.DataFrame([[time, open, high, low, close, volume, wap]], columns=['date','open','high','low','close','volume','wap'])).set_index('date')
                
                
            rtbar[reqId]=data
        except Exception as e:
            logging.error("realtimeBar", exc_info=True)
        
        #pricevalue.append(close)

    def init_tickdata(self, TickerId):
        if "data_tickdata" not in dir(self):
            tickdict=dict()
        else:
            tickdict=self.data_tickdata

        tickdict[TickerId]=[np.nan]*4
        setattr(self, "data_tickdata", tickdict)


    def tickString(self, TickerId, field, value):
        global fasksize
        global fbidsize
        global fask
        global fbid
        marketdata=self.data_tickdata[TickerId]

        
        print 'tickString: tickerID',TickerId,' field', field,'value',value
        
        ## update string ticks

        tickType=field

        if int(tickType)==0:
            ## bid size
            marketdata[0]=int(value)
            fbidsize[TickerId]=int(value)
        elif int(tickType)==3:
            ## ask size
            marketdata[1]=int(value)
            fasksize[TickerId]=int(value)
        elif int(tickType)==1:
            ## bid
            marketdata[0][2]=float(value)
            fbid[TickerId]=float(value)
        elif int(tickType)==2:
            ## ask
            marketdata[0][3]=float(value)
            fask[TickerId]=float(value)
        
    
    
    def tickGeneric(self, TickerId, tickType, value):
        
        global fasksize
        global fbidsize
        global fask
        global fbid
        global bidaskSavedate
        marketdata=self.data_tickdata[TickerId]

        print 'tickGeneric: tickerID',TickerId,'ticktype',tickType,'value',value
        
        ## update generic ticks

        if int(tickType)==0:
            ## bid size
            marketdata[0]=int(value)
            fbidsize[TickerId]=int(value)
        elif int(tickType)==3:
            ## ask size
            marketdata[1]=int(value)
            fasksize[TickerId]=int(value)
        elif int(tickType)==1:
            ## bid
            marketdata[2]=float(value)
            fbid[TickerId]=float(value)
        elif int(tickType)==2:
            ## ask
            marketdata[3]=float(value)
            fask[TickerId]=float(value)
        try:
            global rtdict
            sym=rtdict[TickerId]
            
            if not bidaskSavedate.has_key(sym) or (int(time.time()) - bidaskSavedate[sym]) > 5:
                if fbid.has_key(TickerId) and fask.has_key(TickerId):
                    print "tickGeneric SYM: " + sym + " ", fbid[TickerId], fask[TickerId]
                    bidaskSavedate[sym]=int(time.time())
                
                    eastern=timezone('US/Eastern')
                    nowdate=datetime.datetime.now(get_localzone()).astimezone(eastern).strftime('%Y%m%d %H:%M:%S') 
                    if fbid.has_key(TickerId) > 0 and fask[TickerId] > 0:
                        self.bidask_to_csv(sym, nowdate, fbid[TickerId], fask[TickerId])
                
        except Exception as e:
            logging.error("tickGeneric", exc_info=True)
        
        
    def bidask_to_csv(self, ticker, date, bid, ask):
        data=pd.DataFrame([[date, bid, ask]], columns=['date','Bid','Ask'])
        data=data.set_index('date')
        if bid > 0 and ask > 0:
            data.to_csv('./data/bidask/' + ticker + '.csv')
        return data
        
    def tickSize(self, TickerId, tickType, size):
        global fasksize
        global fbidsize
        ## update ticks of the form new size
        
        marketdata=self.data_tickdata[TickerId]

        
        if int(tickType)==0:
            ## bid
            if not fbidsize.has_key(TickerId):
                fbidsize[TickerId]=0
            marketdata[0]=int(size)
            fbidsize[TickerId]+=int(size)
        elif int(tickType)==3:
            ## ask
            if not fasksize.has_key(TickerId):
                fasksize[TickerId]=0
            marketdata[1]=int(size)
            fasksize[TickerId]+=int(size)
        
        print "tickSize: tickerID",TickerId,"ASKSIZE: " + str(marketdata[0]) +  " BIDSIZE: " + str(marketdata[1])

   
    def tickPrice(self, TickerId, tickType, price, canAutoExecute):
        ## update ticks of the form new price
        global fask
        global fbid
        global bidaskSavedate
        marketdata=self.data_tickdata[TickerId]
        
        print 'tickPrice: tickerID',TickerId,'ticktype',tickType,'price',price 
        if int(tickType)==1:
            ## bid
            marketdata[2]=float(price)
            fbid[TickerId]=float(price)
        elif int(tickType)==2:
            ## ask
            marketdata[3]=float(price)
            fask[TickerId]=float(price)
        try:
            global rtdict
            sym=rtdict[TickerId]
           
            if not bidaskSavedate.has_key(sym) or (int(time.time()) - bidaskSavedate[sym]) > 5:
                if fbid.has_key(TickerId) and fask.has_key(TickerId):
                    bidaskSavedate[sym]=int(time.time())
                    print "tickPrice SYM: " + sym + " ", fbid[TickerId], fask[TickerId], " Timer: ",(int(time.time()) - bidaskSavedate[sym])
                    
                
                    eastern=timezone('US/Eastern')
                    nowdate=datetime.datetime.now(get_localzone()).astimezone(eastern).strftime('%Y%m%d %H:%M:%S') 
                    
                    if fbid.has_key(TickerId) > 0 and fask[TickerId] > 0:
                        self.bidask_to_csv(sym, nowdate, fbid[TickerId], fask[TickerId])
                    
        except Exception as e:
            logging.error("tickPrice", exc_info=True)
        #print "tickPrice: ASK: " + str(marketdata[3]) +  " BID: " + str(marketdata[2])

    def updateMktDepth(self, id, position, operation, side, price, size):
        print 'updateMktDepth: tickerID',id,'position',position,'operation',operation,'side',side,'price',price,'size',size 
        
        """
        Only here for completeness - not required. Market depth is only available if you subscribe to L2 data.
        Since I don't I haven't managed to test this.
        
        Here is the client side call for interest
        
        tws.reqMktDepth(999, ibcontract, 9)
        
        """
        pass

        
    def tickSnapshotEnd(self, tickerId):
        
        print "No longer want to get %d" % tickerId

class IBclient(object):
    """
    Client object
    
    Used to interface with TWS for outside world, does all handling of streaming waiting etc
    
    Create like this
    callback = IBWrapper()
    client=IBclient(callback)
    We then use various methods to get prices etc
    """
    def __init__(self, callback):
        """
        Create like this
        callback = IBWrapper()
        client=IBclient(callback)
        """
        
        tws = EPosixClientSocket(callback)
        (host, port, clientid)=return_IB_connection_info()
        tws.eConnect(host, port, clientid)

        self.tws=tws
        self.cb=callback
        self.accountid=''

    def get_contract_details(self, ibcontract, reqId=MEANINGLESS_NUMBER):
    
        """
        Returns a dictionary of contract_details
        
        
        """
        
        self.cb.init_contractdetails(reqId)
        self.cb.init_error()
    
        self.tws.reqContractDetails(
            reqId,                                         # reqId,
            ibcontract,                                   # contract,
        )
    

        finished=False
        iserror=False
        
        start_time=time.time()
        while not finished and not iserror:
            finished=self.cb.flag_finished_contractdetails
            iserror=self.cb.flag_iserror
            
            if (time.time() - start_time) > MAX_WAIT_SECONDS:
                finished=True
                iserror=True
            pass
    
        contract_details=self.cb.data_contractdetails[reqId]
        if iserror or contract_details=={}:
            print self.cb.error_msg
            print "Problem getting details"
            return None
    
        return contract_details



    def get_next_brokerorderid(self):
        """
        Get the next brokerorderid
        """


        self.cb.init_error()
        self.cb.init_nextvalidid()
        

        start_time=time.time()
        
        ## Note for more than one ID change '1'
        self.tws.reqIds(1)

        finished=False
        iserror=False

        while not finished and not iserror:
            brokerorderid=self.cb.data_brokerorderid
            finished=brokerorderid is not None
            iserror=self.cb.flag_iserror
            if (time.time() - start_time) > MAX_WAIT_SECONDS:
                finished=True
            pass

        
        if brokerorderid is None or iserror:
            print self.cb.error_msg
            print "Problem getting next broker orderid"
            return None
        
        return brokerorderid


    def place_new_IB_order(self, ibcontract, trade, lmtPrice, orderType, orderid=None):
        """
        Places an order
        
        Returns brokerorderid
    
        raises exception if fails
        """
        iborder = IBOrder()
        iborder.action = bs_resolve(trade)
        iborder.lmtPrice = lmtPrice
        iborder.orderType = orderType
        iborder.totalQuantity = abs(trade)
        iborder.tif='DAY'
        iborder.transmit=True

        ## We can eithier supply our own ID or ask IB to give us the next valid one
        if orderid is None:
            print "Getting orderid from IB"
            orderid=self.get_next_brokerorderid()
            
        print "Using order id of %d" % orderid
    
         # Place the order
        self.tws.placeOrder(
                orderid,                                    # orderId,
                ibcontract,                                   # contract,
                iborder                                       # order
            )
    
        return orderid

    def any_open_orders(self):
        """
        Simple wrapper to tell us if we have any open orders
        """
        
        return len(self.get_open_orders())>0

    def get_open_orders(self):
        """
        Returns a list of any open orders
        """
        
        
        self.cb.init_openorders()
        self.cb.init_error()
                
        start_time=time.time()
        self.tws.reqAllopenOrders()
        iserror=False
        finished=False
        
        while not finished and not iserror:
            finished=self.cb.flag_order_structure_finished
            iserror=self.cb.flag_iserror
            if (time.time() - start_time) > MAX_WAIT_SECONDS:
                ## You should have thought that IB would teldl you we had finished
                finished=True
            pass
        
        order_structure=self.cb.data_order_structure
        if iserror:
            print self.cb.error_msg
            print "Problem getting open orders"
    
        return order_structure    
    


    def get_executions(self, reqId=MEANINGLESS_NUMBER):
        try:
            """
            Returns a list of all executions done today
            """
            assert type(reqId) is int
            if reqId==FILL_CODE:
                raise Exception("Can't call get_executions with a reqId of %d as this is reserved for fills %d" % reqId)
    
            self.cb.init_fill_data()
            self.cb.init_error()
            
            ## We can change ExecutionFilter to subset different orders
            ef=ExecutionFilter();
            #ef.m_time="20160101"
            #ef.client_id=0;
            t=2;
           
            while t > 1:
                reqId=reqId+1
                self.tws.reqExecutions(reqId, ef)
        
                iserror=False
                finished=False
                
                start_time=time.time()
                
                while not finished and not iserror:
                    finished=self.cb.flag_fill_data_finished
                    iserror=self.cb.flag_iserror
                    if (time.time() - start_time) > MAX_WAIT_SECONDS:
                        finished=True
                    pass
            
                if iserror:
                    print self.cb.error_msg
                    print "Problem getting executions"
                
                t=t-1;
                
            execlist=self.cb.data_fill_data.values()
            
            return execlist
        except Exception as e:
            logging.error("get_execution", exc_info=True)       
        
    def get_IB_account_data(self):
        try:
            self.cb.init_portfolio_data()
            self.cb.init_error()
            
            ## Turn on the streaming of accounting information
            
            self.tws.reqAccountUpdates(True, self.accountid)
            
            start_time=time.time()
            finished=False
            iserror=False
    
            while not finished and not iserror:
                finished=self.cb.flag_finished_portfolio
                iserror=self.cb.flag_iserror
    
                if (time.time() - start_time) > MAX_WAIT_SECONDS:
                    finished=True
                    print "Didn't get an end for account update, might be missing stuff"
                pass
            if iserror:
                print self.cb.error_msg
                print "Problem getting details"
                return None
    
    
            
            ## Turn off the streaming
            ## Note portfolio_structure will also be updated
            #self.tws.reqAccountUpdates(False, self.accountid)
    
            portfolio_data=self.cb.data_portfoliodata
            account_value=self.cb.data_accountvalue
    
            return (account_value, portfolio_data)
        except Exception as e:
            logging.error("get_account", exc_info=True)       


    def get_IBAsk(self, symname):
        global fdict
        global fask
        tickerid=fdict[symname]
        if tickerid in fask:
            return fask[tickerid]
        else:
            return -1
        
    def get_IBBid(self, symname):
        global fdict
        global fbid
        tickerid=fdict[symname]
        if tickerid in fbid:
            return fbid[tickerid]
        else:
            return -1
    def get_IB_market_data(self, ibcontract, tickerid, dbcontract):     
        try:
            """
            Returns granular market data
            
            Returns a tuple (bid price, bid size, ask price, ask size)
            
            """
            
            ## initialise the tuple
            global fdict
            global rtdict
            global rtfile
            symname=ibcontract.localSymbol
            if ibcontract.secType == 'CASH':
                symname=ibcontract.localSymbol + ibcontract.currency
            rtfile[tickerid]=dbcontract            
            fdict[symname]=tickerid
            rtdict[tickerid]=symname
            self.cb.init_tickdata(tickerid)
            self.cb.init_error()
            
            # Request a market data stream 
            self.tws.reqMktData(
                    tickerid,
                    ibcontract,
                    "",
                    False)       
    
            marketdata=self.cb.data_tickdata[tickerid]
            return marketdata
        except Exception as e:
            logging.error("get_IB_market_data", exc_info=True)   
        
    def get_realtimebar(self, ibcontract, tickerid, whatToShow, dbcontract, sec_interval=5):
        try:
            """
            Returns a list of snapshotted prices, averaged over 'real time bars'
            
            tws is a result of calling IBConnector()
            
            """
            
            data = pd.DataFrame({}, columns=['date','open','high','low','close','volume','wap']).set_index('date')

            tws=self.tws
            
            global finished
            global iserror
            global pricevalue
            global rtbar
            global rtdict
            global rtfile
            global rtreqid
            iserror=False
            
            finished=False
            pricevalue=[]
            symName=ibcontract.localSymbol
            if ibcontract.secType == 'CASH':
                symName=ibcontract.localSymbol + ibcontract.currency
            
            rtreqid[symName]=tickerid
            rtdict[tickerid]=symName
            rtfile[tickerid]=dbcontract
            if tickerid not in rtbar:
                rtbar[tickerid]=data
            
            contract=ibcontract
            logging.info("\nRequesting Real Time data for " + contract.localSymbol + " " + contract.currency + " " + contract.exchange + " " + contract.secType)
        
            # Request current price in 5 second increments
            # It turns out this is the only way to do it (can't get any other increments)
            
            tws.reqRealTimeBars(
                    tickerid,                                          # tickerId,
                    ibcontract,                                   # contract,
                    5, 
                    whatToShow,
                    0)
        
        
            start_time=time.time()
        
            
            return pricevalue
        except Exception as e:
            logging.error("get_realtimebar", exc_info=True)   
        
    def get_history(self, date, contract, whatToShow, dbcontract,tickerid, minDataPoints, durationStr, barSizeSetting):
        try:
            data = pd.DataFrame({}, columns=['date','open','high','low','close','volume','wap']).set_index('date')
            
            WAIT_TIME=60
            global rtbar
            global rtdict
            global rthist
            global rtreqid
            global rtbarsize
            global rtfile
            rtdict[tickerid]=contract.localSymbol
            ticker = contract.localSymbol
            rtbarsize[tickerid]=barSizeSetting
            rtfile[tickerid]=dbcontract
            
            if contract.secType =='CASH':
                rtdict[tickerid]=contract.localSymbol + contract.currency
                ticker=contract.localSymbol + contract.currency
            
            if tickerid not in rtbar:
                rtbar[tickerid]=data
            
            tws = self.tws

            rtreqid[ticker]=tickerid
            
            logging.info("Req ID: " + str(tickerid) + " Requesting historical data End date: " + date + " for " + contract.localSymbol + " " + contract.currency + " " + contract.exchange + " " + contract.secType)
        
            # Request some historical data.
            rthist[tickerid]=Event()
            #for enddateTime in getHistLoop:
            tws.reqHistoricalData(
                tickerid,                                         # tickerId,
                contract,                                   # contract,
                date,                            #enddateTime
                durationStr,                                      # durationStr,
                barSizeSetting,                                    # barSizeSetting,
                whatToShow,                                   # whatToShow,
                0,                                          # useRTH,
                1                                         # formatdate
                )
        
        
            print("====================================================================")
            print(" %s History requested, waiting %ds for TWS responses" % (date, WAIT_TIME))
            print("====================================================================")
            
            try:
                rthist[tickerid].wait(timeout=WAIT_TIME)
            except KeyboardInterrupt:
                pass
            finally:
                if not rthist[tickerid].is_set():
                    print('Failed to get history within %d seconds' % WAIT_TIME)
            
           
            return rtbar[tickerid]
        except Exception as e:
            logging.error("get_history", exc_info=True)   
        
    def proc_history(self, tickerid, contract ,data,barSizeSetting, dbcontract):
        try:
            WAIT_TIME=60
            global rtbar
            global rtdict
            global rthist
            global rtreqid
            global rtbarsize
            global rtfile
            rtfile[tickerid]=dbcontract            
            
            rtbarsize[tickerid]=barSizeSetting
            iserror=False
            
            sym=contract.localSymbol 
            currency=contract.currency
            
            if type == 'CASH':
                rtdict[tickerid]=sym+currency
                rtreqid[sym+currency]=tickerid
            else:
                rtdict[tickerid]=sym
                rtreqid[sym]=tickerid
                
            if tickerid not in rtbar:
                rtbar[tickerid]=pd.DataFrame({}, columns=['date','open','high','low','close','volume']).set_index('date')
                    
            
            data=data.reset_index()
            for i in data.index:
                tick=data.ix[i]
                
                self.cb.historicalData(tickerid, tick['date'],tick['open'],tick['high'],
                                        tick['low'],tick['close'],tick['volume'],-1,-1,-1)
               
                     
            return rtbar[tickerid]
        except Exception as e:
            logging.error("proc_history", exc_info=True)   

    def get_bar(self, symname):
        
        global rtreqid
        global rtbar
        tickerid=rtreqid[symname]
        logging.info("get_bar:" + symname + ":" + str(tickerid))
        if tickerid in rtbar:
            return rtbar[tickerid]
        else:
            return pd.DataFrame()