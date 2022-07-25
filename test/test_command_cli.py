# -*- coding: utf-8 -*-
# @Time    : 2022/2/20 3:59 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test_command_cli.py
# @Software: PyCharm
import json

from common.libs.set_app_context import set_app_context
from app.models.test_case.models import TestCase, db
from app.models.test_case_assert.models import TestCaseAssResponse, TestCaseAssField
from app.models.test_case_db.models import TestDatabases
from app.models.push_reminder.models import DingDingConfModel, MailConfModel
from app.models.admin.models import Admin
from common.libs.query_related import general_query
from app.models.test_project.models import TestProject, TestProjectVersion, TestVersionTask, TestModuleApp, \
    MidProjectAndCase, MidVersionCase, MidTaskCase, \
    MidModuleCase, MidProjectScenario, MidVersionScenario, MidTaskScenario, MidModuleScenario


@set_app_context
def create_user(user_list):
    """
    [
        {
            "name": "测试用户123",
            "mail": "yangyuexiong@gmail.com"
        },
        ...
    ]
    :param user_list:
    :return:
    """
    for i in user_list:
        nickname = i.get('name')
        mail = i.get('mail')
        username = mail.split("@")[0]
        query_user = Admin.query.filter_by(username=username).first()
        if query_user:
            print(f'用户:{username} 已存在')
        else:
            new_admin = Admin(
                username=username,
                password='123456',
                nickname=nickname,
                phone=None,
                mail=mail,
                creator='shell',
                creator_id='0',
                remark='manage shell')
            new_admin.set_code()
            db.session.add(new_admin)
    db.session.commit()
    print('添加成功')


@set_app_context
def create_user_one(username, nickname, mail):
    """1"""
    query_user = Admin.query.filter_by(username=username).first()
    if query_user:
        print(f'用户:{username} 已存在')
    else:
        new_admin = Admin(
            username=username,
            password='123456',
            nickname=nickname,
            phone=None,
            mail=mail,
            creator='shell',
            creator_id='0',
            remark='manage shell')
        new_admin.set_code()
        new_admin.save()


if __name__ == '__main__':
    pass
    # def gen_num():
    #     for i in range(10):
    #         print(f'生成数据：{i}')
    #         yield i
    #
    #
    # nums = gen_num()
    # print([num for num in nums])
    # print(f'打印数据：{num}')

    """用例"""
    # GenNewCaseData.gen_new_project()
    # GenNewCaseData.gen_new_version()
    # GenNewCaseData.gen_new_task()
    # GenNewCaseData.gen_new_module()
    """场景"""
    # GenNewScenarioData.gen_new_project()
    # GenNewScenarioData.gen_new_version()
    # GenNewScenarioData.gen_new_task()
    # GenNewScenarioData.gen_new_module()
    """批量创建用户"""
    # create_user()
    # create_user_one(username='yangyueixong', nickname='yyx', mail='yang@126.com')
