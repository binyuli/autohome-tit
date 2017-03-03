# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import  Request
from bs4 import BeautifulSoup
from autohome_tit.mongodb import mongoservice
from autohome_tit.items import AutohomeDealerpriceUrl
from autohome_tit import pipelines

class AutohomeDealerpriceSpider(RedisSpider):
    name = 'autohome_dealerprice'
    api_url = 'http://dealer.autohome.com.cn%s'
    pipeline = set([pipelines.DealerpricePipeline, ])


    def start_requests(self):
        price_urls = mongoservice.get_dealerprice_url()
        for url in price_urls:
            yield Request(self.api_url%url,callback=self.get_letter)
            yield Request(self.api_url%url, callback=self.get_url)


    def get_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode(), 'lxml')
        carprice_info=soup.find_all('div',class_="carprice-cont")
        for carprice in carprice_info:
            dl_info=carprice.find_all('dl',class_="price-dl")
            for dl in dl_info:
                tr_info=dl.find('dd',id="").find('table',class_="list-table").find_all('tr')
                for tr in tr_info:
                    txt_left=tr.find('td', class_="txt-left")
                    if txt_left:
                        href=txt_left.find('a').get('href')
                        yield Request(self.api_url%href,callback=self.get_url)


    def get_url(self, response):
        soup = BeautifulSoup(response.body_as_unicode(), 'lxml')
        url = response.url
        tit = soup.find('title').get_text().strip()
        result = AutohomeDealerpriceUrl()
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
        result['category'] = '经销商-车型报价'
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
