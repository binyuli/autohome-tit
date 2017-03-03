# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
from autohome_tit.items import AutohomeVideoUrl
from autohome_tit.mongodb import mongoservice
from autohome_tit import pipelines

class AutohomeVideoUrlSpider(RedisSpider):
    name='autohome_video'
    pipeline = set([pipelines.VideoPipeline, ])

    def start_requests(self):
        videourl=mongoservice.get_video_url()
        for brand in videourl:
            url=brand['video_url']
            cid=brand['cid']
            yield Request(url,meta={'cid':cid},headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'},callback=self.get_letter)
            yield Request(url,meta={'cid':cid},headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'},callback=self.get_url)


    def get_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode(), 'lxml')
        cid=response.meta['cid']
        page=soup.find('div',class_="page")
        if page:
            page_info=page.find_all('a')
            num=page_info[-2].get_text().strip()
            page_amount=int(num)
            for page_num in range(1, page_amount + 1):
                url='http://car.autohome.com.cn/video/series-%s-0-0-p%d.html'%(cid,page_num)
                yield Request(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'},callback=self.get_video_list)
        else:
            video_list=soup.find('div',id="video-1")
            if video_list:
                li_info=video_list.find('ul',class_="videocont").find_all('li')
                for li in li_info:
                    href=li.find('div',class_="videocont-text").find('a').get('href')
                    yield Request(href,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'},callback=self.get_url)


    def get_video_list(self,response):
        soup = BeautifulSoup(response.body_as_unicode(), 'lxml')
        video_list = soup.find('div', id="video-1")
        if video_list:
            li_info = video_list.find('ul', class_="videocont").find_all('li')
            for li in li_info:
                href = li.find('div', class_="videocont-text").find('a').get('href')
                yield Request(href,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'}, callback=self.get_url)


    def get_url(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        url=response.url
        tit=soup.find('title').get_text().strip()
        result=AutohomeVideoUrl()
        path=soup.find('div',class_="path")
        if path:
            text=path.get_text().strip()
            add = text.split('：')
            result['address'] = add[1]
        result['category'] = '车型-视频'
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