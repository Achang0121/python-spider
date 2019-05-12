# -*- coding: utf-8 -*-
import scrapy
from shiyanlou.items import MultipageCourseItem


class MulitpageSpider(scrapy.Spider):
    name = 'multipage'
    start_urls = ['https://www.shiyanlou.com/courses/']

    def parse(self, response):
        for course in response.css('div.col-md-3'):
            item = MultipageCourseItem(
                # 课程名称
                name=course.css('h6.course-name::text').extract_first().strip(),
                # 课程图片
                image=course.css('img.cover-image::attr(src)').extract_first()          
            )
            # 构造课程详情页面的链接，爬到的链接是相对链接，调用urljon构造
            course_url = course.css('a::attr(href)').extract_first()
            full_course_url = response.urljoin(course_url)
            # 构造课程详情页的请求，指定回调函数
            request = scrapy.Request(full_course_url, self.parse_author)
            request.meta['item'] = item
            yield request
            
    def parse_author(self, response):
        # 获取未完成的item
        item = response.meta['item']
        item['author'] = response.css('span.bold::text').extract_first()
        yield item