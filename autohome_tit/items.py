# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class AutohomeTitItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class AutohomeUrlItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category=Field()


class AutohomeArticleurlItem(Item):
    tit=Field()
    url=Field()
    address=Field()
    category = Field()


class AutohomeYouChuangurlItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()


class AutohomeShuoKeurlItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()


class AutohomeBaikeUrlItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()


class AutohomeBrandInfoUrlItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()


class AutohomeBrandConfigUrlItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()


class AutohomeVehicleConfigUrlItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()


class AutohomeVehiclePicUrlItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class AutohomeVehicleCarpriceItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class AutohomeVehiclebaojiaItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class AutohomeVehicleKoubeiItem(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class AutohomeDetailedVehicleUrl(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()


class AutohomePicUrl(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class AutohomeUsedCarUrl(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class AutohomeVideoUrl(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class AutohomeZhidaoUrl(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class AutohomeKoubeiUrl(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()
    author_name = Field()
    author_id = Field()
    eval_time = Field()

class AutohomeForumUrl(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class AutohomeBaojiaUrl(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class AutohomeOwnerpriceUrl(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class AutohomeCarStoreUrl(Item):
    tit=Field()
    url=Field()
    address = Field()
    category = Field()

class AutohomeDealerUrl(Item):
    tit=Field()
    url=Field()
    address = Field()
    hot_car=Field()
    category = Field()

class AutohomeDealerpriceUrl(Item):
    tit=Field()
    url=Field()
    address = Field()
    hot_car = Field()
    category = Field()


class AutohomeDealernewsUrl(Item):
    tit=Field()
    url=Field()
    address = Field()
    hot_car = Field()
    category = Field()


class AutohomeDealerinformationUrl(Item):
    tit=Field()
    url=Field()
    address = Field()
    hot_car = Field()
    category = Field()

class AutohomeDealerinfoUrl(Item):
    tit=Field()
    url=Field()
    address = Field()
    hot_car = Field()
    category = Field()


class AutohomeDealermaintainUrl(Item):
    tit=Field()
    url=Field()
    address = Field()
    hot_car = Field()
    category = Field()

class AutohomeDealersalerlistUrl(Item):
    tit=Field()
    url=Field()
    address = Field()
    hot_car = Field()
    category = Field()


class AutohomeForumsUrl(Item):
    tit=Field()
    url=Field()
    id=Field()
    name=Field()
    category = Field()




