# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs

class SunbeamPipeline(object):
    def __init__(self):
       # self.file = codecs.open('sunwz', 'wb', encoding='utf-8')
        self.file = open('sunwz02.json', 'wb')
    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(content)
        return item
    def close_spider(self, spider):
        self.file.close()
