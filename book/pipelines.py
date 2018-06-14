# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# from pymongo import MongoClient
from book.items import AlbumItem, EpisodeItem
import redis

class BookPipeline(object):

    # conn = MongoClient(host='localhost', port=27017)
    # db = conn['ximalaya']
    # album = db['album']
    # episode = db['episode']
    r = redis.Redis(host='localhost',
            port=6379,
            db=0,
            charset='utf-8',
            decode_responses=True)

    def process_item(self, item, spider):
        u_item = str(item).encode('utf-8')

        if isinstance(item, AlbumItem):
            self.r.sadd('album', u_item)

        return item
