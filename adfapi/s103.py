### Quantiacs Mean Reversion Trading System Example
# import necessary Packages below:
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.tsa.stattools as ts
import sys
from numpy import zeros, ones, flipud, log
from numpy.linalg import inv, eig, cholesky as chol
import talib as ta

from statsmodels.regression.linear_model import OLS

##### Do not change this function definition ####
pair1Series=list()
pair2Series=list()
tsPairratio=list()
tsPairratio2=list()
tsZscore=list()
tsZscore2=list()
tsDates=list()
indSmaZscore=list()
indSmaZscore2=list()
intDatapoints=1000
sentEntryOrder = False
sentExitOrder = False
intSMALength = 30
dblUpperThreshold = 1
dblLowerThreshold = -1
instPair1Factor=1
instPair2Factor=1
dblQty=1
dblQty2=1
crossAbove=False
crossBelow=False

def procBar(bar1, bar2, pos, trade):
    global pair1Series
    global pair2Series
    global tsPairratio
    global tsPairratio2
    global tsZscore
    global tsZscore2
    global indSmaZscore
    global indSmaZscore2
    global intDatapoints
    global sentEntryOrder 
    global sentExitOrder 
    global intSMALength 
    global dblUpperThreshold 
    global dblLowerThreshold 
    global instPair1Factor
    global instPair2Factor
    global dblQty
    global dblQty2 
    global crossAbove
    global crossBelow
    
    if bar1['Close'] > 0 and bar2['Close'] > 0:
        xd = bar1['Close'] * instPair1Factor
        yd = bar2['Close'] * instPair2Factor
        pair1Series.append(bar1['Close'])
        pair2Series.append(bar2['Close'])

        dblRatioData = bar1['Close'] / bar2['Close'];
        tsPairratio.append( dblRatioData);
        dblRatioData2 = bar2['Close'] / bar1['Close'];
        tsPairratio2.append( dblRatioData2);

        if len(tsPairratio)< intDatapoints or len(tsPairratio2) < intDatapoints:
            return []

        iStart = len(tsPairratio) - intDatapoints;
        iEnd = len(tsPairratio) - 1;
        dblAverage = np.mean(tsPairratio[iStart:iEnd]);
        dblRatioStdDev = np.std(tsPairratio[iStart:iEnd]);
        dblResidualsData = (dblRatioData - dblAverage);
        dblZscoreData = (dblRatioData - dblAverage) / dblRatioStdDev;
        tsZscore.append(dblZscoreData)
        tsDates.append(bar1['Date'])

        iStart2 = len(tsPairratio2) - intDatapoints;
        iEnd2 = len(tsPairratio2) - 1;
        dblAverage2 = np.mean(tsPairratio[iStart2:iEnd2]);
        dblRatioStdDev2 = np.std(tsPairratio[iStart2:iEnd2]);
        dblResidualsData2 = (dblRatioData2 - dblAverage2);
        dblZscoreData2 = (dblRatioData2 - dblAverage2) / dblRatioStdDev2;
        tsZscore2.append(dblZscoreData2)
        
        signals=pd.DataFrame()
        signals['Date']=tsDates
        signals['tsZscore']=tsZscore
        signals['tsZscore2']=tsZscore2
        #signals['indSmaZscore']=pd.rolling_mean(signals['tsZscore'], intSMALength, min_periods=1)
        #signals['indSmaZscore2']=pd.rolling_mean(signals['tsZscore2'], intSMALength, min_periods=1)    
        
        signals['indSmaZscore']=ta.SMA(np.array(signals['tsZscore']), intSMALength)      
        signals['indSmaZscore2']=ta.SMA(np.array(signals['tsZscore2']), intSMALength)        
        signals=signals.set_index('Date')
        
        #				tsPricePair1.Add(bar1['Date']Time, bar1['Close']);
        #			tsPricePair2.Add(bar2['Date']Time, bar2['Close']);
        #				double dblBeta = tsPricePair1.GetCovariance( tsPricePair2 ) /tsPricePair1.GetVariance(Bars.Ago(intDatapoints).DateTime,	Bars.Ago(1).DateTime);

        #print 'ZScore:' + str(dblZscoreData) + ' Upper: ' +  str(dblUpperThreshold) +  + ' Lower: ' +  str(dblLowerThreshold)
       
        if len(signals['tsZscore']) < 5 or len(signals['indSmaZscore']) < 5 or len(signals['indSmaZscore2']) < 5:
            return [];

        #updateCointData();

        if trade:
                strOrderComment = "zScore: " + str(round(dblZscoreData, 2)) + " zSMA: " + str(round(signals.iloc[-1]['indSmaZscore'], 2));
                strOrderComment2 = "zScore: " + str(round(dblZscoreData2, 2)) + " zSMA: " + str(round(signals.iloc[-1]['indSmaZscore2'], 2));
                #print strOrderComment
                                
                if signals.iloc[-2]['tsZscore'] > signals.iloc[-2]['indSmaZscore']  \
                        and                                                         \
                   signals.iloc[-1]['tsZscore'] <= signals.iloc[-1]['indSmaZscore']:
                        crossBelow=False
                        crossAbove=True

                if signals.iloc[-2]['tsZscore'] < signals.iloc[-2]['indSmaZscore'] \
                       and                                                         \
                   signals.iloc[-1]['tsZscore'] >= signals.iloc[-1]['indSmaZscore']:
                        crossBelow=True
                        crossAbove=False
                       
                #print ' crossAbove: ' + str(crossAbove) + ' crossBelow: ' + str(crossBelow)
                #crossBelow = signals['tsZscore'].iloc[-1] >= signals['indSmaZscore'].iloc[-1] and crossBelow.any()
                #crossAbove = signals['tsZscore'].iloc[-1] <= signals['indSmaZscore'].iloc[-1] and crossAbove.any()
                #print ' crossAbove: ' + str(crossAbove) + ' crossBelow: ' + str(crossBelow)
                if not sentEntryOrder and not pos.has_key(bar1['Symbol']) and not pos.has_key(bar2['Symbol']):

                    #dblQty = Math.Ceiling(1/dblBeta);
                    #dblQty2 = Math.Ceiling(dblBeta);
    
                    # Create the set of short and long simple moving averages over the 
                    # respective periods
                    
                   
                    # Create a 'signal' (invested or not invested) when the short moving average crosses the long
                    # moving average, but only for the period greater than the shortest moving average window
    
                    
                
                    if dblZscoreData >= dblUpperThreshold and crossAbove == 1:
                        
                        #Sell(instPair1, dblQty, strOrderComment);
                        #Buy(instPair2, dblQty2, strOrderComment2);
            
                        #if (myParam.hasOpt)
                        #{
                        #    Sell(myParam.getSym1OptInst(PutCall.Put, bar1['Close'], this), myParam.sym1OptQty, strOrderComment);
                        #    Sell(myParam.getSym2OptInst(PutCall.Call, bar2['Close'], this), myParam.sym2OptQty, strOrderComment2);
                        #}
                        sentEntryOrder = True
                        sentExitOrder = False
                        return ([bar1['Symbol'], -abs(dblQty), strOrderComment], 
                                [bar2['Symbol'], abs(dblQty2), strOrderComment2])
                    elif dblZscoreData <= -1 * dblUpperThreshold and crossBelow==1:
                        #Buy(instPair1, dblQty, strOrderComment);
                        #Sell(instPair2, dblQty2, strOrderComment2);
                        #if (myParam.hasOpt)
                        #{
                        #    Sell(myParam.getSym1OptInst(PutCall.Call, bar1['Close'], this), myParam.sym1OptQty, strOrderComment);
                        #    Sell(myParam.getSym2OptInst(PutCall.Put, bar2['Close'], this), myParam.sym2OptQty, strOrderComment2);
                        #}
                        sentEntryOrder = True
                        sentExitOrder = False
                        return ([bar1['Symbol'], abs(dblQty), strOrderComment], 
                                [bar2['Symbol'], -abs(dblQty2), strOrderComment2])
    
                elif not sentExitOrder and pos.has_key(bar1['Symbol']) and pos.has_key(bar2['Symbol']):
                    
                    if pos[bar1['Symbol']] < 0 and pos[bar2['Symbol']] > 0 and \
                        dblZscoreData <= dblLowerThreshold and crossAbove==1:
                        #Buy(instPair1, dblQty, strOrderComment);
                        #Sell(instPair2, dblQty2, strOrderComment2);
    
                        #if (myParam.hasOpt)
                        #{
                        #   Buy(myParam.instPair1opt, myParam.sym1OptQty, strOrderComment);
                        #   Buy(myParam.instPair2opt, myParam.sym2OptQty, strOrderComment);
                        #}
                        sentEntryOrder = False;
                        sentExitOrder = True;
                        return ([bar1['Symbol'], abs(dblQty), strOrderComment], 
                                [bar2['Symbol'], -abs(dblQty2), strOrderComment2])
    
                    elif pos[bar1['Symbol']] > 0 and pos[bar2['Symbol']] < 0 and \
                        dblZscoreData >= -1 * dblLowerThreshold and crossBelow == 1:
                        #Sell(instPair1, dblQty, strOrderComment);
                        #Buy(instPair2, dblQty2, strOrderComment2);
    
                        #if (myParam.hasOpt)
                        #{
                        #    Buy(myParam.instPair1opt, myParam.sym1OptQty, strOrderComment);
                        #    Buy(myParam.instPair2opt, myParam.sym2OptQty, strOrderComment);
                        #}
                        sentEntryOrder = False;
                        sentExitOrder = True;
                        return ([bar1['Symbol'], -abs(dblQty), strOrderComment], 
                                [bar2['Symbol'], abs(dblQty2), strOrderComment2])
               
def getBar(price, symbol, date):
    bar=dict()
    bar['Close']=price
    bar['Symbol']=symbol
    bar['Date']=date
    return bar

