# _*_ coding: utf-8 _*_
# @Time     : 2018/8/4 0:05
# @Author   : Ole211
# @Site     : 
# @File     : run_time.py    
# @Software : PyCharm
import time
from datetime import datetime

def run_time(func):
    def wrapper(*args, **kwargs):
        t0 = time.time()
        now0 = datetime.now()
        print('start time: {}'.format(now0))
        back = func(*args, **kwargs)
        now = datetime.now()
        print('end time: {}'.format(now))
        print('run time: {}'.format(time.time() - t0))
        return back
    return wrapper

