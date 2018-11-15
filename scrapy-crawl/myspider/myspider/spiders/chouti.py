# -*- coding: utf-8 -*-
import scrapy
import time
import json
from myspider.items import MyspiderItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class ChoutiSpider(scrapy.Spider):
    name = 'chouti'
    allowed_domains = ['dig.chouti.com']
    start_urls = ['https://dig.chouti.com/getTopTenLinksOrComments.json?_={}'.format(int(time.time()))]

    def start_requests(self):
        url = 'https://dig.chouti.com/getTopTenLinksOrComments.json?_={}'.format(int(time.time()))
        yield scrapy.Request(url, callback=self.parse)


    def parse(self, response):
  
        items = MyspiderItem()
        result = json.loads(response.text)
        data = result.get('result').get('data')
        for i in range(10):
            items['create_time'] = data[i].get('createTime')
            items['title'] = data[i].get('title')
            items['videoUrl'] = data[i].get('videoUrl')
            items['author'] = data[i].get('nick')
            print(items['title'])
            yield items

       
 
