#!usr/bin/env python
# -*- coding:utf-8 -*-

from scrapy import Item, Field


class NewsItem(Item):
    """ 新闻信息 """
    # news_id = Field()      # 新闻ID
    news_brief = Field()     # 新闻简介
    news_comments = Field()  # 评论数量
    news_content = Field()   # 新闻内容
    news_cover = Field()     # 新闻封面
    news_img = Field()       # 新闻图片
    news_keywords = Field()  # 新闻关键词
    news_link = Field()      # 新闻链接
    news_media = Field()     # 新闻媒体
    news_site = Field()      # 新闻来源
    news_time = Field()      # 发布时间
    news_title = Field()     # 新闻标题
    news_type = Field()      # 新闻类型