#!/usr/bin/python
# -*- coding: utf-8 -*-

# quandl_data.py

import pandas as pd
import urllib2

def construct_futures_symbols(symbol, start_year=2010, end_year=2014):
 futures = []
 months = 'HMUZ'
 for y in range(start_year, end_year+1):
  for m in months:
   futures.append("%s%s%s" % (symbol, m, y))
 return futures

def download_contract_from_quandl(contract, quth_token, dl_dir):
 api_call_head = "http://www.quandl.com/api/v1/datasets/OFDP/FUTURE_%s.csv" % contract
 params = "?&auth_token=%s&sort_order=asc" % auth_token
 
 data= urllib2.urlopen("%s%s" % (api_call_head, params)).read()

 fc = open('%s/%s.csv' % (dl_dir, contract), 'w')
 fc.write(data)
 fc.close()

def download_historical_contracts(symbol, auth_token, dl_dir, start_year=2010, end_year=2014):
 contracts = construct_futures_symbols(symbol, start_year, end_year)
 for c in contracts:
  download_contract_from_quandl(c, auth_token, dl_dir)

if __name__ == "__main__":
 symbol = 'ES'
 dl_dir = 'quandl/futures/ES'
 auth_token = 'w7YL9rMx8X9R8NTRVp8v'
 start_year = 2010
 end_year = 2014
 download_historical_contracts(symbol, auth_token, dl_dir, start_year, end_year)
 es = pd.io.parsers.read_csv("%s/ESZ2014.csv" % dl_dir)
