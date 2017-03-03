# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
from autohome_tit.items import AutohomeCarStoreUrl
from autohome_tit.mongodb import mongoservice
from autohome_tit import pipelines
import math


class AutohomeCarStoreSpider(RedisSpider):
    name='autohome_carstore'
    api_url='http://mall.autohome.com.cn/list/0-999999-%s-0-0-0-0-0-0-1.html?factoryId=0&minPrice=-1&maxPrice=-1&stageTag=0&importTag=0&double11Tag=0&prefix=&dataSource='
    car_url='http://mall.autohome.com.cn/list/0-999999-%s-0-0-0-0-0-0-%d.html?factoryId=0&minPrice=-1&maxPrice=-1&stageTag=0&importTag=0&double11Tag=0&dataSource=&eventId=&eventProcessId=&providerId=&itemIds='
    pipeline = set([pipelines.CarstorePipeline, ])

    def start_requests(self):
        usedcar_url = mongoservice.get_carstore_url()
        for brand in usedcar_url:
            bid = brand['bid']
            url = self.api_url % bid
            yield Request(url, meta={'bid': bid}, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'},
                          callback=self.get_letter)

    def get_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        bid=response.meta['bid']
        total=soup.find('span',class_="condition-total").get_text()
        num=int(total[1:-3])
        pageamount=math.ceil(num/24)
        page_amount=int(pageamount)+1
        for page_num in range(1, page_amount + 1):
            urls=self.car_url%(bid,page_num)
            yield Request(urls,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'},callback=self.get_car_list)


    def get_car_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        list_info=soup.find('div',id = "list")
        if list_info:
            li_info=list_info.find_all('li',class_="carbox")
            for li in li_info:
                href=li.find('a').get('href')
                yield Request(href,callback=self.get_url)


    def get_url(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        tit=soup.find('title').get_text().strip()
        url=response.url
        result=AutohomeCarStoreUrl()
        breadnav=soup.find('div',class_="breadnav breadnav-select")
        if breadnav:
            address=breadnav.find('ul',class_="fn-clear").get_text().strip()
            result['address']=address
        else:
            result['address'] = ''
        result['category'] = '车商城'
        result['tit']=tit
        result['url']=url
        yield result


    def spider_idle(self):
        """This function is to stop the spider"""
        req = self.next_requests()
        if req:
            self.schedule_next_requests()
        else:
            self.crawler.engine.close_spider(self, reason='finished')

