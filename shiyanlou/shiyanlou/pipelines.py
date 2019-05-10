# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker
from shiyanlou.models import Course, engine

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ShiyanlouPipeline(object):
    
    def open_spider(self, spider):
        Session = sessionmaker(bind=engine)
        self.session = Session()
    
    def process_item(self, item, spider):
        item['students'] = int(item['students'])
        if item['students'] < 1000:
            # 对于不需要的item,主动出发 DropItem异常
            raise DropItem('Course students less than 1000')
        else:
            # 根据item创建Course Model对象并添加到session
            # item 可以当成字典来用，所以也可以用字典解构
            self.session.add(Course(**item))
        return item
    
    def close_spider(self, spider):
        self.session.commit()
        self.session.close()