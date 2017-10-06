from django.db import models
#from custom_user.models import EmailUser
from django.contrib.auth.models import User
from datetime import *
from django.template.defaultfilters import slugify
from django.contrib.humanize.templatetags.humanize import *
from autoslug import AutoSlugField

from django.utils.safestring import mark_safe
from dateutil.relativedelta import relativedelta
import dateutil.parser
import pytz
import os
import re
import uuid
import operator
from pytz import timezone
mytz = pytz.timezone('US/Eastern')

NAME_MAX_LENGTH = 500
COUNTRY_CITY_MAX_LENGTH = 300
PHONE_MAX_LENGTH = 11
GENDER_MAX_LENGTH = 1
MALE = 'M'
FEMALE = 'F'
GENDER_CHOICES = (
    (MALE, 'Male'),
    (FEMALE, 'Female'),
)
UNIVERSITY_MAX_LENGTH = 100
MAJOR_MAX_LENGTH = 300
SPECIALITY_MAX_LENGTH = 200
INTEREST_MAX_LENGTH = 200
INDUSTRY_MAX_LENGTH = 200
FAVORITE_COMPANY_MAX_LENGTH = 200

COMPANY_NAME_MAX_LENGTH = 1000
COMPANY_SHORT_MAX_LENGTH = 500
COMPANY_LONG_MAX_LENGTH = 1000
COMPANY_EMPLOYEE_MAX_LENGTH = 20
COMPANY_CLASS_MAX_LENGTH = 1000
COMPANY_FUNDED_MAX_LENGTH = 300

PRODUCT_NAME_MAX_LENGTH = 500
PRODUCT_CLASS_MAX_LENGTH = 100
PRODUCT_STAGE_MAX_LENGTH = 1000
PRODUCT_MARKET_MAX_LENGTH = 1000

PROGRAM_NAME_MAX_LENGTH = 100

DESCRIPTION_MAX_LENGTH = 200
SHORT_DESCRIPTION_MAX_LENGTH = 2000
LONG_DESCRIPTION_MAX_LENGTH = 10000


    
class Market(models.Model):
    name = models.CharField(max_length=255, null=True, db_index=True)
    vertical = models.CharField(max_length=255, null=True, db_index=True)
    sub_vertical = models.CharField(max_length=255, null=True, db_index=True)
    total = models.IntegerField(default=1)
    slug = AutoSlugField(populate_from='name', unique=True,
                         null=True, blank=True, always_update=True)
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, db_index=True)
    updated_at = models.DateTimeField(
        auto_now_add=True, null=True, db_index=True)
    crawl_source=models.CharField(max_length=200, default='', blank=True, null=True)

    def __unicode__(self):
        return '%s' % self.name

    def save(self, *args, **kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        super(Market, self).save(*args, **kwargs)
        
class FundingStage(models.Model):
    name = models.CharField(
        max_length=PRODUCT_NAME_MAX_LENGTH, blank=True, db_index=True)
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, db_index=True)
    updated_at = models.DateTimeField(
        auto_now_add=True, null=True, db_index=True)
    count = models.IntegerField(default=0, null=True, blank=True)
    stage_step=models.IntegerField(default=0, null=True, blank=True)
    
    crawl_source=models.CharField(max_length=200, default='', blank=True, null=True)

    def __unicode__(self):
        return '%s' % self.name

    def save(self, *args, **kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        super(FundingStage, self).save(*args, **kwargs)


class InvestorType(models.Model):
    name = models.CharField(max_length=PRODUCT_NAME_MAX_LENGTH, blank=True)
    slug = AutoSlugField(populate_from='name', unique=True,
                         null=True, blank=True, always_update=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return '%s' % self.name

    def save(self, *args, **kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        super(InvestorType, self).save(*args, **kwargs)


class Region(models.Model):
    is_save = models.BooleanField(default=True)
    is_confirm = models.BooleanField(default=True)

    last_edited_time = models.DateTimeField(
        auto_now=True, db_index=True)
    created_time = models.DateTimeField(
        auto_now_add=True, db_index=True)

    name = models.CharField(max_length=500, blank=True, db_index=True)
    latitude=models.IntegerField(default=0, db_index=True)
    longitude= models.IntegerField(default=0, db_index=True)
    
    crawl_source=models.CharField(max_length=200, default='', blank=True, null=True)


class Continent(models.Model):
    is_save = models.BooleanField(default=True)
    is_confirm = models.BooleanField(default=True)

    last_edited_time = models.DateTimeField(
        auto_now=True, db_index=True)
    created_time = models.DateTimeField(
        auto_now_add=True, db_index=True)

    name = models.CharField(max_length=500, blank=True, db_index=True)
    latitude=models.IntegerField(default=0, db_index=True)
    longitude= models.IntegerField(default=0, db_index=True)
    
    crawl_source=models.CharField(max_length=200, default='', blank=True, null=True)
    company_count= models.IntegerField(default=0, db_index=True)
    company_investor_count= models.IntegerField(default=0, db_index=True)
    company_startup_count= models.IntegerField(default=0, db_index=True)
    company_public_count= models.IntegerField(default=0, db_index=True)
    
    user_count= models.IntegerField(default=0, db_index=True)


class Country(models.Model):
    is_save = models.BooleanField(default=True)
    is_confirm = models.BooleanField(default=True)

    last_edited_time = models.DateTimeField(
        auto_now=True, db_index=True)
    created_time = models.DateTimeField(
        auto_now_add=True, db_index=True)
    
    continent=models.ForeignKey(Continent, db_index=True)
    
    name = models.CharField(max_length=500, blank=True, db_index=True)
    latitude=models.IntegerField(default=0, db_index=True)
    longitude= models.IntegerField(default=0, db_index=True)
    
    company_count= models.IntegerField(default=0, db_index=True)
    company_investor_count= models.IntegerField(default=0, db_index=True)
    company_startup_count= models.IntegerField(default=0, db_index=True)
    company_public_count= models.IntegerField(default=0, db_index=True)
    user_count= models.IntegerField(default=0, db_index=True)
    
    def __unicode__(self):
        return str(self.name)

    
class State(models.Model):
    is_save = models.BooleanField(default=True)
    is_confirm = models.BooleanField(default=True)

    last_edited_time = models.DateTimeField(
        auto_now=True, db_index=True)
    created_time = models.DateTimeField(
        auto_now_add=True, db_index=True)

    continent=models.ForeignKey(Continent, db_index=True)
    country=models.ForeignKey(Country, db_index=True)
    
    name = models.CharField(max_length=500, blank=True, db_index=True)
    latitude=models.IntegerField(default=0, db_index=True)
    longitude= models.IntegerField(default=0, db_index=True)


class City(models.Model):
    is_save = models.BooleanField(default=True)
    is_confirm = models.BooleanField(default=True)

    last_edited_time = models.DateTimeField(
        auto_now=True, db_index=True)
    created_time = models.DateTimeField(
        auto_now_add=True, db_index=True)

    continent=models.ForeignKey(Continent, db_index=True)
    country=models.ForeignKey(Country, db_index=True)
    state=models.ForeignKey(State, null=True, db_index=True)
    
    name = models.CharField(max_length=500, blank=True, db_index=True)
    latitude=models.IntegerField(default=0, db_index=True)
    longitude= models.IntegerField(default=0, db_index=True)

class Company(models.Model):

    default_last_funding_date = datetime.strptime('2000-01-01', "%Y-%m-%d")

    
    is_private_company_all = models.BooleanField(default=False)
    is_private_company_class = models.BooleanField(default=False)
    is_private_investor_class = models.BooleanField(default=False)
    is_private_company_short = models.BooleanField(default=False)
    is_private_company_long = models.BooleanField(default=False)
    is_private_company_industry = models.BooleanField(default=False)
    is_private_company_country = models.BooleanField(default=False)
    is_private_company_city = models.BooleanField(default=False)
    is_private_company_state = models.BooleanField(default=False)
    is_private_company_region = models.BooleanField(default=False)
    is_private_company_employee = models.BooleanField(default=False)
    is_private_corporation = models.BooleanField(default=False)
    is_private_company_established = models.BooleanField(default=False)
    is_private_company_founded_year = models.BooleanField(default=False)
    is_private_patent = models.BooleanField(default=False)
    is_private_team = models.BooleanField(default=False)
    is_private_company_fundraising = models.BooleanField(default=False)
    is_private_company_logo = models.BooleanField(default=False)
    is_private_company_website = models.BooleanField(default=False)
    is_private_company_founded_day = models.BooleanField(default=False)
    is_private_company_founded_month = models.BooleanField(default=False)
    is_private_company_name = models.BooleanField(default=False)

    
    owner = models.ForeignKey(User, db_index=True)
    company_favorite_count = models.IntegerField(default=0)
    company_recommendation_count = models.IntegerField(default=0)
    
    
    is_active = models.BooleanField(default=True, db_index=True)
    is_public = models.BooleanField(default=False, db_index=True)
    is_save = models.BooleanField(default=False)
    is_confirm = models.BooleanField(default=False, db_index=True)


    is_trusted_vc = models.BooleanField(default=False, db_index=True)
    is_partner = models.BooleanField(default=False, db_index=True)
    is_angel = models.BooleanField(default=False, db_index=True)

    
    is_government = models.BooleanField(default=False)
    is_tips = models.BooleanField(default=False, db_index=True)
    is_dcamp = models.BooleanField(default=False, db_index=True)
    is_rocketpunch = models.BooleanField(default=False, db_index=True)
    is_dart = models.BooleanField(default=False, db_index=True)
    is_bizinkorea = models.BooleanField(default=False, db_index=True)
    is_startup = models.BooleanField(default=True, db_index=True)
    is_investor = models.BooleanField(default=False, db_index=True)
    
    
    ticker = models.CharField(
        max_length=100, blank=True, db_index=True, null=True)
    exchange=models.CharField(
        max_length=100, blank=True, db_index=True, null=True)
    sec_cik=models.CharField(
        max_length=100, blank=True, db_index=True, null=True)
    sec_cik_int=models.CharField(
        max_length=100, blank=True, db_index=True, null=True)
    partner_order = models.IntegerField(default=0)

    last_edited_time = models.DateTimeField(
        'date edited', auto_now=True, db_index=True)
    created_time = models.DateTimeField(
        auto_now_add=True, null=True, db_index=True)
    
    company_name = models.CharField(
        max_length=COMPANY_NAME_MAX_LENGTH, blank=True, db_index=True)
    company_kor_name = models.CharField(
        max_length=COMPANY_NAME_MAX_LENGTH, blank=True, null=True, db_index=True)

    company_class = models.CharField(
        max_length=15, default='Public', db_index=True)
    tips_start_date = models.DateField(null=True, blank=True)
    rocketpunch_url = models.CharField(max_length=1001, blank=True, null=True, db_index=True)
    angellist_url=models.CharField(max_length=702, blank=True, null=True, db_index=True)
    sec_url=models.CharField(max_length=701, blank=True, null=True, db_index=True)
    e27_url=models.CharField(max_length=700, blank=True, null=True, db_index=True)
    f6s_url=models.CharField(max_length=703, blank=True, null=True, db_index=True)
    forbes_url=models.CharField(max_length=707, blank=True, null=True, db_index=True)

    
    investor_class = models.CharField(
        max_length=COMPANY_CLASS_MAX_LENGTH, blank=True, db_index=True)

    company_short = models.CharField(
        max_length=10001, blank=True)

    company_long = models.TextField(blank=True, max_length=10002)

    company_industry = models.CharField(
        max_length=5002, blank=True, db_index=True)

    company_continent = models.CharField(
        max_length=COUNTRY_CITY_MAX_LENGTH, blank=True, db_index=True, null=True)
    continent = models.ForeignKey(Continent, null=True, db_index=True)

    company_country = models.CharField(
        max_length=COUNTRY_CITY_MAX_LENGTH, blank=True, db_index=True)
    country = models.ForeignKey(Country, null=True, db_index=True)

    company_city = models.CharField(
        max_length=COUNTRY_CITY_MAX_LENGTH, blank=True, db_index=True)
    city = models.ForeignKey(City, null=True, db_index=True)
    
    company_state = models.CharField(
        max_length=COUNTRY_CITY_MAX_LENGTH, blank=True, db_index=True, null=True)
    state = models.ForeignKey(State, null=True, db_index=True)

    company_region = models.CharField(
        max_length=COUNTRY_CITY_MAX_LENGTH, blank=True, db_index=True, null=True)
    region = models.ForeignKey(Region, null=True, db_index=True)

    company_location = models.CharField(
        max_length=1003, blank=True, db_index=True, null=True)
    company_location_latitude=models.IntegerField(default=0, db_index=True)
    company_location_longitude= models.IntegerField(default=0, db_index=True)

    # company_region_class = models.ManyToManyField(Region, blank=True, null=True)

    company_employee = models.CharField(
        max_length=COMPANY_EMPLOYEE_MAX_LENGTH, blank=True)

    corporation = models.CharField(max_length=10, blank=True)

    company_established = models.CharField(
        max_length=30, default='1000-01-01', null=True, blank=True, db_index=True)

    company_founded_year = models.IntegerField(
        default=2006, blank=True, null=True, db_index=True)

    company_founded_month = models.IntegerField(
        default=1, blank=True, null=True, db_index=True)

    company_founded_day = models.IntegerField(
        default=1, blank=True,null=True, db_index=True)

    company_website = models.CharField(blank=True, max_length=1007, db_index=True)

    company_logo = models.ImageField(
        max_length=1008, upload_to='img/company', blank=True, default="img/company/noimg.png")

    company_fundraising = models.CharField(
        max_length=COMPANY_FUNDED_MAX_LENGTH, blank=True)
    company_fundraising_currency = models.CharField(
        max_length=COMPANY_FUNDED_MAX_LENGTH, blank=True, null=True)
    company_fundraising_highlight = models.CharField(
        max_length=COMPANY_FUNDED_MAX_LENGTH, blank=True, null=True)
    company_fundraising_deck = models.CharField(blank=True, max_length=1009, null=True)

    company_number = models.CharField(
        max_length=210, blank=True, null=True, db_index=True)
    corporate_number = models.CharField(
        max_length=211, blank=True, null=True, db_index=True)

    employee_total = models.IntegerField(default=0, blank=True)
    employee_total_month_ago = models.IntegerField(default=0, blank=True)
    employee_added_this_month = models.IntegerField(default=0, blank=True)
    employee_growth_month = models.IntegerField(default=0, blank=True)
    employee_total_6month_ago = models.IntegerField(default=0, blank=True)
    employee_added_in_6month = models.IntegerField(default=0, blank=True)
    employee_growth_6month = models.IntegerField(default=0, blank=True)

    employee_added_since_funding = models.IntegerField(default=0, blank=True)
    employee_months_since_funding = models.IntegerField(default=0, blank=True)
    employee_growth_since_funding = models.IntegerField(default=0, blank=True)

    investor_list_csv = models.CharField(max_length=5012, blank=True, null=True, db_index=True)
    product_list_csv = models.CharField(max_length=5013, blank=True, null=True)
    product_market_csv = models.CharField(max_length=5014, blank=True, db_index=True, null=True)
    invested_funding_stage_csv = models.CharField(max_length=5015, blank=True, null=True, db_index=True)

    traffic_growth_month = models.IntegerField(default=0, blank=True)
    last_funding_amt = models.FloatField(default=0, blank=True, db_index=True)
    last_funding_date = models.DateTimeField(null=True, default=default_last_funding_date, db_index=True)
    last_funding_months_ago = models.IntegerField(default=0, blank=True)
    total_funding_amt = models.FloatField(default=0, blank=True, db_index=True)

    funding_stage = models.ForeignKey(FundingStage, null=True, db_index=True)
    funding_stage_name = models.CharField(
        max_length=116, blank=True, null=True)

    product_app_store = models.CharField(max_length=217, blank=True, null=True)
    product_google_play = models.CharField(
        max_length=218, blank=True, null=True)

    company_top_keywords = models.CharField(default='', null=True, max_length=5019)
    company_interests = models.CharField(max_length=5020, blank=True, null=True)
    company_alerts = models.CharField(max_length=221, blank=True, null=True)

    traffic_monthly_unique = models.IntegerField(default=0, blank=True)
    traffic_monthly_unique_week_ago = models.IntegerField(
        default=0, blank=True)
    traffic_monthly_weekly_growth = models.IntegerField(default=0, blank=True)
    traffic_monthly_unique_month_ago = models.IntegerField(
        default=0, blank=True)
    traffic_monthly_monthly_growth = models.IntegerField(default=0, blank=True)
    traffic_mobile_download = models.IntegerField(default=0, blank=True)
    traffic_mobile_download_week_ago = models.IntegerField(
        default=0, blank=True)
    traffic_mobile_download_weekly_growth = models.IntegerField(
        default=0, blank=True)
    traffic_mobile_download_month_ago = models.IntegerField(
        default=0, blank=True)
    traffic_mobile_download_monthly_growth = models.IntegerField(
        default=0, blank=True)

    revenue = models.FloatField(default=0, blank=True)
    total_valuation = models.FloatField(default=0, blank=True, db_index=True)
    total_asset = models.FloatField(default=0, blank=True, db_index=True)
    total_debt = models.FloatField(default=0, blank=True, db_index=True)
    total_capital = models.FloatField(default=0, blank=True, db_index=True)
    total_sales = models.FloatField(default=0, blank=True, db_index=True)
    net_income = models.FloatField(default=0, blank=True)
    operating_income = models.FloatField(default=0, blank=True)
    ratio_sales_net = models.FloatField(default=0, blank=True)
    ratio_sales_operating = models.FloatField(default=0, blank=True)
    period_end_date=models.DateTimeField(null=True, db_index=True)
    
    investor_type = models.ForeignKey(InvestorType, null=True, blank=True)
    investor_fund_sold_3yr = models.IntegerField(default=0, blank=True)
    investor_last_funding_date = models.DateTimeField(null=True)
    investor_portfolio_size = models.IntegerField(default=0, blank=True)
    investor_total_deals = models.IntegerField(default=0, blank=True)

    score1 = models.FloatField(default=0, blank=True, db_index=True)
    score2 = models.FloatField(default=0, blank=True, db_index=True)
    score3 = models.FloatField(default=0, blank=True, db_index=True)
    score4 = models.FloatField(default=0, blank=True, db_index=True)
    score5 = models.FloatField(default=0, blank=True, db_index=True)

    company_linkedin_page = models.CharField(max_length=1017, default='', blank=True, null=True)
    company_facebook_page = models.CharField(max_length=1018, default='', blank=True, null=True)
    company_twitter = models.CharField(max_length=1019, default='', blank=True, null=True)
    
    crawl_source=models.CharField(max_length=200, default='', blank=True, null=True)
    slug = AutoSlugField(populate_from='id',
                         unique=True, null=True, blank=True, always_update=True)

    invested_stages = models.ForeignKey(FundingStage, null=True, related_name='company_invested_stages', db_index=True)
    invested_stages_csv = models.CharField(max_length=5013, blank=True, null=True, db_index=True)
    invested_success = models.IntegerField(default=-1, blank=True, db_index=True)
    invested_success_amt=models.FloatField(default=-1, blank=True, db_index=True)
    invested_founder_csv= models.CharField(max_length=5014, blank=True, null=True, db_index=True)
    invested_market_csv= models.CharField(max_length=5015, blank=True, null=True, db_index=True)
    invested_continent_csv= models.CharField(max_length=5016, blank=True, null=True, db_index=True)
    
    
    def __unicode__(self):
        return self.company_name

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse_lazy
        if self.slug:
            return reverse_lazy('view_company_name',
                                args=[self.slug])
        return reverse_lazy('view_company',
                            args=[self.pk])

    def company_name_as_url(self):
        company_name = unicode(self.company_name).encode('ascii', 'ignore')
        company_url = str(company_name).replace('-', '--')
        company_url = company_url.replace("'", "-c-")
        company_url = company_url.replace(' ', '-')
        return company_url

    def market_as_list(self):
        return self.company_industry.split(',')

    def market_as_list_new(self):
        return self.company_industry.split(',')

    def total_funding(self):
        return "$%s" % intcomma(int(self.total_funding_amt))

    def create_date_formatted(self):
        create_date = self.created_time
        if create_date != None:
            create_date = create_date.strftime('%Y-%m-%d')
        else:
            # create_date = ''
            create_date = "2000-01-01"
        return create_date

    def last_funding(self):
        last_funding_date = self.last_funding_date
        if last_funding_date != None:
            # last_funding_date = last_funding_date.strftime('%Y-%m-%d')
            last_funding_date = last_funding_date.strftime('%Y-%m-%d')
        else:
            # last_funding_date = ''
            last_funding_date = "2000-01-01"
        # return [last_funding_date, "$%s" % intcomma(int(self.last_funding_amt))]
        return [last_funding_date, int(self.last_funding_amt)]

    def employee_count(self):
        return self.employee_total

    def get_employee_month_ago(self):
        return self.employee_total_month_ago

    def get_employee_added_this_month(self):
        return self.employee_added_this_month

    def get_list_investors(self):
        company_investors = CompanyInvestor.objects.filter(owner=self).values_list(
            'investor__company_name', flat=True).distinct('investor__company_name')

        return company_investors

    def get_dict_investors_from_csv(self):
        investor_dict = dict()

        if self.investor_list_csv:
            if len(self.investor_list_csv) > 0:
                # print self.investor_list_csv
                company_investors = self.investor_list_csv.split(';')
                for investor in company_investors:
                    if len(investor) > 1:
                        names= investor.split('|')
                        investor_id=names[0]
                        investor_name=names[1] 
                        investor_dict[investor_id] = investor_name

        return investor_dict

    def get_dict_industries_from_csv(self):
        market_dict = dict()

        if self.product_market_csv:
            if len(self.product_market_csv) > 0:
                # print self.product_market_csv
                company_markets = self.product_market_csv.split(';')
                for market in company_markets:
                    if len(market) > 1 and re.search('|',market):
                        (market_id, market_name) = market.split('|')
                        market_dict[market_id] = market_name

        return market_dict

    def get_dict_products_from_csv(self):
        product_dict = dict()

        if self.product_list_csv:
            if len(self.product_list_csv) > 0:
                # print self.product_list_csv
                product_lists = self.product_list_csv.split(';')
                for product in product_lists:
                    if len(product) > 1:
                        (product_id, product_name) = product.split('|')
                        product_dict[product_id] = product_name

        return product_dict

    def get_list_industries_from_csv(self):
        industries = []
        if len(self.company_industry) > 0:
            industries = self.company_industry.split(', ')
        return industries

    def get_employee_six_month_ago(self):
        return self.employee_total_6month_ago

    def get_employee_added_six_month_ago(self):
        return self.employee_added_in_6month

    def get_financial_status(self):

        try:
            result = FinancialStatus.objects.filter(company=self).exclude(
                updated_year=0, updated_month=0, updated_week=0).order_by('-updated_year', '-last_edited_time')
        except Exception, e:
            return [0, 0, 0, 0, 0, 0, 0, 0]
        else:

            if result.count() == 0:
                return [0, 0, 0, 0, 0, 0, 0, 0]
            else:
                return [result[0].total_asset, result[0].total_debt, result[0].total_capital, result[0].total_sales, result[0].net_income, result[0].operating_income, result[0].ratio_sales_net, result[0].ratio_sales_operating]


class CompanyInvestor(models.Model):
    owner = models.ForeignKey(Company, db_index=True)
    investor = models.ForeignKey(Company, related_name='+', db_index=True)

    last_edited_time = models.DateTimeField(
        'date edited', auto_now=True, db_index=True)
    created_time = models.DateTimeField(
        auto_now_add=True, null=True, db_index=True)

    is_user_input = models.BooleanField(default=False, db_index=True)

    funding_stage = models.ForeignKey(FundingStage, null=True, db_index=True)

    # null
    investor_day = models.IntegerField(
        default=0, blank=True, null=True, db_index=True)
    investor_month = models.IntegerField(
        default=0, blank=True, null=True, db_index=True)
    investor_year = models.IntegerField(
        default=0, blank=True, null=True, db_index=True)
    investor_currency = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    investor_amount = models.CharField(max_length=200, blank=True, null=True, db_index=True)
    
    # cleaned
    invest_currency = models.CharField(max_length=3, blank=True, null=True, db_index=True)
    invest_amt = models.FloatField(default=0, db_index=True)
    invest_date=models.DateTimeField(null=True, db_index=True)
    
    is_active = models.BooleanField(default=True, db_index=True)
    is_tips = models.BooleanField(default=False, db_index=True)
    is_rocketpunch = models.BooleanField(default=False, db_index=True)
    is_estimate=models.BooleanField(default=False, db_index=True)
    crawl_source=models.CharField(max_length=200, default='', blank=True, null=True)
    
    def __repr__(self):
        try:
            #return '{ "date":"%s", "open":%s, "high":%s, "low":%s, "close":%s,"volume":%s }' % (self.date, self.open, self.high, self.low, self.close, self.volume)
            return '{ "date":"%s", "company":%s, "investor":%s, "funding_stage":%s, "invest_date":%s, "invest_currency":%s, "invest_amt":%s }' % \
                (self.created_time, self.owner, self.investor, self.funding_stage,  self.invest_date, self.invest_currency, self.invest_amt)
        except Exception as e:
            print e
        return ''
    
    def __str__(self):
        return self.__repr__()
    
    def __unicode__(self):
        return self.__repr__()



class CompanyInvestingEvent(models.Model):
    owner = models.ForeignKey(Company, null=True)
    investor = models.ManyToManyField(CompanyInvestor)

    funding_stage = models.ForeignKey(FundingStage, null=True, db_index=True)

    event_round = models.CharField(
        max_length=300, blank=True, null=True, db_index=True)
    event_investors = models.CharField(max_length=500, blank=True, null=True)
    event_investors_id = models.CharField(
        max_length=500, blank=True, null=True)

    last_edited_time = models.DateTimeField(
        'date edited', auto_now=True, db_index=True)
    created_time = models.DateTimeField(auto_now_add=True, db_index=True)

    is_user_input = models.BooleanField(default=False)
    is_tips = models.BooleanField(default=False, db_index=True)
    is_rocketpunch = models.BooleanField(default=False, db_index=True)

    event_day = models.IntegerField(
        default=0, blank=True, null=True, db_index=True)
    event_month = models.IntegerField(
        default=0, blank=True, null=True, db_index=True)
    event_year = models.IntegerField(
        default=0, blank=True, null=True, db_index=True)
    event_currency = models.CharField(max_length=100, blank=True, null=True)
    event_amount = models.CharField(max_length=200, blank=True, null=True)
    
    # cleaned
    invest_currency = models.CharField(max_length=3, blank=True, null=True, db_index=True)
    invest_amt = models.FloatField(default=0, db_index=True)
    invest_date=models.DateTimeField(null=True, db_index=True)
    
    crawl_source=models.CharField(max_length=200, default='', blank=True, null=True)
    
    def __repr__(self):
        try:
            #return '{ "date":"%s", "open":%s, "high":%s, "low":%s, "close":%s,"volume":%s }' % (self.date, self.open, self.high, self.low, self.close, self.volume)
            return '{ "date":"%s", "company":%s, "investor":%s, "funding_stage":%s, "invest_date":%s, "invest_currency":%s, "invest_amt":%s }' % \
                (self.created_time, self.owner,  self.investor,  self.funding_stage,  self.invest_date, self.invest_currency, self.invest_amt)
        except Exception as e:
            print e
        return ''
    
    def __str__(self):
        return self.__repr__()
    
    def __unicode__(self):
        return self.__repr__()
    
class Resource(models.Model):

    default_last_funding_date = datetime.strptime('2000-01-01', "%Y-%m-%d")

    owner = models.ForeignKey(User, db_index=True, null=True)
    company_favorite_count = models.IntegerField(default=0)
    company_recommendation_count = models.IntegerField(default=0)
    
    resource_type=models.CharField(max_length=50,default='Energy', blank=True, db_index=True)
    commodity_type=models.CharField(max_length=50,default='oil', blank=True, db_index=True)

    is_active = models.BooleanField(default=True, db_index=True)
    is_commodity = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False, db_index=True)
    is_save = models.BooleanField(default=False)
    is_confirm = models.BooleanField(default=False, db_index=True)

    is_trusted_vc = models.BooleanField(default=False, db_index=True)
    is_partner = models.BooleanField(default=False, db_index=True)
    is_angel = models.BooleanField(default=False, db_index=True)
    
    is_government = models.BooleanField(default=False)
    is_tips = models.BooleanField(default=False, db_index=True)
    is_rocketpunch = models.BooleanField(default=False, db_index=True)
    is_startup = models.BooleanField(default=True, db_index=True)
    is_investor = models.BooleanField(default=False, db_index=True)
    
    
    ticker = models.CharField(
        max_length=100, blank=True, db_index=True, null=True)
    exchange = models.CharField(
        max_length=100, blank=True, db_index=True, null=True)
    sec_cik=models.CharField(
        max_length=100, blank=True, db_index=True, null=True)
    sec_cik_int=models.CharField(
        max_length=100, blank=True, db_index=True, null=True)
    partner_order = models.IntegerField(default=0)



    last_edited_time = models.DateTimeField(
        'resource date edited', auto_now=True, db_index=True)
    created_time = models.DateTimeField(
        auto_now_add=True, null=True, db_index=True)
    
    company_name = models.CharField(
        max_length=COMPANY_NAME_MAX_LENGTH, blank=True, db_index=True)
    company_kor_name = models.CharField(
        max_length=COMPANY_NAME_MAX_LENGTH, blank=True, null=True, db_index=True)

    company_class = models.CharField(
        max_length=15, default='Public', db_index=True)
    tips_start_date = models.DateField(null=True, blank=True)
    rocketpunch_url = models.CharField(max_length=1001, blank=True, null=True, db_index=True)
    angellist_url=models.CharField(max_length=702, blank=True, null=True, db_index=True)
    sec_url=models.CharField(max_length=701, blank=True, null=True, db_index=True)
    e27_url=models.CharField(max_length=700, blank=True, null=True, db_index=True)
    f6s_url=models.CharField(max_length=703, blank=True, null=True, db_index=True)
    forbes_url=models.CharField(max_length=707, blank=True, null=True, db_index=True)

    
    investor_class = models.CharField(
        max_length=COMPANY_CLASS_MAX_LENGTH, blank=True, db_index=True)

    company_short = models.CharField(
        max_length=10001, blank=True)

    company_long = models.TextField(blank=True, max_length=10002)

    company_industry = models.CharField(
        max_length=5002, blank=True, db_index=True)

    company_continent = models.CharField(
        max_length=COUNTRY_CITY_MAX_LENGTH, blank=True, db_index=True, null=True)
    continent = models.ForeignKey(Continent, null=True, db_index=True)

    company_country = models.CharField(
        max_length=COUNTRY_CITY_MAX_LENGTH, blank=True, db_index=True)
    country = models.ForeignKey(Country, null=True, db_index=True)

    company_city = models.CharField(
        max_length=COUNTRY_CITY_MAX_LENGTH, blank=True, db_index=True)
    city = models.ForeignKey(City, null=True, db_index=True)
    
    company_state = models.CharField(
        max_length=COUNTRY_CITY_MAX_LENGTH, blank=True, db_index=True, null=True)
    state = models.ForeignKey(State, null=True, db_index=True)

    company_region = models.CharField(
        max_length=COUNTRY_CITY_MAX_LENGTH, blank=True, db_index=True, null=True)
    region = models.ForeignKey(Region, null=True, db_index=True)

    company_location = models.CharField(
        max_length=1003, blank=True, db_index=True, null=True)
    company_location_latitude=models.IntegerField(default=0, db_index=True)
    company_location_longitude= models.IntegerField(default=0, db_index=True)

    

    company_employee = models.CharField(
        max_length=COMPANY_EMPLOYEE_MAX_LENGTH, blank=True)

    corporation = models.CharField(max_length=10, blank=True)

    company_established = models.CharField(
        max_length=30, default='1000-01-01', null=True, blank=True, db_index=True)

    company_founded_year = models.IntegerField(
        default=2006, blank=True, null=True, db_index=True)

    company_founded_month = models.IntegerField(
        default=1, blank=True, null=True, db_index=True)

    company_founded_day = models.IntegerField(
        default=1, blank=True,null=True, db_index=True)

    company_website = models.CharField(blank=True, max_length=1007, db_index=True)

    company_logo = models.ImageField(
        max_length=1008, upload_to='img/company', blank=True, default="img/company/noimg.png")

    company_fundraising = models.CharField(
        max_length=COMPANY_FUNDED_MAX_LENGTH, blank=True)
    company_fundraising_currency = models.CharField(
        max_length=COMPANY_FUNDED_MAX_LENGTH, blank=True, null=True)
    company_fundraising_highlight = models.CharField(
        max_length=COMPANY_FUNDED_MAX_LENGTH, blank=True, null=True)
    company_fundraising_deck = models.CharField(blank=True, max_length=1009, null=True)

    company_number = models.CharField(
        max_length=210, blank=True, null=True, db_index=True)
    corporate_number = models.CharField(
        max_length=211, blank=True, null=True, db_index=True)

    employee_total = models.IntegerField(default=0, blank=True)
    employee_total_month_ago = models.IntegerField(default=0, blank=True)
    employee_added_this_month = models.IntegerField(default=0, blank=True)
    employee_growth_month = models.IntegerField(default=0, blank=True)
    employee_total_6month_ago = models.IntegerField(default=0, blank=True)
    employee_added_in_6month = models.IntegerField(default=0, blank=True)
    employee_growth_6month = models.IntegerField(default=0, blank=True)

    employee_added_since_funding = models.IntegerField(default=0, blank=True)
    employee_months_since_funding = models.IntegerField(default=0, blank=True)
    employee_growth_since_funding = models.IntegerField(default=0, blank=True)

    investor_list_csv = models.CharField(max_length=5012, blank=True, null=True, db_index=True)
    product_list_csv = models.CharField(max_length=5013, blank=True, null=True)
    product_market_csv = models.CharField(max_length=5014, blank=True, db_index=True, null=True)
    invested_funding_stage_csv = models.CharField(max_length=5015, blank=True, null=True, db_index=True)

    traffic_growth_month = models.IntegerField(default=0, blank=True)
    last_funding_amt = models.FloatField(default=0, blank=True, db_index=True)
    last_funding_date = models.DateTimeField(null=True, default=default_last_funding_date, db_index=True)
    last_funding_months_ago = models.IntegerField(default=0, blank=True)
    total_funding_amt = models.FloatField(default=0, blank=True, db_index=True)

    funding_stage = models.ForeignKey(FundingStage, null=True, db_index=True)
    funding_stage_name = models.CharField(
        max_length=116, blank=True, null=True)

    product_app_store = models.CharField(max_length=217, blank=True, null=True)
    product_google_play = models.CharField(
        max_length=218, blank=True, null=True)

    company_top_keywords = models.CharField(default='', null=True, max_length=5019)
    company_interests = models.CharField(max_length=5020, blank=True, null=True)
    company_alerts = models.CharField(max_length=221, blank=True, null=True)

    traffic_monthly_unique = models.IntegerField(default=0, blank=True)
    traffic_monthly_unique_week_ago = models.IntegerField(
        default=0, blank=True)
    traffic_monthly_weekly_growth = models.IntegerField(default=0, blank=True)
    traffic_monthly_unique_month_ago = models.IntegerField(
        default=0, blank=True)
    traffic_monthly_monthly_growth = models.IntegerField(default=0, blank=True)
    traffic_mobile_download = models.IntegerField(default=0, blank=True)
    traffic_mobile_download_week_ago = models.IntegerField(
        default=0, blank=True)
    traffic_mobile_download_weekly_growth = models.IntegerField(
        default=0, blank=True)
    traffic_mobile_download_month_ago = models.IntegerField(
        default=0, blank=True)
    traffic_mobile_download_monthly_growth = models.IntegerField(
        default=0, blank=True)

    revenue = models.FloatField(default=0, blank=True)
    total_valuation = models.FloatField(default=0, blank=True, db_index=True)
    total_asset = models.FloatField(default=0, blank=True, db_index=True)
    total_debt = models.FloatField(default=0, blank=True, db_index=True)
    total_capital = models.FloatField(default=0, blank=True, db_index=True)
    total_sales = models.FloatField(default=0, blank=True, db_index=True)
    net_income = models.FloatField(default=0, blank=True)
    operating_income = models.FloatField(default=0, blank=True)
    ratio_sales_net = models.FloatField(default=0, blank=True)
    ratio_sales_operating = models.FloatField(default=0, blank=True)
    period_end_date=models.DateTimeField(null=True, db_index=True)
    
    investor_type = models.ForeignKey(InvestorType, null=True, blank=True)
    investor_fund_sold_3yr = models.IntegerField(default=0, blank=True)
    investor_last_funding_date = models.DateTimeField(null=True)
    investor_portfolio_size = models.IntegerField(default=0, blank=True)
    investor_total_deals = models.IntegerField(default=0, blank=True)

    score1 = models.FloatField(default=0, blank=True, db_index=True)
    score2 = models.FloatField(default=0, blank=True, db_index=True)
    score3 = models.FloatField(default=0, blank=True, db_index=True)
    score4 = models.FloatField(default=0, blank=True, db_index=True)
    score5 = models.FloatField(default=0, blank=True, db_index=True)

    company_linkedin_page = models.CharField(max_length=1017, default='', blank=True, null=True)
    company_facebook_page = models.CharField(max_length=1018, default='', blank=True, null=True)
    company_twitter = models.CharField(max_length=1019, default='', blank=True, null=True)
    
    crawl_source=models.CharField(max_length=200, default='', blank=True, null=True)
    slug = AutoSlugField(populate_from='company_name',
                         unique=True, null=True, blank=True, always_update=True)

    invested_stages = models.ForeignKey(FundingStage, null=True, related_name='resource_invested_stages', db_index=True)
    invested_stages_csv = models.CharField(max_length=5013, blank=True, null=True, db_index=True)
    invested_success = models.IntegerField(default=-1, blank=True, db_index=True)
    invested_success_amt=models.FloatField(default=-1, blank=True, db_index=True)
    invested_founder_csv= models.CharField(max_length=5014, blank=True, null=True, db_index=True)
    invested_market_csv= models.CharField(max_length=5015, blank=True, null=True, db_index=True)
    invested_continent_csv= models.CharField(max_length=5016, blank=True, null=True, db_index=True)
    
    
    def __unicode__(self):
        return self.company_name

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse_lazy
        if self.slug:
            return reverse_lazy('view_company_name',
                                args=[self.slug])
        return reverse_lazy('view_company',
                            args=[self.pk])

    def company_name_as_url(self):
        company_name = unicode(self.company_name).encode('ascii', 'ignore')
        company_url = str(company_name).replace('-', '--')
        company_url = company_url.replace("'", "-c-")
        company_url = company_url.replace(' ', '-')
        return company_url

    def market_as_list(self):
        return self.company_industry.split(', ')

    def market_as_list_new(self):
        return self.company_industry.split(',')

    def total_funding(self):
        return "$%s" % intcomma(int(self.total_funding_amt))

    def create_date_formatted(self):
        create_date = self.created_time
        if create_date != None:
            create_date = create_date.strftime('%Y-%m-%d')
        else:
            # create_date = ''
            create_date = "2000-01-01"
        return create_date

    def last_funding(self):
        last_funding_date = self.last_funding_date
        if last_funding_date != None:
            # last_funding_date = last_funding_date.strftime('%Y-%m-%d')
            last_funding_date = last_funding_date.strftime('%Y-%m-%d')
        else:
            # last_funding_date = ''
            last_funding_date = "2000-01-01"
        # return [last_funding_date, "$%s" % intcomma(int(self.last_funding_amt))]
        return [last_funding_date, int(self.last_funding_amt)]

    def employee_count(self):
        return self.employee_total

    def get_employee_month_ago(self):
        return self.employee_total_month_ago

    def get_employee_added_this_month(self):
        return self.employee_added_this_month

    def get_list_investors(self):
        company_investors = CompanyInvestor.objects.filter(owner=self).values_list(
            'investor__company_name', flat=True).distinct('investor__company_name')

        return company_investors

    def get_dict_investors_from_csv(self):
        investor_dict = dict()

        if self.investor_list_csv:
            if len(self.investor_list_csv) > 0:
                # print self.investor_list_csv
                company_investors = self.investor_list_csv.split(';')
                for investor in company_investors:
                    if len(investor) > 1:
                        names= investor.split('|')
                        investor_id=names[0]
                        investor_name=names[1] 
                        investor_dict[investor_id] = investor_name

        return investor_dict

    def get_dict_industries_from_csv(self):
        market_dict = dict()

        if self.product_market_csv:
            if len(self.product_market_csv) > 0:
                # print self.product_market_csv
                company_markets = self.product_market_csv.split(';')
                for market in company_markets:
                    if len(market) > 1 and re.search('|',market):
                        (market_id, market_name) = market.split('|')
                        market_dict[market_id] = market_name

        return market_dict

    def get_dict_products_from_csv(self):
        product_dict = dict()

        if self.product_list_csv:
            if len(self.product_list_csv) > 0:
                # print self.product_list_csv
                product_lists = self.product_list_csv.split(';')
                for product in product_lists:
                    if len(product) > 1:
                        (product_id, product_name) = product.split('|')
                        product_dict[product_id] = product_name

        return product_dict

    def get_list_industries_from_csv(self):
        industries = []
        if len(self.company_industry) > 0:
            industries = self.company_industry.split(', ')
        return industries

    def get_employee_six_month_ago(self):
        return self.employee_total_6month_ago

    def get_employee_added_six_month_ago(self):
        return self.employee_added_in_6month

    def get_financial_status(self):

        try:
            result = FinancialStatus.objects.filter(company=self).exclude(
                updated_year=0, updated_month=0, updated_week=0).order_by('-updated_year', '-last_edited_time')
        except Exception, e:
            return [0, 0, 0, 0, 0, 0, 0, 0]
        else:

            if result.count() == 0:
                return [0, 0, 0, 0, 0, 0, 0, 0]
            else:
                return [result[0].total_asset, result[0].total_debt, result[0].total_capital, result[0].total_sales, result[0].net_income, result[0].operating_income, result[0].ratio_sales_net, result[0].ratio_sales_operating]

class CompanyResource(models.Model):
    company=models.ForeignKey(Company, db_index=True)
    resource=models.ForeignKey(Resource, db_index=True)
    
class Instrument(models.Model):
    resource=models.ForeignKey(Resource, null=True, db_index=True)
    company=models.ForeignKey(Company, null=True, db_index=True)
    broker=models.CharField(max_length=255, null=True, db_index=True)
    sym=models.CharField(max_length=255, null=True, db_index=True)
    cur=models.CharField(max_length=255, null=True, db_index=True)
    exch=models.CharField(max_length=255, null=True, db_index=True)
    sec_type=models.CharField(max_length=255, null=True, db_index=True)
    trade_freq=models.IntegerField(null=True, db_index=True)
    mult=models.FloatField(max_length=255, null=True, db_index=True)
    local_sym=models.CharField(max_length=255, null=True, db_index=True)
    
    subscribe=models.BooleanField(default=False, db_index=True)
    
    contract_month=models.CharField(max_length=255, null=True, db_index=True)
    expiry=models.CharField(max_length=255, null=True, db_index=True)
    ev_rule=models.CharField(max_length=255, null=True, db_index=True)
    liquid_hours=models.CharField(max_length=255, null=True, db_index=True)
    long_name=models.CharField(max_length=255, null=True, db_index=True)
    min_tick=models.FloatField(max_length=255, null=True, db_index=True)
    time_zone_id=models.CharField(max_length=255, null=True, db_index=True)
    trading_hours=models.CharField(max_length=255, null=True, db_index=True)
    under_con_id=models.IntegerField(null=True, db_index=True)
    
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, db_index=True)
    updated_at = models.DateTimeField(
        auto_now_add=True, null=True, db_index=True)
    crawl_source=models.CharField(max_length=200, default='', blank=True, null=True)

    def __unicode__(self):
        return '%s' % self.name

    def save(self, *args, **kwargs):
        eastern=timezone('US/Eastern')
       
        if self.created_at == None:
            self.created_at = datetime.now().replace(tzinfo=eastern)  
        self.updated_at = datetime.now().replace(tzinfo=eastern) 
        
        super(Instrument, self).save(*args, **kwargs)



class System(models.Model):
    #user = models.OneToOneField(User, primary_key=True)
    version= models.CharField(max_length=255, null=True, db_index=True)
    system= models.CharField(max_length=255, null=True, db_index=True)
    name=models.CharField(max_length=255, null=True, db_index=True)
    c2id=models.CharField(max_length=255, null=True, db_index=True)
    c2api=models.CharField(max_length=255, null=True, db_index=True)
    c2qty=models.IntegerField(null=True, db_index=True)
    c2submit=models.BooleanField(default=False)
    c2instrument=models.ForeignKey(Instrument, related_name='c2instrument', null=True, db_index=True)
    ibqty=models.IntegerField(null=True, db_index=True)
    ibinstrument=models.ForeignKey(Instrument, related_name='ibinstrument', null=True, db_index=True)
    ibsubmit=models.BooleanField(default=False)
    trade_freq=models.IntegerField(null=True, db_index=True)
    ibmult=models.IntegerField(null=True, db_index=True)
    c2mult=models.IntegerField(null=True, db_index=True)
    signal=models.CharField(max_length=255, null=True, db_index=True)



class Feed(models.Model):
    instrument=models.ForeignKey(Instrument, db_index=True)
    frequency=models.IntegerField(null=True, db_index=True)
    date=models.DateTimeField(
        null=True, db_index=True)
    open=models.FloatField(null=True)
    high=models.FloatField(null=True)
    low=models.FloatField(null=True)
    close=models.FloatField(null=True)
    change=models.FloatField(null=True)
    settle=models.FloatField(null=True)
    open_interest=models.FloatField(null=True)
    
    volume=models.FloatField(null=True)
    wap=models.FloatField(null=True)
    
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, db_index=True)
    updated_at = models.DateTimeField(
        auto_now_add=True, null=True, db_index=True)
    crawl_source=models.CharField(max_length=200, default='', blank=True, null=True)

    def __repr__(self):
        #return '{ "date":"%s", "open":%s, "high":%s, "low":%s, "close":%s,"volume":%s }' % (self.date, self.open, self.high, self.low, self.close, self.volume)
        return '{ "date":"%s",  "close":%s,"volume":%s }' % (self.date,  self.close, self.volume)
        
    def __str__(self):
        return self.__repr__()
    
    def __unicode__(self):
        return self.__repr__()
    
    def save(self, *args, **kwargs):
        eastern=timezone('US/Eastern')
       
        if self.created_at == None:
            self.created_at = datetime.now().replace(tzinfo=eastern)  
        self.updated_at = datetime.now().replace(tzinfo=eastern)  
        super(Feed, self).save(*args, **kwargs)

class FeedLive(models.Model):
    instrument=models.ForeignKey(Instrument, db_index=True)
    frequency=models.IntegerField(null=True, db_index=True)
    date=models.DateTimeField(
        null=True, db_index=True)
    open=models.FloatField(null=True)
    high=models.FloatField(null=True)
    low=models.FloatField(null=True)
    close=models.FloatField(null=True)
    change=models.FloatField(null=True)
    settle=models.FloatField(null=True)
    open_interest=models.FloatField(null=True)
    
    volume=models.FloatField(null=True)
    wap=models.FloatField(null=True)
    
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, db_index=True)
    updated_at = models.DateTimeField(
        auto_now_add=True, null=True, db_index=True)
    crawl_source=models.CharField(max_length=200, default='', blank=True, null=True)

    def __repr__(self):
        #return '{ "date":"%s", "open":%s, "high":%s, "low":%s, "close":%s,"volume":%s }' % (self.date, self.open, self.high, self.low, self.close, self.volume)
        return '{ "date":"%s",  "close":%s,"volume":%s }' % (self.date,  self.close, self.volume)
        
    def __str__(self):
        return self.__repr__()
    
    def __unicode__(self):
        return self.__repr__()
    
    def save(self, *args, **kwargs):
        eastern=timezone('US/Eastern')
       
        if self.created_at == None:
            self.created_at = datetime.now().replace(tzinfo=eastern)  
        if self.updated_at == None:
            self.updated_at = datetime.now().replace(tzinfo=eastern)  
        super(FeedLive, self).save(*args, **kwargs)

class Prediction(models.Model):
    instrument=models.ForeignKey(Instrument, db_index=True)
    frequency=models.IntegerField(null=True, db_index=True)
    pred_start_date=models.DateTimeField(
        null=True, db_index=True)
    
    date=models.DateTimeField(
        null=True, db_index=True)
    open=models.FloatField(null=True)
    high=models.FloatField(null=True)
    low=models.FloatField(null=True)
    close=models.FloatField(null=True)
    volume=models.FloatField(null=True)
    wap=models.FloatField(null=True)
    algo_name=models.CharField(max_length=200, default='', blank=True, null=True)
    is_scaled=models.BooleanField(default=False)
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, db_index=True)
    updated_at = models.DateTimeField(
        auto_now_add=True, null=True, db_index=True)
    crawl_source=models.CharField(max_length=200, default='', blank=True, null=True)

    def __repr__(self):
        #return '{ "date":"%s", "open":%s, "high":%s, "low":%s, "close":%s,"volume":%s }' % (self.date, self.open, self.high, self.low, self.close, self.volume)
        return '{ "date":"%s", "close":%s, "volume":%s }' % (self.date,  self.close, self.volume)
        
    def __str__(self):
        return self.__repr__()
    
    def __unicode__(self):
        return self.__repr__()
    
    def save(self, *args, **kwargs):
        eastern=timezone('US/Eastern')
       
        if self.created_at == None:
            self.created_at = datetime.now().replace(tzinfo=eastern)  
        self.updated_at = datetime.now().replace(tzinfo=eastern)  
        super(Prediction, self).save(*args, **kwargs)


class BidAsk(models.Model):
    instrument=models.ForeignKey(Instrument, db_index=True)
    frequency=models.IntegerField(null=True, db_index=True)
    ask=models.FloatField(null=True)
    asksize=models.FloatField(null=True)
    bid=models.FloatField(null=True)
    bidsize=models.FloatField(null=True)
    date=models.DateTimeField(
        null=True, db_index=True)
    
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, db_index=True)
    updated_at = models.DateTimeField(
        auto_now_add=True, null=True, db_index=True)
    crawl_source=models.CharField(max_length=200, default='', blank=True, null=True)

    def __unicode__(self):
        return '%s' % self.name

    def save(self, *args, **kwargs):
        eastern=timezone('US/Eastern')
       
        if self.created_at == None:
            self.created_at = datetime.now().replace(tzinfo=eastern)  
        self.updated_at = datetime.now().replace(tzinfo=eastern) 
        super(BidAsk, self).save(*args, **kwargs)


