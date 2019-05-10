# -*- coding: utf-8 -*-
import scrapy
from shiyanlou.items import UserItem


class UsersSpider(scrapy.Spider):
    name = 'users'
    allowed_domains = ['shiyanlou.com']
    
    @property
    def start_urls(self):
        """
        实验楼注册的用户数目前大约六十几万，为了爬虫的效率，
        取id 在 524800～525000 之间的新用户
        每隔10 取一个 ，最后大概爬取 20个用户的数据
        """
        url_tmpl = 'https://www.shiyanlou.com/users/{}/'
        return (url_tmpl.format(i) for i in range(525000, 524800, -10))

    def parse(self, response):
        item = UserItem(
            name = response.xpath('//div[@class="user-meta"]/span/text()').extract()[0].strip(),
            level = response.xpath('//div[@class="user-meta"]/span/text()').extract()[1].strip(),
            status = response.xpath('//div[@class="user-status"]/span/text()').extract_first(default='null').strip(),
            school_job = response.xpath('//div[@class="user-status"]/span[2]/text()').extract_first(default='null').strip(),
            join_date = response.css('span.user-join-date::text').extract_first().strip(),
            learn_courses_num = response.xpath('//span[@class="tab-item"]/text()').re_first('\D+(\d+)\D+')
            )
        if len(response.css('div.user-avatar img').extract()) == 2:
            item['is_vip'] = True
        yield item
