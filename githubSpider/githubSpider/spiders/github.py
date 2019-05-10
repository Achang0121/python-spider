# -*- coding: utf-8 -*-
import scrapy
import json
from githubSpider.items import GithubspiderItem

class GithubSpider(scrapy.Spider):
    name = 'github'
    allowed_domains = ['github.com']
    start_urls = ['http://github.com/shiyanlou?tab=repositories']

    def parse(self, response):
        github_item = GithubspiderItem()
        # 解析仓库列表 得到 name 和 update_time，并获取下一页的链接
        lis = response.xpath('//div[@id="user-repositories-list"]//li[contains(@class, public)]')
        for li in lis: 
            github_item['update_time'] = li.xpath('.//relative-time/@datetime').extract_first()
            github_item['name'] = li.xpath('.//h3/a/text()').extract_first().strip()
            yield github_item          
        btn_group = response.xpath('//a[contains(@class,"BtnGroup")]')
        if len(btn_group) == 1:
            next_page_url = response.xpath('//a[contains(@class,"BtnGroup")]/@href').extract_first()
        else:
            next_page_url = response.xpath('//a[contains(@class,"BtnGroup")][2]/@href').extract_first()
        yield scrapy.Request(url=next_page_url, callback=self.parse)
