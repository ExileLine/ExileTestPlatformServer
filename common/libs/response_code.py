# -*- coding: utf-8 -*-
# @Time    : 2023/1/22 23:35
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : response_code.py
# @Software: PyCharm


SUCCESS, SUCCESS_MESSAGE = 200, "操作成功"
POST_SUCCESS, POST_MESSAGE = 201, "创建成功"
PUT_SUCCESS, PUT_MESSAGE = 203, "编辑成功"
DEL_SUCCESS, DEL_MESSAGE = 204, "删除成功"

Unauthorized = 401  # 未授权

REQUIRED = 10001  # 必传
NO_DATA = 10002  # 未找到
UNIQUE_ERROR = 10003  # 唯一校验
TYPE_ERROR = 10004  # 类型错误
BUSINESS_ERROR = 10005  # 业务校验错误
DATA_ERROR = 10006  # 请求参数错误
