# -*- coding: utf-8 -*-
# @Time    : 2022/4/11 2:04 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : project_init.py
# @Software: PyCharm
import json
import random
import shortuuid

from common.libs.data_dict import GlobalsDict
from common.libs.set_app_context import set_app_context
from common.libs.public_func import gen_request_dict
from ExtendRegister.db_register import db
from app.models.platform_conf.models import PlatformConfModel
from app.models.admin.models import Admin
from app.models.test_project.models import TestProject, TestProjectVersion, TestModuleApp, MidProjectAndCase, \
    MidVersionCase, MidModuleCase
from app.models.test_case.models import TestCase, TestCaseData
from app.models.test_case_assert.models import TestCaseAssertion, TestCaseDataAssBind
from app.models.test_variable.models import TestVariable
from app.models.test_case_db.models import TestDatabases


class ProjectDataInit:
    """项目初始化"""

    project_id = 1

    @set_app_context
    def create_admin(self):
        """创建admin"""

        query_admin = Admin.query.filter_by(username='admin').first()
        if query_admin:
            print('>>> admin 已经存在, 初始密码: 123456')
            return None

        admin = Admin(
            username='admin',
            password='123456',
            nickname='Exile作者',
            phone=15013038819,
            mail="yang6333yyx@126.com",
            creator='shell',
            creator_id=0,
            remark='manage shell'
        )
        admin.set_code()
        admin.save()
        print('>>> 创建 admin 完成')

    @set_app_context
    def create_project_version(self):
        """创建项目以及版本"""

        new_project = TestProject(
            project_name=f'初始化项目:{shortuuid.uuid()}',
            remark="脚本初始化生成",
            creator="shell",
            creator_id=0
        )
        db.session.add(new_project)
        db.session.commit()
        project_id = new_project.id

        for index, i in enumerate(range(0, 5), 1):
            new_version = TestProjectVersion(
                version_name=f"版本迭代:{index}",
                version_number=f"v{index}.0",
                project_id=project_id,
                icon=random.choice([1, 2, 3, 4]),
                remark="脚本初始化生成",
                creator="shell",
                creator_id=0
            )
            db.session.add(new_version)
        db.session.commit()

        self.project_id = project_id
        print('>>> 初始化项目以及版本完成')

    @set_app_context
    def create_module(self):
        """创建模块"""

        for index, i in enumerate(range(0, 5), 1):
            new_module = TestModuleApp(
                project_id=self.project_id,
                module_name=f'模块:{index}',
                module_code=shortuuid.uuid(),
                remark="脚本初始化生成",
                creator="shell",
                creator_id=0
            )
            db.session.add(new_module)
        db.session.commit()
        print('>>> 初始化模块完成')

    @set_app_context
    def create_case(self, num=None):
        """创建用例并关联"""

        request_method = ["GET", "POST", "PUT", "DELETE"]
        case_status_list = ["active", "dev", "debug", "over"]
        num = num if num else 100
        for index in range(1, num):
            new_test_case = TestCase(
                case_name=f"测试{index}",
                request_method=random.choice(request_method),
                request_base_url="http://0.0.0.0:7878",
                request_url='/api/test',
                is_shared=True,
                is_public=True,
                remark="脚本生成:{}".format(index),
                creator="脚本生成:{}".format(index),
                creator_id=0,
                total_execution=random.randint(1, 99),
                case_status=random.choice(case_status_list)
            )
            db.session.add(new_test_case)
        db.session.commit()

        project_id = self.project_id

        case_list = TestCase.query.filter_by(creator_id=0).all()
        version_list = TestProjectVersion.query.filter_by(creator_id=0).all()
        module_list = TestModuleApp.query.filter_by(creator_id=0).all()

        for case in case_list:
            # 用例关联项目
            case_id = case.id
            pc = MidProjectAndCase(
                project_id=project_id,
                case_id=case_id,
                remark=f"脚本生成:{project_id}-{case_id}",
                creator=f"脚本生成:{project_id}-{case_id}",
                creator_id=0
            )
            db.session.add(pc)

            # 用例关联版本
            version_id = random.choice(version_list).id
            vc = MidVersionCase(
                version_id=version_id,
                case_id=case_id,
                remark=f"脚本生成:{version_id}-{case_id}",
                creator=f"脚本生成:{version_id}-{case_id}",
                creator_id=0
            )
            db.session.add(vc)

            # 用例关联模块
            module_id = random.choice(module_list).id
            mc = MidModuleCase(
                module_id=module_id,
                case_id=case_id,
                remark=f"脚本生成:{module_id}-{case_id}",
                creator=f"脚本生成:{module_id}-{case_id}",
                creator_id=0
            )
            db.session.add(mc)

        db.session.commit()
        print('>>> 用例关联项目，用例关联版本，用例关联模块 完成')

    @set_app_context
    def create_case_data(self, num=None):
        """创建参数"""

        num = num if num else 100
        for index in range(1, num):
            request_params_hash = [
                {
                    "active": True,
                    "key": f"k{index}",
                    "value": f"v{index}",
                    "desc": "参数1"
                },
                {
                    "active": True,
                    "key": f"kk{index}",
                    "value": f"vv{index}",
                    "desc": "参数2"
                }
            ]
            request_headers_hash = [
                {
                    "active": True,
                    "key": "token",
                    "value": f"token{index}",
                    "desc": "鉴权"
                },
                {
                    "active": True,
                    "key": "xxx",
                    "value": f"xxx{index}",
                    "desc": "..."
                }
            ]
            request_body_hash = json.dumps({
                "key1": "value1"
            }, ensure_ascii=False)
            request_body_type = "json"
            request_params = gen_request_dict(request_params_hash)
            request_headers = gen_request_dict(request_headers_hash)
            _func = GlobalsDict.request_body_type_func().get(request_body_type)
            request_body = _func(request_body_hash)

            tcd = TestCaseData(
                data_name=f"测试数据:{index}",
                request_params_hash=request_params_hash,
                request_params=request_params,
                request_headers_hash=request_headers_hash,
                request_headers=request_headers,
                request_body_hash=request_body_hash,
                request_body=request_body,
                request_body_type=request_body_type,
                update_var_list=[],
                creator="shell",
                creator_id=0,
            )
            db.session.add(tcd)
        db.session.commit()
        print('>>> 创建参数完成')

    @set_app_context
    def create_ass_response(self, num=None):
        """创建响应断言"""

        x = [
            {
                "response_source": "response_body",
                "assert_key": "data",
                "expect_val": True,
                "expect_val_type": "bool",
                "rule": "==",
                "is_expression": True,
                "python_val_exp": "obj.get('data')"
            },
            {
                "response_source": "response_body",
                "assert_key": "data",
                "expect_val": "yyx",
                "expect_val_type": "str",
                "rule": "==",
                "is_expression": True,
                "python_val_exp": "obj.get('data')"
            },
            {
                "response_source": "response_body",
                "assert_key": "data",
                "expect_val": "123456",
                "expect_val_type": "int",
                "rule": "==",
                "is_expression": True,
                "python_val_exp": "obj.get('data')"
            },
            {
                "response_source": "response_body",
                "assert_key": "data",
                "expect_val": {},
                "expect_val_type": "list",
                "rule": "==",
                "is_expression": True,
                "python_val_exp": "obj.get('data')"
            },
            {
                "response_source": "response_body",
                "assert_key": "data",
                "expect_val": "123",
                "expect_val_type": "json",
                "rule": "==",
                "is_expression": True,
                "python_val_exp": "obj.get('data')"
            },
            {
                "response_source": "response_body",
                "assert_key": "data",
                "expect_val": "aa",
                "expect_val_type": "json_str",
                "rule": "==",
                "is_expression": True,
                "python_val_exp": "obj.get('data')"
            }
        ]
        num = num if num else 100
        for index in range(1, num):
            new_ass_resp = TestCaseAssertion(
                project_id=self.project_id,
                assertion_type='response',
                assert_description=f"响应断言:{index}",
                ass_json=[random.choice(x)],
                remark="脚本生成",
                creator="shell",
                creator_id=0
            )
            db.session.add(new_ass_resp)
        db.session.commit()
        print('>>> 创建响应断言完成')

    @set_app_context
    def create_db(self):
        """创建db"""

        mysql_db = TestDatabases(
            name='测试环境:mysql',
            db_type='mysql',
            db_connection={"host": "127.0.0.1", "password": "1234567890", "port": 33060, "user": "root"},
            remark="脚本生成",
            creator="shell",
            creator_id=0,
        )

        redis_db = TestDatabases(
            name='测试环境:redis',
            db_type='redis',
            db_connection={"db": 0, "host": "127.0.0.1", "password": "1234567890", "port": 63790},
            remark="脚本生成",
            creator="shell",
            creator_id=0,
        )

        postgresql_db = TestDatabases(
            name='测试环境:postgresql',
            db_type='postgresql',
            db_connection={},
            remark="脚本生成",
            creator="shell",
            creator_id=0,
        )

        mongodb_db = TestDatabases(
            name='测试环境:mongodb',
            db_type='mongodb',
            db_connection={},
            remark="脚本生成",
            creator="shell",
            creator_id=0,
        )

        sqlserver_db = TestDatabases(
            name='测试环境:sqlserver',
            db_type='sqlserver',
            db_connection={},
            remark="脚本生成",
            creator="shell",
            creator_id=0,
        )

        oracle_db = TestDatabases(
            name='测试环境:oracle',
            db_type='oracle',
            db_connection={},
            remark="脚本生成",
            creator="shell",
            creator_id=0,
        )

        es_db = TestDatabases(
            name='测试环境:ES',
            db_type='es',
            db_connection={},
            remark="脚本生成",
            creator="shell",
            creator_id=0,
        )
        add_db_list = [
            mysql_db, redis_db, postgresql_db, mongodb_db, sqlserver_db, oracle_db, es_db
        ]
        db.session.add_all(add_db_list)
        db.session.commit()
        print('>>> 创建db完成')

    @set_app_context
    def create_ass_field(self, num=None):
        """创建字段断言"""

        x1 = {
            "db_id": 1,
            "assert_list": [
                {
                    "query": "select id, case_name FROM ExileTestPlatform.exile_test_case WHERE id=1;",
                    "assert_field_list": [
                        {
                            "expect_val_type": "int",
                            "python_val_exp": "obj.get(\"id\")",
                            "rule": "==",
                            "assert_key": "id",
                            "expect_val": "1",
                            "is_expression": True
                        },
                        {
                            "expect_val_type": "str",
                            "python_val_exp": "obj.get(\"case_name\")",
                            "rule": "==",
                            "assert_key": "case_name",
                            "expect_val": "yyx",
                            "is_expression": False
                        }
                    ]
                }
            ]
        }
        x2 = {
            "db_id": 2,
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

        num = num if num else 100
        for index in range(1, num):
            new_ass_field = TestCaseAssertion(
                project_id=self.project_id,
                assertion_type='field',
                assert_description=f"响应断言:{index}",
                ass_json=[random.choice([x1, x2])],
                remark="脚本生成",
                creator="shell",
                creator_id=0
            )
            db.session.add(new_ass_field)
        db.session.commit()
        print('>>> 创建字段断言完成')

    @set_app_context
    def create_case_bind(self):
        """创建用例绑定关系"""
        case_list = TestCase.query.filter_by(creator_id=0).all()
        data_list = TestCaseData.query.filter_by(creator_id=0).all()
        ass_response_list = TestCaseAssertion.query.filter_by(creator_id=0, assertion_type='response').all()
        ass_field_list = TestCaseAssertion.query.filter_by(creator_id=0, assertion_type='field').all()

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
                creator_id=0
            )
            db.session.add(new_bind)
        db.session.commit()
        print('>>> 创建用例绑定关系完成')

    @set_app_context
    def create_var(self):
        """创建变量"""

        for index in range(1, 100):
            tv = TestVariable(
                var_name=f"变量:{index}",
                var_value=f"变量的值:{index}",
                var_type=random.choice(list(range(1, 13))),
                var_source=random.choice(["resp_data", "resp_header"]),
                var_get_key="code",
                expression="obj.get('message')",
                is_expression=1,
                remark="脚本生成",
                creator="shell",
                creator_id=0
            )
            db.session.add(tv)
        db.session.commit()
        print('创建变量完成')


if __name__ == '__main__':
    project_data_init = ProjectDataInit()
    project_data_init.create_admin()
    project_data_init.create_project_version()
    project_data_init.create_module()
    project_data_init.create_case(num=20)
    project_data_init.create_case_data(num=20)
    project_data_init.create_ass_response(num=20)
    project_data_init.create_db()
    project_data_init.create_ass_field(num=20)
    project_data_init.create_case_bind()
    # project_data_init.create_var()
