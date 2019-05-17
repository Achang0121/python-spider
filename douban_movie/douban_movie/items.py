# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    # 页面连接
    url = scrapy.Field()
    # 电影名称
    name = scrapy.Field()
    # 简介
    summary = scrapy.Field()
    # 评分
    score = scrapy.Field()
