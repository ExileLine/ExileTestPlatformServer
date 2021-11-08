# -*- coding: utf-8 -*-
# @Time    : 2021/8/14 4:55 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : case_bind_api.py
# @Software: PyCharm

from all_reference import *
from app.models.test_case.models import TestCase, TestCaseData
from app.models.test_case_assert.models import TestCaseDataAssBind


class CaseBindApi(MethodView):
    """
    用例绑定-数据-断言-变量Api
    """

    def post(self):
        """用例绑定-数据-断言-变量(新增)"""

        data = request.get_json()
        case_id = data.get('case_id')
        data_list = data.get('data_list', [])

        query_case = TestCase.query.get(case_id)
        if not query_case:
            return api_result(code=400, message="用例: {} 不存在".format(case_id))

        if not data_list:
            return api_result(code=201, message="操作成功")

        # TODO 检查这些ID
        for d in data_list:
            case_bind = TestCaseDataAssBind(
                case_id=case_id,
                data_id=d.get('data_id'),
                ass_resp_id_list=d.get('ass_resp_id_list', []),
                ass_field_id_list=d.get('ass_field_id_list', []),
                creator=g.app_user.username,
                creator_id=g.app_user.id
            )
            case_bind.save()
        return api_result(code=201, message="操作成功")

    def put(self):
        """用例绑定-数据-断言-变量(编辑)"""
        data = request.get_json()
        case_id = data.get('case_id')
        data_list = data.get('data_list', [])

        if data_list:
            for d in data_list:
                data_id = d.get('data_id')
                query_bind = TestCaseDataAssBind.query.filter_by(case_id=case_id, data_id=data_id).first()

                if not query_bind:
                    new_bind = TestCaseDataAssBind(
                        case_id=case_id,
                        data_id=data_id,
                        ass_resp_id_list=d.get('ass_resp_id_list', []),
                        ass_field_id_list=d.get('ass_field_id_list', []),
                        creator=g.app_user.username,
                        creator_id=g.app_user.id
                    )
                    db.session.add(new_bind)
                else:
                    query_bind.ass_resp_id_list = d.get('ass_resp_id_list', [])
                    query_bind.ass_field_id_list = d.get('ass_field_id_list', [])
                    query_bind.modifier = g.app_user.username
                    query_bind.modifier_id = g.app_user.id

        else:

            query_bind = TestCaseDataAssBind.query.filter_by(case_id=case_id).all()
            for i in query_bind:
                i.is_deleted = i.id

        try:
            db.session.commit()
        except BaseException as e:
            db.session.rollback()

        return api_result(code=203, message="操作成功")


class CaseBindDataApi(MethodView):
    """
    用例配置数据Api
    """

    def post(self):
        """用例绑定数据"""

        data = request.get_json()
        case_id = data.get('case_id')
        data_id = data.get('data_id')

        query_case = TestCase.query.get(case_id)
        query_case_data = TestCaseData.query.get(data_id)

        if not query_case:
            return api_result(code=400, message='用例id不存在:{}'.format(case_id))

        if not query_case_data:
            return api_result(code=400, message='用例参数id不存在:{}'.format(data_id))

        query_bind = TestCaseDataAssBind.query.filter_by(case_id=case_id, data_id=data_id).first()

        if not query_bind:
            new_bind = TestCaseDataAssBind(
                case_id=case_id,
                data_id=data_id,
                creator=g.app_user.username,
                creator_id=g.app_user.id
            )
            db.session.add(new_bind)
            db.session.commit()
            return api_result(code=203, message='绑定成功')

        if query_bind.is_deleted == 0:
            return api_result(code=400, message='用例:{} 已经绑定:{}'.format(case_id, data_id))

        if query_bind.is_deleted != 0:
            query_bind.is_deleted = 0
            db.session.commit()
            return api_result(code=201, message='状态更新成功,绑定成功')

    def put(self):
        """用例数据解绑"""

        data = request.get_json()
        case_id = data.get('case_id')
        data_id = data.get('data_id')

        query_bind = TestCaseDataAssBind.query.filter_by(case_id=case_id, data_id=data_id).first()

        if not query_bind:
            return api_result(code=400, message='解除绑定失败:错误的case_id:{} 或 data_id:{}'.format(case_id, data_id))

        query_bind.is_deleted = query_bind.id
        query_bind.ass_resp_id_list = []
        query_bind.ass_field_id_list = []
        query_bind.modifier = g.app_user.username
        query_bind.modifier_id = g.app_user.id
        db.session.commit()
        return api_result(code=203, message='状态更新成功,解除绑定成功')


class CaseBindRespAssApi(MethodView):
    """Resp断言规则绑定"""

    def post(self):
        """Resp断言规则绑定"""

        data = request.get_json()
        bind_id = data.get('bind_id')
        ass_resp_ids = data.get('ass_resp_ids', [])

        if not isinstance(ass_resp_ids, list):
            return ab_code(400)

        query_bind = TestCaseDataAssBind.query.get(bind_id)

        if not query_bind:
            return api_result(code=400, message='bind_id:{}不存在'.format(bind_id))

        if query_bind.is_deleted != 0:
            return api_result(code=400, message='已删除is_deleted:{}'.format(query_bind.is_deleted))

        query_bind.ass_resp_id_list = ass_resp_ids
        query_bind.modifier = g.app_user.username
        query_bind.modifier_id = g.app_user.id
        db.session.commit()
        return api_result(code=201, message='Resp检验规则绑定成功')


class CaseBindFieldAssApi(MethodView):
    """Field断言规则绑定"""

    def post(self):
        """Field断言规则绑定"""

        data = request.get_json()
        bind_id = data.get('bind_id')
        ass_field_ids = data.get('ass_field_ids', [])

        if not isinstance(ass_field_ids, list):
            return ab_code(400)

        query_bind = TestCaseDataAssBind.query.get(bind_id)

        if not query_bind:
            return api_result(code=400, message='bind_id:{}不存在'.format(bind_id))

        if query_bind.is_deleted != 0:
            return api_result(code=400, message='已删除is_deleted:{}'.format(query_bind.is_deleted))

        query_bind.ass_field_id_list = ass_field_ids
        query_bind.modifier = g.app_user.username
        query_bind.modifier_id = g.app_user.id
        db.session.commit()
        return api_result(code=201, message='Field检验规则绑定成功')
