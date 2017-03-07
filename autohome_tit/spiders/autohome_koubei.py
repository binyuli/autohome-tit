# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import re
from autohome_tit.mongodb import mongoservice
from autohome_tit.items import AutohomeKoubeiUrl
from autohome_tit import pipelines
import json

class AutohomeKoubeiSpider(RedisSpider):
    name="autohome_koubei"
    pipeline = set([pipelines.KoubeiPipeline, ])


    def start_requests(self):
        koubei_urls = mongoservice.get_koubei_url()
        # koubei_urls = mongoservice.get_koubei_start_url()
        for url in koubei_urls:
            yield Request(url,callback=self.get_pages_koubei)
            # yield Request(url,callback=self.get_koubei)


    def get_pages_koubei(self, response):
        soup = BeautifulSoup(response.body_as_unicode(), 'lxml')
        page_info = soup.find('span', class_='page-item-info')
        if not page_info:
            page_amount = 1
        else:
            m = re.search('(\d+)', page_info.get_text())
            if not m:
                page_amount = 1
            else:
                page_amount = int(m.group(1))
                if page_amount==0:
                    return
        for page_num in range(1, page_amount + 1):
            if 'stopselling' in response.url:
                page_url = '%s/index_%d.html' % (response.url, page_num)
            else:
                page_url = '%sindex_%d.html' % (response.url, page_num)
            yield Request(page_url, dont_filter=True, callback=self.get_indice_koubei)


    def get_indice_koubei(self, response):
        soup = BeautifulSoup(response.body_as_unicode(), 'lxml')
        div_info = soup.find_all('div', class_='title-name name-width-01')
        # result = dict()
        for div in div_info:
            a = div.find('a')
            koubei_url = a['href']
            yield Request(koubei_url, headers={
                              'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'},
                          callback=self.get_koubei)

            # result['koubei_url'] = koubei_url
            # put_result = json.dumps(dict(result), ensure_ascii=False, sort_keys=True, encoding='utf8').encode('utf8')
            # save_result = json.loads(put_result)
            # mongoservice.save_koubei_list(save_result)

    def get_koubei(self, response):
        result = AutohomeKoubeiUrl()
        info = response.body_as_unicode()
        soup = BeautifulSoup(info, 'lxml')

        # author name,id,evaluate time
        authorName = soup.find('a',id='ahref_UserId')
        if authorName:
            result['author_name'] = authorName.get_text().strip()
        authorId = soup.find('input',id='hidAuthorId')
        if authorId:
            result['author_id'] = authorId.get('value')
        evalTime = soup.find('input',id='hidEvalCreated')
        if evalTime:
            result['eval_time'] = evalTime.get('value')

        # breadnav,url,title
        breadnav = soup.find('div',class_="breadnav")
        if breadnav:
            bread_nav = breadnav.get_text().strip()
            add = bread_nav.split('：')
            result['address'] = add[1]
        tit = soup.find('title').get_text().strip()
        url = response.url
        result['category'] = '车型-口碑'
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