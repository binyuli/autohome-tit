# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import  Request
from bs4 import BeautifulSoup
import re
from autohome_tit.mongodb import mongoservice
from autohome_tit.items import AutohomeForumsUrl
from autohome_tit import pipelines
import datetime
import redis
from scrapy.conf import settings

class AutohomeForumsSpider(RedisSpider):
    name = 'autohome_forums'
    api_forum_page = 'http://club.autohome.com.cn/bbs/forum-c-%d-%d.html?qaType=-1#pvareaid=101061'
    forum_url = 'http://club.autohome.com.cn/#pvareaid=103419'
    api_forum='http://club.autohome.com.cn%s'
    pipeline = set([pipelines.ForumsPipeline, ])


    def start_requests(self):
        yield Request(self.forum_url, callback=self.get_forum_list)


    def get_forum_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        forum_tab=soup.find_all('div',class_="forum-tab-box")
        for forum in forum_tab:
            forum_list=forum.find('ul',class_="forum-list")
            a_info=forum_list.find_all('a')
            for infos in a_info:
                href=infos.get('href')
                m = re.search('(\d+)', href)
                name=infos.get_text().strip()
                yield Request(self.api_forum%href,meta={'id': m.group(1),'name':name},callback=self.get_infos)

        forum_brand=soup.find('div',id="tab-4").find('div',class_="forum-tab-box").find('div',class_="forum-brand-box")
        ul_info=forum_brand.find_all('ul',class_="forum-list02")
        for ul in ul_info:
            brand_list=ul.find_all('a')
            for brand in brand_list:
                url=brand.get('href')
                id = re.search('(\d+)', url)
                names = brand.get_text().strip()
                yield Request(self.api_forum % url, meta={'id': id.group(1), 'name': names}, callback=self.get_infos)

    def get_infos(self, response):
        soup = BeautifulSoup(response.body_as_unicode())
        id=response.meta['id']
        name=response.meta['name']
        url = response.url
        tit = soup.find('title').get_text().strip()
        result = AutohomeForumsUrl()
        result['category'] = '论坛'
        result['name'] = name
        result['id'] = id
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