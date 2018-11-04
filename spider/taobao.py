# --*-- coding: utf-8 --*--
# @Time     : 2018/7/15 0:26
# @Author   : Ole211
# @Site     :
# @File     : taobao.py
# @Software : PyCharm
import requests
import sys
# 解析url 用的类库
#Python2
# import urllib
# from urlparse import urlparse
# python3
# from urllib.parse import urlparse
# import urllib.request
import re
import json
import pandas as pd
import csv
from bs4 import BeautifulSoup as bs
import threading
import multiprocessing
from run_time import run_time as run


url = 'http://tieba.baidu.com/f?kw='
headers = {
'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
'upgrade-insecure-requests':'1',
}

class TaobaoScrawl(object):
    """初始化"""
    def __init__(self):
        self.headers = headers
        self.path = './'
        self.pageurl = 'https://s.taobao.com/search?q='
        self.idurl = 'https://item.taobao.com/item.htm?id='
        self.urls = []
        self.nums = 0
    def parse_page(self,url):
        """网页解析"""
        res = requests.get(url, headers = self.headers)
        res.encoding = 'utf-8'
        if res.status_code == 200:
            return res
        return None

    """获取商品信息"""
    def page(self, url):
        item = {}
        res = self.parse_page(url)
        res.encoding = 'gbk'
        pattern = re.compile('<title>(.*?)</title>')
        title = re.findall(pattern, res.text)[0]
        if title[-3:] == u'淘宝网':
            pattern2 = re.compile('<em class="tb-rmb-num">(.*?)</em>')
            price = re.findall(pattern2, res.text)[0]
            item['title'] =title
            item['price'] = price
            item['url'] = url
        return item

    """获取单个页面商品链接"""
    def get_one_page_links(self, kw, pn):
        links = []
        key = kw
        url = self.pageurl + key + '&search_type=item&s=' + str(44*pn)
        res = self.parse_page(url)
        pattern = re.compile('"nid":"(.*?)"')
        allid = re.findall(pattern, res.text)
        for urlid in allid:
            thisurl = self.idurl + urlid
            links.append(thisurl)
        return links


    """获取所有链接"""
    def get_all_links(self, kw, n):
        for pn in range(n):
            self.urls.extend(self.get_one_page_links(kw, pn))
            self.nums = len(self.urls)

    """获取所有商品商品信息"""
    def get_all_shop(self, kw, n):
        data = []
        for pn in range(n):
            links = self.get_one_page_links(kw, pn)
            for url in links:
                print(url)
                item = self.page(url)
                if item:
                    data.append(item)
        return data

    """写入csv文件"""
    def writer_csv(self, kw, link):
        shop = self.page(link)
        if shop:
            items = []
            for k, v in shop.items():
                items.append(v)
            with open(self.path + kw+'.csv', 'a') as csvfile:
                f = csv.writer(csvfile)
                f.writerow(items)

    def save_json(self, item):
        if item:
            with open(kw+'.json', 'a', encoding='utf-8') as f:
                content = json.dumps(item, ensure_ascii=False) + '\n'
                f.write(content)
                print('Save success')
        else:
            print('Empy data')




    """下载入口"""
    def download(self, kw, n):
        for pn in range(n):
            self.urls.extend(self.get_one_page_links(kw, pn))
        threads = [threading.Thread(target=self.writer_csv, args=(kw, link,)) for link in self.urls]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    def taobao_main(self,kw,offset):
        print('正在解析第{}页'.format(offset))
        links = self.get_one_page_links(kw, offset)
        for link in links:
            print('正在下载：{}'.format(link))
            item = self.page(link)
            self.save_json(item)

    @run
    def thread_enter(self, kw, n):
        '''
        淘宝商品多线程下载入口
        :param kw:
        :param n:
        :return:
        '''
        threads = [threading.Thread(target=self.taobao_main, args=(kw, offset )) for offset in range(n)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        return True

######################################################################################
if __name__ == '__main__':
    kw = input("input item: ")
    n = int(input('input page counts: '))
    t = TaobaoScrawl()
    isOk = t.thread_enter(kw, n)
    if isOk:
        print('ok')
