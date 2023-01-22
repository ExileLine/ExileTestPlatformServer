# -*- coding: utf-8 -*-
# @Time    : 2021/7/24 1:15 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : case_assertion_api.py
# @Software: PyCharm

from all_reference import *
from app.api.project_api.project_api import qp
from app.models.test_case_assert.models import TestCaseAssertion
from app.models.test_case_db.models import TestDatabases


class CheckAssertion:
    """检验断言规则"""

    @classmethod
    def ref_variable(cls, var):
        """
        判断是否引用变量(${xxx})
        :param var:
        :return:
        """

        if not isinstance(var, str):
            return False

        if var[0:2] == "${" and var[-1] == "}":
            return True
        return False

    @classmethod
    def convert_variable(cls, val, val_type, func):
        """
        校验参数是否能被转换
        :param val:
        :param val_type:
        :param func:
        :return:
        """
        try:
            print(val, val_type, func)
            print(func(val))
            return True
        except BaseException as e:
            return False

    @classmethod
    def check_ass_json(cls, ass, assertion_type=None):
        """
        校验响应断言规则参数格式
        :param ass:
        :param assertion_type:
        :return:
        """

        ass['uuid'] = f"{shortuuid.uuid()}-{int(time.time())}"

        if assertion_type == "response":
            resp_source = ass.get('response_source')
            if resp_source not in GlobalsDict.resp_source_tuple():
                return False, f'参数来源错误:{resp_source}'

        rule = ass.get('rule')  # ==,>,< ...
        if not GlobalsDict.rule_dict_op().get(rule):
            return False, f"规则: {current_rule} 不存在"

        is_expression = ass.get('is_expression')  # True,False
        if not isinstance(is_expression, bool):
            return False, f'表达式标识错误:{is_expression}'

        expect_val = ass.get('expect_val')
        expect_val_type = ass.get('expect_val_type')  # int,str,bool ...
        expect_val_type_func = GlobalsDict.value_type_dict().get(expect_val_type)
        if not expect_val_type_func:
            return False, f'类型: {expect_val_type} 错误'
        else:
            expect_val = str(expect_val).strip()
            if not cls.ref_variable(expect_val):
                if not cls.convert_variable(val=expect_val, val_type=expect_val_type, func=expect_val_type_func):
                    return False, f'参数: {expect_val} 无法转换至类型: {expect_val_type}'
            return True, ass

    @classmethod
    def check_query(cls, db_type, query):
        """
        检验语句防止删除语句
        :param db_type:
        :param query:
        :return:
        """
        if db_type.lower() == 'mysql':
            pattern = r"\b(exec|insert|drop|grant|alter|delete|update|count|chr|mid|master|truncate|char|delclare)\b|(\*)"
            result = re.search(pattern, query.lower())
            if result:
                print(result.group())
                return True

        elif db_type.lower() == 'redis':
            pattern = r"\b(del|delete|unlink|flushdb|flushall)\b|(\*)"
            result = re.search(pattern, query.lower())
            if result:
                print(result.group())
                return True
        else:
            return False


def assertion_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = request.get_json()
        project_id = data.get('project_id')
        if not qp(project_id):
            return api_result(code=NO_DATA, message=f"项目id: {project_id} 不存在")

        assert_description = data.get('assert_description')
        if not assert_description or assert_description == '':
            return api_result(code=REQUIRED, message='断言描述不能为空')

        ass_json = data.get('ass_json', [])
        if not isinstance(ass_json, list) or not ass_json:
            return api_result(code=TYPE_ERROR, message='断言规则不能为空')

        return func(*args, **kwargs)

    return wrapper


class RespAssertionRuleApi(MethodView):
    """
    响应断言规则Api
    GET: 响应断言规则明细
    POST: 响应断言规则新增
    PUT: 响应断言规则编辑
    DELETE: 响应断言规则删除

    请求例子
    {
        "assert_description": "Resp通用断言",
        "remark": "remark",
        "ass_json": [
            {

                "response_source":"body",
                "assert_key": "code",
                "expect_val": "200",
                "expect_val_type": "int",
                "rule": "==",
                "is_expression": 0,
                "python_val_exp": "okc.get('a').get('b').get('c')[0]"
            },
            {
                "response_source":"headers",
                "assert_key": "code",
                "expect_val": "200",
                "expect_val_type": "str",
                "rule": ">=",
                "is_expression": 0,
                "python_val_exp": "okc.get('a').get('b').get('c')[0]"
            }
            ...
        ]
    }

    ass_json:
        :response_source: 返回值来源(body or headers)
        :assert_key: 返回值的键(用于简单取值)
        :expect_val: 期望值
        :expect_val_type: 期望值类型
        :rule: 规则
        :is_expression: 是否使用取值公式
        :python_val_exp: python取值公式

    """

    def get(self, ass_resp_id):
        """响应断言规则明细"""

        query_ass_resp = TestCaseAssertion.query.get(ass_resp_id)

        if not query_ass_resp:
            return api_result(code=NO_DATA, message='响应断言规则不存在')
        result = query_ass_resp.to_json()
        return api_result(code=SUCCESS, message=SUCCESS_MESSAGE, data=result)

    @assertion_decorator
    def post(self):
        """响应断言规则新增"""

        data = request.get_json()
        project_id = data.get('project_id')
        assert_description = data.get('assert_description')
        ass_json = data.get('ass_json', [])
        is_public = data.get('is_public')
        remark = data.get('remark')

        for ass in ass_json:
            check_bool = check_keys(
                ass, 'assert_key', 'expect_val_type', 'expect_val', 'rule', 'is_expression', 'python_val_exp',
                'response_source'
            )
            if not check_bool:
                return api_result(code=BUSINESS_ERROR, message='检验对象错误', data=a)

            result_bool, result = CheckAssertion.check_ass_json(ass=ass, assertion_type='response')
            if not result_bool:
                return api_result(code=BUSINESS_ERROR, message=result)

        new_ass_resp = TestCaseAssertion(
            project_id=project_id,
            assert_description=assert_description,
            ass_json=ass_json,
            assertion_type="response",
            creator=g.app_user.username,
            creator_id=g.app_user.id,
            remark=remark
        )
        new_ass_resp.is_public = is_public
        new_ass_resp.save()
        return api_result(code=POST_SUCCESS, message=POST_MESSAGE, data=new_ass_resp.to_json())

    @assertion_decorator
    def put(self):
        """响应断言规则编辑"""

        data = request.get_json()
        ass_resp_id = data.get('id')
        assert_description = data.get('assert_description')
        ass_json = data.get('ass_json', [])
        is_public = data.get('is_public')
        remark = data.get('remark')

        query_ass_resp = TestCaseAssertion.query.get(ass_resp_id)

        if not query_ass_resp:
            return api_result(code=NO_DATA, message='断言规则不存在')

        if not bool(is_public) and query_ass_resp.creator_id != g.app_user.id:
            return api_result(code=BUSINESS_ERROR, message='非创建人，无法修改使用状态')

        if not bool(query_ass_resp.is_public):
            if query_ass_resp.creator_id != g.app_user.id:
                return api_result(code=BUSINESS_ERROR, message='该断言规则未开放,只能被创建人修改!')

        for ass in ass_json:
            check_bool = check_keys(
                ass, 'assert_key', 'expect_val_type', 'expect_val', 'rule', 'is_expression', 'python_val_exp',
                'response_source'
            )

            if not check_bool:
                return api_result(code=BUSINESS_ERROR, message='请求参数错误')

            result_bool, result = CheckAssertion.check_ass_json(ass=ass, assertion_type='response')
            if not result_bool:
                return api_result(code=BUSINESS_ERROR, message=result)

        query_ass_resp.assert_description = assert_description
        query_ass_resp.ass_json = ass_json
        query_ass_resp.is_public = is_public
        query_ass_resp.remark = remark
        query_ass_resp.modifier = g.app_user.username
        query_ass_resp.modifier_id = g.app_user.id
        db.session.commit()

        return api_result(code=PUT_SUCCESS, message='编辑成功', data=query_ass_resp.to_json())

    def delete(self):
        """响应断言规则删除"""

        data = request.get_json()
        ass_resp_id = data.get('id')
        query_ass_resp = TestCaseAssertion.query.get(ass_resp_id)

        if not query_ass_resp:
            return api_result(code=NO_DATA, message='响应断言规则不存在')

        if query_ass_resp.creator_id != g.app_user.id:
            return api_result(code=BUSINESS_ERROR, message='非管理员不能删除其他人的断言！')

        query_ass_resp.modifier_id = g.app_user.id
        query_ass_resp.modifier = g.app_user.username
        query_ass_resp.delete()
        return api_result(code=DEL_SUCCESS, message='删除成功')


class FieldAssertionRuleApi(MethodView):
    """
    字段断言规则Api
    GET: 字段断言规则明细
    POST: 字段断言规则新增
    PUT: 字段断言规则编辑
    DELETE: 字段断言规则删除

    请求例子
    {
        "assert_description": "A通用字段校验",
        "remark": "remark",
        "ass_json": [
            {
                "db_id": 1,
                "query": "select id FROM exile_test_case WHERE id=1;",
                "assert_list": [
                    {
                        "assert_key": "id",
                        "expect_val": 1,
                        "expect_val_type": "1",
                        "rule": "=="
                    },
                    {
                        "assert_key": "case_name",
                        "expect_val": "测试用例B1",
                        "expect_val_type": "2",
                        "rule": "=="
                    }
                ]
            }
        ]
    }

    assert_list:
        :assert_key: 键(用于简单取值)
        :expect_val: 期望值
        :expect_val_type: 期望值类型
        :rule: 规则

    """

    def get(self, ass_field_id):
        """字段断言规则明细"""

        query_ass_field = TestCaseAssertion.query.get(ass_field_id)

        if not query_ass_field:
            return api_result(code=NO_DATA, message='字段断言规则不存在')
        result = query_ass_field.to_json()
        return api_result(code=SUCCESS, message=SUCCESS_MESSAGE, data=result)

    @assertion_decorator
    def post(self):
        """字段断言规则新增"""

        data = request.get_json()
        project_id = data.get('project_id')
        version_id_list = data.get('version_id_list')
        assert_description = data.get('assert_description')
        ass_json = data.get('ass_json', [])
        is_public = data.get('is_public')
        remark = data.get('remark')

        for ass_obj in ass_json:

            db_id = ass_obj.get('db_id')
            query_db = TestDatabases.query.get(db_id)
            if not query_db:
                return api_result(code=NO_DATA, message=f'数据库: {db_id} 不存在')

            if query_db.is_deleted:
                return api_result(code=BUSINESS_ERROR, message=f'数据库: {query_db.name} 被禁用')

            assert_list = ass_obj.get('assert_list')
            for ass in assert_list:
                query = ass.get('query')
                assert_field_list = ass.get('assert_field_list')

                db_type = query_db.db_type
                check_query_result = CheckAssertion.check_query(db_type=db_type, query=query)
                if check_query_result:
                    return api_result(code=BUSINESS_ERROR, message='只能使用查询相关的语句或命令')

                for a in assert_field_list:
                    result_bool, result = CheckAssertion.check_ass_json(ass=a)
                    if not result_bool:
                        return api_result(code=BUSINESS_ERROR, message=result)

        new_ass_field = TestCaseAssertion(
            project_id=project_id,
            assert_description=assert_description,
            ass_json=ass_json,
            is_public=is_public,
            assertion_type="field",
            creator=g.app_user.username,
            creator_id=g.app_user.id,
            remark=remark
        )
        new_ass_field.save()
        return api_result(code=POST_SUCCESS, message=POST_MESSAGE, data=new_ass_field.to_json())

    @assertion_decorator
    def put(self):
        """字段断言规则编辑"""

        data = request.get_json()
        ass_field_id = data.get('id')
        version_id_list = data.get('version_id_list')
        assert_description = data.get('assert_description')
        ass_json = data.get('ass_json', [])
        is_public = data.get('is_public')
        remark = data.get('remark')

        query_ass_field = TestCaseAssertion.query.get(ass_field_id)

        if not query_ass_field:
            return api_result(code=NO_DATA, message='字段断言规则不存在')

        if not bool(is_public) and query_ass_field.creator_id != g.app_user.id:
            return api_result(code=BUSINESS_ERROR, message='非创建人，无法修改使用状态')

        if not query_ass_field.is_public:
            if query_ass_field.creator_id != g.app_user.id:
                return api_result(code=BUSINESS_ERROR, message='该字段断言规则未开放,只能被创建人修改!')

        for ass_obj in ass_json:

            db_id = ass_obj.get('db_id')
            query_db = TestDatabases.query.get(db_id)
            if not query_db:
                return api_result(code=NO_DATA, message=f'数据库: {db_id} 不存在')

            if query_db.is_deleted:
                return api_result(code=BUSINESS_ERROR, message=f'数据库: {query_db.name} 被禁用')

            assert_list = ass_obj.get('assert_list')
            for ass in assert_list:
                query = ass.get('query')
                assert_field_list = ass.get('assert_field_list')

                db_type = query_db.db_type
                check_query_result = CheckAssertion.check_query(db_type=db_type, query=query)
                if check_query_result:
                    return api_result(code=BUSINESS_ERROR, message='只能使用查询相关的语句或命令')

                for a in assert_field_list:
                    result_bool, result = CheckAssertion.check_ass_json(ass=a)
                    if not result_bool:
                        return api_result(code=BUSINESS_ERROR, message=result)

        query_ass_field.assert_description = assert_description
        query_ass_field.ass_json = ass_json
        query_ass_field.is_public = is_public
        query_ass_field.remark = remark
        query_ass_field.modifier = g.app_user.username
        query_ass_field.modifier_id = g.app_user.id
        db.session.commit()
        return api_result(code=PUT_SUCCESS, message='编辑成功', data=query_ass_field.to_json())

    def delete(self):
        """字段断言规则删除"""

        data = request.get_json()
        ass_field_id = data.get('id')
        query_ass_field = TestCaseAssertion.query.get(ass_field_id)

        if not query_ass_field:
            return api_result(code=NO_DATA, message='字段断言规则不存在')

        if query_ass_field.creator_id != g.app_user.id:
            return api_result(code=BUSINESS_ERROR, message='非管理员不能删除其他人的断言！')

        query_ass_field.modifier_id = g.app_user.id
        query_ass_field.modifier = g.app_user.username
        query_ass_field.delete()
        return api_result(code=DEL_SUCCESS, message='删除成功')


class AssertionRulePageApi(MethodView):
    """
    assertion rule page api
    POST: 断言规则分页模糊查询
    """

    def post(self):
        """断言规则分页模糊查询"""

        data = request.get_json()
        project_id = data.get('project_id')
        assertion_id = data.get('id')
        assert_description = data.get('assert_description')
        assertion_type = data.get('assertion_type')
        is_deleted = data.get('is_deleted', 0)
        creator_id = data.get('creator_id')
        page = data.get('page')
        size = data.get('size')

        if assertion_type not in ("response", "field"):
            return api_result(code=BUSINESS_ERROR, message=f'断言类型不存在:{assertion_type}')

        where_dict = {
            "project_id": project_id,
            "id": assertion_id,
            "is_deleted": is_deleted,
            "assertion_type": assertion_type,
            "creator_id": creator_id
        }

        result_data = general_query(
            model=TestCaseAssertion,
            field_list=['assert_description'],
            query_list=[assert_description],
            where_dict=where_dict,
            page=page,
            size=size
        )
        return api_result(code=SUCCESS, message=SUCCESS_MESSAGE, data=result_data)
