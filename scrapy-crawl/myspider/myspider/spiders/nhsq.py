# -*- coding: utf-8 -*-
import scrapy
import time

class NhsqSpider(scrapy.Spider):
    name = 'nhsq'
    allowed_domains = ['neihanshequ.com']
    start_urls = ['http://neihanshequ.com/']

    def satrt_requests(self):
        url = 'http://neihanshequ.com/joke/?is_json=1&app_name=neihanshequ_web&max_time={}'.format(int(time.time()))
	yield scrapy.Request(url, callback=self.parse())
    def parse(self, response):
        pass
