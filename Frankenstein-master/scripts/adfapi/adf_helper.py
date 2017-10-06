### Quantiacs Mean Reversion Trading System Example
# import necessary Packages below:
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.tsa.stattools as ts
import sys
from numpy import zeros, ones, flipud, log
from numpy.linalg import inv, eig, cholesky as chol
from statsmodels.regression.linear_model import OLS

pairs=pd.DataFrame({}, columns=['datetime','open','high','low','close','volume','na']);
#datadir = 'tickerData'  # Change this to reflect your data path!
#pairs = create_pairs_dataframe(datadir, symbols)

def getCoint(sym1Data, sym1, sym2Data, sym2):
    pairs=pd.DataFrame()
    pairs[sym1]=sym1Data
    pairs[sym2]=sym2Data
    
    pairs = calculate_spread_zscore(pairs, [sym1, sym2], 500)

    if 'zscore' not in pairs or pairs['zscore'] is None:
	return -1


    confidence=calculate_adf(pairs['spread'])
    
    return confidence
    #if confidence > 95:
    # return True
    #else:
    # return False
     
def calculate_adf(spread):
    
    try:
        spread=spread[~np.isnan(spread)]
        #print '%s' % spread
        cadf = ts.adfuller(spread)
        confidence = 100 - int(cadf[1] * 100)
        if (cadf[1] <= 0.05):
            churst = hurst(spread)
            print_coint(cadf,churst)
            pv=cadf[1]
            
            return (confidence, pv, churst)
        
        return (confidence, cadf[1], -1)
    except:
         print 'calculate_adf Error'
        
def calculate_johansen(y, p):
        """
        Get the cointegration vectors at 95% level of significance
        given by the trace statistic test.
        """

        N, l = y.shape
        jres = coint_johansen(y, p, 1)
        trstat = jres.lr1                       # trace statistic
        tsignf = jres.cvt                       # critical values

        r=0
        for i in range(l):
            if trstat[i] > tsignf[i, 1]:     # 0: 90%  1:95% 2: 99%
                r = i + 1
                
        jres.r = r
        jres.evecr = jres.evec[:, :r]
        print_johansen(jres)
        return jres
        
def print_johansen(jres):
    print "There are ", jres.r, "cointegration vectors"
    print "jres: %s" % jres.evecr
    #v1=jres.evecr[:,0]
    #v2=jres.evecr[:,1]
    #print v1
    #print v2
    #v3=jres.evec[:,2]  # v3 is not a cointegration vector

def hurst(spread):
     #create range of lag values
     lags = range(2,100)
     #calculate the array of the variances of the lagged differences
     tau = [np.sqrt(np.std(np.subtract(spread[lag:], spread[:-lag]))) for lag in lags]
     #use a linear fit to estimate the hurt exponent
     poly = np.polyfit(np.log(lags), np.log(tau),1)
     #return the hurst exponent from the polyfit output
     return poly[0]*2.0

def print_coint(adf, hurst):
    #create a GBM, MR, Trending series
    #gbm = log(cumsum(randn(100000))+1000)
    #mr = log(randn(100000)+1000)
    #tr = log(cumsum(randn(100000)+1)+1000)
    print ""
    print "ADF test for mean reversion"
    print "Datapoints", adf[3]
    print "p-value", adf[1]
   
        
    print "Test-Stat", adf[0]
    for key in adf[4]:
      print adf[0]<adf[4][key],"Critical Values:",key, adf[4][key],"Test-stat: ",adf[0]
    print ""
    print "Hurst Exponent"
    print "Hurst(GBM): %s Hurst(MR): %s Hurst(TREND): %s" % (.50,0,1)
    print "Hurst(Resid): %s" % (hurst)
    if adf[1] <= 0.05:
        print 'The spread is likely Cointegrated with a pvalue of %s' % adf[1]
    else:
        print 'The spread is likely NOT Cointegrated with a pvalue of %s' % adf[1]
    
        
def create_pairs_dataframe(datadir, symbols):
    """Creates a pandas DataFrame containing the closing price
    of a pair of symbols based on CSV files containing a datetime
    stamp and OHLCV data."""

    # Open the individual CSV files and read into pandas DataFrames
    print "Importing CSV data..."
    sym1 = pd.io.parsers.read_csv(os.path.join(datadir, '%s.txt' % symbols[0]),
                                  header=0, index_col=0,
                                  names=['datetime','open','high','low','close','volume','na'])
    sym2 = pd.io.parsers.read_csv(os.path.join(datadir, '%s.txt' % symbols[1]),
                                  header=0, index_col=0,
                                  names=['datetime','open','high','low','close','volume','na'])

    # Create a pandas DataFrame with the close prices of each symbol
    # correctly aligned and dropping missing entries
    print "Constructing dual matrix for %s and %s..." % symbols
    pairs = pd.DataFrame(index=sym1.index)
    pairs['%s' % symbols[0]] = sym1['close']
    pairs['%s' % symbols[1]] = sym2['close']
    pairs = pairs.dropna()
    return pairs

def calculate_spread_zscore(pairs, symbols, lookback=2000):
    try:
        """Creates a hedge ratio between the two symbols by calculating
        a rolling linear regression with a defined lookback period. This
        is then used to create a z-score of the 'spread' between the two
        symbols based on a linear combination of the two."""
    
        # Use the pandas Ordinary Least Squares method to fit a rolling
        # linear regression between the two closing price time series
        #print "Fitting the rolling Linear Regression..."
       
        model = pd.ols(y=pairs['%s' % symbols[0]],
                       x=pairs['%s' % symbols[1]],
                       window=lookback)
    
        # Construct the hedge ratio and eliminate the first
        # lookback-length empty/NaN period
        pairs['hedge_ratio'] = model.beta['x']
        #pairs = pairs.dropna()
    
        # Create the spread and then a z-score of the spread
        #print "Creating the spread/zscore columns..."
        pairs['spread'] = pairs['%s' % symbols[0]] - pairs['hedge_ratio']*pairs['%s' % symbols[1]]
        pairs['zscore'] = (pairs['spread'] - np.mean(pairs['spread']))/np.std(pairs['spread'])
    except Exception as e:
        print 'calculate_spread_zscore Error: ' + str(e)
        
    return pairs


def make_signals(pairs, symbols, symidx, pos, settings, nDates, 
                                     z_entry_threshold=2.0, 
                                     z_exit_threshold=1.0):
    
    pairs = calculate_spread_zscore(pairs, symbols, 500)

    if pairs['zscore'] is None:
	return pairs, pos, settings


    cadf=calculate_adf(pairs['spread'])
    
    if cadf[1] <= 0.05:
        return pairs, pos, settings
        
    isInTrade=0
   
    if '%s_%s' % (symbols[0], symbols[1]) in settings:
       isInTrade= settings['%s_%s' % (symbols[0], symbols[1])];
    
    #print 'zscore: %5.3f ' % (pairs['zscore'].iat[-1])
    if isInTrade == 0 and pairs['zscore'].iat[-1] <= -z_entry_threshold:
        pos[0,symidx[0]] = 1
        pos[0,symidx[1]] = -1
        print 'date: %d entry, zscore: %5.3f' % (nDates[symidx[0]], pairs['zscore'].iat[-1])    
        isInTrade=1
    elif isInTrade == 0 and pairs['zscore'].iat[-1]  >= z_entry_threshold:
        pos[0,symidx[0]] = -1
        pos[0,symidx[1]] = 1
        print 'date: %d entry 2, zscore: %5.3f' % (nDates[symidx[0]], pairs['zscore'].iat[-1])
        isInTrade=2
    elif isInTrade > 0 and np.abs(pairs['zscore'].iat[-1]) <= z_exit_threshold:
        if isInTrade==1:
            pos[0,symidx[0]] = -1
            pos[0,symidx[1]] = 1
        if isInTrade==2:
            pos[0,symidx[0]] = 1
            pos[0,symidx[1]] = -1
        print 'date: %d exit, zscore: %5.3f' % (nDates[symidx[0]], pairs['zscore'].iat[-1])
        isInTrade=0
        
    settings['%s_%s' % (symbols[0], symbols[1])]=isInTrade
    return pairs, pos, settings

##### Do not change this function definition #####
def myTradingSystem(DATE, OPEN, HIGH, LOW, CLOSE, VOL, exposure, equity, settings):
    global pairs;

    # This system uses mean reversion techniques to allocate capital into the desired equities

    # This strategy evaluates two averages over time of the close over a long/short
    # scale and builds the ratio. For each day, "smaQuot" is an array of "nMarkets"
    # size.

    
    
    nMarkets = np.shape(CLOSE)[1]
    
    positions=equity[1]
    
    pos= np.zeros((1,nMarkets))
    
    nDates=DATE;
    closePrices=pd.DataFrame(CLOSE, columns=settings['markets']); 
    #print 'nmarkets: %s closePrices: %s' % (symbols[0], closePrices[symbols[0]])
    #print 'nmarkets: %s ' % (nMarkets)
    #calculate_johansen(closePrices,1)
    
    symidx=(1,2);
    symbols=(settings['markets'][symidx[0]], settings['markets'][symidx[1]])
    #print '%s: %s, %s: %s' % (symbols[0], positions[symidx[0]], symbols[1], positions[symidx[1]])
    pairs['%s' % symbols[0]] = closePrices[symbols[0]]; #np.take(CLOSE, sym0_idx, axis=1);
    pairs['%s' % symbols[1]] = closePrices[symbols[1]]; #np.take(CLOSE, sym1_idx, axis=1);
    
    (pairs,pos, settings)=make_signals(pairs, symbols, symidx, pos, settings, nDates, 2.0, 1.0)
    if pos[0,symidx[0]] > 0:
        print '%s LONG: %s, %s SHORT: %s' % (symbols[0], closePrices[symbols[0]][0], symbols[1], closePrices[symbols[0]][1])
    elif pos[0, symidx[0]] < 0:
        print '%s SHORT: %s, %s LONG: %s' % (symbols[0], closePrices[symbols[0]][0], symbols[1], closePrices[symbols[0]][1])
    #print '%s: %5.3f, %s: %5.3f' % (symbols[0], pos[0,symidx[0]], symbols[1], pos[0,symidx[1]])
    
    #periodLong= 200
    #periodShort= 40

    #smaLong=   np.sum(CLOSE[-periodLong:,:], axis=0)/periodLong
    #smaRecent= np.sum(CLOSE[-periodShort:,:],axis=0)/periodShort
    #smaQuot= smaRecent / smaLong

    # For each day, scan the ratio of moving averages over the markets and find the
    # market with the maximum ratio and the market with the minimum ratio:
    #longEquity = np.where(smaQuot == np.nanmin(smaQuot))
    #shortEquity= np.where(smaQuot == np.nanmax(smaQuot))

    # Take a contrarian view, going long the market with the minimum ratio and
    # going short the market with the maximum ratio. The array "pos" will contain
    # all zero entries except for those cases where we go long (1) and short (-1):
    #pos= np.zeros((1,nMarkets))
    #pos[0,longEquity[0][0]] = 1
    #pos[0,shortEquity[0][0]]= -1

    # For the position sizing, we supply a vector of weights defining our
    # exposure to the markets in settings['markets']. This vector should be
    # normalized.
    pos= pos/np.nansum(abs(pos))

    return pos, settings


##### Do not change this function definition #####
def mySettings():
    # Default competition and evaluation mySettings
    settings= {}

    # S&P 100 stocks
    # settings['markets']=['CASH','AAPL','ABBV','ABT','ACN','AEP','AIG','ALL', \
    # 'AMGN','AMZN','APA','APC','AXP','BA','BAC','BAX','BK','BMY','BRKB','C', \
    # 'CAT','CL','CMCSA','COF','COP','COST','CSCO','CVS','CVX','DD','DIS','DOW',\
    # 'DVN','EBAY','EMC','EMR','EXC','F','FB','FCX','FDX','FOXA','GD','GE', \
    # 'GILD','GM','GOOGL','GS','HAL','HD','HON','HPQ','IBM','INTC','JNJ','JPM', \
    # 'KO','LLY','LMT','LOW','MA','MCD','MDLZ','MDT','MET','MMM','MO','MON', \
    # 'MRK','MS','MSFT','NKE','NOV','NSC','ORCL','OXY','PEP','PFE','PG','PM', \
    # 'QCOM','RTN','SBUX','SLB','SO','SPG','T','TGT','TWX','TXN','UNH','UNP', \
    # 'UPS','USB','UTX','V','VZ','WAG','WFC','WMT','XOM']

    # Futures Contracts
    settings['markets']  = ['F_AD','F_CL','F_GC', 'F_BO'] #, 'F_BP', 'F_C', 'F_CD',  \
    #'F_DJ', 'F_EC', 'F_ES', 'F_FV', 'F_HO', 'F_HG', 'F_NG', 'F_LC', \
    #'F_LN', 'F_NQ', 'F_RB', 'F_S', 'F_SF', 'F_SI', 'F_SM', 'F_SP', \
    #'F_TY', 'F_US', 'F_W', 'F_YM']


    settings['lookback']= 504
    settings['budget']= 1000000
    settings['slippage']= 0.05

    return settings

ss_ejcp0 = '''\
         2.9762  4.1296  6.9406
         9.4748 11.2246 15.0923
        15.7175 17.7961 22.2519
        21.8370 24.1592 29.0609
        27.9160 30.4428 35.7359
        33.9271 36.6301 42.2333
        39.9085 42.7679 48.6606
        45.8930 48.8795 55.0335
        51.8528 54.9629 61.3449
        57.7954 61.0404 67.6415
        63.7248 67.0756 73.8856
        69.6513 73.0946 80.0937'''

ss_ejcp1 = '''\
         2.7055   3.8415   6.6349
        12.2971  14.2639  18.5200
        18.8928  21.1314  25.8650
        25.1236  27.5858  32.7172
        31.2379  33.8777  39.3693
        37.2786  40.0763  45.8662
        43.2947  46.2299  52.3069
        49.2855  52.3622  58.6634
        55.2412  58.4332  64.9960
        61.2041  64.5040  71.2525
        67.1307  70.5392  77.4877
        73.0563  76.5734  83.7105'''

ss_ejcp2 = '''\
         2.7055   3.8415   6.6349
        15.0006  17.1481  21.7465
        21.8731  24.2522  29.2631
        28.2398  30.8151  36.1930
        34.4202  37.1646  42.8612
        40.5244  43.4183  49.4095
        46.5583  49.5875  55.8171
        52.5858  55.7302  62.1741
        58.5316  61.8051  68.5030
        64.5292  67.9040  74.7434
        70.4630  73.9355  81.0678
        76.4081  79.9878  87.2395'''

ejcp0 = np.array(ss_ejcp0.split(),float).reshape(-1,3)
ejcp1 = np.array(ss_ejcp1.split(),float).reshape(-1,3)
ejcp2 = np.array(ss_ejcp2.split(),float).reshape(-1,3)

def c_sja(n, p):
    if ((p > 1) or (p < -1)):
        jc = np.zeros(3)
    elif ((n > 12) or (n < 1)):
        jc = np.zeros(3)
    elif p == -1:
        jc = ejcp0[n-1,:]
    elif p == 0:
        jc = ejcp1[n-1,:]
    elif p == 1:
        jc = ejcp2[n-1,:]

    return jc

'''
function jc = c_sjt(n,p)
% PURPOSE: find critical values for Johansen trace statistic
% ------------------------------------------------------------
% USAGE:  jc = c_sjt(n,p)
% where:    n = dimension of the VAR system
%               NOTE: routine doesn't work for n > 12
%           p = order of time polynomial in the null-hypothesis
%                 p = -1, no deterministic part
%                 p =  0, for constant term
%                 p =  1, for constant plus time-trend
%                 p >  1  returns no critical values
% ------------------------------------------------------------
% RETURNS: a (3x1) vector of percentiles for the trace
%          statistic for [90% 95% 99%]
% ------------------------------------------------------------
% NOTES: for n > 12, the function returns a (3x1) vector of zeros.
%        The values returned by the function were generated using
%        a method described in MacKinnon (1996), using his FORTRAN
%        program johdist.f
% ------------------------------------------------------------
% SEE ALSO: johansen()
% ------------------------------------------------------------
% % References: MacKinnon, Haug, Michelis (1996) 'Numerical distribution
% functions of likelihood ratio tests for cointegration',
% Queen's University Institute for Economic Research Discussion paper.
% -------------------------------------------------------
% written by:
% James P. LeSage, Dept of Economics
% University of Toledo
% 2801 W. Bancroft St,
% Toledo, OH 43606
% jlesage@spatial-econometrics.com
% these are the values from Johansen's 1995 book
% for comparison to the MacKinnon values
%jcp0 = [ 2.98   4.14   7.02
%        10.35  12.21  16.16
%        21.58  24.08  29.19
%        36.58  39.71  46.00
%        55.54  59.24  66.71
%        78.30  86.36  91.12
%       104.93 109.93 119.58
%       135.16 140.74 151.70
%       169.30 175.47 187.82
%       207.21 214.07 226.95
%       248.77 256.23 270.47
%       293.83 301.95 318.14];
%
'''


ss_tjcp0 = '''\
         2.9762   4.1296   6.9406
        10.4741  12.3212  16.3640
        21.7781  24.2761  29.5147
        37.0339  40.1749  46.5716
        56.2839  60.0627  67.6367
        79.5329  83.9383  92.7136
       106.7351 111.7797 121.7375
       137.9954 143.6691 154.7977
       173.2292 179.5199 191.8122
       212.4721 219.4051 232.8291
       255.6732 263.2603 277.9962
       302.9054 311.1288 326.9716'''


ss_tjcp1 = '''\
          2.7055   3.8415   6.6349
         13.4294  15.4943  19.9349
         27.0669  29.7961  35.4628
         44.4929  47.8545  54.6815
         65.8202  69.8189  77.8202
         91.1090  95.7542 104.9637
        120.3673 125.6185 135.9825
        153.6341 159.5290 171.0905
        190.8714 197.3772 210.0366
        232.1030 239.2468 253.2526
        277.3740 285.1402 300.2821
        326.5354 334.9795 351.2150'''

ss_tjcp2 = '''\
           2.7055   3.8415   6.6349
          16.1619  18.3985  23.1485
          32.0645  35.0116  41.0815
          51.6492  55.2459  62.5202
          75.1027  79.3422  87.7748
         102.4674 107.3429 116.9829
         133.7852 139.2780 150.0778
         169.0618 175.1584 187.1891
         208.3582 215.1268 228.2226
         251.6293 259.0267 273.3838
         298.8836 306.8988 322.4264
         350.1125 358.7190 375.3203'''

tjcp0 = np.array(ss_tjcp0.split(),float).reshape(-1,3)
tjcp1 = np.array(ss_tjcp1.split(),float).reshape(-1,3)
tjcp2 = np.array(ss_tjcp2.split(),float).reshape(-1,3)

def c_sjt(n, p):
    if ((p > 1) or (p < -1)):
        jc = np.zeros(3)
    elif ((n > 12) or (n < 1)):
        jc = np.zeros(3)
    elif p == -1:
        jc = tjcp0[n-1,:]
    elif p == 0:
        jc = tjcp1[n-1,:]
    elif p == 1:
        jc = tjcp2[n-1,:]
    else:
        raise ValueError('invalid p')

    return jc

tdiff = np.diff

def rows(x):
    return x.shape[0]

def trimr(x, front, end):
    if end > 0:
        return x[front:-end]
    else:
        return x[front:]

import statsmodels.tsa.tsatools as tsat
mlag = tsat.lagmat

class Holder(object):
    pass


def mlag_(x, maxlag):
    '''return all lags up to maxlag
    '''
    return x[:-lag]

def lag(x, lag):
    return x[:-lag]

def detrend(y, order):
    if order == -1:
        return y
    return OLS(y, np.vander(np.linspace(-1,1,len(y)), order+1)).fit().resid

def resid(y, x):

    #print '%s %s' % (y,x)
    if x.size == 0:
        return y
    r = y - np.dot(x, np.dot(np.linalg.pinv(x), y))
    return r




def coint_johansen(x, p, k, coint_trend=None):

    #    % error checking on inputs
    #    if (nargin ~= 3)
    #     error('Wrong # of inputs to johansen')
    #    end
    nobs, m = x.shape
    #print 'x: %s' % (x)
    #why this?  f is detrend transformed series, p is detrend data
    if (p > -1):
        f = 0
    else:
        f = p

    if coint_trend is not None:
        f = coint_trend  #matlab has separate options


    x     = detrend(x,p)
    dx    = tdiff(x,1, axis=0)
    #dx    = trimr(dx,1,0)
    z     = mlag(dx,k)#[k-1:]
    #print z.shape
    z = trimr(z,k,0)
    z     = detrend(z,f)
    #print 'dx: %s z: %s' % (dx, z)
    dx = trimr(dx,k,0)

    dx    = detrend(dx,f)
    #r0t   = dx - z*(z\dx)
    
    
    r0t   = resid(dx, z)  #diff on lagged diffs
    #lx = trimr(lag(x,k),k,0)
    lx = lag(x,k)
    lx = trimr(lx, 1, 0)
    dx    = detrend(lx,f)
    print 'rkt', dx.shape, z.shape
    #rkt   = dx - z*(z\dx)
    rkt   = resid(dx, z)  #level on lagged diffs
    skk   = np.dot(rkt.T, rkt) / rows(rkt)
    sk0   = np.dot(rkt.T, r0t) / rows(rkt)
    s00   = np.dot(r0t.T, r0t) / rows(r0t)
    sig   = np.dot(sk0, np.dot(inv(s00), (sk0.T)))
    tmp   = inv(skk)
    #du, au = eig(np.dot(tmp, sig))
    au, du = eig(np.dot(tmp, sig))  #au is eval, du is evec
    #orig = np.dot(tmp, sig)

    #% Normalize the eigen vectors such that (du'skk*du) = I
    temp   = inv(chol(np.dot(du.T, np.dot(skk, du))))
    dt     = np.dot(du, temp)


    #JP: the next part can be done much  easier

    #%      NOTE: At this point, the eigenvectors are aligned by column. To
    #%            physically move the column elements using the MATLAB sort,
    #%            take the transpose to put the eigenvectors across the row

    #dt = transpose(dt)

    #% sort eigenvalues and vectors

    #au, auind = np.sort(diag(au))
    auind = np.argsort(au)
    #a = flipud(au)
    aind = flipud(auind)
    a = au[aind]
    #d = dt[aind,:]
    d = dt[:,aind]

    #%NOTE: The eigenvectors have been sorted by row based on auind and moved to array "d".
    #%      Put the eigenvectors back in column format after the sort by taking the
    #%      transpose of "d". Since the eigenvectors have been physically moved, there is
    #%      no need for aind at all. To preserve existing programming, aind is reset back to
    #%      1, 2, 3, ....

    #d  =  transpose(d)
    #test = np.dot(transpose(d), np.dot(skk, d))

    #%EXPLANATION:  The MATLAB sort function sorts from low to high. The flip realigns
    #%auind to go from the largest to the smallest eigenvalue (now aind). The original procedure
    #%physically moved the rows of dt (to d) based on the alignment in aind and then used
    #%aind as a column index to address the eigenvectors from high to low. This is a double
    #%sort. If you wanted to extract the eigenvector corresponding to the largest eigenvalue by,
    #%using aind as a reference, you would get the correct eigenvector, but with sorted
    #%coefficients and, therefore, any follow-on calculation would seem to be in error.
    #%If alternative programming methods are used to evaluate the eigenvalues, e.g. Frame method
    #%followed by a root extraction on the characteristic equation, then the roots can be
    #%quickly sorted. One by one, the corresponding eigenvectors can be generated. The resultant
    #%array can be operated on using the Cholesky transformation, which enables a unit
    #%diagonalization of skk. But nowhere along the way are the coefficients within the
    #%eigenvector array ever changed. The final value of the "beta" array using either method
    #%should be the same.


    #% Compute the trace and max eigenvalue statistics */
    lr1 = zeros(m)
    lr2 = zeros(m)
    cvm = zeros((m,3))
    cvt = zeros((m,3))
    iota = ones(m)
    t, junk = rkt.shape
    for i in range(0, m):
        tmp = trimr(log(iota-a), i ,0)
        lr1[i] = -t * np.sum(tmp, 0)  #columnsum ?
        #tmp = np.log(1-a)
        #lr1[i] = -t * np.sum(tmp[i:])
        lr2[i] = -t * log(1-a[i])
        cvm[i,:] = c_sja(m-i,p)
        cvt[i,:] = c_sjt(m-i,p)
        aind[i]  = i
    #end

    result = Holder()
    #% set up results structure
    #estimation results, residuals
    result.rkt = rkt
    result.r0t = r0t
    result.eig = a
    result.evec = d  #transposed compared to matlab ?
    result.lr1 = lr1
    result.lr2 = lr2
    result.cvt = cvt
    result.cvm = cvm
    result.ind = aind
    result.meth = 'johansen'

    return result