# -*- coding: utf-8 -*-

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from douban_movie.items import MovieItem


class AwesomeMovieSpider(CrawlSpider):
    name = 'awesome-movie'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/subject/3011091/']

    rules = (
            Rule(LinkExtractor(allow=r'.*movie.douban.com/subject/.*'), 
            callback='parse_page', 
            follow=True),
    )

    def parse_item(self, response):
        item = MovieItem()
        item['url'] = response.url
        item['name'] = response.xpath(
                '//div[@id="content"]//h1/span[1]/text()').extract_first().strip()
        item['summary'] = response.xpath(
                '//span[@property="v:summary"]/text()').extract_first().strip()
        item['score'] = response.xpath(
                '//strong[contains(@class, "rating_num")]/text()').extract_first()
        return item
    
    def parse_start_url(self, response):
        yield self.parse_item(response)


    def parse_page(self, response):
        yield self.parse_item(response)

