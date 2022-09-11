# -*- coding: utf-8 -*-
# @Time    : 2022/7/28 14:40
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test_case_loader.py
# @Software: PyCharm

import asyncio

from common.libs.async_test_runner import AsyncCaseRunner, case_list, scenario_list

test_obj = {
    "execute_id": 8646,
    "execute_name": "执行用例8646:[登录成功okc2]",
    "execute_type": "case",
    "execute_label": "only",
    "execute_user_id": 1,
    "execute_username": "admin",
    "base_url": "",
    "use_base_url": False,
    "data_driven": True,
    "is_execute_all": False,
    "case_list": case_list,
    "scenario_list": scenario_list,
    "execute_dict": {},
    "is_dd_push": False,
    "dd_push_id": None,
    "ding_talk_url": "",
    "is_send_mail": False,
    "mail_list": [],
    "trigger_type": "user_execute",
    "request_timeout": 3,
    "is_safe_scan": False,
    "safe_scan_proxies_url": "",
    "call_safe_scan_data": {},
    "safe_scan_report_url": ""
}

if __name__ == '__main__':
    """单元测试"""

    acr = AsyncCaseRunner(test_obj=test_obj, is_debug=True)
    asyncio.run(acr.main())
