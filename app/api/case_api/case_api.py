# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 9:45 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : case_api.py
# @Software: PyCharm

from all_reference import *
from app.models.test_case.models import TestCase
from app.models.test_project.models import TestProjectVersion, MidProjectVersionAndCase
from app.models.test_case_assert.models import TestCaseDataAssBind


def check_method(current_method):
    """检查method"""
    if current_method.upper() in ['GET', 'POST', 'PUT', 'DELETE']:
        return current_method.upper()
    else:
        return False


p = [
    ("version_id_list", "版本迭代"),
    ("case_name", "用例名称"),
    ("request_method", "请求方式"),
    ("request_base_url", "base url"),
    ("request_url", "url")
]


def check_version(version_id_list):
    for version_obj in version_id_list:
        version_id = version_obj.get('id')
        if not TestProjectVersion.query.get(version_id):
            return False
    return True


class CaseApi(MethodView):
    """
    用例Api
    GET: 用例详情
    POST: 用例新增
    PUT: 用例编辑
    DELETE: 用例删除
    """

    def get(self, case_id):
        """用例详情"""

        result = query_case_zip(case_id=case_id)

        if not result:
            return api_result(code=400, message='用例id:{}不存在'.format(case_id))

        return api_result(code=200, message='操作成功', data=result)

    def post(self):
        """用例新增"""

        data = request.get_json()
        version_id_list = data.get('version_id_list', [])
        case_name = data.get('case_name')
        request_method = data.get('request_method')
        request_base_url = data.get('request_base_url')
        request_url = data.get('request_url')
        is_shared = data.get('is_shared', True)
        is_public = data.get('is_public', True)
        remark = data.get('remark')

        check_bool, check_msg = RequestParamKeysCheck(data, p).ck()
        if not check_bool:
            return api_result(code=400, message=check_msg)

        if not isinstance(version_id_list, list) or not version_id_list:
            return api_result(code=400, message='版本迭代不能为空')

        if not check_version(version_id_list):
            return api_result(code=400, message='版本迭代不存在')

        request_base_url = request_base_url.replace(" ", "")
        if not request_base_url:
            return api_result(code=400, message='环境不能为空')

        request_method_result = check_method(current_method=request_method)

        if not request_method_result:
            return api_result(code=400, message='请求方式:{} 不存在'.format(request_method))

        query_case = TestCase.query.filter_by(case_name=case_name).first()

        if query_case:
            return api_result(code=400, message='用例名称:{} 已经存在'.format(case_name))

        new_test_case = TestCase(
            case_name=case_name,
            request_method=request_method_result,
            request_base_url=request_base_url,
            request_url=request_url,
            is_shared=is_shared,
            is_public=is_public if isinstance(is_public, bool) else True,
            remark=remark,
            creator=g.app_user.username,
            creator_id=g.app_user.id,
        )
        new_test_case.save()
        case_id = new_test_case.id

        for version_obj in version_id_list:
            version_id = version_obj.get('id')
            new_mid = MidProjectVersionAndCase(
                version_id=version_id,
                case_id=case_id,
                creator=g.app_user.username,
                creator_id=g.app_user.id
            )
            db.session.add(new_mid)
        db.session.commit()

        data['id'] = case_id

        return api_result(code=201, message='创建成功', data=data)

    def put(self):
        """用例编辑"""

        data = request.get_json()
        version_id_list = data.get('version_id_list', [])
        case_id = data.get('id')
        case_name = data.get('case_name')
        request_method = data.get('request_method')
        request_base_url = data.get('request_base_url')
        request_url = data.get('request_url')
        is_shared = data.get('is_shared', True)
        is_public = data.get('is_public', True)
        remark = data.get('remark')

        check_bool, check_msg = RequestParamKeysCheck(data, p).ck()
        if not check_bool:
            return api_result(code=400, message=check_msg)

        if not isinstance(version_id_list, list) or not version_id_list:
            return api_result(code=400, message='版本迭代不能为空')

        if not check_version(version_id_list):
            return api_result(code=400, message='版本迭代不存在')

        request_base_url = request_base_url.replace(" ", "")
        if not request_base_url:
            return api_result(code=400, message='环境不能为空')

        query_case = TestCase.query.get(case_id)

        if not query_case:
            return api_result(code=400, message='用例id:{}数据不存在'.format(case_id))

        if not bool(is_public) and query_case.creator_id != g.app_user.id:
            return api_result(code=400, message='非创建人，无法修改使用状态')

        if not bool(is_shared) and query_case.creator_id != g.app_user.id:
            return api_result(code=400, message='非创建人，无法修改执行状态')

        if not bool(query_case.is_public):
            if query_case.creator_id != g.app_user.id:
                return api_result(code=400, message='该用例未开放,只能被创建人修改!')

        if query_case.case_name != case_name:
            if TestCase.query.filter_by(case_name=case_name).all():
                return api_result(code=400, message='用例名称:{} 已经存在'.format(case_name))

        query_case.case_name = case_name
        query_case.request_method = request_method
        query_case.request_base_url = request_base_url
        query_case.request_url = request_url
        query_case.is_shared = is_shared
        query_case.is_public = is_public if isinstance(is_public, bool) else True
        query_case.remark = remark
        query_case.modifier = g.app_user.username
        query_case.modifier_id = g.app_user.id

        new_version_id_list = [version_obj.get('id') for version_obj in version_id_list]

        query_mid_all = MidProjectVersionAndCase.query.filter_by(case_id=case_id).all()

        remain_list = []

        for q in query_mid_all:
            if q.version_id not in new_version_id_list:
                q.is_deleted = q.id
                q.modifier = g.app_user.username
                q.modifier_id = g.app_user.id
                q.remark = "源数据差集(逻辑删除)"
            else:
                remain_list.append(q.version_id)

        jj = ActionSet.gen_intersection(remain_list, new_version_id_list)
        cj = ActionSet.gen_difference(new_version_id_list, remain_list)

        for version_id in jj:  # 激活
            update_mid = MidProjectVersionAndCase.query.filter_by(version_id=version_id, case_id=case_id).first()
            update_mid.modifier = g.app_user.username
            update_mid.modifier_id = g.app_user.id
            update_mid.is_deleted = 0
            update_mid.remark = '交集(激活)'

        for version_id in cj:  # 创建新的
            new_mid = MidProjectVersionAndCase(
                version_id=version_id,
                case_id=case_id,
                creator=g.app_user.username,
                creator_id=g.app_user.id,
                remark="新数据差集(创建)"
            )
            db.session.add(new_mid)

        db.session.commit()

        return api_result(code=203, message='编辑成功')

    def delete(self):
        """用例删除"""

        data = request.get_json()
        case_id = data.get('id')

        query_case = TestCase.query.get(case_id)

        if not query_case:
            return api_result(code=400, message='用例id:{}数据不存在'.format(case_id))

        query_case.modifier = g.app_user.username
        query_case.modifier_id = g.app_user.id
        query_case.delete()
        return api_result(code=204, message='删除成功')


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
        case_id = data.get('case_id')
        case_name = data.get('case_name', '')
        creator_id = data.get('creator_id')
        is_deleted = data.get('is_deleted', False)
        page = data.get('page')
        size = data.get('size')

        # TODO 旧数据 version_id 为 0,后续去除
        if not version_id:
            query_version = TestProjectVersion.query.filter_by(project_id=project_id).all()
            version_id_tuple = tuple([version.id for version in query_version])
            version_id_list = (0,) + version_id_tuple if version_id_tuple else (0, 0)
        else:
            version_id_list = (0, version_id)

        limit = page_size(page=page, size=size)

        sql = f"""
        SELECT
            A.id,
            A.case_name,
            A.request_method,
            A.request_base_url,
            A.request_url,
            A.total_execution,
            A.creator,
            A.create_time,
            A.create_timestamp,
            A.modifier,
            A.update_time,
            A.update_timestamp
        FROM
            exile_test_case A
        WHERE
            EXISTS (
                SELECT
                    B.id, B.case_id, B.version_id
                FROM
                    exile_test_mid_version_case B
                WHERE
                    B.case_id = A.id 
                    AND B.is_deleted = 0
                    AND B.version_id in {version_id_list})
                {f'AND creator_id={creator_id}' if creator_id else ''}
                AND is_deleted = {is_deleted}
                AND case_name LIKE"%{case_name}%"
            ORDER BY
                A.create_timestamp DESC
            LIMIT {limit[0]},{limit[1]};
        """

        sql_count = f"""
        SELECT 
            COUNT(*)
        FROM
            exile_test_case A
        WHERE
            EXISTS (
                SELECT
                    B.id, B.case_id, B.version_id
                FROM
                    exile_test_mid_version_case B
                WHERE
                    B.case_id = A.id
                    AND B.is_deleted = 0 
                    AND B.version_id in {version_id_list})
                {f'AND creator_id={creator_id}' if creator_id else ''}
                AND is_deleted = {is_deleted}
                AND case_name LIKE"%{case_name}%";
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

        return api_result(code=200, message='操作成功', data=result_data)


class CaseCopyApi(MethodView):
    """
    用例复制Api
    POST: 用例复制
    """

    def post(self):
        """用例复制"""

        data = request.get_json()
        case_id = data.get('case_id')

        query_case = TestCase.query.get(case_id)

        if not query_case:
            return api_result(code=400, message='用例id:{}不存在'.format(case_id))

        new_test_case = TestCase(
            case_name=query_case.case_name,
            request_method=query_case.request_method,
            request_base_url=query_case.request_base_url,
            request_url=query_case.request_url,
            is_shared=query_case.is_shared,
            is_public=query_case.is_public,
            remark="用例: {}-{} 的复制".format(query_case.id, query_case.case_name),
            creator=g.app_user.username,
            creator_id=g.app_user.id,
        )
        new_test_case.save()
        new_test_case_id = new_test_case.id

        query_bind = TestCaseDataAssBind.query.filter_by(case_id=case_id, is_deleted=0).all()

        if query_bind:
            for index, d in enumerate(query_bind, 1):
                new_bind = TestCaseDataAssBind(
                    case_id=new_test_case_id,
                    data_id=d.data_id,
                    ass_resp_id_list=d.ass_resp_id_list,  # TODO 检查 ass_resp_id_list 中的 id 是否存在
                    ass_field_id_list=d.ass_field_id_list,  # TODO 检查 ass_field_id_list 中的 id 是否存在
                    creator=g.app_user.username,
                    creator_id=g.app_user.id,
                    remark="用例复制生成"
                )
                db.session.add(new_bind)

        query_mid = MidProjectVersionAndCase.query.filter_by(case_id=case_id, is_deleted=0).all()

        version_id_list = [mid.version_id for mid in query_mid]

        if version_id_list:
            for version_id in version_id_list:
                new_mid = MidProjectVersionAndCase(
                    case_id=new_test_case_id,
                    version_id=version_id,
                    creator=g.app_user.username,
                    creator_id=g.app_user.id,
                    remark="用例复制生成"
                )
                db.session.add(new_mid)

        db.session.commit()

        return api_result(code=200, message='操作成功')
