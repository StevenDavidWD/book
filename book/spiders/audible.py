# -*- coding: utf-8 -*-
import scrapy
from book.items import AlbumItem, EpisodeItem, CommentItem
import redis
import time
import json

class AudibleSpider(scrapy.Spider):
    name = 'audible'
    allowed_domains = ['audible.co.uk']
    start_urls = json.load(open('./start_urls.json', 'r'))
    r = redis.Redis()

    def parse(self, response):
        url = response.xpath('//div[@class="responsive-product-square"]/div/a/@href').extract()
        for u in url:
            if 'pd' in u:
                u  = 'https://www.audible.co.uk' + u
                request = scrapy.Request(u, callback=self.parse_album)
                yield request

        # for i in range(2, 1630):
        #     url = self.start_urls[0] + '&page=' + str(i)
        #     request = scrapy.Request(url, callback=self.parse)
        #     yield request
        #  #    time.sleep(1)


    def parse_album(self, response):
        album = AlbumItem()
        album['url'] = response.url
        album['aid'] = response.url.split('?')[0].split('/')[-1]
        album['title'] = response.xpath('//h1/text()').extract()[0]
        album['author'] = response.xpath('//div[@class="bc-row-responsive"]//span/ul/li/a/text()').extract()[0]
        album['broadcaster'] = response.xpath('//div[@class="bc-row-responsive"]//span/ul/li/a/text()').extract()[1]
        album['category'] = response.xpath('//div[@class="bc-container"]/nav/a/text()').extract()
        album['introduction'] = ''.join(response.xpath('//div[@class="bc-container productPublisherSummary"]//p/text()').extract())
        album['cover_url'] = response.xpath('//div[@class="bc-row-responsive"]//img/@src').extract()[0]
        album['source'] = self.name
        album['language'] = 'English'
        album['episode'] = list()
        album['comment'] = list()

        com = response.xpath('//div[contains(@class, "bc-spacing-top-medium")]')
        for c in com:
            try:
                comment = CommentItem()
                comment['reviewer'] = c.xpath('./div/div//ul/li/a/text()').extract()[0].strip('\n\t ')
                comment['text'] = c.xpath('./div/p/text()').extract()[0].strip(' \n\t')
                album['comment'].append(comment)
            except:
                pass

        yield album
