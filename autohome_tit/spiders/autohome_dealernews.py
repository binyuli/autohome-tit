# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import  Request
from bs4 import BeautifulSoup
from autohome_tit.mongodb import mongoservice
from autohome_tit.items import AutohomeDealernewsUrl
from autohome_tit import pipelines

class AutohomeDealernewsSpider(RedisSpider):
    name = 'autohome_dealernews'
    api_url = 'http://dealer.autohome.com.cn%s'
    pipeline = set([pipelines.DealernewsPipeline, ])


    def start_requests(self):
        news_urls = mongoservice.get_dealernews_url()
        for url in news_urls:
            yield Request(self.api_url%url,callback=self.get_letter)
            yield Request(self.api_url%url, callback=self.get_url)


    def get_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode(), 'lxml')
        screen_dl_info=soup.find_all('dl',class_="screen-dl")
        for screen_dl in screen_dl_info:
            dd_info=screen_dl.find('dd',class_="fn-clear").find_all('a')
            for dd in dd_info[1:]:
                url=dd.get('href')
                yield Request(self.api_url % url, callback=self.get_url)


        dl_info=soup.find('div',class_="dealeron-cont").find_all('dl',class_="promot-dl ")
        for dl in dl_info:
            href=dl.find('dd').find('p',class_="name font-yh").find('a').get('href')
            yield Request(self.api_url%href,callback=self.get_url)


    def get_url(self, response):
        soup = BeautifulSoup(response.body_as_unicode(), 'lxml')
        url = response.url
        tit = soup.find('title').get_text().strip()
        result = AutohomeDealernewsUrl()
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
        result['category'] = '经销商-促销信息'
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
