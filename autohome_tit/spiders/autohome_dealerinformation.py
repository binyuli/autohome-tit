# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import  Request
from bs4 import BeautifulSoup
from autohome_tit.mongodb import mongoservice
from autohome_tit.items import AutohomeDealerinformationUrl
from autohome_tit import pipelines

class AutohomeDealerinformatioSpider(RedisSpider):
    name = 'autohome_dealerinformation'
    api_url = 'http://dealer.autohome.com.cn%s'
    pipeline = set([pipelines.DealerinformationPipeline, ])


    def start_requests(self):
        # fi=open('autohome_tit/dealer','r')
        # for line in fi:
        #     brand_info=eval(line)
        #     if brand_info.has_key('informationList') :
        #         url = brand_info['informationList']
        #         dealer_id = brand_info['dealer_id']
        #         yield Request(self.api_url % url, meta={'dealer_id': dealer_id}, callback=self.get_page_list)
        #         yield Request(self.api_url % url, callback=self.get_url)
        news_list = mongoservice.get_dealerinformation_url()
        for news in news_list:
            url=news['informationList']
            dealer_id=news['dealer_id']
            yield Request(self.api_url%url,meta={'dealer_id':dealer_id},callback=self.get_letter)
            yield Request(self.api_url%url, callback=self.get_url)


    def get_page_list(self,response):
        dealer_id=response.meta['dealer_id']
        soup = BeautifulSoup(response.body_as_unicode(), 'lxml')
        pageinfo=soup.find('div',class_="page dealer-page").find('span',class_="grey-999").get_text().strip()
        page_amount = pageinfo[1:-1]
        for page_num in range(int(page_amount)+1):
            url='http://dealer.autohome.com.cn/%s/informationList_c0_s0_p%d.html#newlist'%(dealer_id,page_num)
            yield Request(url,callback=self.get_letter)


    def get_letter(self,response):
        soup = BeautifulSoup(response.body_as_unicode())
        dl_info=soup.find('div',class_="dealeron-cont").find_all('dl',class_="promot-dl new-dl")
        for dl in dl_info:
            href=dl.find('dd').find('p',class_="name font-yh").find('a').get('href')
            yield Request(self.api_url%href,callback=self.get_url)


    def get_url(self, response):
        soup = BeautifulSoup(response.body_as_unicode(), 'lxml')
        url = response.url
        tit = soup.find('title').get_text().strip()
        result = AutohomeDealerinformationUrl()
        hotcar = soup.find('div', id="hotcar")
        if hotcar:
            hot_car = hotcar.get_text().strip()
            if '：' in hot_car:
                car = hot_car.split('：')
                result['hot_car'] = car[1]
        breadnav = soup.find('div', id="breadnav")
        if breadnav:
            bread_nav = breadnav.get_text().strip()
            add = bread_nav.split('：')
            result['address'] = add[1]
        result['category'] = '经销商-新闻资讯'
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
