# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.conf import settings
import pymongo


class ZhihuspiderPipeline(object):

    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_NAME']
        docname = settings['MONGODB_DOCNAME']
        connection = pymongo.MongoClient(port=port, host=host)
        self.post = connection[dbname][docname]

    def process_item(self, item, spider):
        post_item = dict(item)
        self.post.insert(post_item)
