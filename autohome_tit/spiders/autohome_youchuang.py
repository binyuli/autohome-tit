# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
from autohome_tit.items import AutohomeYouChuangurlItem
from autohome_tit import pipelines

class AutohomeYouChuangSpider(RedisSpider):
    name="autohome_youchuang"
    get_url="http://youchuang.autohome.com.cn/#pvareaid=2125196"
    pipeline = set([pipelines.YouchuangPipeline, ])


    def start_requests(self):
        yield Request(self.get_url,callback=self.get_page)


    def get_page(self,response):
        info = response.body_as_unicode()
        soup = BeautifulSoup(info)
        inheadleft=soup.find('div',class_="inheadleft")
        inheadul=inheadleft.find('ul',class_="inheadul")
        if inheadul:
            authorlist_link=inheadul.find('li',class_="authorlist-link").find('a').get('href')
            notice=inheadul.find('a',id="nav-notice").get('href')
            authorlist_url='http://youchuang.autohome.com.cn/'+authorlist_link
            notice_url='http://youchuang.autohome.com.cn/'+notice
            yield Request(authorlist_url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'},callback=self.get_page_authorlist)
            yield Request(authorlist_url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'},callback=self.get_urls)
            yield Request(notice_url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'},callback=self.get_urls)
        bigpage=soup.find('div',class_="bigpage")
        if bigpage:
            href_info=bigpage.find_all('a')
            num=href_info[-2].get_text().encode('utf-8')
            n = int(num)
            if not n:
                page_amount = 1
            else:
                page_amount = n
            for page_num in range(1, page_amount + 1):
                urls='http://youchuang.autohome.com.cn/?type=2&page=%d&pagesize=15'%page_num
                yield Request(urls,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'},callback=self.get_youchuang)

    def get_page_authorlist(self,response):
        info = response.body_as_unicode()
        soup = BeautifulSoup(info)
        page_info=soup.find('div',class_="pagination")
        if not page_info:
            page_amount = 1
        else:
            m = page_info[-2].get_text().strip()
            if not m:
                page_amount = 1
            else:
                page_amount = int(m)
        for page_num in range(1, page_amount + 1):
            page_url = '%s?page=%d' % (response.url, page_num)
            yield Request(page_url,callback=self.get_page_authorlist)


    def get_authorlist_url(self,response):
        info = response.body_as_unicode()
        soup = BeautifulSoup(info)
        authorlist=soup.find('div',class_="authorlist mt12")
        if authorlist:
            dl_info=authorlist.find_all('dl')
            for dl in dl_info:
                href=dl.find('dt').find('a',class_="amallimg").get('href')
                url='http://youchuang.autohome.com.cn%s'%href
                yield Request(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'},callback=self.get_urls)
                yield Request(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'},callback=self.get_urls)


    def get_page_author(self,response):
        info = response.body_as_unicode()
        soup = BeautifulSoup(info)
        url = response.url
        urls = url.split('#')
        page_info=soup.find('div',class_="bigpage")
        if not page_info:
            page_amount = 1
        else:
            m = page_info[-2].get_text().strip()
            if not m:
                page_amount = 1
            else:
                page_amount = int(m)
        for page_num in range(1, page_amount + 1):
            page_url = '%s?InfoType=0&page=%d&pagesize=20' % (urls[0], page_num)
            yield Request(page_url,callback=self.get_author)


    def get_author(self,response):
        info = response.body_as_unicode()
        soup = BeautifulSoup(info)
        ul_info=soup.find('ul',id="response_flow")
        if ul_info:
            li_info=ul_info.find_all('li')
            for li in li_info:
                href=li.find('div',class_="waterfall-link").find('a').get('href')
                url='http://youchuang.autohome.com.cn/'+href
                yield Request(url,callback=self.get_urls)


    def get_youchuang(self,response):
        info = response.body_as_unicode()
        soup = BeautifulSoup(info)
        card_content=soup.find_all('div',class_="card-contents")
        for card in card_content:
            href=card.find('a').get('href')
            url='http://youchuang.autohome.com.cn%s'%href
            yield Request(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'},callback=self.get_urls)


    def get_urls(self,response):
        info = response.body_as_unicode()
        soup = BeautifulSoup(info)
        url=response.url
        tit=soup.find('title').get_text().strip()
        result=AutohomeYouChuangurlItem()

        article_current=soup.find('div',class_="article-current")
        if article_current:
            text=article_current.get_text().strip()
            add = text.split('：')
            result['address'] = add[1]
        result['category'] = '优创'
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