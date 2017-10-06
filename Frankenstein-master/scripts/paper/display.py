# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 20:57:32 2015

@author: hidemi
"""
import math
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import datetime
from datetime import datetime as dt
from scipy import stats
from scipy.stats import kurtosis, skew
import statsmodels.tsa.stattools as ts
from sklearn.preprocessing import scale, robust_scale, minmax_scale
from sklearn.learning_curve import learning_curve
from sklearn.metrics import accuracy_score,average_precision_score,f1_score,\
                            log_loss,precision_score,recall_score, roc_auc_score,\
                            confusion_matrix, hamming_loss, jaccard_similarity_score,\
                            zero_one_loss
from suztoolz.transform import softmax_score, numberZeros, ratio, hurst


sns.set_style("darkgrid", {"axes.facecolor": ".9"})
sns.color_palette("Set1", n_colors=8, desat=.5)
    
def compareEquity(sst, title, filename):
    #check if there's time in the index
    if not sst.index.to_datetime()[0].time() and not sst.index.to_datetime()[1].time():
        barSize = '1 day'
    else:
        barSize = '1 min'
        
    nrows = sst.gainAhead.shape[0]
    #signalCounts = sst.signals.shape[0]
    print '\nThere are %0.f signal counts' % nrows
    if 1 in sst.signals.value_counts():
        print sst.signals.value_counts()[1], 'beLong Signals',
    if -1 in sst.signals.value_counts():
        print sst.signals.value_counts()[-1], 'beShort Signals',
    if 0 in sst.signals.value_counts():
        print sst.signals.value_counts()[0], 'beFlat Signals',
    #  Compute cumulative equity for all days
    equityAllSignals = np.zeros(nrows)
    equityAllSignals[0] = 1
    for i in range(1,nrows):
        equityAllSignals[i] = (1+sst.gainAhead.iloc[i-1])*equityAllSignals[i-1]
        
    #  Compute cumulative equity for days with beLong signals    
    equityBeLongSignals = np.zeros(nrows)
    equityBeLongSignals[0] = 1
    for i in range(1,nrows):
        if (sst.signals.iloc[i-1] > 0):
            equityBeLongSignals[i] = (1+sst.gainAhead.iloc[i-1])*equityBeLongSignals[i-1]
        else:
            equityBeLongSignals[i] = equityBeLongSignals[i-1]
            
    #  Compute cumulative equity for days with beShort signals    
    equityBeLongAndShortSignals = np.zeros(nrows)
    equityBeLongAndShortSignals[0] = 1
    for i in range(1,nrows):
        if (sst.signals.iloc[i-1] < 0):
            equityBeLongAndShortSignals[i] = (1+-sst.gainAhead.iloc[i-1])*equityBeLongAndShortSignals[i-1]
        elif (sst.signals.iloc[i-1] > 0):
            equityBeLongAndShortSignals[i] = (1+sst.gainAhead.iloc[i-1])*equityBeLongAndShortSignals[i-1]
        else:
            equityBeLongAndShortSignals[i] = equityBeLongAndShortSignals[i-1]

    #  Compute cumulative equity for days with beShort signals    
    equityBeShortSignals = np.zeros(nrows)
    equityBeShortSignals[0] = 1
    for i in range(1,nrows):
        if (sst.signals.iloc[i-1] < 0):
            equityBeShortSignals[i] = (1+-sst.gainAhead.iloc[i-1])*equityBeShortSignals[i-1]
        else:
            equityBeShortSignals[i] = equityBeShortSignals[i-1] 
    
    #plt.close('all')
    fig, ax = plt.subplots(1, figsize=(8,7))
    ax.plot(sst.index.to_datetime(), equityBeLongSignals,label="Long 1 Signals",color='b')
    ax.plot(sst.index.to_datetime(), equityBeShortSignals,label="Short -1 Signals",color='r')
    ax.plot(sst.index.to_datetime(), equityBeLongAndShortSignals,label="Long & Short",color='g')
    ax.plot(sst.index.to_datetime(), equityAllSignals,label="BuyHold",ls='--',color='c')
    # rotate and align the tick labels so they look better
    years = mdates.YearLocator()   # every year
    months = mdates.MonthLocator()  # every month
    days = mdates.DayLocator()
    # format the ticks
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_minor_locator(months)    
    y_formatter = matplotlib.ticker.ScalarFormatter(useOffset=False)
    ax.yaxis.set_major_formatter(y_formatter)
    
    if barSize != '1 day' and nrows <=1440:
        hours = mdates.HourLocator() 
        minutes = mdates.MinuteLocator()
        # format the ticks
        ax.xaxis.set_major_locator(hours)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H"))
        ax.xaxis.set_minor_locator(minutes)
    else:
        hours = mdates.HourLocator() 
        minutes = mdates.MinuteLocator()
        # format the ticks
        ax.xaxis.set_major_locator(days)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        ax.xaxis.set_minor_locator(hours)

    #ax.fmt_xdata = mdates.DateFormatter("%Y-%m-%d %H:%M")
    plt.title(title)
    plt.ylabel("TWR")
    plt.legend(loc="best")
    fig.autofmt_xdate()
    plt.savefig(filename)
    #plt.show()
    shortTrades, longTrades = numberZeros(sst.signals.values)
    allTrades = shortTrades+ longTrades
    print '\nValidation Period from', sst.index[0],'to',sst.index[-1]
    print 'TWR for Buy & Hold is %0.3f, %i days' % (equityAllSignals[nrows-1], nrows)
    print 'TWR for %i beLong trades is %0.3f' % (longTrades, equityBeLongSignals[nrows-1])
    print 'TWR for %i beShort trades is %0.3f' % (shortTrades,equityBeShortSignals[nrows-1])
    print 'TWR for %i beLong and beShort trades is %0.3f' % (allTrades,equityBeLongAndShortSignals[nrows-1])
    
    #check
    #pd.concat([sst,pd.Series(data=equityAllSignals,name='equityAllSignals',index=sst.index),\
    #        pd.Series(data=equityBeLongSignals,name='equityBeLongSignals',index=sst.index),
    #        pd.Series(data=equityBeShortSignals,name='equityBeShortSignals',index=sst.index),
    #        pd.Series(data=equityBeLongAndShortSignals,name='equityBeLongAndShortSignals',index=sst.index),
    #        ],axis=1)
    
