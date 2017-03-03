# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
from autohome_tit.items import AutohomeVehicleKoubeiItem
from autohome_tit.mongodb import mongoservice
from autohome_tit import pipelines


class AutohomeVehicleKoubeiSpider(RedisSpider):
    name = 'autohome_vehiclekoubei'
    pipeline = set([pipelines.VehicleKoubeiPipeline, ])

    def start_requests(self):
        config_url = mongoservice.get_vehiclekoubei_url()
        for url in config_url:
            yield Request(url,callback=self.get_url)


    def get_url(self, response):
        soup = BeautifulSoup(response.body_as_unicode())
        result = AutohomeVehicleKoubeiItem()
        breadnav = soup.find('div', class_="breadnav")
        if breadnav:
            address = breadnav.get_text().strip()
            add = address.split('：')
            result['address'] = add[1]
        tit = soup.find('title').get_text().strip()
        url = response.url
        result['category'] = '车型-口碑'
        result['tit'] = tit
        result['url'] = url
        yield result


    def spider_idle(self):
        """This function is to stop the spider"""
        req = self.next_requests()
        if req:
            self.schedule_next_requests()
        else:
            self.crawler.engine.close_spider(self, reason='finished')