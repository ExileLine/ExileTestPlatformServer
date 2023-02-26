# -*- coding: utf-8 -*-
# @Time    : 2023/2/25 19:27
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : ui_control_dict_api.py
# @Software: PyCharm


from all_reference import *


class UiControlDictApi(MethodView):
    """
    UI控件字典Api
    GET: 获取UI控件字典
    POST: 获取UI控件字典
    """

    def get(self):
        """获取UI控件字典"""

        ucd = UiControlDict.get_ucd()
        return api_result(code=SUCCESS, message=SUCCESS_MESSAGE, data=ucd)

    def post(self):
        """获取UI控件字典"""

        ucd = UiControlDict.get_ucd()
        return api_result(code=SUCCESS, message=POST_MESSAGE, data=ucd)
