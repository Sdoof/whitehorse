#!/usr/bin/python
# -*- coding: utf-8 -*-

# price_retrieval.py

import datetime
import MySQLdb as mdb
import urllib2

db_host = 'localhost'
db_user = 'sec_user'
db_pass = 'password'
db_name = 'securities_master'
con = mdb.connect(db_host, db_user, db_pass, db_name)

def obtain_list_of_db_tickers():
 with con:
  cur = con.cursor()
  cur.execute("SELECT id, ticker from symbol")
  data = cur.fetchall()
  return [(d[0], d[1]) for d in data]

def get_daily_historic_data_yahoo(ticker, start_date=(2000,1,1), end_date= datetime.date.today().timetuple()[0:3]):

 """Obtains data from Yahoo Finance. 
    ticker: "GOOG"
    start_date: Start date in (YYYY,M,D)
    end_date: (YYYY, M, D) """

 yahoo_url = "http://ichart.finance.yahoo.com/table.csv?s=%s&a=%s&b=%s&c=%s&d=%s&e=%s&f=%s" % (ticker, start_date[1] - 1, start_date[2], start_date[0], end_date[1]-1, end_date[2], end_date[0])

 try:
  yf_data = urllib2.urlopen(yahoo_url).readlines()[1:]
  prices = []
  for y in yf_data:
   p = y.strip().split(',')
   prices.append((datetime.datetime.strptime(p[0], '%Y-%m-%d'), p[1], p[2], p[3], p[4], p[5], p[6]))
 except Exception, e:
   print "Could not download Yahoo data: %s" % e
 return prices

def insert_daily_data_into_db(data_vendor_id, symbol_id, daily_data):
  now = datetime.datetime.utcnow()
  daily_data = [(data_vendor_id, symbol_id, d[0], now, now, d[1], d[2], d[3], d[4], d[5], d[6]) for d in daily_data]
  
  column_str = """data_vendor_id, symbol_id, price_date, created_date, last_updated_date, open_price, high_price, low_price, close_price, volume, adj_close_price"""
  insert_str = ("%s, " * 11)[:-2]
  final_str = "INSERT INTO daily_prices (%s) VALUES (%s)" % (column_str, insert_str)

  with con:
   cur = con.cursor()
   cur.executemany(final_str, daily_data)

if __name__ == "__main__":
 tickers = obtain_list_of_db_tickers()
 for t in tickers:
  print "Adding data for %s" % t[1]
  yf_data = get_daily_historic_data_yahoo(t[1])
  insert_daily_data_into_db('1',t[0], yf_data)
