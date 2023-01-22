# -*- coding: utf-8 -*-
# @Time    : 2022/1/14 10:51 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : platform_conf_api.py
# @Software: PyCharm

from all_reference import *
from app.models.platform_conf.models import PlatformConfModel


class PlatformConfApi(MethodView):
    """
    平台配置Api
    GET: 获取平台配置
    POST: 新增平台配置
    """

    def get(self):
        """获取平台配置"""

        res = db.session.query(func.max(PlatformConfModel.weights)).one()
        query_platform_conf = PlatformConfModel.query.filter_by(weights=res[0]).first()
        result = query_platform_conf.to_json()
        return api_result(code=200, message=SUCCESS_MESSAGE, data=result)

    # def post(self):
    #     """新增平台配置"""
    #
    #     data = request.get_json()
    #     platform_icon = data.get('platform_icon')
    #     platform_name = data.get('platform_name')
    #     platform_login_msg = data.get('platform_login_msg')
    #     weights = data.get('weights')
    #     remark = data.get('remark')
    #
    #     if PlatformConfModel.query.filter_by(platform_name=platform_name).first():
    #         return api_result(code=400, message='平台名称已经存在')
    #
    #     new_platform_conf = PlatformConfModel(
    #         platform_icon=platform_icon,
    #         platform_name=platform_name,
    #         platform_login_msg=platform_login_msg,
    #         weights=weights,
    #         remark=remark
    #     )
    #
    #     new_platform_conf.save()
    #     return api_result(code=201, message=SUCCESS_MESSAGE)
