# -*- coding: utf-8 -*-
# @Time    : 2021/8/9 5:41 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_tools.py
# @Software: PyCharm

import json

import requests


def current_request(method=None, **kwargs):
    """
    构造请求
    :param method: 请求方式
    :param kwargs: 请求体以及扩展参数
    :return:
    """

    def json_format(d):
        """json格式打印"""
        try:
            print(json.dumps(d, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False))
        except BaseException as e:
            # print('json格式打印异常:{}\n'.format(str(e)))
            print(d)

    def show_log(url=None, headers_param=None, json_param=None, json_response=None):
        """
        打印请求日志
        :param url: URL
        :param headers_param: 请求头
        :param json_param: 请求体
        :param json_response: 返回值
        :return:
        """
        try:
            print('=' * 33 + ' url ' + '=' * 33)
            print(url)

            print('=' * 33 + ' headers param ' + '=' * 33)
            json_format(headers_param)

            print('=' * 33 + ' json or param ' + '=' * 33)
            json_format(json_param)

            print('=' * 33 + ' response ' + '=' * 33)
            json_format(json_response)

            print('=' * 33 + ' end show log ' + '=' * 33)
        except BaseException as e:
            print('show_log error {}'.format(str(e)))

    current_url = kwargs.get('url')
    current_headers = kwargs.get('headers', {})
    d = kwargs.get('json', kwargs.get('data', kwargs.get('params')))

    if kwargs.get('other'):
        del kwargs['other']
    else:
        pass

    if hasattr(requests, method):
        response = getattr(requests, method)(**kwargs, verify=False)
        show_log(current_url, current_headers, d, response.json())
    else:
        response = {
            "error": "requests 没有 {} 方法".format(method)
        }
        show_log(current_url, current_headers, d, response)
    return response
