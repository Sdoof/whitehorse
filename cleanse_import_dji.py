# -*- coding: utf-8 -*- 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from django.db import models
import sys

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

def read_csv(filename):
    inst=comp.getInstrument('^DJI','DJI','Index','Index','Dow Jones Industrial Average')
    resource_list=Resource.objects.filter(company_name='Dow Jones Industrial Average')
    resource=resource_list[0]
    exchange2=resource.exchange
    #CompanyResource.objects.filter(resource_id=resource.id).delete()
    
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            (Name,exchange,Symbol,Industry)=row
            
            print row;
            #company_list=Company.objects.filter(company_name=Name)
            #if company_list and len(company_list) > 0:
            #    company=company_list[0]
            #else:
            #    company=Company()
            #company.exchange=exchange
            #company.ticker=Symbol
            #if Sector != 'n/a':
            #    markets.append(Sector)
            
            if Industry != 'n/a':
                if re.search(Industry,','):
                    markets=Industry.split(',')
                else:
                    markets=[]
                    markets.append(Industry)
                    
            jsonobj = {
              'name': Name,
              'markets': markets,
              'exchange': exchange + ',' + exchange2,
              'ticker' : Symbol,
              'is_public': True,
              #'company_website': Summary_Quote,
            }
            
            company=comp.getCompany(jsonobj)
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
                
            
            
read_csv('csv/dji.csv')
