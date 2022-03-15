# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 3:08 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : command_register.py
# @Software: PyCharm

import os
import click
import random
import shutil

from sqlalchemy import or_, and_

from common.libs.db import project_db
from ExtendRegister.db_register import db
from app.models.admin.models import Admin, Role, Permission, MidAdminAndRole, MidPermissionAndRole, ApiResource
from app.models.test_case.models import TestCase, TestCaseData
from app.models.test_case_scenario.models import TestCaseScenario
from app.models.test_variable.models import TestVariable
from app.models.test_case_assert.models import TestCaseAssResponse, TestCaseAssField
from app.models.push_reminder.models import MailConfModel, DingDingConfModel
from app.models.platform_conf.models import PlatformConfModel
from app.models.ui_auto_file.models import UiAutoFile
from app.models.test_project.models import TestProject, TestProjectVersion, MidProjectVersionAndCase, \
    MidProjectVersionAndScenario
from app.models.test_case_config.models import TestDatabases

"""
export FLASK_APP=ApplicationExample.py
"""


def register_commands(app):
    """flask cli"""

    @app.cli.command("hello_world", help='hello-world')
    def hello_world():
        print('hello world')

    @app.cli.command(help='首次进行ORM操作')
    def orm():

        migrations_path = os.getcwd() + "/migrations"

        if os.path.exists(migrations_path):
            shutil.rmtree(migrations_path)
            print('migrations 删除')
        else:
            print('migrations 不存在')

        try:
            query_table_sql = """SHOW TABLES LIKE 'alembic_version';"""
            print(query_table_sql)
            query_result = project_db.execute_sql(sql=query_table_sql)
            print('query_result:{} {}'.format(query_result, bool(query_result)))
            if bool(query_result):
                delete_table_sql = """DROP TABLE alembic_version;"""
                print(delete_table_sql)
                delete_result = project_db.execute_sql(sql=delete_table_sql)
                print('delete_result:{} {}'.format(delete_result, bool(delete_result)))
            else:
                pass
        except BaseException as e:
            print('删除 alembic_version 失败:{}'.format(str(e)))

        try:
            os.system("flask db init")
            os.system("flask db migrate")
            os.system("flask db upgrade")
            print('创建成功')
        except BaseException as e:
            print('创建失败:{}'.format(str(e)))

    @app.cli.command(help='更新表')
    def table():
        try:
            os.system("flask db migrate")
            os.system("flask db upgrade")
            print('创建成功')
        except BaseException as e:
            print('创建失败:{}'.format(str(e)))

    @app.cli.command("create_user", help="创建用户")
    @click.option("--username", help="用户名", type=str)
    @click.option("--password", help="密码", type=str)
    def create_user(username, password):
        """
        command: flask create_user --username admin --password 123456
        command: flask create_user --username yyx --password 123456
        command: flask create_user --username okc --password 123456
        """

        query_user = Admin.query.filter_by(username=username).first()
        if query_user:
            print('用户:{} 已存在'.format(username))
        else:
            new_admin = Admin(
                username=username,
                password=password,
                phone=None,
                mail=None,
                creator='shell',
                creator_id='0',
                remark='manage shell')
            new_admin.set_code()
            db.session.add(new_admin)
            db.session.commit()
            print('用户: {} 添加成功'.format(username))

    @app.cli.command("crm_init", help='CRM初始化')
    def crm_init():
        """
        CRM初始化
        """

        admin = {
            'username': 'admin',
            'password': '123456',
            'phone': '15013038819',
            'mail': 'yangyuexiong33@gmail.com',
            'code': '00001'
        }
        admin2 = {
            'username': 'admin2',
            'password': '123456',
            'phone': '15013038818',
            'mail': 'yangyuexiong33@gmail.com',
            'code': '00002'
        }
        admin3 = {
            'username': 'admin3',
            'password': '123456',
            'phone': '15013038817',
            'mail': 'yangyuexiong33@gmail.com',
            'code': '00003'
        }
        admin4 = {
            'username': 'admin4',
            'password': '123456',
            'phone': '15013038816',
            'mail': 'yangyuexiong33@gmail.com',
            'code': '00004'
        }

        admin_list = [admin, admin2, admin3, admin4]
        role_list = ['超级管理员', '管理员A', '管理员B', '管理员C', '管理员D']
        api_resource = [
            {
                'name': 'crm首页',
                'url': '/crm/index_api',
                'method': 'GET'
            },
            {
                'name': 'crm测试',
                'url': '/crm/test',
                'method': 'GET'
            },

            {
                'name': '用户列表',
                'url': '/crm/admin/page',
                'method': 'POST'
            },
            {
                'name': '用户详情',
                'url': '/crm/admin',
                'method': 'GET',
                'is_url_var': '1'
            },
            {
                'name': '用户新增',
                'url': '/crm/admin',
                'method': 'POST'
            },
            {
                'name': '用户编辑',
                'url': '/crm/admin',
                'method': 'PUT'
            },
            {
                'name': '用户(禁用/启用)',
                'url': '/crm/admin',
                'method': 'DELETE'
            },
            {
                'name': '用户配置角色',
                'url': '/crm/admin/rel',
                'method': 'POST'
            },

            {
                'name': '角色列表',
                'url': '/crm/role/page',
                'method': 'POST'
            },
            {
                'name': '角色详情',
                'url': '/crm/role',
                'method': 'GET',
                'is_url_var': '1'
            },
            {
                'name': '角色新增',
                'url': '/crm/role',
                'method': 'POST'
            },
            {
                'name': '角色编辑',
                'url': '/crm/role',
                'method': 'PUT'
            },
            {
                'name': '角色(禁用/启用)',
                'url': '/crm/role',
                'method': 'DELETE'
            },
            {
                'name': '角色配置权限',
                'url': '/crm/role/rel',
                'method': 'POST'
            },

            {
                'name': '权限列表',
                'url': '/crm/permission/page',
                'method': 'POST'
            },
            {
                'name': '权限详情',
                'url': '/crm/permission',
                'method': 'GET',
                'is_url_var': '1'
            },
            {
                'name': '权限新增',
                'url': '/crm/permission',
                'method': 'POST'
            },
            {
                'name': '权限编辑',
                'url': '/crm/permission',
                'method': 'PUT'
            },
            {
                'name': '权限(禁用/启用)',
                'url': '/crm/permission',
                'method': 'DELETE'
            },

            {
                'name': '接口列表',
                'url': '/crm/api_resource/page',
                'method': 'POST'
            },
            {
                'name': '接口详情',
                'url': '/crm/api_resource',
                'method': 'GET',
                'is_url_var': '1'
            },
            {
                'name': '接口新增',
                'url': '/crm/api_resource',
                'method': 'POST'
            },
            {
                'name': '接口编辑',
                'url': '/crm/api_resource',
                'method': 'PUT'
            },
            {
                'name': '接口(禁用/启用)',
                'url': '/crm/api_resource',
                'method': 'DELETE'
            },

        ]

        # 创建用户
        for ad in admin_list:
            print(ad)
            query_admin = Admin.query.filter(
                or_(Admin.username == ad.get('username'), Admin.phone == ad.get('phone'))).first()
            if query_admin:
                print('CRM用户: {} 已存在'.format(query_admin))
            else:
                new_admin = Admin(
                    username=ad.get('username'),
                    password=ad.get('password'),
                    phone=ad.get('phone'),
                    mail=ad.get('mail'),
                    code=ad.get('code'),
                    creator='shell',
                    creator_id='0',
                    remark='manage shell')
                db.session.add(new_admin)
                db.session.commit()
                print('CRM用户: {} 添加成功'.format(admin))

        # 创建角色
        for role in role_list:
            query_role = Role.query.filter_by(name=role).first()
            if query_role:
                print('CRM角色: {} 已存在'.format(query_role))
            else:
                new_role = Role(name=role, creator='shell', creator_id='0', remark='manage shell')
                db.session.add(new_role)
                db.session.commit()
                print('CRM角色: {} 添加成功'.format(role))

        # 创建权限
        for api in api_resource:
            name = api.get('name')
            url = api.get('url')
            method = api.get('method')
            query_api = ApiResource.query.filter(and_(ApiResource.url == url, ApiResource.method == method)).first()
            if query_api:
                print('CRM Api: {} 已存在'.format(query_api))
            else:
                api_resource = ApiResource(
                    name=name,
                    url=url,
                    method=api.get('method'),
                    is_url_var=api.get('is_url_var'),
                    creator='shell',
                    creator_id='0',
                    remark='manage shell'
                )
                db.session.add(api_resource)
                db.session.commit()
                print('CRM Api 创建完成:{}'.format(name))

                query_permission = Permission.query.filter_by(name=name).first()
                if query_permission:
                    print('CRM 权限: {} 已存在'.format(query_permission))
                else:
                    permission = Permission(
                        name=name,
                        resource_id=api_resource.id,
                        resource_type='SERVER_API',
                        creator='shell',
                        creator_id='0',
                        remark='manage shell'
                    )
                    db.session.add(permission)
                    db.session.commit()
                    print('CRM 权限 创建完成:{}'.format(name))

        # 为admin设置所有角色权限
        root_admin = Admin.query.filter_by(username='admin').first()
        super_role = Role.query.filter_by(name='超级管理员').first()
        all_role = Role.query.all()
        all_permission = Permission.query.all()

        # 配置权限
        for per in all_permission:
            query_mid_permission_role = MidPermissionAndRole.query.filter_by(
                role_id=super_role.id,
                permission_id=per.id).first()
            if query_mid_permission_role:
                print('角色:{} 已拥有权限:{}'.format(super_role.name, per.name))
            else:
                mid_permission_role = MidPermissionAndRole(
                    permission_id=per.id,
                    role_id=super_role.id,
                    creator='shell',
                    creator_id='0'
                )
                db.session.add(mid_permission_role)
                print('角色:{} 添加 权限:{} 完成'.format(super_role.name, per.name))
        db.session.commit()

        # 配置角色
        for role in all_role:
            query_mid_admin_role = MidAdminAndRole.query.filter_by(admin_id=root_admin.id, role_id=role.id).first()
            if query_mid_admin_role:
                print('用户:{} 已拥有角色:{}'.format(root_admin.username, role.name))
            else:
                mid_admin_role = MidAdminAndRole(
                    admin_id=root_admin.id,
                    role_id=role.id,
                    creator='shell',
                    creator_id='0'
                )
                db.session.add(mid_admin_role)
                print('用户:{} 添加 角色:{} 完成'.format(root_admin.username, role.name))
        db.session.commit()

    @app.cli.command("create_test_data", help='生成测试数据')
    def create_test_data():
        request_method = ["GET", "POST", "PUT", "DELETE"]

        def create_platform_conf():
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

        def create_project_version():
            new_project = TestProject(
                project_name='初始化项目',
                remark="脚本生成",
                creator="shell",
                creator_id=999999,
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
                    creator_id=999999,
                )
                db.session.add(new_version)
            db.session.commit()

        def create_case():
            api_list = [
                '/api/case_execute_logs_page',
                '/api/field_ass_rule_page',
                '/api/case_bind_field_ass',
                '/api/case_req_data_page',
                '/api/resp_ass_rule_page',
                '/api/case_bind_resp_ass',
                '/api/case_scenario_page',
                '/api/case_execute_logs',
                '/api/case_logs_page',
                '/api/field_ass_rule',
                '/api/case_bind_data',
                '/api/case_env_page',
                '/api/case_req_data',
                '/api/case_var_page',
                '/api/resp_ass_rule',
                '/api/case_scenario',
                '/api/case_db_page',
                '/api/case_report',
                '/api/user_page',
                '/api/case_page',
                '/api/case_bind',
                '/api/rule_test',
                '/api/case_send',
                '/api/case_exec',
                '/api/case_env',
                '/api/case_var',
                '/api/case_set',
                '/api/tourist',
                '/api/case_db',
                '/api/index',
                '/api/login',
                '/api/case',
                '/api/field_ass_rule/<ass_field_id>',
                '/api/case_req_data/<req_data_id>',
                '/api/resp_ass_rule/<ass_resp_id>',
                '/api/case_scenario/<scenario_id>',
                '/api/case_env/<env_id>',
                '/api/case_var/<var_id>',
                '/api/case_db/<db_id>',
                '/api/case/<case_id>',
                '/static/<filename>'
            ]
            for index, url in enumerate(api_list, 1):
                new_test_case = TestCase(
                    case_name="测试:" + url,
                    request_method=random.choice(request_method),
                    request_base_url="http://0.0.0.0:7272",
                    request_url=url,
                    is_shared=True,
                    is_public=True,
                    remark="脚本生成:{}".format(index),
                    creator="脚本生成:{}".format(index),
                    creator_id=999999,
                    total_execution=random.randint(1, 99)
                )
                db.session.add(new_test_case)
            db.session.commit()

        def update_case():
            all_case = TestCase.query.all()
            for index, case in enumerate(all_case, 1):
                case.request_method = random.choice(request_method)
                case.modifier = "脚本生成:{}".format(random.randint(1, len(all_case)))
                case.modifier_id = 888888
            db.session.commit()

        def set_case_version():
            all_case = TestCase.query.all()
            all_version_id = [v.id for v in TestProjectVersion.query.all()]

            for case in all_case:
                mid = MidProjectVersionAndCase(
                    version_id=random.choice(all_version_id),
                    task_id=0,
                    case_id=case.id,
                    remark="脚本生成",
                    creator="shell",
                    creator_id=999999
                )
                db.session.add(mid)
            db.session.commit()

        def create_case_data():
            for index, i in enumerate(range(0, 33)):
                tcd = TestCaseData(
                    data_name="测试数据:{}".format(index),
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

        def create_var():
            for index, i in enumerate(range(0, 13)):
                tv = TestVariable(
                    var_name="变量:{}".format(index),
                    var_value="变量的值:{}".format(index),
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

        def create_db():
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

        def create_ass_resp():
            for index, i in enumerate(range(0, 13)):
                ar = TestCaseAssResponse(
                    assert_description="业务逻辑断言:{}".format(index),
                    ass_json=[
                        {
                            "response_source": "response_body",
                            "assert_key": "code",
                            "expect_val": "200",
                            "expect_val_type": "1",
                            "rule": "==",
                            "is_expression": 0,
                            "python_val_exp": "okc.get('a').get('b').get('c')[0]"
                        },
                        {
                            "response_source": "response_headers",
                            "assert_key": "log_uuid",
                            "expect_val": "qwertyuiop",
                            "expect_val_type": "2",
                            "rule": ">=",
                            "is_expression": 0,
                            "python_val_exp": "okc.get('a').get('b').get('c')[0]"
                        },
                        {
                            "response_source": "response_body",
                            "assert_key": "message",
                            "expect_val": "index",
                            "expect_val_type": "2",
                            "rule": "==",
                            "is_expression": 0,
                            "python_val_exp": "okc.get('a').get('b').get('c')[0]"
                        },
                        {
                            "response_source": "response_body",
                            "assert_key": "message",
                            "expect_val": "index",
                            "expect_val_type": "2",
                            "rule": "==",
                            "is_expression": 1,
                            "python_val_exp": "okc.get('message')"
                        },
                        {
                            "response_source": "response_body",
                            "assert_key": "message",
                            "expect_val": "yangyuexiongyyx",
                            "expect_val_type": "2",
                            "rule": "==",
                            "is_expression": 1,
                            "python_val_exp": "okc.get('token')"
                        }
                    ],
                    remark="脚本生成",
                    creator="shell",
                    creator_id=999999
                )
                db.session.add(ar)
            db.session.commit()

        def create_ass_field():
            for index, i in enumerate(range(0, 13)):
                af = TestCaseAssField(
                    assert_description="数据字段断言:{}".format(index),
                    ass_json=[
                        {
                            "db_id": 1,
                            "assert_list": [
                                {
                                    "query": "select id, case_name FROM ExileTestPlatform.exile_test_case WHERE id=1;",
                                    "assert_field_list": [
                                        {
                                            "rule": "==",
                                            "assert_key": "id",
                                            "expect_val": 11,
                                            "is_expression": 1,
                                            "python_val_exp": "obj.get('id')",
                                            "expect_val_type": "1"
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    remark="脚本生成",
                    creator="shell",
                    creator_id=999999
                )
                db.session.add(af)
            db.session.commit()

        create_platform_conf()
        create_project_version()
        create_case()
        update_case()
        set_case_version()
        create_case_data()
        create_var()
        create_db()
        create_ass_resp()
        create_ass_field()
