# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
from autohome_tit.items import AutohomeUsedCarUrl
from autohome_tit.mongodb import mongoservice
from autohome_tit import pipelines


class AutohomeUsedCarUrlSpider(RedisSpider):
    name='autohome_usedcar'
    api_car_page = 'a0_0msdgscncgpi1ltocsp%dexx0/'
    api_car = 'http://www.che168.com%s'
    pipeline = set([pipelines.UsedcarPipeline, ])


    def start_requests(self):
        used_car_url=mongoservice.get_used_car_url()
        for url in used_car_url:
            yield Request(url,callback=self.get_letter)
            yield Request(url,callback=self.get_url)


    def get_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode(), 'lxml')
        if 'list' in response.url:
            return
        page_info = soup.find('div',id="listpagination")
        if not page_info:
            page_amount = 1
        else:
            nums=page_info.find_all('a')
            num=nums[-2].get_text().strip()
            m=int(num)
            if not m:
                page_amount = 1
            else:
                page_amount = m

        for page_num in range(1, page_amount + 1):
            url = response.url
            if '?' in response.url:
                urls = url.split('?')
                page_url = urls[0] + self.api_car_page % page_num
            else:
                page_url = url + self.api_car_page % page_num
            yield Request(page_url, dont_filter=True, callback=self.get_indice_usedcar)


    def get_indice_usedcar(self, response):
        soup = BeautifulSoup(response.body_as_unicode(), 'lxml')
        div_info = soup.find('div', id="a2")
        if not div_info:
            return
        ul_info = div_info.find('ul', class_='fn-clear')
        li_info = ul_info.find_all('li', infoid=True)
        for li in li_info:
            usedcar_url = li.find('a', target='_blank')['href']
            url='http://www.che168.com'+usedcar_url
            yield Request(url,callback=self.get_url)


    def get_url(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        tits=soup.find('title')
        if tits:
            tit=soup.find('title').get_text().strip()
            url=response.url
            result=AutohomeUsedCarUrl()
            breadnav=soup.find('div',class_="breadnav content")
            if breadnav:
                bread_nav=breadnav.get_text().strip()
                result['address'] = bread_nav
            result['category'] = '二手车'
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





