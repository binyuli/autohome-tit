# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
from autohome_tit.items import AutohomeBrandInfoUrlItem
from autohome_tit import pipelines
import json

class AutohomeBrandInfoSpider(RedisSpider):
    name="autohome_brandinfo"
    get_brand_url = 'http://www.autohome.com.cn/car/?pvareaid=101452'
    api_brand_url = 'http://www.autohome.com.cn/grade/carhtml/%s.html'
    pipeline = set([pipelines.BrandInfoPipeline, ])

    def start_requests(self):
        yield Request(self.get_brand_url, callback=self.get_brand_letter)


    def get_brand_letter(self, response):
        soup = BeautifulSoup(response.body)
        div_info = soup.find('div', id='tab-content-item1')
        ul_info = div_info.find('ul', class_='find-letter-list')
        li_info = ul_info.find_all('li')
        for li in li_info:
            brand_letter = li.get_text()
            yield Request(self.api_brand_url % brand_letter,callback=self.get_brand_list)


    def get_brand_list(self, response):
        result=dict()
        info = response.body
        soup = BeautifulSoup(info, 'lxml')
        dl_info = soup.find_all('dl')
        for dl in dl_info:
            li_info = dl.find_all('li', id=True)
            for li in li_info:
                href=li.find('a').get('href')
                result['href']=href
                yield Request(href,callback=self.get_url)


    def get_url(self,response):
        info = response.body_as_unicode()
        soup = BeautifulSoup(info, 'lxml')
        url=response.url
        tit=soup.find('title').get_text().strip()
        result=AutohomeBrandInfoUrlItem()
        breadnav=soup.find('div',class_="breadnav fn-left")
        if breadnav:
            text=breadnav.get_text().strip()
            add = text.split('：')
            result['address'] = add[1]
        result['category'] = '车系首页'
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



