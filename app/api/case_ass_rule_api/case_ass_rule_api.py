# -*- coding: utf-8 -*-
# @Time    : 2021/7/24 1:15 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : case_ass_rule_api.py
# @Software: PyCharm

from app.all_reference import *
from app.models.test_case.models import TestCaseAssResponse, TestCaseAssField


# 旧数据结构,暂时保留
def check_field_ass_old(aj_list):
    """检查:断言新增的参数"""

    for a in aj_list:
        check_bool = check_keys(
            a, 'db_name', 'table_name', 'query', 'assert_list'
        )
        query = a.get('query', [])
        query_len = len(query)
        assert_list = a.get('assert_list', [])
        assert_list_len = len(assert_list)

        if not check_bool or not isinstance(query, list) or not isinstance(assert_list, list):
            return False, 'ass_json 参数错误'

        max_len = max([query_len, assert_list_len])
        for index, i in enumerate(range(max_len)):
            if not query or not assert_list:
                return True, 'pass'

            if query:
                query_obj = query.pop()
                if not isinstance(query_obj, dict):
                    return False, 'query 对象:{} 类型错误:{} 位置:{}'.format(query_obj, type(query_obj), index)
                if not check_keys(query_obj, 'field_name', 'field_key', 'query_rule', 'is_sql', 'sql'):
                    return False, 'query对象key错误,位置:{}'.format(index)

            if assert_list:
                ass_obj = assert_list.pop()
                if not isinstance(ass_obj, dict):
                    return False, 'assert_list对象:{} 类型错误:{} 位置:{}'.format(ass_obj, type(ass_obj), index)

                if not check_keys(ass_obj, 'assert_key', 'expect_val', 'expect_val_type', 'rule'):
                    return False, 'assert_list对象key错误,位置:{}'.format(index)


def check_field_ass(aj_list):
    """检查:断言新增的参数"""

    for a in aj_list:
        check_bool = check_keys(a, 'sql', 'assert_list')
        sql = a.get('sql')
        assert_list = a.get('assert_list', [])
        print(check_bool)

        pattern = r"\b(exec|insert|drop|grant|alter|delete|update|count|chr|mid|master|truncate|char|delclare)\b|(\*)"
        r = re.search(pattern, sql.lower())
        if r:
            return False, '{}:不属于查询类别的Sql语句'.format(r.group())

        if not check_bool or not isinstance(assert_list, list):
            return False, 'ass_json 参数错误'

        if assert_list:
            ass_obj = assert_list.pop()
            print(ass_obj)
            if not isinstance(ass_obj, dict):
                return False, 'assert_list对象:{} 类型错误:{}'.format(ass_obj, type(ass_obj))

            if not check_keys(ass_obj, 'assert_key', 'expect_val', 'expect_val_type', 'rule'):
                return False, 'assert_list对象key错误:{}'.format(ass_obj)
    return True, 'True'


class RespAssertionRuleApi(MethodView):
    """
    返回值断言规则Api
    GET: 断言规则详情
    POST: 断言规则新增
    PUT: 断言规则编辑
    DELETE: 断言规则删除


    :assert_key: 返回值的键(用于简单取值)
    :expect_val: 期望值
    :expect_val_type: 期望值类型
    :rule: 规则
    :is_expression: 是否使用取值公式
    :python_val_exp: python取值公式


    ass_json_demo = {
            "assert_key": "code",
            "expect_val": "200",
            "expect_val_type": "1",
            "rule": "=",
            "is_expression": 0,
            "python_val_exp": "okc.get('a').get('b').get('c')[0]"
        }
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
        remark = data.get('remark')

        if not isinstance(ass_json, list) or not ass_json:
            return ab_code(400)

        new_ass_json = []

        for a in ass_json:
            check_bool = check_keys(
                a, 'assert_key', 'expect_val_type', 'expect_val', 'rule', 'is_expression', 'python_val_exp'
            )
            if not check_bool:
                return api_result(code=400, message='检验对象错误', data=a)

            rule = rule_save_dict.get(a.get('rule'))
            if not rule:
                return api_result(code=400, message='规则参数错误:{}'.format(a.get('rule')))

            is_expression = a.get('is_expression')
            is_rule_source_bool = bool(str(is_expression) in ['0', '1'])
            if not is_rule_source_bool:
                return api_result(code=400, message='规则参数错误:{}'.format(is_expression))

            expect_val = a.get('expect_val')
            expect_val_type = expect_val_type_dict.get(str(a.get('expect_val_type')))
            try:
                a['expect_val'] = expect_val_type(expect_val)
                new_ass_json.append(a)
            except BaseException as e:
                return api_result(code=400, message='参数:{} 无法转换至 类型:{}'.format(expect_val, type(expect_val_type())))

        new_ass_resp = TestCaseAssResponse(
            assert_description=assert_description,
            ass_json=new_ass_json,
            creator='调试',
            creator_id=1,
            remark=remark
        )
        db.session.add(new_ass_resp)
        db.session.commit()
        return api_result(code=201, message='创建成功', data=data)

    def put(self):
        """返回值断言编辑"""

        data = request.get_json()
        ass_resp_id = data.get('ass_resp_id')
        assert_description = data.get('assert_description')
        ass_json = data.get('ass_json', [])
        remark = data.get('remark')

        if not isinstance(ass_json, list) or not ass_json:
            return ab_code(400)

        new_ass_json = []

        for a in ass_json:
            check_bool = check_keys(
                a, 'assert_key', 'expect_val_type', 'expect_val', 'rule', 'is_expression', 'python_val_exp'
            )
            if not check_bool:
                return api_result(code=400, message='检验对象错误', data=a)

            rule = rule_save_dict.get(a.get('rule'))
            if not rule:
                return api_result(code=400, message='规则参数错误:{}'.format(a.get('rule')))

            is_expression = a.get('is_expression')
            is_rule_source_bool = bool(str(is_expression) in ['0', '1'])
            if not is_rule_source_bool:
                return api_result(code=400, message='规则参数错误:{}'.format(is_expression))

            expect_val = a.get('expect_val')
            expect_val_type = expect_val_type_dict.get(str(a.get('expect_val_type')))
            try:
                a['expect_val'] = expect_val_type(expect_val)
                new_ass_json.append(a)
            except BaseException as e:
                return api_result(code=400, message='参数:{} 无法转换至 类型:{}'.format(expect_val, type(expect_val_type())))

        query_ass_resp = TestCaseAssResponse.query.get(ass_resp_id)

        if query_ass_resp:
            query_ass_resp.assert_description = assert_description
            query_ass_resp.ass_json = new_ass_json
            query_ass_resp.remark = remark
            query_ass_resp.modifier = "调试"
            query_ass_resp.modifier_id = 1
            db.session.commit()
            return api_result(code=203, message='编辑成功')

        return api_result(code=400, message='返回值断言id:{}数据不存在'.format(ass_resp_id))

    def delete(self):
        """返回值断言删除"""

        data = request.get_json()
        ass_resp_id = data.get('ass_resp_id')
        query_ass_resp = TestCaseAssResponse.query.get(ass_resp_id)

        if query_ass_resp:
            query_ass_resp.is_deleted = query_ass_resp.id
            query_ass_resp.modifier = "调试"
            query_ass_resp.modifier_id = 1
            db.session.commit()
            return api_result(code=204, message='删除成功')

        return api_result(code=400, message='返回值断言id:{}数据不存在'.format(ass_resp_id))


class FieldAssertionRuleApi(MethodView):
    """
    字段断言规则Api
    GET: 断言规则详情
    POST: 断言规则新增
    PUT: 断言规则编辑
    DELETE: 断言规则删除

    query:
        :field_name: 字段的名称
        :field_key: 字段的值
        :query_rule: 查询规则
        :is_sql: 是否使用sql(开启后将不使用上述的field_name,field_key,query_rule)
        :sql: sql

    assert_list:
        :assert_key: 键(用于简单取值)
        :expect_val: 期望值
        :expect_val_type: 期望值类型
        :rule: 规则

    ass_json_demo = {

                "sql": "SELECT * FROM exilic_test_case WHERE id=1;",
                "assert_list": [
                    {
                        "assert_key": "id",
                        "expect_val": "1",
                        "expect_val_type": "1",
                        "rule": "="
                    }
                ]
            }
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
        assert_description = data.get('assert_description')
        ass_json = data.get('ass_json', [])
        remark = data.get('remark')

        if not isinstance(ass_json, list) or not ass_json:
            return ab_code(400)

        to_ass_json = copy.deepcopy(ass_json)
        _bool, _msg = check_field_ass(to_ass_json)

        if not _bool:
            return api_result(code=400, message='{}'.format(_msg))

        new_ass_field = TestCaseAssField(
            assert_description=assert_description,
            ass_json=ass_json,
            creator='调试',
            creator_id=1,
            remark=remark
        )
        new_ass_field.save()
        return api_result(code=201, message='创建成功', data=ass_json)

    def put(self):
        """字段断言编辑"""

        data = request.get_json()
        ass_field_id = data.get('ass_field_id')
        assert_description = data.get('assert_description')
        ass_json = data.get('ass_json', [])
        remark = data.get('remark')

        if not isinstance(ass_json, list) or not ass_json:
            return ab_code(400)

        to_ass_json = copy.deepcopy(ass_json)
        _bool, _msg = check_field_ass(to_ass_json)

        if not _bool:
            return api_result(code=400, message='{}'.format(_msg))

        query_ass_field = TestCaseAssField.query.get(ass_field_id)

        if not query_ass_field:
            return api_result(code=400, message='字段断言id:{}数据不存在'.format(ass_field_id))

        query_ass_field.assert_description = assert_description
        query_ass_field.ass_json = ass_json
        query_ass_field.remark = remark
        query_ass_field.modifier = "调试"
        query_ass_field.modifier_id = 1
        db.session.commit()
        return api_result(code=203, message='编辑成功')

    def delete(self):
        """字段断言规则删除"""

        data = request.get_json()
        ass_field_id = data.get('ass_field_id')
        query_ass_field = TestCaseAssField.query.get(ass_field_id)

        if query_ass_field:
            query_ass_field.is_deleted = query_ass_field.id
            query_ass_field.modifier = "调试"
            query_ass_field.modifier_id = 1
            db.session.commit()
            return api_result(code=204, message='删除成功')

        return api_result(code=400, message='字段断言id:{}数据不存在'.format(ass_field_id))


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
        is_deleted = data.get('is_deleted', False)
        page, size = page_size(**data)

        sql = """
        SELECT * 
        FROM exilic_ass_response  
        WHERE 
        id LIKE"%%" 
        and assert_description LIKE"%B1%" 
        and is_deleted=0
        ORDER BY create_timestamp LIMIT 0,20;
        """

        result_data = general_query(
            model=TestCaseAssResponse,
            field_list=['id', 'assert_description'],
            query_list=[resp_ass_id, assert_description],
            is_deleted=is_deleted,
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
        """用例变量分页模糊查询"""

        data = request.get_json()
        field_ass_id = data.get('field_ass_id')
        assert_description = data.get('assert_description')
        is_deleted = data.get('is_deleted', False)
        page, size = page_size(**data)

        sql = """
        SELECT * 
        FROM exilic_ass_field  
        WHERE 
        id LIKE"%%" 
        and assert_description LIKE"%B1%" 
        and is_deleted=0
        ORDER BY create_timestamp LIMIT 0,20;
        """

        result_data = general_query(
            model=TestCaseAssField,
            field_list=['id', 'assert_description'],
            query_list=[field_ass_id, assert_description],
            is_deleted=is_deleted,
            page=page,
            size=size
        )
        return api_result(code=200, message='操作成功', data=result_data)
