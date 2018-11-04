# _*_ coding: utf-8 _*_
# @Time     : 2018/7/16 0:34
# @Author   : Ole211
# @Site     : 
# @File     : dagong.py    
# @Software : PyCharm
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')
import threading
from run_time import run_time as run
import time



headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',

}
class Dagong(object):
    def __init__(self):
        self.server = 'http://www.wodedagong.com'
        self.target = 'http://www.wodedagong.com/AjaxTools/GetDataHandler.ashx?action=get_more_enterprise'
        self.headers = headers
        self.urls = []
        self.nums = 0

    def parse(self, target):
        res = requests.get(url=target, headers=self.headers)
        if res.status_code == 200:
            return res.text
        return None

    def parse_page(self):
        data = {
            'PageIndex': '4',
            'EnterpriseType': '0'
        }
        res = requests.post(url=self.target, params=data, headers=self.headers)
        if res.status_code == 200:
            return res.text
        return None

    def get_links(self):
        html = self.parse(self.target)
        soup = bs(html, 'html.parser')
        a = soup.select('a')
        for i in a:
            t = self.server + i['href']
            self.urls.append(t)
        self.urls = list(set(self.urls))
        self.nums = len(self.urls)


    def get_one_page_info(self, pageurl):
        html = self.parse(pageurl)
        soup = bs(html, 'html.parser')
        info = {}
        info['title'] = soup.select('#ctl00_ContentPlaceHolder1_ent_title')[0].text
        info['price'] = soup.select('#ctl00_ContentPlaceHolder1_ent_price')[0].text
        info['int_price'] = [int(i.strip('元')) for i in  info['price'].split('-')]
        info['average_price'] = sum(info['int_price'])/2
        info['WageDes'] = soup.select('#ctl00_ContentPlaceHolder1_LabelWageDes')[0].text
        info['WorkDes'] = soup.select('#ctl00_ContentPlaceHolder1_LabelWorkDes')[0].text
        info['EnterpriseDes'] = soup.select('#ctl00_ContentPlaceHolder1_LabelEnterpriseDesc')[0].text
        return info

    @run
    def write_to_file(self,url):
        content = self.get_one_page_info(url)
        with open('./job.txt', 'a') as f:
            f.write(json.dumps(content, ensure_ascii=False) + '\n')
            f.close()

    # 保存为csv
    @run
    def write_to_csv(self):
        data = []
        # for url in self.urls:
        #     print(url)
        #     data.append(self.get_one_page_info(url))
        for i in range(self.nums):
            print(i, self.urls[i])
            try:
                data.append(self.get_one_page_info(self.urls[i]))
            except Exception as e:
                print(e)
                continue
            print(' 已经下载： %.3f%%' % float(i/self.nums*100) + '\r')
        df = pd.DataFrame(data)
        df.to_csv('job.csv', encoding='utf_8_sig')
        print('保存csv成功！')

    # 多线程下载,保存txt
    @run
    def download(self):
        print(self.nums)
        threads = [threading.Thread(target=self.write_to_file, args=(url,))
                   for url in self.urls]
        for t in threads:
            t.start()
        for t in threads:
            t.join()



if __name__ == '__main__':
    d = Dagong()
    d.get_links()
    print(d.nums)
    print('暂停3秒')
    time.sleep(3)

    #保存csv
    d.write_to_csv()

    # 多线程下载，保存TXT
    # d.download()


    # d = Dagong()
    # d.get_links()
    # print('开始下载')
    # for i in range(d.nums):
    #     d.write_to_file(d.get_one_page_info(d.urls[i]))
    #     sys.stdout.write('  已下载： %.3f%%' % float(i/d.nums*100) + '\r')
    #     sys.stdout.flush()
    # print('下载完成')


