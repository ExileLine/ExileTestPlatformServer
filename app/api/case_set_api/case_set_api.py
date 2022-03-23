# -*- coding: utf-8 -*-
# @Time    : 2021/10/29 7:18 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : case_set_api.py
# @Software: PyCharm


from all_reference import *
from app.models.test_case_set.models import TestCaseSet

set_type_tuple = ("case", "scenario")


class CaseSetApi(MethodView):
    """
    用例收藏Api
    POST: 用例收藏
    """

    def post(self):
        """用例收藏"""

        data = request.get_json()
        set_id = data.get('set_id')
        set_type = data.get('set_type')
        is_set = data.get('is_set')

        if set_type not in set_type_tuple:
            return api_result(code=400, message=f'类型错误: {set_type}')

        __key = f"{set_type}_id"

        query_set = TestCaseSet.query.filter(getattr(TestCaseSet, __key) == set_id).first()
        if query_set:
            query_set.is_set = is_set
            query_set.modifier = g.app_user.username
            query_set.modifier_id = g.app_user.id
            db.session.commit()
        else:
            new_set = TestCaseSet()
            setattr(new_set, __key, set_id)
            new_set.user_id = g.app_user.id
            new_set.is_set = is_set
            new_set.creator = g.app_user.username
            new_set.creator_id = g.app_user.id
            new_set.save()

        return api_result(code=200, message='操作成功')
