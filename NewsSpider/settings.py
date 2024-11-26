#!usr/bin/env python
# -*- coding:utf-8 -*-


import datetime


BOT_NAME = 'NewsSpider'

SPIDER_MODULES = ['NewsSpider.spiders']
NEWSPIDER_MODULE = 'NewsSpider.spiders'

ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 16
LOG_LEVEL = 'DEBUG'

# DOWNLOAD_DELAY = 1

DOWNLOADER_MIDDLEWARES = {
    'NewsSpider.middlewares.MyUserAgentMiddleware': 101,
}


EXPORTER_FILE = "news.csv"


today = datetime.datetime.now()
log_file = 'NewsSpider/log/scrapy_{}_{}_{}.log'.format(today.year, today.month, today.day)
LOG_LEVEL = 'DEBUG'
LOG_FILE = log_file

# Enable the Elasticsearch pipeline
ITEM_PIPELINES = {
    'NewsSpider.pipelines.NewsElasticPipeline': 300,
}

# Elasticsearch settings
ELASTICSEARCH_HOST = "http://localhost:9200"
ELASTICSEARCH_INDEX = 'news_index'  # Change the index name if needed