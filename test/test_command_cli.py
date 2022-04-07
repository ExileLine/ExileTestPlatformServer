# -*- coding: utf-8 -*-
# @Time    : 2022/2/20 3:59 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_command_cli.py
# @Software: PyCharm
import json

from common.libs.set_app_context import set_app_context
from app.models.test_case.models import TestCase, db
from app.models.test_case_assert.models import TestCaseAssResponse, TestCaseAssField
from app.models.test_case_db.models import TestDatabases
from app.models.test_project.models import TestProject, TestProjectVersion, MidProjectVersionAndCase, \
    MidProjectVersionAndScenario, TestModuleApp
from app.models.push_reminder.models import DingDingConfModel, MailConfModel
from app.models.admin.models import Admin
from common.libs.query_related import general_query
from app.models.test_project.models import TestProject, TestProjectVersion, TestVersionTask, TestModuleApp, \
    MidProjectVersionAndCase, MidProjectVersionAndScenario


@set_app_context
def main():
    """1"""
    # __case()
    # __scenario()
    # q = MidRelationCase.query.filter(
    #     MidRelationCase.is_deleted == 0,
    #     MidRelationCase.case_id == 175,
    #     MidRelationCase.task_id != 0
    # ).all()


if __name__ == '__main__':
    pass
    import requests

    resp = requests.get(url='http://0.0.0.0:7272/api/index/1')
    # print(resp.json())

    # def gen_num():
    #     for i in range(10):
    #         print(f'生成数据：{i}')
    #         yield i
    #
    #
    # nums = gen_num()
    # print([num for num in nums])
    # print(f'打印数据：{num}')
