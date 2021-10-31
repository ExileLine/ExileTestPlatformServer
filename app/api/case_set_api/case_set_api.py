# -*- coding: utf-8 -*-
# @Time    : 2021/10/29 7:18 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : case_set_api.py
# @Software: PyCharm


from all_reference import *
from app.models.admin.models import Admin
from app.models.test_case_set.models import TestCaseSet


def func(x):
    try:
        return int(x)
    except BaseException:
        return ab_code(400)


class CaseSetApi(MethodView):
    """
    用户用例收藏列表Api
    POST: 更新收藏列表
    """

    def post(self):
        """更新收藏列表"""

        data = request.get_json()
        user_id = data.get('user_id', 0)
        case_id_list = data.get('case_id_list', [])
        scenario_id_list = data.get('scenario_id_list', [])

        if not check_keys(data, "user_id", "case_id_list") or not isinstance(case_id_list, list) or not isinstance(
                scenario_id_list, list):
            return ab_code(400)

        user = Admin.query.get(user_id)
        case_id_list = list(map(func, case_id_list))
        scenario_id_list = list(map(func, scenario_id_list))

        if not user:
            return api_result(code=400, message="用户不存在:{}".format(user_id))

        query_case_set = TestCaseSet.query.filter_by(user_id=user_id).first()

        if query_case_set:
            query_case_set.case_id_list = case_id_list
            query_case_set.scenario_id_list = scenario_id_list
            query_case_set.modifier = g.app_user.username
            query_case_set.modifier_id = g.app_user.id
            db.session.commit()
        else:
            case_set = TestCaseSet(
                user_id=user_id,
                case_id_list=case_id_list,
                scenario_id_list=scenario_id_list,
                creator=g.app_user.username,
                creator_id=g.app_user.id
            )
            case_set.save()
        return api_result(code=200, message='操作成功')
