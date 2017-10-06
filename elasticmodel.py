#from django.db import models
#from django.contrib.auth.models import User
#from taggit.managers import TaggableManager
#from taggit.models import TaggedItemBase
#from django.utils.safestring import mark_safe
#from main.models import *
from datetime import *
#from django.template.defaultfilters import slugify
#from django.contrib.humanize.templatetags.humanize import *
#from autoslug import AutoSlugField
from dateutil.relativedelta import relativedelta
import dateutil.parser
import pytz
import os
import re
import uuid
import operator


COMPANY_FUNDED_MAX_LENGTH=1000

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

from elasticsearch_dsl import Keyword, Mapping, Nested, Text
from datetime import datetime
from elasticsearch_dsl import DocType, Date, Nested, Boolean, \
    analyzer, InnerObjectWrapper, Completion, Keyword, Text, Integer, Float, MetaField, Object, Long, String,analysis
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.query import MultiMatch, Match, Query, SF
from elasticsearch_dsl import Search, Q


myindex='beginning'
connections.configure(
    default={
        'hosts': ['localhost:9200']
    }
)


def get_resource_continent_id():
    seq=Sequence(_id='resource_continent_id')
    seq.save()
    #pass #print seq._version
    return seq._version + 10000000

def get_syndicate_id():
    seq=Sequence(_id='syndicate_id')
    seq.save()
    #pass #print seq._version
    return seq._version + 10000000

def get_system_id():
    seq=Sequence(_id='system_id')
    seq.save()
    pass #print seq._version
    return seq._version + 10000000


def get_instrument_id():
    seq=Sequence(_id='instrument_id')
    seq.save()
    pass #print seq._version
    return seq._version + 10000000

def get_notification_id():
    seq=Sequence(_id='notification_id')
    seq.save()
    pass #print seq._version
    return seq._version + 10000000


def get_partnership_id():
    seq=Sequence(_id='partnership_id')
    seq.save()
    pass #print seq._version
    return seq._version + 10000000

def get_company_category_list_id():
    seq=Sequence(_id='company_category_list_id')
    seq.save()
    pass #print seq._version
    return seq._version + 10000000

def get_product_category_list_id():
    seq=Sequence(_id='product_category_list_id')
    seq.save()
    pass #print seq._version
    return seq._version + 10000000


def get_category_list_id():
    seq=Sequence(_id='category_list_id')
    seq.save()
    pass #print seq._version
    return seq._version + 10000000

def get_banner_list_id():
    seq=Sequence(_id='banner_list_id')
    seq.save()
    pass #print seq._version
    return seq._version + 10000000

def get_company_investing_event_id():
    seq=Sequence(_id='company_investing_event_id')
    seq.save()
    pass #print seq._version
    return seq._version + 10000000


def get_company_investor_id():
    seq=Sequence(_id='company_investor_id')
    seq.save()
    pass #print seq._version
    return seq._version + 10000000


def get_company_portfolio_id():
    seq=Sequence(_id='company_portfolio_id')
    seq.save()
    pass #print seq._version
    return seq._version + 10000000

def get_market_count_id():
    seq=Sequence(_id='market_count_id')
    seq.save()
    pass #print seq._version
    return seq._version + 10000000


def get_market_dict_id():
    seq=Sequence(_id='market_dict_id')
    seq.save()
    pass #print seq._version
    return seq._version + 10000000


def get_resource_country_status_id():
    seq=Sequence(_id='resource_country_status_id')
    seq.save()
    pass #print seq._version
    return seq._version + 10000000

def get_resource_country_id():
    seq=Sequence(_id='resource_country_id')
    seq.save()
    pass #print seq._version
    return seq._version + 10000000

def get_resource_continent_status_id():
    seq=Sequence(_id='resource_continent_status_id')
    seq.save()
    pass #print seq._version
    return seq._version + 10000000


def get_recent_update_id():
    seq=Sequence(_id='recent_update_id')
    seq.save()
    pass #print seq._version
    return seq._version + 10000000


def get_market_watch_id():
    seq=Sequence(_id='market_watch_id')
    seq.save()
    pass #print seq._version
    return seq._version + 10000000


def get_press_article_id():
    seq=Sequence(_id='press_article_id')
    seq.save()
    pass #print seq._version
    return seq._version + 10000000

def get_article_relation_id():
    seq=Sequence(_id='article_relation_id')
    seq.save()
    pass #print seq._version
    return seq._version + 10000000


def get_social_feed_id():
    seq=Sequence(_id='social_feed_id')
    seq.save()
    pass #print seq._version
    return seq._version + 10000000

def get_region_id():
    seq=Sequence(_id='region_id')
    seq.save()
    pass #print seq._version
    return seq._version + 10

def get_investor_type_id():
    seq=Sequence(_id='investor_type_id')
    seq.save()
    pass #print seq._version
    return seq._version + 10

def get_job_type_id():
    seq=Sequence(_id='job_type_id')
    seq.save()
    pass #print seq._version
    return seq._version + 10

def get_job_skill_id():
    seq=Sequence(_id='job_skill_id')
    seq.save()
    pass #print seq._version
    return seq._version + 10

def get_job_role_id():
    seq=Sequence(_id='job_role_id')
    seq.save()
    pass #print seq._version
    return seq._version + 50


def get_school_id():
    seq=Sequence(_id='school_id')
    seq.save()
    pass #print seq._version
    return seq._version + 35000

def get_funding_stage_id():
    seq=Sequence(_id='funding_stage_id')
    seq.save()
    pass #print seq._version
    return seq._version + 4000

def get_city_id():
    seq=Sequence(_id='city_id')
    seq.save()
    pass #print seq._version
    return seq._version + 5000

def get_state_id():
    seq=Sequence(_id='state_id')
    seq.save()
    pass #print seq._version
    return seq._version + 1000

def get_country_id():
    seq=Sequence(_id='country_id')
    seq.save()
    pass #print seq._version
    return seq._version + 300

def get_continent_id():
    seq=Sequence(_id='continent_id')
    seq.save()
    pass #print seq._version
    return seq._version + 10

def get_location_id():
    seq=Sequence(_id='location_id')
    seq.save()
    pass #print seq._version
    return seq._version + 10

def get_crawled_article_id():
    seq=Sequence(_id='crawled_article_id')
    seq.save()
    pass #print seq._version
    return seq._version + 8000000

def get_market_id():
    seq=Sequence(_id='market_id')
    seq.save()
    pass #print seq._version
    return seq._version + 120000

def get_resource_id():
    seq=Sequence(_id='resource_id')
    seq.save()
    pass #print seq._version
    return seq._version + 100000000

def get_product_id():
    seq=Sequence(_id='product_id')
    seq.save()
    pass #print seq._version
    return seq._version + 100000000

def get_job_id():
    seq=Sequence(_id='job_id')
    seq.save()
    pass #print seq._version
    return seq._version + 100000000

def get_company_id():
    seq=Sequence(_id='company_id')
    seq.save()
    pass #print seq._version
    return seq._version + 100000000

class Sequence(DocType):
    class Meta:
        index = 'sequence'


class SearchQuerySet():
    def models(self, name):
        if name == Company:
            return Company.search()
        elif name == Product:
            return Product.search()
        elif name  == Job:
            return Job.search()
        elif name == Resource:
            return Resource.search()
        elif name == UserDefault:
            return UserDefault.search()
        elif name == CategoryList:
            return CategoryList.search()
        elif name == CompanyCategoryList:
            return CompanyCategoryList.search()
        elif name == ProductCategoryList:
            return ProductCategoryList.search()
        elif name == CompanyMember:
            return CompanyMember.search()
        elif name == CompanyInvestor:
            return CompanyInvestor.search()
        elif name == CompanyInvestingEvent:
            return CompanyInvestingEvent.search()
        elif name == Country:
            return Country.search()
        elif name == Continent:
            return Continent.search()
        elif name == City:
            return City.search()
        elif name == Notification:
            return Notification.search()
        elif name == UserDefaultView:
            return UserDefaultView.search()
        elif name == BannerList:
            return BannerList.search()


html_strip = analyzer('html_strip',
    tokenizer="standard",
    filter=["standard", "lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)

class Company(DocType):

    id=Long()

    my_id=Text()
    django_id=Text()
    company_id=Long()
    django_ct=Text()
    text=Text()
    
    last_edited_time = Date()
    created_time = Date()
    
    owner_id=Integer()
    
    is_private_company_all = Boolean()
    is_private_company_class = Boolean()
    is_private_investor_class = Boolean()
    is_private_company_short = Boolean()
    is_private_company_long = Boolean()
    is_private_company_industry = Boolean()
    is_private_company_country = Boolean()
    is_private_company_city = Boolean()
    is_private_company_state = Boolean()
    is_private_company_region = Boolean()
    is_private_company_employee = Boolean()
    is_private_corporation = Boolean()
    is_private_company_established = Boolean()
    is_private_company_founded_year = Boolean()
    is_private_patent = Boolean()
    is_private_team = Boolean()
    is_private_company_fundraising = Boolean()
    is_private_company_logo = Boolean()
    is_private_company_website = Boolean()
    is_private_company_founded_day = Boolean()
    is_private_company_founded_month = Boolean()
    is_private_company_name = Boolean()

    
    company_favorite_count = Integer()
    company_recommendation_count = Integer()
    
    
    is_active = Boolean()
    is_public = Boolean()
    is_save = Boolean()
    is_confirm = Boolean()


    is_trusted_vc = Boolean()
    is_partner = Boolean()
    is_angel = Boolean()

    
    is_government = Boolean()
    is_tips = Boolean()
    is_dcamp = Boolean()
    is_rocketpunch = Boolean()
    is_dart = Boolean()
    is_bizinkorea = Boolean()
    is_startup = Boolean()
    is_investor = Boolean()
    
    
    ticker = Text()
    exchange=Text()
    sec_cik=Text()
    sec_cik_int=Text()
    partner_order = Integer()

    last_edited_time = Date()
    created_time = Date()
    
    company_name = Text( fields={'raw': String(index='not_analyzed')})
    
    company_kor_name = Text()

    company_class = Text(fields={'raw': String(index='not_analyzed')})
    tips_start_date = Date()
    rocketpunch_url = Text()
    angellist_url=Text()
    sec_url=Text()
    e27_url=Text()
    f6s_url=Text()
    forbes_url=Text()

    
    investor_class = Text( fields={'raw': String(index='not_analyzed')})

    company_short = Text( fields={'raw': String(index='not_analyzed')})

    company_long = Text()

    company_industry = Text( fields={'raw': String(index='not_analyzed')})

    company_continent = Text( fields={'raw': String(index='not_analyzed')})
    #continent=models.ForeignKey(Continent,  )
    continent_id=Integer()


    company_country = Text( fields={'raw': String(index='not_analyzed')})
    #country=models.ForeignKey(Country,  )
    country_id=Integer()


    company_city = Text( fields={'raw': String(index='not_analyzed')})
    #city=models.ForeignKey(City,  )
    city_id=Integer()

    
    company_state = Text( fields={'raw': String(index='not_analyzed')})
    #state=models.ForeignKey(State,  )
    state_id=Integer()


    company_region =Text( fields={'raw': String(index='not_analyzed')})
    #region=models.ForeignKey(Region,  )
    region_id=Integer()
    company_location = Text()
    company_location_latitude=Integer()
    company_location_longitude= Integer()

    # company_region_class = ManyToManyField(Region)

    company_employee = Text()

    corporation = Text()

    company_established = Text()

    company_founded_year = Integer()

    company_founded_month = Integer()

    company_founded_day = Integer()

    company_website = Text()

    company_logo = Text()

    company_fundraising = Text()
    company_fundraising_currency = Text()
    company_fundraising_highlight = Text()
    company_fundraising_deck = Text()

    company_number = Text()
    corporate_number = Text()

    employee_total = Integer()
    employee_total_month_ago = Integer()
    employee_added_this_month = Integer()
    employee_growth_month = Integer()
    employee_total_6month_ago = Integer()
    employee_added_in_6month = Integer()
    employee_growth_6month = Integer()

    employee_added_since_funding = Integer()
    employee_months_since_funding = Integer()
    employee_growth_since_funding = Integer()

    investor_list_csv = Text( fields={'raw': Keyword()})
    product_list_csv = Text( fields={'raw': Keyword()})
    product_market_csv = Text( fields={'raw': Keyword()})
    invested_funding_stage_csv = Text()

    traffic_growth_month = Integer()
    last_funding_amt = Float()
    last_funding_date = Date()
    last_funding_months_ago = Integer()
    total_funding_amt = Float()

    #funding_stage=models.ForeignKey(FundingStage,  )

    funding_stage_id=Integer()

    funding_stage_name = Text(fields={'raw': String(index='not_analyzed')})

    product_app_store = Text()
    product_google_play = Text()

    company_top_keywords = Text()
    company_interests = Text()
    company_alerts = Text()

    traffic_monthly_unique = Integer()
    traffic_monthly_unique_week_ago = Integer()
    traffic_monthly_weekly_growth = Integer()
    traffic_monthly_unique_month_ago = Integer()
    traffic_monthly_monthly_growth = Integer()
    traffic_mobile_download = Integer()
    traffic_mobile_download_week_ago = Integer()
    traffic_mobile_download_weekly_growth = Integer()
    traffic_mobile_download_month_ago = Integer()
    traffic_mobile_download_monthly_growth = Integer()

    revenue = Float()
    total_valuation = Float()
    total_asset = Float()
    total_debt = Float()
    total_capital = Float()
    total_sales = Float()
    net_income = Float()
    operating_income = Float()
    ratio_sales_net = Float()
    ratio_sales_operating = Float()
    period_end_date=Date()
    
    #investor_type=models.ForeignKey(InvestorType,  )
    
    investor_type_id=Integer()
    
    investor_fund_sold_3yr = Integer()
    investor_last_funding_date = Date()
    investor_portfolio_size = Integer()
    investor_total_deals = Integer()

    score1 = Float()
    score2 = Float()
    score3 = Float()
    score4 = Float()
    score5 = Float()

    company_linkedin_page = Text()
    company_facebook_page = Text()
    company_twitter = Text()
    
    crawl_source=Text()
    slug = Text()

    #invested_stages=models.ForeignKey(FundingStage,  related_name='company_invested_stages')

    invested_stages_id=Integer()
    
    invested_stages_csv = Text()
    invested_success = Integer()
    invested_success_amt=Float()
    invested_founder_csv= Text()
    invested_market_csv= Text()
    invested_continent_csv= Text()
    
    
    class Meta:
        index = myindex
        
        
    def save(self, *args, ** kwargs):
        if not self.created_time:
            self.created_time = datetime.now()
            self.is_active=True
        if not self.company_logo:
            self.company_logo="http://beginning.wold/media/img/company/noimg.png"
        if not self.company_class:
            self.company_class='Startup'
        self.last_edited_time = datetime.now()
        if not self.id:
            self.id=get_company_id()
            self._id='main.company.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.company'
            self.text=self.company_name
            self.is_startup=True
            self.slug=str(self.id) + '_' + slugify(self.company_name)
            self.is_active=True
                
        super(Company, self).save(*args, **kwargs)
    

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
        company_investors = CompanyInvestor.search().filter('term',owner_id=self.id).execute()
        investors=[]
        for investor in company_investors:
            investors.append(investor.investor_name)
            
        return investors

    def get_dict_investors_from_csv(self):
        investor_dict = dict()

        if self.investor_list_csv:
            if len(self.investor_list_csv) > 0:
                # pass #print self.investor_list_csv
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
                # pass #print self.product_market_csv
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
                # pass #print self.product_list_csv
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


class Market(DocType):
    id=Long()
    name = Text()
    vertical = Text()
    sub_vertical = Text()
    total = Integer()
    slug = Text()
    
    created_at = Date()
    updated_at = Date()
    crawl_source=Text()

    class Meta:
        index = myindex
        
    
    def save(self, *args, ** kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if not self.id:
            self.id=get_market_id()
            self._id='main.market.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.market'
            self.text=self.market_name
            self.slug=str(self.id) + '_' + slugify(self.name)

        if not self.total:
            self.total=1
            
        super(Market, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s' % self.name

class Product(DocType):
    #owner=models.ForeignKey(Company)
    id=Long()
    my_id=Text()
    django_id=Text()
    company_id=Long()
    django_ct=Text()
    text=Text()
    
    product_id=Long()
    owner_id=Integer()
    owner_name = Text()
    owner_email = Text()
    owner_slug = Text()
    product_city= Text()
    product_country= Text()
    investor_list_csv= Text()
    
    product_market_csv = Text()

    is_save = Boolean()
    is_confirm = Boolean()
    is_active = Boolean()

    last_edited_time = Date()
    created_time = Date()

    product_favorite_count = Integer()
    product_recommendation_count = Integer()

    is_private_product_all = Boolean()
    is_private_product_name = Boolean()
    is_private_product_class = Boolean()
    is_private_product_stage = Boolean()
    is_private_product_market = Boolean()
    is_private_product_released = Boolean()
    is_private_product_release_month = Boolean()
    is_private_product_release_day = Boolean()
    is_private_product_short = Boolean()
    is_private_product_long = Boolean()
    is_private_product_website = Boolean()
    is_private_product_video = Boolean()
    is_private_product_bm = Boolean()
    is_private_product_google_play = Boolean()
    is_private_product_app_store = Boolean()
    is_private_product_logo = Boolean()
    
    is_free = Boolean()
    
    product_name = Text()
    product_kor_name = Text()

    product_class = Text()

    product_stage = Text()

    product_market = Text()


    markets = Nested(
            doc_class=Market,
    )
    
    product_release_year = Integer()

    product_release_month = Integer()

    product_release_day = Integer()

    product_short = Text()

    product_long = Text()

    product_website = Text()

    product_video = Text()

    product_bm = Text()

    product_google_play = Text()

    product_app_store = Text()

    product_linkedin_page = Text()
    product_facebook_page = Text()
    product_twitter = Text()

    is_dart = Boolean()
    is_rocketpunch = Boolean()
    rocketpunch_url = Text()

    product_logo = Text()

    is_private_product_screenshot = Boolean()
    product_screenshot_count = Integer()
    product_screenshot_1 = Text()
    product_screenshot_2 = Text()
    product_screenshot_3 = Text()
    product_screenshot_4 = Text()
    product_screenshot_5 = Text()
    product_screenshot_6 = Text()
    product_screenshot_7 = Text()
    product_screenshot_8 = Text()
    product_screenshot_9 = Text()
    product_screenshot_10 = Text()

    slug = Text()
    
    alexa_rank = Integer()
    facebook_like = Integer()
    facebook_talking = Integer()
    crawl_source=Text()

    class Meta:
        index = myindex
    
    def save(self, *args, ** kwargs):
        # doing something strange when updating...
        #self.product_market = self.product_market.lower()
        if not self.created_time:
            self.created_time = datetime.now()
            self.is_active=True
        if not self.product_logo:
            self.product_logo="http://beginning.wold/media/img/product/noimg.png"
        self.last_edited_time = datetime.now()
        if not self.id:
            self.id=get_product_id()
            self.product_id=self.id
            self._id='main.product.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.product'
            self.text=self.product_name
            self.slug=str(self.id) + '_' + slugify(self.product_name)
            self.is_confirm = False
            self.is_active=True
            
        super(Product, self).save(*args, **kwargs)
    
    
    def __unicode__(self):
        return self.product_name

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse_lazy
        if self.slug:
            return reverse_lazy('view_product_name', args=[self.slug])
        return reverse_lazy('view_product', args=[self.pk])

    def product_name_as_url(self):
        product_name = unicode(self.product_name).encode('ascii', 'ignore')
        product_url = str(product_name).replace('-', '--')
        product_url = str(product_name).replace('()', '')
        product_url = product_url.replace("'", "-c-")
        product_url = product_url.replace(' ', '-')
        return product_url

    def product_name_as_replaced(self):
        replaced_name = self.product_name.encode('utf-8')
        replaced_name = str(replaced_name).lower()
        replaced_name = replaced_name.replace("'", "")
        replaced_name = replaced_name.replace(":", "")
        return replaced_name

    def get_product_short_string(self):
        return self.product_short.encode('utf-8').lower()

    def get_similar_product(self):
        return SimilarProduct.search().filter(owner=self)

    def market_as_list(self):
        return self.product_market.split(',')

    def market_exist(self, market):
        market_lower_list = []
        market_list = self.market_as_list()
        for market_ in market_list:
            market_lower_list.append(str(market_).lower())

        if market in market_lower_list:
            return True
        else:
            return False

    def video_as_embedded(self):
        if 'youtube.com' in self.product_video:
            if '?v=' in self.product_video:
                return 'http://www.youtube.com/embed/' + self.product_video.split('?v=')[-1]
            else:
                return self.product_video
        elif 'youtu.be' in self.product_video:
            if '?v=' in self.product_video:
                return 'http://www.youtube.com/embed/' + self.product_video.split('?v=')[-1]
            else:
                return 'http://www.youtube.com/embed/' + self.product_video.split('/')[-1]
        elif 'vimeo.com' in self.product_video:
            return 'https://player.vimeo.com/video/' + self.product_video.split('/')[-1]
        elif 'youku.com' in self.product_video:
            split_url = self.product_video.split('/')[-1]
            split_url1 = split_url.split('.')[0]
            split_url2 = split_url1.split('_')[1]
            return 'http://player.youku.com/embed/%s' % split_url2
        else:
            return self.product_video


    def get_list_investors(self):
        company_investors = CompanyInvestor.search().filter(owner=self.owner).values(
            'investor__company_name', 'investor__slug').distinct()

        return company_investors

    def get_last_funded(self):
        investor = CompanyInvestor.search().filter(
            owner=self.owner).order_by('last_edited_time')

        if investor:
            if investor.last().investor_day and investor.last().investor_month and investor.last().investor_year:
                return "%s/%s/%s" % (investor.last().investor_day, investor.last().investor_month, investor.last().investor_year)
            else:
                return "-"
        else:
            return "-"

    def natural_day_added(self):
        if self.created_time == None:
            created_time = "2015-11-01 11:00:00"
            parse_created_time = datetime.strptime(
                created_time, '%Y-%m-%d %H:%M:%S')
            return naturaltime(parse_created_time)
        else:
            return naturaltime(self.created_time)

    def natural_day_released(self):

        if self.product_release_year != None and self.product_release_month != None and self.product_release_day:
            date_released = "%s-%s-%s" % (self.product_release_year,
                                          self.product_release_month, self.product_release_day)
            parse_date_released = datetime.strptime(date_released, '%Y-%m-%d')
            date_now = datetime.now().date()
            # return parse_date_released
            MOMENT = 120

            if isinstance(parse_date_released, datetime):
                delta = datetime.now().date() - parse_date_released.date()
                if delta.days > 6:
                    return parse_date_released.strftime("%b %d, %Y")
                if delta.days > 1:
                    return parse_date_released.strftime("%A")
                elif delta.days == 1:
                    return 'yesterday'
                elif delta.seconds > 3600:
                    return str(delta.seconds / 3600) + ' hours ago'
                elif delta.seconds > MOMENT:
                    return str(delta.seconds / 60) + ' minutes ago'
                else:
                    return parse_date_released.strftime("%b %d, %Y")
                return defaultfilters.date(parse_date_released)
            else:
                return str(parse_date_released)
        else:
            return "-"

    def percent_web_traffic(self):
        # last_crawler_date = alexaRank.search().order_by('last_edited_time').last().last_edited_time.date()

        webRank = alexaRank.search().filter(website_company=self.owner, website_product=self).exclude(website_rank=0).exclude(updated_year=0).exclude(updated_month=0).order_by('last_edited_time')
        #webRank = self.alexarank_set.exclude(
        #    updated_year=0, updated_month=0).order_by('last_edited_time')

        if webRank.count() > 1:

            total_count = webRank.count()

            prev_rank = int(webRank[total_count - 2].website_rank)
            curr_rank = int(webRank[total_count - 1].website_rank)

            percent = "{:.0%}".format(
                float((prev_rank - curr_rank)) / float(prev_rank) * 100.0)
            total = float((prev_rank - curr_rank)) / float(prev_rank) * 100.0
            return str(int(total)) + "%"
        else:
            return "0%"

    def ten_percent_web_traffic_in_two_weeks(self):
        # webRank = alexaRank.search().filter(website_company=self.owner,website_product=self).exclude(website_rank=0).exclude(updated_year=0).exclude(updated_month=0).order_by('last_edited_time')
        last_crawler_date = alexaRank.search().order_by(
            'last_edited_time').last().last_edited_time.date()
        webRank = self.alexarank_set.exclude(
            updated_year=0, updated_month=0).order_by('last_edited_time')

        if webRank.count() > 2:

            if webRank.last().last_edited_time.date() == last_crawler_date:
                total_count = webRank.count()
                this_week = int(webRank[total_count - 1].website_rank)
                previous_week = int(webRank[total_count - 2].website_rank)
                previous_previous_week = int(
                    webRank[total_count - 3].website_rank)

                if int(previous_week) > 0 and int(this_week) > 0 and int(previous_previous_week) > 0:
                    percent_1 = float((previous_week - this_week)
                                      ) / float(previous_week) * 100.0
                    percent_2 = float(
                        (previous_previous_week - previous_week)) / float(previous_previous_week) * 100.0

                    if percent_1 >= 5.0 and percent_2 >= 5.0:
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False

    def percent_fb_like(self):
        fbLike = FacebookLike.search().filter(facebook_company=self.owner, facebook_product=self).exclude(
            facebook_like=0).exclude(updated_year=0).exclude(updated_month=0).order_by('last_edited_time')

        if fbLike.count() > 1:
            total_count = fbLike.count()

            prev_rank = int(fbLike[total_count - 2].facebook_like)
            curr_rank = int(fbLike[total_count - 1].facebook_like)

            percent = "{:.0%}".format(
                float((curr_rank - prev_rank)) / float(prev_rank) * 100.0)
            total = float((curr_rank - prev_rank)) / float(prev_rank) * 100.0
            return str(int(total)) + "%"
        else:
            return "0%"

    def last_web_traffic_rank(self):
        if int(self.alexa_rank) <= 0:
                    return "-"
        else:
            return self.alexa_rank

    def last_web_traffic_rank_with_zero_callback(self):
        if int(self.alexa_rank) <= 0:
                    return 0
        else:
            return self.alexa_rank


    def total_funding(self):
        funding_list = []
        usd_to_krw = Currency.search().get(currency_name='KRW').currency_price

        total_funding = 0

        investing_event_list = CompanyInvestingEvent.search().filter(
            owner=self.owner)

        for investor in investing_event_list:
            if investor.event_currency and investor.event_amount:
                if investor.event_currency == 'USD':
                    total_funding += int(investor.event_amount.replace(',', ''))
                elif investor.event_currency == 'KRW':
                    total_funding += int(investor.event_amount.replace(',',
                                                                       '').replace('-', '0')) / usd_to_krw

        return total_funding

    def get_dict_industries_from_csv(self):
        market_dict = dict()

        if self.product_market_csv:
            if len(self.product_market_csv) > 0:
                # pass #print self.product_market_csv
                company_markets = self.product_market_csv.split(';')
                for market in company_markets:
                    if len(market) > 1 and re.search('|',market):
                        (market_id, market_name) = market.split('|')
                        market_dict[market_id] = market_name

        return market_dict

    def get_dict_investors_from_csv(self):
        market_dict = dict()

        if self.investor_list_csv:
            if len(self.investor_list_csv) > 0:
                # pass #print self.investor_list_csv
                company_markets = self.investor_list_csv.split(';')
                for market in company_markets:
                    if len(market) > 1 and re.search('|',market):
                        (market_id, market_name) = market.split('|')
                        market_dict[market_id] = market_name

        return market_dict

class UserProfile(DocType):
    #user=models.ForeignKey(User,)
    user_id=Long()
    user_name=Text()
    is_input = Boolean()
    last_edited_time = Date()
    created_time = Date()

    is_private_all = Boolean()
    is_private_city = Boolean()

    continent_name = Text()
    #continent=models.ForeignKey(Continent,  )
    continent_id=Integer()


    country_name = Text()
    #country=models.ForeignKey(Country,  )
    country_id=Integer()


    city_name = Text()
    #city=models.ForeignKey(City,  )
    city_id=Integer()

    
    state_name = Text()
    #state=models.ForeignKey(State,  )
    state_id=Integer()


    region_name = Text()
    #region=models.ForeignKey(Region,  )
    region_id=Integer()


    location = Text()
    location_latitude=Integer()
    location_longitude= Integer()

    is_private_phone = Boolean()
    phone_1_0 = Text()
    phone_1_1 = Text()
    phone_1_2 = Text()

    profile_has_image = Boolean()
    profile_image = Text()

    is_private_gender = Boolean()
    gender = Text()

    is_private_university = Boolean()
    university = Text()
    
    university_csv = Text()
    
    is_private_major = Boolean()
    major = Text()

    is_private_speciality = Boolean()
    speciality = Text()

    is_private_career = Boolean()

    is_private_honor = Boolean()

    is_private_work = Boolean()

    is_private_interest = Boolean()
    interest = Text()

    is_private_industry = Boolean()
    industry = Text()
    is_private_website = Boolean()
    website = Text()

    is_private_social = Boolean()
    social_facebook = Text()
    social_twitter = Text()
    social_linkedin = Text()
    social_google = Text()
    social_blog = Text()
    social_github = Text()
    social_stack = Text()

    favorite_industry = Text()
    favorite_company = Text()

    is_job_hunting = Boolean()

    # CV
    profile_has_cv = Boolean()
    profile_cv = Text()
    profile_cv_plain = Text()
    profile_cv_mini = Text()
    profile_cv_accomplishment = Text()
    profile_cv_honor = Text()
    desired_salary = Integer()

    is_public=Boolean()
    invest_market_csv = Text()
    profile_top_keywords = Text()
    
    last_invested_amt = Float()
    last_invested_date = Date()
    last_invested_months_ago = Integer()
    total_invested_amt = Float()

    crawl_source=Text()

    class Meta:
        index = myindex
    
    def save(self, *args, ** kwargs):
        # doing something strange when updating...
        #self.userprofile_market = self.userprofile_market.lower()
        if not self.created_time:
            self.created_time = datetime.now()
            self.is_active=True
        if not self.profile_image:
            self.profile_image="http://beginning.wold/media/img/profile/noimg_profile.png"
        self.last_edited_time = datetime.now()
        if not self.id:
            self.id=self.user_id
            self._id='main.userprofile.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.userprofile'
            self.text=self.user_name
            self.slug=str(self.id) + '_' + slugify(self.user_name)
            self.is_confirm = False
            self.is_public=False
            self.is_job_hunting=True
            self.gender='M'
        super(UserProfile, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.user_name

    def get_dict_industries_from_csv(self):
        market_dict = dict()

        if self.invest_market_csv:
            if len(self.invest_market_csv) > 0:
                # pass #print self.invest_market_csv
                company_markets = self.invest_market_csv.split(';')
                for market in company_markets:
                    if len(market) > 1 and re.search('|',market):
                        (market_id, market_name) = market.split('|')
                        market_dict[market_id] = market_name

        return market_dict
    
    def get_dict_schools_from_csv(self):
        school_dict = dict()

        if self.university_csv:
            if len(self.university_csv) > 0:
                # pass #print self.university_csv
                universities = self.university_csv.split(';')
                for school in universities:
                    if len(school) > 1 and re.search('|',school):
                        ids = school.split('|')
                        school_id=ids[0]
                        school_name=' '.join(ids[1:len(ids)])
                        school_dict[school_id]=school_name
                        
        return school_dict


class UserDefault(DocType):
    user_id=Long()
    id=Long()
    my_id=Text()
    django_id=Text()
    company_id=Long()
    django_ct=Text()
    text=Text()
    
    
    invitation_code = Text()
    first_name = Text()
    last_name = Text()
    middle_name = Text()
    prefix = Text()
    company = Text()
    title = Text()

    user_name=Text()
    
    email_confirm_link = Text()
    email_company = Text()
    
    date_expired = Date()

    is_term_agree = Boolean()
    is_investor = Boolean()
    is_authorized_investor = Boolean()
    is_premium = Boolean()
    is_paying = Boolean()
    is_email_confirm = Boolean()

    is_product_noti = Boolean()
    is_company_noti = Boolean()
    is_admin_noti = Boolean()
    is_newsletter_noti = Boolean()
    is_public=Boolean()

    is_job_hunting = Boolean()
    is_active = Boolean()
    #is_startup = Boolean()
    is_save = Boolean()
    is_confirm = Boolean()
    is_trusted_vc = Boolean()
    is_partner = Boolean()
    is_angel = Boolean()
    is_government = Boolean()
    is_tips = Boolean()
    is_rocketpunch = Boolean()
    is_investor = Boolean()

    
    crawl_source=Text()

    # User Profile Info
    
    continent_name = Text()
    #continent=models.ForeignKey(Continent,  )
    continent_id=Integer()


    country_name = Text()
    #country=models.ForeignKey(Country,  )
    country_id=Integer()


    city_name = Text()
    #city=models.ForeignKey(City,  )
    city_id=Integer()

    
    state_name = Text()
    #state=models.ForeignKey(State,  )
    state_id=Integer()


    region_name = Text()
    #region=models.ForeignKey(Region,  )
    region_id=Integer()


    location = Text()
    location_latitude=Integer()
    location_longitude= Integer()

    phone_1_0 = Text()
    phone_1_1 = Text()
    phone_1_2 = Text()

    profile_has_image = Boolean()
    profile_image = Text()

    gender = Text()
    university = Text()
    university_csv = Text()
    major = Text()
    speciality = Text()
    interest = Text()
    industry = Text()
    website = Text()
    social_facebook = Text()
    social_twitter = Text()
    social_linkedin = Text()
    social_google = Text()
    social_blog = Text()
    social_github = Text()
    social_stack = Text()

    favorite_industry = Text()
    favorite_company = Text()

    profile_has_cv = Boolean()
    profile_cv = Text()
    profile_cv_plain = Text()
    profile_cv_mini = Text()
    profile_cv_accomplishment = Text()
    profile_cv_honor = Text()

    desired_salary = Integer()

    invest_market_csv = Text()
    profile_top_keywords = Text()
    
    last_invested_amt = Float()
    last_invested_date = Date()
    last_invested_months_ago = Integer()
    total_invested_amt = Float()
    #invested_stages=models.ForeignKey(FundingStage,  )
    invested_stages_id=Long()

    invested_stages_csv = Text()
    
    # user company info
    #owner=models.ForeignKey(User, related_name='userdefaultowner')
    owner_id=Integer()

    company_favorite_count = Integer()
    company_recommendation_count = Integer()
    partner_order = Integer()

    last_edited_time = Date()
    created_time = Date()

    company_name = Text()
    company_kor_name = Text()

    company_class = Text()
    
    tips_start_date = Date()
    rocketpunch_url = Text()

    investor_class = Text()

    company_short = Text()
    company_long = Text()

    company_industry = Text()

    company_continent = Text()
    
    company_country = Text()
        
    company_city = Text()
    
    company_state = Text()
    
    company_region = Text()
    
    company_location = Text()
    company_location_latitude=Integer()
    company_location_longitude= Integer()

    # company_region_class = ManyToManyField(Region)

    company_employee = Text()

    corporation = Text()

    company_established = Text()

    company_founded_year = Integer()

    company_founded_month = Integer()

    company_founded_day = Integer()

    company_website = Text()

    company_logo = Text()

    company_fundraising = Text()
    company_fundraising_currency = Text()
    company_fundraising_highlight = Text()
    company_fundraising_deck = Text()

    company_number = Text()
    corporate_number = Text()

    employee_total = Integer()
    employee_total_month_ago = Integer()
    employee_added_this_month = Integer()
    employee_growth_month = Integer()
    employee_total_6month_ago = Integer()
    employee_added_in_6month = Integer()
    employee_growth_6month = Integer()

    employee_added_since_funding = Integer()
    employee_months_since_funding = Integer()
    employee_growth_since_funding = Integer()

    investor_list_csv = Text()
    product_list_csv = Text()
    product_market_csv = Text()

    traffic_growth_month = Integer()
    last_funding_amt = Float()
    last_funding_date = Date()
    last_funding_months_ago = Integer()
    total_funding_amt = Float()

    #funding_stage=models.ForeignKey(FundingStage,  )

    funding_stage_id=Long()

    funding_stage_name =  Text(fields={'raw': String(index='not_analyzed')})

    product_app_store = Text()
    product_google_play = Text()

    company_top_keywords = Text()
    company_interests = Text()
    company_alerts = Text()

    traffic_monthly_unique = Integer()
    traffic_monthly_unique_week_ago = Integer()
    traffic_monthly_weekly_growth = Integer()
    traffic_monthly_unique_month_ago = Integer()
    traffic_monthly_monthly_growth = Integer()
    traffic_mobile_download = Integer()
    traffic_mobile_download_week_ago = Integer()
    traffic_mobile_download_weekly_growth = Integer()
    traffic_mobile_download_month_ago = Integer()
    traffic_mobile_download_monthly_growth = Integer()

    revenue = Float()
    total_valuation = Float()
    total_asset = Float()
    total_debt = Float()
    total_capital = Float()
    total_sales = Float()
    net_income = Float()
    operating_income = Float()
    ratio_sales_net = Float()
    ratio_sales_operating = Float()

    #investor_type=models.ForeignKey(InvestorType,  )

    investor_type_id=Long()

    investor_fund_sold_3yr = Integer()
    investor_last_funding_date = Date()
    investor_portfolio_size = Integer()
    investor_total_deals = Integer()

    #invested_stages=models.ForeignKey(FundingStage,  related_name='user_invested_stages')

    invested_stages_id=Long()

    invested_stages_csv = Text()

    score1 = Float()
    score2 = Float()
    score3 = Float()
    score4 = Float()
    score5 = Float()

    company_linkedin_page = Text()
    company_facebook_page = Text()
    company_twitter = Text()
    
    
    class Meta:
        index = myindex
    
    def save(self, *args, ** kwargs):
        # doing something strange when updating...
        #self.userdefault_market = self.userdefault_market.lower()
        if not self.created_time:
            self.created_time = datetime.now()
            self.is_active=True
        if not self.profile_image:
            self.profile_image="http://beginning.wold/media/img/profile/noimg_profile.png"
        else:
            self.company_logo=self.profile_image
        
        self.last_edited_time = datetime.now()
        if not self.id:
            self.user_name = self.first_name + '_' + self.last_name
            self.company_name=self.user_name
            self.id=self.user_id
            self._id='main.user_default.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.user_default'
            self.text=self.user_name
            self.slug=str(self.id) + '_' + slugify(self.user_name)
            self.gender='M'
            self.date_expired=datetime(2100,1,1).date() + timedelta(days=14)
            self.is_confirm = False
            self.is_public=False
            self.is_job_hunting=True
            self.company_class='Startup'
            self.is_product_noti = True
            self.is_company_noti = True
            self.is_admin_noti = True
            self.is_newsletter_noti = True
            self.is_public=False
            self.is_job_hunting = True
            self.is_active = True
            #self.is_startup = True
            
        super(UserDefault, self).save(*args, **kwargs)
        
    def get_dict_industries_from_csv(self):
        market_dict = dict()

        if self.invest_market_csv:
            if len(self.invest_market_csv) > 0:
                # pass #print self.invest_market_csv
                company_markets = self.invest_market_csv.split(';')
                for market in company_markets:
                    if len(market) > 1 and re.search('|',market):
                        (market_id, market_name) = market.split('|')
                        market_dict[market_id] = market_name

        return market_dict
    
    def market_as_list(self):
        return self.get_dict_industries_from_csv().values()
    
    def get_dict_schools_from_csv(self):
        school_dict = dict()

        if self.university_csv:
            if len(self.university_csv) > 0:
                # pass #print self.university_csv
                universities = self.university_csv.split(';')
                for school in universities:
                    if len(school) > 1 and re.search('|',school):
                        ids = school.split('|')
                        school_id=ids[0]
                        school_name=' '.join(ids[1:len(ids)])
                        school_dict[school_id]=school_name
                        
        return school_dict
    
        
    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_profile_image(self):
        return self.profile_image

    def get_dict_investors_from_csv(self):
        investor_dict = dict()

        if self.investor_list_csv:
            if len(self.investor_list_csv) > 0:
                # pass #print self.investor_list_csv
                company_investors = self.investor_list_csv.split(';')
                for investor in company_investors:
                    if len(investor) > 1:
                        (investor_id, investor_name) = investor.split('|')
                        investor_dict[investor_id] = investor_name

        return investor_dict

    def get_dict_products_from_csv(self):
        product_dict = dict()

        if self.product_list_csv:
            if len(self.product_list_csv) > 0:
                # pass #print self.product_list_csv
                product_lists = self.product_list_csv.split(';')
                for product in product_lists:
                    if len(product) > 1:
                        (product_id, product_name) = product.split('|')
                        product_dict[product_id] = product_name

        return product_dict
    
    
    def last_funding(self):
        last_funding_date = self.last_funding_date
        if last_funding_date != None and last_funding_date.year > 1999:
            # last_funding_date = last_funding_date.strftime('%Y-%m-%d')
            last_funding_date = last_funding_date.strftime('%Y-%m-%d')
        else:
            # last_funding_date = ''
            last_funding_date = ""
        # return [last_funding_date, "$%s" % intcomma(int(self.last_funding_amt))]
        return [last_funding_date, int(self.last_funding_amt)]


    def create_date_formatted(self):
        create_date = self.created_time
        if create_date != None:
            create_date = create_date.strftime('%Y-%m-%d')
        else:
            # create_date = ''
            create_date = "1900-01-01"
        return create_date
    

    
class Resource(DocType):
    #owner=models.ForeignKey(User)

    owner_id=Integer()
    id=Long()
    resource_id=Long()
    company_favorite_count = Integer()
    company_recommendation_count = Integer()
    
    resource_type=Text()
    commodity_type=Text()

    is_active = Boolean()
    is_commodity = Boolean()
    is_public = Boolean()
    is_save = Boolean()
    is_confirm = Boolean()

    is_trusted_vc = Boolean()
    is_partner = Boolean()
    is_angel = Boolean()
    
    is_government = Boolean()
    is_tips = Boolean()
    is_rocketpunch = Boolean()
    #is_startup = Boolean()
    is_investor = Boolean()
    
    
    ticker = Text()
    exchange = Text()
    sec_cik=Text()
    sec_cik_int=Text()
    partner_order = Integer()



    last_edited_time = Date()
    created_time = Date()
    
    company_name = Text()
    company_kor_name = Text()

    company_class = Text()
    tips_start_date = Date()
    rocketpunch_url = Text()
    angellist_url=Text()
    sec_url=Text()
    e27_url=Text()
    f6s_url=Text()
    forbes_url=Text()

    
    investor_class = Text()

    company_short = Text()

    company_long = Text()

    company_industry = Text()

    company_continent = Text()
    #continent=models.ForeignKey(Continent,  )
    continent_id=Integer()


    company_country = Text()
    #country=models.ForeignKey(Country,  )
    country_id=Integer()


    company_city = Text()
    #city=models.ForeignKey(City,  )
    city_id=Integer()

    
    company_state = Text()
    #state=models.ForeignKey(State,  )
    state_id=Integer()


    company_region = Text()
    #region=models.ForeignKey(Region,  )
    region_id=Integer()


    company_location = Text()
    company_location_latitude=Integer()
    company_location_longitude= Integer()

    

    company_employee = Text()

    corporation = Text()

    company_established = Text()

    company_founded_year = Integer()

    company_founded_month = Integer()

    company_founded_day = Integer()

    company_website = Text()

    company_logo = Text()
    
    company_fundraising = Text()
    company_fundraising_currency = Text()
    company_fundraising_highlight = Text()
    company_fundraising_deck = Text()

    company_number = Text()
    corporate_number = Text()

    employee_total = Integer()
    employee_total_month_ago = Integer()
    employee_added_this_month = Integer()
    employee_growth_month = Integer()
    employee_total_6month_ago = Integer()
    employee_added_in_6month = Integer()
    employee_growth_6month = Integer()

    employee_added_since_funding = Integer()
    employee_months_since_funding = Integer()
    employee_growth_since_funding = Integer()

    investor_list_csv = Text()
    product_list_csv = Text()
    product_market_csv = Text()
    invested_funding_stage_csv = Text()

    traffic_growth_month = Integer()
    last_funding_amt = Float()
    last_funding_date = Date()
    last_funding_months_ago = Integer()
    total_funding_amt = Float()

    #funding_stage=models.ForeignKey(FundingStage,  )

    funding_stage_id=Long()

    funding_stage_name =  Text(fields={'raw': String(index='not_analyzed')})

    product_app_store = Text()
    product_google_play = Text()

    company_top_keywords = Text()
    company_interests = Text()
    company_alerts = Text()

    traffic_monthly_unique = Integer()
    traffic_monthly_unique_week_ago = Integer()
    traffic_monthly_weekly_growth = Integer()
    traffic_monthly_unique_month_ago = Integer()
    traffic_monthly_monthly_growth = Integer()
    traffic_mobile_download = Integer()
    traffic_mobile_download_week_ago = Integer()
    traffic_mobile_download_weekly_growth = Integer()
    traffic_mobile_download_month_ago = Integer()
    traffic_mobile_download_monthly_growth = Integer()

    revenue = Float()
    total_valuation = Float()
    total_asset = Float()
    total_debt = Float()
    total_capital = Float()
    total_sales = Float()
    net_income = Float()
    operating_income = Float()
    ratio_sales_net = Float()
    ratio_sales_operating = Float()
    period_end_date=Date()
    
    #investor_type=models.ForeignKey(InvestorType,  )
    
    investor_type_id=Long()

    investor_fund_sold_3yr = Integer()
    investor_last_funding_date = Date()
    investor_portfolio_size = Integer()
    investor_total_deals = Integer()

    score1 = Float()
    score2 = Float()
    score3 = Float()
    score4 = Float()
    score5 = Float()

    company_linkedin_page = Text()
    company_facebook_page = Text()
    company_twitter = Text()
    
    crawl_source=Text()
    slug = Text()
    
    #invested_stages=models.ForeignKey(FundingStage,  related_name='resource_invested_stages')

    invested_stages_id=Long()

    invested_stages_csv = Text()
    invested_success = Integer()
    invested_success_amt=Float()
    invested_founder_csv= Text()
    invested_market_csv= Text()
    invested_continent_csv= Text()
    
    
    class Meta:
        index = myindex
        
        
    def save(self, *args, ** kwargs):
        if not self.created_time:
            self.created_time = datetime.now()
            self.is_active=True
        if not self.company_logo:
            self.company_logo="http://beginning.wold/media/img/company/noimg.png"
        if not self.company_class:
            self.company_class='Resource'
        self.last_edited_time = datetime.now()
        if not self.id:
            self.id=get_resource_id()
            self.resource_id=self.id
            self._id='main.resource.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.resource'
            self.text=self.company_name
            #self.is_startup=True
            self.slug=str(self.id) + '_' + slugify(self.company_name)
            self.is_active=True
            
            self.company_favorite_count = 0
            self.company_recommendation_count = 0
            self.resource_type='Energy'
            self.commodity_type='oil'
        
        super(Resource, self).save(*args, **kwargs)


        
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
        company_investors = CompanyInvestor.search().filter(owner=self).values_list(
            'investor__company_name', flat=True).distinct('investor__company_name')

        return company_investors

    def get_dict_investors_from_csv(self):
        investor_dict = dict()

        if self.investor_list_csv:
            if len(self.investor_list_csv) > 0:
                # pass #print self.investor_list_csv
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
                # pass #print self.product_market_csv
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
                # pass #print self.product_list_csv
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
            result = FinancialStatus.search().filter(company_id=self.id).exclude(
                updated_year=0, updated_month=0, updated_week=0).order_by('-updated_year', '-last_edited_time')
        except Exception as  e:
            return [0, 0, 0, 0, 0, 0, 0, 0]
        else:

            if result.count() == 0:
                return [0, 0, 0, 0, 0, 0, 0, 0]
            else:
                return [result[0].total_asset, result[0].total_debt, result[0].total_capital, result[0].total_sales, result[0].net_income, result[0].operating_income, result[0].ratio_sales_net, result[0].ratio_sales_operating]

    #def save(self, *args, **kwargs):
    #    if self.company_established != None and len(self.company_established) > 3:
    #        company_founded = dateutil.parser.parse(self.company_established)
    #        self.company_founded_year = company_founded.year
    #        self.company_founded_month = company_founded.month
    #        self.company_founded_day = company_founded.day
    #
    #    super(Company, self).save(*args, **kwargs)



class JobType(DocType):
    name = Text()
    total = Integer()
    slug = Text()
    
    created_at = Date()
    updated_at = Date()

    class Meta:
        index = myindex
        
    
    def save(self, *args, ** kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if not self.id:
            self.id=get_job_type_id()
            self._id='main.job_type.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.job_type'
            self.text=self.job_type_name
            self.slug=str(self.id) + '_' + slugify(self.name)

        if not self.total:
            self.total=1
            
        super(JobType, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return '%s' % self.name


class JobRole(DocType):
    name = Text()
    slug = Text()
    
    created_at = Date()
    updated_at = Date()

    class Meta:
        index = myindex
        
    
    def save(self, *args, ** kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if not self.id:
            self.id=get_job_role_id()
            self._id='main.job_role.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.job_role'
            self.text=self.job_role_name
            self.slug=str(self.id) + '_' + slugify(self.name)
            
        super(JobRole, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return '%s' % self.name


class JobSkill(DocType):
    name = Text()
    total = Integer()
    slug = Text()
    
    created_at = Date()
    updated_at = Date()

    class Meta:
        index = myindex
        
    
    def save(self, *args, ** kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if not self.id:
            self.id=get_job_skill_id()
            self._id='main.job_skill.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.job_skill'
            self.text=self.job_skill_name
            self.slug=str(self.id) + '_' + slugify(self.name)
            
        super(JobSkill, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return '%s' % self.name



class Job(DocType):
    #owner=models.ForeignKey(Company)
    owner_id=Integer()
    id=Long()
    my_id=Text()
    django_id=Text()
    company_id=Long()
    django_ct=Text()
    text=Text()
    
    job_id=Long()
    
    is_active = Boolean()

    is_save = Boolean()
    is_confirm = Boolean()

    last_edited_time = Date()
    created_time = Date()

    jobs_favorite_count = Integer()
    jobs_recommendation_count = Integer()

    is_private_jobs_all = Boolean()
    is_private_jobs_name = Boolean()
    jobs_name = Text()
    jobs_company_name = Text()

    is_private_country = Boolean()
    jobs_country = Text()

    is_private_city = Boolean()
    jobs_city = Text()

    jobs_type=Nested(
        doc_class=JobType,
        properties={
            'name': Text(fields={'raw': Keyword()})
        }
    )
    
    jobs_type_id=Long()


    jobs_role=Nested(
        doc_class=JobRole,
        properties={
            'name': Text(fields={'raw': Keyword()})
        }
    )
    
    jobs_role_id=Long()


    is_private_jobs_skill = Boolean()
    jobs_skill = Text()
    skills = Nested(
        doc_class=JobSkill,
        properties={
            'name': Text(fields={'raw': Keyword()})
        }
    )
    
    is_private_jobs_salary_min = Boolean()
    jobs_salary_min = Integer()

    is_private_jobs_salary_max = Boolean()
    jobs_salary_max = Integer()

    is_private_jobs_equity_min = Boolean()
    jobs_equity_min = Float()

    is_private_jobs_equity_max = Boolean()
    jobs_equity_max = Float()

    is_private_jobs_class = Boolean()
    jobs_class = Text()

    is_private_jobs_stage = Boolean()
    jobs_stage = Text()

    is_private_jobs_market = Boolean()
    jobs_market = Text()
    markets = Nested (
        doc_class=Market
        )

    is_private_jobs_posted = Boolean()
    jobs_post_year = Integer()

    is_private_jobs_post_month = Boolean()
    jobs_post_month = Integer()

    is_private_jobs_post_day = Boolean()
    jobs_post_day = Integer()

    is_private_jobs_short = Boolean()
    jobs_short = Text()

    is_private_jobs_long = Boolean()
    jobs_long = Text()

    is_private_jobs_website = Boolean()
    jobs_website = Text()
    jobs_email = Text()

    is_private_jobs_video = Boolean()
    jobs_video = Text()

    is_private_jobs_bm = Boolean()
    jobs_bm = Text()

    is_private_jobs_google_play = Boolean()
    jobs_google_play = Text()

    is_private_jobs_app_store = Boolean()
    jobs_app_store = Text()
    jobs_facebook_page = Text()

    is_private_jobs_logo = Boolean()
    jobs_logo = Text()

    is_private_jobs_screenshot = Boolean()
    jobs_screenshot_count = Integer()
    jobs_screenshot_1 = Text()
    jobs_screenshot_2 = Text()
    jobs_screenshot_3 = Text()
    jobs_screenshot_4 = Text()
    jobs_screenshot_5 = Text()
    jobs_screenshot_6 = Text()
    jobs_screenshot_7 = Text()
    jobs_screenshot_8 = Text()
    jobs_screenshot_9 = Text()
    jobs_screenshot_10 = Text()

    crawl_source = Text()

    slug = Text()
    
    
    def save(self, *args, ** kwargs):
        self.jobs_market = self.jobs_market.lower()
        self.jobs_skill = self.jobs_skill.lower()
        
        '''
        if self.owner is not None and len(self.jobs_city) < 1:
            try:
                self.jobs_city = self.owner.joblocationinfo.job_city
            except Exception as e:
                pass #print e
        if self.owner is not None and len(self.jobs_country) < 1:
            try:
                self.jobs_country = self.owner.joblocationinfo.job_country
            except Exception as e:
                pass #print e
        '''     
        if self.created_time == None:
            self.created_time = datetime.now()
        self.last_edited_time = datetime.now()

        if not self.created_time:
            self.created_time = datetime.now()
            self.is_active=True
        if not self.jobs_logo:
            self.jobs_logo="http://beginning.wold/media/img/job/noimg.png"
        self.last_edited_time = datetime.now()
        if not self.id:
            self.id=get_job_id()
            self.job_id=self.id
            self._id='main.job.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.job'
            self.text=self.jobs_name
            self.slug=str(self.id) + '_' + self.jobs_name
            
        super(Job, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return self.jobs_name

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse_lazy
        return reverse_lazy('view_job', args=[self.pk])

    def jobs_name_as_url(self):
        jobs_name = unicode(self.jobs_name).encode('ascii', 'ignore')
        jobs_url = str(jobs_name).replace('-', '--')
        jobs_url = str(jobs_name).replace('()', '')
        jobs_url = jobs_url.replace("'", "-c-")
        jobs_url = jobs_url.replace(' ', '-')
        return jobs_url

    def jobs_name_as_replaced(self):
        replaced_name = self.jobs_name.encode('utf-8')
        replaced_name = str(replaced_name).lower()
        replaced_name = replaced_name.replace("'", "")
        replaced_name = replaced_name.replace(":", "")
        return replaced_name

    def get_jobs_short_string(self):
        return self.jobs_short.encode('utf-8').lower()

    def get_similar_jobs(self):
        return SimilarJob.search().filter(owner=self)

    def skill_as_list(self):
        return self.jobs_skill.split(', ')

    def market_as_list(self):
        return self.jobs_market.split(',')

    def market_exist(self, market):
        market_lower_list = []
        market_list = self.market_as_list()
        for market_ in market_list:
            market_lower_list.append(str(market_).lower())

        if market in market_lower_list:
            return True
        else:
            return False

    def video_as_embedded(self):
        if 'youtube.com' in self.jobs_video:
            if '?v=' in self.jobs_video:
                return 'http://www.youtube.com/embed/' + self.jobs_video.split('?v=')[-1]
            else:
                return self.jobs_video
        elif 'youtu.be' in self.jobs_video:
            if '?v=' in self.jobs_video:
                return 'http://www.youtube.com/embed/' + self.jobs_video.split('?v=')[-1]
            else:
                return 'http://www.youtube.com/embed/' + self.jobs_video.split('/')[-1]
        elif 'vimeo.com' in self.jobs_video:
            return 'https://player.vimeo.com/video/' + self.jobs_video.split('/')[-1]
        elif 'youku.com' in self.jobs_video:
            split_url = self.jobs_video.split('/')[-1]
            split_url1 = split_url.split('.')[0]
            split_url2 = split_url1.split('_')[1]
            return 'http://player.youku.com/embed/%s' % split_url2
        else:
            return self.jobs_video

        
    def get_list_investors(self):
        company_investors = CompanyInvestor.search().filter(owner=self.owner).values(
            'investor__company_name', 'investor__slug').distinct()

        return company_investors

    def get_last_funded(self):
        investor = CompanyInvestor.search().filter(
            owner=self.owner).order_by('last_edited_time')

        if investor:
            if investor.last().investor_day and investor.last().investor_month and investor.last().investor_year:
                return "%s/%s/%s" % (investor.last().investor_day, investor.last().investor_month, investor.last().investor_year)
            else:
                return "-"
        else:
            return "-"

    def natural_day_added(self):
        if self.created_time == None:
            created_time = "2015-11-01 11:00:00"
            parse_created_time = datetime.strptime(
                created_time, '%Y-%m-%d %H:%M:%S')

            return naturaltime(parse_created_time)
        else:
            return naturaltime(self.created_time)

    def natural_day_posted(self):

        if self.jobs_post_year != None and self.jobs_post_month != None and self.jobs_post_day:
            date_posted = "%s-%s-%s" % (self.jobs_post_year,
                                        self.jobs_post_month, self.jobs_post_day)
            parse_date_posted = datetime.strptime(date_posted, '%Y-%m-%d')
            date_now = datetime.now().date()
            # return parse_date_posted
            MOMENT = 120

            if isinstance(parse_date_posted, datetime):
                delta = datetime.now().date() - parse_date_posted.date()
                if delta.days > 6:
                    return parse_date_posted.strftime("%b %d, %Y")
                if delta.days > 1:
                    return parse_date_posted.strftime("%A")
                elif delta.days == 1:
                    return 'yesterday'
                elif delta.seconds > 3600:
                    return str(delta.seconds / 3600) + ' hours ago'
                elif delta.seconds > MOMENT:
                    return str(delta.seconds / 60) + ' minutes ago'
                else:
                    return parse_date_posted.strftime("%b %d, %Y")
                return defaultfilters.date(parse_date_posted)
            else:
                return str(parse_date_posted)
        else:
            return "-"

    def percent_web_traffic(self):
        # last_crawler_date = alexaRank.search().order_by('last_edited_time').last().last_edited_time.date()

        # webRank = alexaRank.search().filter(website_company=self.owner, website_jobs=self).exclude(website_rank=0).exclude(updated_year=0).exclude(updated_month=0).order_by('last_edited_time')
        webRank = self.alexarank_set.exclude(
            updated_year=0, updated_month=0).order_by('last_edited_time')

        if webRank.count() > 1:

            total_count = webRank.count()

            prev_rank = int(webRank[total_count - 2].website_rank)
            curr_rank = int(webRank[total_count - 1].website_rank)

            percent = "{:.0%}".format(
                float((prev_rank - curr_rank)) / float(prev_rank) * 100.0)
            total = float((prev_rank - curr_rank)) / float(prev_rank) * 100.0
            return str(int(total)) + "%"
        else:
            return "0%"

    def ten_percent_web_traffic_in_two_weeks(self):
        # webRank = alexaRank.search().filter(website_company=self.owner,website_jobs=self).exclude(website_rank=0).exclude(updated_year=0).exclude(updated_month=0).order_by('last_edited_time')
        last_crawler_date = alexaRank.search().order_by(
            'last_edited_time').last().last_edited_time.date()
        webRank = self.alexarank_set.exclude(
            updated_year=0, updated_month=0).order_by('last_edited_time')

        if webRank.count() > 2:

            if webRank.last().last_edited_time.date() == last_crawler_date:
                total_count = webRank.count()
                this_week = int(webRank[total_count - 1].website_rank)
                previous_week = int(webRank[total_count - 2].website_rank)
                previous_previous_week = int(
                    webRank[total_count - 3].website_rank)

                if int(previous_week) > 0 and int(this_week) > 0 and int(previous_previous_week) > 0:
                    percent_1 = float((previous_week - this_week)
                                      ) / float(previous_week) * 100.0
                    percent_2 = float(
                        (previous_previous_week - previous_week)) / float(previous_previous_week) * 100.0

                    if percent_1 >= 5.0 and percent_2 >= 5.0:
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False

    def percent_fb_like(self):
        fbLike = FacebookLike.search().filter(facebook_company=self.owner, facebook_jobs=self).exclude(
            facebook_like=0).exclude(updated_year=0).exclude(updated_month=0).order_by('last_edited_time')

        if fbLike.count() > 1:
            total_count = fbLike.count()

            prev_rank = int(fbLike[total_count - 2].facebook_like)
            curr_rank = int(fbLike[total_count - 1].facebook_like)

            percent = "{:.0%}".format(
                float((curr_rank - prev_rank)) / float(prev_rank) * 100.0)
            total = float((curr_rank - prev_rank)) / float(prev_rank) * 100.0
            return str(int(total)) + "%"
        else:
            return "0%"

    def last_web_traffic_rank(self):
        return self.alexa_rank

    def last_web_traffic_rank_with_zero_callback(self):
        return self.alexa_rank

    def total_funding(self):
        funding_list = []
        usd_to_krw = Currency.search().get(currency_name='KRW').currency_price

        total_funding = 0

        investing_event_list = CompanyInvestingEvent.search().filter(
            owner=self.owner)

        for investor in investing_event_list:
            if investor.event_currency and investor.event_amount:
                if investor.event_currency == 'USD':
                    total_funding += int(investor.event_amount.replace(',', ''))
                elif investor.event_currency == 'KRW':
                    total_funding += int(investor.event_amount.replace(',',
                                                                       '').replace('-', '0')) / usd_to_krw

        return total_funding

    def get_best_all_market(self):
        list_markets = self.markets.all().values('name', 'total')

        best_market = []
        final = {}

        for market in list_markets:

            if market['name'] != "":
                result = alexaRank.search().select_related('website_jobs').filter(website_jobs_id__in=Job.search().select_related('markets').filter(markets__name=market['name']).values_list(
                    'id', flat=True)).exclude(website_rank=0).exclude(updated_year=0).exclude(updated_month=0).order_by('website_rank').values('website_rank', 'website_jobs_id')

                if result.count() > 0:
                    if result[0]['website_jobs_id'] == self.id:
                        final[market['name']] = market['total']

        if len(final) == 0:
            return [False, ""]
        else:
            sorted_final = sorted(
                final.items(), key=operator.itemgetter(1), reverse=True)
            return [True, sorted_final[0][0]]



    
class CrawledArticle(DocType):
    id=Long()
    has_intel=Boolean()
    intel_entity_json=Text()
    intel_json=Text()
    text=Text()
    
    is_save = Boolean()
    is_confirm = Boolean()
    
    #socialfeed=models.ForeignKey(SocialFeed)
    
    socialfeed_id=Long()

    
    #twitter_official_company=models.ForeignKey(Company)
    
    twitter_official_company_id=Long()

    #twitter_official_product=models.ForeignKey(Product)
    twitter_official_product_id=Long()

    
    is_tweet=Boolean()
    twitter_article_json=Text()
    twitter_article_id=Long()
    twitter_article_author=Text()
    
    article_dest_html=Text()
    article_dest_date=Date()
    
    article_media_url=Text()
    article_media_thumb=Text()
    article_media_type=Text()
    
    last_edited_time = Date()
    created_time = Date()

    from_site = Text()
    from_url = Text()
    from_location =  Text()
    from_country = Text()
    from_article_json=Text()
    from_entity_json=Text()
    is_new = Boolean()

    article_url = Text()
    article_original_url = Text()
    article_twitter_title = Text()
    article_title = Text()
    article_author = Text()
    article_author_email = Text()

    article_short = Text()
    article_date = Date()
    article_month = Integer()
    article_day = Integer()
    article_year = Integer()
    article_shared = Integer()
    article_shared_facebook = Integer()
    article_shared_twitter = Integer()
    
    
    class Meta:
        index = myindex
        
    def save(self, *args, ** kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if not self.id:
            self.id=get_crawled_article_id()
            self._id='main.crawled_article.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.crawled_article'
            self.text=self.article_title
            self.slug=str(self.id) + '_' + slugify(self.article_title)
            
        super(CrawledArticle, self).save(*args, **kwargs)


class SocialFeed(DocType):
    twitter= Text()
    twitter_name=Text()
    twitter_description= Text()
    twitter_id=Long()
    twitter_verified=Boolean()
    twitter_lang=Text()
    website= Text()
    facebook= Text()
    linkedin= Text()
    is_news=Boolean()
    is_official=Boolean()
    is_product=Boolean()
    is_company=Boolean()
    #company=models.ForeignKey(Company,)
    company_id=Long()

    #product=models.ForeignKey(Product,)
    product_id=Long()

    #user=models.ForeignKey(User,)
    user_id=Long()

    crawl_least_id=Long()
    last_crawled_unixtime=Integer()
    last_streamed_unixtime=Integer()
    is_followed= Boolean()
    followed_by= Text()
    class Meta:
        index = myindex
        
        
    def save(self, *args, ** kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if not self.id:
            self.id=get_social_feed_id()
            self._id='main.social_feed.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.social_feed'
            #self.text=self.article_title
            #self.slug=str(self.id) + '_' + slugify(self.article_title)
            
        super(SocialFeed, self).save(*args, **kwargs)

class ArticleRelation(DocType):
    #article=models.ForeignKey(CrawledArticle,)
    article_id=Long()

    #company=models.ForeignKey(Company,)
    company_id=Long()

    #product=models.ForeignKey(Product,)
    product_id=Long()

    #user=models.ForeignKey(User, related_name='article_reference_user')
    user_id=Long()

    title_match=Boolean()
    content_match=Boolean()
    last_edited_time = Date()
    created_time = Date()
    accuracy_verified=Boolean()
    #accuracy_verified_by=models.ForeignKey(User,  related_name='accuracy_verification_user')
    accuracy_verified_by_id=Long()

    is_accurate=Boolean()
    class Meta:
        index = myindex
        
        
    def save(self, *args, ** kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if not self.id:
            self.id=get_article_relation_id()
            self._id='main.article_relation.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.article_relation'
            #self.text=self.article_title
            #self.slug=str(self.id) + '_' + slugify(self.article_title)
            
        super(ArticleRelation, self).save(*args, **kwargs)
        
class PressArticle(DocType):
    #owner=models.ForeignKey(Company)
    owner_id=Integer()

    is_product = Boolean()
    #product=models.ForeignKey(Product)
    product_id=Long()


    last_edited_time = Date()
    created_time = Date()

    press_url = Text()
    press_title = Text()
    press_date = Date()
    press_month = Integer()
    press_day = Integer()
    press_year = Integer()

    class Meta:
        index = myindex
        
        
    def save(self, *args, ** kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if not self.id:
            self.id=get_press_article_id()
            self._id='main.press_article.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.press_article'
            #self.text=self.article_title
            #self.slug=str(self.id) + '_' + slugify(self.article_title)
            
        super(PressArticle, self).save(*args, **kwargs)

class MarketWatch(DocType):
    is_save=Boolean()
    is_confirm=Boolean()

    last_edited_time = Date()
    created_time = Date()

    #owner=models.ForeignKey(User)

    owner_id=Integer()

    market = Text()

    
    class Meta:
        index = myindex
        
        
    def save(self, *args, ** kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if not self.id:
            self.id=get_market_watch_id()
            self._id='main.market_watch.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.market_watch'
            #self.text=self.article_title
            #self.slug=str(self.id) + '_' + slugify(self.article_title)
            
        super(MarketWatch, self).save(*args, **kwargs)

class RecentUpdate(DocType):
    is_save=Boolean()
    is_confirm=Boolean()

    last_edited_time = Date()
    created_time = Date()

    target = Text()
    #company=models.ForeignKey(Company,  )
    company_id=Long()

    company_slug=Text()
    company_name=Text()
    #product=models.ForeignKey(Product,  )
    product_id=Long()

    product_slug=Text()
    product_name=Text()
    #user=models.ForeignKey(User,  )
    user_id=Long()

    user_slug=Text()
    user_name=Text()
    #alexa_rank=models.ForeignKey(alexaRank)
    alexa_rank_id=Long()

    #facebook_like=models.ForeignKey(FacebookLike)
    facebook_like_id=Long()

    #article=models.ForeignKey(CrawledArticle)
    article_id=Long()

    article_url = Text()
    article_title = Text()
    change = Text()
    change_percent = Text()


    class Meta:
        index = myindex
        
        
    def save(self, *args, ** kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if not self.id:
            self.id=get_recent_update_id()
            self._id='main.recent_update.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.recent_update'
            #self.text=self.article_title
            #self.slug=str(self.id) + '_' + slugify(self.article_title)
            
        super(RecentUpdate, self).save(*args, **kwargs)
        
    def percent_as_inverse_int(self):
        return -int(float(self.change_percent))

    def percent_as_int(self):
        return int(float(self.change_percent))
    
        
class UserNotification(DocType):
    id=Long()

    is_email_agree = Boolean()
    is_program_agree = Boolean()
    is_product_agree = Boolean()
    is_recruiting_agree = Boolean()
    is_management_agree = Boolean()
    class Meta:
        index = myindex


html_strip = analyzer('html_strip',
    tokenizer="standard",
    filter=["standard", "lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)

class School(DocType):
    id=Long()
    name = Text()
    city = Text()
    nation = Text()
    global_rank = Integer()
    slug =Text()
    
    created_at = Date()
    updated_at = Date()
    crawl_source=Text()

    class Meta:
        index = myindex
        
    
    def save(self, *args, ** kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if not self.id:
            self.id=get_school_id()
            self._id='main.school.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.school'
            self.text=self.school_name
            self.slug=str(self.id) + '_' + slugify(self.name)
            
        super(School, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s' % self.name



class FundingStage(DocType):
    id=Long()
    name = Text(fields={'raw': String(index='not_analyzed')})
    created_at = Date()
    updated_at = Date()
    count = Integer()
    slug=Text()
    stage_step=Integer()
    
    crawl_source=Text()

    class Meta:
        index = myindex
    
    def save(self, *args, ** kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if not self.id:
            self.id=get_funding_stage_id()
            self._id='main.funding_stage.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.funding_stage'
            self.text=self.funding_stage_name
            self.slug=str(self.id) + '_' + slugify(self.name)
            
        super(FundingStage, self).save(*args, **kwargs)


    def __unicode__(self):
        return '%s' % self.name


class InvestorType(DocType):
    id=Long()
    name = Text()
    slug = Text()
    
    created_at = Date()
    updated_at = Date()

    class Meta:
        index = myindex
    
    def save(self, *args, ** kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if not self.id:
            self.id=get_investor_type_id()
            self._id='main.investor_type.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.investor_type'
            self.slug=str(self.id) + '_' + slugify(self.name)
            
        super(InvestorType, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return '%s' % self.name


class Region(DocType):
    is_save = Boolean()
    is_confirm = Boolean()
    
    last_edited_time = Date()
    created_time = Date()

    id=Long()

    name = Text()
    slug = Text()
    latitude=Integer()
    longitude= Integer()
    
    crawl_source=Text()

    class Meta:
        index = myindex
    
    def save(self, *args, ** kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if not self.id:
            self.id=get_region_id()
            self._id='main.region.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.region'
            self.slug=str(self.id) + '_' + slugify(self.name)
            
        super(Region, self).save(*args, **kwargs)
        

class Continent(DocType):
    is_save = Boolean()
    is_confirm = Boolean()
    
    last_edited_time = Date()
    created_time = Date()

    id=Long()

    name = Text()
    slug = Text()
    latitude=Integer()
    longitude= Integer()
    
    crawl_source=Text()
    company_count= Integer()
    company_investor_count= Integer()
    company_startup_count= Integer()
    company_public_count= Integer()
    
    user_count= Integer()

    class Meta:
        index = myindex
    
    def save(self, *args, ** kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if not self.id:
            self.id=get_continent_id()
            self._id='main.continent.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.continent'
            self.slug=str(self.id) + '_' + slugify(self.name)
            
        super(Continent, self).save(*args, **kwargs)
        
class Country(DocType):
    is_save = Boolean()
    is_confirm = Boolean()
    
    last_edited_time = Date()
    created_time = Date()
    
    #continent=models.ForeignKey(Continent)
    
    continent_id=Integer()

    
    id=Long()
    name = Text()
    slug = Text()
    latitude=Integer()
    longitude= Integer()
    
    company_count= Integer()
    company_investor_count= Integer()
    company_startup_count= Integer()
    company_public_count= Integer()
    user_count= Integer()
    
    class Meta:
        index = myindex
    
    def save(self, *args, ** kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if not self.id:
            self.id=get_country_id()
            self._id='main.country.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.country'
            self.slug=str(self.id) + '_' + slugify(self.name)
            
        super(Country, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return str(self.name)

    
class State(DocType):
    is_save = Boolean()
    is_confirm = Boolean()
    
    last_edited_time = Date()
    created_time = Date()

    #continent=models.ForeignKey(Continent)

    id=Long()
    continent_id=Integer()

    #country=models.ForeignKey(Country)
    country_id=Integer()

    
    name = Text()
    latitude=Integer()
    longitude= Integer()

    class Meta:
        index = myindex
    
    def save(self, *args, ** kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if not self.id:
            self.id=get_state_id()
            self._id='main.state.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.state'
            self.slug=str(self.id) + '_' + slugify(self.name)
            
        super(State, self).save(*args, **kwargs)

class City(DocType):
    is_save = Boolean()
    is_confirm = Boolean()

    last_edited_time = Date()
    created_time = Date()

    #continent=models.ForeignKey(Continent)

    continent_id=Integer()

    #country=models.ForeignKey(Country)
    country_id=Integer()

    #state=models.ForeignKey(State,  )
    state_id=Integer()

    id=Long()
    name = Text()
    latitude=Integer()
    longitude= Integer()

    class Meta:
        index = myindex
    
    def save(self, *args, ** kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if not self.id:
            self.id=get_city_id()
            self._id='main.city.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.city'
            self.slug=str(self.id) + '_' + slugify(self.name)
            
        super(City, self).save(*args, **kwargs)

class CrawlLocationSearch(DocType):
    is_save = Boolean()
    is_confirm = Boolean()

    last_edited_time = Date()
    created_time = Date()

    name = Text()
    
    continent_name = Text()
    #continent=models.ForeignKey(Continent,  )
    continent_id=Integer()


    country_name = Text()
    #country=models.ForeignKey(Country,  )
    country_id=Integer()


    city_name = Text()
    #city=models.ForeignKey(City,  )
    city_id=Integer()

    
    state_name = Text()
    #state=models.ForeignKey(State,  )
    state_id=Integer()


    region_name = Text()
    #region=models.ForeignKey(Region,  )
    region_id=Integer()


    location_name = Text()
    location_latitude=Integer()
    location_longitude= Integer()

    crawl_source=Text()

    class Meta:
        index = myindex


class ResourceContinent(DocType):
    is_save = Boolean()
    is_confirm = Boolean()

    last_edited_time = Date()
    created_time = Date()

    #continent=models.ForeignKey(Continent)

    continent_id=Integer()

    id=Long()
    
    name = Text()
    slug=Text()
    latitude=Integer()
    longitude= Integer()
    
    crawl_source=Text()
    
    updated_date=Date()
    #resource=models.ForeignKey(Resource)
    resource_id=Long()

    resource_type=Text()
    commodity_type=Text()
    
    production= Float()
    consumption= Float()
    pct_resource= Float()
    production= Float()
    import_usd= Float()
    export_usd= Float()
    import_qty= Float()
    export_qty= Float()
    
    class Meta:
        index = myindex
    
    def save(self, *args, ** kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if not self.id:
            self.id=get_resource_continent_id()
            self._id='main.resource_continent.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.resource_continent'
            self.slug=str(self.id) + '_' + slugify(self.name)
            
        super(ResourceContinent, self).save(*args, **kwargs)

class ResourceContinentStatus(DocType):
    is_save = Boolean()
    is_confirm = Boolean()

    last_edited_time = Date()
    created_time = Date()

    #continent=models.ForeignKey(Continent)

    continent_id=Integer()

    id=Long()
    name = Text()
    latitude=Integer()
    longitude= Integer()
    
    crawl_source=Text()
    
    
    updated_date=Date()
    #resource=models.ForeignKey(Resource)
    resource_id=Long()

    resource_type=Text()
    commodity_type=Text()
    
    production= Float()
    consumption= Float()
    pct_resource= Float()
    production= Float()
    import_usd= Float()
    export_usd= Float()
    import_qty= Float()
    export_qty= Float()

    class Meta:
        index = myindex
    
    def save(self, *args, ** kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if not self.id:
            self.id=get_resource_continent_status_id()
            self._id='main.resource_continent_status.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.resource_continent_status'
            self.slug=str(self.id) + '_' + slugify(self.name)
            
        super(ResourceContinentStatus, self).save(*args, **kwargs)

class ResourceCountry(DocType):
    is_save = Boolean()
    is_confirm = Boolean()

    last_edited_time = Date()
    created_time = Date()
    
    #continent=models.ForeignKey(Continent)
    
    continent_id=Integer()

    #country=models.ForeignKey(Country)
    country_id=Integer()

    continent_name=Text()
    name = Text()
    latitude=Integer()
    longitude= Integer()

    updated_date=Date()
    #resource=models.ForeignKey(Resource)
    resource_id=Long()

    resource_type=Text()
    commodity_type=Text()
    
    production= Float()
    consumption= Float()
    pct_total_production= Float()
    pct_total_consumption= Float()
    total_resource_type_production= Float()
    total_resource_type_consumption= Float()
    import_usd= Float()
    export_usd= Float()
    import_qty= Float()
    export_qty= Float()
    
    def __unicode__(self):
        return str(self.name)

    class Meta:
        index = myindex
    
    def save(self, *args, ** kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if not self.id:
            self.id=get_resource_country_id()
            self._id='main.resource_country.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.resource_country'
            self.slug=str(self.id) + '_' + slugify(self.name)
            
        super(ResourceCountry, self).save(*args, **kwargs)

class ResourceCountryStatus(DocType):
    is_confirm = Boolean()

    is_save = Boolean()
    last_edited_time = Date()
    created_time = Date()
    
    #continent=models.ForeignKey(Continent)
    
    continent_id=Integer()

    #country=models.ForeignKey(Country)
    country_id=Integer()

    
    continent_name=Text()
    name = Text()
    latitude=Integer()
    longitude= Integer()

    updated_date=Date()
    #resource=models.ForeignKey(Resource)
    resource_id=Long()

    resource_type=Text()
    commodity_type=Text()
    
    production= Float()
    consumption= Float()
    pct_total_production= Float()
    pct_total_consumption= Float()
    import_usd= Float()
    export_usd= Float()
    import_qty= Float()
    export_qty= Float()
    
    def __unicode__(self):
        return str(self.name)
    
    class Meta:
        index = myindex
    
    def save(self, *args, ** kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if not self.id:
            self.id=get_resource_country_status_id()
            self._id='main.resource_country_status.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.resource_country_status'
            self.slug=str(self.id) + '_' + slugify(self.name)
            
        super(ResourceCountryStatus, self).save(*args, **kwargs)
    

class MarketDict(DocType):
    name = Text()
    category_level1 = Text()
    category_level2 = Text()
    category_level3 = Text()
    total = Integer()
    slug = Text()
    created_at = Date()
    updated_at = Date()
    crawl_source=Text()
    
    class Meta:
        index = myindex
    
    def save(self, *args, ** kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if not self.id:
            self.id=get_market_dict_id()
            self._id='main.market_dict.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.market_dict'
            self.slug=str(self.id) + '_' + slugify(self.name)
            
        super(MarketDict, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return '%s' % self.name

        
class MarketCount(DocType):
    name = Text()
    #market=models.ForeignKey(Market,  )
    market_id=Long()
    market_name=Text()
    
    count_type=Text()
    
    continent_name = Text()
    #continent=models.ForeignKey(Continent,  )
    continent_id=Integer()


    country_name = Text()
    #country=models.ForeignKey(Country,  )
    country_id=Integer()

    
    company_count = Integer()
    investor_count = Integer()
    startup_count = Integer()
    public_count = Integer()
    product_count = Integer()
    user_count = Integer()
    
    created_at = Date()
    updated_at = Date()
    crawl_source=Text()

    class Meta:
        index = myindex
    
    def save(self, *args, ** kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if not self.market_name and self.market_id:
            markets=Market.search().filter('term',id=self.market_id).execute()
            if markets and len(markets) > 0:
                self.market_name=markets[0].name
                
        if not self.id:
            self.id=get_market_count_id()
            self._id='main.market_count.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.market_count'
            self.slug=str(self.id) + '_' + slugify(self.name)
            
        super(MarketCount, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return '%s' % self.name

   
class UserRanking(DocType):
    last_edited_time = Date()
    created_time = Date(
         editable=True)
    #user=models.ForeignKey(User,  )
    user_id=Long()

    #market=models.ForeignKey(Market,  )
    market_id=Long()


    total_amount_invested=Integer()
    total_investments=Integer()
    total_exits=Integer()
    total_wins=Integer()
    total_losses=Integer()
    invest_accuracy=Integer()
    
    market_rank = Integer()
    is_best_in_market = Boolean()
    alexa_rank = Integer()
    facebook_like = Integer()
    facebook_talking = Integer()

class Program(DocType):
    #owner=models.ForeignKey(Company)
    owner_id=Integer()


    is_save = Boolean()
    is_confirm = Boolean()

    last_edited_time = Date()
    created_time = Date()
    program_favorite_count = Integer()
    program_recommendation_count = Integer()

    is_private_program_all = Boolean()

    is_private_program_image = Boolean()
    program_image = Text(
        upload_to='img/investment', )

    is_private_program_description = Boolean()
    program_description = Text()

    is_private_program_deadline_year = Boolean()
    program_deadline_year = Integer()

    is_private_program_deadline_month = Boolean()
    program_deadline_month = Integer()

    is_private_program_deadline_day = Boolean()
    program_deadline_day = Integer()

    is_private_program_investment_size = Boolean()
    program_investment_size_start = Text()
    program_investment_size_end = Text()

    is_private_program_target = Boolean()
    program_target = Text()

    is_private_program_target_country = Boolean()
    program_target_country = Text()

    class Meta:
        index = myindex

    def __unicode__(self):
        return self.owner.company_name

class Location(DocType):
    last_edited_time = Date()
    created_time = Date()
    
    continent_name = Text()
    #continent=models.ForeignKey(Continent,  )
    continent_id=Integer()


    country_name = Text()
    #country=models.ForeignKey(Country,  )
    country_id=Integer()


    city_name = Text()
    #city=models.ForeignKey(City,  )
    city_id=Integer()

    
    state_name = Text()
    #state=models.ForeignKey(State,  )
    state_id=Integer()


    region_name = Text()
    #region=models.ForeignKey(Region,  )
    region_id=Integer()


    location = Text()
    location_latitude=Integer()
    location_longitude= Integer()
    
    class Meta:
        index = myindex



class alexaRank(DocType):
    is_save = Boolean()
    is_confirm = Boolean()
    
    last_edited_time = Date()
    created_time = Date()
    updated_year = Integer()
    updated_month = Integer()
    updated_week = Integer()

    website = Text()
    #website_company=models.ForeignKey(Company)
    website_company_id=Long()

    #website_product=models.ForeignKey(Product)
    website_product_id=Long()

    website_rank = Integer()

    class Meta:
        index = myindex

        
        
    def save(self, *args, ** kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()

        #if not self.id:
        #    self.id=get_alexa_rank_id()
        #    self._id='main.alexa_rank.' + str(self.id)
        #    self.my_id=self._id
        #    self.django_id=str(self.id)
        #    self.django_ct='main.alexa_rank'
        #    #self.text=self.article_title
        #    #self.slug=str(self.id) + '_' + slugify(self.article_title)
            
        super(alexaRank, self).save(*args, **kwargs)
        
class FacebookLike(DocType):
    facebook_company_id=Long()
    facebook_product_id=Long()

    is_save=Boolean()
    is_confirm=Boolean()

    last_edited_time = Date()
    created_time = Date()
    updated_year = Integer()
    updated_month = Integer()
    updated_week = Integer()

    facebook_page = Text()
    #facebook_company=models.ForeignKey(Company)

    #facebook_product=models.ForeignKey(Product)

    facebook_like = Integer()
    
    class Meta:
        index = myindex

    def save(self, *args, ** kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()

        super(FacebookLike, self).save(*args, **kwargs)

class FacebookTalking(DocType):
    is_save = Boolean()
    is_confirm = Boolean()

    last_edited_time = Date()
    created_time = Date()
    updated_year = Integer()
    updated_month = Integer()
    updated_week = Integer()

    facebook_page = Text()
    #facebook_company=models.ForeignKey(Company)
    facebook_company_id=Long()

    #facebook_product=models.ForeignKey(Product)
    facebook_product_id=Long()

    facebook_talking = Integer()

    class Meta:
        index = myindex

    def save(self, *args, ** kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()

        super(FacebookTalking, self).save(*args, **kwargs)


class ProductRanking(DocType):
    last_edited_time = Date()
    created_time = Date()
    #product=models.ForeignKey(Product,  )
    product_id=Long()

    #market=models.ForeignKey(Market,  )
    market_id=Long()


    market_rank = Integer()
    is_best_in_market = Boolean()
    alexa_rank = Integer()
    facebook_like = Integer()
    facebook_talking = Integer()

    class Meta:
        index = myindex

    def save(self, *args, ** kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()

        super(ProductRanking, self).save(*args, **kwargs)



class CompanyMember(DocType):
    #owner=models.ForeignKey(Company)
    owner_id=Integer()


    last_edited_time = Date()
    created_time = Date()

    is_user_company_current = Text()
    user_company_start_month = Integer()
    user_company_start_year = Integer()
    user_company_end_month = Integer()
    user_company_end_year = Integer()

    #user=models.ForeignKey(User,  )  # 

    user_id=Long()

    user_char_id = Text()
    user_name = Text()
    user_title = Text()
    user_role = Text()

    is_user_input = Boolean()
    is_user_contact = Boolean()
    #user_contact_target=models.ForeignKey(Product,  )
    user_contact_target_id=Long()

    crawl_source=Text()

    class Meta:
        index = myindex

    def save(self, *args, ** kwargs):
        if self.created_time == None:
            self.created_time = datetime.now()
        self.last_edited_time  = datetime.now()
        super(CompanyMember, self).save(*args, **kwargs)


class CompanyPortfolio(DocType):
    #owner=models.ForeignKey(Company)
    owner_id=Integer()

    id=Long()

    last_edited_time = Date()
    created_time = Date()

    portfolio_company_id = Text()
    portfolio_company_name = Text()
    #investee=models.ForeignKey(Company, related_name='+')
    investee_id=Long()

    portfolio_day = Integer()
    portfolio_month = Integer()
    portfolio_year = Integer()
    portfolio_amount = Text()
    crawl_source=Text()
    
    class Meta:
        index = myindex
    
    def save(self, *args, ** kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()

        
        if not self.id:
            self.id=get_company_portfolio_id()
            self._id='main.company_portfolio.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.company_portfolio'
            #self.slug=str(self.id) + '_' + slugify(self.name)
            
        super(CompanyPortfolio, self).save(*args, **kwargs)

class CompanyInvestor(DocType):
    #owner=models.ForeignKey(Company)
    owner_id=Integer()
    owner_name=Text()
    
    #investor=models.ForeignKey(Company, related_name='+')
    investor_id=Long()
    investor_name=Text()
    
    id=Long()
    last_edited_time = Date(
        'date edited',  )
    created_time = Date()

    is_user_input = Boolean()

    #funding_stage=models.ForeignKey(FundingStage,  )

    funding_stage_id=Integer()
    funding_stage_name= Text(fields={'raw': String(index='not_analyzed')})


    # null
    investor_day = Integer()
    investor_month = Integer()
    investor_year = Integer()
    investor_currency = Text()
    investor_amount = Text()
    
    # cleaned
    invest_currency = Text()
    invest_amt = Float()
    invest_date=Date()
    
    is_active = Boolean()
    is_tips = Boolean()
    is_rocketpunch = Boolean()
    is_estimate=Boolean()
    crawl_source=Text()
    
    class Meta:
        index = myindex
    
    def save(self, *args, ** kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if not self.funding_stage_name and self.funding_stage_id:
            funding_list=FundingStage.search().filter('term',id=self.funding_stage_id).execute()
            if funding_list and len(funding_list) > 0:
                self.funding_stage_name=funding_list[0].name
                
        if not self.owner_name and self.owner_id:
            company_list=Company.search().filter('term',id=self.owner_id).execute()
            if company_list and len(company_list) > 0:
                self.owner_name=company_list[0].company_name
                self.owner_short=company_list[0].company_short
                self.owner_score1=company_list[0].score1
                self.owner_score2=company_list[0].score2
                self.owner_score3=company_list[0].score3
        if not self.investor_name and self.investor_id:
            company_list=Company.search().filter('term',id=self.investor_id).execute()
            if company_list and len(company_list) > 0:
                self.investor_name=company_list[0].company_name
                self.investor_short=company_list[0].company_short
                self.investor_score1=company_list[0].score1
                self.investor_score2=company_list[0].score2
                self.investor_score3=company_list[0].score3
                
        if not self.id:
            self.id=get_company_investor_id()
            self._id='main.company_investor.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.company_investor'
            self.slug=str(self.id) + '_' + slugify(self.name)
            
        super(CompanyInvestor, self).save(*args, **kwargs)
        

    def __repr__(self):
        return ''
    
    def __str__(self):
        return self.__repr__()
    
    def __unicode__(self):
        return self.__repr__()



'''
properties={
     'investor_name' :  Text(fields={'raw': String(index='not_analyzed')}),
     'investor_id' : Integer(),
     'invest_amt' : Float(),
}
'''
class CompanyInvestingEvent(DocType):
    #owner=models.ForeignKey(Company)
    owner_id=Integer()
    owner_name=Text()
    
    id=Long()
    


    investor = Nested(
            doc_class=CompanyInvestor,
            
    )
    

    funding_stage_id=Integer()
    funding_stage_name= Text(fields={'raw': String(index='not_analyzed')})
    event_round = Text()
    
    event_investors = Text()
    event_investors_id = Text()

    last_edited_time = Date(
        'date edited',  )
    created_time = Date()

    is_user_input = Boolean()
    is_tips = Boolean()
    is_rocketpunch = Boolean()

    event_day = Integer()
    event_month = Integer()
    event_year = Integer()
    event_currency = Text()
    event_amount = Text()
    
    # cleaned
    invest_currency = Text()
    invest_amt = Float()
    invest_date=Date()
    
    crawl_source=Text()
    
    class Meta:
        index = myindex
    
    def save(self, *args, ** kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        
        if not self.funding_stage_name and self.funding_stage_id:
            funding_list=FundingStage.search().filter('term',id=self.funding_stage_id).execute()
            if funding_list and len(funding_list) > 0:
                self.funding_stage_name=funding_list[0].name
                self.event_round=self.funding_stage_name
        

        if not self.owner_name and self.owner_id:
            company_list=Company.search().filter('term',id=self.owner_id).execute()
            if company_list and len(company_list) > 0:
                self.owner_name=company_list[0].company_name
                self.owner_short=company_list[0].company_short
                self.owner_score1=company_list[0].score1
                self.owner_score2=company_list[0].score2
                self.owner_score3=company_list[0].score3
                
        if not self.investor:
            self.investor=[]
            
        if not self.id:
            self.id=get_company_investing_event_id()
            self._id='main.company_investing_event.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.company_investing_event'
            #self.slug=str(self.id) + '_' + slugify(self.name)
            
        super(CompanyInvestingEvent, self).save(*args, **kwargs)
    
    
    def __repr__(self):
        try:
            #return '{ "date":"%s", "open":%s, "high":%s, "low":%s, "close":%s,"volume":%s }' % (self.date, self.open, self.high, self.low, self.close, self.volume)
            return '{ "date":"%s", "company":%s, "investor":%s, "funding_stage":%s, "invest_date":%s, "invest_currency":%s, "invest_amt":%s }' % \
                (self.created_time, self.owner,  self.investor,  self.funding_stage,  self.invest_date, self.invest_currency, self.invest_amt)
        except Exception as e:
            pass #print e
        return ''
    
    def __str__(self):
        return self.__repr__()
    
    def __unicode__(self):
        return self.__repr__()


class Currency(DocType):
    last_edited_time = Date(
        'date edited',  )
    currency_name = Text()
    currency_price = Float()

    class Meta:
        index = myindex

class CurrencyConversion(DocType):
    last_edited_time = Date(
        'date edited',  )
    from_currency_name = Text()
    to_currency_name = Text()
    from_currency_price = Float()
    to_currency_price = Float()

    class Meta:
        index = myindex


class ApplicationGooglePlayCrawlList(DocType):
    app_id = Text() 
    app_url = Text() 
    link = Text() 
    item_name = Text() 
    updated = Text() 
    author = Text() 
    filesize = Text() 
    downloads = Text() 
    version = Text() 
    compatibility = Text() 
    content_rating = Text() 
    author_link = Text() 
    genre = Text() 
    price = Text() 
    rating_value = Text() 
    review_number = Text() 
    description = Text() 
    iap = Text() 
    developer_badge = Text() 
    physical_address = Text() 
    video_url = Text() 
    developer_id = Text() 
    crawled = Boolean()
    class Meta:
        index = myindex
      
class ApplicationCrawlList(DocType):
    last_edited_time = Date()
    created_time = Date()

    app_url = Text()
    crawled = Boolean()
    
    crawl_source=Text()
    class Meta:
        index = myindex

      
class ApplicationInfo(DocType):
    last_edited_time = Date()
    created_time = Date()

    #company=models.ForeignKey(Company,  )

    company_id=Long()

    #product=models.ForeignKey(Product,  )
    product_id=Long()


    platform = Text()
    app_name = Text()
    app_developer = Text()
    app_developer_url = Text()
    app_developer_id= Text()
    app_numeric_id= Text()
    app_id= Text()
    app_url = Text()
    app_icon= Text()
    is_free=Boolean()
    price=Float()
    
    
    updated_date = Date()
    released_date = Date()
    
    rank_all = Integer()
    rank_grossing = Integer()
    rank_min = Integer()
    rating_number = Integer()
    rating = Float()
    installation_number = Text()
    active_user = Integer()
    
    crawl_source=Text()
    class Meta:
        index = myindex
        
class ApplicationStatus(DocType):
    is_save=Boolean()
    is_confirm=Boolean()
    last_edited_time = Date()
    created_time = Date()

    updated_year = Integer()
    updated_month = Integer()
    updated_week = Integer()

    #product=models.ForeignKey(Product,  )

    product_id=Long()


    platform = Text()
    app_name = Text()
    app_developer = Text()
    updated_date = Date()
    released_date = Date()
    rank_all = Integer()
    rank_grossing = Integer()
    rank_min = Integer()
    rating_number = Integer()
    rating = Float(.0)
    installation_number = Text()
    active_user = Integer()
    crawl_source=Text()
    class Meta:
        index = myindex

class EmployeeStatus(DocType):
    is_save=Boolean()
    is_confirm=Boolean()
    last_edited_time = Date()
    created_time = Date()

    is_kreditdata = Boolean()

    updated_year = Integer()
    updated_month = Integer()
    updated_week = Integer()
    

    #company=models.ForeignKey(Company)
    company_id=Long()


    employee = Integer()
    new_employee = Integer()
    left_employee = Integer()
    
    updated_date = Date()
    currency = Text()

    salary = Float()

    crawl_source=Text()

    class Meta:
        index = myindex


class FinancialStatus(DocType):
    is_save=Boolean()
    is_confirm=Boolean()
    last_edited_time = Date()
    created_time = Date()
    
    updated_year = Integer()
    updated_month = Integer()
    updated_day = Integer()
    updated_week = Integer()

    period_end_date=Date()
    #company=models.ForeignKey(Company)
    company_id=Long()

    currency=Text()
    total_asset = Float()
    total_debt = Float()
    total_capital = Float()
    total_sales = Float()
    net_income = Float()
    operating_income = Float()
    ratio_sales_net = Float()
    ratio_sales_operating = Float()

    class Meta:
            index = myindex
            
            
class BannerList(DocType):
    #user=models.ForeignKey(User,   )
    user_id=Long()

    name = Text()
    html = Text()
    banner_pic = Text()
    preview_pic = Text()
    slug = Text()
    is_public = Boolean()
    created_at = Date()
    updated_at = Date()
    class Meta:
        index = myindex

    def __unicode__(self):
        return '%s' % self.name

    def save(self, *args, **kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if not self.slug:
            self.slug=str(self.user_id) + '_' + slugify(self.name)
            pass #print self.slug
            
        if not self.id:
            self.id=get_banner_list_id()
            self._id='main.banner_list.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.banner_list'
            
        
        super(BannerList, self).save(*args, **kwargs)
        
class CategoryList(DocType):
    #user=models.ForeignKey(User,   )
    user_id=Long()

    name = Text()
    slug = Text()
    is_public = Boolean()
    created_at = Date()
    updated_at = Date()

    class Meta:
        index = myindex

    def __unicode__(self):
        return '%s' % self.name

    def save(self, *args, **kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if not self.slug:
            self.slug=str(self.user_id) + '_' + slugify(self.name)
            pass #print self.slug
            
        if not self.id:
            self.id=get_category_list_id()
            self._id='main.category_list.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.category_list'
            
            
        super(CategoryList, self).save(*args, **kwargs)


class ProductCategoryList(DocType):
    #category_list=models.ForeignKey(CategoryList,  )
    category_list_id=Long()

    category_list_slug = Text()
    #product=models.ForeignKey(Product,  )
    product_id=Long()

    #company=models.ForeignKey(Company,  )
    company_id=Long()

    created_at = Date()
    updated_at = Date()

    class Meta:
        index = myindex
    def __unicode__(self):
        return '%s' % self.category_list

    def from_user(self):
        return '%s' % self.category_list.user

    def save(self, *args, **kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if self.company_id == None:
            self.company_id=self.product.owner_id
        if self.category_list_slug == None:
            self.category_list_slug=self.category_list.slug
        cc_list=CompanyCategoryList.search().filter(category_list_id=self.category_list_id).filter(company_id=self.company_id)
        if cc_list.count() < 1:
            cc=CompanyCategoryList()
            cc.category_list_id=self.category_list_id
            cc.category_list_slug=self.category_list_slug
            cc.company_id=self.company_id
            cc.save()
        
        if not self.id:
            self.id=get_product_category_list_id()
            self._id='main.product_category_list.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.product_category_list'
            
        super(ProductCategoryList, self).save(*args, **kwargs)


class CompanyCategoryList(DocType):
    #category_list=models.ForeignKey(CategoryList,  )
    category_list_id=Long()

    category_list_slug = Text()
    #company=models.ForeignKey(Company,  )
    company_id=Long()

    created_at = Date()
    updated_at = Date()

    def __unicode__(self):
        return '%s' % self.category_list

    class Meta:
        index = myindex

    def save(self, *args, **kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if self.category_list_slug == None:
            self.category_list_slug=CategoryList.search().get(id=self.category_list_id).slug

        if not self.id:
            self.id=get_company_category_list_id()
            self._id='main.company_category_list.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.company_category_list'
            
        super(CompanyCategoryList, self).save(*args, **kwargs)

class SimilarJob(DocType):
    #owner=models.ForeignKey(Job)
    owner_id=Integer()

    #target=models.ForeignKey(Job, related_name='+')
    target_id=Long()


    last_edited_time = Date()
    created_time = Date()

    is_user_input = Boolean()


class UserDefaultView(DocType):
    #user=models.ForeignKey(User)
    user_id=Long()

    name=Text()
    order_by=Text()
    column_1 = Boolean()
    column_2 = Boolean()
    column_3 = Boolean()
    column_4 = Boolean()
    column_5 = Boolean()
    column_6 = Boolean()
    column_7 = Boolean()
    column_8 = Boolean()
    column_9 = Boolean()
    column_10 = Boolean()
    column_11 = Boolean()
    column_12 = Boolean()
    column_13 = Boolean()
    column_14 = Boolean()
    column_15 = Boolean()
    column_16 = Boolean()
    column_17 = Boolean()
    column_18 = Boolean()
    column_19 = Boolean()
    column_20 = Boolean()
    column_21 = Boolean()
    column_22 = Boolean()
    column_23 = Boolean()
    column_24 = Boolean()
    column_25 = Boolean()
    column_26 = Boolean()
    column_27 = Boolean()
    column_28 = Boolean()
    column_29 = Boolean()
    column_30 = Boolean()
    column_31 = Boolean()
    column_32 = Boolean()
    column_33 = Boolean()
    column_34 = Boolean()
    column_35 = Boolean()
    column_36 = Boolean()
    column_37 = Boolean()
    column_38 = Boolean()
    column_39 = Boolean()
    column_40 = Boolean()
    column_41 = Boolean()
    column_42 = Boolean()
    column_43 = Boolean()
    column_44 = Boolean()
    column_45 = Boolean()
    column_46 = Boolean()
    column_47 = Boolean()
    column_48 = Boolean()
    column_49 = Boolean()
    column_50 = Boolean()
    column_51 = Boolean()
    column_52 = Boolean()
    column_53 = Boolean()
    column_54 = Boolean()
    column_55 = Boolean()
    column_56 = Boolean()
    column_57 = Boolean()
    column_58 = Boolean()
    column_59 = Boolean()
    column_60 = Boolean()
    column_61 = Boolean()
    column_62 = Boolean()

    created_at = Date()
    updated_at = Date()

    class Meta:
        index = myindex
        
    def __unicode__(self):
        return '%s' % self.user

    def as_array(self):
        result = []
        for val in range(1, 62):
            try:
                value = getattr(self, "column_%d"%val)
            except AttributeError as e:
                pass #print e.message
                value = False
            result.append(str(value).lower())
        return result


class ConnectWithTeam(DocType):
    #sender=models.ForeignKey(User,  related_name="sender")
    sender_id=Long()

    #receiver=models.ForeignKey(User,  related_name="receiver")
    receiver_id=Long()

    #company=models.ForeignKey(Company)
    company_id=Long()

    from_user = Text()
    subject = Text()
    message = Text()
    created_time = Date()
    updated_time = Date()

    class Meta:
        index = myindex
        
    def __unicode__(self):
        return "sender : %s / receiver : %s" % (self.sender, self.receiver)


class Interest(DocType):
    #from_company=models.ForeignKey(
    from_company_id=Long()

    #Company, related_name='interest_from_company')
    #from_user=models.ForeignKey(User, related_name='interest_from_user')
    from_user_id=Long()

    #to_company=models.ForeignKey(
    to_company_id=Long()

    #Company,  related_name='interest_to_company')
    #to_user=models.ForeignKey(User,  related_name='interest_to_user')
    to_user_id=Long()

    #job=models.ForeignKey(Job)
    job_id=Long()

    name = Text()
    slug = Text()
    
    created_at = Date()
    updated_at = Date()
    is_mutual = Boolean()

    class Meta:
        index = myindex
        
    def __unicode__(self):
        return '%s' % self.name

    def save(self, *args, **kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        super(Interest, self).save(*args, **kwargs)

class InterestUser(DocType):
    #category_list=models.ForeignKey(CategoryList,  )
    category_list_id=Long()

    #from_user=models.ForeignKey(User, related_name='interest_user_from_user')
    from_user_id=Long()

    #to_user=models.ForeignKey(User,  related_name='interest_user_to_user')
    to_user_id=Long()

    created_at = Date()
    updated_at = Date()

    
    class Meta:
        index = myindex
    def __unicode__(self):
        return '%s' % self.to_user

    def save(self, *args, **kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        super(InterestUser, self).save(*args, **kwargs)


class Syndicate(DocType):
    
    #user=models.ForeignKey(User, related_name='founder_user_id',             )
    id=Long()
    user_id=Long()

    #company=models.ForeignKey(Company, related_name='founder_company_id',       )
    company_id=Long()

    #recipient=models.ForeignKey(Company, related_name='recipient_company_id',     )
    recipient_id=Long()


    deal_type = Text( )
    
    amount = Text()
    terms = Text()

    last_edited_time = Date()
    created_time = Date()

    invest_date = Date()
    
    last_edited_time = Date()
    created_time = Date()

    carry_per_deal = Float()
    deals_per_year = Integer()
    typical_investment_amt = Float()
    minimum_investment_amt = Float()

     # CV
    profile_has_cv = Boolean()
    profile_cv = Text()
    profile_cv_plain = Text()
    profile_cv_mini = Text()
    profile_cv_accomplishment = Text()
    profile_cv_honor = Text()
    
    # Note
    profile_has_note = Boolean()
    profile_note = Text()
    profile_note_plain = Text()
    profile_note_sharing = Text()
    
    is_founder = Boolean()
    is_ongoing = Boolean()
    is_private = Boolean()
    is_lead_private = Boolean()
    
    class Meta:
        index = myindex

    def save(self, *args, **kwargs):
        if self.created_time == None:
            self.created_time = datetime.now()
        self.last_edited_time = datetime.now()
        
        if not self.id:
            self.id=get_syndicate_id()
            self._id='main.syndicate.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.syndicate'
            
        super(Syndicate, self).save(*args, **kwargs)


class SyndicateProduct(DocType):
    #syndicate_founders_apply_id=models.ForeignKey(Syndicate)
    syndicate_founders_apply_id=Long()

    #product=models.ForeignKey(Product)
    product_id=Long()


    class Meta:
        index = myindex

class SyndicateCompany(DocType):
    #syndicate_founders_apply_id=models.ForeignKey(Syndicate)
    syndicate_founders_apply_id=Long()

    #company=models.ForeignKey(Company)
    company_id=Long()

    class Meta:
        index = myindex

class SyndicateAccepted(DocType):
    #syndicate=models.ForeignKey(
    syndicate_id=Long()

    #    Syndicate,  )
    #user=models.ForeignKey(User,  )
    user_id=Long()

    last_edited_time = Date()
    created_time = Date()

    class Meta:
        index = myindex
    
class SyndicateIntroAccepted(DocType):
    #syndicate=models.ForeignKey(
    syndicate_id=Long()

    #Syndicate,  )
    #user=models.ForeignKey(User,  )
    user_id=Long()


    last_edited_time = Date()
    created_time = Date()
    
    class Meta:
        index = myindex
        
class SyndicateMember(DocType):
    #syndicate=models.ForeignKey(
    syndicate_id=Long()

    #Syndicate, related_name='lead_syndicate')
    #user=models.ForeignKey(User,  )
    user_id=Long()

    #syndicate_member = models.ForeignKey(
    #    Syndicate, related_name='member_syndicate')
    
    last_edited_time = Date()
    created_time = Date()

    class Meta:
        index = myindex
        
class SyndicateDeal(DocType):
    #application=models.ForeignKey(Syndicate)
    #syndicate=models.ForeignKey(
    syndicate_id=Long()

    #Syndicate, related_name='deal_syndicate',  )
    #user=models.ForeignKey(User,  )
    user_id=Long()

    amount = Text()
    terms = Text()
    
    last_edited_time = Date()
    created_time = Date()

    class Meta:
        index = myindex
        
class Partnership(DocType):
    #from_company=models.ForeignKey(Company, related_name='partnership_from_company',  )
    from_company_id=Long()

    #from_user=models.ForeignKey(User, related_name='partnership_from_user')
    from_user_id=Long()

    #to_company=models.ForeignKey(Company,  related_name='partnership_to_company')
    to_company_id=Long()

    #to_user=models.ForeignKey(User,  related_name='partnership_to_user')
    to_user_id=Long()

    unique_code = Text() 
    name = Text()
    partnership_type=Text()
    description = Text()

    #type_job=models.ForeignKey(Job,  )

    type_job_id=Long()

    #type_product=models.ForeignKey(Product,  )
    type_product_id=Long()

    #type_company=models.ForeignKey(Company,  )
    type_company_id=Long()

    #type_syndicate=models.ForeignKey(Syndicate,  )
    type_syndicate_id=Long()

    
    is_confirm = Boolean()
    is_reject = Boolean()
    slug = Text()
    created_at = Date()
    updated_at = Date()
    
    class Meta:
        index = myindex
    def __unicode__(self):
        return '%s' % self.name

    def save(self, *args, **kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if not self.partnership_type:
            self.partnership_type='General Partnerships'
        if not self.id:
            self.id=get_partnership_id()
            self._id='main.partnership.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.partnership'
            self.slug=str(self.id) + '_' + slugify(self.name)
            
        super(Partnership, self).save(*args, **kwargs)

class Notification(DocType):
    #owner=models.ForeignKey(User)
    owner_id=Integer()

    #target=models.ForeignKey(User, related_name='+')
    target_id=Long()


    last_edited_time = Date()
    created_time = Date()
    is_new = Boolean()

    notification_type = Text()
    #type_partnership=models.ForeignKey(Partnership)
    type_partnership_id=Long()

    #type_company=models.ForeignKey(Company)
    type_company_id=Long()

    #type_product=models.ForeignKey(Product)
    type_product_id=Long()

    #type_job=models.ForeignKey(Job)
    type_job_id=Long()

    #type_program=models.ForeignKey(Program)
    type_program_id=Long()

    #type_member=models.ForeignKey(User, related_name="++")
    type_member_id=Long()


    class Meta:
        index = myindex
    
    def save(self, *args, **kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if not self.id:
            self.id=get_notification_id()
            self._id='main.notification.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.notification'
            #self.slug=str(self.id) + '_' + slugify(self.name)
            
        super(Notification, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return "from %s" % self.id
    
class MatchCountryToMarket(DocType):
    #country=models.ForeignKey(Country)
    country_id=Integer()

    #market=models.ForeignKey(Market, related_name='matchcountrytomarket')
    market_id=Long()
    market_name=Text()
    rating = Float()
    created_at = Date()
    updated_at = Date()
    
    
    class Meta:
        index = myindex
        

class MatchCountryToMarketContinent(DocType):

    last_edited_time = Date()
    created_time = Date()

    name = Text()
    latitude=Integer()
    longitude= Integer()
    
    rating= Float()

    class Meta:
        index = myindex
        

class MatchCountryToMarketCountry(DocType):

    last_edited_time = Date()
    created_time = Date()
    
    #continent=models.ForeignKey(Continent)
    
    continent_id=Integer()

    
    name = Text()
    latitude=Integer()
    longitude= Integer()

    rating= Float()

    def __unicode__(self):
        return str(self.name)
    

class MatchCompanyToInvestor(DocType):
    #owner=models.ForeignKey(User)
    owner_id=Integer()

    #company=models.ForeignKey(Company)
    company_id=Long()

    #investor=models.ForeignKey(Company, related_name='investor_match')
    investor_id=Long()

    continent_criteria= Boolean()
    success_criteria= Boolean()
    founder_criteria= Boolean()
    market_criteria= Boolean()
    stage_criteria= Boolean()
    match_count = Integer()
    
    class Meta:
        index = myindex
        
    def save(self, *args, **kwargs):
        self.match_count=0
        if self.continent_criteria:
            self.match_count+=1
        if self.success_criteria:
            self.match_count+=1
        if self.founder_criteria:
            self.match_count+=1
        if self.market_criteria:
            self.match_count+=1
        if self.stage_criteria:
            self.match_count+=1
        super(MatchCompanyToInvestor, self).save(*args, **kwargs)


class MatchCompanyToUser(DocType):
    #owner=models.ForeignKey(User)
    owner_id=Integer()

    #company=models.ForeignKey(Company)
    company_id=Long()

    #angel=models.ForeignKey(User, related_name='angel_match')
    user_id=Long()

    success_criteria= Boolean()
    founder_criteria= Boolean()
    market_criteria= Boolean()
    stage_criteria= Boolean()

    class Meta:
        index = myindex
        
class MatchCompanyToCompany(DocType):
    #company=models.ForeignKey(Company)
    company_id=Long()

    #competitor=models.ForeignKey(Company, related_name='company_match')
    competitor_id=Long()

    match_count=Integer()
    score_diff=Integer()
    
    class Meta:
        index = myindex
        
    def save(self, *args, **kwargs):
        super(MatchCompanyToCompany, self).save(*args, **kwargs)

class MatchCompanyToCompanyLocal(DocType):
    #company=models.ForeignKey(Company)
    company_id=Long()

    #competitor=models.ForeignKey(Company, related_name='company_match2')
    competitor_id=Long()

    match_count=Integer()
    score_diff=Integer()
    
    class Meta:
        index = myindex
    def save(self, *args, **kwargs):
        super(MatchCompanyToCompanyLocal, self).save(*args, **kwargs)




class RankInvestmentByCountry(DocType):
    #country=models.ForeignKey(Country)
    country_id=Integer()

    #continent=models.ForeignKey(Continent,  )
    continent_id=Integer()

    name = Text()
    latitude=Integer()
    longitude= Integer()
    rating= Float()
    
    class Meta:
        index = myindex

class RankInvestorByCountry(DocType):
    #country=models.ForeignKey(Country)
    country_id=Integer()

    #investor=models.ForeignKey(Company)
    investor_id=Long()

    investor_name=Text()
    rating= Float()
    rank=Integer()

    class Meta:
        index = myindex

class CompanyMarket(DocType):
    #company=models.ForeignKey(Company)
    company_id=Long()

    #market=models.ForeignKey(Market)
    market_id=Long()

    class Meta:
        index = myindex
        
class UserMarket(DocType):
    #user=models.ForeignKey(UserDefault)
    user_id=Long()

    #market=models.ForeignKey(Market)
    market_id=Long()

    class Meta:
        index = myindex
    

        
class CompanyResource(DocType):
    #company=models.ForeignKey(Company)
    company_id=Long()

    #resource=models.ForeignKey(Resource)
    resource_id=Long()

    
    class Meta:
        index = myindex
    
    


class Instrument(DocType):
    #resource=models.ForeignKey(Resource,  )
    id=Long()
    resource_id=Long()

    #company=models.ForeignKey(Company,  )
    company_id=Long()

    broker=Text(fields={'raw': String(index='not_analyzed'), 'keyword': Keyword()})
    sym=Text(fields={'raw': String(index='not_analyzed'), 'keyword': Keyword()})
    text=Text(fields={'raw': String(index='not_analyzed'), 'keyword': Keyword()})
    cur=Text(fields={'raw': String(index='not_analyzed'), 'keyword': Keyword()})
    exch=Text(fields={'raw': String(index='not_analyzed'), 'keyword': Keyword()})
    sec_type=Text(fields={'raw': String(index='not_analyzed'), 'keyword': Keyword()})
    trade_freq=Integer()
    mult=Float()
    local_sym=Text(fields={'raw': String(index='not_analyzed'), 'keyword': Keyword()})
    
    contract_month=Text(fields={'raw': String(index='not_analyzed'), 'keyword': Keyword()})
    expiry=Text(fields={'raw': String(index='not_analyzed'), 'keyword': Keyword()})
    ev_rule=Text(fields={'raw': String(index='not_analyzed'), 'keyword': Keyword()})
    liquid_hours=Text(fields={'raw': String(index='not_analyzed'), 'keyword': Keyword()})
    long_name=Text(fields={'raw': String(index='not_analyzed'), 'keyword': Keyword()})
    min_tick=Float()
    time_zone_id=Long()
    trading_hours=Text()
    under_con_id=Long()
    
    created_at = Date()
    updated_at = Date()
    crawl_source=Text()

    
    class Meta:
        index = myindex
    
    def __unicode__(self):
        return '%s' % self.name

    def save(self, *args, **kwargs):
        eastern=timezone('US/Eastern')
       
        if self.created_at == None:
            self.created_at = datetime.now().replace(tzinfo=eastern)  
        self.updated_at = datetime.now().replace(tzinfo=eastern) 
        
        if not self.id:
            self.id=get_instrument_id()
            self._id='main.instrument.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.instrument'
            #self.text=self.article_title
            #self.slug=str(self.id) + '_' + slugify(self.article_title)
            
        super(Instrument, self).save(*args, **kwargs)



class System(DocType):
    #user = models.ForeignKey(User, primary_key=True)
    version= Text()
    system= Text()
    name=Text()
    c2id=Text()
    c2api=Text()
    c2qty=Integer()
    c2submit=Boolean()
    #c2instrument=models.ForeignKey(Instrument, related_name='c2instrument',  )
    c2instrument_id=Long()

    ibqty=Integer()
    #ibinstrument=models.ForeignKey(Instrument, related_name='ibinstrument',  )
    ibinstrument_id=Long()

    ibsubmit=Boolean()
    trade_freq=Integer()
    ibmult=Integer()
    c2mult=Integer()
    signal=Text()

    class Meta:
        index = myindex
    
    def __unicode__(self):
        return '%s' % self.name

    def save(self, *args, **kwargs):
        eastern=timezone('US/Eastern')
       
        if self.created_at == None:
            self.created_at = datetime.now().replace(tzinfo=eastern)  
        self.updated_at = datetime.now().replace(tzinfo=eastern) 
        
        if not self.id:
            self.id=get_system_id()
            self._id='main.system.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.system'
            #self.text=self.article_title
            #self.slug=str(self.id) + '_' + slugify(self.article_title)
            
        super(System, self).save(*args, **kwargs)



class Feed(DocType):
    #instrument=models.ForeignKey(Instrument)
    instrument_id=Long()

    frequency=Integer()
    pct_change=Float()
    settle=Float()
    open_interest=Float()

    date=Date()
    open=Float()
    high=Float()
    low=Float()
    close=Float()
    
    volume=Float()
    wap=Float()
    
    created_at = Date()
    updated_at = Date()
    crawl_source=Text()

    class Meta:
        index = myindex
        
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
        
        '''
        if not self.id:
            #self.id=get_feed_id()
            self._id='main.feed.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.feed'
            #self.text=self.article_title
            #self.slug=str(self.id) + '_' + slugify(self.article_title)
            
        '''
         
        super(Feed, self).save(*args, **kwargs)


class Prediction(DocType):
    #instrument=models.ForeignKey(Instrument)
    instrument_id=Long()

    frequency=Integer()
    pred_start_date=Date()
    
    date=Date()
    open=Float()
    high=Float()
    low=Float()
    close=Float()
    volume=Float()
    wap=Float()
    algo_name=Text()
    is_scaled=Boolean()
    created_at = Date()
    updated_at = Date()
    crawl_source=Text()

    class Meta:
        index = myindex
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
        
        '''
        if not self.id:
            #self.id=get_prediction_id()
            self._id='main.prediction.' + str(self.id)
            self.my_id=self._id
            self.django_id=str(self.id)
            self.django_ct='main.prediction'
            #self.text=self.article_title
            #self.slug=str(self.id) + '_' + slugify(self.article_title)
            
        ''' 
        super(Prediction, self).save(*args, **kwargs)


class BidAsk(DocType):
    #instrument=models.ForeignKey(Instrument)
    instrument_id=Long()

    frequency=Integer()
    ask=Float()
    asksize=Float()
    bid=Float()
    bidsize=Float()
    date=Date()
    
    created_at = Date()
    updated_at = Date()
    crawl_source=Text()

    
    class Meta:
        index = myindex
        
    def __unicode__(self):
        return '%s' % self.name

    def save(self, *args, **kwargs):
        eastern=timezone('US/Eastern')
       
        if self.created_at == None:
            self.created_at = datetime.now().replace(tzinfo=eastern)  
        self.updated_at = datetime.now().replace(tzinfo=eastern) 
        super(BidAsk, self).save(*args, **kwargs)



class ROI(DocType):
    #instrument=models.ForeignKey(Instrument)
    instrument_id=Long()

    frequency=Integer()
    pred_start_date=Date()
    algo_name=Text()
    
    open_date=Date()
    close_date=Date()
    open_price=Float()
    open_qty=Float()
    close_price=Float()
    close_qty=Float()
    direction=Text( )
    pnl=Float()
    pnl_pct=Float()
    is_profitable=Boolean()
    
    is_scaled=Boolean()
    created_at = Date()
    updated_at = Date()
    crawl_source=Text()
    class Meta:
        index = myindex
        
    def __repr__(self):
        #return '{ "date":"%s", "open":%s, "high":%s, "low":%s, "close":%s,"volume":%s }' % (self.date, self.open, self.high, self.low, self.close, self.volume)
        return '{ "open_date":"%s", "close_date":"%s", "is_profitable":%s, "pnl_pct":%s }' % (self.open_date,  self.close_date, self.is_profitable, self.pnl_pct)
        
    def __str__(self):
        return self.__repr__()
    
    def __unicode__(self):
        return self.__repr__()
    
    def save(self, *args, **kwargs):
        eastern=timezone('US/Eastern')
       
        if self.created_at == None:
            self.created_at = datetime.now().replace(tzinfo=eastern)  
        self.updated_at = datetime.now().replace(tzinfo=eastern)  
        super(ROI, self).save(*args, **kwargs)


class UpdateHistory(DocType):
    update_type=Text( ) #Algo, User
    update_name=Text( )
    #update_user=models.ForeignKey(UserDefault)
    update_user_id=Long()

    #update_company=models.ForeignKey(Company)
    update_company_id=Long()

    update_dest_type=Text( )
    update_dest_table=Text( )
    update_dest_field=Text( )
    update_dest_op_type=Text( ) #Update, Delete
    update_dest_old_val=Text( )
    update_dest_new_val=Text( )

    created_at = Date()
    updated_at = Date()


    class Meta:
        index = myindex
        
        
class CompanyMainInfo(DocType):
    reindex_related = ('company',)
    #company=models.ForeignKey(Company,)
    company_id=Long()


    #owner=models.ForeignKey(User)

    owner_id=Integer()

    
    is_active = Boolean()
    is_public = Boolean()
    is_save = Boolean()
    is_confirm = Boolean()
    is_trusted_vc = Boolean()
    is_partner = Boolean()
    is_government = Boolean()
    
    
    ticker = Text()
    exchange=Text()
    sec_cik=Text()
    sec_cik_int=Text()
    partner_order = Integer()

    company_name = Text()
    company_kor_name = Text()

    corporation = Text()


    company_number = Text()
    corporate_number = Text()

    last_edited_time = Date()
    created_time = Date()

    
    class Meta:
        index = myindex
    
class CompanySummaryInfo(DocType):
    reindex_related = ('company',)
    
    #company=models.ForeignKey(Company,)
    
    company_id=Long( unique=True)


    company_class = Text(
         )
    investor_class = Text()
    company_short = Text()
    company_long = Text()
    
    company_established = Text(
         )

    company_founded_year = Integer(
        )

    company_founded_month = Integer(
        )

    company_founded_day = Integer(
        )

    last_edited_time = Date()
    created_time = Date()

   
    
    class Meta:
        index = myindex
        
class CompanySocialInfo(DocType):
    reindex_related = ('company',)

    #company=models.ForeignKey(Company,)

    company_id=Long( unique=True)

    
    tips_start_date = Date()
    company_website = Text()
    company_logo = Text()
    rocketpunch_url = Text()
    angellist_url=Text()
    sec_url=Text()
    e27_url=Text()
    f6s_url=Text()
    forbes_url=Text()
    
    is_tips = Boolean()
    is_angel = Boolean()
    is_dcamp = Boolean()
    is_rocketpunch = Boolean()
    is_dart = Boolean()
    is_bizinkorea = Boolean()
    is_startup = Boolean()
    is_investor = Boolean()

    company_linkedin_page = Text()
    company_facebook_page = Text()
    company_twitter = Text()

    
    last_edited_time = Date()
    created_time = Date()
    
    
    class Meta:
        index = myindex


        
    def save(self, *args, ** kwargs):
        if not self.created_time:
            self.created_time = datetime.now()
            self.is_active=True
        if not self.company_logo:
            self.company_logo="http://beginning.wold/media/img/company/noimg.png"
        if not self.company_class:
            self.company_class='Startup'
        self.last_edited_time = datetime.now()

        super(Company, self).save(*args, **kwargs)
            
class CompanyLocationInfo(DocType):
    reindex_related = ('company',)
    #company=models.ForeignKey(Company,)
    company_id=Long( unique=True)

    
    company_continent = Text()
    #continent=models.ForeignKey(Continent,  )
    continent_id=Integer()


    company_country = Text()
    #country=models.ForeignKey(Country,  )
    country_id=Integer()


    company_city = Text()
    #city=models.ForeignKey(City,  )
    city_id=Integer()

    
    company_state = Text()
    #state=models.ForeignKey(State,  )
    state_id=Integer()


    company_region = Text()
    #region=models.ForeignKey(Region,  )
    region_id=Integer()


    company_location = Text()
    company_location_latitude=Integer()
    company_location_longitude= Integer()
    
    last_edited_time = Date()
    created_time = Date()
    
    class Meta:
        index = myindex


class CompanyScoreInfo(DocType):
    reindex_related = ('company',)
    #company=models.ForeignKey(Company,)
    company_id=Long(unique=True)

    score1 = Float()
    score2 = Float()
    score3 = Float()
    score4 = Float()
    score5 = Float()
    
    last_edited_time = Date()
    created_time = Date()

    class Meta:
        index = myindex
        
class CompanyEmployeeInfo(DocType):
    reindex_related = ('company',)
    #company=models.ForeignKey(Company,)
    company_id=Long( unique=True)


    company_employee = Text()
    employee_total = Integer()
    employee_total_month_ago = Integer()
    employee_added_this_month = Integer()
    employee_growth_month = Integer()
    employee_total_6month_ago = Integer()
    employee_added_in_6month = Integer()
    employee_growth_6month = Integer()

    employee_added_since_funding = Integer()
    employee_months_since_funding = Integer()
    employee_growth_since_funding = Integer()
    
    last_edited_time = Date()
    created_time = Date()

    
    class Meta:
        index = myindex
        
class CompanyTrafficInfo(DocType):
    reindex_related = ('company',)
    #company=models.ForeignKey(Company,)
    company_id=Long( unique=True)

    
    company_favorite_count = Integer()
    company_recommendation_count = Integer()
    traffic_monthly_unique = Integer()
    traffic_monthly_unique_week_ago = Integer()
    traffic_monthly_weekly_growth = Integer()
    traffic_monthly_unique_month_ago = Integer()
    traffic_monthly_monthly_growth = Integer()
    traffic_mobile_download = Integer()
    traffic_mobile_download_week_ago = Integer()
    traffic_mobile_download_weekly_growth = Integer()
    traffic_mobile_download_month_ago = Integer()
    traffic_mobile_download_monthly_growth = Integer()
    traffic_growth_month = Integer()
    
    last_edited_time = Date()
    created_time = Date()

    class Meta:
        index = myindex

        
class CompanyFinanceInfo(DocType):
    reindex_related = ('company',)
    #company=models.ForeignKey(Company,)
    company_id=Long( unique=True)

    revenue = Float()
    total_valuation = Float()
    total_asset = Float()
    total_debt = Float()
    total_capital = Float()
    total_sales = Float()
    net_income = Float()
    operating_income = Float()
    ratio_sales_net = Float()
    ratio_sales_operating = Float()
    period_end_date=Date()
    
    last_edited_time = Date()
    created_time = Date()

    class Meta:
        index = myindex

class CompanyFundingInfo(DocType):
    reindex_related = ('company',)
    
    #company = models.ForeignKey(Company)
    
    company_id=Long( unique=True)
    
    #investor_type = models.ForeignKey(InvestorType,  )
    
    investor_type_id=Long()

    investor_fund_sold_3yr = Integer()
    investor_last_funding_date = Date()
    investor_portfolio_size = Integer()
    investor_total_deals = Integer()
    #invested_stages=models.ForeignKey(FundingStage,  related_name='company_funding_invested_stages')
    invested_stages_id=Long()

    invested_stages_csv = Text()
    invested_success = Integer()
    invested_success_amt=Float()
    invested_founder_csv= Text()
    invested_market_csv= Text()
    invested_continent_csv= Text()
    invested_funding_stage_csv = Text()

    investor_list_csv = Text()
    
    
    company_fundraising = Text()
    company_fundraising_currency = Text()
    company_fundraising_highlight = Text()
    company_fundraising_deck = Text()


    last_funding_amt = Float()
    last_funding_date = Date()
    last_funding_months_ago = Integer()
    total_funding_amt = Float()
    #funding_stage=models.ForeignKey(FundingStage,  )
    funding_stage_id=Long()

    funding_stage_name = Text()
    
    last_edited_time = Date()
    created_time = Date()

    class Meta:
        index = myindex


class CompanyProductInfo(DocType):
    reindex_related = ('company',)
    #company=models.ForeignKey(Company,)
    company_id=Long( unique=True)

    product_list_csv = Text()
    product_app_store = Text()
    product_google_play = Text()
    
    last_edited_time = Date()
    created_time = Date()

    class Meta:
        index = myindex

    

class CompanyCrawlInfo(DocType):
    reindex_related = ('company',)
    #company=models.ForeignKey(Company)
    company_id=Long(unique=True)

    crawl_source=Text()
    
    last_edited_time = Date()
    created_time = Date()

    class Meta:
        index = myindex

class CompanySlugInfo(DocType):
    reindex_related = ('company',)
    
    #company=models.ForeignKey(Company,)
    
    company_id=Long( unique=True)

    slug=Text()
    
    last_edited_time = Date()
    created_time = Date()

    class Meta:
        index = myindex

class CompanyMarketInfo(DocType):
    reindex_related = ('company',)
    #company=models.ForeignKey(Company,)
    company_id=Long(unique=True)


    company_industry = Text()

    product_market_csv = Text()
    company_top_keywords = Text()
    company_interests = Text()
    company_alerts = Text()
    
    last_edited_time = Date()
    created_time = Date()
    
    class Meta:
        index = myindex

    def market_as_list(self):
        return self.company_industry.split(',')

    def market_as_list_new(self):
        return self.company_industry.split(',')

    def get_dict_industries_from_csv(self):
        market_dict = dict()

        if self.product_market_csv:
            if len(self.product_market_csv) > 0:
                # pass #print self.product_market_csv
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
                # pass #print self.product_list_csv
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
    


class Career(DocType):
    #owner=models.ForeignKey(User)
    owner_id=Integer()


    career_year = Integer()
    career_end_year = Integer()
    career_description = Text()
    class Meta:
        index = myindex

#    def __unicode__(self):
#        return self.owner


class Honor(DocType):
    #owner=models.ForeignKey(User)
    owner_id=Integer()


    honor_month = Integer()
    honor_year = Integer()
    honor_end_month = Integer()
    honor_end_year = Integer()
    honor_description = Text()
    honor_temp = Boolean()
    class Meta:
        index = myindex


class CompanyHonor(DocType):
    #owner=models.ForeignKey(Company)
    owner_id=Integer()


    company_honor_year = Integer()
    company_honor_end_year = Integer()
    company_honor_description = Text()
    class Meta:
        index = myindex


class ProductHistory(DocType):
    #owner=models.ForeignKey(Product)
    owner_id=Integer()


    company_honor_year = Integer()
    company_honor_end_year = Integer()
    company_honor_description = Text()
    class Meta:
        index = myindex


class UserCompany(DocType):
    #owner=models.ForeignKey(User)
    owner_id=Integer()


    is_company_current = Boolean()
    company_start_month = Integer()
    company_start_year = Integer()
    company_end_month = Integer()
    company_end_year = Integer()
    company_id = Text()
    company_name = Text()
    company_title = Text()
    company_role = Text()
    class Meta:
        index = myindex


class ProgramQuestion(DocType):
    #owner=models.ForeignKey(Program)
    owner_id=Integer()


    last_edited_time = Date()
    created_time = Date()

    program_question_order = Text()
    program_question_sentence = Text()
    program_question_type = Text()
    program_choice_count = Text()

    class Meta:
        index = myindex

    def __unicode__(self):
        return self.program_question_sentence


class ParagraphQuestion(DocType):
    #owner=models.ForeignKey(ProgramQuestion)
    owner_id=Integer()
    class Meta:
        index = myindex


    question_character_limit = Text()


class ChoiceQuestion(DocType):
    #owner=models.ForeignKey(ProgramQuestion)
    owner_id=Integer()

    class Meta:
        index = myindex


    choice_answer = Text()


class UserFavorite(DocType):
    #owner=models.ForeignKey(User)
    owner_id=Integer()


    last_edited_time = Date(
        'date edited',  )
    created_time = Date()

    favorite_type = Text()
    type_id = Text()
    #type_company=models.ForeignKey(Company)
    type_company_id=Long()

    #type_product=models.ForeignKey(Product)
    type_product_id=Long()

    class Meta:
        index = myindex


class ProgramApplication(DocType):
    #owner=models.ForeignKey(Program)
    owner_id=Integer()


    last_edited_time = Date()
    created_time = Date()

    company_id = Text()

    class Meta:
        index = myindex

class ProgramApplicationAnswer(DocType):
    #owner=models.ForeignKey(ProgramApplication)
    owner_id=Integer()


    question_id = Text()
    question_order = Text()
    answer = Text()
    class Meta:
        index = myindex


class ProgramApplicationTextAnswer(DocType):
    #owner=models.ForeignKey(ProgramApplication)
    owner_id=Integer()


    question_id = Text()
    question_order = Text()
    answer = Text()
    class Meta:
        index = myindex


class UserComment(DocType):
    #owner=models.ForeignKey(User)
    owner_id=Integer()


    last_edited_time = Date()
    created_time = Date()

    comment_type = Text()
    type_id = Text()
    comment_content = Text()
    class Meta:
        index = myindex


class CompanyPatent(DocType):
    #owner=models.ForeignKey(Company)
    owner_id=Integer()


    last_edited_time = Date()
    created_time = Date()
    is_private = Boolean()

    patent_title = Text()
    patent_number = Text()
    patent_inventor = Text()
    patent_issued_month = Integer()
    patent_issued_day = Integer()
    patent_issued_year = Integer()
    patent_description = Text()
    patent_url = Text()
    class Meta:
        index = myindex


class InvitationCode(DocType):
    code = Text()

    code_usage_count = Integer()

    class Meta:
        index = myindex
        


class SimilarProduct(DocType):
    #owner=models.ForeignKey(Product)
    owner_id=Integer()

    #target=models.ForeignKey(Product, related_name='+')
    target_id=Long()


    last_edited_time = Date()
    created_time = Date()

    is_user_input = Boolean()


class UserInvoice(DocType):
    #user=models.ForeignKey(User)
    user_id=Long()

    last_edited_time = Date()
    created_time = Date()
    amount = Integer()
    name = Text()


class UserSubscription(DocType):
    #user=models.ForeignKey(User)
    user_id=Long()

    #invoice=models.ForeignKey(UserInvoice)
    invoice_id=Long()

    last_edited_time = Date()
    created_time = Date()
    purchased_at = Date(auto_now_add=True)
    invoice_name = Text()


class UserFeedback(DocType):
    #owner=models.ForeignKey(User)
    owner_id=Integer()


    last_edited_time = Date()
    created_time = Date()

    contents = Text()


class UserActivity(DocType):
    #owner=models.ForeignKey(User)
    owner_id=Integer()

    last_edited_time = Date()
    created_time = Date()

    activity_type = Text()
    target_type = Text()
    #target_product=models.ForeignKey(Product)
    target_product_id=Long()

    #target_company=models.ForeignKey(Company)
    target_company_id=Long()


    def time_to_now(self):
        to_now = datetime.now(mytz).replace(
            tzinfo=None) - self.last_edited_time.replace(tzinfo=None)
        to_now_min = int(to_now.total_seconds() / 60) - 60 * 9
        return to_now_min


class TrendsCSV(DocType):
    is_save=Boolean()
    is_confirm=Boolean()

    last_edited_time = Date()
    created_time = Date()

    csv_date = Text()
    csv_market = Text()
    csv_file = Text(upload_to='csv/trends/')


class ExcelUpdate(DocType):
    is_save=Boolean()
    is_confirm=Boolean()
    is_again = Boolean()
    last_edited_time = Date()
    created_time = Date()

    excel_file = Text(upload_to='excel/')
    num_investors = Integer()


class EmployeeUpdate(DocType):
    is_save=Boolean()
    is_confirm=Boolean()
    is_again = Boolean()
    last_edited_time = Date()
    created_time = Date()

    excel_file = Text(upload_to='excel/')
    start_year = Integer()
    start_month = Integer()
    num_month = Integer()


class BusinessNumberUpdate(DocType):
    is_save=Boolean()
    is_confirm=Boolean()
    last_edited_time = Date()
    created_time = Date()

    excel_file = Text(upload_to='excel/')


class FreeUserLimit(DocType):
    day = Integer()
    created_time = Date()
    updated_time = Date(auto_now_add=True)


class UploadReport(DocType):
    unique_code = Text(
         unique=True,  editable=False)
    title = Text()
    document = Text(upload_to='report')
    total_download = Integer()
    total_view = Integer()
    date = Date()
    slug = Text()
    created_time = Date()
    updated_time = Date(auto_now_add=True)

    def __unicode__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if self.unique_code == None:
            self.unique_code = uuid.uuid4().hex
        self.updated_time = datetime.now()
        super(UploadReport, self).save(*args, **kwargs)


class SaveFilterCompanies(DocType):
    #user=models.ForeignKey(User)
    user_id=Long()

    name = Text()
    location = Text()
    total_funding = Text()
    investor = Text()
    founded_year = Text()
    vertical = Text()
    stage = Text()
    keyword = Text()
    traffic_monthly_unique = Text()
    traffic_monthly_unique_week_ago = Text()
    traffic_monthly_weekly_growth = Text()
    traffic_monthly_unique_month_ago = Text()
    traffic_monthly_monthly_growth = Text()
    traffic_mobile_download = Text()
    traffic_mobile_download_week_ago = Text()
    traffic_mobile_download_weekly_growth = Text()
    traffic_mobile_download_month_ago = Text()
    traffic_mobile_download_monthly_growth = Text()
    subscribe_company_alert = Boolean()
    subscribe_news_alert = Boolean()
    slug = Text()
    created_at = Date()
    updated_at = Date()

    class Meta:
            index = myindex
            
    def __unicode__(self):
        return '%s' % self.name

    def save(self, *args, **kwargs):
        if self.created_at == None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        super(SaveFilterCompanies, self).save(*args, **kwargs)



class WebStatus(DocType):
    is_save=Boolean()
    is_confirm=Boolean()
    last_edited_time = Date()
    created_time = Date()

    updated_year = Integer()
    updated_month = Integer()
    updated_day = Integer()
    updated_week = Integer()

    #product=models.ForeignKey(Product)

    product_id=Long()


    traffic = Text()
    visits = Text()
    pageviews = Text()
    visitduration = Text()
    bouncerate = Text()
    crawl_source=Text()

    class Meta:
        index = myindex
        
class HomeRanking(DocType):
    last_edited_time = Date()
    created_time = Date()
    name = Text()
    #company=models.ForeignKey(
    company_id=Long()

    #Company,  )
    #product=models.ForeignKey(
    product_id=Long()

    #Product,  )
    company_name=Text()
    company_logo=Text()
    company_slug=Text()
    company_short=Text()
    rank=Integer()
    prior_rank=Integer()
    score=Integer()
    score1=Integer()
    score2=Integer()
    score3=Integer()
    score4=Integer()
    score5=Integer()
    prior_score=Integer()
    
    product_name = Text()
    product_slug = Text()
    product_website = Text()
    product_google_play = Text()
    product_app_store = Text()
    product_facebook_page = Text()
    product_video = Text()
    product_short = Text()
    #company
    last_funding_date = Date()
    last_funding_amt = Float()
    total_funding_amt = Float()
    investor_list_csv = Text()

    market_total=Integer()
    market_name=Text()
    def get_dict_investors_from_csv(self):
        investor_dict = dict()

        if self.investor_list_csv:
            if len(self.investor_list_csv) > 0:
                # pass #print self.investor_list_csv
                company_investors = self.investor_list_csv.split(';')
                for investor in company_investors:
                    if len(investor) > 1:
                        (investor_id, investor_name) = investor.split('|')
                        investor_dict[investor_id] = investor_name

        return investor_dict
    def video_as_embedded(self):
        if 'youtube.com' in self.product_video:
            if '?v=' in self.product_video:
                return 'http://www.youtube.com/embed/' + self.product_video.split('?v=')[-1]
            else:
                return self.product_video
        elif 'youtu.be' in self.product_video:
            if '?v=' in self.product_video:
                return 'http://www.youtube.com/embed/' + self.product_video.split('?v=')[-1]
            else:
                return 'http://www.youtube.com/embed/' + self.product_video.split('/')[-1]
        elif 'vimeo.com' in self.product_video:
            return 'https://player.vimeo.com/video/' + self.product_video.split('/')[-1]
        elif 'youku.com' in self.product_video:
            split_url = self.product_video.split('/')[-1]
            split_url1 = split_url.split('.')[0]
            split_url2 = split_url1.split('_')[1]
            return 'http://player.youku.com/embed/%s' % split_url2
        else:
            return self.product_video
