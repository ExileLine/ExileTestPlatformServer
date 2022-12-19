# -*- coding: utf-8 -*-
# @Time    : 2022/12/14 17:08
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test_celery.py
# @Software: PyCharm

import time
import datetime

import requests
from celery.result import AsyncResult
from celery_app import cel


def main(n):
    """并发测试"""
    start_time = time.time()
    for i in range(0, n):
        headers = {
            'token': '123',
            'Content-Type': 'application/json'
        }
        res = requests.get(url="http://0.0.0.0:7878/api/test_celery", headers=headers, verify=False)
        print(i, res.json())
    end_time = time.time()
    print(start_time)
    print(end_time)
    print(end_time - start_time)
    print(time.time())
    print(datetime.datetime.now())


def get_res(i):
    """获取异步任务结果"""

    res = AsyncResult(id=i, app=cel)
    print(res.get())


if __name__ == '__main__':
    """
    12进程300并发
        
        任务触发最后时间:
            299 {'code': 200, 'data': ['7f365941-19fb-4c3d-989e-3417920b33f8'], 'message': '调试Celery异步任务'}
            1671011664.696519
            1671011669.9463391
            5.249820232391357
            1671011669.946368
            2022-12-14 17:54:29.946373
        
        最后一个任务完成的时间:
            {'message': '完成向yyx123发送邮件任务', 'datetime': '2022-12-14T17:55:15.200119', 'time': 1671011715.20056}
        
        总耗时:
            45.25s
    
    24进程300并发
        
        任务触发最后时间:
            299 {'code': 200, 'data': ['6867be88-66e5-431c-a0c8-a232ddc6f47f'], 'message': '调试Celery异步任务'}
            1671011935.80136
            1671011941.267381
            5.4660210609436035
            1671011941.267408
            2022-12-14 17:59:01.267413
        
        最后一个任务完成的时间:
            {'message': '完成向yyx123发送邮件任务', 'datetime': '2022-12-14T17:59:22.214532', 'time': 1671011962.214887}
        
        总耗时:
            20.94s
    
    36进程300并发
        
        任务触发最后时间:
            299 {'code': 200, 'data': ['77efa261-d875-46a7-a546-f7ce0537d901'], 'message': '调试Celery异步任务'}
            1671012379.370048
            1671012385.160349
            5.7903008460998535
            1671012385.160379
            2022-12-14 18:06:25.160385
            
        最后一个任务完成的时间:    
            {'message': '完成向yyx123发送邮件任务', 'datetime': '2022-12-14T18:06:37.787768', 'time': 1671012397.788213}
            
        总耗时:
            12.63s
    """

    main(120)
    # get_res(i="77efa261-d875-46a7-a546-f7ce0537d901")
