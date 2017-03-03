# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
from autohome_tit.mongodb import mongoservice
from autohome_tit.items import AutohomeDetailedVehicleUrl
from autohome_tit import pipelines

class AutohomeDetailedVehicleUrlSpider(RedisSpider):
    name="autohome_detaile"
    pipeline = set([pipelines.DetaileVehiclePipeline, ])


    def start_requests(self):
        detailed_vehicle_url = mongoservice.get_car_type_url()
        for url in detailed_vehicle_url:
            yield Request(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'},callback=self.get_letter)
            yield Request(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'},callback=self.get_url)


    def get_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        ml_leftnavboxs=soup.find('div',id="ml_leftnavboxs1")
        if ml_leftnavboxs:
            a_info=ml_leftnavboxs.find('dl').find_all('a')
            for href in a_info:
                url=href.get('href')
                urls='http://www.autohome.com.cn%s'%url
                yield Request(urls,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'},callback=self.get_url)


    def get_url(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        url=response.url
        tit=soup.find('title').get_text().strip()
        result=AutohomeDetailedVehicleUrl()

        breadnav=soup.find('div',class_="breadnav fn-left")
        if breadnav:
            bread_nav=breadnav.get_text().strip()
            add = bread_nav.split('：')
            result['address'] = add[1]
        result['category'] = '车型详解'
        result['url']=url
        result['tit']=tit
        yield result


    def spider_idle(self):
        """This function is to stop the spider"""
        req = self.next_requests()
        if req:
            self.schedule_next_requests()
        else:
            self.crawler.engine.close_spider(self, reason='finished')


