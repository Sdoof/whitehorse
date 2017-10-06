#!/usr/bin/python
# -*- coding: utf8 -*-

import pandas as pd
import pandas.io.sql as psql
import MySQLdb as mdb

#Connect to MySQL
db_host = 'localhost'
db_user = 'sec_user'
db_pass = 'password'
db_name = 'securities_master'
con = mdb.connect(db_host, db_user, db_pass, db_name)

#select all of the historic Google adj close data
sql = """SELECT dp.price_date, dp.adj_close_price FROM symbol AS sym INNER JOIN daily_prices AS dp ON dp.symbol_id = sym.id WHERE sym.ticker = 'GOOG' ORDER BY dp.price_date ASC;"""

goog = psql.read_sql(sql, con=con, index_col='price_date')

print goog.tail()
