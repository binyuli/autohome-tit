# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
from autohome_tit.mongodb import mongoservice
import json


class AutohomeDealerlistSpider(RedisSpider):
    name='autohome_dealerlist'
    api_url='http://dealer.autohome.com.cn/china#pvareaid=2113384'
    dealer='http://dealer.autohome.com.cn/china?countyId=0&brandId=0&seriesId=0&factoryId=0&pageIndex=%d&kindId=1&orderType=0'

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
        result=dict()
        header_nav=soup.find('div',class_="header-nav").find('ul',class_="nav-ul")
        nav_1=header_nav.find('li',id="nav_1")
        if nav_1:
            price=nav_1.find('a').get('href')
            result['price']=price

        nav_2=header_nav.find('li',id="nav_2")
        if nav_2:
            newslist=nav_2.find('a').get('href')
            result['newslist']=newslist

        nav_3=header_nav.find('li',id="nav_3")
        if nav_3:
            informationList=nav_3.find('a').get('href')
            result['informationList']=informationList

        nav_4=header_nav.find('li',id="nav_4")
        if nav_4:
            info=nav_4.find('a').get('href')
            result['info']=info

        nav_35=header_nav.find('li',id="nav_35")
        if nav_35:
            maintain=nav_35.find('a').get('href')
            result['maintain']=maintain

        nav_5=header_nav.find('li',id="nav_5")
        if nav_5:
            salerlist=nav_5.find('a').get('href')
            result['salerlist']=salerlist
        url=response.url
        number = filter(str.isdigit, url)
        result['dealer_id']=str(number)
        put_result = json.dumps(dict(result), ensure_ascii=False, sort_keys=True, encoding='utf8').encode('utf8')
        save_result = json.loads(put_result)
        # put_result = json.dumps(dict(result), ensure_ascii=False, sort_keys=True, encoding='utf8').encode('utf8')
        # open('autohome_tit/dealer', 'a').write(put_result + '\n')
        mongoservice.save_dealerlist(save_result)


    def spider_idle(self):
        """This function is to stop the spider"""
        req = self.next_requests()
        if req:
            self.schedule_next_requests()
        else:
            self.crawler.engine.close_spider(self, reason='finished')
