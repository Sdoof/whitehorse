#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import lxml.html
import MySQLdb as mdb

from math import ceil

def obtain_parse_wiki_snp500():
  now = datetime.datetime.utcnow()
  page = lxml.html.parse('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
  symbolslist=page.xpath('//table[1]/tr')[1:502]

  symbols = []
  for i, symbol in enumerate(symbolslist):
   tds= symbol.getchildren()
   sd = {'ticker': tds[0].getchildren()[0].text, 'name': tds[2].getchildren()[0].text, 'sector': tds[3].text}
   symbols.append( (sd['ticker'],'stock', sd['name'], sd['sector'], 'USD', now, now))
  return symbols

def insert_snp500_symbols(symbols):
 db_host = 'localhost'
 db_user = 'sec_user'
 db_pass = 'password'
 db_name = 'securities_master'
 con = mdb.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name)
 column_str = "ticker, instrument, name, sector, currency, created_date, last_updated_date"
 insert_str = ("%s, " * 7 )[:-2]
 final_str = "INSERT INTO symbol (%s) VALUES (%s)" % (column_str, insert_str)
 print final_str, len(symbols)

 with con:
  cur = con.cursor()
  for i in range(0, int(ceil(len(symbols) / 100.0))):
   cur.executemany(final_str, symbols[i*100:(i+1)*100-1])

if __name__ == "__main__":
 symbols  = obtain_parse_wiki_snp500()
 insert_snp500_symbols(symbols)
# print symbols[:][0]\
