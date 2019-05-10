# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker
from shiyanlou.models import Course, engine, User
from datetime import datetime
from shiyanlou.items import CourseItem, UserItem

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ShiyanlouPipeline(object):
    
    def open_spider(self, spider):
        Session = sessionmaker(bind=engine)
        self.session = Session()
    
    def process_item(self, item, spider):
        """
        对于不同的item使用不同的处理函数
        """
        if isinstance(item, CourseItem):
            self._process_course_item(item)
        elif isinstance(item, UserItem):
            self._process_user_item(item)
            
    def _process_course_item(self, item):        
        item['students'] = int(item['students'])
        if item['students'] < 1000:
            # 对于不需要的item,主动出发 DropItem异常
            raise DropItem('Course students less than 1000')
        else:
            # 根据item创建Course Model对象并添加到session
            # item 可以当成字典来用，所以也可以用字典解构
            self.session.add(Course(**item))
        return item
    
    def _process_user_item(self, item):
        # 抓到的数据类似 'L123456' 需要去掉L并转化为int
        item['level'] = int(item['level'][1:])
        # 抓取到的数据类似 '2019-01-01 加入实验楼'， 把其中的日期字符转换成date对象
        item['join_date'] = datetime.strptime(item['join_date'].split()[0], '%Y-%m-%d')
        item['learn_courses_num'] = int(item['learn_courses_num'])
        self.session.add(User(**item))
        
        
    
    def close_spider(self, spider):
        self.session.commit()
        self.session.close()