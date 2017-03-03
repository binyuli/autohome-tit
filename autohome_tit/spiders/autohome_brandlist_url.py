# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from bs4 import BeautifulSoup
import json
import re
from autohome_tit.mongodb import mongoservice

class AutohomeBrandListUrlSpider(RedisSpider):
    name="autohome_brandlist"
    get_brand_url = 'http://www.autohome.com.cn/car/?pvareaid=101452'
    api_brand_url = 'http://www.autohome.com.cn/grade/carhtml/%s.html'


    def start_requests(self):
        yield Request(self.get_brand_url, callback=self.get_brand_letter)


    def get_brand_letter(self, response):
        soup = BeautifulSoup(response.body)
        div_info = soup.find('div', id='tab-content-item1')
        ul_info = div_info.find('ul', class_='find-letter-list')
        li_info = ul_info.find_all('li')
        for li in li_info:
            brand_letter = li.get_text().strip()
            yield Request(self.api_brand_url % brand_letter, callback=self.get_brand_list)


    def get_brand_list(self, response):
        info = response.body
        soup = BeautifulSoup(info, 'lxml')
        dl_info = soup.find_all('dl')
        for dl in dl_info:
            href = dl.find('dt').find('a').get('href')
            bids = re.findall(r"brand-(.+?).html", href)
            bid = bids[0]
            li_info = dl.find_all('li', id=True)
            for li in li_info:
                hrefs=li.find('h4').find('a').get('href')
                m = re.search('(\d+)', li['id'])
                cid = m.group(1)
                yield Request(hrefs,meta={'bid':bid,'cid':cid},callback=self.get_car_info)


    def get_car_info(self,response):
        info = response.body_as_unicode()
        soup = BeautifulSoup(info, 'lxml')
        bid=response.meta['bid']
        cid=response.meta['cid']
        result= dict()
        models_nav=soup.find('div',class_="models_nav")
        if models_nav:
            models_info=models_nav.find_all('a')
            koubei_url=models_info[0].get('href')
            config_url=models_info[1].get('href')
            pic_url=models_info[2].get('href')
            article_url=models_info[3].get('href')
            used_car_url=models_info[4].get('href')
            forum_url=models_info[5].get('href')

            result['koubei_url'] = koubei_url
            result['config_url'] = 'http://www.autohome.com.cn/'+config_url
            result['pic_url'] = pic_url
            result['article_url'] = article_url
            result['used_car_url'] = used_car_url
            result['forum_url'] = forum_url
            result['bid'] = bid
            result['cid'] = cid
            put_result = json.dumps(dict(result), ensure_ascii=False, sort_keys=True, encoding='utf8').encode('utf8')
            save_result = json.loads(put_result)
            mongoservice.save_brandlist(save_result)

        nav_top=soup.find('div',id='navTop')
        if nav_top:
            li_info=nav_top.find('ul').find_all('li')

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

            detailed_vehicle = li_info[5].find('a')
            if detailed_vehicle:
                href = detailed_vehicle.get('href')
                detailed_vehicle_url='http://www.autohome.com.cn%s'%href
                result['detailed_vehicle_url'] = detailed_vehicle_url

            article = li_info[6].find('a')
            if article:
                article_url = article.get('href')
                result['article_url'] = article_url

            video = li_info[7].find('a')
            if video:
                video_url = video.get('href')
                result['video_url'] = video_url

            used_car = li_info[8].find('a')
            if used_car:
                used_car_url = used_car.get('href')
                result['used_car_url'] = used_car_url

            price_car = li_info[9].find('a')
            if price_car:
                price_car_url = price_car.get('href')
                result['price_car_url'] = price_car_url

            zhidao = li_info[10].find('a')
            if zhidao:
                zhidao_url = zhidao.get('href')
                result['zhidao_url'] =zhidao_url

            forum = li_info[11].find('a')
            if forum:
                forum_url = forum.get('href')
                result['forum_url'] = forum_url
            result['bid']=bid
            result['cid']=cid
            put_result = json.dumps(dict(result), ensure_ascii=False, sort_keys=True, encoding='utf8').encode('utf8')
            save_result = json.loads(put_result)
            mongoservice.save_brandlist(save_result)


    def spider_idle(self):
        """This function is to stop the spider"""
        req = self.next_requests()
        if req:
            self.schedule_next_requests()
        else:
            self.crawler.engine.close_spider(self, reason='finished')



