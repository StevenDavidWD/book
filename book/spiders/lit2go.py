# -*- coding: utf-8 -*-
import scrapy
from book.items import AlbumItem, EpisodeItem, CommentItem
import redis

class Lit2goSpider(scrapy.Spider):
    name = 'lit2go'
    allowed_domains = ['etc.usf.edu']
    start_urls = ['http://etc.usf.edu/lit2go/books/index/a']
    r = redis.Redis()

    def parse(self, response):
        url = response.xpath('//figcaption[@class="title"]/a/@href').extract()
        for u in url:
            yield scrapy.Request(u, callback=self.parse_album)

        url = response.xpath('//section[@class="pagination"]/ul/li/a/@href').extract()
        for u in url:
            yield scrapy.Request(u, callback=self.parse)

    def parse_album(self, response):
        album = AlbumItem()
        album['url'] = response.url
        album['aid'] = response.url.split('/')[-3]
        album['title'] = response.xpath('//h2/text()').extract()[0].strip('\n').strip(' ')
        album['author'] = response.xpath('//h3/a/text()').extract()[0]
        album['category'] = response.xpath('//div[@id="column_secondary"]/ul/div')[2].xpath('.//a/text()').extract()
        album['introduction'] = ''.join(t.strip(' \t\n') for t in response.xpath('//div[@id="column_primary"]/p//text()').extract())
        album['cover_url'] = response.xpath('//div[@id="page_thumbnail"]/img/@src').extract()[0]
        album['broadcaster'] = str()
        album['source'] = self.name
        album['language'] = 'English'
        album['episode'] = list()
        album['comment'] = list()

        epi = response.xpath('//dl/dt/a')
        for e in epi:
            episode = EpisodeItem()
            episode['title'] = e.xpath('./text()').extract()[0]
            episode['eid'] = e.xpath('./@href').extract()[0].split('/')[-2]
            album['episode'].append(episode)

        yield album
