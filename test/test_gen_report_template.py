# -*- coding: utf-8 -*-
# @Time    : 2022/3/31 4:16 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_gen_report_template.py
# @Software: PyCharm

import os
import sys
import time
import json

from common.libs.db import R
from common.libs.report_template import RepostTemplate


def test_gen_repost():
    """测试生成测试报告"""
    # data = json.loads(R.get('task_all_first_log:30'))
    data = R.get('task_all_first_log:30')
    print(data)
    test_repost = RepostTemplate(data=data).generate_html_report()
    report_name = f"Test_Report_{time.strftime('%Y-%m-%d_%H_%M_%S')}_yyx.html"
    path = f"{os.getcwd().split('ExileTestPlatformServer')[0]}ExileTestPlatformServer/app/static/report/{report_name}"
    with open(path, "w+", encoding="utf-8") as f:
        f.write(test_repost)


if __name__ == '__main__':
    test_gen_repost()

    data1 = R.get('task_all_first_log:30')
    data1_sizeof = sys.getsizeof(data1)
    print(data1_sizeof, f"={int(data1_sizeof / 1024)}KB")
    data2 = str(json.loads(R.get('task_all_first_log:30')))
    data2_sizeof = sys.getsizeof(data2)
    print(data2_sizeof, f"={int(data2_sizeof / 1024)}KB")
