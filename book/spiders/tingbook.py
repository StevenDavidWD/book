# -*- coding: utf-8 -*-
import scrapy
from book.items import AlbumItem, EpisodeItem, CommentItem
import redis
import time

class TingbookSpider(scrapy.Spider):
    name = 'tingbook'
    allowed_domains = ['tingbook.com']
    start_urls = ['http://www.tingbook.com/book/list_1.html']
    r = redis.Redis()

    def parse(self, response):
        url = response.xpath('//ul[@class="library_list clearfix"]/li/span[@class="works_info"]/h4/a/@href').extract()
        for u in url:
            u = 'http://www.tingbook.com' + u.strip('..')
            req = scrapy.Request(u, callback=self.parse_album)
            req.meta['phantomjs'] = True
            yield req
            time.sleep(1)

        for i in range(2, 32):
            u = 'http://www.tingbook.com/book/list_1_' + str(i) + '.html'
            yield scrapy.Request(u, callback=self.parse)

    def parse_album(self, response):
        album = AlbumItem()
        album['source'] = self.name
        album['language'] = 'Chinese'
        album['url'] = response.url
        album['aid'] = response.url.split('/')[-1].strip('.html')
        album['title'] = response.xpath('//h2/text()').extract()[0].strip('.')
        album['broadcaster'] = response.xpath('//div[@class="detail-info-header-box-rt detail-info-list"]/ul/li')[0].xpath('./a/text()').extract()[0]
        album['author'] = response.xpath('//div[@class="detail-info-header-box-rt detail-info-list"]/ul/li')[1].xpath('./a/text()').extract()[0]
        album['category'] = list() 
        album['introduction'] = response.xpath('//div[@class="real-text"]/text()').extract() 
        album['cover_url'] = response.xpath('//span[@class="cover_mask"]/a/img/@src').extract()[0]
        album['episode'] = list()
        album['comment'] = list()

        epi = response.xpath('//div[@class="playerlist"]/ul/li/span[@class="col_1"]/a')
        for e in epi:
            episode = EpisodeItem()
            episode['title'] = e.xpath('./text()').extract()[0]
            episode['eid'] = e.xpath('./@tip').extract()[0]
            album['episode'].append(episode)

        com = response.xpath('//ul[@class="comment-list"]/li/span[@class="comment_detail"]')
        for c in com:
            comment = CommentItem()
            comment['reviewer'] = c.xpath('./p[@class="comment_publish"]/text()').extract()[0]
            comment['text'] = c.xpath('./p[@class="comment_words"]/text()').extract()[0]
            album['comment'].append(comment)


        yield album
