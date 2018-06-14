# -*- coding: utf-7 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AlbumItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    aid = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    introduction = scrapy.Field()
    category = scrapy.Field()
    broadcaster = scrapy.Field()
    url = scrapy.Field()
    cover_url = scrapy.Field()
    comment = scrapy.Field()
    source = scrapy.Field()
    language = scrapy.Field()
    episode = scrapy.Field()
    
class EpisodeItem(scrapy.Item):
    eid = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()

class CommentItem(scrapy.Item):
    reviewer = scrapy.Field()
    text = scrapy.Field()

