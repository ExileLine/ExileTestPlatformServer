# -*- coding: utf-8 -*-
# @Time    : 2021/10/14 10:15 上午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : case_report_api.py
# @Software: PyCharm


from all_reference import *
from app.models.test_logs.models import TestExecuteLogs


class CaseRepostApi(MethodView):
    """
    生成测试报告
    """

    def post(self):
        """生成测试报告"""
        data = request.get_json()
        log_id = data.get('log_id')
        query_t_e_l = TestExecuteLogs.query.get(log_id)
        if not query_t_e_l:
            return api_result(code=400, message="id:{} 日志丢失,生成测试报告失败".format(log_id))

        redis_key = query_t_e_l.to_json().get('redis_key')
        redis_val = R.get(redis_key)

        if not redis_val:
            return api_result(code=400, message="key:{} 日志丢失,生成测试报告失败".format(redis_key))

        # TODO vue 模板渲染
        return api_result(code=200, message="操作成功", data=json.loads(redis_val))
