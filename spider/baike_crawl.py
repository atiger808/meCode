# _*_ coding: utf-8 _*_
# @Time     : 2018/8/8 2:05
# @Author   : Ole211
# @Site     : 
# @File     : baike_crawl.py    
# @Software : PyCharm

import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
import random
import time
import os
import re
import codecs
# from headers import headers
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

headers = {
'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
'upgrade-insecure-requests':'1',
}

random.seed(datetime.now())
def get_links(article_url):
    start_url = 'https://baike.baidu.com{}?bk_fr=chain_bottom&timestamp={}'.format(article_url, str(int(time.time()*1000)))
    res = requests.get(start_url, headers=headers)
    if res.status_code == 200:
        res.encoding = 'utf-8'
        soup = bs(res.text, 'html.parser')
        # 获取内容
        content= soup.findAll(class_='para')
        return content, soup.find(class_='lemma-summary').findAll('a', href=re.compile('^(/item/)'))
    print('fail: {}'.format(start_url))
    return None

def save_txt(filename, content):
    filepath = 'static/documents/' + filename + '.txt'
    # filepath = filepath.decode('utf8')
    print(filepath)
    time.sleep(5)

    if not os.path.exists(filepath):
        with codecs.open(filepath, 'w') as f:
            for i in content:
                f.write(i.text.strip() + '\n')
        print('download Done..')
    else:
        print('already exists')

def go(kw):
    content, links = get_links('/item/'+kw)
    n = 0
    while len(links) > 0:
        link = links[random.randint(0, len(links)-1)]
        n +=1
        print(link.text)
        save_txt(link.text.strip(), content)
        start_url = 'https://baike.baidu.com{}?bk_fr=chain_bottom&timestamp={}'.format(link.attrs['href'], str(int(time.time()*1000)))
        print(start_url)
        content, links = get_links(link.attrs['href'])
    print('over')


if __name__ == '__main__':
    kw = raw_input('input kw: ')
    go(kw)