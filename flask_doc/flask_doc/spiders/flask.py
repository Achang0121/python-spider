# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from flask_doc.items import PageItem


class FlaskSpider(CrawlSpider):
    """
    目标：1、爬取Flask文档的所有页面文本，
          2、文本不能包含html标签，不能连续出现两个以上的空白字符
          3、结果存入redis
    """

    name = 'flask'
    allowed_domains = ['flask.pocoo.org']
    start_urls = ['http://flask.pocoo.org/docs/1.0/']

    rules = (
        Rule(LinkExtractor(allow=r'.*docs/1.0/.*'), 
            callback='parse_item', 
            follow=True),
    )

    # 解析函数
    def parse_item(self, response):
        item = PageItem()
        """
        url: 当前页面的url
        text: 当前页面的文本
        """
        item['url'] = response.url
        item['text'] = ' '.join(response.xpath('//text()').extract_first())
        yield item
