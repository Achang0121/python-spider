# -*- coding: utf-8 -*-
import scrapy
from GitHubSpider.items import GithubSpiderItem

class GithubSpider(scrapy.Spider):
    name = 'github'
    allowed_domains = ['github.com']
    start_urls = ['http://github.com/shiyanlou?tab=repositories']

    
    def parse(self, response):
        item = GithubSpiderItem()
        
        lis = response.xpath('//div[@id="user-repositories-list"]//li[contains(@class, "public")]')
        for li in lis:
            item['update_time'] = li.xpath('.//relative-time/@datetime').extract_first()
            item['name'] = li.xpath('.//h3/a/text()').extract_first().strip()
            yield item
        btn_group = response.xpath('//a[contains(@class, "BtnGroup")]')
        if len(btn_group) == 1:
            next_page_url = response.xpath('//a[contains(@class, "BtnGroup")]/@href').extract_first()
        else:
            next_page_url = response.xpath('//a[contains(@class, "BtnGroup")][2]/@href').extract_first()
        yield scrapy.Request(url=next_page_url, callback=self.parse)
