#!/usr/bin/env python3
import scrapy
import json

class CourseSpider(scrapy.Spider):
    name = 'courses'


    # 模拟登录的核心: 构造一个 scrapy.Request 对象
    # 使用 POST 方式将用户的邮箱和密码数据传递给实验楼服务器
    # start_requests 的返回值须为可迭代对象，所以不能直接返回 scrapy.Request()
    # 在外层加上方括号，返回一个列表
    def start_requests(self):
        return [scrapy.Request(
            # url 就是我们要请求的登录地址
            url = 'https://www.shiyanlou.com/api/v2/auth/login',
            # 请求方式是 POST
            method = 'POST',
            # 构造一个JSON 格式的字典，字典中写入 login 和 password 两个字段的值
            body = json.dumps({
                'login': '*****@***.com',
                'password': '*******'
            }),
            # 传入的用户数据是 JSON 格式，是由 Content-Type 决定的
            # 这里需要将这个字段作为 headers 的键值对写入
            headers = {
                'Content-Type':'application/json;charset=UTF-8',
            },
            # 设置钩子函数， 即登录成功后自动运行此函数
            callback = self.after_parse 
        )]

    def after_parse(self, response):
        return scrapy.Request(
            url = 'https://www.shiyanlou.com/user/988159/',
            callback = self.parse_after_login
        )

    def parse_after_login(self, response):
        yield {
            '累计实验次数': response.xpath('//ul[@class="user-lab-info-box"]/li[2]//li[2]/text()').extract_first().split()[1],
            '有效学习时间': response.xpath('//ul[@class="user-lab-info-box"]/li[3]//li[2]/text()').extract_first().split()[1]
        }

