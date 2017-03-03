# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
from autohome_tit.mongodb import mongoservice
from autohome_tit.items import AutohomeBrandConfigUrlItem
from autohome_tit import pipelines

class AutohomeConfigSpider(RedisSpider):
    name="autohome_config"
    pipeline = set([pipelines.ConfigPipeline, ])


    def start_requests(self):
        config_urls = mongoservice.get_config_url()
        for url in config_urls:
            yield Request(url,headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'},callback=self.get_koubei)


    def get_koubei(self, response):
        result = AutohomeBrandConfigUrlItem()
        info = response.body_as_unicode()
        soup = BeautifulSoup(info, 'lxml')
        breadnav=soup.find('div',class_="path")
        if breadnav:
            bread_nav=breadnav.get_text().strip()
            add = bread_nav.split(':')
            result['address'] = add[1]
        tit=soup.find('title').get_text().strip()
        url=response.url
        result['category'] = '车型-参数配置'
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
