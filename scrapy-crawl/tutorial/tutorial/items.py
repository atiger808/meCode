# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    image_url = scrapy.Field()
    author = scrapy.Field()



# 爬取的目标是从非结构化得数据里面提取结构化数据
# item 是一种简单的容器， 类似字典
