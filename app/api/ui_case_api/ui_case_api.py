# -*- coding: utf-8 -*-
# @Time    : 2023/1/17 14:31
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : ui_case_api.py
# @Software: PyCharm

from all_reference import *


class UiCaseApi(MethodView):
    """
    UI用例 Api
    GET: UI用例详情
    POST: 新增UI用例
    PUT: 编辑UI用例
    DELETE: 删除UI用例
    """

    def get(self, ui_case_id):
        """UI用例详情"""

        meta_data = [
            {
                "uuid": "RqceT7F7VR7MUepkCe3TgP",
                "index": 1,
                "title": "开始",
                "type": "master",
                "business_list": [
                    {
                        "uuid": "43mcDsxMP5hfgwXpYFekNf",
                        "index": 1,
                        "type": "ui_control",
                        "title": "启动浏览器控件",
                        "function": "open",
                        "args": {
                            "url": "http://localhost:3200/login"
                        }
                    }
                ]
            },
            {
                "uuid": "Paahmn4pisq6DCMAb6MTj7",
                "index": 2,
                "title": "登录",
                "type": "master",
                "business_list": [
                    {
                        "uuid": "BeKExy3oDBmffkyh6z5sFh",
                        "index": 1,
                        "type": "ui_control",
                        "title": "应用A，页面A，输入账号",
                        "function": "input",
                        "args": {
                            "mode": "XPATH",
                            "value": "//*[@id=\"login-form\"]/div[1]/div[2]/div/div/div/input",
                            "data": "admin"
                        }
                    },
                    {
                        "uuid": "TgxCgmQ3eAiYJ9poTDa3y8",
                        "index": 2,
                        "type": "ui_control",
                        "title": "输入密码",
                        "function": "input",
                        "args": {
                            "mode": "XPATH",
                            "value": "//*[@id=\"login-form\"]/div[2]/div[2]/div/div/div/input",
                            "data": "123456"
                        }
                    },
                    {
                        "uuid": "bAYF8u42at5VDYHRwc63bu",
                        "index": 3,
                        "type": "ui_control",
                        "title": "点击登录",
                        "function": "click",
                        "args": {
                            "mode": "XPATH",
                            "value": "//*[@id=\"login-form\"]/div[3]/div[2]/div/div/div/button[1]"
                        }
                    },
                ]
            },
            {
                "uuid": "DuykYPs5UhqhULXCqerzGq",
                "index": 3,
                "title": "嵌套循环操作",
                "type": "master",
                "business_list": [
                    {
                        "uuid": "VwfKjeL87DVythEsHsC8Jd",
                        "index": 1,
                        "type": "logic_control",
                        "title": "第一层循环",
                        "function": "for",
                        "num": 3,
                        "data_source": [],
                        "business_list": [
                            {
                                "uuid": "BeKExy3oDBmffkyh6z5sFh",
                                "index": 1,
                                "type": "ui_control",
                                "title": "输入账号",
                                "function": "input",
                                "args": {
                                    "mode": "XPATH",
                                    "value": "//*[@id=\"login-form\"]/div[1]/div[2]/div/div/div/input",
                                    "data": "admin"
                                }
                            },
                            {
                                "uuid": "TgxCgmQ3eAiYJ9poTDa3y8",
                                "index": 2,
                                "type": "ui_control",
                                "title": "输入密码",
                                "function": "input",
                                "args": {
                                    "mode": "XPATH",
                                    "value": "//*[@id=\"login-form\"]/div[2]/div[2]/div/div/div/input",
                                    "data": "123456"
                                }
                            },
                            {
                                "uuid": "bAYF8u42at5VDYHRwc63bu",
                                "index": 3,
                                "type": "ui_control",
                                "title": "点击登录",
                                "function": "click",
                                "args": {
                                    "mode": "XPATH",
                                    "value": "//*[@id=\"login-form\"]/div[3]/div[2]/div/div/div/button[1]"
                                }
                            },
                            {
                                "uuid": "bzjmqAUjuYTs3sASxoXh3r",
                                "index": 4,
                                "type": "logic_control",
                                "title": "第二层循环",
                                "function": "for",
                                "num": 3,
                                "data_source": [],
                                "business_list": [
                                    {
                                        "uuid": "6nBzTGWXAaDdE8fo5XaGVr",
                                        "index": 11,
                                        "type": "ui_control",
                                        "title": "输入项目名称",
                                        "function": "input",
                                        "args": {
                                            "mode": "XPATH",
                                            "value": "//*[@id=\"project-search-container\"]/div/form/div/div/div/input",
                                            "data": "zxc"
                                        }
                                    },
                                    {
                                        "uuid": "oHCN6jjbDCYWzgjzNojecC",
                                        "index": 22,
                                        "type": "ui_control",
                                        "title": "点击搜索",
                                        "function": "click",
                                        "args": {
                                            "mode": "XPATH",
                                            "value": "//*[@id=\"project-search-container\"]/div/form/div/span"
                                        }
                                    },
                                    {
                                        "uuid": "dPHmBmPcAGpp5zqcX7MsUV",
                                        "index": 33,
                                        "type": "ui_control",
                                        "title": "点击项目3",
                                        "function": "click",
                                        "args": {
                                            "mode": "XPATH",
                                            "value": "//*[@id=\"main-container\"]/div[1]/div[1]/div/div"
                                        }
                                    },
                                    {
                                        "uuid": "68AUdem7SfBnx8CAQs3Uen",
                                        "index": 3332,
                                        "type": "ui_control",
                                        "title": "点击暗夜2",
                                        "function": "click",
                                        "args": {
                                            "mode": "XPATH",
                                            "value": "//*[@id=\"app\"]/div/div[1]/div[2]/div[3]"
                                        }
                                    },
                                    {
                                        "uuid": "fhHpv6Wa9ADgJP3xdoG79c",
                                        "index": 3331,
                                        "type": "ui_control",
                                        "title": "点击光明2",
                                        "function": "click",
                                        "args": {
                                            "mode": "XPATH",
                                            "value": "//*[@id=\"app\"]/div/div[1]/div[2]/div[2]"
                                        }
                                    },
                                    {
                                        "uuid": "gdympUTxBA59FGNt9J6D8f",
                                        "index": 1,
                                        "type": "ui_control",
                                        "title": "点击前往首页",
                                        "function": "click",
                                        "args": {
                                            "mode": "XPATH",
                                            "value": "//*[@id=\"app\"]/div/div[1]/div[1]/div[1]/span"
                                        }
                                    }
                                ]
                            },
                            {
                                "uuid": "Ca8QoABC2QtnjzfHtkAfsq",
                                "index": 4,
                                "type": "ui_control",
                                "title": "点击下拉",
                                "function": "click",
                                "args": {
                                    "mode": "XPATH",
                                    "value": "//*[@id=\"app\"]/div/div[1]/button[4]/span/div"
                                }
                            },
                            {
                                "uuid": "Zf3tJvN3t4n8RFLCiTVYLm",
                                "index": 5,
                                "type": "ui_control",
                                "title": "点击退出",
                                "function": "click",
                                "args": {
                                    "mode": "XPATH",
                                    "value": "/html/body/div[2]/div/div/div/div[3]/li/span/div"
                                }
                            }
                        ]
                    }
                ]
            },
            {
                "uuid": "3Lr7gkJx9WjXr8DRzWoU4e",
                "index": 1,
                "title": "结束",
                "type": "master",
                "business_list": [
                    {
                        "uuid": "e6rL6LWxRZkyGYkQadn3yz",
                        "index": 1,
                        "type": "ui_control",
                        "title": "关闭浏览器",
                        "function": "close",
                        "args": {}
                    }
                ]
            }
        ]
        return api_result(code=SUCCESS, message=SUCCESS_MESSAGE, data=meta_data)

    def post(self):
        """新增UI用例"""
        return api_result(code=POST_SUCCESS, message=POST_MESSAGE, data=[])

    def put(self):
        """编辑UI用例"""
        return api_result(code=PUT_SUCCESS, message=PUT_MESSAGE, data=[])

    def delete(self):
        """删除UI用例"""
        return api_result(code=DEL_SUCCESS, message=DEL_MESSAGE, data=[])
