# -*- coding: utf-8 -*-
import scrapy
import json
import redis

class CommentSpider(scrapy.Spider):
    name = 'comment'
    allowed_domains = ['jd.com']
    start_urls = json.load(open('/home/stevenwd/book/comments.json', 'r'))
    r = redis.Redis()

    def parse(self, response):
        book = 'http:' + response.xpath('//li[@class="gl-item"]')[0].xpath('.//a/@href')[0].extract()
        book_num = book.split('jd.com/')[1].split('.html')[0]
        # comment_url = "http://sclub.jd.com/productpage/p-" + book_num + "-s-0-t-3-p-0.html?callback=fetchJSON_comment98vv0"

        # yield scrapy.Request(comment_url, callback=parse_comment)

        self.r.sadd('book', book_num)
