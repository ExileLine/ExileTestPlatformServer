# -*- coding: utf-8 -*-
# @Time    : 2021/7/24 1:15 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : ass_rule_api.py
# @Software: PyCharm

from app.all_reference import *
from app.models.test_case.models import TestCaseAssResponse, TestCaseAssField


def check_field_ass(aj_list):
    """检查:断言新增的参数"""

    def check_keys(dic, *keys):
        for k in keys:
            if k not in dic.keys():
                return False
        return True

    for a in aj_list:
        check_bool = check_keys(
            a, 'db_name', 'table_name', 'query', 'assert_list'
        )
        query = a.get('query', [])
        query_len = len(query)
        assert_list = a.get('assert_list', [])
        assert_list_len = len(assert_list)
        if check_bool and isinstance(query, list) and isinstance(assert_list, list):
            max_len = max([query_len, assert_list_len])
            for index, i in enumerate(range(max_len)):
                if query:
                    query_obj = query.pop()
                    if isinstance(query_obj, dict):
                        if check_keys(query_obj, 'field_name', 'field_key', 'query_rule', 'is_sql', 'sql'):
                            pass
                        else:
                            return False, 'query对象key错误,位置:{}'.format(index)
                    else:
                        return False, 'query 对象:{} 类型错误:{} 位置:{}'.format(query_obj, type(query_obj), index)

                if assert_list:
                    ass_obj = assert_list.pop()
                    if isinstance(ass_obj, dict):
                        if check_keys(ass_obj, 'assert_key', 'assert_val', 'assert_val_type', 'rule'):
                            pass
                        else:
                            return False, 'assert_list对象key错误,位置:{}'.format(index)
                    else:
                        return False, 'assert_list对象:{} 类型错误:{} 位置:{}'.format(ass_obj, type(ass_obj), index)
                else:
                    return True, 'pass'
        else:
            return False, 'ass_json 参数错误'


class RespAssertionRuleApi(MethodView):
    """
    返回值断言规则Api
    GET: 断言规则详情
    POST: 断言规则新增
    PUT: 断言规则编辑
    DELETE: 断言规则删除

    ass_json_demo = {
            "assert_key": "code",
            "assert_val": "200",
            "assert_val_type": "1",
            "expect_val": "333",
            "rule": "=",
            "is_rule_source": 0,
            "python_val_exp": "okc.get('a').get('b').get('c')[0]"
        }
    """

    def get(self, ass_resp_id):
        """返回值断言明细"""
        query_ass_resp = TestCaseAssResponse.query.get(ass_resp_id)
        if query_ass_resp:
            return api_result(code=200, message='操作成功', data=query_ass_resp.to_json())
        else:
            return api_result(code=400, message='返回值断言id:{}数据不存在'.format(ass_resp_id))

    def post(self):
        """返回值断言新增"""
        data = request.get_json()
        assert_description = data.get('assert_description')
        ass_json = data.get('ass_json', [])
        remark = data.get('remark')

        if isinstance(ass_json, list) and ass_json:
            for a in ass_json:
                check_bool = check_keys(
                    a, 'assert_key', 'assert_val', 'assert_val_type', 'expect_val', 'rule', 'is_rule_source',
                    'python_val_exp'
                )
                if check_bool:
                    rule = a.get('rule')
                    is_rule_source = a.get('is_rule_source')
                    ass_rule_bool = bool(rule in ['>', '<', '='])
                    is_rule_source_bool = bool(str(is_rule_source) in ['0', '1'])
                    if ass_rule_bool and is_rule_source_bool:
                        pass
                    else:
                        return api_result(code=400, message='检验规则或规则来源错误:{},{}'.format(rule, is_rule_source))
                else:
                    return api_result(code=400, message='检验对象错误', data=a)

            new_ass_resp = TestCaseAssResponse(
                assert_description=assert_description,
                ass_json=ass_json,
                creator='调试',
                creator_id=1,
                remark=remark
            )
            db.session.add(new_ass_resp)
            db.session.commit()
            return api_result(code=201, message='创建成功', data=data)
        else:
            return ab_code(400)

    def put(self):
        """返回值断言编辑"""
        data = request.get_json()
        ass_resp_id = data.get('ass_resp_id')
        assert_description = data.get('assert_description')
        ass_json = data.get('ass_json', [])
        remark = data.get('remark')

        if isinstance(ass_json, list) and ass_json:
            for a in ass_json:
                check_bool = check_keys(
                    a, 'assert_key', 'assert_val', 'assert_val_type', 'expect_val', 'rule', 'is_rule_source',
                    'python_val_exp'
                )
                if check_bool:
                    rule = a.get('rule')
                    is_rule_source = a.get('is_rule_source')
                    ass_rule_bool = bool(rule in ['>', '<', '='])
                    is_rule_source_bool = bool(str(is_rule_source) in ['0', '1'])
                    if ass_rule_bool and is_rule_source_bool:
                        pass
                    else:
                        return api_result(code=400, message='检验规则或规则来源错误:{},{}'.format(rule, is_rule_source))
                else:
                    return api_result(code=400, message='检验对象错误', data=a)

            query_ass_resp = TestCaseAssResponse.query.get(ass_resp_id)

            if query_ass_resp:
                query_ass_resp.assert_description = assert_description
                query_ass_resp.ass_json = ass_json
                query_ass_resp.remark = remark
                query_ass_resp.modifier = "调试"
                query_ass_resp.modifier_id = 1
                db.session.commit()
                return api_result(code=203, message='编辑成功')
            else:
                return api_result(code=400, message='返回值断言id:{}数据不存在'.format(ass_resp_id))
        else:
            return ab_code(400)

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
        else:
            return api_result(code=400, message='返回值断言id:{}数据不存在'.format(ass_resp_id))


class FieldAssertionRuleApi(MethodView):
    """
    字段断言规则Api
    GET: 断言规则详情
    POST: 断言规则新增
    PUT: 断言规则编辑
    DELETE: 断言规则删除

    ass_json_demo = {
                "db_name": "online",
                "table_name": "ol_user",
                "query": [
                    {
                        "field_name": "id",
                        "field_key": "1",
                        "query_rule": "=",
                        "is_sql": "1",
                        "sql": "SELECT * FROM ol_user WHERE id=1;"
                    },
                    {
                        "field_name": "name",
                        "field_key": "yyx",
                        "query_rule": "=",
                        "is_sql": "1",
                        "sql": "SELECT * FROM ol_user WHERE id=1;"
                    }
                ],
                "assert_list": [
                    {
                        "assert_key": "id",
                        "assert_val": "1",
                        "assert_val_type": "1",
                        "rule": "="
                    }
                ]
            }
    """

    def get(self, ass_field_id):
        """字段断言明细"""
        query_ass_field = TestCaseAssField.query.get(ass_field_id)
        if query_ass_field:
            return api_result(code=200, message='操作成功', data=query_ass_field.to_json())
        else:
            return api_result(code=400, message='字段断言id:{}数据不存在'.format(ass_field_id))

    def post(self):
        """字段断言新增"""
        data = request.get_json()
        assert_description = data.get('assert_description')
        ass_json = data.get('ass_json', [])
        remark = data.get('remark')

        if isinstance(ass_json, list) and ass_json:
            to_ass_json = copy.deepcopy(ass_json)
            _bool, _msg = check_field_ass(to_ass_json)
            if _bool:
                new_ass_field = TestCaseAssField(
                    assert_description=assert_description,
                    ass_json=ass_json,
                    creator='调试',
                    creator_id=1,
                    remark=remark
                )
                db.session.add(new_ass_field)
                db.session.commit()
                return api_result(code=201, message='创建成功')
            else:
                return api_result(code=400, message='{}'.format(_msg))
        else:
            ab_code(400)

    def put(self):
        """字段断言编辑"""
        data = request.get_json()
        ass_field_id = data.get('ass_field_id')
        assert_description = data.get('assert_description')
        ass_json = data.get('ass_json', [])
        remark = data.get('remark')

        if isinstance(ass_json, list) and ass_json:
            to_ass_json = copy.deepcopy(ass_json)
            _bool, _msg = check_field_ass(to_ass_json)
            if _bool:
                query_ass_field = TestCaseAssField.query.get(ass_field_id)
                if query_ass_field:
                    query_ass_field.assert_description = assert_description
                    query_ass_field.ass_json = ass_json
                    query_ass_field.remark = remark
                    query_ass_field.modifier = "调试"
                    query_ass_field.modifier_id = 1
                    db.session.commit()
                    return api_result(code=203, message='编辑成功')
                else:
                    return api_result(code=400, message='字段断言id:{}数据不存在'.format(ass_field_id))
            else:
                return api_result(code=400, message='{}'.format(_msg))
        else:
            ab_code(400)

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
        else:
            return api_result(code=400, message='字段断言id:{}数据不存在'.format(ass_field_id))


class RuleTestApi(MethodView):
    """
    取值规程调试Api

    get_dict_val_demo = {
        "rule_str": "okc.get('a').get('b').get('c')",
        "data_self": {
            "a": {
                "b": {
                    "c": [
                        1,
                        2,
                        3
                    ]
                }
            }
        }
    }

    get_list_val_demo = {
        "rule_str": "d[0].get('a')[0]",
        "data_self": [
            {
                "a": [
                    {
                        "b": "b"
                    }
                ]
            }
        ]
    }

    get_str_val_demo = {
        "rule_str": "x[0:3]",
        "data_self": "123456789"
    }

    """

    def post(self):
        data = request.get_json()
        rule_str = data.get('rule_str', "")
        data_self = data.get('data_self', {})
        data_type = data.get('data_type', {})
        print(rule_str)
        print(data_self)

        if isinstance(data_self, dict):
            d = data_self
            rs = rule_str.split('.')
            rs[0] = 'd'
            new_rule_str = '.'.join(rs)
        elif isinstance(data_self, list):
            d = data_self
            rs = rule_str.split("[")
            rs[0] = 'd'
            new_rule_str = '['.join(rs)
        elif isinstance(data_self, str):
            # todo 切片,函数,正则
            # d = data_self
            # rs = rule_str.split("[")
            # rs[0] = 'd'
            new_rule_str = rule_str

        else:
            return api_result(code=400, message='取值参数主体类型应该为:JSON,Dict,List,Str')

        print("exec:{}".format(new_rule_str))

        try:
            _locals = locals()
            # print(globals())
            # print(_locals)
            exec("""rule_result={}""".format(new_rule_str), globals(), _locals)
            rule_result = _locals['rule_result']
        except BaseException as e:
            return api_result(code=400, message='取值规则语法错误:{}:,错误原因:{}'.format(rule_str, str(e)))

        if rule_result:
            resp_data = {
                "bool": True,
                "result_data": rule_result
            }
            return api_result(code=200, message='取值规则正确', data=resp_data)
        else:
            resp_data = {
                "bool": False,
                "result_data": None
            }
            return api_result(code=400, message='未找到对应的值,请检查取值规则', data=resp_data)
