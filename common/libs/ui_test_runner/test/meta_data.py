# -*- coding: utf-8 -*-
# @Time    : 2023/1/30 12:00
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : meta_data.py
# @Software: PyCharm

import json
import shortuuid


class TestMetaData:
    """测试"""

    home = {
        "uuid": shortuuid.uuid(),
        "index": 1,
        "type": "ui_control",
        "title": "点击前往首页",
        "function": "click",
        "args": {
            "mode": "XPATH",
            "value": """//*[@id="app"]/div/div[1]/div[1]/div[1]/span"""
        }
    }

    acc = {
        "uuid": shortuuid.uuid(),
        "index": 1,
        "type": "ui_control",
        "title": "输入账号",
        "function": "input",
        "args": {
            "mode": "XPATH",
            "value": """//*[@id="login-form"]/div[1]/div[2]/div/div/div/input""",
            "data": "admin",
        }
    }
    pwd = {
        "uuid": shortuuid.uuid(),
        "index": 2,
        "type": "ui_control",
        "title": "输入密码",
        "function": "input",
        "args": {
            "mode": "XPATH",
            "value": """//*[@id="login-form"]/div[2]/div[2]/div/div/div/input""",
            "data": "123456"
        }
    }
    login = {
        "uuid": shortuuid.uuid(),
        "index": 3,
        "type": "ui_control",
        "title": "点击登录",
        "function": "click",
        "args": {
            "mode": "XPATH",
            "value": """//*[@id="login-form"]/div[3]/div[2]/div/div/div/button[1]"""
        }
    }

    project_name = {
        "uuid": shortuuid.uuid(),
        "index": 11,
        "type": "ui_control",
        "title": "输入项目名称",
        "function": "input",
        "args": {
            "mode": "XPATH",
            "value": """//*[@id="project-search-container"]/div/form/div/div/div/input""",
            "data": "zxc"
        }
    }
    project_select = {
        "uuid": shortuuid.uuid(),
        "index": 22,
        "type": "ui_control",
        "title": "点击搜索",
        "function": "click",
        "args": {
            "mode": "XPATH",
            "value": """//*[@id="project-search-container"]/div/form/div/span"""
        }
    }
    project_click = {
        "uuid": shortuuid.uuid(),
        "index": 33,
        "type": "ui_control",
        "title": "点击项目3",
        "function": "click",
        "args": {
            "mode": "XPATH",
            "value": """//*[@id="main-container"]/div[1]/div[1]/div/div"""
        }
    }

    logout1 = {
        "uuid": shortuuid.uuid(),
        "index": 4,
        "type": "ui_control",
        "title": "点击下拉",
        "function": "click",
        "args": {
            "mode": "XPATH",
            "value": """//*[@id="app"]/div/div[1]/button[4]/span/div"""
        }
    }
    logout2 = {
        "uuid": shortuuid.uuid(),
        "index": 5,
        "type": "ui_control",
        "title": "点击退出",
        "function": "click",
        "args": {
            "mode": "XPATH",
            "value": """/html/body/div[2]/div/div/div/div[3]/li/span/div"""
        }
    }

    assert_task = {
        "uuid": shortuuid.uuid(),
        "index": 4,
        "title": "检验是否登录成功",
        "type": "master",
        "business_list": [
            {
                "uuid": shortuuid.uuid(),
                "index": 1,
                "type": "assert_control",
                "title": "UI断言控件",
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
    }

    light = {
        "uuid": shortuuid.uuid(),
        "index": 3331,
        "type": "ui_control",
        "title": "点击光明2",
        "function": "click",
        "args": {
            "mode": "XPATH",
            "value": """//*[@id="app"]/div/div[1]/div[2]/div[2]"""
        }
    }
    dark = {
        "uuid": shortuuid.uuid(),
        "index": 3332,
        "type": "ui_control",
        "title": "点击暗夜2",
        "function": "click",
        "args": {
            "mode": "XPATH",
            "value": """//*[@id="app"]/div/div[1]/div[2]/div[3]"""
        }
    }

    child_master = {
        "uuid": shortuuid.uuid(),
        "index": 5,
        "title": "循环四(业务块)",
        "type": "master",
        "business_list": [
            {
                "uuid": shortuuid.uuid(),
                "index": 1,
                "type": "ui_control",
                "title": "循环四-点击控件1",
                "function": "click",
                "args": {}
            },
            {
                "uuid": shortuuid.uuid(),
                "index": 2,
                "type": "logic_control",
                "title": "循环控件",
                "function": "for",
                "num": 2,
                "data_source": [],
                "business_list": [
                    {
                        "uuid": shortuuid.uuid(),
                        "index": 771,
                        "type": "ui_control",
                        "title": "循环四-内循环-点击控件2",
                        "function": "click",
                        "args": {}
                    }
                ]
            }
        ]
    }


start = {
    "uuid": shortuuid.uuid(),
    "index": 1,
    "title": "开始",
    "type": "master",
    "business_list": [
        {
            "uuid": shortuuid.uuid(),
            "index": 1,
            "type": "ui_control",
            "title": "启动浏览器控件",
            "function": "open",
            "args": {
                # "url": "https://www.baidu.com"
                "url": "http://localhost:3200/login"
            }
        },
    ]
}

test_001 = {
    "uuid": shortuuid.uuid(),
    "index": 2,
    "title": "登录",
    "type": "master",
    "business_list": [
        TestMetaData.acc,
        TestMetaData.pwd,
        TestMetaData.login,

        TestMetaData.project_name,
        TestMetaData.project_select,
        TestMetaData.project_click,

        TestMetaData.dark,
        TestMetaData.light,

        TestMetaData.logout1,
        TestMetaData.logout2,
        # TestMetaData.assert_task
    ]
}

test_for_001 = {
    "uuid": shortuuid.uuid(),
    "index": 3,
    "title": "嵌套循环操作",
    "type": "master",
    "business_list": [
        {
            "uuid": shortuuid.uuid(),
            "index": 1,
            "type": "logic_control",
            "title": "第一层循环",
            "function": "for",
            "num": 3,  # 调试
            "data_source": [],
            "business_list": [
                TestMetaData.acc,
                TestMetaData.pwd,
                TestMetaData.login,

                {
                    "uuid": shortuuid.uuid(),
                    "index": 4,
                    "type": "logic_control",
                    "title": "第二层循环",
                    "function": "for",
                    "num": 3,
                    "data_source": [],
                    "business_list": [
                        TestMetaData.project_name,
                        TestMetaData.project_select,
                        TestMetaData.project_click,
                        TestMetaData.dark,
                        TestMetaData.light,
                        TestMetaData.home,

                        # {
                        #     "uuid": shortuuid.uuid(),
                        #     "index": 44,
                        #     "type": "logic",
                        #     "title": "循环三(逻辑块)",
                        #     "function": "for",
                        #     "num": 2,
                        #     "data_source": [],
                        #     "business_list": [
                        #         TestMetaData.dark,
                        #         TestMetaData.light,
                        #     ]
                        # }
                    ]
                },

                TestMetaData.logout1,
                TestMetaData.logout2,

            ]
        },
    ]
}

test_002 = {
    "uuid": shortuuid.uuid(),
    "index": 3,
    "title": "循环录入数据",
    "type": "master",
    "business_list": [
        {
            "uuid": shortuuid.uuid(),
            "index": 1,
            "type": "logic_control",
            "title": "循环控件",
            "function": "for",
            "num": 2,  # 调试
            "data_source": [],
            "business_list": [
                {
                    "uuid": shortuuid.uuid(),
                    "index": 1,
                    "type": "ui_control",
                    "title": "输入控件A",
                    "function": "input",
                    "args": {
                        "username": "admin"
                    }
                },
                {
                    "uuid": shortuuid.uuid(),
                    "index": 2,
                    "type": "ui_control",
                    "title": "输入控件B",
                    "function": "input",
                    "args": {
                        "password": "123456"
                    }
                },
                {
                    "uuid": shortuuid.uuid(),
                    "index": 3,
                    "type": "ui_control",
                    "title": "点击控件C",
                    "function": "click",
                    "args": {}
                },
                {
                    "uuid": shortuuid.uuid(),
                    "index": 4,
                    "type": "logic",
                    "title": "循环二(逻辑块)",
                    "function": "for",
                    "num": 3,
                    "data_source": [],
                    "business_list": [
                        {
                            "uuid": shortuuid.uuid(),
                            "index": 11,
                            "type": "ui_control",
                            "title": "点击控件X-3",
                            "function": "click",
                            "args": {}
                        },
                        {
                            "uuid": shortuuid.uuid(),
                            "index": 22,
                            "type": "ui_control",
                            "title": "点击控件Y-3",
                            "function": "click",
                            "args": {}
                        },
                        {
                            "uuid": shortuuid.uuid(),
                            "index": 33,
                            "type": "ui_control",
                            "title": "点击控件Z-3",
                            "function": "click",
                            "args": {}
                        },
                        {
                            "uuid": shortuuid.uuid(),
                            "index": 44,
                            "type": "logic",
                            "title": "循环三(逻辑块)",
                            "function": "for",
                            "num": 2,
                            "data_source": [],
                            "business_list": [
                                {
                                    "uuid": shortuuid.uuid(),
                                    "index": 3331,
                                    "type": "ui_control",
                                    "title": "===点击控件OKC===2",
                                    "function": "click",
                                    "args": {}
                                },
                                {
                                    "uuid": shortuuid.uuid(),
                                    "index": 3332,
                                    "type": "ui_control",
                                    "title": "===点击控件LOL===2",
                                    "function": "click",
                                    "args": {}
                                },
                            ]
                        }
                    ]
                },
                TestMetaData.child_master
            ]
        },
        {
            "uuid": shortuuid.uuid(),
            "index": 2,
            "title": "操作2",
            "type": "master",
            "business_list": [
                {
                    "uuid": shortuuid.uuid(),
                    "index": 1,
                    "type": "ui_control",
                    "title": "点击控件",
                    "function": "click",
                    "args": {}
                },
            ]
        }
    ]
}

end = {
    "uuid": shortuuid.uuid(),
    "index": 1,
    "title": "结束",
    "type": "master",
    "business_list": [
        {
            "uuid": shortuuid.uuid(),
            "index": 1,
            "type": "ui_control",
            "title": "关闭浏览器",
            "function": "close",
            "args": {}
        },
    ]
}

meta_data = [
    start,
    test_001,
    test_for_001,
    # test_002,
    end
]

if __name__ == '__main__':
    print(json.dumps(meta_data, ensure_ascii=False))