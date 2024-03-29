# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 9:45 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : case_api.py
# @Software: PyCharm

from all_reference import *
from app.models.test_case.models import TestCase
from app.models.test_project.models import (
    TestProjectVersion, TestModuleApp, MidProjectAndCase, MidVersionCase, MidModuleCase, MidTaskCase
)
from app.api.project_api.project_api import qp_deco

params_key = [
    ("case_name", "用例名称"),
    ("request_method", "请求方式"),
    ("request_base_url", "base url"),
    ("request_url", "url")
]


def check_method(current_method):
    """
    检查method
    :param current_method:
    :return:
    """
    if current_method.upper() in GlobalsDict.method_dict():
        return current_method.upper()
    else:
        return False


def new_check_version(project_id, version_id_list):
    """
    检查入参的 version_id 是否存在
    :param project_id: 项目id
    :param version_id_list: 版本id列表
    :return:
    """

    version_id_list = [obj.get('id') for obj in version_id_list]
    query_version = TestProjectVersion.query.filter(
        TestProjectVersion.id.in_(version_id_list),
        TestProjectVersion.project_id == project_id,
        TestProjectVersion.is_deleted == 0
    ).all()
    query_version_id_list = [version.id for version in query_version]
    check_diff = ActionSet.gen_difference(version_id_list, query_version_id_list)
    return check_diff


def new_check_module(project_id, module_id_list):
    """
    检查入参的 module_id 是否存在
    :param project_id: 项目id
    :param module_id_list: 模块id列表
    :return:
    """

    module_id_list = [obj.get('id') for obj in module_id_list]
    query_module = TestModuleApp.query.filter(
        TestModuleApp.id.in_(module_id_list),
        TestModuleApp.project_id == project_id,
        TestModuleApp.is_deleted == 0
    ).all()
    query_module_id_list = [module.id for module in query_module]
    check_diff = ActionSet.gen_difference(module_id_list, query_module_id_list)
    return check_diff


def case_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        data = request.get_json()
        project_id = data.get('project_id', 0)
        version_list = data.get('version_list', [])
        module_list = data.get('module_list', [])
        case_name = data.get('case_name', '').strip()
        request_method = data.get('request_method').upper()
        request_base_url = data.get('request_base_url', '').strip()
        case_status = data.get('case_status')

        check_bool, check_msg = RequestParamKeysCheck(data, params_key).result()
        if not check_bool:
            return api_result(code=NO_DATA, message=check_msg)

        if version_list:
            result = new_check_version(project_id, version_list)
            if result:
                return api_result(code=NO_DATA, message=f'项目id: {project_id} 未关联->版本迭代id:{result}')

        if module_list:
            result = new_check_module(project_id, module_list)
            if result:
                return api_result(code=NO_DATA, message=f'项目id: {project_id} 未关联->模块id:{result}')

        request_base_url = request_base_url.replace(" ", "")
        if not request_base_url:
            return api_result(code=NO_DATA, message='环境不能为空')

        request_method_result = check_method(current_method=request_method)
        if not request_method_result:
            return api_result(code=NO_DATA, message=f'请求方式: {request_method} 不存在')

        if not case_name:
            return api_result(code=NO_DATA, message='用例名称不能为空')

        if case_status not in ('active', 'dev', 'debug', 'over'):
            return api_result(code=NO_DATA, message=f'用例状态不存在: {case_status}')

        return func(*args, **kwargs)

    return wrapper


class CaseApi(MethodView):
    """
    用例Api
    GET: 用例详情
    POST: 用例新增
    PUT: 用例编辑
    DELETE: 用例删除
    """

    # decorators = [case_decorator]

    def get(self, case_id):
        """用例详情"""

        result = query_case_assemble(case_id=case_id)

        if not result:
            return api_result(code=NO_DATA, message=f'用例id:{case_id}不存在')

        return api_result(code=SUCCESS, message=SUCCESS_MESSAGE, data=result)

    @qp_deco
    @case_decorator
    def post(self):
        """用例新增"""

        data = request.get_json()
        project_id = data.get('project_id', 0)
        version_list = data.get('version_list', [])
        module_list = data.get('module_list', [])
        case_name = data.get('case_name', '').strip()
        request_method = data.get('request_method').upper()
        request_base_url = data.get('request_base_url', '').strip()
        request_url = data.get('request_url', '').strip()
        is_public = data.get('is_public')
        case_status = data.get('case_status', 'debug')
        remark = data.get('remark')

        query_case = TestCase.query.join(MidProjectAndCase, TestCase.id == MidProjectAndCase.case_id).filter(
            TestCase.is_deleted == 0,
            TestCase.case_name == case_name,
            MidProjectAndCase.project_id == project_id
        ).first()

        if query_case:
            return api_result(code=UNIQUE_ERROR, message=f'用例名称: {case_name} 已经存在')

        new_test_case = TestCase(
            case_name=case_name,
            request_method=request_method,
            request_base_url=request_base_url,
            request_url=request_url,
            is_public=is_public,
            creator=g.app_user.username,
            creator_id=g.app_user.id,
            case_status=case_status,
            remark=remark,
        )
        new_test_case.save()
        case_id = new_test_case.id

        version_id_list = [obj.get('id') for obj in version_list]
        module_id_list = [obj.get('id') for obj in module_list]

        mid_pc = MidProjectAndCase(
            project_id=project_id, case_id=case_id, creator=g.app_user.username, creator_id=g.app_user.id
        )
        db.session.add(mid_pc)
        list(map(lambda version_id: db.session.add(
            MidVersionCase(
                version_id=version_id, case_id=case_id, creator=g.app_user.username, creator_id=g.app_user.id)),
                 version_id_list))
        list(map(lambda module_id: db.session.add(
            MidModuleCase(
                module_id=module_id, case_id=case_id, creator=g.app_user.username, creator_id=g.app_user.id)),
                 module_id_list))
        db.session.commit()
        return api_result(code=POST_SUCCESS, message=POST_MESSAGE, data=new_test_case.to_json())

    @qp_deco
    @case_decorator
    def put(self):
        """用例编辑"""

        data = request.get_json()
        project_id = data.get('project_id', 0)
        version_list = data.get('version_list', [])
        module_list = data.get('module_list', [])
        case_id = data.get('id')
        case_name = data.get('case_name', '').strip()
        request_method = data.get('request_method').upper()
        request_base_url = data.get('request_base_url', '').strip()
        request_url = data.get('request_url', '').strip()
        is_public = data.get('is_public')
        case_status = data.get('case_status')
        remark = data.get('remark')

        query_case = TestCase.query.get(case_id)
        query_is_public = bool(query_case.is_public)

        if not query_case:
            return api_result(code=NO_DATA, message=f'用例不存在: {case_id}')

        if not query_is_public and query_case.creator_id != g.app_user.id:
            return api_result(code=NOT_CREATOR_ERROR, message=NOT_CREATOR_ERROR_MESSAGE)

        if query_case.case_name != case_name:
            if TestCase.query.join(MidProjectAndCase, TestCase.id == MidProjectAndCase.case_id).filter(
                    TestCase.is_deleted == 0,
                    TestCase.case_name == case_name,
                    MidProjectAndCase.project_id == project_id
            ).all():
                return api_result(code=UNIQUE_ERROR, message=f'用例名称:{case_name} 已经存在')

        query_case.case_name = case_name
        query_case.request_method = request_method
        query_case.request_base_url = request_base_url
        query_case.request_url = request_url
        query_case.is_public = is_public
        query_case.modifier = g.app_user.username
        query_case.modifier_id = g.app_user.id
        query_case.case_status = case_status
        query_case.remark = remark

        db.session.query(MidVersionCase).filter(MidVersionCase.case_id == case_id).delete(
            synchronize_session=False)

        db.session.query(MidModuleCase).filter(MidModuleCase.case_id == case_id).delete(
            synchronize_session=False)

        if version_list:
            version_id_list = [obj.get('id') for obj in version_list]
            list(map(lambda version_id: db.session.add(
                MidVersionCase(
                    version_id=version_id, case_id=case_id, modifier=g.app_user.username, modifier_id=g.app_user.id)),
                     version_id_list))

        if module_list:
            module_id_list = [obj.get('id') for obj in module_list]
            list(map(lambda module_id: db.session.add(
                MidModuleCase(
                    module_id=module_id, case_id=case_id, modifier=g.app_user.username, modifier_id=g.app_user.id)),
                     module_id_list))

        db.session.commit()
        return api_result(code=PUT_SUCCESS, message=PUT_MESSAGE, data=query_case.to_json())

    def delete(self):
        """用例删除"""

        data = request.get_json()
        case_id = data.get('id')

        query_case = TestCase.query.get(case_id)
        if not query_case:
            return api_result(code=NO_DATA, message=f'用例不存在:{case_id}')

        if query_case.creator_id != g.app_user.id:
            return api_result(code=BUSINESS_ERROR, message='非管理员不能删除其他人的用例！')

        db.session.query(MidProjectAndCase).filter_by(case_id=case_id).delete(synchronize_session=False)
        db.session.query(MidVersionCase).filter_by(case_id=case_id).delete(synchronize_session=False)
        db.session.query(MidModuleCase).filter_by(case_id=case_id).delete(synchronize_session=False)
        db.session.query(MidTaskCase).filter_by(case_id=case_id).delete(synchronize_session=False)
        query_case.modifier = g.app_user.username
        query_case.modifier_id = g.app_user.id
        query_case.delete()
        return api_result(code=DEL_SUCCESS, message=DEL_MESSAGE)


class CasePageApi(MethodView):
    """
    case page api
    POST: 用例分页模糊查询
    """

    def post(self):
        """用例分页模糊查询"""
        data = request.get_json()
        project_id = data.get('project_id')
        version_id = data.get('version_id', 0)
        module_id = data.get('module_id', 0)
        case_id = data.get('case_id')
        case_name = data.get('case_name', '')
        request_url = data.get('request_url', '')
        request_method = data.get('request_method')
        case_status = data.get('case_status')
        creator_id = data.get('creator_id')
        is_deleted = data.get('is_deleted', False)
        field_order_by = data.get('field_order_by', 'update_time')
        is_desc = data.get('is_desc', True)
        page = data.get('page')
        size = data.get('size')
        limit = page_size(page=page, size=size)

        if not project_id:
            return api_result(code=NO_DATA, message='项目不存在')

        sql = f"""
        SELECT
            *
        FROM
            exile5_test_case
        WHERE
            id in( SELECT DISTINCT
                    A.id FROM exile5_test_case AS A
                    INNER JOIN exile5_test_mid_project_case AS B ON A.id = B.case_id
                    {'INNER JOIN exile5_test_mid_version_case AS C ON A.id = C.case_id' if version_id else ''}
                    {'INNER JOIN exile5_test_mid_module_case AS D ON A.id = D.case_id' if module_id else ''}
                WHERE
                    A.is_deleted = 0
                    AND B.project_id = {project_id}
                    {f'AND C.version_id={version_id}' if version_id else ''}
                    {f'AND D.module_id={module_id}' if module_id else ''}
                )
            AND is_deleted = 0
            AND case_name LIKE "%{case_name}%"
            AND request_url LIKE "%{request_url}%"
            {f"AND request_method='{request_method}'" if request_method else ''}
            {f"AND case_status='{case_status}'" if case_status else ''}
            {f'AND creator_id={creator_id}' if creator_id else ''}
        ORDER BY
            {f'{f"{field_order_by} DESC" if is_desc else field_order_by}' if field_order_by else 'update_time DESC'}
        LIMIT {limit[0]},{limit[1]};
        """

        sql_count = f"""
        SELECT
            COUNT(*)
        FROM
            exile5_test_case
        WHERE
            id in( SELECT DISTINCT
                    A.id FROM exile5_test_case AS A
                    INNER JOIN exile5_test_mid_project_case AS B ON A.id = B.case_id
                    {'INNER JOIN exile5_test_mid_version_case AS C ON A.id = C.case_id' if version_id else ''}
                    {'INNER JOIN exile5_test_mid_module_case AS D ON A.id = D.case_id' if module_id else ''}
                WHERE
                    A.is_deleted = 0
                    AND B.project_id = {project_id}
                    {f'AND C.version_id={version_id}' if version_id else ''}
                    {f'AND D.module_id={module_id}' if module_id else ''}
                )
            AND is_deleted = 0
            AND case_name LIKE "%{case_name}%"
            AND request_url LIKE "%{request_url}%"
            {f"AND request_method='{request_method}'" if request_method else ''}
            {f"AND case_status='{case_status}'" if case_status else ''}
            {f'AND creator_id={creator_id}' if creator_id else ''}
        """

        # print(sql)
        # print(sql_count)

        result_list = project_db.select(sql)
        result_count = project_db.select(sql_count)

        result_data = {
            'records': result_list if result_list else [],
            'now_page': page,
            'total': result_count[0].get('COUNT(*)')
        }

        return api_result(code=SUCCESS, message=SUCCESS_MESSAGE, data=result_data)
