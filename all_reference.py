# -*- coding: utf-8 -*-
# @Time    : 2021/5/11 下午4:33
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : all_reference.py
# @Software: PyCharm

import os
import re
import json
import copy
import time
import datetime
import threading
from functools import wraps

import requests
import shortuuid
from loguru import logger
from sqlalchemy import or_, and_, func
from flask.views import MethodView
from flask import abort, render_template, request, g

from ExtendRegister.db_register import db
from common.libs.data_dict import GlobalsDict, expect_val_type_dict, rule_dict, execute_type_tuple, UiControlDict
from common.libs.db import project_db, R
from common.libs.api_result import *
from common.libs.response_code import *
from common.libs.set_app_context import set_app_context
from common.libs.customException import method_view_ab_code as ab_code
from common.libs.customException import flask_restful_ab_code as ab_code_2
from common.libs.public_func import check_keys, json_format, timer, RequestParamKeysCheck, ActionSet, gen_request_dict, \
    TimeTool
from common.libs.auth import Token, AdminRefreshCache
from common.libs.query_related import page_size, general_query, query_case_assemble, MapToJsonObj
from common.libs.execute_code import execute_code