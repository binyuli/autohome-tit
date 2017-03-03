# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
from autohome_tit.mongodb import mongoservice


class AutohomeVehicleListSpider(RedisSpider):
    name='autohome_vehiclelist'

    def start_requests(self):
        baojia_url = mongoservice.get_baojia_url()
        for url in baojia_url:
            urls='http://www.autohome.com.cn'+url
            yield Request(urls,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'},callback=self.get_letter)


    def get_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        ul_info=soup.find_all('ul',class_="interval01-list")
        if ul_info:
            for ul in ul_info:
                li_info=ul.find_all('li')
                for li in li_info:
                    href=li.find('a').get('href')
                    urls='http://www.autohome.com.cn'+href
                    yield Request(urls,callback=self.get_url)


    def get_url(self,response):
        result = dict()
        soup = BeautifulSoup(response.body_as_unicode())
        nav_typebar=soup.find('div',class_="nav-typebar nav-typebar-g12 fn-clear")
        li_info=nav_typebar.find('ul').find_all('li')

        config = li_info[1].find('a')
        if config:
            config_url = config.get('href')
            result['config_url'] = config_url

        pic = li_info[2].find('a')
        if pic:
            pic_url = pic.get('href')
            result['pic_url'] = pic_url

        baojia = li_info[3].find('a')
        if baojia:
            baojia_url = baojia.get('href')
            result['baojia_url'] = baojia_url

        koubei = li_info[4].find('a')
        if koubei:
            koubei_url = koubei.get('href')
            result['koubei_url'] = koubei_url

        price_car = li_info[8].find('a')
        if price_car:
            price_car_url = price_car.get('href')
            result['price_car_url'] = price_car_url

        mongoservice.save_Vehiclelist(result)


    def spider_idle(self):
        """This function is to stop the spider"""
        req = self.next_requests()
        if req:
            self.schedule_next_requests()
        else:
            self.crawler.engine.close_spider(self, reason='finished')