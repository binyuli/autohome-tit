# -*- coding: utf-8 -*-

# Scrapy settings for autohome_tit project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'autohome_tit'

SPIDER_MODULES = ['autohome_tit.spiders']
NEWSPIDER_MODULE = 'autohome_tit.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'autohome_tit (+http://www.yourdomain.com)'

# Obey robots.txt rules(autohome doesn't have a robots file)
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'autohome_tit.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'autohome_tit.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'autohome_tit.pipelines.SomePipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# Don't cleanup redis queues, allows to pause/resume crawls.
SCHEDULER_PERSIST = True
# REDIS_START_URLS_BATCH_SIZE = 1000000

# LOG_STDOUT=True
# LOG_FILE = 'log.txt'


MONGODB_SERVER = "192.168.17.61"
MONGODB_PORT = 27017
MONGODB_DB = "Autohome_tit"

ITEM_PIPELINES = {
    # 'autohome_tit.pipelines.ArticlePipeline': 300,
    # 'autohome_tit.pipelines.BrandInfoPipeline': 301,
    # 'autohome_tit.pipelines.DetaileVehiclePipeline': 302,
    # 'autohome_tit.pipelines.ForumPipeline': 303,
    'autohome_tit.pipelines.KoubeiPipeline': 304,
    # 'autohome_tit.pipelines.PicturePipeline': 305,
    # 'autohome_tit.pipelines.ShuokePipeline': 306,
    # 'autohome_tit.pipelines.BaikePipeline': 307,
    # 'autohome_tit.pipelines.UsedcarPipeline': 308,
    # 'autohome_tit.pipelines.VideoPipeline': 309,
    # 'autohome_tit.pipelines.YouchuangPipeline': 310,
    # 'autohome_tit.pipelines.ZhidaoPipeline': 311,
    # 'autohome_tit.pipelines.IndexPipeline': 312,
    # 'autohome_tit.pipelines.DealerPipeline': 313,
    # 'autohome_tit.pipelines.OwnerpricePipeline': 314,
    # 'autohome_tit.pipelines.BaojiaPipeline': 315,
    # 'autohome_tit.pipelines.CarstorePipeline': 316,
    # 'autohome_tit.pipelines.DealerpricePipeline': 317,
    # 'autohome_tit.pipelines.DealernewsPipeline': 318,
    # 'autohome_tit.pipelines.DealerinformationPipeline': 319,
    # 'autohome_tit.pipelines.DealerinfoPipeline': 320,
    # 'autohome_tit.pipelines.DealermaintainPipeline': 321,
    # 'autohome_tit.pipelines.DealersalerlistPipeline': 322,
    # 'autohome_tit.pipelines.ConfigPipeline': 323,
    # 'autohome_tit.pipelines.ForumsPipeline': 324,
    # 'autohome_tit.pipelines.VehicleconfigPipeline': 325,
    # 'autohome_tit.pipelines.VehiclePicPipeline': 326,
    # 'autohome_tit.pipelines.VehicleCarpricePipeline': 327,
    # 'autohome_tit.pipelines.VehicleBaojiaPipeline': 328,
    # 'autohome_tit.pipelines.VehicleKoubeiPipeline': 329,
}


REDIS_HOST = '192.168.17.51'
REDIS_PORT = 6379

FILTER_MOD = 'Update'
START_DATE = '2014-1-1'