import matplotlib.pyplot as plt
import matplotlib.animation as anim
import time
import matplotlib.ticker as tick
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import statsmodels.tsa.stattools as ts
import numpy as np
import sys
import time
from numpy import zeros, ones, flipud, log
from numpy.linalg import inv, eig, cholesky as chol
import talib as ta
import logging
import    os
import re
import datetime as datetime
import dateutil
sys.path.append("../")
import paper.calc as calc
from statsmodels.regression.linear_model import OLS
#from numba import jit

##### Do not change this function definition ####
pairSeries=dict()
pairHSeries=dict()
pairLSeries=dict()
pairVSeries=dict()
pairOSeries=dict()
tsPairratio=dict()
tsZscore=dict()
tsDates=dict()
indSmaZscore=dict()
intDatapoints=84
sentEntryOrder = dict()
sentExitOrder = dict()
entryOrderPrice =dict()
exitOrderPrice=dict() 
crossAbove=dict()
crossBelow=dict()
intSMALength = 30
instPair1Factor=1
instPair2Factor=1
dblQty=1
dblQty2=1

dblUpperThreshold = 1;
dblLowerThreshold = 0;
dblRiskPer = 0.05;
dblTargetPer = 0.05;
dblStartStop = 0.06;
dblPlaceStop = 0.14;
dblBBUOrder = 2;
dblBBLOrder = 2;
sigDF=pd.DataFrame();

def procBar(bar1, bar2, pos, trade):
    global pairSeries
    global pairHSeries
    global pairLSeries
    global pairVSeries
    global tsPairratio
    global tsZscore
    global tsDates
    global indSmaZscore
    global intDatapoints
    global sentEntryOrder 
    global sentExitOrder 
    global entryOrderPrice 
    global exitOrderPrice 
    global intSMALength 
    global dblUpperThreshold 
    global dblLowerThreshold 
    global instPair1Factor
    global instPair2Factor
    global dblQty
    global dblQty2 
    global crossAbove
    global crossBelow
    global sigDF
    
    #logging.info('procBar: %s %s %s' % (bar1, pos, trade))
    bar1=bar1.copy()
    bar2=bar2.copy()
    if bar1['Close'] > 0 and bar2['Close'] > 0:
        xd = bar1['Close'] * instPair1Factor
        yd = bar2['Close'] * instPair2Factor
        sym1=bar1['Symbol']
        sym2=bar2['Symbol']
        bar1['Date']=datetime.datetime.fromtimestamp(float(bar1['Date']))
        bar2['Date']=datetime.datetime.fromtimestamp(float(bar2['Date']))
        logging.info("s106:procBar:" + sym1 + "," + sym2 + "," + str(bar1['Date']))
        if not pairSeries.has_key(sym1):
            pairSeries[sym1]=list()
            pairHSeries[sym1]=list()
            pairLSeries[sym1]=list()
            pairVSeries[sym1]=list()
        if not pairSeries.has_key(sym2):
            pairSeries[sym2]=list()
            pairHSeries[sym2]=list()
            pairLSeries[sym2]=list()
            pairVSeries[sym2]=list()
        if not tsPairratio.has_key(sym1+sym2):
            tsPairratio[sym1+sym2]=list()
        if not tsPairratio.has_key(sym2+sym1):
            tsPairratio[sym2+sym1]=list()
        if not tsZscore.has_key(sym1+sym2):
            tsZscore[sym1+sym2]=list()
        if not tsZscore.has_key(sym2+sym1):
            tsZscore[sym2+sym1]=list()
        if not tsDates.has_key(sym1):
            tsDates[sym1]=list()
        if not tsDates.has_key(sym2):
            tsDates[sym2]=list()
        if not tsDates.has_key(sym1+sym2):
            tsDates[sym1+sym2]=list()
        if not tsDates.has_key(sym2+sym1):
            tsDates[sym2+sym1]=list()
        if not crossAbove.has_key(sym1+sym2):
            crossAbove[sym1+sym2]=False
        if not crossBelow.has_key(sym1+sym2):
            crossBelow[sym1+sym2]=False
        if not sentEntryOrder.has_key(sym1+sym2):
            sentEntryOrder[sym1+sym2]=False
        if not sentExitOrder.has_key(sym1+sym2):
            sentExitOrder[sym1+sym2]=False
        
        '''
        if len(tsDates[sym1]) < 1 or datetime.datetime(bar1['Date'].year, bar1['Date'].month, bar1['Date'].day) > datetime.datetime(tsDates[sym1][0].year, tsDates[sym1][0].month, tsDates[sym1][0].day) + dateutil.relativedelta.relativedelta(days=1):
            pairSeries[sym1]=list()
            pairHSeries[sym1]=list()
            pairLSeries[sym1]=list()
            pairVSeries[sym1]=list()
            pairSeries[sym2]=list()
            pairHSeries[sym2]=list()
            pairLSeries[sym2]=list()
            pairVSeries[sym2]=list()
            tsPairratio[sym1+sym2]=list()
            tsPairratio[sym2+sym1]=list()
            tsZscore[sym1+sym2]=list()
            tsZscore[sym2+sym1]=list()
            tsDates[sym1]=list()
            tsDates[sym2]=list()
            tsDates[sym1+sym2]=list()
            crossAbove[sym1+sym2]=False
            crossBelow[sym1+sym2]=False
            #sentEntryOrder[sym1+sym2]=False
            #sentExitOrder[sym1+sym2]=False
        '''
             
        if bar1['Date'] not in tsDates[sym1]:
            pairSeries[sym1].append(bar1['Close'])
            pairHSeries[sym1].append(bar1['High'])
            pairLSeries[sym1].append(bar1['Low'])
            pairVSeries[sym1].append(bar1['Volume'])
            tsDates[sym1].append(bar1['Date'])
        
        if bar2['Date'] not in tsDates[sym2] and sym1 != sym2:
            pairSeries[sym2].append(bar2['Close'])
            pairHSeries[sym2].append(bar2['High'])
            pairLSeries[sym2].append(bar2['Low'])
            pairVSeries[sym2].append(bar2['Volume'])
            tsDates[sym2].append(bar2['Date'])

        dblRatioData = bar1['Close'] / bar2['Close'];
        tsPairratio[sym1+sym2].append( dblRatioData );
        
        if sym1 != sym2:
            dblRatioData2 = bar2['Close'] / bar1['Close'];
            tsPairratio[sym2+sym1].append( dblRatioData2 );

        if len(tsPairratio[sym1+sym2])< intDatapoints or len(tsPairratio[sym2+sym1]) < intDatapoints:
            return []

        iStart = len(tsPairratio[sym1+sym2]) - intDatapoints;
        iEnd = len(tsPairratio[sym1+sym2]) - 1;
        dblAverage = np.mean(tsPairratio[sym1+sym2][iStart:iEnd]);
        dblRatioStdDev = np.std(tsPairratio[sym1+sym2][iStart:iEnd]);
        dblResidualsData = (dblRatioData - dblAverage);
        dblZscoreData = (dblRatioData - dblAverage) / dblRatioStdDev;
        tsZscore[sym1+sym2].append(dblZscoreData)
        tsDates[sym1+sym2].append(bar1['Date'])
        
        if sym1 != sym2:
            iStart2 = len(tsPairratio[sym2+sym1]) - intDatapoints;
            iEnd2 = len(tsPairratio[sym2+sym1]) - 1;
            dblAverage2 = np.mean(tsPairratio[sym2+sym1][iStart2:iEnd2]);
            dblRatioStdDev2 = np.std(tsPairratio[sym2+sym1][iStart2:iEnd2]);
            dblResidualsData2 = (dblRatioData2 - dblAverage2);
            dblZscoreData2 = (dblRatioData2 - dblAverage2) / dblRatioStdDev2;
            tsZscore[sym2+sym1].append(dblZscoreData2)
            tsDates[sym2+sym1].append(bar2['Date'])
         
         
        
        signals=pd.DataFrame()
        #signals['Date']=tsDates[sym1+sym2]
        #signals['tsZscore']=tsZscore[sym1+sym2]
        #signals['tsZscore2']=tsZscore[sym2+sym1]
        #signals['indSmaZscore']=pd.rolling_mean(signals['tsZscore'], intSMALength, min_periods=1)
        #signals['indSmaZscore2']=pd.rolling_mean(signals['tsZscore2'], intSMALength, min_periods=1)    
        
        idxRanges=np.arange(100)
        endDate=tsDates[sym1][-1]
        startIdx=-1
        for idx in idxRanges:
            startIdx=-idx-1
            startDate=tsDates[sym1][-startIdx-1]
            if startDate.day != endDate.day:
                break
            
        signals['Date']=tsDates[sym1][-startIdx:]
        signals['indEMA9']=ta.EMA(np.array(pairSeries[sym1]), timeperiod=9)[-startIdx:]
        signals['indEMA20']=ta.EMA(np.array(pairSeries[sym1]), timeperiod=20)[-startIdx:]
        
        
        df=pd.DataFrame({ 'v' : pairVSeries[sym1][-startIdx:], 
                          'h' : pairHSeries[sym1][-startIdx:], 
                          'l' : pairLSeries[sym1][-startIdx:], 
                         },
                         columns=['v','h','l'] )
        
        signals['vwap_pandas'] = (df.v*(df.h+df.l)/2).cumsum() / df.v.cumsum()
        
        v = df.v.values
        h = df.h.values
        l = df.l.values

        
        signals['vwap'] = np.cumsum(v*(h+l)/2) / np.cumsum(v)
        #signals['vwap_numba'] = vwap(v,h,l)
        
        '''
        (signals['indBbu'], signals['indBbm'], signals['indBbl']) = ta.BBANDS(
            np.array(signals['tsZscore']), 
            timeperiod=intSMALength,
            # number of non-biased standard deviations from the mean
            nbdevup=dblBBUOrder,
            nbdevdn=dblBBLOrder,
            # Moving average type: simple moving average here
            matype=0)
            
        (signals['indBbu2'], signals['indBbm2'], signals['indBbl2']) = ta.BBANDS(
            np.array(signals['tsZscore2']), 
            timeperiod=intSMALength,
            # number of non-biased standard deviations from the mean
            nbdevup=dblBBUOrder,
            nbdevdn=dblBBLOrder,
            # Moving average type: simple moving average here
            matype=0)
        
        
        signals['indSmaZscore']=ta.SMA(np.array(signals['tsZscore']), intSMALength)      
        signals['indSmaZscore2']=ta.SMA(np.array(signals['tsZscore2']), intSMALength)        
        '''
        signals=signals.set_index('Date')
               
        if len(signals['indEMA9']) < 5: # or len(signals['indSmaZscore']) < 5 or len(signals['indSmaZscore2']) < 5:
            return [];

        #updateCointData();

        
        if trade:
                #print strOrderComment
                
                #(z1CBBbu, z1CABbu)=crossCheck(signals, 'bb'+sym1+sym2, 'tsZscore', 'indBbu')
                #(z1CBBbl, z1CABbl)=crossCheck(signals, 'bb2'+sym1+sym2, 'tsZscore2','indBbl')
                
                #print ' crossAbove: ' + str(crossAbove) + ' crossBelow: ' + str(crossBelow)
                #crossBelow = signals['tsZscore'].iloc[-1] >= signals['indSmaZscore'].iloc[-1] and crossBelow.any()
                #crossAbove = signals['tsZscore'].iloc[-1] <= signals['indSmaZscore'].iloc[-1] and crossAbove.any()
                #print ' crossAbove: ' + str(crossAbove) + ' crossBelow: ' + str(crossBelow)
    
                sigDF=signals
                (crossBelow[sym1+sym2+'EMAVWAP'], crossAbove[sym1+sym2+'EMAVWAP'])=crossCheck(signals, sym1+sym2+'EMAVWAP', 'indEMA9', 'vwap')           
                (crossBelow[sym1+sym2+'EMA9_20'], crossAbove[sym1+sym2+'EMA9_20'])=crossCheck(signals, sym1+sym2+'EMA9_20', 'indEMA9', 'indEMA20')
                       
                if not sentEntryOrder[sym1+sym2] and not pos.has_key(bar1['Symbol']): # and not pos.has_key(bar2['Symbol']):
                    logging.info('procBar:EMA9 and VWAP crossCheck (Below, Above): %s %s' % (crossBelow[sym1+sym2+'EMAVWAP'], crossAbove[sym1+sym2+'EMAVWAP']))
                    logging.info('procBar:EMA9 and EMA20 crossCheck (Below, Above): %s %s' % (crossBelow[sym1+sym2+'EMA9_20'], crossAbove[sym1+sym2+'EMA9_20']))
                    strOrderComment =  '{Entry: 1 | Exit: 0 | symPair: ' + sym1+sym2 + ' | EMA9: ' + str(round(signals.iloc[-1]['indEMA9'], 2)) + ' | EMA20: ' + str(round(signals.iloc[-1]['indEMA20'], 2)) + ' | vwap: ' + str(round(signals.iloc[-1]['vwap'], 2)) + '}';
                    
                    
                    if crossAbove[sym1+sym2+'EMAVWAP']:
                        
                        sentEntryOrder[sym1+sym2] = True
                        sentExitOrder[sym1+sym2] = False
                        entryOrderPrice[sym1+sym2]=bar1['Close']
                        return ([[bar1['Symbol'], -abs(dblQty), strOrderComment]])
                    elif crossBelow[sym1+sym2+'EMAVWAP']:
                        sentEntryOrder[sym1+sym2] = True
                        sentExitOrder[sym1+sym2] = False
                
                        entryOrderPrice[sym1+sym2]=bar1['Close']
                        return ([[bar1['Symbol'], abs(dblQty), strOrderComment]])
    
                elif not sentExitOrder[sym1+sym2] and pos.has_key(bar1['Symbol']): # and pos.has_key(bar2['Symbol']):
                    logging.info('procBar:EMA9 and VWAP crossCheck (Below, Above): %s %s' % (crossBelow[sym1+sym2+'EMAVWAP'], crossAbove[sym1+sym2+'EMAVWAP']))
                    logging.info('procBar:EMA9 and EMA20 crossCheck (Below, Above): %s %s' % (crossBelow[sym1+sym2+'EMA9_20'], crossAbove[sym1+sym2+'EMA9_20']))
                    strOrderComment =  '{Entry: 0 | Exit: 1 | symPair: ' + sym1+sym2 + ' | EMA9: ' + str(round(signals.iloc[-1]['indEMA9'], 2)) + ' | EMA20: ' + str(round(signals.iloc[-1]['indEMA20'], 2)) + ' | vwap: ' + str(round(signals.iloc[-1]['vwap'], 2)) + '}';

                    openAt=entryOrderPrice[sym1+sym2]
                    closeAt=bar1['Close']
                    qty=abs(pos[bar1['Symbol']])
                    if pos[bar1['Symbol']] > 0:
                        side='long'
                    else:
                        side='short'
                    mult=500
                    calcqty=10
                    (pl, value)=calc.calc_pl(openAt, closeAt, calcqty, mult, side)
                    plval=500
                    print pos[bar1['Symbol']], pl, value, value * 0.01
                    if pos[bar1['Symbol']] < 0 and pl > plval:
                        sentEntryOrder[sym1+sym2] = False;
                        sentExitOrder[sym1+sym2] = True;
                
                        return ([[bar1['Symbol'], -pos[bar1['Symbol']], strOrderComment]])
    
                    elif pos[bar1['Symbol']] > 0 and pl > plval:
                        print pl, value, value * 0.01
                        sentEntryOrder[sym1+sym2] = False;
                        sentExitOrder[sym1+sym2] = True;
                
                        return ([[bar1['Symbol'], -pos[bar1['Symbol']], strOrderComment]])

                    if crossBelow[sym1+sym2+'EMA9_20'] or crossAbove[sym1+sym2+'EMA9_20']:
                        if pos[bar1['Symbol']]  and pl > 0:
                            sentEntryOrder[sym1+sym2] = False;
                            sentExitOrder[sym1+sym2] = True;
                            return ([[bar1['Symbol'], -pos[bar1['Symbol']], strOrderComment]])
'''               
@jit
def vwap(v, h, l):
    tmp1 = np.zeros_like(v)
    tmp2 = np.zeros_like(v)
    for i in range(0,len(v)):
        tmp1[i] = tmp1[i-1] + v[i] * ( h[i] + l[i] ) / 2.
        tmp2[i] = tmp2[i-1] + v[i]
    return tmp1 / tmp2
'''
def getPlot(title=''):
    global sigDF
    colnames=sigDF.columns.values.tolist()
    
    fig, ax = plt.subplots()
    
    
    def update(i):
        try:
            #plt.clf()
            
            ax.clear() 
            plt.title(title)
            for col in colnames:
                ax.plot( sigDF[col], label=col)      
            
            #barSize='1 day'
            #try:
            #    if sigDF.index.to_datetime()[0].time() and not sigDF.index.to_datetime()[1].time():
            #        barSize = '1 day'
            #    else:
            #        barSize = '1 min'
            #except Exception as e:
            #    print e
            #if barSize != '1 day':
            
            #def format_date(x, pos=None):
            #    thisind = np.clip(int(x), 0, sigDF.shape[0] - 1)
            #    return sigDF.index[thisind].strftime("%Y-%m-%d %H:%M")
            #ax.xaxis.set_major_formatter(tick.FuncFormatter(format_date))
            # 
            #else:
            #    def format_date(x, pos=None):
            #        thisind = np.clip(int(x + 0.5), 0, sigDF.shape[0] - 1)
            #        return sigDF.index[thisind].strftime("%Y-%m-%d")
            #    #ax.xaxis.set_major_formatter(tick.FuncFormatter(format_date))
            #   
            # Now add the legend with some customizations.
            legend = ax.legend(loc='best', shadow=True)
            try:
                # The frame is matplotlib.patches.Rectangle instance surrounding the legend.
                frame = legend.get_frame()
                frame.set_facecolor('0.90')
                
                # Set the fontsize
                for label in legend.get_texts():
                    label.set_fontsize(8)
                    label.set_fontweight('bold')
                    
            
                # use a more precise date string for the x axis locations in the
                # toolbar
            
                fig.fmt_xdata = mdates.DateFormatter('%Y-%m-%d %H:%M')
                
                
                # rotate and align the tick labels so they look better
                fig.autofmt_xdate()
            except Exception as e:
                print e
        except Exception as e:
            print e
            
    #plt.ylabel(ylabel)
    #plt.imshow(frames[k],cmap=plt.cm.gray)
    fig.canvas.draw()
    a = anim.FuncAnimation(fig, update, repeat=True,interval=15)
    plt.show()
    #plt.savefig(filename)
    
    #plt.show()
    #plt.close(fig)
    #plt.close()
    
def getBar(price, symbol, date, high=0, low=0, vol=0):
    bar=dict()
    bar['Close']=price
    bar['Symbol']=symbol
    bar['Date']=date
    if high:
        bar['High']=high
    if low:
        bar['Low']=low
    if vol:
        bar['Volume']=vol
    return bar

def updateEntry(symPair, entryOrder, exitOrder):
    sentEntryOrder[symPair] = entryOrder
    sentExitOrder[symPair] = exitOrder

def crossCheck(signals, symPair, tsz, check2):
    global crossBelow
    global crossAbove
    if not crossBelow.has_key(symPair):
        crossBelow[symPair]=False
    if not crossAbove.has_key(symPair):
        crossAbove[symPair]=False
    
    if re.search('EMA9_20',symPair):
        crossBelow[symPair]=False
        crossAbove[symPair]=False
        
    if re.search('VWAP',symPair):
        crossBelow[symPair]=False
        crossAbove[symPair]=False
        
    
        
    if signals.iloc[-2][tsz] > signals.iloc[-2][check2]  \
            and                                                         \
       signals.iloc[-1][tsz] <= signals.iloc[-1][check2]:
            crossBelow[symPair]=False
            crossAbove[symPair]=True
    print 'Prior: ',tsz, signals.iloc[-2][tsz], check2, signals.iloc[-2][check2]
    print 'Current: ',tsz, signals.iloc[-1][tsz], check2, signals.iloc[-1][check2]
    logging.info('Prior crossCheck: %s %s %s %s' %( tsz, signals.iloc[-2][tsz], check2, signals.iloc[-2][check2] ) )
    logging.info('Current crossCheck: %s %s %s %s' %( tsz, signals.iloc[-1][tsz], check2, signals.iloc[-1][check2] ) )
    if signals.iloc[-2][tsz] < signals.iloc[-2][check2] \
           and                                                         \
       signals.iloc[-1][tsz] >= signals.iloc[-1][check2]:
             crossBelow[symPair]=True
             crossAbove[symPair]=False
    
    return (crossBelow[symPair], crossAbove[symPair])
#def updateEntry(systemname, broker, sym1, sym2, currency, date, isLive):
#    data=portfolio.get_portfolio(systemname, broker, date, isLive)
#    qty1=portfolio.get_pos(data, broker, sym1, currency, date)
#    qty2=portfolio.get_pos(data, broker, sym1, currency, date)
    