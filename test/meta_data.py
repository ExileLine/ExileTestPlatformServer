# -*- coding: utf-8 -*-
# @Time    : 2023/1/4 14:36
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : meta_data.py
# @Software: PyCharm


import json

ccc = {
    "index": 5,
    "title": "循环四(业务块)",
    "type": "master",
    "business_list": [
        {
            "index": 1,
            "type": "ui_control",
            "desc": "循环四-点击控件1",
            "function": "click",
            "args": {}
        },
        {
            "index": 2,
            "type": "logic_control",
            "function": "for",
            "num": 2,
            "data_source": [],
            "action": [
                {
                    "index": 771,
                    "type": "ui_control",
                    "desc": "循环四-内循环-点击控件1",
                    "function": "click",
                    "args": {}
                }
            ]
        }
    ]
}

meta_data = [
    {
        "index": 1,
        "title": "开始",
        "type": "master",
        "business_list": [
            {
                "index": 1,
                "type": "ui_control",
                "desc": "启动浏览器控件",
                "function": "open",
                "args": {
                    "url": "https://www.github.com"
                }
            },
        ]
    },
    {
        "index": 2,
        "title": "登录",
        "type": "master",
        "business_list": [
            {
                "index": 1,
                "type": "ui_control",
                "desc": "输入控件",
                "function": "input",
                "args": {
                    "username": "admin"
                }
            },
            {
                "index": 2,
                "type": "ui_control",
                "desc": "输入控件",
                "function": "input",
                "args": {
                    "password": "123456"
                }
            },
            {
                "index": 3,
                "type": "ui_control",
                "desc": "点击控件",
                "function": "click",
                "args": {}
            },
            {
                "index": 4,
                "title": "检验是否登录成功",
                "type": "master",
                "business_list": [
                    {
                        "index": 1,
                        "type": "assert_control",
                        "function": "ui_assert",
                        "args": {
                            "expected_results": "aaa",
                            "rule": "==",
                            "actual_results": "",
                            "actual_results_source": {
                                "source": "web_ui",
                                "args": {
                                    "web_ui": {},
                                    "api_response": {}
                                }
                            },
                        }
                    },
                ]
            },
        ]
    },
    {
        "index": 3,
        "title": "循环录入数据",
        "type": "master",
        "business_list": [
            {
                "index": 1,
                "type": "logic_control",
                "function": "for",
                "num": 2,  # 调试
                "data_source": [],
                "action": [
                    {
                        "index": 1,
                        "type": "ui_control",
                        "desc": "输入控件A",
                        "function": "input",
                        "args": {
                            "username": "admin"
                        }
                    },
                    {
                        "index": 2,
                        "type": "ui_control",
                        "desc": "输入控件B",
                        "function": "input",
                        "args": {
                            "password": "123456"
                        }
                    },
                    {
                        "index": 3,
                        "type": "ui_control",
                        "desc": "点击控件C",
                        "function": "click",
                        "args": {}
                    },
                    {
                        "index": 4,
                        "type": "logic",
                        "desc": "循环二(逻辑块)",
                        "function": "for",
                        "num": 5,
                        "data_source": [],
                        "action": [
                            {
                                "index": 11,
                                "type": "ui_control",
                                "desc": "点击控件X",
                                "function": "click",
                                "args": {}
                            },
                            {
                                "index": 22,
                                "type": "ui_control",
                                "desc": "点击控件Y",
                                "function": "click",
                                "args": {}
                            },
                            {
                                "index": 33,
                                "type": "ui_control",
                                "desc": "点击控件Z",
                                "function": "click",
                                "args": {}
                            },
                            {
                                "index": 44,
                                "type": "logic",
                                "desc": "循环三(逻辑块)",
                                "function": "for",
                                "num": 2,
                                "data_source": [],
                                "action": [
                                    {
                                        "index": 3331,
                                        "type": "ui_control",
                                        "desc": "===点击控件OKC-1===",
                                        "function": "click",
                                        "args": {}
                                    },
                                    {
                                        "index": 3332,
                                        "type": "ui_control",
                                        "desc": "===点击控件OKC-2===",
                                        "function": "click",
                                        "args": {}
                                    },
                                ]
                            }
                        ]
                    },
                    ccc
                ]
            },
            {
                "index": 2,
                "title": "操作2",
                "type": "master",
                "business_list": [
                    {
                        "index": 1,
                        "type": "ui_control",
                        "desc": "点击控件",
                        "function": "click",
                        "args": {}
                    },
                ]
            }
        ]
    }
]


class CustomLogic:
    """自定义逻辑"""

    @classmethod
    def _if(cls, _b: any) -> bool:
        """if"""

        if _b:
            return True
        else:
            return False

    @classmethod
    def _for(cls, business_list: list, *args):
        """for"""

        for b in business_list:
            print(b, args)

    @classmethod
    def _try(cls, _t, _e):
        """try"""

        try:
            _t
        except BaseException as e:
            _e


logic_dict = {
    "if": CustomLogic._if,
    "for": CustomLogic._for,
    "try": CustomLogic._try
}


def get_logic(business_dict: dict) -> any:
    """

    :param business_dict: 逻辑块对象
    :return:
    """

    business_type = business_dict.get('type')
    business_function = business_dict.get('function')
    logic_function = logic_dict.get(business_function)

    if business_type == 'logic_control' and logic_function:
        return logic_function


def __for_func(action_list: list, data_list: list = None, num: int = 0, t: int = 0, first: bool = True) -> None:
    """

    :param action_list: 任务列表
    :param data_list: 数据列表
    :param num: 轮次(data_list为空时使用,否则按照数据列表长度作为循序次数)
    :param t: 子循环的轮次
    :param first: 是否首次循环
    :return:
    """

    for i in range(1, num + 1):
        if first:
            print(f'=== 第 {i} 轮开始 ===')

        for index, ac in enumerate(action_list, 1):
            ac_function = ac.get('function')
            if ac_function == 'for':
                ac_num = ac.get('num')
                ac_action = ac.get('action')
                __for_func(action_list=ac_action, num=ac_num, t=i, first=False)
            else:

                """
                selenium 逻辑操作...
                """
                if first:
                    print(f">>>{i}", ac, first)
                else:
                    print(f">>>{t}", ac, first)

        if first:
            print(f'=== 第 {i} 轮结束 ===\n')


def test_001(test_data: list):
    """测试"""

    for m in test_data:
        business_title = m.get('title')
        business_list = m.get('business_list')
        print(business_title)
        print(business_list)
        if business_list:
            test_001(business_list)
        else:
            """
            for function 特殊处理
            """
            function = m.get('function')
            m_action = m.get('action')
            if function == 'for':
                m_num = m.get('num')
                __for_func(action_list=m_action, num=m_num, t=1)
            else:
                """
                普通 function 执行
                """
                print(">>>", m)
                logic_function = get_logic(business_dict=m)
                print(">>>", logic_function, m_action, '\n')


if __name__ == '__main__':
    # print(json.dumps(meta_data, ensure_ascii=False))
    l1 = meta_data[2].get('business_list')[0]
    print(l1)
    test_001(test_data=meta_data)
