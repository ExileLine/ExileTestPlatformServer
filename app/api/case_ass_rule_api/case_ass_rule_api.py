# -*- coding: utf-8 -*-
# @Time    : 2021/7/24 1:15 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : case_ass_rule_api.py
# @Software: PyCharm

from all_reference import *
from app.models.test_case_assert.models import TestCaseAssResponse, TestCaseAssField
from app.models.test_case_db.models import TestDatabases


def gen_new_ass(ass_obj):
    """
    {
        "assert_key": "id",
        "expect_val": "1",
        "expect_val_type": "1",
        "is_expression": 1,
        "python_val_exp": "obj.get('id')",
        "rule": "=="
    }
    :param ass_obj:
    :return:
    """

    expect_val = ass_obj.get('expect_val')
    check_expect_val = str(expect_val).strip()
    if check_expect_val[0:2] == "${" and check_expect_val[-1] == "}":
        return ass_obj

    con_bool, new_expect_val = type_conversion(
        type_key=ass_obj.get('expect_val_type'),
        val=ass_obj.get('expect_val'),
        type_dict='ass'
    )

    if not con_bool:
        return False

    ass_obj['expect_val'] = new_expect_val

    return ass_obj


def check_query(db_type, query):
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


class RespAssertionRuleApi(MethodView):
    """
    返回值断言规则Api
    GET: 断言规则详情
    POST: 断言规则新增
    PUT: 断言规则编辑
    DELETE: 断言规则删除

    req_demo = {
        "assert_description": "Resp通用断言123",
        "remark": "remark",
        "ass_json": [
            {

                "resp_source":"body",
                "assert_key": "code",
                "expect_val": "200",
                "expect_val_type": "1",
                "rule": "==",
                "is_expression": 0,
                "python_val_exp": "okc.get('a').get('b').get('c')[0]"
            },
            {
                "resp_source":"headers",
                "assert_key": "code",
                "expect_val": "200",
                "expect_val_type": "1",
                "rule": ">=",
                "is_expression": 0,
                "python_val_exp": "okc.get('a').get('b').get('c')[0]"
            },
            {
                "resp_source":"headers",
                "assert_key": "message",
                "expect_val": "index",
                "expect_val_type": "2",
                "rule": "==",
                "is_expression": 0,
                "python_val_exp": "okc.get('a').get('b').get('c')[0]"
            }
        ]
    }

    ass_json:
        :resp_source: 返回值来源(body or headers)
        :assert_key: 返回值的键(用于简单取值)
        :expect_val: 期望值
        :expect_val_type: 期望值类型
        :rule: 规则
        :is_expression: 是否使用取值公式
        :python_val_exp: python取值公式

    """

    def get(self, ass_resp_id):
        """返回值断言明细"""

        query_ass_resp = TestCaseAssResponse.query.get(ass_resp_id)

        if not query_ass_resp:
            return api_result(code=400, message='返回值断言id:{}数据不存在'.format(ass_resp_id))

        return api_result(code=200, message='操作成功', data=query_ass_resp.to_json())

    def post(self):
        """返回值断言新增"""

        data = request.get_json()
        assert_description = data.get('assert_description')
        ass_json = data.get('ass_json', [])
        is_public = data.get('is_public', 1)
        remark = data.get('remark')

        if not assert_description or assert_description == '':
            return api_result(code=400, message='断言描述不能为空')

        if not isinstance(ass_json, list) or not ass_json:
            return ab_code(400)

        new_ass_json = []

        for a in ass_json:
            check_bool = check_keys(
                a, 'assert_key', 'expect_val_type', 'expect_val', 'rule', 'is_expression', 'python_val_exp',
                'response_source'
            )
            if not check_bool:
                return api_result(code=400, message='检验对象错误', data=a)

            rule = rule_dict.get(a.get('rule'))

            resp_source = a.get('response_source')

            if resp_source not in resp_source_tuple:
                return api_result(code=400, message='来源参数错误:{}'.format(resp_source))

            if not rule:
                return api_result(code=400, message='规则参数错误:{}'.format(a.get('rule')))

            is_expression = a.get('is_expression')
            is_rule_source_bool = bool(str(is_expression) in ['0', '1'])

            if not is_rule_source_bool:
                return api_result(code=400, message='规则参数错误:{}'.format(is_expression))

            expect_val = a.get('expect_val')
            expect_val_type = expect_val_type_dict.get(str(a.get('expect_val_type')))

            try:
                check_expect_val = str(expect_val).strip()
                if check_expect_val[0:2] == "${" and check_expect_val[-1] == "}":
                    new_ass_json.append(a)
                else:
                    # a['rule'] = rule
                    a['expect_val'] = expect_val_type(expect_val)  # 类型转换
                    new_ass_json.append(a)
            except BaseException as e:
                return api_result(code=400, message='参数:{} 无法转换至 类型:{}'.format(expect_val, type(expect_val_type())))

        new_ass_resp = TestCaseAssResponse(
            assert_description=assert_description,
            ass_json=new_ass_json,
            is_public=is_public,
            creator=g.app_user.username,
            creator_id=g.app_user.id,
            remark=remark
        )
        new_ass_resp.save()
        return api_result(code=201, message='创建成功', data=data)

    def put(self):
        """返回值断言编辑"""

        data = request.get_json()
        ass_resp_id = data.get('id')
        assert_description = data.get('assert_description')
        ass_json = data.get('ass_json', [])
        is_public = data.get('is_public', 1)
        remark = data.get('remark')

        query_ass_resp = TestCaseAssResponse.query.get(ass_resp_id)

        if not query_ass_resp:
            return api_result(code=400, message='返回值断言id:{}数据不存在'.format(ass_resp_id))

        if not assert_description or assert_description == '':
            return api_result(code=400, message='断言描述不能为空')

        if not bool(is_public) and query_ass_resp.creator_id != g.app_user.id:
            return api_result(code=400, message='非创建人，无法修改使用状态')

        if not bool(query_ass_resp.is_public):
            if query_ass_resp.creator_id != g.app_user.id:
                return api_result(code=400, message='该Resp断言规则未开放,只能被创建人修改!')

        if not isinstance(ass_json, list) or not ass_json:
            return ab_code(400)

        new_ass_json = []

        for a in ass_json:
            check_bool = check_keys(
                a, 'assert_key', 'expect_val_type', 'expect_val', 'rule', 'is_expression', 'python_val_exp',
                'response_source'
            )
            if not check_bool:
                return api_result(code=400, message='请求参数错误')

            rule = rule_dict.get(a.get('rule'))

            resp_source = a.get('response_source')

            if resp_source not in resp_source_tuple:
                return api_result(code=400, message='来源参数错误:{}'.format(resp_source))

            if not rule:
                return api_result(code=400, message='规则参数错误:{}'.format(a.get('rule')))

            is_expression = a.get('is_expression')
            is_rule_source_bool = bool(str(is_expression) in ['0', '1'])

            if not is_rule_source_bool:
                return api_result(code=400, message='规则参数错误:{}'.format(is_expression))

            expect_val = a.get('expect_val')
            expect_val_type = a.get('expect_val_type')
            expect_val_type_func = expect_val_type_dict.get(str(expect_val_type))

            try:
                check_expect_val = str(expect_val).strip()
                if check_expect_val[0:2] == "${" and check_expect_val[-1] == "}":
                    new_ass_json.append(a)
                else:
                    # a['rule'] = rule
                    a['expect_val'] = expect_val_type_func(expect_val)
                    new_ass_json.append(a)
            except BaseException as e:
                return api_result(code=400,
                                  message='参数:{} 无法转换至 类型:{}'.format(expect_val, type(expect_val_type_func())))

        query_ass_resp.assert_description = assert_description
        query_ass_resp.ass_json = new_ass_json
        query_ass_resp.is_public = is_public
        query_ass_resp.remark = remark
        query_ass_resp.modifier = g.app_user.username
        query_ass_resp.modifier_id = g.app_user.id
        db.session.commit()

        return api_result(code=203, message='编辑成功')

    def delete(self):
        """返回值断言删除"""

        data = request.get_json()
        ass_resp_id = data.get('id')
        query_ass_resp = TestCaseAssResponse.query.get(ass_resp_id)

        if not query_ass_resp:
            return api_result(code=400, message='返回值断言id:{}数据不存在'.format(ass_resp_id))

        if query_ass_resp.creator_id != g.app_user.id:
            return api_result(code=400, message='非管理员不能删除其他人的断言！')

        query_ass_resp.modifier_id = g.app_user.id
        query_ass_resp.modifier = g.app_user.username
        query_ass_resp.delete()
        return api_result(code=204, message='删除成功')


class FieldAssertionRuleApi(MethodView):
    """
    字段断言规则Api
    GET: 断言规则详情
    POST: 断言规则新增
    PUT: 断言规则编辑
    DELETE: 断言规则删除

    req_demo = {
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
        """字段断言明细"""

        query_ass_field = TestCaseAssField.query.get(ass_field_id)

        if not query_ass_field:
            return api_result(code=400, message='字段断言id:{}数据不存在'.format(ass_field_id))

        return api_result(code=200, message='操作成功', data=query_ass_field.to_json())

    def post(self):
        """字段断言新增"""

        data = request.get_json()
        version_id_list = data.get('version_id_list')
        assert_description = data.get('assert_description')
        ass_json = data.get('ass_json', [])
        is_public = data.get('is_public', 1)
        remark = data.get('remark')

        for ass_obj in ass_json:
            db_id = ass_obj.get('db_id')
            assert_list = ass_obj.get('assert_list')

            query_db = TestDatabases.query.get(db_id)
            if not query_db or query_db.is_deleted:
                return api_result(code=400, message=f'数据库不存在或被禁用: {db_id}')

            for ass in assert_list:
                query = ass.get('query')
                assert_field_list = ass.get('assert_field_list')

                db_type = query_db.db_type
                check_query_result = check_query(db_type=db_type, query=query)
                if check_query_result:
                    return api_result(code=400, message='只能使用查询相关的语句或命令')

                new_assert_field_list = list(map(gen_new_ass, assert_field_list))
                if False in new_assert_field_list:
                    return api_result(code=400, message="期望值无法转换至类型，请检查")
                ass['assert_field_list'] = new_assert_field_list

        new_ass_field = TestCaseAssField(
            assert_description=assert_description,
            ass_json=ass_json,
            is_public=is_public,
            creator=g.app_user.username,
            creator_id=g.app_user.id,
            remark=remark
        )
        new_ass_field.save()
        return api_result(code=201, message='创建成功', data=ass_json)

    def put(self):
        """字段断言编辑"""

        data = request.get_json()
        ass_field_id = data.get('id')
        version_id_list = data.get('version_id_list')
        assert_description = data.get('assert_description')
        ass_json = data.get('ass_json', [])
        is_public = data.get('is_public', 1)
        remark = data.get('remark')

        query_ass_field = TestCaseAssField.query.get(ass_field_id)

        if not query_ass_field:
            return api_result(code=400, message='字段断言id:{}数据不存在'.format(ass_field_id))

        if not bool(is_public) and query_ass_field.creator_id != g.app_user.id:
            return api_result(code=400, message='非创建人，无法修改使用状态')

        if not bool(query_ass_field.is_public):
            if query_ass_field.creator_id != g.app_user.id:
                return api_result(code=400, message='该字段断言规则未开放,只能被创建人修改!')

        if not isinstance(ass_json, list) or not ass_json:
            return ab_code(400)

        for ass_obj in ass_json:
            db_id = ass_obj.get('db_id')
            assert_list = ass_obj.get('assert_list')

            query_db = TestDatabases.query.get(db_id)
            if not query_db or query_db.is_deleted:
                return api_result(code=400, message=f'数据库不存在或被禁用: {db_id}')

            for ass in assert_list:
                query = ass.get('query')
                assert_field_list = ass.get('assert_field_list')

                db_type = query_db.db_type
                check_query_result = check_query(db_type=db_type, query=query)
                if check_query_result:
                    return api_result(code=400, message='只能使用查询相关的语句或命令')

                new_assert_field_list = list(map(gen_new_ass, assert_field_list))
                if False in new_assert_field_list:
                    return api_result(code=400, message="期望值无法转换至类型，请检查")
                ass['assert_field_list'] = new_assert_field_list

        query_ass_field.assert_description = assert_description
        query_ass_field.ass_json = ass_json
        query_ass_field.is_public = is_public
        query_ass_field.remark = remark
        query_ass_field.modifier = g.app_user.username
        query_ass_field.modifier_id = g.app_user.id
        db.session.commit()
        return api_result(code=203, message='编辑成功')

    def delete(self):
        """字段断言规则删除"""

        data = request.get_json()
        ass_field_id = data.get('id')
        query_ass_field = TestCaseAssField.query.get(ass_field_id)

        if not query_ass_field:
            return api_result(code=400, message='字段断言id:{}数据不存在'.format(ass_field_id))

        if query_ass_field.creator_id != g.app_user.id:
            return api_result(code=400, message='非管理员不能删除其他人的断言！')

        query_ass_field.modifier_id = g.app_user.id
        query_ass_field.modifier = g.app_user.username
        query_ass_field.delete()
        return api_result(code=204, message='删除成功')


class RespAssertionRulePageApi(MethodView):
    """
    resp assertion rule page api
    POST: 返回值断言规则分页模糊查询
    """

    def post(self):
        """用例变量分页模糊查询"""

        data = request.get_json()
        resp_ass_id = data.get('resp_ass_id')
        assert_description = data.get('assert_description')
        is_deleted = data.get('is_deleted', 0)
        creator_id = data.get('creator_id')
        page = data.get('page')
        size = data.get('size')

        sql = """
        SELECT * 
        FROM exile_ass_response  
        WHERE 
        id = "id" 
        and assert_description LIKE"%B1%" 
        and is_deleted = 0
        and creator_id = 1
        ORDER BY create_timestamp LIMIT 0,20;
        """

        where_dict = {
            "id": resp_ass_id,
            "is_deleted": is_deleted,
            "creator_id": creator_id
        }

        result_data = general_query(
            model=TestCaseAssResponse,
            field_list=['assert_description'],
            query_list=[assert_description],
            where_dict=where_dict,
            page=page,
            size=size
        )
        return api_result(code=200, message='操作成功', data=result_data)


class FieldAssertionRulePageApi(MethodView):
    """
    field assertion rule page api
    POST: 字段断言规则分页模糊查询
    """

    def post(self):
        """字段断言分页模糊查询"""

        data = request.get_json()
        field_ass_id = data.get('field_ass_id')
        assert_description = data.get('assert_description')
        is_deleted = data.get('is_deleted', 0)
        creator_id = data.get('creator_id')
        page = data.get('page')
        size = data.get('size')

        sql = """
        SELECT * 
        FROM exile_ass_field  
        WHERE 
        id = "id" 
        and assert_description LIKE"%B1%" 
        and is_deleted = 0
        and creator_id = 1
        ORDER BY create_timestamp LIMIT 0,20;
        """

        where_dict = {
            "id": field_ass_id,
            "is_deleted": is_deleted,
            "creator_id": creator_id
        }

        result_data = general_query(
            model=TestCaseAssField,
            field_list=['assert_description'],
            query_list=[assert_description],
            where_dict=where_dict,
            page=page,
            size=size
        )
        return api_result(code=200, message='操作成功', data=result_data)
