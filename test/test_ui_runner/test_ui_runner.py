# -*- coding: utf-8 -*-
# @Time    : 2023/2/22 17:46
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test_ui_runner.py
# @Software: PyCharm


from test.test_ui_runner.meta_data import meta_data as md
from test.test_ui_runner.meta_data import meta_data2 as md2
from common.libs.BaseWebDriver import BaseWebDriver
from common.libs.ui_test_runner.ui_case_runner import ExecuteUiCase

test_obj = {
    "project_id": 30,
    "execute_id": 5,
    "execute_user_id": 1,
    "execute_username": "admin",
    "execute_key": "ui_case",
    "execute_name": "测试UI自动化",
    "execute_type": "ui_case",
    "execute_label": "execute_label",
    "execute_logs_id": 999,
    "ui_case_list": [
        {
            "case_name": "测试UI自动化",
            "case_status": "debug",
            "create_time": "2023-02-15 18:03:23",
            "create_timestamp": 1676454640,
            "creator": "admin",
            "creator_id": 1,
            "id": 6,
            "is_deleted": 0,
            "is_public": True,
            "meta_data": md,
            "modifier": None,
            "modifier_id": None,
            "remark": "测试UI自动化123",
            "status": 1,
            "total_execution": 0,
            "update_time": "2023-02-15 18:03:24",
            "update_timestamp": None
        }
    ],
    # "use_dd_push": use_dd_push,
    # "dd_push_id": dd_push_id,
    # "ding_talk_url": ding_talk_url,
    # "use_mail": use_mail,
    # "mail_list": mail_list,
}

if __name__ == '__main__':
    ex_ui_case = ExecuteUiCase(test_obj=test_obj, web_driver=BaseWebDriver, is_debug=True)
    ex_ui_case.main()
