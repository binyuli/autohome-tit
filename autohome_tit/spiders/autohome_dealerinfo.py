# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import  Request
from bs4 import BeautifulSoup
from autohome_tit.mongodb import mongoservice
from autohome_tit.items import AutohomeDealerinfoUrl
from autohome_tit import pipelines

class AutohomeDealerinfoSpider(RedisSpider):
    name = 'autohome_dealerinfo'
    api_url = 'http://dealer.autohome.com.cn%s'
    pipeline = set([pipelines.DealerinfoPipeline, ])


    def start_requests(self):
        info_urls = mongoservice.get_dealerinfo_url()
        for url in info_urls:
            yield Request(self.api_url%url, callback=self.get_url)


    def get_url(self, response):
        soup = BeautifulSoup(response.body_as_unicode(), 'lxml')
        url = response.url
        tit = soup.find('title').get_text().strip()
        result = AutohomeDealerinfoUrl()
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
        result['category'] = '经销商-公司介绍'
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
