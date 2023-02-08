# -*- coding: utf-8 -*-
# @Time    : 2023/1/17 14:31
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : ui_case_api.py
# @Software: PyCharm

from all_reference import *
from app.models.test_project.models import TestProject, TestProjectVersion, TestModuleApp
from app.models.ui_test_case.models import (
    UiTestCase, MidProjectAndUiCase, MidVersionUiCase, MidTaskUiCase, MidModuleUiCase
)
from app.api.case_api.case_api import new_check_version, new_check_module

demo_data = [
    {
        "uuid": "RqceT7F7VR7MUepkCe3TgP",
        "index": 1,
        "title": "开始",
        "type": "master",
        "business_list": [
            {
                "uuid": "43mcDsxMP5hfgwXpYFekNf",
                "index": 1,
                "type": "ui_control",
                "title": "启动浏览器控件",
                "function": "open",
                "args": {
                    "url": "http://localhost:3200/login"
                }
            }
        ]
    },
    {
        "uuid": "Paahmn4pisq6DCMAb6MTj7",
        "index": 2,
        "title": "登录",
        "type": "master",
        "business_list": [
            {
                "uuid": "BeKExy3oDBmffkyh6z5sFh",
                "index": 1,
                "type": "ui_control",
                "title": "输入账号",
                "function": "input",
                "args": {
                    "mode": "XPATH",
                    "value": "//*[@id=\"login-form\"]/div[1]/div[2]/div/div/div/input",
                    "data": "admin"
                }
            },
            {
                "uuid": "TgxCgmQ3eAiYJ9poTDa3y8",
                "index": 2,
                "type": "ui_control",
                "title": "输入密码",
                "function": "input",
                "args": {
                    "mode": "XPATH",
                    "value": "//*[@id=\"login-form\"]/div[2]/div[2]/div/div/div/input",
                    "data": "123456"
                }
            },
            {
                "uuid": "bAYF8u42at5VDYHRwc63bu",
                "index": 3,
                "type": "ui_control",
                "title": "点击登录",
                "function": "click",
                "args": {
                    "mode": "XPATH",
                    "value": "//*[@id=\"login-form\"]/div[3]/div[2]/div/div/div/button[1]"
                }
            },
        ]
    },
    {
        "uuid": "DuykYPs5UhqhULXCqerzGq",
        "index": 3,
        "title": "嵌套循环操作",
        "type": "master",
        "business_list": [
            {
                "uuid": "VwfKjeL87DVythEsHsC8Jd",
                "index": 1,
                "type": "logic_control",
                "title": "第一层循环",
                "function": "for",
                "num": 3,
                "data_source": [],
                "business_list": [
                    {
                        "uuid": "BeKExy3oDBmffkyh6z5sFh",
                        "index": 1,
                        "type": "ui_control",
                        "title": "输入账号",
                        "function": "input",
                        "args": {
                            "mode": "XPATH",
                            "value": "//*[@id=\"login-form\"]/div[1]/div[2]/div/div/div/input",
                            "data": "admin"
                        }
                    },
                    {
                        "uuid": "TgxCgmQ3eAiYJ9poTDa3y8",
                        "index": 2,
                        "type": "ui_control",
                        "title": "输入密码",
                        "function": "input",
                        "args": {
                            "mode": "XPATH",
                            "value": "//*[@id=\"login-form\"]/div[2]/div[2]/div/div/div/input",
                            "data": "123456"
                        }
                    },
                    {
                        "uuid": "bAYF8u42at5VDYHRwc63bu",
                        "index": 3,
                        "type": "ui_control",
                        "title": "点击登录",
                        "function": "click",
                        "args": {
                            "mode": "XPATH",
                            "value": "//*[@id=\"login-form\"]/div[3]/div[2]/div/div/div/button[1]"
                        }
                    },
                    {
                        "uuid": "bzjmqAUjuYTs3sASxoXh3r",
                        "index": 4,
                        "type": "logic_control",
                        "title": "第二层循环",
                        "function": "for",
                        "num": 3,
                        "data_source": [],
                        "business_list": [
                            {
                                "uuid": "RqceT7F7VR7MUepkCe3123",
                                "index": 1,
                                "title": "录入数据",
                                "type": "master",
                                "business_list": [
                                    {
                                        "uuid": "6nBzTGWXAaDdE8fo5Xa123",
                                        "index": 11,
                                        "type": "ui_control",
                                        "title": "输入人员名称",
                                        "function": "input",
                                        "args": {
                                            "mode": "XPATH",
                                            "value": "//*[@id=\"project-search-container\"]/div/form/div/div/div/input",
                                            "data": "zxc"
                                        }
                                    },
                                    {
                                        "uuid": "oHCN6jjbDCYWzgjzNoj123",
                                        "index": 22,
                                        "type": "ui_control",
                                        "title": "点击搜索",
                                        "function": "click",
                                        "args": {
                                            "mode": "XPATH",
                                            "value": "//*[@id=\"project-search-container\"]/div/form/div/span"
                                        }
                                    },
                                    {
                                        "uuid": "dPHmBmPcAGpp5zqcX7M123",
                                        "index": 33,
                                        "type": "ui_control",
                                        "title": "编辑",
                                        "function": "click",
                                        "args": {
                                            "mode": "XPATH",
                                            "value": "//*[@id=\"main-container\"]/div[1]/div[1]/div/div"
                                        }
                                    },
                                    {
                                        "uuid": "68AUdem7SfBnx8CAQs3123",
                                        "index": 3332,
                                        "type": "ui_control",
                                        "title": "保存",
                                        "function": "click",
                                        "args": {
                                            "mode": "XPATH",
                                            "value": "//*[@id=\"app\"]/div/div[1]/div[2]/div[3]"
                                        }
                                    },
                                ]
                            },

                        ]
                    },
                    {
                        "uuid": "Zf3tJvN3t4n8RFLCiTVYLm",
                        "index": 5,
                        "type": "ui_control",
                        "title": "点击退出",
                        "function": "click",
                        "args": {
                            "mode": "XPATH",
                            "value": "/html/body/div[2]/div/div/div/div[3]/li/span/div"
                        }
                    }
                ]
            }
        ]
    },
    {
        "uuid": "3Lr7gkJx9WjXr8DRzWoU4e",
        "index": 1,
        "title": "结束",
        "type": "master",
        "business_list": [
            {
                "uuid": "e6rL6LWxRZkyGYkQadn3yz",
                "index": 1,
                "type": "ui_control",
                "title": "关闭浏览器",
                "function": "close",
                "args": {}
            }
        ]
    }
]


def ui_case_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        data = request.get_json()
        project_id = data.get('project_id', 0)
        version_list = data.get('version_list', [])
        module_list = data.get('module_list', [])
        case_name = data.get('case_name', '').strip()
        case_status = data.get('case_status')
        meta_data = data.get('meta_data')

        query_project = TestProject.query.get(project_id)
        if not query_project:
            return api_result(code=NO_DATA, message=f'项目: {project_id} 不存在')

        if version_list:
            result = new_check_version(project_id, version_list)
            if result:
                return api_result(code=NO_DATA, message=f'项目:{query_project.project_name}下不存在->版本迭代id:{result}')

        if module_list:
            result = new_check_module(project_id, module_list)
            if result:
                return api_result(code=NO_DATA, message=f'项目:{query_project.project_name}下不存在->模块id:{result}')

        if not case_name:
            return api_result(code=NO_DATA, message='用例名称不能为空')

        if case_status not in ('active', 'dev', 'debug', 'over'):
            return api_result(code=NO_DATA, message=f'用例状态不存在: {case_status}')

        if not isinstance(meta_data, list):
            return api_result(code=TYPE_ERROR, message='WebUI操作步骤集合错误')

        return func(*args, **kwargs)

    return wrapper


class UiCaseApi(MethodView):
    """
    UI用例 Api
    GET: UI用例详情
    POST: 新增UI用例
    PUT: 编辑UI用例
    DELETE: 删除UI用例
    """

    def get(self, ui_case_id):
        """UI用例详情"""

        return api_result(code=SUCCESS, message=SUCCESS_MESSAGE, data=demo_data)

    @ui_case_decorator
    def post(self):
        """新增UI用例"""

        data = request.get_json()
        project_id = data.get('project_id', 0)
        version_list = data.get('version_list', [])
        module_list = data.get('module_list', [])
        case_name = data.get('case_name', '').strip()
        meta_data = data.get('meta_data')
        is_shared = data.get('is_shared')
        is_public = data.get('is_public')
        case_status = data.get('case_status', 'debug')
        remark = data.get('remark')

        query_ui_case = UiTestCase.query.join(MidProjectAndUiCase, UiTestCase.id == MidProjectAndUiCase.case_id).filter(
            UiTestCase.is_deleted == 0,
            UiTestCase.case_name == case_name,
            MidProjectAndUiCase.project_id == project_id
        ).first()

        if query_ui_case:
            return api_result(code=UNIQUE_ERROR, message=f'UI用例名称: {case_name} 已经存在')

        new_ui_case = UiTestCase(
            case_name=case_name,
            is_shared=is_shared,
            is_public=is_public,
            creator=g.app_user.username,
            creator_id=g.app_user.id,
            case_status=case_status,
            remark=remark,
            meta_data=meta_data
        )
        new_ui_case.save()
        case_id = new_ui_case.id

        version_id_list = [obj.get('id') for obj in version_list]
        module_id_list = [obj.get('id') for obj in module_list]

        mid_pc = MidProjectAndUiCase(
            project_id=project_id, case_id=case_id, creator=g.app_user.username, creator_id=g.app_user.id
        )
        db.session.add(mid_pc)
        list(map(lambda version_id: db.session.add(
            MidVersionUiCase(
                version_id=version_id, case_id=case_id, creator=g.app_user.username, creator_id=g.app_user.id)),
                 version_id_list))
        list(map(lambda module_id: db.session.add(
            MidModuleUiCase(
                module_id=module_id, case_id=case_id, creator=g.app_user.username, creator_id=g.app_user.id)),
                 module_id_list))
        db.session.commit()
        return api_result(code=POST_SUCCESS, message=POST_MESSAGE, data=new_ui_case.to_json())

    @ui_case_decorator
    def put(self):
        """编辑UI用例"""

        data = request.get_json()
        project_id = data.get('project_id', 0)
        version_list = data.get('version_list', [])
        module_list = data.get('module_list', [])
        case_id = data.get('id')
        case_name = data.get('case_name', '').strip()
        meta_data = data.get('meta_data')
        is_shared = data.get('is_shared')
        is_public = data.get('is_public')
        case_status = data.get('case_status')
        remark = data.get('remark')

        query_ui_case = UiTestCase.query.get(case_id)

        if not query_ui_case:
            return api_result(code=NO_DATA, message=f'UI用例不存在:{case_id}')

        if not bool(is_public) and query_ui_case.creator_id != g.app_user.id:
            return api_result(code=BUSINESS_ERROR, message='非创建人，无法修改使用状态')

        if not bool(is_shared) and query_ui_case.creator_id != g.app_user.id:
            return api_result(code=BUSINESS_ERROR, message='非创建人，无法修改执行状态')

        if not bool(query_ui_case.is_public):
            if query_ui_case.creator_id != g.app_user.id:
                return api_result(code=BUSINESS_ERROR, message='该用例未开放,只能被创建人修改!')

        if query_ui_case.case_name != case_name:
            if UiTestCase.query.join(MidProjectAndUiCase, UiTestCase.id == MidProjectAndUiCase.case_id).filter(
                    UiTestCase.is_deleted == 0,
                    UiTestCase.case_name == case_name,
                    MidProjectAndUiCase.project_id == project_id
            ).all():
                return api_result(code=UNIQUE_ERROR, message=f'UI用例名称:{case_name} 已经存在')

        query_ui_case.case_name = case_name
        query_ui_case.meta_data = meta_data
        query_ui_case.is_shared = is_shared
        query_ui_case.is_public = is_public
        query_ui_case.modifier = g.app_user.username
        query_ui_case.modifier_id = g.app_user.id
        query_ui_case.case_status = case_status
        query_ui_case.remark = remark

        db.session.query(MidVersionUiCase).filter(MidVersionUiCase.case_id == case_id).delete(
            synchronize_session=False)

        db.session.query(MidModuleUiCase).filter(MidModuleUiCase.case_id == case_id).delete(
            synchronize_session=False)

        if version_list:
            version_id_list = [obj.get('id') for obj in version_list]
            list(map(lambda version_id: db.session.add(
                MidVersionUiCase(
                    version_id=version_id, case_id=case_id, modifier=g.app_user.username, modifier_id=g.app_user.id)),
                     version_id_list))

        if module_list:
            module_id_list = [obj.get('id') for obj in module_list]
            list(map(lambda module_id: db.session.add(
                MidModuleUiCase(
                    module_id=module_id, case_id=case_id, modifier=g.app_user.username, modifier_id=g.app_user.id)),
                     module_id_list))

        db.session.commit()

        return api_result(code=PUT_SUCCESS, message=PUT_MESSAGE, data=query_ui_case.to_json())

    def delete(self):
        """删除UI用例"""

        data = request.get_json()
        case_id = data.get('id')

        query_ui_case = UiTestCase.query.get(case_id)
        if not query_ui_case:
            return api_result(code=NO_DATA, message=f'UI用例不存在:{case_id}')

        if query_ui_case.creator_id != g.app_user.id:
            return api_result(code=BUSINESS_ERROR, message='非管理员不能删除其他人的用例！')

        db.session.query(MidProjectAndUiCase).filter_by(case_id=case_id).delete(synchronize_session=False)
        db.session.query(MidVersionUiCase).filter_by(case_id=case_id).delete(synchronize_session=False)
        db.session.query(MidModuleUiCase).filter_by(case_id=case_id).delete(synchronize_session=False)
        db.session.query(MidTaskUiCase).filter_by(case_id=case_id).delete(synchronize_session=False)
        query_ui_case.modifier = g.app_user.username
        query_ui_case.modifier_id = g.app_user.id
        query_ui_case.delete()
        return api_result(code=DEL_SUCCESS, message=DEL_MESSAGE, data=[])
