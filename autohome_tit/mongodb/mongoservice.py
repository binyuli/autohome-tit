import pymongo
from scrapy.conf import settings

connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
db = connection[settings['MONGODB_DB']]


def get_carstore_url():
    collection = db['Brand']
    starturls = list()
    for item in collection.find():
        brand = dict()
        if 'cid' in item.keys() and 'bid' in item.keys():
            brand['cid'] = item['cid']
            brand['bid'] = item['bid']
            starturls.append(brand)
    return starturls


def get_koubei_url():
    collection = db['Brand']
    starturls = set()
    for brand in collection.find():
        if 'koubei_url' in brand.keys():
            starturls.add(brand['koubei_url'])
    return starturls


def get_forum_url():
    collection = db['Brand']
    starturls = set()
    for brand in collection.find():
        if 'forum_url' in brand.keys():
            starturls.add(brand['forum_url'])
    return starturls


def get_pic_url():
    collection = db['Brand']
    starturls = set()
    for brand in collection.find():
        if 'pic_url' in brand.keys():
            starturls.add(brand['pic_url'])
    return starturls

def get_baojia_url():
    collection = db['Brand']
    starturls = set()
    for brand in collection.find():
        if 'baojia_url' in brand.keys():
            starturls.add(brand['baojia_url'])
    return starturls


def get_article_url():
    collection = db['Brand']
    starturls = set()
    for brand in collection.find():
        if 'article_url' in brand.keys():
            starturls.add(brand['article_url'])
    return starturls


def get_car_type_url():
    collection = db['Brand']
    starturls = set()
    for brand in collection.find():
        if 'detailed_vehicle_url' in brand.keys():
            starturls.add(brand['detailed_vehicle_url'])
    return starturls


def get_price_car_url():
    collection = db['Brand']
    starturls = set()
    for brand in collection.find():
        if 'price_car_url' in brand.keys():
            starturls.add(brand['price_car_url'])
    return starturls


def get_video_url():
    collection = db['Brand']
    starturls = list()
    for item in collection.find():
        brand = dict()
        if 'cid' in item.keys() and 'video_url' in item.keys():
            brand['cid'] = item['cid']
            brand['video_url'] = item['video_url']
            starturls.append(brand)
    return starturls


def get_used_car_url():
    collection = db['Brand']
    starturls = set()
    for brand in collection.find():
        if 'used_car_url' in brand.keys():
            starturls.add(brand['used_car_url'])
    return starturls


def get_ask_url():
    collection = db['Brand']
    starturls = set()
    for brand in collection.find():
        if 'zhidao_url' in brand.keys():
            starturls.add(brand['zhidao_url'])
    return starturls


def get_config_url():
    collection = db['Brand']
    starturls = set()
    for brand in collection.find():
        if 'config_url' in brand.keys():
            starturls.add(brand['config_url'])
    return starturls

def get_dealerprice_url():
    collection = db['DealerList']
    starturls = set()
    for brand in collection.find():
        if 'price' in brand.keys():
            starturls.add(brand['price'])
    return starturls


def get_dealernews_url():
    collection = db['DealerList']
    starturls = set()
    for brand in collection.find():
        if 'newslist' in brand.keys():
            starturls.add(brand['newslist'])
    return starturls


def get_dealerinformation_url():
    collection = db['DealerList']
    starturls = list()
    for item in collection.find():
        info=dict()
        if 'informationList' in item.keys() and 'dealer_id' in item.keys():
            info['informationList']=item['informationList']
            info['dealer_id']=item['dealer_id']
            starturls.append(info)
    return starturls


def get_dealerinfo_url():
    collection = db['DealerList']
    starturls = set()
    for brand in collection.find():
        if 'info' in brand.keys():
            starturls.add(brand['info'])
    return starturls


def get_dealermaintain_url():
    collection = db['DealerList']
    starturls = set()
    for brand in collection.find():
        if 'maintain' in brand.keys():
            starturls.add(brand['maintain'])
    return starturls


def get_dealersalerlist_url():
    collection = db['DealerList']
    starturls = set()
    for brand in collection.find():
        if 'salerlist' in brand.keys():
            starturls.add(brand['salerlist'])
    return starturls

# ------- lby ------------
def save_koubei_list(result):
    collection = db['koubeiList']
    collection.save(result)
def get_koubei_start_url():
    collection = db['koubeiList']
    starturls = set()
    for koubei in collection.find():
        if 'koubei_url' in koubei.keys():
            starturls.add(koubei['koubei_url'])
    return starturls



def save_brandlist(result):
    collection = db['Brand']
    collection.save(result)


def save_dealerlist(result):
    collection = db['DealerList']
    collection.save(result)

def save_Vehiclelist(result):
    collection = db['Vehiclelist']
    collection.save(result)

def get_vehicleconfig_url():
    collection = db['Vehiclelist']
    starturls = set()
    for brand in collection.find():
        if 'config_url' in brand.keys():
            starturls.add(brand['config_url'])
    return starturls

def get_vehiclepic_url():
    collection = db['Vehiclelist']
    starturls = set()
    for brand in collection.find():
        if 'pic_url' in brand.keys():
            starturls.add(brand['pic_url'])
    return starturls

def get_vehiclebaojia_url():
    collection = db['Vehiclelist']
    starturls = set()
    for brand in collection.find():
        if 'baojia_url' in brand.keys():
            starturls.add(brand['baojia_url'])
    return starturls

def get_vehiclekoubei_url():
    collection = db['Vehiclelist']
    starturls = set()
    for brand in collection.find():
        if 'koubei_url' in brand.keys():
            starturls.add(brand['koubei_url'])
    return starturls

def get_vehiclecarprice_url():
    collection = db['Vehiclelist']
    starturls = set()
    for brand in collection.find():
        if 'price_car_url' in brand.keys():
            starturls.add(brand['price_car_url'])
    return starturls