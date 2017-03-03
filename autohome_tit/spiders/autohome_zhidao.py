# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
from autohome_tit.items import AutohomeZhidaoUrl
from autohome_tit.mongodb import mongoservice
from autohome_tit import pipelines


class AutohomeZhiDaoUrlSpider(RedisSpider):
    name='autohome_zhidao'
    pipeline = set([pipelines.ZhidaoPipeline, ])

    def start_requests(self):
        zhidao_url = mongoservice.get_ask_url()
        for url in zhidao_url:
            yield Request(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'},callback=self.get_letter)
            yield Request(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'},callback=self.get_url)

    def get_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        hl_con=soup.find('div',id="hl-con")
        if hl_con:
            li_info=hl_con.find('ul').find_all('li')
            for li in li_info:
                href=li.find('a').get('href')
                yield Request(href,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'},callback=self.get_url)

    def get_url(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        tit=soup.find('title').get_text().strip()
        url=response.url
        result=AutohomeZhidaoUrl()
        result['tit']=tit
        result['url']=url
        result['category'] = '车型-问答'
        yield result


    def spider_idle(self):
        """This function is to stop the spider"""
        req = self.next_requests()
        if req:
            self.schedule_next_requests()
        else:
            self.crawler.engine.close_spider(self, reason='finished')