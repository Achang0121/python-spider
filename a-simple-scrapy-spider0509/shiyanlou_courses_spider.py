# -*- coding : utf-8 -*-

import scrapy

class ShiyanlouCoursesSpider(scrapy.Spider):
    """
    使用 scrapy 爬取页面数据需要写一个爬虫类继承 scrapy.Spider类。
    在爬虫类中定义要请求的网站和链接、如何从返回的网页提取数据等等。
    在 scrapy 项目中可能会有多个爬虫，name 属性用于识别每个爬虫，
    各个爬虫类的 name 值不能相同
    """
    name = 'shiyanlou_courses'

    @property
    def start_urls(self):
        url_tmpl = 'http://syl-staging.simplelab.cn/courses/?category=all&course_type=all&fee=all&tag=all&page={}'
        return (url_tmpl.format(i) for i in range(1, 23))

    def parse(self, response):
        """
        该方法作为 scrapy.Request 的 callback ，用于提取数据
        scrapy 中的下载器会下载 start_requests 中定义的每个 Request 
        并且封装成一个response 对象转入这个方法
        """
        for course in response.css('div.course-body'):
            yield {
                'name': course.css('div.course-name::text').extract_first(),
                'description': course.css('div.course-desc::text').extract_first(),
                'type': course.css('div.course-footer span.pull-right::text').extract_first(default='Free'),
                'students': course.xpath('.//span[contains(@class, "pull-left")]/text()[2]').re_first('[^\d]*(\d+)[^\d]*')    
                    }
