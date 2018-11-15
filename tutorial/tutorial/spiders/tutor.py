# -*- coding: utf-8 -*-
import scrapy
from Tutorial.items import TutorialItem

class TutorSpider(scrapy.Spider):
    name = 'tutor'
    #allowed_domains = ['http://www.taobao.com/']
    start_urls = ['http://www.taobao.com//']



    #默认处理response 函数
    def parse(self, response):
	items = TutorialItem()	
	items['name'] = 'xxxx'
	items['image_url'] = 'http://xxxx'
	items['author']	= 'xxx'

	yield items

        filename = response.url.split('.')[-2]
	print('filename', filename)
	with open('{}.html'.format(filename), 'wb') as f:
		f.write(response.body)
	print('完成')
	`
from scrapy import Spider
from scrapy import Request


class TestSpider(Spider):
	name = 'test'
	start_urls = [
		'http://www.baidu.com/'
	]
	
	def login_parse(self, reponse):
		print(response)
		for i in range(10):
			yield Request('https://tieba.baidu.com/f?kw=%E4%B8%96%E7%95%8C%E6%9D%AF&ie=utf-8&pn={}'.format(i*50))
##
#	def start_requests(self):
#		print('1111')
###		return Request('http://www.example.com/login', method='POST', body='username=heitu&password=1234', callback=self.login_parse)
#import requests

#start_url = 'http://www.jianshu.com/'
#res = requests.get(start_url)
#print(res.text)
