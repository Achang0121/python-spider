# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
import redis
import json


class FlaskDocPipeline(object):
    def process_item(self, item, spider):
        """
        将 item 结果以 JSON 形式保存到 Redis 数据库的 list 结构中
        """
        item['text'] = re.sub('\s+', ' ', item['text']) # 多个空白字符，替换为一个空格
        # 将序列化后的item存入redis的 key 为 flask_doc:items 的list中
        self.redis.lpush('flask_doc:items', json.dumps(dict(item)))
        return item

    def open_spider(self, spider):
        # 连接数据库
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)
