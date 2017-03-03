# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
from autohome_tit.items import AutohomeShuoKeurlItem
from autohome_tit import pipelines

class AutohomeShuoKeSpider(RedisSpider):
    name="autohome_shuoke"
    get_url="http://shuoke.autohome.com.cn/#pvareaid=103410"
    pipeline = set([pipelines.ShuokePipeline, ])


    def start_requests(self):
        yield Request(self.get_url,callback=self.get_shuoke)


    def get_shuoke(self,response):
        info = response.body_as_unicode()
        soup = BeautifulSoup(info)
        nav_channel=soup.find('div',class_="nav-channel")
        if nav_channel:
            article=nav_channel.find('li',id="li2").find('a').get('href')
            tag=nav_channel.find('li',id="li3").find('a').get('href')
            author=nav_channel.find('li',id="li4").find('a').get('href')

            yield Request(article,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'},callback=self.get_urls)
            yield Request(tag,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'},callback=self.get_urls)
            yield Request(author,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'},callback=self.get_urls)

            yield Request(article, headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'},callback=self.get_article)
            yield Request(tag, headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'},callback=self.get_tag)


        num=soup.find('span',class_="page-item-info").get_text().strip()
        n=int(num[1:-1])
        if not n:
            page_amount = 1
        else:
            page_amount = n
        for page_num in range(1, page_amount + 1):
            url='http://shuoke.autohome.com.cn/%d/'%page_num
            yield Request(url,callback=self.get_shuoke_url)



    def get_shuoke_url(self,response):
        info = response.body_as_unicode()
        soup = BeautifulSoup(info)
        articleList=soup.find('ul',id="articleList")
        if articleList:
            li_info=articleList.find_all('li')
            for li in li_info:
                infos=li.find('div',class_="info-list-pic")
                if infos:
                    href=infos.find('a').get('href')
                    yield Request(href,callback=self.get_urls)


    def get_article(self,response):
        info = response.body_as_unicode()
        soup = BeautifulSoup(info)
        page_info=soup.find('span',class_="page-item-info")
        if page_info:
            num=page_info.get_text().strip()
            n = int(num[1:-1])
            if not n:
                page_amount = 1
            else:
                page_amount = n
            for page_num in range(1, page_amount + 1):
                url='http://shuoke.autohome.com.cn/article/page-%d/'%page_num
                yield Request(url,callback=self.get_article_url)


    def get_article_url(self,response):
        info = response.body_as_unicode()
        soup = BeautifulSoup(info)
        info_list=soup.find('ul',class_="info-list infoThing mt15")
        if info_list:
            li_info=info_list.find_all('li')
            for li in li_info:
                href=li.find('a').get('href')
                yield Request(href,callback=self.get_urls)


    def get_tag(self, response):
        info = response.body_as_unicode()
        soup = BeautifulSoup(info)
        theme_list=soup.find('div',class_="label-theme-list")
        if theme_list:
            dl_info=theme_list.find_all('dl')
            for dl in dl_info:
                a_info=dl.find('dd').find_all('a')
                for href_info in a_info:
                    href=href_info.get('href')
                    url='http://shuoke.autohome.com.cn%s'%href
                    yield Request(url,callback=self.get_urls)


    def get_urls(self,response):
        info = response.body_as_unicode()
        soup = BeautifulSoup(info)
        result=AutohomeShuoKeurlItem()
        breadnav=soup.find('div',class_="breadnav")
        if breadnav:
            bread_nav=breadnav.get_text().strip()
            add = bread_nav.split('：')
            result['address'] = add[1]
        url=response.url
        tit=soup.find('title').get_text().strip()
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