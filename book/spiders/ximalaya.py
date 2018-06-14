# -*- coding: utf-8 -*-
import scrapy
from book.items import AlbumItem, EpisodeItem
import redis

class XimalayaSpider(scrapy.Spider):
    name = 'ximalaya'
    allowed_domains = ['ximalaya.com']
    start_urls = ['http://ximalaya.com/youshengshu/']
    r = redis.Redis()

    def parse(self, response):
        url = response.xpath('//div[@class="content"]/ul/li//a/@href').extract()
        for u in url:
            u = 'http://www.ximalaya.com' + u
            if 'youshengshu' in u:
                yield scrapy.Request(u, callback=self.parse_album)

        url = response.xpath('//div[@class="pagination-wrap"]//a/@href').extract()
        for u in url:
            u = 'http://www.ximalaya.com' + u
            if 'youshengshu/p' in u:
                yield scrapy.Request(u, callback=self.parse)

    def parse_album(self, response):
        album = AlbumItem()
        album['url'] = response.url
        album['aid'] = response.url.split('/')[-2]
        album['title'] = response.xpath('//h1/text()').extract()[0]
        album['broadcaster'] = response.xpath('//div[@class="xui-card-body"]/div/div/p/a/text()').extract()[0]
        album['category'] = response.xpath('//span[@class="xui-tag-text"]/a/text()').extract()
        album['introduction'] = ''.join(response.xpath('//p[@data-flag="normal"]//text()').extract()).strip('\xa0')
        album['cover_url'] = response.xpath('//div[@class="detail layout-main"]//img/@src').extract()[0]
        album['source'] = self.name
        album['language'] = 'Chinese'
        album['author'] = str()

        album['episode'] = list()
        album['comment'] = list()

        epi = response.xpath('//div[contains(@class, "sound-list")]/ul/li/div[contains(@class, "text")]/a')
        for e in epi:
            episode = EpisodeItem()
            episode['title'] = e.xpath('./@title').extract()[0]
            episode['eid'] = e.xpath('./@href').extract()[0].split('/')[-1]
            album['episode'].append(episode)
        yield album


