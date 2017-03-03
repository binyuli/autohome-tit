# -*- coding: utf-8 -*-
import scrapy
import scrapy_redis

from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.conf import settings
from scrapy.utils.log import configure_logging

from spiders.autohome_article import AutohomeArticleSpider
from spiders.autohome_baike import AutohomeBaikeSpider
from spiders.autohome_brandinfo import AutohomeBrandInfoSpider
from spiders.autohome_brandlist_url import AutohomeBrandListUrlSpider
from spiders.autohome_detailed_vehicle import AutohomeDetailedVehicleUrlSpider
from spiders.autohome_forum import AutohomeForumSpider
from spiders.autohome_indexurl import AutohomeUrlSpider
from spiders.autohome_koubei import AutohomeKoubeiSpider
from spiders.autohome_pic import AutohomePicUrlSpider
from spiders.autohome_shuoke import AutohomeShuoKeSpider
from spiders.autohome_usedcar import AutohomeUsedCarUrlSpider
from spiders.autohome_video import AutohomeVideoUrlSpider
from spiders.autohome_youchuang import AutohomeYouChuangSpider
from spiders.autohome_zhidao import AutohomeZhiDaoUrlSpider
from spiders.autohome_baojia import AutohomeBaojiaSpider
from spiders.autohome_ownerprice import AutohomeOwnerpriceSpider
from spiders.autohome_dealer import AutohomeDealerSpider
from spiders.autohome_carstore import AutohomeCarStoreSpider
from spiders.autohome_brandconfig import AutohomeConfigSpider
from spiders.autohome_dealerinfo import AutohomeDealerinfoSpider
from spiders.autohome_dealerinformation import AutohomeDealerinformatioSpider
from spiders.autohome_dealerlist import AutohomeDealerlistSpider
from spiders.autohome_dealernews import AutohomeDealernewsSpider
from spiders.autohome_dealerprice import AutohomeDealerpriceSpider
from spiders.autohome_dealersalerlist import AutohomeDealersalerlistSpider
from spiders.autohome_maintain import AutohomeDealermaintainSpider
from spiders.autohome_forums import AutohomeForumsSpider

import os
import pymongo
import json

# the spider we need to scheduler
# ArticleSpider = AutohomeArticleSpider()
# BaikeSpider = AutohomeBaikeSpider()
# BaojiaUrlSpider = AutohomeBaojiaSpider()
# ConfigSpider = AutohomeConfigSpider()
# BrandInfoSpider = AutohomeBrandInfoSpider()
# BrandListUrlSpider = AutohomeBrandListUrlSpider()
# CarStoreSpider = AutohomeCarStoreSpider()
# DealerSpider = AutohomeDealerSpider()
# DealerinfoSpider = AutohomeDealerinfoSpider
# InformatioSpider = AutohomeDealerinformatioSpider()
# DealerlistSpider = AutohomeDealerlistSpider()
# DealernewsSpider = AutohomeDealernewsSpider()
# DealerpriceSpider = AutohomeDealerpriceSpider()
# DealersalerlistSpider = AutohomeDealersalerlistSpider()
# DetailedVehicleUrlSpider = AutohomeDetailedVehicleUrlSpider()
# ForumSpider = AutohomeForumSpider()
# UrlSpider = AutohomeUrlSpider()
KoubeiSpider = AutohomeKoubeiSpider()
# DealermaintainSpider = AutohomeDealermaintainSpider()
# OwnerpriceSpider = AutohomeOwnerpriceSpider()
# PicUrlSpider = AutohomePicUrlSpider()
# ShuoKeSpider = AutohomeShuoKeSpider()
# UsedCarUrlSpider = AutohomeUsedCarUrlSpider()
# VideoUrlSpider = AutohomeVideoUrlSpider()
# YouChuangSpider = AutohomeYouChuangSpider()
# ZhiDaoUrlSpider = AutohomeZhiDaoUrlSpider()
# ForumsSpider = AutohomeForumsSpider()

connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
db = connection[settings['MONGODB_DB']]

configure_logging(settings)
runner = CrawlerRunner(settings)


@defer.inlineCallbacks
def crawl():
    # yield runner.crawl(UrlSpider)
    # yield runner.crawl(BrandListUrlSpider)
    # yield runner.crawl(DealerlistSpider)
    # yield runner.crawl(BrandInfoSpider)
    # yield runner.crawl(BaikeSpider)
    # yield runner.crawl(ArticleSpider)
    # yield runner.crawl(DetailedVehicleUrlSpider)
    # yield runner.crawl(ConfigSpider)
    # # yield runner.crawl(ForumSpider)
    yield runner.crawl(KoubeiSpider)
    # yield runner.crawl(PicUrlSpider)
    # yield runner.crawl(ShuoKeSpider)
    # yield runner.crawl(UsedCarUrlSpider)
    # yield runner.crawl(VideoUrlSpider)
    # yield runner.crawl(YouChuangSpider)
    # yield runner.crawl(ZhiDaoUrlSpider)
    # yield runner.crawl(BaojiaUrlSpider)
    # yield runner.crawl(OwnerpriceSpider)
    # yield runner.crawl(DealerSpider)
    # yield runner.crawl(DealerinfoSpider)
    # yield runner.crawl(InformatioSpider)
    # yield runner.crawl(DealernewsSpider)
    # yield runner.crawl(DealerpriceSpider)
    # yield runner.crawl(DealersalerlistSpider)
    # yield runner.crawl(DealermaintainSpider)
    # yield runner.crawl(CarStoreSpider)
    # yield runner.crawl(ForumsSpider)
    reactor.stop()


crawl()
reactor.run()  # the script will block here until the last crawl call is finished