# _*_ coding: utf-8 _*_
# @Time     : 2018/6/26 21:18
# @Author   : Ole211
# @Site     : 
# @File     : tieba_scrawl.py    
# @Software : PyCharm4

import re
import json
import requests
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

class TiebaScrawl(object):
    def __init__(self):
        self.server = url
        self.nums = 0

    def parse_page(self, target):
        """网页解析"""
        res = requests.get(url=target, headers = headers)
        if res.status_code == 200:
            return res.text
        return None

    def get_one_page_data(self, target):
        """获取单个页面数据"""
        html = self.parse_page(target)
        pattern = re.compile('<div class="t_con cleafix">.*? title="回复">(.*?)</span>'+
                          '.*? href="/p/(.*?)" title="(.*?)" target='+
                          '.*?target="_blank">(.*?)</a></span>'+
                        '.*?title="创建时间">(.*?)</span>.*?</div>', re.S)
        allid = re.findall(pattern, html)
        pagedata = []
        print(allid)
        for i in allid:
            page = {}
            page['replynum'] = int(i[0])
            page['url'] = self.server + i[1]
            page['title'] = i[2]
            page['author'] = i[3]
            page['createtime'] = i[4]
            pagedata.append(page)
        print(pagedata)
        return pagedata

    def get_data(self, name, begin_page, end_page):
        """获取全部数据"""
        data = []
        kw = name
        self.nums = int(end_page) - int(begin_page)
        for i in range(int(begin_page), int(end_page)):
            pn = (i-1) * 50
            target = self.server + kw + '&pn=' +str(pn)
            pagedata = self.get_one_page_data(target)
            data.extend(pagedata)
        return data

    def download(self, name, begin_page, end_page):
        """下载入口"""
        total_data = []
        kw = name
        self.nums = end_page - begin_page
        print('开始下载', name)
        for i in range(begin_page, end_page):
            pn = (i-1) * 50
            target = self.server + kw + '&pn=' + str(pn)
            pagedata = self.get_one_page_data(target)
            total_data.extend(pagedata)
            sys.stdout.write('  已经下载; %.3f%%' % float(i/self.nums*100) + '\r')
            sys.stdout.flush()
        df = pd.DataFrame(total_data)
        df.to_csv('./' + kw + '.csv')
        print('下载完成')
        return total_data

if __name__ == '__main__':
    kw = input('输入贴吧名称：')
    begin = int(input('起始页：'))
    end = int(input('结束页：'))
    d1 = TiebaScrawl()
    data = d1.get_data(kw, begin, end)
    for i in data:
        print(i)