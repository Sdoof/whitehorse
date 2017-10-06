# -*- coding: utf-8 -*- 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from django.db import models
import sys

import urllib2

from bs4 import BeautifulSoup

sys.path.append("../")
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beCOMPANY.settings")
import beCOMPANY
import beCOMPANY.settings as bsettings
from main.models import *
import datetime
import re
import csv
import spark.company as comp

def output_csv(filename, queryset):

    opts = queryset.model._meta
    model = queryset.model
    f = open(filename, 'w')
    writer = csv.writer(f)
    field_names = [field.name for field in opts.fields]
    # Write a first row with header information
    writer.writerow(field_names)
    # Write data rows
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])
    f.close()

def read_csv():

    inst=comp.getInstrument('^GSPC', 'NYSE,NASDAQ', 'Index','Index','S&P 500')
    
    resource_list=Resource.objects.filter(company_name='S&P 500')
    resource=resource_list[0]
    resource.exchange='SP500'
    resource.save()
    exchange=resource.exchange
    #CompanyResource.objects.filter(resource_id=resource.id).delete()
    
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request("http://en.wikipedia.org/wiki/List_of_S%26P_500_companies", headers=hdr)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page, "lxml")

    table = soup.find('table', {'class': 'wikitable sortable'})
    sector_tickers = dict()
    for row in table.findAll('tr'):
        col = row.findAll('td')
        if len(col) > 0:
            sector = str(col[3].string.strip()).lower().replace(' ', '_')
            ticker = str(col[0].string.strip())
            a=col[1].find('a')
            url=a['href']
            market1 = str(col[3].string.strip())
            market2 = str(col[4].string.strip())
            markets=[market1,market2]
            name=str(col[1].string.strip())
                                
            jsonobj = {
              'name': name,
              'markets': markets,
              'ticker' : ticker,
              'is_public': True,
            }
            print jsonobj
            Symbol=ticker
            Name=name
            company=comp.getCompany(jsonobj)
            if company.exchange and not re.search('500',company.exchange):
                company.exchange=company.exchange+','+exchange
                print company.exchange
                company.save()
            else:
                company.exchange=exchange
                print company.exchange
                company.save()
            
            
            
            cr_list=CompanyResource.objects.filter(resource_id=resource.id, company_id=company.id)
            if cr_list and len(cr_list) > 0:
                cr=cr_list[0]
            else:
                cr=CompanyResource()
                cr.resource_id=resource.id
                cr.company_id=company.id
                cr.save()
                
            #(contractMonth,currency,evMultiplier,evRule,exchange,expiry,liquidHours,longName,minTick,secType,symbol,timeZoneId,tradingHours,underConId)=row
            inst_list=Instrument.objects.filter(resource_id=resource.id, company_id=company.id)
            #.filter(sym=symbol).filter(contractMonth=contractMonth).filter(secType=secType)
            if inst_list and len(inst_list) > 0:
                inst=inst_list[0]
            else:
                inst=Instrument()
                inst.company_id=company.id
                inst.resource_id=resource.id
                
                inst.broker='ib'
                #inst.contractMonth=contractMonth
                inst.cur='USD'
                inst.mult=1 #float(evMultiplier)
                #inst.evRule=evRule
                inst.exch=exchange 
                #inst.expiry=expiry
                #inst.liquidHours=liquidHours
                inst.longName=Name #longName
                #inst.minTick=minTick
                inst.sec_type='STK' #secType
                inst.sym=Symbol
                inst.local_sym=Symbol
                #inst.timeZoneId=timeZoneId
                #inst.tradingHours=tradingHours
                #inst.underConId=underConId
                inst.save()
            print "Saving ",inst.sym
            
            
read_csv()
