# -*- coding: utf-8 -*-
import scrapy
from GitHubSpider.items import GithubSpiderItem

class GithubSpider(scrapy.Spider):
    name = 'github'
    allowed_domains = ['github.com']
    
    @property
    def start_urls(self):  
        return ('https://github.com/shiyanlou?tab=repositories',)

    
    def parse(self, response):
        
        lis = response.xpath('//div[@id="user-repositories-list"]//li[contains(@class, "public")]')
        for li in lis:
            item = GithubSpiderItem()
            item['update_time'] = li.xpath('.//relative-time/@datetime').extract_first()
            item['name'] = li.xpath('.//h3/a/text()').extract_first().strip()
            detail_url = li.xpath('.//a[contains(@itemprop, "codeRepository")]/@href').extract_first()
            full_url = response.urljoin(detail_url)
            request = scrapy.Request(url=full_url, callback=self.parse_details)
            request.meta['item'] = item
            yield request

        btn_group = response.xpath('//a[contains(@class, "BtnGroup")]')
        if len(btn_group) == 1:
            next_page_url = response.xpath('//a[contains(@class, "BtnGroup")]/@href').extract_first()
        else:
            next_page_url = response.xpath('//a[contains(@class, "BtnGroup")][2]/@href').extract_first()
        yield response.follow(url=next_page_url, callback=self.parse)
        
    def parse_details(self, response):
        item = response.meta['item']
        item['commits'] = response.xpath('//li[contains(@class, "commits")]//span/text()').extract_first().strip()
        item['branches'] = response.xpath('//ul[@class="numbers-summary"]/li[2]//span/text()').extract_first().strip()
        item['releases'] = response.xpath('//ul[@class="numbers-summary"]/li[3]//span/text()').extract_first().strip()
        yield item
        
