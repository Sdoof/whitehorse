# -*- coding: utf-8 -*- 
import re
import psycopg2
import logging
from datetime import datetime
import urllib2
from xml.dom import minidom
import requests
from time import gmtime, strftime, localtime, sleep
import json
from pandas.io.json import json_normalize
import numpy as np
import pandas as pd
import time as mytime
import logging
import os
import sys
import twitter
import linkedin
sys.path.append("../../../../")
sys.path.append("../../../")
sys.path.append("../../")
sys.path.append("../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beCOMPANY.settings")
import json
import codecs
import StringIO
import re
from django.template.defaultfilters import slugify
from django.db import models
from django.core.paginator import Page
import os
import beCOMPANY.settings as settings
from main.models import *
from BeautifulSoup import BeautifulSoup
import os
from cookielib import LWPCookieJar
import requests
import cookielib
from HTMLParser import HTMLParser
import json
from dateutil.parser import parse as parse_date
import subprocess
from os import listdir
from os.path import isfile, join
import os
import binascii
import hashlib
import hmac
import json
import socket
import time
import urllib
import urllib2

import re
import stem.process
import io
import pycurl
import stem.process
from stem.util import term
from stem import Signal
from stem.control import Controller
import random
from os import listdir
from os.path import isfile, join
from random import randint

crawl_source='angellist'


def getInstrument(sym, exchange, resource_type, commodity_type, name):
    
    
    inst_list=Instrument.objects.filter(sym=sym)
    if inst_list and len(inst_list) > 0:
        inst=inst_list[0]
    else:
        inst=Instrument()
        inst.sym=sym
        inst.exch=exchange
        inst.sec_type=resource_type
        inst.save()    

    if not inst.resource_id:
        resource_list=Resource.objects.filter(company_name=name)
        
        if resource_list and len(resource_list) > 0:
            resource=resource_list[0]
        else:
            resource=Resource()
    else:
        resource=inst.resource
    resource.company_name=name
    resource.owner_id=35
    resource.ticker=sym
    resource.exchange=exchange
    resource.resource_type=resource_type
    resource.commodity_type=commodity_type
    resource.save()
            
    inst.resource_id=resource.id
    inst.exch=exchange
    inst.save()

    return inst


def getCompanyJsonObj(json_obj):
    company=getCompany(json_obj)
    if company:
        getInvestors(json_obj,company)
        getFounders(json_obj, company)      
        getPortfolio(json_obj, company)
                
def getCompanyJson():
    mypath='./companies/'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for file in onlyfiles:
        
        if re.search('json', file):
            try:
                page = open(mypath + file, 'r')
                content=page.read()
                page.close()
                json_obj=json.loads(content)
                company=getCompany(json_obj)
                if company:
                    getInvestors(json_obj,company)
                    getFounders(json_obj, company)      
                    getPortfolio(json_obj, company)
            except Exception as e:
                print e

def getPeopleJson():
    mypath='./people/'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for file in onlyfiles:
        if re.search('json', file):
            try:
                page = open(mypath + file, 'r')
                content=page.read()
                page.close()
                json_obj=json.loads(content)
                company=getPerson(json_obj)
            except Exception as e:
                print e
                
round_dict=dict()
company_stage_dict=dict()
stage_dict=dict()
def getStage(name):
    if len(stage_dict.keys()) < 1:
        stage_list = FundingStage.objects.all()
        for stage in stage_list:
            if not stage.stage_step:
                stage.stage_step=getStageStep(stage.name)
                stage.save()
                
            stage_dict[stage.name]=stage
    
    if stage_dict.has_key(name):
        return stage_dict[name]
    else:
        stage=FundingStage()
        stage.name=name
        stage.save()
        return stage


def getStageStep(name):
    if name in ["Credit Guarantee Support",
                "Debt Financing",
                "Debt Financing",
                "Venture",
                "Series",
                "Bridge",
                "RCPS",
                "Round",
                "No Stage",
                "Venture",
                ]:
        return 3
    if name in ["Closed",
                "N.A",
                "Seed",
                "CB",
                "PF",
                "N/A",
                "Grant",
                "Crowdfunding",
                "Seed",
                "Angel",
                "Closed",
                "No Stage",
                "Series",
                "Angel",
                "Series A",
                "Pre Series A",
                "pre-Series A",
                "Pre Series A",
                "Series A",
                "Series A+"]:
        return 1
    elif name in [
            "Series B+",
            "Series B",
            "Series  B",
            "Series B",
            ]:
        return 2
    elif name in [
            "Series C",
            "Series C"
            ]:
        return 3
    elif name in [
            "Series D",
            "Series D"
            ]:
        return 4
    elif name in [
            "Series E",
            "Series E"
            ]:
        return 5    
    elif name in [
            "Series F",
            "Series F"
            ]:
        return 6
    elif name in [
            "Acquired",
            "Acquired",
            "IPO",
            "Exited",
            "IPO",
            "Take Over",
            ]:
        return 7
    else:
        return 1
    
def getCorrectName(name):
    if name:
        name=re.sub('Unknown','',name)
        name=re.sub('^[\s]*','',name)
        name=re.sub('[\s]*$','',name)
    if name == 'SeriesA':
        #print 'SeriesA'
        return 'Series A'
        
    elif name == 'Series Pre-A':
        #print 'Series Pre-A'
        return 'Pre Series A'
    elif re.search('A',name):
        return 'Series A'
    elif re.search('B',name):
        return 'Series B'
    elif re.search('C',name):
        return 'Series C'
    elif re.search('D',name):
        return 'Series D'
    elif re.search('Seed',name):
        return 'Seed'
    elif re.search('M &amp; A',name):
        return 'Acquired'
    elif re.search('IPO',name):
        return 'IPO'
    elif re.search('Investment',name):
        return 'Venture'
    elif re.search('Angel',name):
        return 'Angel'
    
    elif name == 'Fund':
        print 'Fund'
        return 'Fund'
    elif name == 'Series A - Early':
        #print 'Series A - Early'
        return 'Series A'
        
    elif name == 'Post-IPO Equity':
        #print 'Post-IPO Equity'
        return 'Post-IPO Equity'
    elif name == 'Private Equity':
        #print 'Private Equity'
        return 'Private Equity'
    elif name == 'Round A':
        #print 'Round A'
        return 'Series A'
        
    elif name == 'Loan':
        #print 'Loan'
        return 'Debt Financing'
        
    elif name == 'Venture':
        #print 'Venture'
        return 'Venture'
    elif name == 'Seris B' or name in [
            "Series B",
            "Series  B",
            "Series B"]:
        #print 'Series B'
        return 'Series B'
        
    elif name == 'Aqcuired':
        #print 'Aqcuired'
        return 'Acquired'
    elif name and re.search('Acquired',name):
        #print 'Acquired'
        return 'Acquired'
    elif name and re.search('Exited',name):
        #print 'Acquired'
        return 'Exited'
    elif name and re.search('Amgel',name):
        #print 'Acquired'
        return 'Angel'
    elif not name:
        #print 'Venture'
        return 'Venture'
    else:
        #print name
        return name    
    
def updateInvestorEvent(event, stage):
    name=getCorrectName(event.event_round)
    isUpdate=False
    if name:
        if name != event.event_round or not event.funding_stage or event.funding_stage != stage:
            print name, stage.id
            event.funding_stage=stage
            event.event_round=name
            investor_list=event.investor.all()
            for investor in investor_list:
                if not investor.funding_stage:
                    investor.funding_stage=stage
                    investor.save()
            isUpdate=True
        
        key=str(event.owner_id)+'|'+str(event.event_year) + '|' + str(event.event_month)
        round_dict[key]=stage
        if not company_stage_dict.has_key(event.owner_id):
            company_stage_dict[event.owner_id]=stage
        else:
            if company_stage_dict[event.owner_id].stage_step < stage.stage_step:
                company_stage_dict[event.owner_id]=stage
    if event.event_year >=1900 and event.event_year <= 10000:
        if event.event_month >= 1 and event.event_month <= 12:
            if not event.invest_date:
                invest_date=datetime(event.event_year,event.event_month, 1)
                event.invest_date=invest_date
                isUpdate=True
    if event.event_currency and len(event.event_currency) == 3:
        if not event.invest_currency:
            event.invest_currency=event.event_currency
            isUpdate=True
    amt=event.event_amount
    if amt:
        #amt=re.sub('\D','',amt)
        if not event.invest_amt and amt:
            event.invest_amt=round(int(amt))
            print "Saving Investment Amt", event.invest_amt,event
            isUpdate=True
    #if isUpdate:
    #    event.save()
        
def updateInvestor(invest, funding_stage_id):
    isUpdate=False
    amt=invest.investor_amount
            
    
    if not invest.funding_stage_id or invest.funding_stage_id != funding_stage_id or not invest.invest_amt:
        if amt:
            print amt
            #amt=re.sub('\D','',amt)
            if not invest.invest_amt and amt:
                invest.invest_amt=round(int(amt))
                print "Saving Investment Amt", invest.invest_amt,invest
        invest.funding_stage_id=funding_stage_id
        isUpdate=True
        
    if invest.investor_year >=1900 and invest.investor_year <= 10000:
        if invest.investor_month >= 1 and invest.investor_month <= 12:
            if not invest.invest_date:
                invest_date=datetime(invest.investor_year,invest.investor_month, 1)
                invest.invest_date=invest_date
                isUpdate=True
    if invest.investor_currency and len(invest.investor_currency) == 3:
        if not invest.invest_currency:
            invest.invest_currency=invest.investor_currency
            isUpdate=True



def getApp(company_id, product_id, json_obj):
    
    # Open 'file.txt' from the file system for 
    
    '''
     var jsonobj = 
        {
            company = models.ForeignKey(Company, null=True, db_index=True)
            product = models.ForeignKey(Product, null=True, db_index=True)

            platform = models.CharField(max_length=100, db_index=True)
            app_name = models.CharField(max_length=500, db_index=True)
            app_developer = models.CharField(max_length=500,null=True)
            app_developer_url = models.CharField(max_length=500,null=True)
            app_developer_id= models.CharField(max_length=500, null=True)
            app_numeric_id= models.CharField(max_length=100, null=True)
            app_id= models.CharField(max_length=100, null=True)
            app_url = models.CharField(max_length=500,null=True)
            app_icon= models.CharField(max_length=100, null=True)
            is_free=models.BooleanField(default=0, default=True, db_index=True)
            price=models.FloatField(null=True)
            
            
            updated_date = models.DateField(blank=True, null=True, db_index=True)
            released_date = models.DateField(blank=True, null=True, db_index=True)
            
            rank_all = models.IntegerField(default=0)
            rank_grossing = models.IntegerField(default=0)
            rank_min = models.IntegerField(default=0)
            rating_number = models.IntegerField(default=0, db_index=True)
            rating = models.FloatField(default=0.0, db_index=True)
            installation_number = models.CharField(
                max_length=200, blank=True, null=True, db_index=True)
            active_user = models.IntegerField(default=0, db_index=True)
       }
    '''    
    facebook=''
    twitter=''
    linkedin=''
    company_website=''
    ticker=''
    exchange=''
    logo=''
    city=''
    company_desc=''
    platform='ios'
    app_name=''
    app_developer=''
    app_developer_url=''
    app_developer_id=''
    app_numeric_id=''
    app_id=''
    app_url=''
    app_icon=''
    released_date=None
    is_free=True
    price=0
    rating=0
    rating_number=0
    installs=0
        
    if json_obj.has_key('platform'):
        platform=json_obj['platform']
        
    if json_obj.has_key('app_name'):
        app_name=json_obj['app_name'].encode('utf8')
    
    if json_obj.has_key('app_developer'):
        app_developer=json_obj['app_developer']
        
    if json_obj.has_key('app_developer_url'):
        app_developer_url=json_obj['app_developer_url']

    if json_obj.has_key('app_developer_id'):
        app_developer_id=json_obj['app_developer_id']
        

    if json_obj.has_key('app_numeric_id'):
        app_numeric_id=json_obj['app_numeric_id']
        

    if json_obj.has_key('app_id'):
        app_id=json_obj['app_id']
        

    if json_obj.has_key('app_url'):
        app_url=json_obj['app_url']
        

    if json_obj.has_key('app_icon'):
        app_icon=json_obj['app_icon']
        
    if json_obj.has_key('is_free'):
        is_free=json_obj['is_free']

    if json_obj.has_key('price'):
        price=json_obj['price']

    if json_obj.has_key('rating'):
        rating=json_obj['rating']
        
    if json_obj.has_key('rating_number'):
        rating_number=json_obj['rating_number']
    
    if json_obj.has_key('installs'):
        installs=json_obj['installs']
    
    if json_obj.has_key('released_date'):
        released_date=dateutil.parser.parse(json_obj['released_date'])
    
    
    if json_obj.has_key('short_desc'):
        company_desc=json_obj['short_desc'].encode('utf8')
        #stripped = lambda s: "".join(i for i in s if 31 < ord(i) < 127)
        #content=stripped(r.text)
        #company_desc=re.sub('^[\s]*','',company_desc)
        #company_desc=re.sub('[\s]*$','',company_desc)
        
    if json_obj.has_key('twitter_url'):
        twitter=json_obj['twitter_url'].encode('utf8')
        
    if json_obj.has_key('facebook_url'):
        facebook=json_obj['facebook_url']
        
    if json_obj.has_key('linkedin_url'):
        linkedin=json_obj['linkedin_url']
        
    if json_obj.has_key('logo_url'):
        logo=json_obj['logo_url']
        
    if json_obj.has_key('website_url'):
        company_website=json_obj['website_url']
        
    long_desc=''
    country=''
    
    if json_obj.has_key('location'):
        city=json_obj['location']
        
    markets=[]
    if json_obj.has_key('markets'):
        markets=json_obj['markets']
        
    tags=''
    prod_market_csv=''
    #if markets:
    #    (prod_market_csv, tags)=getMarkets(markets)
    
    if twitter:
            if re.search('twitter.com/',twitter.lower()):
                res=twitter.lower().split('twitter.com/')
                twitter=res[-1]
            twitter=re.sub('@','',twitter)
            twitter=re.sub('\s','',twitter)
            twitter=re.sub('/','',twitter)
            twitter=re.sub('^[\s]*','',twitter)
            twitter=re.sub('[\s]*$','',twitter)
            
    #app_name=re.sub('^[\s]*','',app_name)
    #app_name=re.sub('[\s]*$','',app_name)
    #app_name=re.sub('^\W','',app_name)
    #app_name=re.sub('\W$','',app_name)
    
    if not re.search('http',app_name) and len(app_name) < 500 and len(app_name) > 1:
            print app_name, '\n'
            apps=ApplicationInfo.objects.filter(app_id=app_id, product_id=product_id, app_name__iexact=app_name)
            if apps and len(apps) > 0:
                app=apps[0]
            else:
                app=ApplicationInfo()
                app.company_id=company_id
                app.product_id=product_id
                app.app_name=app_name
                
                app.platform=platform
                app.app_developer =app_developer ; # models.CharField(max_length=500,null=True)
                app.app_developer_url =app_developer_url ; # models.CharField(max_length=500,null=True)
                app.app_developer_id=app_developer_id; # models.CharField(max_length=500, null=True)
                app.app_numeric_id=app_numeric_id; # models.CharField(max_length=100, null=True)
                app.app_id=app_id; # models.CharField(max_length=100, null=True)
                app.app_url =app_url ; # models.CharField(max_length=500,null=True)
                app.app_icon=app_icon; # models.CharField(max_length=100, null=True)
                app.is_free=is_free; #models.BooleanField(default=0, default=True, db_index=True)
                app.price=price; #models.FloatField(null=True)
                app.released_date=released_date
                #app.updated_date =updated_date ; # models.DateField(blank=True, null=True, db_index=True)
                #app.released_date =released_date ; # models.DateField(blank=True, null=True, db_index=True)
                
                #app.rank_all =rank_all ; # models.IntegerField(default=0)
                #app.rank_grossing =rank_grossing ; # models.IntegerField(default=0)
                #app.rank_min =rank_min ; # models.IntegerField(default=0)
                app.rating_number =rating_number ; # models.IntegerField(default=0, db_index=True)
                app.rating =rating ; # models.FloatField(default=0.0, db_index=True)
                app.installation_number =installs #ation_number ; # models.CharField(
                #app.active_user =active_user ; # models.IntegerField(default=0, db_index=True)
                
                app.save()
                
            if rating_number and rating:
                apps=ApplicationStatus.objects.filter(product_id=product_id, platform=platform, updated_year=datetime.now().year, updated_month=datetime.now().month)
                if not apps or len(apps) < 1:
                    app=ApplicationStatus()
                    #app.company_id=company_id
                    app.platform=platform
                    app.product_id=product_id
                    app.app_name=app_name
                    app.app_developer =app_developer ; # models.CharField(max_length=500,null=True)
                    #app.app_developer_url =app_developer_url ; # models.CharField(max_length=500,null=True)
                    #app.app_developer_id=app_developer_id; # models.CharField(max_length=500, null=True)
                    #app.app_numeric_id=app_numeric_id; # models.CharField(max_length=100, null=True)
                    #app.app_id=app_id; # models.CharField(max_length=100, null=True)
                    #app.app_url =app_url ; # models.CharField(max_length=500,null=True)
                    #app.app_icon=app_icon; # models.CharField(max_length=100, null=True)
                    #app.is_free=is_free; #models.BooleanField(default=0, default=True, db_index=True)
                    #app.price=price; #models.FloatField(null=True)
                    #app.released_date=released_date
                    
                    #app.updated_date =updated_date ; # models.DateField(blank=True, null=True, db_index=True)
                    #app.released_date =released_date ; # models.DateField(blank=True, null=True, db_index=True)
                    
                    #app.rank_all =rank_all ; # models.IntegerField(default=0)
                    #app.rank_grossing =rank_grossing ; # models.IntegerField(default=0)
                    #app.rank_min =rank_min ; # models.IntegerField(default=0)
                    app.rating_number =rating_number ; # models.IntegerField(default=0, db_index=True)
                    
                    app.updated_year = datetime.now().year
                    
                    app.updated_month = datetime.now().month
                    
                    app.updated_week = 1
                    
                    app.rating =rating ; # models.FloatField(default=0.0, db_index=True)
                    app.installation_number = installs #installation_number ; # models.CharField(
                    #app.active_user =active_user ; # models.IntegerField(default=0, db_index=True)
                    
                    app.save()
def getCompany(json_obj):
    
    # Open 'file.txt' from the file system for 
    
    '''
     var jsonobj = 
        {
          'name': name,
          'short_desc':short_desc,
          "description": description
          'product_desc': product_desc,
          'product_img':product_img,
          'location': location,
          'markets': markets,
          'logo_url' : logo_url,
          'company_size':employee_count,
          'twitter_url':twitter,
          'facebook_url':facebook,
          'linkedin_url':linkedin,
          'website_url': website,
          'exchange': exchange,
          'ticker': ticker,
          'is_public': is_public,
          'blog_url':blog,
          'founders':founders,
          'investments':investments,
          'investors':investors,
          'employees':employees,
          'advisors':advisors,
          'board_members':board_members,
          'portfolios':portfolio,
          'portfolio_investors':portfolio_investors,
          'title': product_name
    
       }
    '''    
    facebook=''
    twitter=''
    linkedin=''
    company_website=''
    ticker=''
    exchange=''
    logo=''
    city=''
    long_name=''
    company_desc=''
    is_public=False
    released_date=None
    established=None
    
    company_name=json_obj['name'].encode('utf8')
    
    if json_obj.has_key('company_name'):
        company_name=json_obj['company_name'].encode('utf8')
        company_name=re.sub('^[\s]*','',company_name)
        company_name=re.sub('[\s]*$','',company_name)
    
    if json_obj.has_key('long_name'):
        long_name=json_obj['long_name'].encode('utf8')
        long_name=re.sub('^[\s]*','',long_name)
        long_name=re.sub('[\s]*$','',long_name)
    
    if json_obj.has_key('description'):
        company_desc=json_obj['description'].encode('utf8')
        
    if json_obj.has_key('released_date'):
        released_date=dateutil.parser.parse(json_obj['released_date'])

    if json_obj.has_key('established'):
        established=dateutil.parser.parse(json_obj['established'])
           
    if json_obj.has_key('ticker'):
        ticker=json_obj['ticker']
        
    if json_obj.has_key('exchange'):
        exchange=json_obj['exchange']
        
    if json_obj.has_key('is_public'):
        is_public=json_obj['is_public']
    
    if json_obj.has_key('short_desc'):
        company_desc=json_obj['short_desc'].encode('utf8')
        #stripped = lambda s: "".join(i for i in s if 31 < ord(i) < 127)
        #content=stripped(r.text)
        company_desc=re.sub('^[\s]*','',company_desc)
        company_desc=re.sub('[\s]*$','',company_desc)
        
    if json_obj.has_key('twitter_url'):
        twitter=json_obj['twitter_url'].encode('utf8')
        
    if json_obj.has_key('facebook_url'):
        facebook=json_obj['facebook_url']
        
    if json_obj.has_key('linkedin_url'):
        linkedin=json_obj['linkedin_url']
        
    if json_obj.has_key('logo_url'):
        logo=json_obj['logo_url']
    
    if json_obj.has_key('website_url'):
        company_website=json_obj['website_url']
    long_desc=''
    country=''
    if json_obj.has_key('location'):
        city=json_obj['location']
    markets=[]
    if json_obj.has_key('markets'):
        markets=json_obj['markets']
    tags=''
    prod_market_csv=''
    if markets:
        (prod_market_csv, tags)=getMarkets(markets)
    
    print prod_market_csv
    if twitter:
            if re.search('twitter.com/',twitter.lower()):
                res=twitter.lower().split('twitter.com/')
                twitter=res[-1]
            twitter=re.sub('@','',twitter)
            twitter=re.sub('\s','',twitter)
            twitter=re.sub('/','',twitter)
            twitter=re.sub('^[\s]*','',twitter)
            twitter=re.sub('[\s]*$','',twitter)
    company_name=re.sub('^[\s]*','',company_name)
    company_name=re.sub('[\s]*$','',company_name)
    #company_name=re.sub('^\W','',company_name)
    #company_name=re.sub('\W$','',company_name)
    company=None
    
    if not re.search('http',company_name) and len(company_name) < 300 and len(company_name) > 1:
            print company_name, '\n'
            print tags,'\n',  
            #print logo,'\n', 
            #print company_desc,'\n',
            print country,'\n',company_website,'\n',prod_market_csv,'\n'
            if twitter:
                print twitter,'\n'
                
            if facebook:
                print facebook,'\n'
                
            if linkedin:
                print linkedin,'\n'
            print "Name: ", company_name
            #print "Desc: ",company_desc
            #print "Long-Desc:",long_desc
            companies=Company.objects.filter(company_name__iexact=company_name)
            if companies and len(companies) > 0:
                company=companies[0]
            else:
                company=Company()
                user_id=35
                company.owner_id=user_id
                company.company_name=company_name
                
                if long_name:
                    company.company_kor_name=long_name
                if tags:
                    company.company_top_keywords=tags
                if tags:
                    company.company_industry=tags
                if logo:
                    company.company_logo=logo
                if city:
                    company.company_city=city
                if country:
                    company.company_country=country
                if company_website:
                    company.company_website=company_website
                if long_desc:
                    company.company_long=long_desc
                if company_desc:
                    company.company_short=company_desc
                if twitter:
                    company.company_twitter=twitter
                if facebook:
                    company.company_facebook_page=facebook
                if linkedin:
                    company.company_linkedin_page=linkedin
                if prod_market_csv:
                    company.product_market_csv=prod_market_csv
                if ticker:
                    company.ticker=ticker
                if exchange:
                    company.exchange=exchange
                if is_public:
                    company.is_public=is_public
                    
                if established:
                    company.company_established = str(established.year) + '-' + str(established.month) + '-' + str(established.day)
                    
                    company.company_founded_year = established.year
                
                    company.company_founded_month = established.month
                
                    company.company_founded_day = established.day
                
                company.crawl_source=crawl_source
                
                if company_name:
                    company.save()
                    print "Company ID", company.id
                    
                    if json_obj.has_key('company_size'):
                        size=json_obj['company_size']
                        if size:
                            if re.search('-',size):
                                sizes=size.split('-')
                                if sizes[0] and sizes[1]:
                                    size=str(round((int(sizes[0]) + int(sizes[1]))/2))
                                else:
                                    size=sizes[0]
                            size=re.sub('\D','',size)
                            print 'Employee Size',size
                            if size:
                                update_date=datetime.now()
                                emp_status=EmployeeStatus.objects.filter(company_id=company.id).filter(updated_year=update_date.year).filter(updated_month=update_date.month)
                                if emp_status and len(emp_status) > 0:
                                    employee=emp_status[0]
                                else:
                                    employee=EmployeeStatus()
                                    employee.company_id=company.id
                                    employee.updated_year=update_date.year
                                    employee.updated_month=update_date.month
                                    employee.updated_day=1
                                employee.crawl_source=crawl_source
                                employee.employee=int(size)
                                employee.save()
                    
    if company and json_obj.has_key('product_desc') and json_obj.has_key('product_img') and json_obj.has_key('product_name') and len(json_obj['product_name']) >= 3:
        product_desc=json_obj['product_desc'].encode('utf8')
        product_img=json_obj['product_img']
        product_website=''
        product_email=''
        app_store_url=''
        google_play_url=''
        video_url=''
        isFree=True
        screenshots=[]
        
        if json_obj.has_key('free'):
            isFree=json_obj['free']
            
        if json_obj.has_key('product_website'):
            product_website=json_obj['product_website']
        if json_obj.has_key('video'):
            video_url=json_obj['video']
            
        if json_obj.has_key('video_url'):
            video_url=json_obj['video_url']
            
        if json_obj.has_key('screenshots'):
            screenshots=json_obj['screenshots']
        
        if json_obj.has_key('app_store_url'):
            app_store_url=json_obj['app_store_url']
            if not re.search('http', app_store_url):
                app_store_url=''
        
        if json_obj.has_key('google_play_url'):
            google_play_url=json_obj['google_play_url']
            if not re.search('http', google_play_url):
                google_play_url=''
                
        if json_obj.has_key('product_email'):
            product_email=json_obj['product_email']
            
        if json_obj.has_key('product_name') and len(json_obj['product_name']) >= 3:
            product_name=json_obj['product_name'].encode('utf8')
        else:
            product_name=company.company_name
        
        product_list=Product.objects.filter(owner_id=company.id).filter(product_name__iexact=product_name)
            
        if product_list and len(product_list) > 0:
            product=product_list[0]
        else:
            product=Product()
            product.owner_id=company.id
            if product_name:
                product.product_name=product_name
            else:
                product.product_name=company.company_name
            
            
            if product_desc:
                product.product_short=product_desc
                print product.product_short
                
            if len(screenshots) > 0:
                #i=0
                #for screenshot in screenshots:
                #    if re.search('^\/',screenshots[i]):
                #        screenshots[i]='http:' + screenshots[i]
                #    i+=1
                #product.product_video=screenshots[0]
                product.product_screenshot_1=screenshots[0]
                if len(screenshots) > 1:
                    product.product_screenshot_2=screenshots[1]
                if len(screenshots) > 2:
                    product.product_screenshot_3=screenshots[2]
                if len(screenshots) > 3:
                    product.product_screenshot_4=screenshots[3]
                if len(screenshots) > 4:
                    product.product_screenshot_5=screenshots[4]
                if len(screenshots) > 5:
                    product.product_screenshot_6=screenshots[5]
                if len(screenshots) > 6:
                    product.product_screenshot_7=screenshots[6]
                if len(screenshots) > 8:
                    product.product_screenshot_8=screenshots[7]
                if len(screenshots) > 9:
                    product.product_screenshot_9=screenshots[8]
                if len(screenshots) > 10:
                    product.product_screenshot_10=screenshots[9]
                product.product_screenshot_count=len(screenshots)
                
            elif product_img:
                product.product_screenshot_1=product_img
                #product.product_video=product_img
            if video_url:
                product.product_video=video_url
                
            if twitter:
                product.product_twitter=twitter
            if facebook:
                product.product_facebook_page=facebook
            if linkedin:
                product.product_linkedin_page=linkedin
            if prod_market_csv:
                product.product_market_csv=prod_market_csv
            if tags:
                product.product_market=tags
            if app_store_url:
                product.product_app_store=app_store_url
            if google_play_url:
                product.product_google_play=google_play_url
            product.is_free=isFree
            
            if product_email:
                product.owner_email=product_email
            
            if logo:
                product.product_logo=logo
            
            if released_date:
                product.product_release_year=released_date.year
                product.product_release_month=released_date.month
                product.product_release_day=released_date.day
            
            product.owner_name=company.company_name
            
            if product_website and re.search('http',product_website):
                product.product_website=product_website
                
            elif company_website and re.search('http',company_website):
                product.product_website=company_website
            product.save()
            
            if prod_market_csv:
                market_dict=product.get_dict_industries_from_csv()
                for market_id in market_dict.keys():
                    rank_list=ProductRanking.objects.filter(product_id=product.id).filter(market_id=market_id)
                    if rank_list and len(rank_list) > 0:
                        rank=rank_list[0]
                    else:
                        rank=ProductRanking()
                        rank.product_id=product.id
                        rank.market_id=market_id
                        rank.save()
    if json_obj.has_key('return_product'):
        return company, product          
                        
    return company

def getPortfolio(json_obj,company):
    # investors
    '''
    var portfolio={
                                                'name': name,
                                                'link': link,
                                                'img':img,
                                                'investor_type':investor_type,
                                                'record_type':record_type,
                                                'bio':bio,
                                                'slug':slug,
                                            }
    '''
    if json_obj.has_key('portfolios'):
        portfolios=json_obj['portfolios']
        
        for portfolio in portfolios:
            if portfolio.has_key('record_type'):
                if portfolio['record_type'] == 'User':
                    procUser(portfolio, 'Portfolio',company)
                    return
            
            if portfolio and portfolio.has_key('name'):
                name=portfolio['name']
                img=''
                bio=''
                if json_obj.has_key('name'):
                    name=json_obj['name']
                    if re.search('\(',name):
                        names=name.split('(')
                        name=''.join(names[0:-1])
                        if re.search('\)',names[-1]):
                            names2=name.split(')')
                            name2=names2[-1]
                            name2=re.sub('^[\s]*','',name2)
                            name2=re.sub('[\s]*$','',name2)
                            name+=' ' + name2

               
                    name=re.sub('^[\s]*','',name)
                    name=re.sub('[\s]*$','',name)
                    
                if portfolio.has_key('investor_type'):
                    investor_type=portfolio['investor_type']
                    
                if portfolio.has_key('img'):
                    img=portfolio['img']
                    if re.search('\?',img):
                        imgs=img.split('?')
                        img=''.join(imgs[0:-1])
                if portfolio.has_key('bio'):
                    bio=portfolio['bio']
                
                co_list=Company.objects.filter(company_name__iexact=name)
                if co_list and len(co_list) > 0:
                    mycompany=co_list[0]
                else:
                    mycompany=Company()
                    user_id=35
                    mycompany.owner_id=user_id
                    mycompany.company_name=name
                    mycompany.company_logo=img
                    mycompany.company_short=bio
                    mycompany.crawl_source=crawl_source
                    mycompany.save();
                portfolio_id=mycompany.id
                ci_list=CompanyPortfolio.objects.filter(investee_id=portfolio_id).filter(owner=company)
                
                if ci_list and len(ci_list)>0:
                   ci=ci_list[0]
                   print "CompanyPortfolio Found", ci.id
                else:
                    ci=CompanyPortfolio()
                    ci.portfolio_company_id = str(portfolio_id)
                    ci.portfolio_company_name = mycompany.company_name
                    ci.investee = mycompany
                    ci.owner=company
                    ci.crawl_source=crawl_source
                    ci.save()
                    print "CompanyPortfolio", ci.id

def getInvestors(json_obj,company):
    # investors
    investments=json_obj['investments']
    for investment in investments:
        #print investor_list
        investors=investment['investors']
        num_cos=len(investors)
        round=investment['stage']
        has_round=False
        if round:
            print round
            round=re.sub('Round:','',round)
            round=re.sub('^[\s]*','',round)
            round=re.sub('[\s]*$','',round)
            stage_list=FundingStage.objects.filter(name=round)
            if stage_list and len(stage_list) > 0:
                stage=stage_list[0]
            else:
                stage=FundingStage()
                stage.name=round
                stage.save()
            print "Round,",round
            has_round=True
            
        round_size=investment['raised_amt']
        has_size=False
        if round_size:
            print round_size
            round_size=re.sub('Round Size:','',round_size)
            round_size=re.sub('^[\s]*','',round_size)
            round_size=re.sub('[\s]*$','',round_size)
            round_size=re.sub('US\$','',round_size)
            if re.search('M',round_size):
                round_size=re.sub('M','',round_size)
                round_size=int(float(round_size) * 1000000)
            elif re.search('K',round_size):
                round_size=re.sub('K','',round_size)
                round_size=int(float(round_size) * 1000)
            elif re.search('B',round_size):
                round_size=re.sub('B','',round_size)
                round_size=int(float(round_size) * 1000000000)
            else:
                round_size=re.sub('\D','',round_size)
                if round_size:
                    round_size=int(float(round_size))
                else:
                    round_size=0
            print "Round Size,",round_size
            total_round_size=round_size
            individual_round_size=total_round_size
            if num_cos > 1:
                individual_round_size/=num_cos
            print "Round Size,",individual_round_size," each "
            round_size=individual_round_size
            has_size=True
        
        round_date=investment['date']
        has_date=False
        if round_date:
            print round_date
            round_date=re.sub('Date:','',round_date)
            round_date=re.sub('^[\s]*','',round_date)
            round_date=re.sub('[\s]*$','',round_date)
            round_date=parse_date(round_date)
            print "Date,",round_date.year,'-',round_date.month
            has_date=True
        '''
        var investors={
                'name': name,
                'link': link,
                'img':img,
                //'investor_type':investor_type,
                //'location':loc,
                'slug':slug,
            }
        var jsonobj={
                'stage':stage,
                'date':date,
                'raised_amt':raised_amt,
                'article_url':article_url,
                'investors':investors,
            }
        '''
        
        if has_round and has_size and has_date:
            #print content
            investor_ids=[]
            for investor in investors:
                #investor=investor.find('table-col')
                if investor and investor.has_key('name'):
                    #print investor
                    
                    name=investor['name']
                    co_list=Company.objects.filter(company_name=name)
                    if co_list and len(co_list) > 0:
                        mycompany=co_list[0]
                    else:
                        mycompany=Company()
                        user=User.objects.get(pk=35)
                        mycompany.owner=user
                        mycompany.company_name=name
                        mycompany.crawl_source=crawl_source
                        mycompany.save();
                    investor_id=mycompany.id
                    investor_ids.append(investor_id)
            
            CompanyInvestor.objects.filter(owner=company).filter(investor_year=round_date.year).filter(investor_month=round_date.month).delete()
            CompanyInvestingEvent.objects.filter(owner=company).filter(event_year=round_date.year).filter(event_month=round_date.month).delete()
            
            for investor_id in investor_ids:
                if investor_id:
                    round_date=datetime(round_date.year,round_date.month,1)
                    ci_list=CompanyInvestor.objects.filter(investor_id=investor_id).filter(owner=company).filter(investor_year=round_date.year).filter(investor_month=round_date.month)
                    if ci_list and len(ci_list)>0:
                       ci=ci_list[0]
                       print "CompanyInvestor Found", ci.id
                    else:
                        ci=CompanyInvestor()
                        ci.investor_currency='USD'
                        ci.investor_amount=round_size
                        ci.investor_day=1
                        ci.investor_month=round_date.month
                        ci.investor_year=round_date.year
                        ci.created_time= round_date
                        ci.last_edited_time=round_date
                        ci.is_user_input=False
                        ci.investor_id=investor_id
                        ci.owner=company
                        ci.funding_stage=stage
                        ci.is_active=True
                        ci.is_tips=False
                        ci.crawl_source=crawl_source
                        ci.is_estimate=True
                        updateInvestor(ci, stage.id)
                        ci.save()
                        print "CompanyInvestor", ci.id
                     
                    
                    event_list=CompanyInvestingEvent.objects.filter(owner=company).filter(event_round=stage.name).filter(event_year=round_date.year).filter(event_month=round_date.month)
                    if event_list and len(event_list) > 0:
                        event=event_list[0]
                        event.investor=CompanyInvestor.objects.filter(owner=company).filter(investor_year=round_date.year).filter(investor_month=round_date.month)
                        event.save()
                        print "Event Found", event.id
                    else:
                        event=CompanyInvestingEvent()
                        event.event_round=stage.name
                        event.funding_stage=stage
                        event.event_currency='USD'
                        event.event_amount=total_round_size
                        event.event_day=1
                        event.event_month=round_date.month
                        event.event_year=round_date.year
                        event.created_time= round_date
                        event.last_edited_time=round_date
                        event.is_user_input=False
                        event.owner=company
                        event.is_tips=False
                        event.save()
                        event.investor=CompanyInvestor.objects.filter(owner=company).filter(investor_year=round_date.year).filter(investor_month=round_date.month)
                        event.crawl_source=crawl_source
                        updateInvestorEvent(event, stage)
                        event.save()
                        print "Event Found", event.id
         

def getFounders(json_obj,company):
    '''
        var advisors={
                'name': name,
                'link': link,
                'img':img,
                'title':role_title,
                'record_type':record_type,
                'bio':bio,
                'slug':slug,
            }
        var board={
                                                'name': name,
                                                'link': link,
                                                'img':img,
                                                'title':role_title,
                                                'record_type':record_type,
                                                'bio':bio,
                                                'slug':slug,
                                            }
                          
        var employee={
                                                'name': name,
                                                'link': link,
                                                'img':img,
                                                'title':role_title,
                                                'record_type':record_type,
                                                'bio':bio,
                                                'slug':slug,
                                            }
            var founders={
                                                    'name':name,
                                                    'img':img,
                                                    'link':link,
                                                    'bio':bio,
                                                    'slug':slug,
                                                }
            var portfolio_investors={
                                                'name': name,
                                                'link': link,
                                                'record_type':record_type,
                                                'slug':slug,
                                            }
                                            
        var investors={
                                                'name': name,
                                                'link': link,
                                                'img':img,
                                                'investor_type':investor_type,
                                                'record_type':record_type,
                                                'bio':bio,
                                                'slug':slug,
                                            }
    '''
    # investors
    if json_obj.has_key('advisors'):
        advisors=json_obj['advisors']
        for advisor in advisors:
            procUser(advisor, 'Advisor', company)

    if json_obj.has_key('board_members'):
        board_members=json_obj['board_members']
        for advisor in board_members:
            procUser(advisor, 'Board Member', company)
    
    if json_obj.has_key('founders'):
        founders=json_obj['founders']
        for advisor in founders:
            procUser(advisor, 'Founder', company)
    
    if json_obj.has_key('employees'):   
        employees=json_obj['employees']
        for advisor in employees:
            procUser(advisor, 'Employee', company)
        
    if json_obj.has_key('portfolio_investors'):
        portfolio_investors=json_obj['portfolio_investors']
        for advisor in portfolio_investors:
            procUser(advisor, 'Portfolio Investor', company)
    
    if json_obj.has_key('investors'):
        investors=json_obj['investors']
        for advisor in investors:
            procUser(advisor, 'Investor', company)    
            #print investor_list
        
def procUser(advisor, role, company):
        if advisor.has_key('record_type'):
            if advisor['record_type'] != 'User':
                return
        if not advisor.has_key('name') or len(advisor['name']) < 2 or not re.search(' ',advisor['name']):
            return
        print advisor
        name=advisor['name']
        link=advisor['link']
        slug=advisor['slug']
        username=slug
        if len(username) > 20:
            username=username[0:20]
        username+=str(randint(1000000,9999999))
        
        img=''
        bio=''
        title=''
        record_type=''
        investor_type=''
        
            
        if advisor.has_key('investor_type'):
            investor_type=advisor['investor_type']
            
        if advisor.has_key('img'):
            img=advisor['img']
            if re.search('\?',img):
                imgs=img.split('?')
                img=''.join(imgs[0:-1])
        if advisor.has_key('bio'):
            bio=advisor['bio']
        if advisor.has_key('title'):
            title=advisor['title']
        else:
            title=role

        first_name=''
        last_name=''        
        if advisor.has_key('name'):
            name=advisor['name']
            if re.search('\(',name):
                names=name.split('(')
                name=''.join(names[0:-1])
                if re.search('\)',names[-1]):
                    names2=name.split(')')
                    name2=names2[-1]
                    name2=re.sub('^[\s]*','',name2)
                    name2=re.sub('[\s]*$','',name2)
                    name+=' ' + name2
                
            name=re.sub('^[\s]*','',name)
            name=re.sub('[\s]*$','',name)

        if re.search(' ',name):    
            names=name.split(' ')
            last_name=names[-1]
            first_name=' '.join(names[0:-1])
            
        user_list=UserDefault.objects.filter(first_name=first_name).filter(last_name=last_name).filter(is_public=True).filter(crawl_source=crawl_source)
        if user_list and len(user_list) > 0:
            user=user_list[0]
        else:
            user_account=User()
            user_account.username=username
            user_account.save()
            
            user=UserDefault()
            user.user_id=user_account.id
            user.first_name=first_name
            user.last_name=last_name
            user.is_public=True
            
        print 'Saving',user.first_name, ' ',last_name
            
        user.crawl_source=crawl_source
        user.profile_image=img
        user.title=title
        user.company=company.company_name
        user.save()
        
        profile=UserProfile()
        profile.user_id=user.user_id
        profile.profile_image=img
        profile.profile_cv_accomplishment=bio
        profile.profile_cv_mini=title
        profile.is_public=True
        profile.save()
        
        if user:
            member_list=CompanyMember.objects.filter(owner_id=company.id).filter(user_id=user.user_id)
            if member_list and len(member_list) > 0:
                member=member_list[0]
            else:
                member=CompanyMember()
                member.owner=company
                member.user_id=user.user_id
            member.user_title=title
            member.user_role=role
            member.user_name=first_name + ' ' + last_name
            member.crawl_source=crawl_source
            print 'Saving',member.user_name
            member.save()
            
        
                                    
def getMarkets(markets):
    keyword_csv=''
    market_csv=''   
    if markets:
        
        for market in markets:
            market=re.sub('^[\s]*','',market)
            market=re.sub('[\s]*$','',market)
            if market and len(market) > 1:
                #print market,','
                marketdb=Market.objects.filter(name=market)
                if len(marketdb) < 1:
                    marketdb=Market()
                    marketdb.name=market
                    marketdb.crawl_source=crawl_source
                    marketdb.save()
                else:
                    marketdb=marketdb[0]
                keyword_csv+=marketdb.name + ','
                market_csv+=str(marketdb.id) + '|' + market + ';'
    return ( market_csv, keyword_csv )

def getSchools(schools_json):
    keyword_csv=''
    school_csv=''   
    university=''
    if schools_json:
        
        for school_json in schools_json:
            school=school_json['name']
            
            school=re.sub('^[\s]*','',school)
            school=re.sub('[\s]*$','',school)
            if school and len(school) > 1:
                if not university:
                    university=school
                #print school,','
                schooldb=School.objects.filter(name=school)
                if len(schooldb) < 1:
                    schooldb=School()
                    schooldb.name=school
                    schooldb.crawl_source=crawl_source
                    schooldb.save()
                    print "Added School ID",school
                else:
                    schooldb=schooldb[0]
                    print "Found School ID",schooldb.id
                keyword_csv+=schooldb.name + ','
                school_csv+=str(schooldb.id) + '|' + school + ';'
    return ( school_csv, keyword_csv, university)

# People #
def getPerson(json_obj):
    
    '''
    {  
   "angel_id":"45184",
   "board_companies":[  
      {  
         "link":"https://angel.co/novatel-wireless",
         "name":"Novatel Wireless",
         "record_type":"Startup",
         "slug":"novatel-wireless"
      },
      {  
         "link":"https://angel.co/tellabs",
         "name":"Tellabs",
         "record_type":"Startup",
         "slug":"tellabs"
      }
   ],
   "city":"",
   "education":[  
      {  
         "classmates":[  

         ],
         "degree_name":"",
         "degree_type":"",
         "description":"",
         "full_degree_name":"",
         "graduation_month":"",
         "graduation_month_name":"",
         "graduation_year":"",
         "id":57356,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/new_tags/i/86172-b65118dadbfbfdf625601f9fceca737b-medium.png",
         "link":"https://angel.co/tel-aviv-university",
         "majors":[  

         ],
         "name":"Tel Aviv University",
         "new_tag":{  
            "display_name":"Tel Aviv University",
            "logo_src":"https://d1qb2nb5cznatu.cloudfront.net/new_tags/i/86172-b65118dadbfbfdf625601f9fceca737b-medium.png?buster=1440133912",
            "slug_url":"https://angel.co/tel-aviv-university",
            "tag_url":"https://angel.co/tel-aviv-university"
         },
         "new_tag_id":86172,
         "slug":"tel-aviv-university",
         "user_id":45184
      },
      {  
         "classmates":[  

         ],
         "degree_name":"",
         "degree_type":"",
         "description":"",
         "full_degree_name":"",
         "graduation_month":"",
         "graduation_month_name":"",
         "graduation_year":"",
         "id":57366,
         "img":"https://angel.co/images/shared/nopic_college.png",
         "link":"https://angel.co/open-university-of-israel",
         "majors":[  

         ],
         "name":"Open University of Israel",
         "new_tag":{  
            "display_name":"Open University of Israel",
            "logo_src":"https://angel.co/images/shared/nopic_college.png",
            "slug_url":"https://angel.co/open-university-of-israel",
            "tag_url":"https://angel.co/open-university-of-israel"
         },
         "new_tag_id":81809,
         "slug":"open-university-of-israel",
         "user_id":45184
      }
   ],
   "experience":[  
      {  
         "date_range":"",
         "dates_for_select":{  
            "ended_at":{  
               "month":"",
               "year":""
            },
            "started_at":{  
               "month":"",
               "year":""
            }
         },
         "desc":"",
         "featured":true,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/37992-14a2e8a09b2d806b3e8ea888b3bdf963-thumb_jpg.jpg",
         "link":"https://angel.co/arbinet",
         "name":"Arbinet",
         "past":false,
         "pending_approval":false,
         "role":"Founder",
         "slug":"arbinet",
         "startup_avatar":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/37992-14a2e8a09b2d806b3e8ea888b3bdf963-thumb_jpg.jpg?buster=1326847151",
         "startup_company_name":"Arbinet",
         "startup_high_concept":"",
         "startup_id":37992,
         "startup_slug_url":"https://angel.co/arbinet",
         "title":"Founder",
         "token":"BHK",
         "who_confirms":"startup",
         "work_from":"",
         "work_to":""
      },
      {  
         "date_range":"",
         "dates_for_select":{  
            "ended_at":{  
               "month":"",
               "year":""
            },
            "started_at":{  
               "month":"",
               "year":""
            }
         },
         "desc":"",
         "featured":true,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/45890-70c036c0f32960ab83234c76b53276a9-thumb_jpg.jpg",
         "link":"https://angel.co/transit-wireless",
         "name":"Transit Wireless",
         "past":false,
         "pending_approval":false,
         "role":"Founder",
         "slug":"transit-wireless",
         "startup_avatar":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/45890-70c036c0f32960ab83234c76b53276a9-thumb_jpg.jpg?buster=1326853969",
         "startup_company_name":"Transit Wireless",
         "startup_high_concept":"",
         "startup_id":45890,
         "startup_slug_url":"https://angel.co/transit-wireless",
         "title":"Founder",
         "token":"BHM",
         "who_confirms":"startup",
         "work_from":"",
         "work_to":""
      },
      {  
         "date_range":"",
         "dates_for_select":{  
            "ended_at":{  
               "month":"",
               "year":""
            },
            "started_at":{  
               "month":"",
               "year":""
            }
         },
         "desc":"",
         "featured":true,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/37969-14f2f7513dd3e75b7e6681ad4ef99f6f-thumb_jpg.jpg",
         "link":"https://angel.co/tellabs",
         "name":"Tellabs",
         "past":false,
         "pending_approval":false,
         "role":"Board_member",
         "slug":"tellabs",
         "startup_avatar":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/37969-14f2f7513dd3e75b7e6681ad4ef99f6f-thumb_jpg.jpg?buster=1410579214",
         "startup_company_name":"Tellabs",
         "startup_high_concept":"",
         "startup_id":37969,
         "startup_slug_url":"https://angel.co/tellabs",
         "title":"Board_member",
         "token":"fWEC",
         "who_confirms":"startup",
         "work_from":"",
         "work_to":""
      },
      {  
         "date_range":"Apr '14 to Nov '15",
         "dates_for_select":{  
            "ended_at":{  
               "month":11,
               "year":2015
            },
            "started_at":{  
               "month":4,
               "year":2014
            }
         },
         "desc":"",
         "featured":true,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/184683-3e1e720b6df3e26fd651dd659d1aacf7-thumb_jpg.jpg",
         "link":"https://angel.co/novatel-wireless",
         "name":"Novatel Wireless",
         "past":true,
         "pending_approval":false,
         "role":"Employee",
         "slug":"novatel-wireless",
         "startup_avatar":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/184683-3e1e720b6df3e26fd651dd659d1aacf7-thumb_jpg.jpg?buster=1407036586",
         "startup_company_name":"Novatel Wireless",
         "startup_high_concept":"",
         "startup_id":184683,
         "startup_slug_url":"https://angel.co/novatel-wireless",
         "title":"CEO",
         "token":"fWEU",
         "who_confirms":"startup",
         "work_from":"2014-4-01",
         "work_to":"2015-11-01"
      },
      {  
         "date_range":"May '04 to Nov '11",
         "dates_for_select":{  
            "ended_at":{  
               "month":11,
               "year":2011
            },
            "started_at":{  
               "month":5,
               "year":2004
            }
         },
         "desc":"",
         "featured":true,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/45889-b56fb5cab81c88387df5b6e5d498c198-thumb_jpg.jpg",
         "link":"https://angel.co/groundlink",
         "name":"GroundLink",
         "past":true,
         "pending_approval":false,
         "role":"Employee",
         "slug":"groundlink",
         "startup_avatar":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/45889-b56fb5cab81c88387df5b6e5d498c198-thumb_jpg.jpg?buster=1326853967",
         "startup_company_name":"GroundLink",
         "startup_high_concept":"",
         "startup_id":45889,
         "startup_slug_url":"https://angel.co/groundlink",
         "title":"CEO",
         "token":"3KeZ",
         "who_confirms":"startup",
         "work_from":"2004-5-01",
         "work_to":"2011-11-01"
      },
      {  
         "date_range":"",
         "dates_for_select":{  
            "ended_at":{  
               "month":"",
               "year":""
            },
            "started_at":{  
               "month":"",
               "year":""
            }
         },
         "desc":"",
         "featured":false,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/45889-b56fb5cab81c88387df5b6e5d498c198-thumb_jpg.jpg",
         "link":"https://angel.co/groundlink",
         "name":"GroundLink",
         "past":false,
         "pending_approval":false,
         "role":"Founder",
         "slug":"groundlink",
         "startup_avatar":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/45889-b56fb5cab81c88387df5b6e5d498c198-thumb_jpg.jpg?buster=1326853967",
         "startup_company_name":"GroundLink",
         "startup_high_concept":"",
         "startup_id":45889,
         "startup_slug_url":"https://angel.co/groundlink",
         "title":"Founder",
         "token":"BHL",
         "who_confirms":"startup",
         "work_from":"",
         "work_to":""
      },
      {  
         "date_range":"",
         "dates_for_select":{  
            "ended_at":{  
               "month":"",
               "year":""
            },
            "started_at":{  
               "month":"",
               "year":""
            }
         },
         "desc":"",
         "featured":false,
         "img":"https://angel.co/images/shared/nopic_startup.png",
         "link":"https://angel.co/comgates",
         "name":"Comgates",
         "past":false,
         "pending_approval":false,
         "role":"Founder",
         "slug":"comgates",
         "startup_avatar":"https://angel.co/images/shared/nopic_startup.png",
         "startup_company_name":"Comgates",
         "startup_high_concept":"",
         "startup_id":45891,
         "startup_slug_url":"https://angel.co/comgates",
         "title":"Founder",
         "token":"BHN",
         "who_confirms":"startup",
         "work_from":"",
         "work_to":""
      },
      {  
         "date_range":"",
         "dates_for_select":{  
            "ended_at":{  
               "month":"",
               "year":""
            },
            "started_at":{  
               "month":"",
               "year":""
            }
         },
         "desc":"",
         "featured":false,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/45892-f263bbc91a3f7c02a7324dd4cde90671-thumb_jpg.jpg",
         "link":"https://angel.co/elematics",
         "name":"Elematics",
         "past":false,
         "pending_approval":false,
         "role":"Founder",
         "slug":"elematics",
         "startup_avatar":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/45892-f263bbc91a3f7c02a7324dd4cde90671-thumb_jpg.jpg?buster=1326853971",
         "startup_company_name":"Elematics",
         "startup_high_concept":"",
         "startup_id":45892,
         "startup_slug_url":"https://angel.co/elematics",
         "title":"Founder",
         "token":"BHP",
         "who_confirms":"startup",
         "work_from":"",
         "work_to":""
      },
      {  
         "date_range":"",
         "dates_for_select":{  
            "ended_at":{  
               "month":"",
               "year":""
            },
            "started_at":{  
               "month":"",
               "year":""
            }
         },
         "desc":"",
         "featured":false,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/45893-68cdc4df647684ec4ba0921229128e40-thumb_jpg.jpg",
         "link":"https://angel.co/governing-dynamics",
         "name":"Governing Dynamics",
         "past":false,
         "pending_approval":false,
         "role":"Founder",
         "slug":"governing-dynamics",
         "startup_avatar":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/45893-68cdc4df647684ec4ba0921229128e40-thumb_jpg.jpg?buster=1326853973",
         "startup_company_name":"Governing Dynamics",
         "startup_high_concept":"",
         "startup_id":45893,
         "startup_slug_url":"https://angel.co/governing-dynamics",
         "title":"Founder",
         "token":"BHQ",
         "who_confirms":"startup",
         "work_from":"",
         "work_to":""
      },
      {  
         "date_range":"",
         "dates_for_select":{  
            "ended_at":{  
               "month":"",
               "year":""
            },
            "started_at":{  
               "month":"",
               "year":""
            }
         },
         "desc":"",
         "featured":false,
         "img":"https://angel.co/images/shared/nopic_startup.png",
         "link":"https://angel.co/voicesmart",
         "name":"VoiceSmart",
         "past":false,
         "pending_approval":false,
         "role":"Founder",
         "slug":"voicesmart",
         "startup_avatar":"https://angel.co/images/shared/nopic_startup.png",
         "startup_company_name":"VoiceSmart",
         "startup_high_concept":"",
         "startup_id":45895,
         "startup_slug_url":"https://angel.co/voicesmart",
         "title":"Founder",
         "token":"BHT",
         "who_confirms":"startup",
         "work_from":"",
         "work_to":""
      },
      {  
         "date_range":"",
         "dates_for_select":{  
            "ended_at":{  
               "month":"",
               "year":""
            },
            "started_at":{  
               "month":"",
               "year":""
            }
         },
         "desc":"",
         "featured":false,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/45897-965cec0c553c087323f3f3441a909017-thumb_jpg.jpg",
         "link":"https://angel.co/limores",
         "name":"LimoRes",
         "past":false,
         "pending_approval":false,
         "role":"Founder",
         "slug":"limores",
         "startup_avatar":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/45897-965cec0c553c087323f3f3441a909017-thumb_jpg.jpg?buster=1326853977",
         "startup_company_name":"LimoRes",
         "startup_high_concept":"",
         "startup_id":45897,
         "startup_slug_url":"https://angel.co/limores",
         "title":"Founder",
         "token":"BHV",
         "who_confirms":"startup",
         "work_from":"",
         "work_to":""
      },
      {  
         "date_range":"",
         "dates_for_select":{  
            "ended_at":{  
               "month":"",
               "year":""
            },
            "started_at":{  
               "month":"",
               "year":""
            }
         },
         "desc":"",
         "featured":false,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/45890-70c036c0f32960ab83234c76b53276a9-thumb_jpg.jpg",
         "link":"https://angel.co/transit-wireless",
         "name":"Transit Wireless",
         "past":false,
         "pending_approval":false,
         "role":"Employee",
         "slug":"transit-wireless",
         "startup_avatar":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/45890-70c036c0f32960ab83234c76b53276a9-thumb_jpg.jpg?buster=1326853969",
         "startup_company_name":"Transit Wireless",
         "startup_high_concept":"",
         "startup_id":45890,
         "startup_slug_url":"https://angel.co/transit-wireless",
         "title":"Employee",
         "token":"3Kf1",
         "who_confirms":"startup",
         "work_from":"",
         "work_to":""
      },
      {  
         "date_range":"",
         "dates_for_select":{  
            "ended_at":{  
               "month":"",
               "year":""
            },
            "started_at":{  
               "month":"",
               "year":""
            }
         },
         "desc":"",
         "featured":false,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/45894-c8248df084e02731771584232690c003-thumb_jpg.jpg",
         "link":"https://angel.co/digimeld",
         "name":"DigiMeld",
         "past":false,
         "pending_approval":false,
         "role":"Employee",
         "slug":"digimeld",
         "startup_avatar":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/45894-c8248df084e02731771584232690c003-thumb_jpg.jpg?buster=1409066356",
         "startup_company_name":"DigiMeld",
         "startup_high_concept":"",
         "startup_id":45894,
         "startup_slug_url":"https://angel.co/digimeld",
         "title":"Employee",
         "token":"BHS",
         "who_confirms":"startup",
         "work_from":"",
         "work_to":""
      },
      {  
         "date_range":"",
         "dates_for_select":{  
            "ended_at":{  
               "month":"",
               "year":""
            },
            "started_at":{  
               "month":"",
               "year":""
            }
         },
         "desc":"Join the movement. Unleash your inner health hero.",
         "featured":false,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/296014-c350bbd67de98dc4d4bf1b4830be8cd9-thumb_jpg.jpg",
         "link":"https://angel.co/healthgames",
         "name":"HealthGames",
         "past":false,
         "pending_approval":false,
         "role":"Advisor",
         "slug":"healthgames",
         "startup_avatar":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/296014-c350bbd67de98dc4d4bf1b4830be8cd9-thumb_jpg.jpg?buster=1387560913",
         "startup_company_name":"HealthGames",
         "startup_high_concept":"Join the movement. Unleash your inner health hero.",
         "startup_id":296014,
         "startup_slug_url":"https://angel.co/healthgames",
         "title":"Advisor",
         "token":"5Y6y",
         "who_confirms":"tagged",
         "work_from":"",
         "work_to":""
      },
      {  
         "date_range":"",
         "dates_for_select":{  
            "ended_at":{  
               "month":"",
               "year":""
            },
            "started_at":{  
               "month":"",
               "year":""
            }
         },
         "desc":"Rights Resolution and Content Monetization Platform",
         "featured":false,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/1188874-026a04edc97e5d18b89e69255de45d5d-thumb_jpg.jpg",
         "link":"https://angel.co/dubset-2",
         "name":"Dubset",
         "past":false,
         "pending_approval":false,
         "role":"Advisor",
         "slug":"dubset-2",
         "startup_avatar":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/1188874-026a04edc97e5d18b89e69255de45d5d-thumb_jpg.jpg?buster=1465904416",
         "startup_company_name":"Dubset",
         "startup_high_concept":"Rights Resolution and Content Monetization Platform",
         "startup_id":1188874,
         "startup_slug_url":"https://angel.co/dubset-2",
         "title":"Advisor",
         "token":"t4HR",
         "who_confirms":"tagged",
         "work_from":"",
         "work_to":""
      },
      {  
         "date_range":"",
         "dates_for_select":{  
            "ended_at":{  
               "month":"",
               "year":""
            },
            "started_at":{  
               "month":"",
               "year":""
            }
         },
         "desc":"Venture Capital Direct Secondaries (liquidity) and Equity Exchange Fund",
         "featured":false,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/85752-11a43486a8f7bd2614db07f6cdd4e9c0-thumb_jpg.jpg",
         "link":"https://angel.co/the-founders-club",
         "name":"The Founders Club",
         "past":false,
         "pending_approval":false,
         "role":"Advisor",
         "slug":"the-founders-club",
         "startup_avatar":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/85752-11a43486a8f7bd2614db07f6cdd4e9c0-thumb_jpg.jpg?buster=1335383986",
         "startup_company_name":"The Founders Club",
         "startup_high_concept":"Venture Capital Direct Secondaries (liquidity) and Equity Exchange Fund",
         "startup_id":85752,
         "startup_slug_url":"https://angel.co/the-founders-club",
         "title":"Advisor",
         "token":"28VG",
         "who_confirms":"tagged",
         "work_from":"",
         "work_to":""
      },
      {  
         "date_range":"",
         "dates_for_select":{  
            "ended_at":{  
               "month":"",
               "year":""
            },
            "started_at":{  
               "month":"",
               "year":""
            }
         },
         "desc":"",
         "featured":false,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/46045-5898138776d1e4c43802fb0dfffc36de-thumb_jpg.jpg",
         "link":"https://angel.co/cvidya",
         "name":"cVidya",
         "past":false,
         "pending_approval":false,
         "role":"Advisor",
         "slug":"cvidya",
         "startup_avatar":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/46045-5898138776d1e4c43802fb0dfffc36de-thumb_jpg.jpg?buster=1408332734",
         "startup_company_name":"cVidya",
         "startup_high_concept":"",
         "startup_id":46045,
         "startup_slug_url":"https://angel.co/cvidya",
         "title":"Advisor",
         "token":"4mGn",
         "who_confirms":"startup",
         "work_from":"",
         "work_to":""
      },
      {  
         "date_range":"",
         "dates_for_select":{  
            "ended_at":{  
               "month":"",
               "year":""
            },
            "started_at":{  
               "month":"",
               "year":""
            }
         },
         "desc":"",
         "featured":false,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/184683-3e1e720b6df3e26fd651dd659d1aacf7-thumb_jpg.jpg",
         "link":"https://angel.co/novatel-wireless",
         "name":"Novatel Wireless",
         "past":false,
         "pending_approval":false,
         "role":"Board_member",
         "slug":"novatel-wireless",
         "startup_avatar":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/184683-3e1e720b6df3e26fd651dd659d1aacf7-thumb_jpg.jpg?buster=1407036586",
         "startup_company_name":"Novatel Wireless",
         "startup_high_concept":"",
         "startup_id":184683,
         "startup_slug_url":"https://angel.co/novatel-wireless",
         "title":"Board_member",
         "token":"fWEM",
         "who_confirms":"startup",
         "work_from":"",
         "work_to":""
      },
      {  
         "date_range":"Jan '95 to Jan '00, Jan '00 to Mar '11",
         "dates_for_select":{  
            "ended_at":{  
               "month":1,
               "year":2000
            },
            "started_at":{  
               "month":1,
               "year":1995
            }
         },
         "desc":"",
         "featured":false,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/37992-14a2e8a09b2d806b3e8ea888b3bdf963-thumb_jpg.jpg",
         "link":"https://angel.co/arbinet",
         "name":"Arbinet",
         "past":true,
         "pending_approval":false,
         "role":"Employee",
         "slug":"arbinet",
         "startup_avatar":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/37992-14a2e8a09b2d806b3e8ea888b3bdf963-thumb_jpg.jpg?buster=1326847151",
         "startup_company_name":"Arbinet",
         "startup_high_concept":"",
         "startup_id":37992,
         "startup_slug_url":"https://angel.co/arbinet",
         "title":"CEO",
         "token":"mD8s",
         "who_confirms":"startup",
         "work_from":"1995-1-01",
         "work_to":"2000-1-01"
      }
   ],
   "facebook_url":"http://www.facebook.com/profile.php?id=700526486",
   "founded_companies":[  
      {  
         "link":"https://angel.co/groundlink",
         "name":"GroundLink",
         "record_type":"Startup",
         "slug":"groundlink"
      },
      {  
         "link":"https://angel.co/arbinet",
         "name":"Arbinet",
         "record_type":"Startup",
         "slug":"arbinet"
      },
      {  
         "link":"https://angel.co/elematics",
         "name":"Elematics",
         "record_type":"Startup",
         "slug":"elematics"
      },
      {  
         "link":"https://angel.co/governing-dynamics",
         "name":"Governing Dynamics",
         "record_type":"Startup",
         "slug":"governing-dynamics"
      },
      {  
         "link":"https://angel.co/limores",
         "name":"LimoRes",
         "record_type":"Startup",
         "slug":"limores"
      },
      {  
         "link":"https://angel.co/voicesmart",
         "name":"VoiceSmart",
         "record_type":"Startup",
         "slug":"voicesmart"
      },
      {  
         "link":"https://angel.co/comgates",
         "name":"Comgates",
         "record_type":"Startup",
         "slug":"comgates"
      },
      {  
         "link":"https://angel.co/transit-wireless",
         "name":"Transit Wireless",
         "record_type":"Startup",
         "slug":"transit-wireless"
      }
   ],
   "linkedin_url":"http://www.linkedin.com/pub/alex-mashinsky/0/1/906",
   "location":[  
      "United States",
      "New York City",
      "San Francisco",
      "United Kingdom"
   ],
   "logo_url":"https://d1qb2nb5cznatu.cloudfront.net/users/45184-large",
   "long_desc":"Help with strategy, introductions, recruiting, execution, IP, exits. Vision, Founded 7 startups, raised over $300m, Hired over 500 team members, had 4 exits totaling over $1b, authored over 50 patents, invested in more than 60 startups, passed investing in google, skype, ICQ and a few others (ouch). Most of what I learned was from my failures and from trying to do too much at the same time.",
   "markets":[  
      "Clean Technology",
      "Advertising Exchanges",
      "Electrical Distribution",
      "Telecommunications",
      "Internet",
      "Gift Card",
      "Gift Registries",
      "Mobile Coupons",
      "Local Coupons",
      "Local Search",
      "Transportation",
      "Mobile",
      "VoIP",
      "Music",
      "Search",
      "Automotive",
      "Internet Infrastructure",
      "Communities",
      "Big Data",
      "Mobile Advertising",
      "Music Services",
      "Cloud-Based Music",
      "SaaS",
      "Advertising",
      "Analytics",
      "Mobile Commerce",
      "Marketplaces",
      "Loyalty Programs",
      "Social Commerce",
      "Crowdsourcing"
   ],
   "name":"Alex Mashinsky",
   "portfolios":[  
      {  
         "company":{  
            "company_name":"cVidya",
            "high_concept":"",
            "id":46045,
            "logo_thumb_url":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/46045-5898138776d1e4c43802fb0dfffc36de-thumb_jpg.jpg?buster=1408332734",
            "quality":8.24,
            "slug_url":"https://angel.co/cvidya"
         },
         "confirmed":true,
         "desc":"",
         "exit":"Acquired by Amdocs",
         "featured":false,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/46045-5898138776d1e4c43802fb0dfffc36de-thumb_jpg.jpg",
         "investments":[  
            {  
               "amount":200000,
               "round":"Series C",
               "year":2014
            }
         ],
         "link":"https://angel.co/cvidya",
         "name":"cVidya",
         "record_type":"Company",
         "role":"Investor",
         "slug":"cvidya",
         "title":"Investor",
         "token":"48j9"
      },
      {  
         "company":{  
            "company_name":"AIP",
            "high_concept":"",
            "id":62111,
            "logo_thumb_url":"https://angel.co/images/shared/nopic_startup.png",
            "quality":6.57,
            "slug_url":"https://angel.co/aip"
         },
         "confirmed":true,
         "desc":"",
         "exit":"",
         "featured":false,
         "img":"https://angel.co/images/shared/nopic_startup.png",
         "investments":[  

         ],
         "link":"https://angel.co/aip",
         "name":"AIP",
         "record_type":"Company",
         "role":"Investor",
         "slug":"aip",
         "title":"Investor",
         "token":"48ja"
      },
      {  
         "company":{  
            "company_name":"Alkemy Environmental ",
            "high_concept":"Alkemy is paid to convert toxic ash into building materials sold for high profit",
            "id":21699,
            "logo_thumb_url":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/21699-007218abfe94789f7ff5402a3fba0347-thumb_jpg.jpg?buster=1315731863",
            "quality":7.01,
            "slug_url":"https://angel.co/alkemy-environmental"
         },
         "confirmed":true,
         "desc":"Alkemy is paid to convert toxic ash into building materials sold for high profit",
         "exit":"",
         "featured":false,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/21699-007218abfe94789f7ff5402a3fba0347-thumb_jpg.jpg",
         "investments":[  

         ],
         "link":"https://angel.co/alkemy-environmental",
         "name":"Alkemy Environmental ",
         "record_type":"Company",
         "role":"Investor",
         "slug":"alkemy-environmental",
         "title":"Investor",
         "token":"fA1"
      },
      {  
         "company":{  
            "company_name":"Name.Space",
            "high_concept":"Top-Level Domain Registry",
            "id":27999,
            "logo_thumb_url":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/27999-6f3f34f295e5add77f2808138c9d3f1b-thumb_jpg.jpg?buster=1324516252",
            "quality":7.3,
            "slug_url":"https://angel.co/name-space"
         },
         "confirmed":true,
         "desc":"Top-Level Domain Registry",
         "exit":"",
         "featured":false,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/27999-6f3f34f295e5add77f2808138c9d3f1b-thumb_jpg.jpg",
         "investments":[  

         ],
         "link":"https://angel.co/name-space",
         "name":"Name.Space",
         "record_type":"Company",
         "role":"Investor",
         "slug":"name-space",
         "title":"Investor",
         "token":"Qiz"
      },
      {  
         "company":{  
            "company_name":"nSphere",
            "high_concept":"nSphere provide access to properietary local content and helps publishers monetize it",
            "id":22147,
            "logo_thumb_url":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/22147-b2a3bb971bd6cac3f4da4dec7b949ac9-thumb_jpg.jpg?buster=1315731397",
            "quality":6.83,
            "slug_url":"https://angel.co/nsphere"
         },
         "confirmed":true,
         "desc":"nSphere provide access to properietary local content and helps publishers monetize it",
         "exit":"",
         "featured":false,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/22147-b2a3bb971bd6cac3f4da4dec7b949ac9-thumb_jpg.jpg",
         "investments":[  

         ],
         "link":"https://angel.co/nsphere",
         "name":"nSphere",
         "record_type":"Company",
         "role":"Investor",
         "slug":"nsphere",
         "title":"Investor",
         "token":"MN7"
      },
      {  
         "company":{  
            "company_name":"Novatel Wireless",
            "high_concept":"",
            "id":184683,
            "logo_thumb_url":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/184683-3e1e720b6df3e26fd651dd659d1aacf7-thumb_jpg.jpg?buster=1407036586",
            "quality":7.75,
            "slug_url":"https://angel.co/novatel-wireless"
         },
         "confirmed":true,
         "desc":"",
         "exit":"",
         "featured":false,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/184683-3e1e720b6df3e26fd651dd659d1aacf7-thumb_jpg.jpg",
         "investments":[  
            {  
               "amount":4000000,
               "round":"Series C",
               "year":2014
            }
         ],
         "link":"https://angel.co/novatel-wireless",
         "name":"Novatel Wireless",
         "record_type":"Company",
         "role":"Investor",
         "slug":"novatel-wireless",
         "title":"Investor",
         "token":"ennf"
      },
      {  
         "company":{  
            "company_name":"eBuddy",
            "high_concept":"Web & Smartphone Instant Messenger with 400m downloads. ",
            "id":22626,
            "logo_thumb_url":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/22626-67403624b25857d002a712b90a10758f-thumb_jpg.jpg?buster=1315730873",
            "quality":10,
            "slug_url":"https://angel.co/ebuddy"
         },
         "confirmed":true,
         "desc":"Web & Smartphone Instant Messenger with 400m downloads. ",
         "exit":"Acquired",
         "featured":false,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/22626-67403624b25857d002a712b90a10758f-thumb_jpg.jpg",
         "investments":[  

         ],
         "link":"https://angel.co/ebuddy",
         "name":"eBuddy",
         "record_type":"Company",
         "role":"Investor",
         "slug":"ebuddy",
         "title":"Investor",
         "token":"gPe"
      },
      {  
         "company":{  
            "company_name":"Slide",
            "high_concept":"",
            "id":32430,
            "logo_thumb_url":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/32430-04173531c67440ad1e1f2531921e52d9-thumb_jpg.jpg?buster=1326842673",
            "quality":10,
            "slug_url":"https://angel.co/slide"
         },
         "confirmed":true,
         "desc":"",
         "exit":"Acquired by Google",
         "featured":false,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/32430-04173531c67440ad1e1f2531921e52d9-thumb_jpg.jpg",
         "investments":[  

         ],
         "link":"https://angel.co/slide",
         "name":"Slide",
         "record_type":"Company",
         "role":"Investor",
         "slug":"slide",
         "title":"Investor",
         "token":"WkW"
      },
      {  
         "company":{  
            "company_name":"TrialPay",
            "high_concept":"Transactional advertising platform",
            "id":32497,
            "logo_thumb_url":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/32497-9a2569437cd0f297b795c25b7e629b54-thumb_jpg.jpg?buster=1345490812",
            "quality":10,
            "slug_url":"https://angel.co/trialpay"
         },
         "confirmed":true,
         "desc":"Transactional advertising platform",
         "exit":"Acquired by Visa",
         "featured":false,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/32497-9a2569437cd0f297b795c25b7e629b54-thumb_jpg.jpg",
         "investments":[  

         ],
         "link":"https://angel.co/trialpay",
         "name":"TrialPay",
         "record_type":"Company",
         "role":"Investor",
         "slug":"trialpay",
         "title":"Investor",
         "token":"WmH"
      },
      {  
         "company":{  
            "company_name":"Tellabs",
            "high_concept":"",
            "id":37969,
            "logo_thumb_url":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/37969-14f2f7513dd3e75b7e6681ad4ef99f6f-thumb_jpg.jpg?buster=1410579214",
            "quality":6.95,
            "slug_url":"https://angel.co/tellabs"
         },
         "confirmed":true,
         "desc":"",
         "exit":"Acquired for $890M",
         "featured":false,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/37969-14f2f7513dd3e75b7e6681ad4ef99f6f-thumb_jpg.jpg",
         "investments":[  
            {  
               "amount":0,
               "round":"",
               "year":2014
            }
         ],
         "link":"https://angel.co/tellabs",
         "name":"Tellabs",
         "record_type":"Company",
         "role":"Investor",
         "slug":"tellabs",
         "title":"Investor",
         "token":"fWE8"
      },
      {  
         "company":{  
            "company_name":"IronPlanet",
            "high_concept":"",
            "id":39430,
            "logo_thumb_url":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/39430-c9ff71098c12d96d77a944cc7d3be1f0-thumb_jpg.jpg?buster=1326848311",
            "quality":8.6,
            "slug_url":"https://angel.co/ironplanet"
         },
         "confirmed":true,
         "desc":"",
         "exit":"Acquired by Richie Brothers Auctioneers",
         "featured":false,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/39430-c9ff71098c12d96d77a944cc7d3be1f0-thumb_jpg.jpg",
         "investments":[  
            {  
               "amount":2000000,
               "round":"Series A",
               "year":2010
            }
         ],
         "link":"https://angel.co/ironplanet",
         "name":"IronPlanet",
         "record_type":"Company",
         "role":"Investor",
         "slug":"ironplanet",
         "title":"Investor",
         "token":"BHW"
      },
      {  
         "company":{  
            "company_name":"Intelius",
            "high_concept":"",
            "id":45899,
            "logo_thumb_url":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/45899-77c4507c9cd32e385ba3d53da1f55410-thumb_jpg.jpg?buster=1326853979",
            "quality":6.57,
            "slug_url":"https://angel.co/intelius"
         },
         "confirmed":true,
         "desc":"",
         "exit":"",
         "featured":false,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/45899-77c4507c9cd32e385ba3d53da1f55410-thumb_jpg.jpg",
         "investments":[  

         ],
         "link":"https://angel.co/intelius",
         "name":"Intelius",
         "record_type":"Company",
         "role":"Investor",
         "slug":"intelius",
         "title":"Investor",
         "token":"BJ1"
      },
      {  
         "company":{  
            "company_name":"DigiMeld",
            "high_concept":"",
            "id":45894,
            "logo_thumb_url":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/45894-c8248df084e02731771584232690c003-thumb_jpg.jpg?buster=1409066356",
            "quality":6.57,
            "slug_url":"https://angel.co/digimeld"
         },
         "confirmed":true,
         "desc":"",
         "exit":"",
         "featured":false,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/45894-c8248df084e02731771584232690c003-thumb_jpg.jpg",
         "investments":[  

         ],
         "link":"https://angel.co/digimeld",
         "name":"DigiMeld",
         "record_type":"Company",
         "role":"Investor",
         "slug":"digimeld",
         "title":"Investor",
         "token":"BJ2"
      },
      {  
         "company":{  
            "company_name":"Arno Pharmacuticals",
            "high_concept":"",
            "id":45900,
            "logo_thumb_url":"https://angel.co/images/shared/nopic_startup.png",
            "quality":6.81,
            "slug_url":"https://angel.co/arno-pharmacuticals"
         },
         "confirmed":true,
         "desc":"",
         "exit":"2006 IPO",
         "featured":false,
         "img":"https://angel.co/images/shared/nopic_startup.png",
         "investments":[  

         ],
         "link":"https://angel.co/arno-pharmacuticals",
         "name":"Arno Pharmacuticals",
         "record_type":"Company",
         "role":"Investor",
         "slug":"arno-pharmacuticals",
         "title":"Investor",
         "token":"BJ3"
      },
      {  
         "company":{  
            "company_name":"Local Matters",
            "high_concept":"",
            "id":45901,
            "logo_thumb_url":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/45901-c648b55a2e3c698ef31596e6b72fa51d-thumb_jpg.jpg?buster=1326853981",
            "quality":7.29,
            "slug_url":"https://angel.co/local-matters"
         },
         "confirmed":true,
         "desc":"",
         "exit":"",
         "featured":false,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/45901-c648b55a2e3c698ef31596e6b72fa51d-thumb_jpg.jpg",
         "investments":[  

         ],
         "link":"https://angel.co/local-matters",
         "name":"Local Matters",
         "record_type":"Company",
         "role":"Investor",
         "slug":"local-matters",
         "title":"Investor",
         "token":"BJ4"
      },
      {  
         "company":{  
            "company_name":"Arbinet",
            "high_concept":"",
            "id":37992,
            "logo_thumb_url":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/37992-14a2e8a09b2d806b3e8ea888b3bdf963-thumb_jpg.jpg?buster=1326847151",
            "quality":10,
            "slug_url":"https://angel.co/arbinet"
         },
         "confirmed":true,
         "desc":"",
         "exit":"2004 IPO",
         "featured":false,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/37992-14a2e8a09b2d806b3e8ea888b3bdf963-thumb_jpg.jpg",
         "investments":[  

         ],
         "link":"https://angel.co/arbinet",
         "name":"Arbinet",
         "record_type":"Company",
         "role":"Investor",
         "slug":"arbinet",
         "title":"Investor",
         "token":"BJ5"
      },
      {  
         "company":{  
            "company_name":"GroundLink",
            "high_concept":"",
            "id":45889,
            "logo_thumb_url":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/45889-b56fb5cab81c88387df5b6e5d498c198-thumb_jpg.jpg?buster=1326853967",
            "quality":10,
            "slug_url":"https://angel.co/groundlink"
         },
         "confirmed":true,
         "desc":"",
         "exit":"Acquired by Comvest Partners",
         "featured":false,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/45889-b56fb5cab81c88387df5b6e5d498c198-thumb_jpg.jpg",
         "investments":[  

         ],
         "link":"https://angel.co/groundlink",
         "name":"GroundLink",
         "record_type":"Company",
         "role":"Investor",
         "slug":"groundlink",
         "title":"Investor",
         "token":"BJ6"
      },
      {  
         "company":{  
            "company_name":"Miasole",
            "high_concept":"",
            "id":34658,
            "logo_thumb_url":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/34658-a45ed4a16e8ba10eee6cfd6151a476bb-thumb_jpg.jpg?buster=1326844623",
            "quality":8.94,
            "slug_url":"https://angel.co/miasole"
         },
         "confirmed":true,
         "desc":"",
         "exit":"",
         "featured":false,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/34658-a45ed4a16e8ba10eee6cfd6151a476bb-thumb_jpg.jpg",
         "investments":[  

         ],
         "link":"https://angel.co/miasole",
         "name":"Miasole",
         "record_type":"Company",
         "role":"Investor",
         "slug":"miasole",
         "title":"Investor",
         "token":"BJ7"
      },
      {  
         "company":{  
            "company_name":"Yitran",
            "high_concept":"",
            "id":45902,
            "logo_thumb_url":"https://angel.co/images/shared/nopic_startup.png",
            "quality":6.57,
            "slug_url":"https://angel.co/yitran"
         },
         "confirmed":true,
         "desc":"",
         "exit":"",
         "featured":false,
         "img":"https://angel.co/images/shared/nopic_startup.png",
         "investments":[  

         ],
         "link":"https://angel.co/yitran",
         "name":"Yitran",
         "record_type":"Company",
         "role":"Investor",
         "slug":"yitran",
         "title":"Investor",
         "token":"BJ9"
      },
      {  
         "company":{  
            "company_name":"Linkstorm",
            "high_concept":"",
            "id":35657,
            "logo_thumb_url":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/35657-bea11f434c733ccb45e1056507f45216-thumb_jpg.jpg?buster=1407426323",
            "quality":10,
            "slug_url":"https://angel.co/linkstorm"
         },
         "confirmed":true,
         "desc":"",
         "exit":"",
         "featured":false,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/35657-bea11f434c733ccb45e1056507f45216-thumb_jpg.jpg",
         "investments":[  

         ],
         "link":"https://angel.co/linkstorm",
         "name":"Linkstorm",
         "record_type":"Company",
         "role":"Investor",
         "slug":"linkstorm",
         "title":"Investor",
         "token":"BJa"
      },
      {  
         "company":{  
            "company_name":"MSG Telco",
            "high_concept":"",
            "id":802709,
            "logo_thumb_url":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/802709-9a82cf277ac0be74b237da17b9ae6a1f-thumb_jpg.jpg?buster=1465579999",
            "quality":6.75,
            "slug_url":"https://angel.co/msg-telco"
         },
         "confirmed":true,
         "desc":"",
         "exit":"",
         "featured":false,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/802709-9a82cf277ac0be74b237da17b9ae6a1f-thumb_jpg.jpg",
         "investments":[  
            {  
               "amount":0,
               "round":"Series B",
               "year":2014
            }
         ],
         "link":"https://angel.co/msg-telco",
         "name":"MSG Telco",
         "record_type":"Company",
         "role":"Investor",
         "slug":"msg-telco",
         "title":"Investor",
         "token":"fWEo"
      },
      {  
         "company":{  
            "company_name":"Javelin Pharmaceuticals",
            "high_concept":"",
            "id":45904,
            "logo_thumb_url":"https://angel.co/images/shared/nopic_startup.png",
            "quality":6.57,
            "slug_url":"https://angel.co/javelin-pharmaceuticals"
         },
         "confirmed":true,
         "desc":"",
         "exit":"Acquired for $95M",
         "featured":false,
         "img":"https://angel.co/images/shared/nopic_startup.png",
         "investments":[  

         ],
         "link":"https://angel.co/javelin-pharmaceuticals",
         "name":"Javelin Pharmaceuticals",
         "record_type":"Company",
         "role":"Investor",
         "slug":"javelin-pharmaceuticals",
         "title":"Investor",
         "token":"BJc"
      },
      {  
         "company":{  
            "company_name":"Feeny Wireless",
            "high_concept":"",
            "id":741738,
            "logo_thumb_url":"https://angel.co/images/shared/nopic_startup.png",
            "quality":6.57,
            "slug_url":"https://angel.co/feeny-wireless"
         },
         "confirmed":true,
         "desc":"",
         "exit":"Acquired by Novatel Wireless",
         "featured":false,
         "img":"https://angel.co/images/shared/nopic_startup.png",
         "investments":[  
            {  
               "amount":0,
               "round":"Series C",
               "year":2015
            }
         ],
         "link":"https://angel.co/feeny-wireless",
         "name":"Feeny Wireless",
         "record_type":"Company",
         "role":"Investor",
         "slug":"feeny-wireless",
         "title":"Investor",
         "token":"fWEq"
      },
      {  
         "company":{  
            "company_name":"Comgates",
            "high_concept":"",
            "id":45891,
            "logo_thumb_url":"https://angel.co/images/shared/nopic_startup.png",
            "quality":7.12,
            "slug_url":"https://angel.co/comgates"
         },
         "confirmed":true,
         "desc":"",
         "exit":"",
         "featured":false,
         "img":"https://angel.co/images/shared/nopic_startup.png",
         "investments":[  

         ],
         "link":"https://angel.co/comgates",
         "name":"Comgates",
         "record_type":"Company",
         "role":"Investor",
         "slug":"comgates",
         "title":"Investor",
         "token":"BJd"
      },
      {  
         "company":{  
            "company_name":"Transit Wireless",
            "high_concept":"",
            "id":45890,
            "logo_thumb_url":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/45890-70c036c0f32960ab83234c76b53276a9-thumb_jpg.jpg?buster=1326853969",
            "quality":7.12,
            "slug_url":"https://angel.co/transit-wireless"
         },
         "confirmed":true,
         "desc":"",
         "exit":"Acquired by Ontario Teachers' Pension Plan",
         "featured":false,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/45890-70c036c0f32960ab83234c76b53276a9-thumb_jpg.jpg",
         "investments":[  
            {  
               "amount":0,
               "round":"",
               "year":""
            }
         ],
         "link":"https://angel.co/transit-wireless",
         "name":"Transit Wireless",
         "record_type":"Company",
         "role":"Investor",
         "slug":"transit-wireless",
         "title":"Investor",
         "token":"BJe"
      },
      {  
         "company":{  
            "company_name":"LimoRes",
            "high_concept":"",
            "id":45897,
            "logo_thumb_url":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/45897-965cec0c553c087323f3f3441a909017-thumb_jpg.jpg?buster=1326853977",
            "quality":7.12,
            "slug_url":"https://angel.co/limores"
         },
         "confirmed":true,
         "desc":"",
         "exit":"",
         "featured":false,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/45897-965cec0c553c087323f3f3441a909017-thumb_jpg.jpg",
         "investments":[  

         ],
         "link":"https://angel.co/limores",
         "name":"LimoRes",
         "record_type":"Company",
         "role":"Investor",
         "slug":"limores",
         "title":"Investor",
         "token":"BJf"
      },
      {  
         "company":{  
            "company_name":"Entelos",
            "high_concept":"",
            "id":45905,
            "logo_thumb_url":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/45905-59b47562f8ae798d411b5ba5836ece04-thumb_jpg.jpg?buster=1408461615",
            "quality":6.57,
            "slug_url":"https://angel.co/entelos"
         },
         "confirmed":true,
         "desc":"",
         "exit":"",
         "featured":false,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/45905-59b47562f8ae798d411b5ba5836ece04-thumb_jpg.jpg",
         "investments":[  

         ],
         "link":"https://angel.co/entelos",
         "name":"Entelos",
         "record_type":"Company",
         "role":"Investor",
         "slug":"entelos",
         "title":"Investor",
         "token":"BJg"
      },
      {  
         "company":{  
            "company_name":"LionCao",
            "high_concept":"",
            "id":45907,
            "logo_thumb_url":"https://angel.co/images/shared/nopic_startup.png",
            "quality":6.57,
            "slug_url":"https://angel.co/lioncao"
         },
         "confirmed":true,
         "desc":"",
         "exit":"",
         "featured":false,
         "img":"https://angel.co/images/shared/nopic_startup.png",
         "investments":[  

         ],
         "link":"https://angel.co/lioncao",
         "name":"LionCao",
         "record_type":"Company",
         "role":"Investor",
         "slug":"lioncao",
         "title":"Investor",
         "token":"BJi"
      },
      {  
         "company":{  
            "company_name":"Survey.com",
            "high_concept":"Cost effective data collection and merchandising services.",
            "id":129622,
            "logo_thumb_url":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/129622-31305688116aef7e566391ceec82f02e-thumb_jpg.jpg?buster=1433969953",
            "quality":5.32,
            "slug_url":"https://angel.co/survey-com"
         },
         "confirmed":true,
         "desc":"Cost effective data collection and merchandising services.",
         "exit":"",
         "featured":false,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/129622-31305688116aef7e566391ceec82f02e-thumb_jpg.jpg",
         "investments":[  
            {  
               "amount":0,
               "round":"Series A",
               "year":2004
            }
         ],
         "link":"https://angel.co/survey-com",
         "name":"Survey.com",
         "record_type":"Company",
         "role":"Investor",
         "slug":"survey-com",
         "title":"Investor",
         "token":"mD7Q"
      }
   ],
   "short_desc":"CEO RTX former CEO of Novatel Wireless ($MIFI) Founder of @arbinet, @groundlink, @transit-wireless, @comgates, @elematics. Investor in 61 startups. $550m raised",
   "twitter_url":"http://twitter.com/#!/Mashinsky",
   "website_url":"http://www.governingdynamics.com",
   "angellist_url":"https://angel.co/mashinsky"
}
     var jsonobj = 
                                    {
                                      'name': name,
                                      'short_desc':short_desc,
                                      'long_desc':long_desc,
                                      'location': location,
                                      'markets': markets,
                                      'city': city,
                                      'logo_url' : logo_url,
                                      'twitter_url':twitter,
                                      'facebook_url':facebook,
                                      'linkedin_url':linkedin,
                                      'website_url': website,
                                      'blog_url':blog,
                                      'founded_companies':founded_companies,
                                      'board_companies':board_companies,
                                      'portfolios':portfolio,
                                      'education':education,
                                      'experience':experience
                                   }
    '''    
    facebook=''
    twitter=''
    linkedin=''
    website=''
    blog=''
    last_name=''
    first_name=''
    short_desc=''
    long_desc=''
    schools=''
    logo='img/profile/noimg_profile.png'
    
    name=json_obj['name']
    if re.search(' ',name):    
        name=re.sub('^[\s]*','',name)
        name=re.sub('[\s]*$','',name)
        names=name.split(' ')
        last_name=names[-1]
        first_name=' '.join(names[0:-1])
    username=name
    username=re.sub('[\W]*','',username)
    if len(username) > 20:
        username=username[0:20]
    
    username+=str(randint(1000000,9999999))
        
    if json_obj.has_key('short_desc'):
        short_desc=json_obj['short_desc'].encode('utf8')
        #stripped = lambda s: "".join(i for i in s if 31 < ord(i) < 127)
        #content=stripped(r.text)
        short_desc=re.sub('^[\s]*','',short_desc)
        short_desc=re.sub('[\s]*$','',short_desc)
        
    if json_obj.has_key('long_desc'):
        long_desc=json_obj['long_desc'].encode('utf8')
        #stripped = lambda s: "".join(i for i in s if 31 < ord(i) < 127)
        #content=stripped(r.text)
        long_desc=re.sub('^[\s]*','',long_desc)
        long_desc=re.sub('[\s]*$','',long_desc)
        
    if json_obj.has_key('twitter_url'):
        twitter=json_obj['twitter_url'].encode('utf8')
    if json_obj.has_key('facebook_url'):
        facebook=json_obj['facebook_url']
        
    if json_obj.has_key('linkedin_url'):
        linkedin=json_obj['linkedin_url']
    
    if json_obj.has_key('logo_url'):
        logo=json_obj['logo_url']
    
    if json_obj.has_key('website_url'):
        website=json_obj['website_url']
        
    if json_obj.has_key('blog_url'):
        blog=json_obj['blog_url']
        
    country=''
    city=''
    cities=json_obj['location']
    if cities and len(cities) > 0:
        city=cities[0]
    if json_obj.has_key('markets'):
        markets=json_obj['markets']
    tags=''
    prod_market_csv=''
    if markets:
        (prod_market_csv,tags)=getMarkets(markets)
    
    if json_obj.has_key('education'):
        schools=json_obj['education']
    university_csv=''
    universities=''
    main_university=''
    if schools:
        (university_csv, universities, main_university)=getSchools(schools)
        
    if twitter:
            if re.search('twitter.com/',twitter.lower()):
                res=twitter.lower().split('twitter.com/')
                twitter=res[-1]
            twitter=re.sub('@','',twitter)
            twitter=re.sub('\s','',twitter)
            twitter=re.sub('/','',twitter)
            twitter=re.sub('^[\s]*','',twitter)
            twitter=re.sub('[\s]*$','',twitter)
            
    user_list=UserDefault.objects.filter(first_name=first_name).filter(last_name=last_name)
    if user_list and len(user_list) > 0:
        user=user_list[0]
    else:
        user_account=User()
        user_account.username=username
        user_account.save()
        
        user=UserDefault()
        user.user_id=user_account.id
        user.first_name=first_name
        user.last_name=last_name
        user.is_public=True
        user.company=''
        
        print "Adding User ID",user.user_id
        user.crawl_source=crawl_source
        if not user.title and short_desc:
            user.title=short_desc
        user.profile_image=logo
        user.save()
    
        profile=UserProfile()
        profile.user_id=user.user_id
        if logo:
            profile.profile_image=logo
            profile.profile_has_image=True
        if city:
            profile.city_name=city
        if tags:
            profile.profile_top_keywords=tags
            profile.industry=tags
            profile.interest=tags
        if prod_market_csv:
            profile.invest_market_csv=prod_market_csv
        if long_desc:
            profile.profile_cv_accomplishment=long_desc
        if short_desc:
            profile.profile_cv_mini=short_desc
        if twitter:
            profile.social_twitter=twitter
        if facebook:
            profile.social_facebook=facebook
        if linkedin:
            profile.social_linkedin=linkedin
        if blog:
            profile.social_blog=blog
        if website:
            profile.website=website
        if university_csv:
            profile.university_csv=university_csv
        if main_university:
            profile.university=main_university
            print "Found Schools",universities
            
        profile.save()

    ''' 
    # var founded_companies={
                                                'name': name,
                                                'link': link,
                                                'record_type':record_type,
                                                'slug':slug,
                                            }
    var board_companies={
                                                'name': name,
                                                'link': link,
                                                'record_type':record_type,
                                                'slug':slug,
                                            }
    var portfolios={
                                                'name': name,
                                                'link': link,
                                                'record_type':record_type,
                                                'slug':slug,
                                            }
    '''
    if json_obj.has_key('founded_companies'):
        advisors=json_obj['founded_companies']
        for advisor in advisors:
            procCompany(advisor, 'Founder', user)
    
    if json_obj.has_key('board_companies'):
        advisors=json_obj['board_companies']
        for advisor in advisors:
            procCompany(advisor, 'Board Member', user)
    '''
    "experience":[  
      {  
         "date_range":"",
         "dates_for_select":{  
            "ended_at":{  
               "month":"",
               "year":""
            },
            "started_at":{  
               "month":"",
               "year":""
            }
         },
         "desc":"",
         "featured":true,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/37992-14a2e8a09b2d806b3e8ea888b3bdf963-thumb_jpg.jpg",
         "link":"https://angel.co/arbinet",
         "name":"Arbinet",
         "past":false,
         "pending_approval":false,
         "role":"Founder",
         "slug":"arbinet",
         "startup_avatar":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/37992-14a2e8a09b2d806b3e8ea888b3bdf963-thumb_jpg.jpg?buster=1326847151",
         "startup_company_name":"Arbinet",
         "startup_high_concept":"",
         "startup_id":37992,
         "startup_slug_url":"https://angel.co/arbinet",
         "title":"Founder",
         "token":"BHK",
         "who_confirms":"startup",
         "work_from":"",
         "work_to":""
      },]
      '''
    if json_obj.has_key('experience'):
        advisors=json_obj['experience']
        for advisor in advisors:
            if advisor.has_key('role'):
                procCompany(advisor, advisor['role'], user)
    '''
    "portfolios":[  
      {  
         "company":{  
            "company_name":"cVidya",
            "high_concept":"",
            "id":46045,
            "logo_thumb_url":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/46045-5898138776d1e4c43802fb0dfffc36de-thumb_jpg.jpg?buster=1408332734",
            "quality":8.24,
            "slug_url":"https://angel.co/cvidya"
         },
         "confirmed":true,
         "desc":"",
         "exit":"Acquired by Amdocs",
         "featured":false,
         "img":"https://d1qb2nb5cznatu.cloudfront.net/startups/i/46045-5898138776d1e4c43802fb0dfffc36de-thumb_jpg.jpg",
         "investments":[  
            {  
               "amount":200000,
               "round":"Series C",
               "year":2014
            }
         ],
         "link":"https://angel.co/cvidya",
         "name":"cVidya",
         "record_type":"Company",
         "role":"Investor",
         "slug":"cvidya",
         "title":"Investor",
         "token":"48j9"
      },]
    '''
    if json_obj.has_key('portfolios'):
        advisors=json_obj['portfolios']
        for advisor in advisors:
            procCompany(advisor, 'Investor', user)
                            


def procCompany(json_obj, role, user):
    if json_obj.has_key('record_type'):
            if json_obj['record_type'] == 'User':
                return
    '''
     var jsonobj ={
                                                'name': name,
                                                'link': link,
                                                'record_type':record_type,
                                                'slug':slug,
                                            }
    '''    
    company_name=json_obj['name'].encode('utf8')
    if company_name:
        company_name=re.sub('^[\s]*','',company_name)
        company_name=re.sub('[\s]*$','',company_name)
    
    if not re.search('http',company_name) and len(company_name) < 200 and len(company_name) > 5:
        companies=Company.objects.filter(company_name=company_name)
        if companies and len(companies) > 0:
            company=companies[0]
        else:
            company=Company()
            defaultuser=User.objects.get(pk=35)
            company.owner=defaultuser
            company.company_name=company_name
            company.crawl_source=crawl_source
            company.save()
        if user:
            member_list=CompanyMember.objects.filter(owner_id=company.id).filter(user_id=user.user_id)
            if member_list and len(member_list) > 0:
                member=member_list[0]
            else:
                member=CompanyMember()
                member.owner=company
                member.user_id=user.user_id
                if user.title:
                    title=user.title
                else:
                    title=role
                if json_obj.has_key('title') and json_obj['title']:
                    title=json_obj['title']
                
                member.user_title=title
                member.user_role=role
                member.user_name=user.first_name + ' ' + user.last_name
                member.crawl_source=crawl_source
                member.save()
                
                if not user.company or user.company=='':
                    user.company=company.company_name
                    user.save()

            '''
            "investments":[  
            {  
               "amount":200000,
               "round":"Series C",
               "year":2014
            }
            ],
            '''
            if json_obj.has_key('investments'):
                invest_list=json_obj['investments']
                for invest in invest_list:
                    if invest.has_key('year') and len(str(invest['year']))>  0:
                        year=int(invest['year'])
                        month=1
                        if invest.has_key('month'):
                            month=int(invest['month'])
                        round=''
                        round_size=0
                        stage=None
                        if invest.has_key('round'):
                            round=invest['round']
                            if not round:
                                round='Venture'
                                
                            if round:
                                print round
                                round=re.sub('Round:','',round)
                                round=re.sub('^[\s]*','',round)
                                round=re.sub('[\s]*$','',round)
                                stage_list=FundingStage.objects.filter(name=round)
                                if stage_list and len(stage_list) > 0:
                                    stage=stage_list[0]
                                else:
                                    stage=FundingStage()
                                    stage.name=round
                                    stage.save()
                                print "Round,",round
                                has_round=True
                        investor=getCompanyFromUser(user)
                        if investor:
                            if invest.has_key('amount'):          
                                round_size=str(invest['amount'])
                                has_size=False
                                if round_size:
                                    print round_size
                                    round_size=re.sub('Round Size:','',round_size)
                                    round_size=re.sub('^[\s]*','',round_size)
                                    round_size=re.sub('[\s]*$','',round_size)
                                    round_size=re.sub('US\$','',round_size)
                                    if re.search('M',round_size):
                                        round_size=re.sub('M','',round_size)
                                        round_size=int(float(round_size) * 1000000)
                                    elif re.search('K',round_size):
                                        round_size=re.sub('K','',round_size)
                                        round_size=int(float(round_size) * 1000)
                                    elif re.search('B',round_size):
                                        round_size=re.sub('B','',round_size)
                                        round_size=int(float(round_size) * 1000000000)
                                    else:
                                        round_size=re.sub('\D','',round_size)
                                        if round_size:
                                            round_size=int(float(round_size))
                                        else:
                                            round_size=0
                                            
                                    
                            round_date=datetime(year, month,1)
                            
                            CompanyInvestor.objects.filter(owner=company).filter(investor_year=round_date.year).filter(investor_month=round_date.month).delete()
                            CompanyInvestingEvent.objects.filter(owner=company).filter(event_year=round_date.year).filter(event_month=round_date.month).delete()

                            ci_list=CompanyInvestor.objects.filter(investor_id=investor.id).filter(owner=company).filter(investor_year=round_date.year).filter(investor_month=round_date.month)
                            if ci_list and len(ci_list)>0:
                               ci=ci_list[0]
                               print "CompanyInvestor Found", ci.id
                            else:
                                ci=CompanyInvestor()
                                ci.investor_currency='USD'
                                ci.investor_amount=round_size
                                ci.investor_day=1
                                ci.investor_month=round_date.month
                                ci.investor_year=round_date.year
                                ci.created_time= round_date
                                ci.last_edited_time=round_date
                                ci.is_user_input=False
                                ci.investor_id=investor.id
                                ci.owner=company
                                ci.funding_stage=stage
                                ci.is_active=True
                                ci.is_tips=False
                                ci.crawl_source=crawl_source
                                ci.is_estimate=True
                                updateInvestor(ci,stage.id)
                                ci.save()
                                print "CompanyInvestor", ci.id
        
                            
                        event_list=CompanyInvestingEvent.objects.filter(owner=company).filter(event_round=stage.name).filter(event_year=round_date.year).filter(event_month=round_date.month)
                        if event_list and len(event_list) > 0:
                            event=event_list[0]
                            event.investor=CompanyInvestor.objects.filter(owner=company).filter(investor_year=round_date.year).filter(investor_month=round_date.month)
                            event.save()
                            print "Event Found", event.id
                        else:
                            event=CompanyInvestingEvent()
                            event.event_round=stage.name
                            event.funding_stage=stage
                            event.event_currency='USD'
                            event.event_amount=round_size
                            event.event_day=1
                            event.event_month=round_date.month
                            event.event_year=round_date.year
                            event.created_time= round_date
                            event.last_edited_time=round_date
                            event.is_user_input=False
                            event.owner=company
                            event.is_tips=False
                            event.save()
                            event.investor=CompanyInvestor.objects.filter(owner=company).filter(investor_year=round_date.year).filter(investor_month=round_date.month)
                            event.crawl_source=crawl_source
                            updateInvestorEvent(event, stage)
                            event.save()
                            print "Event Found", event.id
                    
                    
                    
def getCompanyFromUser(user):
    company=None
    company_name=user.first_name + ' ' + user.last_name
    companies=Company.objects.filter(company_name=company_name)
    if companies and len(companies) > 0:
        company=companies[0]
        return company
    else:
        company=Company()
        company.owner_id=user.user_id
        company.company_name=company_name
        profiles=UserProfile.objects.filter(user_id=user.user_id)
        if profiles and len(profiles) > 0:
            profile=profiles[0]
            company.company_top_keywords=profile.profile_top_keywords
            company.company_industry=profile.industry
            company.company_logo=profile.profile_image
            company.company_city=profile.city_name
            company.company_country=profile.country_name
            company.company_website=profile.website
            company.company_long=profile.profile_cv_accomplishment
            company.company_short=profile.profile_cv_mini
            company.company_twitter=profile.social_twitter
            company.company_facebook_page=profile.social_facebook
            company.company_linkedin_page=profile.social_linkedin
            company.product_market_csv=profile.invest_market_csv
            company.company_class='Investor'
            company.is_angel=True
            company.crawl_source=crawl_source
            company.save()
    print "Created Company ",company.company_name," with ID ",company.id
    return company
        
def getCorrectRoundName(name):
    if name:
        name=re.sub('Unknown','',name)
        name=re.sub('^[\s]*','',name)
        name=re.sub('[\s]*$','',name)
    if name == 'SeriesA':
        #print 'SeriesA'
        return 'Series A'
        
    elif name == 'Series Pre-A':
        #print 'Series Pre-A'
        return 'Pre Series A'
    elif re.search('A',name):
        return 'Series A'
    elif re.search('B',name):
        return 'Series B'
    elif re.search('C',name):
        return 'Series C'
    elif re.search('D',name):
        return 'Series D'
    elif re.search('Seed',name):
        return 'Seed'
    elif re.search('M &amp; A',name):
        return 'Acquired'
    elif re.search('IPO',name):
        return 'IPO'
    elif re.search('Investment',name):
        return 'Venture'
    elif re.search('Angel',name):
        return 'Angel'
    
    elif name == 'Fund':
        print 'Fund'
        return 'Fund'
    elif name == 'Series A - Early':
        #print 'Series A - Early'
        return 'Series A'
        
    elif name == 'Post-IPO Equity':
        #print 'Post-IPO Equity'
        return 'Post-IPO Equity'
    elif name == 'Private Equity':
        #print 'Private Equity'
        return 'Private Equity'
    elif name == 'Round A':
        #print 'Round A'
        return 'Series A'
        
    elif name == 'Loan':
        #print 'Loan'
        return 'Debt Financing'
        
    elif name == 'Venture':
        #print 'Venture'
        return 'Venture'
    elif name == 'Seris B' or name in [
            "Series B",
            "Series  B",
            "Series B"]:
        #print 'Series B'
        return 'Series B'
        
    elif name == 'Aqcuired':
        #print 'Aqcuired'
        return 'Acquired'
    elif name and re.search('Acquired',name):
        #print 'Acquired'
        return 'Acquired'
    elif name and re.search('Exited',name):
        #print 'Acquired'
        return 'Exited'
    elif name and re.search('Amgel',name):
        #print 'Acquired'
        return 'Angel'
    elif not name:
        #print 'Venture'
        return 'Venture'
    else:
        #print name
        return name    
    