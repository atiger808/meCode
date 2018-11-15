# _*_ coding: utf-8 _*_
# @Time     : 2018/8/5 14:19
# @Author   : Ole211
# @Site     : 
# @File     : huawei.py    
# @Software : PyCharm

import requests
from bs4 import BeautifulSoup as bs
import re
from run_time import run_time as run
from setting import headers
import json
import os
import multiprocessing
import threading
import asyncio


base_url = 'https://www.huawei.com'
news_main_url = 'https://www.huawei.com/cn/press-events/news'
target_url = ['https://www.huawei.com/cn/press-events/news?d=ws&pagesize=10&pageindex={}'.format(offset) for offset in range(1, 3)]

def parse(url):
    '''
    页面解析函数
    :param url:
    :return:
    '''
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        return res.text
    return None

def get_total_count(news_main_url):
    '''
    获取新闻页面总页数
    :param news_main_url:
    :return:
    '''
    html = parse(news_main_url)
    soup = bs(html, 'html.parser')
    total_count = int(soup.find(id='span-total-count').text.strip())
    return total_count

def save_json(dic):
    '''
    保存为json 文件函数
    :param dic:
    :return:
    '''
    if dic:
        with open('d:/huaweiNews.json', 'a', encoding='utf-8') as f:
            content = json.dumps(dic, ensure_ascii=False) + '\n'
            f.write(content)
        print('Save Success')
    else:
        print('Empty data')

def get_content(news_url):
    '''
    获取页面数据
    返回一个字典
    :param news_url:
    :return:
    '''
    html = parse(news_url)
    if html:
        soup = bs(html, 'html.parser')
        dic = {}
        dic['title'] = soup.find(class_='title').find('h1').text.strip()
        dic['date'] = soup.find(class_='title').find('span').text.strip()
        dic['url'] = news_url
        div = soup.find(id='newsContent').findAll('div')
        for i in div:
            p = i.findAll('p')
            if p:
                dic['content'] = i.text
                return dic
    return None

def get_links(target_url):
    '''
    返回一个翻页页面的所有新闻链接
    :param target_url:
    :return:
    '''
    html = parse(target_url)
    if html:
        soup = bs(html, 'html.parser')
        a = soup.findAll('a', href=re.compile('^(/cn/)'))
        news_url = []
        for link in a:
            if 'href' in link.attrs:
                news_url.append(link.attrs['href'])
    return news_url



def main(offset):
    '''
    开始执行函数
    :param offset:
    :return:
    '''
    target_url = 'https://www.huawei.com/cn/press-events/news?d=ws&pagesize=10&pageindex={}'.format(offset)
    print('正在下载第%s页' % offset)
    links = get_links(target_url)
    for link in links:
        news_url = base_url + link
        dic = get_content(news_url)
        print('正在保存: %s' % news_url)
        save_json(dic)

@run
def multi_enter(n):
    '''
    多进程下载版本入口
    :param n:
    :return:
    '''
    processes = [multiprocessing.Process(target=main, args=(offset, )) for offset in range(1, n+1)]
    for t in processes:
        t.start()
    for t in processes:
        t.join()

@run
def thread_enter(n):
    '''
    多线程下载版本入口
    :param n:
    :return:
    '''
    threads = [threading.Thread(target=main, args=(offset, )) for offset in range(1, n+1)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


###################################
#      以下为异步下载部分        #

async def task(offset):
    main(offset)
    # await asyncio.sleep(1)


async def async_main(loop, n):
    tasks = [loop.create_task(task(offset)) for offset in range(1, n+1)]
    await asyncio.wait(tasks)

@run
def async_enter(n):
    '''
    异步下载版本入口
    :param n:
    :return:
    '''
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_main(loop, n))
    loop.close()

#             END                 #
###################################

if __name__ == '__main__':
    # if os.path.exists('d:/huaweiNews.json'):
    #     os.remove('d:/huaweiNews.json')
    #     print('删除成功')
    n = get_total_count(news_main_url)
    # print(type(n))
    # thread_enter(n)
    # multi_enter(n)
    # async_enter(5)

