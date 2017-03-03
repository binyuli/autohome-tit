# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
from autohome_tit.items import AutohomeDealerUrl
from autohome_tit import pipelines


class AutohomeDealerSpider(RedisSpider):
    name='autohome_dealer'
    api_url='http://dealer.autohome.com.cn/china#pvareaid=2113384'
    dealer='http://dealer.autohome.com.cn/china?countyId=0&brandId=0&seriesId=0&factoryId=0&pageIndex=%d&kindId=1&orderType=0'
    pipeline = set([pipelines.DealerPipeline, ])

    def start_requests(self):
        yield Request(self.api_url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'},callback=self.get_letter)


    def get_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        pagemount=re.findall(r'var dealerCount = (.+?);',str(soup))
        page_mount=int(pagemount[0])
        for page_num in range(1, page_mount + 1):
            url=self.dealer%page_num
            yield Request(url,callback=self.get_dealer_url)


    def get_dealer_url(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        list_box=soup.find('div',class_="dealer-list-wrap").find('ul',class_="list-box")
        if list_box:
            li_info=list_box.find_all('li',class_="list-item")
            for li in li_info:
                href=li.find('a').get('href')
                yield Request(href,callback=self.get_url)


    def get_url(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        tit=soup.find('title').get_text().strip()
        url=response.url
        result=AutohomeDealerUrl()
        breadnav=soup.find('div',id="breadnav")

        if breadnav:
            bread_nav=breadnav.get_text().strip()
            address = bread_nav.split('：')
            result['address'] = address[1]
        else:
            result['address'] = ''
        hotcar=soup.find('div',id="hotcar")
        if hotcar:
            hot_car=hotcar.get_text().strip()
            car=hot_car.split('：')
            result['hot_car']=car[1]
        result['category'] = '经销商'
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
