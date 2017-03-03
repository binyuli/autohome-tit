# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
from autohome_tit.items import AutohomeOwnerpriceUrl
from autohome_tit.mongodb import mongoservice
from autohome_tit import pipelines


class AutohomeOwnerpriceSpider(RedisSpider):
    name='autohome_ownerprice'
    pipeline = set([pipelines.OwnerpricePipeline, ])

    def start_requests(self):
        baojia_url = mongoservice.get_price_car_url()
        for url in baojia_url:
            yield Request(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'},callback=self.get_letter)
            yield Request(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'},callback=self.get_url)


    def get_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        model_list=soup.find_all('div',class_="model-list")
        if model_list:
            for model in model_list:
                ul_info=model.find_all('ul')
                for ul in ul_info:
                    href=ul.find('li',class_="model-list-item").find('a').get('href')
                    urls='http://jiage.autohome.com.cn'+href
                    yield Request(urls,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'},callback=self.get_url)


    def get_url(self,response):
        result = AutohomeOwnerpriceUrl()
        soup = BeautifulSoup(response.body_as_unicode())
        breadnav=soup.find('div',class_="breadnav fn-left")
        if breadnav:
            bread_nav=breadnav.get_text().strip()
            add = bread_nav.split('：')
            result['address'] = add[1]

        tit=soup.find('title').get_text().strip()
        url=response.url
        result['category'] = '车型-车主价格'
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