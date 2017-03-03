# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
from autohome_tit.items import AutohomeArticleurlItem
from autohome_tit import pipelines

class AutohomeArticleSpider(RedisSpider):
    name="autohome_article"
    get_url="http://www.autohome.com.cn/all/#pvareaid=103449"
    pipeline = set([pipelines.ArticlePipeline, ])

    def start_requests(self):
        yield  Request(self.get_url,callback=self.get_letter)


    def get_letter(self,response):
        info = response.body_as_unicode()
        soup = BeautifulSoup(info)
        li_info=soup.find('div',id="ulNav").find_all('li')
        for li in li_info:
            href=li.find('a').get('href')
            yield Request(href,callback=self.get_article_url)
        channelPage=soup.find('div',id="channelPage")
        if channelPage:
            a_info=channelPage.find_all('a')
            num = a_info[-2].get_text().encode('utf-8')
            n = int(num)
            if not n:
                page_amount = 1
            else:
                page_amount = n
            for page_num in range(1, page_amount + 1):
                urls='http://www.autohome.com.cn/all/%d/#liststart'%page_num
                yield Request(urls,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'},callback=self.get_article)


    def get_article(self,response):
        info = response.body_as_unicode()
        soup = BeautifulSoup(info)
        auto_channel=soup.find('div',class_="article-wrapper")
        if auto_channel:
            li_info=auto_channel.find_all('li')
            for li in li_info:
                a_info=li.find('a')
                if a_info:
                    href = a_info.get('href')
                    yield Request(href, headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'},
                                  callback=self.get_article_url)


    def get_article_url(self,response):
        info = response.body_as_unicode()
        result = AutohomeArticleurlItem()
        soup = BeautifulSoup(info)
        breadnav=soup.find('div',class_="breadnav fn-left")
        if breadnav:
            address=breadnav.get_text().strip()
            add=address.split('：')
            result['address']=add[1]
        tit=soup.find('title').get_text().strip()
        url=response.url
        result['category']='article'
        result['url']=url
        result['tit']=tit
        yield result


    def spider_idle(self):
        """This function is to stop the spider"""
        req = self.next_requests()
        if req:
            self.schedule_next_requests()
        else:
            self.crawler.engine.close_spider(self, reason='finished')



