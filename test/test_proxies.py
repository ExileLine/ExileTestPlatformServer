# -*- coding: utf-8 -*-
# @Time    : 2022/6/27 18:46
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test_proxies.py
# @Software: PyCharm


import requests

s = {'url': 'http://106.75.174.40:5000/api/login', 'headers': {}, 'json': {'password': '123456', 'username': 'admin'}}

proxies = {
    'http': '192.168.9.103:7007',
    'https': '192.168.9.103:7007',
}

if __name__ == '__main__':
    r = requests.post(**s, proxies=proxies)
    print(r)
    print(r.json())
