# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class XieZhengPipeline(object):
    def __init__(self):
        self.file = open('xiezheng.json', 'wb')

    def process_item(self, item, spider):
        print(item['nickname'])
        content = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.write(content)
        return item

    def close_spider(self, spider):
        self.file.close()
