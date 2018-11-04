# _*_ coding: utf-8 _*_
# @Time     : 2018/8/3 20:52
# @Author   : Ole211
# @Site     : 
# @File     : hikvision.py    
# @Software : PyCharm

import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import sqlite3
import json
import multiprocessing
import threading
import asyncio
from run_time import run_time as run

lock = threading.Lock()

headers = {
'Cookie': 'UM_distinctid=164ffcfa9bf42c-060de39e6e2fa4-541f3415-144000-164ffcfa9c07a4; CNZZDATA1262633151=134277208-1533300087-http%253A%252F%252Fwww.hikvision.com%252F%7C1533300087; ASP.NET_SessionId=gtv1eqfwmuemvz45g3npimfp; bdshare_firstime=1533300263300',
'Host': 'www.hikvision.com',
'Origin': 'http://www.hikvision.com',
'Referer': 'http://www.hikvision.com/cn/newsmt_xx_63.html',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
'X-Requested-With': 'XMLHttpRequest',
}

base_url = 'http://www.hikvision.com/cn/'
index_url = 'http://www.hikvision.com/cn/newsmt_xx_63.html'
img_base_url = 'http://www.hikvision.com'
post_url = 'http://www.hikvision.com/ashx/newstp.ashx'
newsurl = 'http://www.hikvision.com/cn/news_detail_63_i2508.html'

class Hikvision_DB(object):

    def __init__(self):
        self.conn = None

    def create_db(self):
        self.conn = sqlite3.connect('d:/hk_test.db')
        # 创建 hikvison 表
        self.conn.execute("""
        create table if not exists hk_test (
        id INTEGER PRIMARY KEY,
        date DATE DEFAULT NULL,
        title varchar DEFAULT NULL,
        counts INTEGER DEFAULT NULL,
        content varchar DEFAULT NULL,
        url varchar DEFAULT NULL)
        """)

    def save_db(self, dic):
        if dic:
            data = (dic['url_id'], dic['date'], dic['title'], dic['updatehit_counts'], dic['content'], dic['url'])
            insert_hikvision_cmd = "insert or replace into hk_test (id, date, title, counts, content, url) values (?, ?, ?, ?, ?, ?)"
            self.conn.execute(insert_hikvision_cmd, data)
            self.conn.commit()
            self.conn.close()
            print('Save db Success')
        else:
            print('Empty data')


def parse(post_url, offset):
    '''
    通过 post 请求，返回页面数据
    :param post_url:
    :param offset: 页面索引
    :return:
    '''
    data = {
        'pageIndex': str(offset),
        'pageSize': '5',
        'kind2': '63',
        'kind': '63',
        'stat': '1',
    }
    res = requests.post(post_url, headers=headers, data=data)
    if res.status_code == 200:
        return res.text
    return None


def get_one_page_links(post_url, offset):
    '''
    获取单个翻页新闻链接
    :param post_url:
    :param offset:
    :return: news_urls 新闻链接
    '''
    news_urls = []
    html = parse(post_url, offset)
    if html:
        print('正在解析第{}页'.format(offset))
        soup = bs(html, 'html.parser')
        links  =  soup.findAll('a')
        for i in links:
            if '查看详细' in i.text:
                continue
            link = base_url + i['href']
            news_urls.append(link)
    return news_urls


def get_updatehit(newsurl):
    '''
    获取新闻浏览数
    :param newsurl:
    :return:
    '''
    updatehit_id = re.findall(re.compile(r'_i(.*?).html'), newsurl)[0]
    updatehit_url = 'http://www.hikvision.com/cn/ashx/updatehit.ashx?id={}&type=1'.format(updatehit_id)
    res = requests.get(updatehit_url, headers=headers)
    if res.status_code == 200:
        return int(res.text.strip()), int(updatehit_id)
    return None

def save_csv():
    pass

def get_newsurl_data(newsurl):
    '''
    获取单个新闻页面数据
    :param newsurl:
    :return:
    '''
    res = requests.get(newsurl, headers=headers)
    res.encoding='utf-8'
    soup = bs(res.text, 'html.parser')
    dic = {}
    try:
        dic['date'] = soup.findAll(class_='newsxx')[0].findAll(class_= 'newsxxtime')[1].find('span').text.split('：')[-1]
        dic['updatehit_counts'], dic['url_id'] = get_updatehit(newsurl)
        dic['title'] = soup.find(class_ = 'newsxxtop').text.strip()
        dic['content'] = '\n'.join([p.text.strip() for p in soup.find(class_='newsxxbody').findAll('p')])
        dic['url'] = newsurl
        # img = soup.find(class_ = 'newsxxbody').findAll('img')
        # img_url = [img_base_url+i['src'] for i in img ]
        # img_title = [i['title'] for i in img ]
    except Exception as e:
        print('下载失败：{}'.format(newsurl))
        print(e)
    finally:
        return dic

    # print(date)
    # print(updatehit_counts)
    # print(title)
    # print(img)
    # print(img_url)
    # print(img_title)
    # print(content)



def down_load_html(offset):
    newsurls = get_one_page_links(post_url, offset)
    for newsurl in newsurls:
        print('正在下载：{}'.format(newsurl))
        dic = get_newsurl_data(newsurl)
        # 未启用线程锁
        # d = Hikvision_DB()
        # d.create_db()
        # d.save_db(dic)

        # 启动线程锁
        lock.acquire()
        try:
            d = Hikvision_DB()
            d.create_db()
            d.save_db(dic)
        finally:
            lock.release()



@run
def go(offset):
    total_data = []
    for offset in range(1, offset):
        one_page_links = get_one_page_links(post_url, offset)
        for newsurl in one_page_links:
            print('正在爬取：{}'.format(newsurl))
            dic = get_newsurl_data(newsurl)
            total_data.append(dic)
    return total_data


@run
def multi_main(n):
    """
    多进程下载版本
    :return:
    """
    processes = [multiprocessing.Process(target=down_load_html, args=(offset, )) for offset in range(1, n)]
    for t in processes:
        t.start()
    for t in processes:
        t.join()

@run
def thread_main(n):
    """
    多线程下载版本
    :return:
    """
    threads = [threading.Thread(target=down_load_html, args=(offset, )) for offset in range(1, n)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


async def task(offset):
    down_load_html(offset)


async def main(loop, n):
    """
    异步下载版本
    :param loop:
    :return:
    """
    tasks = [loop.create_task(task(offset)) for offset in range(1, n+1)]
    await asyncio.wait(tasks)

def async_main(n):
    # 建立 loop
    loop = asyncio.get_event_loop()
    # 执行 loop
    loop.run_until_complete(main(loop, n))
    # 关闭loop
    loop.close()


if __name__ == '__main__':
    # multi_main(20)  # 会出现io读取被locked的情况
    thread_main(20)   #未出现被locked的情况
    # async_main(20)
    # df = pd.DataFrame(go(155))
    # df.to_csv('hk.csv')
    # print('完成')

