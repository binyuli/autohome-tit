# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import  Request
from bs4 import BeautifulSoup
from autohome_tit.mongodb import mongoservice
from autohome_tit.items import AutohomeDealersalerlistUrl
from autohome_tit import pipelines

class AutohomeDealersalerlistSpider(RedisSpider):
    name = 'autohome_dealersalerlist'
    api_url = 'http://dealer.autohome.com.cn%s'
    pipeline = set([pipelines.DealersalerlistPipeline, ])


    def start_requests(self):
        # fi = open('autohome_tit/dealer', 'r')
        # for line in fi:
        #     brand_info = eval(line)
        #     if brand_info.has_key('salerlist'):
        #         url = brand_info['salerlist']
        #         yield Request(self.api_url % url, callback=self.get_url)
        salerlist_urls = mongoservice.get_dealersalerlist_url()
        for url in salerlist_urls:
            yield Request(self.api_url%url, callback=self.get_url)


    def get_url(self, response):
        soup = BeautifulSoup(response.body_as_unicode(), 'lxml')
        url = response.url
        tit = soup.find('title').get_text().strip()
        result = AutohomeDealersalerlistUrl()
        hotcar = soup.find('div', id="hotcar")
        if hotcar:
            hot_car = hotcar.get_text().strip()
            if '：' in hot_car:
                car = hot_car.split('：')
                result['hot_car'] = car[1]
        breadnav = soup.find('div', id="breadnav")
        if breadnav:
            bread_nav = breadnav.get_text().strip()
            add = bread_nav.split('：')
            result['address'] = add[1]
        result['category'] = '经销商-销售顾问'
        result['url'] = url
        result['tit'] = tit
        yield result


    def spider_idle(self):
        """This function is to stop the spider"""
        req = self.next_requests()
        if req:
            self.schedule_next_requests()
        else:
            self.crawler.engine.close_spider(self, reason='finished')
