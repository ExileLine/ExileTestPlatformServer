# -*- coding: utf-8 -*-
# @Time    : 2022/4/11 2:04 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : project_init.py
# @Software: PyCharm

import random
import shortuuid

from common.libs.set_app_context import set_app_context
from ExtendRegister.db_register import db
from app.models.platform_conf.models import PlatformConfModel
from app.models.admin.models import Admin
from app.models.test_project.models import TestProject, TestProjectVersion, TestModuleApp, MidProjectAndCase, \
    MidVersionCase, MidModuleCase
from app.models.test_case.models import TestCase, TestCaseData
from app.models.test_case_assert.models import TestCaseAssResponse, TestCaseAssField, TestCaseDataAssBind
from app.models.test_variable.models import TestVariable
from app.models.test_case_db.models import TestDatabases


class ProjectDataInit:
    """项目初始化"""

    project_id = None

    @set_app_context
    def create_platform_conf(self):
        """创建平台基础配置"""
        pc = PlatformConfModel(
            platform_name="放逐测试平台-demo",
            platform_login_msg="Sign in to Exile Test Platform",
            weights=9999,
            remark="脚本生成",
            creator="shell",
            creator_id=999999
        )
        db.session.add(pc)
        db.session.commit()
        print('创建平台基础配置完成')

    @set_app_context
    def create_admin(self):
        """创建admin"""

        admin = Admin(
            username='admin',
            password='123456',
            phone=None,
            mail=None,
            creator='shell',
            creator_id='0',
            remark='manage shell')
        admin.set_code()
        db.session.add(admin)
        db.session.commit()
        print('创建 admin 完成')

    @set_app_context
    def create_project_version(self):
        """创建项目以及版本"""
        new_project = TestProject(
            project_name='初始化项目',
            remark="脚本生成",
            creator="shell",
            creator_id=999999
        )
        db.session.add(new_project)
        db.session.commit()
        project_id = new_project.id

        for index, i in enumerate(range(0, 5), 1):
            new_version = TestProjectVersion(
                version_name=f"版本迭代:{index}",
                version_number=f"v1.{index}",
                project_id=project_id,
                remark="脚本生成",
                creator="shell",
                creator_id=999999
            )
            db.session.add(new_version)
        db.session.commit()
        print('创建项目以及版本完成')

    @set_app_context
    def create_module(self):
        """创建模块"""

        if self.project_id:
            project_id = self.project_id
        else:
            query_project = TestProject.query.get(1)
            project_id = query_project.id

        for index, i in enumerate(range(0, 5), 1):
            new_module = TestModuleApp(
                project_id=project_id,
                module_name=f'模块:{index}',
                module_code=shortuuid.uuid(),
                remark="脚本生成",
                creator="shell",
                creator_id=999999
            )
            db.session.add(new_module)
        db.session.commit()
        print('创建模块完成')

    @set_app_context
    def create_case(self, num=None):
        """创建用例并关联"""
        request_method = ["GET", "POST", "PUT", "DELETE"]
        num = num if num else 100
        for index in range(1, num):
            new_test_case = TestCase(
                case_name=f"测试{index}",
                request_method=random.choice(request_method),
                request_base_url="http://0.0.0.0:7272",
                request_url='/test',
                is_shared=True,
                is_public=True,
                remark="脚本生成:{}".format(index),
                creator="脚本生成:{}".format(index),
                creator_id=999999,
                total_execution=random.randint(1, 99)
            )
            db.session.add(new_test_case)
        db.session.commit()

        if self.project_id:
            project_id = self.project_id
        else:
            query_project = TestProject.query.get(1)
            project_id = query_project.id

        case_list = TestCase.query.filter_by(creator_id=999999).all()
        version_list = TestProjectVersion.query.filter_by(creator_id=999999).all()
        module_list = TestModuleApp.query.filter_by(creator_id=999999).all()

        for case in case_list:
            # 用例关联项目
            case_id = case.id
            pc = MidProjectAndCase(
                project_id=project_id,
                case_id=case_id,
                remark=f"脚本生成:{project_id}-{case_id}",
                creator=f"脚本生成:{project_id}-{case_id}",
                creator_id=999999
            )
            db.session.add(pc)

            # 用例关联版本
            version_id = random.choice(version_list).id
            vc = MidVersionCase(
                version_id=version_id,
                case_id=case_id,
                remark=f"脚本生成:{version_id}-{case_id}",
                creator=f"脚本生成:{version_id}-{case_id}",
                creator_id=999999
            )
            db.session.add(vc)

            # 用例关联模块
            module_id = random.choice(module_list).id
            mc = MidModuleCase(
                module_id=module_id,
                case_id=case_id,
                remark=f"脚本生成:{module_id}-{case_id}",
                creator=f"脚本生成:{module_id}-{case_id}",
                creator_id=999999
            )
            db.session.add(mc)

        db.session.commit()
        print('用例关联项目，用例关联版本，用例关联模块 完成')

    @set_app_context
    def create_case_data(self, num=None):
        """创建参数"""

        num = num if num else 100
        for index in range(1, num):
            tcd = TestCaseData(
                data_name=f"测试数据:{index}",
                request_headers={
                    "token": "${token}"
                },
                request_params={},
                request_body={
                    "user_id": "${user_id}",
                    "password": index * random.randint(111111, 333333)
                },
                request_body_type=1,
                update_var_list=[],
                remark="脚本生成",
                creator="shell",
                creator_id=999999
            )
            db.session.add(tcd)
        db.session.commit()
        print('创建参数完成')

    @set_app_context
    def create_ass_response(self, num=None):
        """创建响应断言"""
        x = [
            {
                "rule": "==",
                "assert_key": "code",
                "expect_val": 401,
                "is_expression": 0,
                "python_val_exp": "obj.get('code')",
                "expect_val_type": 1,
                "response_source": "response_body"
            },
            {
                "rule": "==",
                "assert_key": "code",
                "expect_val": 200,
                "is_expression": 0,
                "python_val_exp": "obj.get('code')",
                "expect_val_type": 1,
                "response_source": "response_body"
            },
            {
                "rule": "==",
                "assert_key": "message",
                "expect_val": '操作成功',
                "is_expression": 0,
                "python_val_exp": "obj.get('message')",
                "expect_val_type": 1,
                "response_source": "response_body"
            }
        ]
        num = num if num else 100
        for index in range(1, num):
            new_ass_resp = TestCaseAssResponse(
                assert_description=f"响应断言:{index}",
                ass_json=[random.choice(x)],
                remark="脚本生成",
                creator="shell",
                creator_id=999999
            )
            db.session.add(new_ass_resp)
        db.session.commit()
        print('创建响应断言完成')

    @set_app_context
    def create_ass_field(self, num=None):
        """创建字段断言"""
        x1 = [
            {
                "db_id": 12,
                "assert_list": [
                    {
                        "query": "select id FROM exile_test_case WHERE id=1;",
                        "assert_field_list": [
                            {
                                "rule": "==",
                                "assert_key": "id",
                                "expect_val": 1,
                                "expect_val_type": "1"
                            },
                            {
                                "rule": "==",
                                "assert_key": "case_name",
                                "expect_val": "测试用例B1",
                                "expect_val_type": "2"
                            }
                        ]
                    }
                ]
            },

        ]
        x2 = [
            {
                "db_id": 9,
                "query": "get 127.0.0.1",
                "assert_list": [
                    {
                        "rule": "==",
                        "assert_key": "username",
                        "expect_val": "user_00007",
                        "is_expression": 1,
                        "python_val_exp": "obj.get('username')",
                        "expect_val_type": "2"
                    }
                ]
            }
        ]
        num = num if num else 100
        for index in range(1, num):
            new_ass_field = TestCaseAssField(
                assert_description=f"响应断言:{index}",
                ass_json=[random.choice([x1, x2])],
                remark="脚本生成",
                creator="shell",
                creator_id=999999
            )
            db.session.add(new_ass_field)
        db.session.commit()
        print('创建字段断言完成')

    @set_app_context
    def create_case_bind(self):
        """创建用例绑定关系"""
        case_list = TestCase.query.filter_by(creator_id=999999).all()
        data_list = TestCaseData.query.filter_by(creator_id=999999).all()
        ass_response_list = TestCaseAssResponse.query.filter_by(creator_id=999999).all()
        ass_field_list = TestCaseAssField.query.filter_by(creator_id=999999).all()

        for case in case_list:
            case_id = case.id
            data_id = random.choice(data_list).id
            new_bind = TestCaseDataAssBind(
                case_id=case_id,
                data_id=data_id,
                ass_resp_id_list=[random.choice(ass_response_list).id],
                ass_field_id_list=[random.choice(ass_field_list).id],
                remark="脚本生成",
                creator="shell",
                creator_id=999999
            )
            db.session.add(new_bind)
        db.session.commit()
        print('创建用例绑定关系完成')

    @set_app_context
    def create_var(self):
        """创建变量"""

        for index in range(1, 100):
            tv = TestVariable(
                var_name=f"变量:{index}",
                var_value=f"变量的值:{index}",
                var_type=random.choice(list(range(1, 13))),
                var_source=random.choice(["resp_data", "resp_headers"]),
                var_get_key="code",
                expression="obj.get('message')",
                is_expression=1,
                remark="脚本生成",
                creator="shell",
                creator_id=999999
            )
            db.session.add(tv)
        db.session.commit()
        print('创建变量完成')

    @set_app_context
    def create_db(self):
        """创建db"""

        mysql_db = TestDatabases(
            name='测试环境:mysql',
            db_type='mysql',
            db_connection={"host": "127.0.0.1", "password": "1234567890", "port": 33060, "user": "root"},
            remark="脚本生成",
            creator="shell",
            creator_id=999999,
        )
        redis_db = TestDatabases(
            name='测试环境:redis',
            db_type='redis',
            db_connection={"db": 0, "host": "127.0.0.1", "password": "1234567890", "port": 63790},
            remark="脚本生成",
            creator="shell",
            creator_id=999999,
        )
        es_db = TestDatabases(
            name='测试环境:ES',
            db_type='redis',
            db_connection={},
            remark="脚本生成",
            creator="shell",
            creator_id=999999,
        )
        db.session.add_all([mysql_db, redis_db, es_db])
        db.session.commit()
        print('创建db完成')


if __name__ == '__main__':
    project_data_init = ProjectDataInit()
    project_data_init.create_platform_conf()
    project_data_init.create_admin()
    project_data_init.create_project_version()
    project_data_init.create_module()
    project_data_init.create_case(num=10000)
    project_data_init.create_case_data(num=10000)
    project_data_init.create_ass_response(num=10000)
    project_data_init.create_ass_field(num=10000)
    project_data_init.create_case_bind()
    project_data_init.create_var()
    project_data_init.create_db()
