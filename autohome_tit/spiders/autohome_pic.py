# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import  Request
from bs4 import BeautifulSoup
from autohome_tit.mongodb import mongoservice
from autohome_tit.items import AutohomePicUrl
from autohome_tit import pipelines
import math
import json

class AutohomePicUrlSpider(RedisSpider):
    name = 'autohome_pic'
    pic_url='http://car.autohome.com.cn%s'
    pipeline = set([pipelines.PicturePipeline, ])

    def start_requests(self):
        picture_urls = mongoservice.get_pic_url()
        for url in picture_urls:
            yield Request(url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'}, callback=self.get_pic_letter)
            yield Request(url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'}, callback=self.get_url)


    def get_pic_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        choise_cont=soup.find('div',class_="choise-cont ma-b-10")
        if choise_cont:
            cont_text=choise_cont.find('div',class_='choise-cont-text')
            a_info=cont_text.find_all('a')
            for href in a_info:
                url=href.get('href')
                text=href.get_text().strip()
                t=text.split('(')
                acount=t[1][:-1]
                urls='http://car.autohome.com.cn%s'%url
                yield Request(urls,meta={'acount':acount},callback=self.get_page_list)
                yield Request(urls,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'},callback=self.get_url)


    def get_page_list(self,response):
        acount=response.meta['acount']
        pageacount=math.ceil(int(acount)/60)
        page_acount=int(pageacount)
        url=response.url
        pageurl=url.split('.html')
        for page_num in range(page_acount+1):
            urls='%s-p%d.html'%(pageurl[0],page_num+1)
            yield Request(urls,callback=self.get_pic)


    def get_pic(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        row_info=soup.find_all('div',class_="row")
        uibox=row_info[-1].find('div',class_="uibox")
        if uibox:
            li_info=uibox.find('ul').find_all('li')
            for li in li_info:
                href=li.find('a').get('href')
                yield Request(self.pic_url%href,callback=self.get_url)


    def get_url(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        tit=soup.find('title').get_text().strip()
        url=response.url
        result=AutohomePicUrl()
        breadnav=soup.find('div',class_="breadnav")
        if breadnav:
            bread_nav=breadnav.get_text().strip()
            if '：' in bread_nav:
                add = bread_nav.split('：')
                result['address'] = add[1]
            else:
                result['address'] = bread_nav

        result['category'] = '车型图片'
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
