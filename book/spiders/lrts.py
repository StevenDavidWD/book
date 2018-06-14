# -*- coding: utf-8 -*-
import scrapy
from book.items import AlbumItem, EpisodeItem, CommentItem
import redis

class LrtsSpider(scrapy.Spider):
    name = 'lrts'
    allowed_domains = ['lrts.me']
    start_urls = ['http://www.lrts.me/book/category/1']
    r = redis.Redis()

    def parse(self, response):
        url = response.xpath('//li[@class="book-item"]//a[@class="book-item-name"]/@href').extract()
        for u in url:
            u = 'http://www.lrts.me' + u
            req = scrapy.Request(u, callback=self.parse_album)
            req.meta['phantomjs'] = True
            yield req

        url = response.xpath('//div[@class="pagination"]/a/@href').extract()
        for u in url:
            u = 'http://www.lrts.me' + u
            yield scrapy.Request(u, callback=self.parse)

    def parse_album(self, response):
        album = AlbumItem()
        album['url'] = response.url
        album['aid'] = response.url.split('/')[-1]
        album['title'] = response.xpath('//div[@class="d-r"]/h1/text()').extract()[0]
        album['broadcaster'] = response.xpath('//ul[@class="d-grid nowrap"]//a[@class="g-user"]/text()').extract()[0]
        album['author'] = response.xpath('//ul[@class="d-grid nowrap"]//a[@class="author"]/text()').extract()[0]
        album['category'] = response.xpath('//ul[@class="d-grid"]')[0].xpath('./li/text()').extract()[0]
        album['introduction'] = response.xpath('//div[@class="d-desc f14"]/p/text()').extract()[0]
        album['cover_url'] = response.xpath('//div[@class="d-cover d-book-cover"]/img/@src').extract()[0]
        album['source'] = self.name
        album['language'] = 'Chinese'
        album['episode'] = list()
        album['comment'] = list()

        epi = response.xpath('//ul[@id="pul"]/li') 
        for e in epi:
            episode = EpisodeItem()
            episode['title'] = e.xpath('./a/text()').extract()[0]
            episode['eid'] = e.xpath('./a/@player-info').extract()[0].split('=')[-1]
            album['episode'].append(episode)


        com = response.xpath('//div[@class="d-comments-list"]/ul/li/div[@class="photo-s50-r"]')
        for c in com:
            comment = CommentItem()
            comment['reviewer'] = c.xpath('./a/text()').extract()[0]
            comment['text'] = c.xpath('./p/text()').extract()[0].strip('\n\t')
            album['comment'].append(comment)

        yield album

