# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings
from scrapy import log
import functools
from scrapy.exceptions import DropItem


def check_spider_pipeline(process_item_method):

    """
    此方法用于检验不同的spider所对应处理item的pipeline
    :param process_item_method:
    :return:
    """
    @functools.wraps(process_item_method)
    def wrapper(self, item, spider):

        # message template for debugging
        msg = '%%s %s pipeline step' % (self.__class__.__name__,)

        # if class is in the spider's pipeline, then use the
        # process_item method normally.
        if self.__class__ in spider.pipeline:
            # print(spider.pipeline)
            spider.log(msg % 'executing', level=log.DEBUG)
            return process_item_method(self, item, spider)

        # otherwise, just return the untouched item (skip this step in
        # the pipeline)
        else:
            # spider.log(msg % 'skipping', level=log.DEBUG)
            return item

    return wrapper

class KoubeiPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['AutohomeKoubei']

    @check_spider_pipeline
    def process_item(self, item, spider):
        result = dict(item)
        url = result['url']
        urls = self.collection.find_one({'url': url})
        if not urls:
            self.collection.insert(result)
            log.msg("BrandInfoItem %s create to mongodb database!" % url, level=log.DEBUG, spider=spider)

        else:
            # brand同样一旦检测到id存在,直接丢弃掉
            return DropItem
            log.DEBUG("The brand has existed")

        return item


class BaojiaPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['Baojia']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item


class ConfigPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['Config']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item


class ArticlePipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['Article']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class BrandInfoPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['BrandInfo']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class DetaileVehiclePipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['DetaileVehicle']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class ForumPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['Forum']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item


class ForumsPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['Forums']

    @check_spider_pipeline
    def process_item(self, item, spider):
        result = dict(item)
        id = result['id']
        fid = self.collection.find_one({'id': id})
        if not fid:
            self.collection.insert(dict(item))
            log.msg("ForumItem add to mongodb database!", level=log.DEBUG, spider=spider)
        else:
            return DropItem
        return item

class PicturePipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['Picture']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class ShuokePipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['Shuoke']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class BaikePipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['Baike']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class UsedcarPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['Usedcar']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class VideoPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['Video']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class YouchuangPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['Youchuang']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class ZhidaoPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['Zhidao']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class IndexPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['Index']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item


class CarstorePipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['CarStore']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item


class OwnerpricePipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['OwnerPrice']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class DealerPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['Dealer']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item


class DealerpricePipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['Dealerprice']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item


class DealernewsPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['Dealernews']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item


class DealerinformationPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['DealerInformation']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item


class DealerinfoPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['DealerInfo']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class DealermaintainPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['Dealermaintain']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class DealersalerlistPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['Dealersalerlist']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class VehicleconfigPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['VehicleConfig']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class VehiclePicPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['VehiclePic']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class VehicleBaojiaPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['VehicleBaojia']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item


class VehicleKoubeiPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['VehicleKoubei']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item


class VehicleCarpricePipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db['VehicleCarprice']

    @check_spider_pipeline
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item