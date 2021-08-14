# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 3:08 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : command_register.py
# @Software: PyCharm

import os
import click
import platform

from sqlalchemy import or_, and_

from ExtendRegister.db_register import db
from app.models.admin.models import Admin, Role, Permission, MidAdminAndRole, MidPermissionAndRole, ApiResource


# export FLASK_APP=ApplicationExample.py

def register_commands(app):
    @app.cli.command("hello_world", help='hello-world')
    def hello_world():
        print('hello world')

    @app.cli.command(help='首次进行ORM操作')
    def orm():
        
        ps = platform.system()
        if ps in ['Linux', 'Darwin']:
            os.system("rm -rf " + os.getcwd() + "/migrations")
        elif ps == 'Windows':
            os.system("rd " + os.getcwd() + "/migrations")
        else:
            print('未找到操作系统:'.format(ps))

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
        command: flask create_user --username yyx --password 123456
        """

        query_user = Admin.query.filter_by(username=username).first()
        if query_user:
            print('用户:{}'.format(username))
        else:
            new_admin = Admin(
                username=username,
                password=password,
                phone=None,
                mail=None,
                code=str(Admin.query.count() + 1).zfill(5),
                creator='shell',
                creator_id='0',
                remark='manage shell')
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
