# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import  Request
from bs4 import BeautifulSoup
import re
from autohome_tit.mongodb import mongoservice
from autohome_tit.items import AutohomeForumUrl
from autohome_tit import pipelines
import datetime
import redis
from scrapy.conf import settings

class AutohomeForumSpider(RedisSpider):
    name = 'autohome_forum'
    api_forum_page = 'http://club.autohome.com.cn/bbs/forum-c-%d-%d.html?qaType=-1#pvareaid=101061'
    forum_url = 'http://club.autohome.com.cn/#pvareaid=103419'
    api_forum = 'http://club.autohome.com.cn%s'
    pipeline = set([pipelines.ForumPipeline, ])


    def __init__(self, *a, **kw):
        RedisSpider.__init__(self)
        self.SETTING_DATE = settings['START_DATE']
        if self.SETTING_DATE:
            filter_mod = settings['FILTER_MOD']
            setting_date = datetime.datetime.strptime(self.SETTING_DATE, '%Y-%m-%d').date()
            self.start_date = str()
            if filter_mod == 'Update':
                re_connection = redis.Redis(host=settings['REDIS_HOST'], port=settings['REDIS_PORT'], db=0)
                update_date = re_connection.hget('time_spider filter', 'last_date')
                if not update_date:
                    self.start_date = setting_date
                else:
                    update_date = datetime.datetime.strptime(update_date, '%Y-%m-%d').date()
                    self.start_date = update_date if (setting_date - update_date).days < 0 else setting_date
            else:  # All
                self.start_date = setting_date


    def start_requests(self):
        forum_urls = mongoservice.get_forum_url()
        for url in forum_urls:
            m = re.search('(\d+)', url)
            yield Request(url, meta={'brand': m.group(1)}, callback=self.get_pages_forum)
            yield Request(url, meta={'brand': m.group(1)}, callback=self.get_url)
        yield Request(self.forum_url, callback=self.get_forum_list)


    def get_forum_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        forum_tab=soup.find_all('div',class_="forum-tab-box")
        for forum in forum_tab[1:]:
            forum_list=forum.find('ul',class_="forum-list")
            a_info=forum_list.find_all('a')
            for infos in a_info:
                href=infos.get('href')
                m = re.search('(\d+)', href)
                yield Request(self.api_forum%href,meta={'brand': m.group(1)},callback=self.get_pages_forum)


    def get_pages_forum(self, response):
        soup = BeautifulSoup(response.body_as_unicode())
        brand=response.meta['brand']
        span_info = soup.find('span', class_='fr')
        if not span_info:
            self.logger.error("论坛翻页标签发生改变,请注意检查! 论坛URL: " + response.url)
            return
        m = re.search('(\d+)', span_info.get_text())
        if not m:
            self.logger.error("论坛翻页标签发生改变,请注意检查! 论坛URL: " + response.url)
            return
        page_amount = int(m.group(1))
        for page_num in range(1, page_amount + 1):
            cid = int(brand)
            yield Request(self.api_forum_page % (cid, page_num),meta={'page_num': page_num}, dont_filter=True, callback=self.get_forums)


    def get_forums(self, response):
        soup = BeautifulSoup(response.body_as_unicode(), 'lxml')
        page_num = response.meta['page_num']
        dl_info = soup.find_all('dl', class_='list_dl', lang=True)
        if not dl_info:
            self.logger.error("没有论坛列表标签,请注意检查! 论坛URL: " + response.url)
        for dl in dl_info:
            if self.SETTING_DATE:
                # latest_reply_time = dl.xpath('.//span[@class="ttime"]/text()').extract_first().strip()
                latest_reply_time = dl.find('span',class_="ttime").get_text().strip()
                if not latest_reply_time:
                    continue
                lr_date = datetime.datetime.strptime(latest_reply_time, '%Y-%m-%d %H:%M').date()
                diff_days = (lr_date - self.start_date).days
                if diff_days < 0:
                    if page_num != 1:
                        return
                    else:
                        continue
            a_info = dl.find('a', href=re.compile('bbs'))
            if not a_info:
                continue
            yield Request('http://club.autohome.com.cn%s' % a_info['href'], callback=self.get_url)

        # carea = response.xpath('//div[@class="carea"]')
        # dl_info = carea.xpath('.//dl[@class="list_dl "]')
        # page_num = response.meta['page_num']
        # if not dl_info:
        #     self.logger.error("There is not forum list tag, please check ! the URL: " + response.url)
        #     return
        # for dl in dl_info:
        #     if self.SETTING_DATE:
        #         latest_reply_time = dl.xpath('.//span[@class="ttime"]/text()').extract_first().strip()
        #         if not latest_reply_time:
        #             continue
        #         lr_date = datetime.datetime.strptime(latest_reply_time, '%Y-%m-%d %H:%M').date()
        #         diff_days = (lr_date - self.start_date).days
        #         if diff_days < 0:
        #             if page_num != 1:
        #                 return
        #             else:
        #                 continue
        #     a_info = dl.xpath('.//a[@class="a_topic"]/@href').extract_first()
        #     if not a_info:
        #         continue
        #     yield Request('http://club.autohome.com.cn%s' % a_info, callback=self.get_url)


    def get_url(self,response):
        soup = BeautifulSoup(response.body_as_unicode(), 'lxml')
        url=response.url
        tit=soup.find('title').get_text().strip()
        result = AutohomeForumUrl()
        result['category'] = '论坛'
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