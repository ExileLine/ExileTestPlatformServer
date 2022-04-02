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
from app.models.test_case_config.models import TestDatabases
from app.models.test_project.models import TestProject, TestProjectVersion, MidProjectVersionAndCase, \
    MidProjectVersionAndScenario, TestModuleApp
from app.models.push_reminder.models import DingDingConfModel, MailConfModel
from app.models.admin.models import Admin
from common.libs.query_related import general_query
from app.models.test_project.models import TestProject, TestProjectVersion, TestVersionTask, TestModuleApp, \
    MidProjectVersionAndCase, MidProjectVersionAndScenario, MidRelationCase, MidRelationScenario


def __case():
    old_mid = MidProjectVersionAndCase.query.all()
    for index, o in enumerate(old_mid, 1):
        __id = o.id
        case_id = o.case_id
        project_id = o.project_id
        module_id = o.module_id
        version_id = o.version_id
        task_id = o.task_id
        print(f"index:{index}")

        remark = f"源数据id:{__id}"

        q1 = MidRelationCase.query.filter_by(case_id=case_id, project_id=project_id).first()
        if not q1:
            if project_id:
                print('=== q1 ===')
                n1 = MidRelationCase(case_id=case_id, project_id=project_id, remark=remark)
                db.session.add(n1)

        q2 = MidRelationCase.query.filter_by(case_id=case_id, module_id=module_id).first()
        if not q2:
            if module_id:
                print('=== q2 ===')
                n2 = MidRelationCase(case_id=case_id, module_id=module_id, remark=remark)
                db.session.add(n2)

        q3 = MidRelationCase.query.filter_by(case_id=case_id, version_id=version_id).first()
        if not q3:
            if version_id:
                print('=== q3 ===')
                n3 = MidRelationCase(case_id=case_id, version_id=version_id, remark=remark)
                db.session.add(n3)

        q4 = MidRelationCase.query.filter_by(case_id=case_id, task_id=task_id).first()
        if not q4:
            if task_id:
                print('=== q4 ===')
                n4 = MidRelationCase(case_id=case_id, task_id=task_id, remark=remark)
                db.session.add(n4)

    db.session.commit()


def __scenario():
    old_mid = MidProjectVersionAndScenario.query.all()
    for index, o in enumerate(old_mid, 1):
        __id = o.id
        scenario_id = o.scenario_id
        project_id = o.project_id
        module_id = o.module_id
        version_id = o.version_id
        task_id = o.task_id
        print(f"index:{index}")

        remark = f"源数据id:{__id}"

        q1 = MidRelationScenario.query.filter_by(scenario_id=scenario_id, project_id=project_id).first()
        if not q1:
            if project_id:
                print('=== q1 ===')
                n1 = MidRelationScenario(scenario_id=scenario_id, project_id=project_id, remark=remark)
                db.session.add(n1)

        q2 = MidRelationScenario.query.filter_by(scenario_id=scenario_id, module_id=module_id).first()
        if not q2:
            if module_id:
                print('=== q2 ===')
                n2 = MidRelationScenario(scenario_id=scenario_id, module_id=module_id, remark=remark)
                db.session.add(n2)

        q3 = MidRelationScenario.query.filter_by(scenario_id=scenario_id, version_id=version_id).first()
        if not q3:
            if version_id:
                print('=== q3 ===')
                n3 = MidRelationScenario(scenario_id=scenario_id, version_id=version_id, remark=remark)
                db.session.add(n3)

        q4 = MidRelationScenario.query.filter_by(scenario_id=scenario_id, task_id=task_id).first()
        if not q4:
            if task_id:
                print('=== q4 ===')
                n4 = MidRelationScenario(scenario_id=scenario_id, task_id=task_id, remark=remark)
                db.session.add(n4)

    db.session.commit()


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
