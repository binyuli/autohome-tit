# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
from autohome_tit.items import AutohomeBaikeUrlItem
from autohome_tit import pipelines
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class AutohomeBaikeSpider(RedisSpider):
    name="autohome_shuyu"
    get_url="http://car.autohome.com.cn/shuyu/index.html#pvareaid=103435"
    pipeline = set([pipelines.BaikePipeline, ])


    def start_requests(self):
        yield Request(self.get_url,headers={'User-Agent':'User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'},callback=self.get_letter)

    def get_letter(self,response):
        info = response.body_as_unicode()
        soup = BeautifulSoup(info)
        frame_left=soup.find('div',id="frame_left")
        ul=frame_left.find('ul')
        if ul:
            h3_info=ul.find_all('h3')
            for h3 in h3_info:
                href=h3.find('a').get('href')
                url='http://car.autohome.com.cn'+href
                yield Request(url,headers={'User-Agent':'User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'},callback=self.get_info_url)
                yield Request(url,headers={'User-Agent':'User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'},callback=self.get_baike_url)


    def get_info_url(self,response):
        info = response.body_as_unicode()
        soup = BeautifulSoup(info)
        frame_left = soup.find('div', id="frame_left")
        ul = frame_left.find('ul')
        if ul:
            li_info=ul.find_all('li')
            for li in li_info:
                listtree=li.find('div',class_="listtree")
                if listtree:
                    dl_info=listtree.find('dl').find_all('a')
                    for dl in dl_info:
                        href=dl.get('href')
                        url = 'http://car.autohome.com.cn' + href
                        yield Request(url,headers={'User-Agent':'User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'},callback=self.get_baike_url)


    def get_baike_url(self,response):
        info = response.body_as_unicode()
        result = AutohomeBaikeUrlItem()
        soup = BeautifulSoup(info)
        subnav=soup.find('div',class_="subnav overflow")
        if subnav:
            ul_info=subnav.find('ul',class_="fl subnavul")
            if ul_info:
                text=ul_info.get_text().strip()
                result['address']=text
        else:
            result['address'] = ''
        url=response.url
        tit=soup.find('title').get_text().strip()
        result['category'] = '百科'
        result['url']=url
        result['tit']=tit
        yield result


    def spider_idle(self):
        """This function is to stop the spider"""
        req = self.next_requests()
        if req:
            self.schedule_next_requests()
        else:
            self.crawler.engine.close_spider(self, reason='finished')