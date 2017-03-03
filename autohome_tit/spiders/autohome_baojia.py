# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
from autohome_tit.items import AutohomeBaojiaUrl
from autohome_tit.mongodb import mongoservice
from autohome_tit import pipelines


class AutohomeBaojiaSpider(RedisSpider):
    name='autohome_baojia'
    pipeline = set([pipelines.BaojiaPipeline, ])

    def start_requests(self):
        baojia_url = mongoservice.get_baojia_url()
        for url in baojia_url:
            urls='http://www.autohome.com.cn'+url
            yield Request(urls,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'},callback=self.get_letter)
            yield Request(urls,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'},callback=self.get_url)


    def get_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        ul_info=soup.find_all('ul',class_="interval01-list")
        if ul_info:
            for ul in ul_info:
                li_info=ul.find_all('li')
                for li in li_info:
                    href=li.find('a').get('href')
                    urls='http://www.autohome.com.cn'+href
                    yield Request(urls,callback=self.get_url)


    def get_url(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        result = AutohomeBaojiaUrl()
        breadnav=soup.find('div',class_="breadnav fn-left")
        if breadnav:
            address=breadnav.get_text().strip()
            add = address.split('：')
            result['address']=add[1]
        tit=soup.find('title').get_text().strip()
        url=response.url
        result['category'] = '报价'
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