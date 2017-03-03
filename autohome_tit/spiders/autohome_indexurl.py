# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
from autohome_tit.items import AutohomeUrlItem
from autohome_tit import pipelines


class AutohomeUrlSpider(RedisSpider):
    name = "autohome_brandurl"
    brand_url="http://www.autohome.com.cn/beijing/"
    pipeline = set([pipelines.IndexPipeline])

    def start_requests(self):
        yield Request(self.brand_url,callback=self.get_brand_letter)


    def get_brand_letter(self, response):
        info = response.body_as_unicode()
        soup = BeautifulSoup(info)
        a_info=soup.find('ul',class_="choose-car").find('a')
        href=a_info.get('href')
        li_info=soup.find('div',class_="navlink").find_all('a')
        for li in li_info:
            url=li.get('href')
            if url!="javascript:void(0);":
                yield Request(url,callback=self.get_url)

        ul_info=soup.find('div',class_="navcar").find('ul').find_all('a')
        for ul in ul_info:
            car_url=ul.get('href')
            yield Request(car_url,callback=self.get_url)
        yield Request(href,callback=self.get_url)


    def get_url(self,response):
        info = response.body
        soup = BeautifulSoup(info)
        result = AutohomeUrlItem()
        title = soup.find('title')
        if title:
            tit=title.get_text().strip()
            url=response.url
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
