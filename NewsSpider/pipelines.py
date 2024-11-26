#!usr/bin/env python
# -*- coding:utf-8 -*-

from elasticsearch import Elasticsearch
from NewsSpider.items import NewsItem
from NewsSpider.utils.bloom import BloomFilter
import logging

class NewsElasticPipeline(object):

    @classmethod
    def from_settings(cls, settings):
        return cls(settings)

    def __init__(self, settings):
        # 初始化 Elasticsearch 客户端，增加 scheme 参数
        self.es = Elasticsearch(settings["ELASTICSEARCH_HOST"])
        self.index_name = settings['ELASTICSEARCH_INDEX']
        
        # 初始化 BloomFilter 来避免重复存储
        self.filter = BloomFilter()

        # 记录插入的条目数
        self.count = 0

    def process_item(self, item, spider):
        if isinstance(item, NewsItem):
            if not self.filter.contains(item['news_link']):
                self.index_item(item)
                self.filter.insert(item['news_link'])
                self.count += 1
                print('已经插入 Elasticsearch {}，当前新闻链接为 {}'.format(self.count, item['news_link']))
            else:
                print('{} 已经存在于 Elasticsearch'.format(item['news_link']))
        return item

    def index_item(self, item):
        doc = {
            'news_brief': item.get('news_brief', ''),
            'news_comments': item.get('news_comments', ''),
            'news_content': item.get('news_content', ''),
            'news_cover': item.get('news_cover', ''),
            'news_img': item.get('news_img', ''),
            'news_keywords': item.get('news_keywords', ''),
            'news_link': item.get('news_link', ''),
            'news_media': item.get('news_media', ''),
            'news_site': item.get('news_site', ''),
            'news_time': item.get('news_time', ''),
            'news_title': item.get('news_title', ''),
            'news_type': item.get('news_type', ''),
        }
        try:
            self.es.index(index=self.index_name, body=doc)
        except Exception as e:
            logging.error(f"Failed to insert item into Elasticsearch: {e}")

    def close_spider(self, spider):
        print('总共插入 Elasticsearch 的条目数: {0}'.format(self.count))