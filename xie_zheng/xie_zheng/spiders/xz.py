# -*- coding: utf-8 -*-
import scrapy
from xie_zheng.items import XieZhengItem
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



class XzSpider(scrapy.Spider):
    name = 'xz'
    allowed_domains = ['m.maoyan.com/']
    url = ['http://m.maoyan.com/mmdb/comments/movie/248566.json?_v_=yes&offset={}'.format(i) for i in range(1, 3)]

    def parse(self, response):
        links = ['http://m.maoyan.com/mmdb/comments/movie/248566.json?_v_=yes&offset={}'.format(i) for i in range(1,10)]
        for link in links:
            print('网址==========', links)
            yield scrapy.Request(link, callback=self.parse_item)

    def parse_item(self, response):
        items = XieZhengItem()
        data = json.loads(response.text)['cmts']
        for i in data:
            items['date'] = i['time'].split('  ')[0]
            items['nickname'] = i['nickName']
            items['city'] = i['cityName']
            items['rate'] = i['score']
            items['comment'] = i['content']
            yield items 
