# -*- coding: utf-8 -*-
import scrapy
from sunbeam.items import SunbeamItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



class SunwzSpider(scrapy.Spider):
    name = 'sunwz'  # 爬虫名字是唯一的
    allowed_domains = ['wz.sun0769.com']

    url = 'http://wz.sun0769.com/index.php/question/questionType?type=4&page={}' 
    offset = 0
    start_urls = [url.format(offset)]
    #start_urls = ['http://http://wz.sun0769.com/index.php/question/questionType?type=4&page={}'.format(i) for i in range(0,94110, 30 )]
#
#    def start_request(self):
#        for i in range(0, 90, 30):
#            yield scrapy.Request(self.url.format(i))

    def parse(self, response):
        #取页面帖子的链接
        links = response.xpath('//div[@class="greyframe"]/table//td/a[@class="news14"]/@href').extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_item)
        # 设置翻页
        if self.offset <= 94410:
            self.offset += 30
            yield scrapy.Request(self.url.format(self.offset), callback=self.parse)


    def parse_item(self, response):
        items = SunbeamItem()
        # 内容
        items['content'] = response.xpath('//div[@class="c1 text14_2"]/text()')[0].extract()
        # 标题
        items['title'] = response.xpath('//div[contains(@class, "pagecenter p3")]//strong/text()').extract()[0].split(':')[0].replace('编号', '')
        print(items['title'])
        # 编号
        items['number'] = response.xpath('//div[contains(@class, "pagecenter p3")]//strong/text()').extract()[0].split(':')[-1].strip()
        print(items['number'])
        
        print(items['title'][0])
        # url
        items['url'] = response.url
        yield items


