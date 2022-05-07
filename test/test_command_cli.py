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
from app.models.push_reminder.models import DingDingConfModel, MailConfModel
from app.models.admin.models import Admin
from common.libs.query_related import general_query
from app.models.test_project.models import TestProject, TestProjectVersion, TestVersionTask, TestModuleApp, \
    MidProjectVersionAndCase, MidProjectVersionAndScenario, MidProjectAndCase, MidVersionAndCase, MidTaskAndCase, \
    MidModuleAndCase, MidProjectAndScenario, MidVersionAndScenario, MidTaskAndScenario, MidModuleAndScenario


class GenNewCaseData:
    """1"""

    @staticmethod
    @set_app_context
    def gen_new_project():
        """MidProjectVersionAndCase -> MidProjectAndCase"""
        hash_map = {}
        query_list = MidProjectVersionAndCase.query.all()
        for index, i in enumerate(query_list, 1):
            case_id = i.case_id
            project_id = i.project_id
            if hash_map.get(case_id):
                pass
            else:
                if project_id:
                    hash_map[case_id] = project_id

        for k, v in hash_map.items():
            new_mid = MidProjectAndCase(project_id=int(v), case_id=int(k), remark='刷数据')
            db.session.add(new_mid)
        db.session.commit()

    @staticmethod
    @set_app_context
    def gen_new_version():
        """MidProjectVersionAndCase -> MidVersionAndCase"""
        hash_map = {}
        query_list = MidProjectVersionAndCase.query.all()
        for index, i in enumerate(query_list, 1):
            case_id = i.case_id
            version_id = i.version_id

            if hash_map.get(version_id):
                if case_id in hash_map.get(version_id):
                    pass
                else:
                    hash_map.get(version_id).append(case_id)
            else:
                if version_id:
                    hash_map[version_id] = [case_id]

        print(hash_map)
        for version_id, case_id_list in hash_map.items():
            print(version_id, case_id_list)

            list(map(lambda case_id: db.session.add(
                MidVersionAndCase(version_id=int(version_id), case_id=int(case_id), remark='刷数据')), case_id_list))
        db.session.commit()

    @staticmethod
    @set_app_context
    def gen_new_task():
        """MidProjectVersionAndCase -> MidTaskAndCase"""
        hash_map = {}
        query_list = MidProjectVersionAndCase.query.all()
        for index, i in enumerate(query_list, 1):
            case_id = i.case_id
            task_id = i.task_id

            if hash_map.get(task_id):
                if case_id in hash_map.get(task_id):
                    pass
                else:
                    hash_map.get(task_id).append(case_id)
            else:
                if task_id:
                    hash_map[task_id] = [case_id]

        print(hash_map)
        for task_id, case_id_list in hash_map.items():
            print(task_id, case_id_list)
            list(map(lambda case_id: db.session.add(
                MidTaskAndCase(task_id=int(task_id), case_id=int(case_id), remark='刷数据')), case_id_list))
        db.session.commit()

    @staticmethod
    @set_app_context
    def gen_new_module():
        """MidProjectVersionAndCase -> MidModuleAndCase"""
        hash_map = {}
        query_list1 = TestModuleApp.query.all()
        query_list2 = MidProjectVersionAndCase.query.all()
        for index, i in enumerate(query_list1, 1):
            module_id = i.id
            case_list = i.case_list
            if case_list:
                if hash_map.get(module_id):
                    pass
                else:
                    hash_map[module_id] = case_list

        print(hash_map)

        for index, i in enumerate(query_list2, 1):
            module_id = i.module_id
            case_id = i.case_id
            if module_id:
                if hash_map.get(module_id):
                    if case_id not in hash_map.get(module_id):
                        hash_map.get(module_id).append(case_id)
                else:
                    if module_id:
                        hash_map[module_id] = [case_id]

        print(hash_map)

        for module_id, case_id_list in hash_map.items():
            print(module_id, case_id_list)
            list(map(lambda case_id: db.session.add(
                MidModuleAndCase(module_id=int(module_id), case_id=int(case_id), remark='刷数据')), case_id_list))
        db.session.commit()


class GenNewScenarioData:
    """2"""

    @staticmethod
    @set_app_context
    def gen_new_project():
        """MidProjectVersionAndScenario -> MidProjectAndScenario"""
        hash_map = {}
        query_list = MidProjectVersionAndScenario.query.all()
        for index, i in enumerate(query_list, 1):
            scenario_id = i.scenario_id
            project_id = i.project_id
            if hash_map.get(scenario_id):
                pass
            else:
                if project_id:
                    hash_map[scenario_id] = project_id

        for k, v in hash_map.items():
            new_mid = MidProjectAndScenario(project_id=int(v), scenario_id=int(k), remark='刷数据')
            db.session.add(new_mid)
        db.session.commit()

    @staticmethod
    @set_app_context
    def gen_new_version():
        """MidProjectVersionAndScenario -> MidVersionAndScenario"""
        hash_map = {}
        query_list = MidProjectVersionAndScenario.query.all()
        for index, i in enumerate(query_list, 1):
            scenario_id = i.scenario_id
            version_id = i.version_id

            if hash_map.get(version_id):
                if scenario_id in hash_map.get(version_id):
                    pass
                else:
                    hash_map.get(version_id).append(scenario_id)
            else:
                if version_id:
                    hash_map[version_id] = [scenario_id]

        print(hash_map)
        for version_id, scenario_id_list in hash_map.items():
            print(version_id, scenario_id_list)

            list(map(lambda scenario_id: db.session.add(
                MidVersionAndScenario(version_id=int(version_id), scenario_id=int(scenario_id), remark='刷数据')),
                     scenario_id_list))
        db.session.commit()

    @staticmethod
    @set_app_context
    def gen_new_task():
        """MidProjectVersionAndScenario -> MidTaskAndScenario"""
        hash_map = {}
        query_list = MidProjectVersionAndScenario.query.all()
        for index, i in enumerate(query_list, 1):
            scenario_id = i.scenario_id
            task_id = i.task_id

            if hash_map.get(task_id):
                if scenario_id in hash_map.get(task_id):
                    pass
                else:
                    hash_map.get(task_id).append(scenario_id)
            else:
                if task_id:
                    hash_map[task_id] = [scenario_id]

        print(hash_map)
        for task_id, scenario_id_list in hash_map.items():
            print(task_id, scenario_id_list)
            list(map(lambda scenario_id: db.session.add(
                MidTaskAndScenario(task_id=int(task_id), scenario_id=int(scenario_id), remark='刷数据')),
                     scenario_id_list))
        db.session.commit()

    @staticmethod
    @set_app_context
    def gen_new_module():
        """MidProjectVersionAndScenario -> MidModuleAndScenario"""
        hash_map = {}
        query_list1 = TestModuleApp.query.all()
        query_list2 = MidProjectVersionAndScenario.query.all()
        for index, i in enumerate(query_list1, 1):
            module_id = i.id
            scenario_list = i.scenario_list
            if scenario_list:
                if hash_map.get(module_id):
                    pass
                else:
                    hash_map[module_id] = scenario_list

        print(hash_map)

        for index, i in enumerate(query_list2, 1):
            module_id = i.module_id
            scenario_id = i.scenario_id
            if module_id:
                if hash_map.get(module_id):
                    if scenario_id not in hash_map.get(module_id):
                        hash_map.get(module_id).append(scenario_id)
                else:
                    if module_id:
                        hash_map[module_id] = [scenario_id]

        print(hash_map)

        for module_id, scenario_id_list in hash_map.items():
            print(module_id, scenario_id_list)
            list(map(lambda scenario_id: db.session.add(
                MidModuleAndScenario(module_id=int(module_id), scenario_id=int(scenario_id), remark='刷数据')),
                     scenario_id_list))
        db.session.commit()


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
