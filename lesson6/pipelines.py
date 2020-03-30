# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient


class DataBasePipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.leroy_3003

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(self.item_res(item))
        return item

    def item_res(self, item):
        if item:
            i = 0
            item['props'] = list()
            for h in item._values['pr_h']:
                item['props'].append(f"{h}:{item._values['pr_p'][i]}")
                i += 1
            item._values['pr_h'] = ''
            item._values['pr_p'] = ''
            if len(item._values['price']):
                item._values['price'] = item._values['price'][0]
        return item


class LeroyPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item
