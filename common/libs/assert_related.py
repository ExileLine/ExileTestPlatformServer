# -*- coding: utf-8 -*-
# @Time    : 2021/9/1 5:20 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : assert_related.py
# @Software: PyCharm

"""
该函数已经无法在新的数据结构中使用,保留仅用于重构过程中作为参考!
该函数已经无法在新的数据结构中使用,保留仅用于重构过程中作为参考!
该函数已经无法在新的数据结构中使用,保留仅用于重构过程中作为参考!
"""

import json
import redis

from common.libs.db import MyPyMysql, MyPostgreSql, MySqlServer
from common.libs.execute_code import execute_code
from common.libs.StringIOLog import StringIOLog
from common.libs.data_dict import GlobalsDict, rule_dict, expect_val_type_dict
from common.libs.db import project_db


class AssertMain:
    """
    断言类
    """

    @classmethod
    def gen_assert_result(cls, rule_key, this_val, expect_val_type, expect_val, sio=None):
        """
        断言
        :param rule_key: 规则比较符
        :param this_val: 当前值
        :param expect_val_type: 期望值类型
        :param expect_val: 期望值
        :param sio: sio
        :return:
        """
        rule = rule_dict.get(rule_key)  # 从字典中取出反射的规则函数 如: == 转 __eq__
        native_function = expect_val_type_dict.get(str(expect_val_type))  # 从字典中取出反射的类型函数 如: "1" 转 int

        if not isinstance(expect_val, native_function):
            try:
                expect_val = native_function(expect_val)  # 期望值根据类型转换
            except BaseException as e:
                raise ValueError(f'期望值:{expect_val} 转换:{native_function} 类型失败')

        this_val_type = type(this_val)
        expect_val_type = type(expect_val)

        message = f'{this_val}:{this_val_type} [{rule_key}] {expect_val}:{expect_val_type}'
        sio = sio if sio else StringIOLog()
        sio.log(f'function: {native_function}')
        sio.log(message)

        if not this_val_type == expect_val_type:
            raise TypeError(f"当前值:{this_val} 类型:{expect_val_type} 与 期望值:{expect_val} 类型:{expect_val_type} 不一致,无法用于比较")

        if not hasattr(this_val, rule):
            raise AttributeError(f"当前值:{this_val} 没有属性:{rule_key}")

        result = getattr(this_val, rule)(expect_val)

        return result


class AssertResponseMain(AssertMain):
    """Response 断言类"""

    def __init__(self, sio=None, resp_json=None, resp_headers=None, assert_description=None, assert_key=None, rule=None,
                 expect_val=None, response_source=None, expect_val_type=None, is_expression=None, python_val_exp=None):
        self.sio = sio if sio else StringIOLog()
        self.resp_json = resp_json
        self.resp_headers = resp_headers
        self.assert_description = assert_description
        self.this_val = None
        self.assert_key = assert_key
        self.rule = rule
        self.expect_val = expect_val
        self.response_source = response_source
        self.expect_val_type = expect_val_type
        self.is_expression = is_expression
        self.python_val_exp = python_val_exp

    def set_this_val(self):
        """
        用键获取需要断言的值
        :return:
        """

        if self.response_source not in GlobalsDict.resp_source_tuple():
            self.sio.log(f"response 来源错误: {self.response_source}", status="error")
            return False

        if self.response_source == GlobalsDict.resp_source_tuple()[0]:  # response_body
            if self.is_expression:
                result_json = execute_code(code=self.python_val_exp, data=self.resp_json)
                result = result_json.get('result_data')
                self.sio.log(f"=== 公式取值结果: {result} ===")
                self.this_val = result
            else:
                self.this_val = self.resp_json.get(self.assert_key)  # 直接常规取值:紧限于返回值的第一层键值对如:{"code":200,"message":"ok"}

        if self.response_source == GlobalsDict.resp_source_tuple()[1]:  # response_headers
            if self.is_expression:
                result_json = execute_code(code=self.python_val_exp, data=self.resp_headers)
                result = result_json.get('result_data')
                self.sio.log(f"=== 公式取值结果: {result} ===")
                self.this_val = result
            else:
                self.this_val = self.resp_headers.get(
                    self.assert_key)  # 直接常规取值:紧限于返回值的第一层键值对如:{"code":200,"message":"ok"}

    def main(self):
        """
        resp断言
        :this_val: 当前值
        :rule: 规则
        :expect_val_type: 期望值类型
        :expect_val: 期望值
        ps:如果该方法报错,是参数在入库的时候接口没有做好检验或者手动修改了数据库的数据
        """

        try:
            self.set_this_val()
        except BaseException as e:
            self.sio.log(f"获取需要断言的值:{str(e)}", status="error")
            return False

        try:
            self.sio.log(f'=== 断言:{self.assert_description} ===')
            self.sio.log('=== 键值:{} ==='.format({self.assert_key: self.this_val}))

            if self.gen_assert_result(this_val=self.this_val, rule_key=self.rule, expect_val_type=self.expect_val_type,
                                      expect_val=self.expect_val, sio=self.sio):
                self.sio.log('=== Response 断言通过 ===', status='success')
                return True
            else:
                self.sio.log('=== Response 断言失败 ===', status="error")
                return False

        except BaseException as e:
            self.sio.log(f'数据异常:{str(e)}', status='error')
            self.sio.log(
                '这种情况一般会因为以下两种原因导致:\n1.查看数据库确认该数据是否有被手动修改过\n2.查看: case_assertion_api.py 中的 RespAssertionRuleApi 中的逻辑是否被修改',
                status='error')
            self.sio.log('=== 断言异常 ===', status="error")
            return False


class AssertFieldMain(AssertMain):
    """Field 断言类"""

    def __init__(self, sio=None, assert_description=None, db_id=None, assert_list=None):

        self.sio = sio if sio else StringIOLog()
        self.assert_description = assert_description
        self.db_id = db_id
        self.assert_list = assert_list

        self.query_result = None
        self.db_type = None
        self.db_connection = {}
        self.db_obj = None

        self.ass_field_success = []
        self.ass_field_fail = []

        self.db_dict = {
            "mysql": self.get_mysql,
            "redis": self.get_redis,
            "postgresql": self.get_postgresql,
            "mongodb": self.get_mongodb,
            'es': self.get_es,
            "oracle": self.get_oracle,
            "db2": self.get_db2,
            "sqlserver": self.get_sqlserver
        }

    def get_mysql(self):
        """连接:Mysql"""

        db = MyPyMysql(**self.db_connection, debug=True)  # MySql实例
        ping = db.ping()
        return {
            "db": db,
            "cmd": "select"
        }

    def get_redis(self):
        """连接:Redis"""

        self.db_connection.update({"decode_responses": True})  # bytes to str
        pool = redis.ConnectionPool(**self.db_connection)
        db = redis.Redis(connection_pool=pool)  # Redis实例
        db.ping()

        return {
            "db": db,
            "cmd": "execute_command"
        }

    def get_postgresql(self):
        """连接:PostgreSQL"""

        db = MyPostgreSql(**self.db_connection)  # postgreSql实例
        return {
            "db": db,
            "cmd": "select"
        }

    def get_mongodb(self):
        """连接:Mongodb"""

    def get_es(self):
        """连接:ES"""

    def get_oracle(self):
        """连接:Oracle"""

    def get_db2(self):
        """连接:DB2"""

    def get_sqlserver(self):
        """连接:SqlServer"""

        connection = {
            "server": f"{self.db_connection['host']}:{self.db_connection['port']}",
            "user": self.db_connection['user'],
            "password": self.db_connection['password']
        }
        db = MySqlServer(**connection)  # Sqlserver实例
        return {
            "db": db,
            "cmd": "select"
        }

    def query_db_connection(self):
        """查询db配置是否存在或者可用"""

        sql = f"""select * from exile_test_databases where id={self.db_id} and is_deleted=0;"""
        query_db = project_db.select(sql=sql, only=True)

        if not query_db:
            self.sio.log(f"=== 数据库不存在或禁用: {self.db_id} === ", status='error')
            self.ass_field_fail.append('数据库不存在或禁用')
            return False

        self.db_type = query_db.get('db_type', '')
        self.db_connection = query_db.get('db_connection')
        return True

    def ping_db_connection(self, from_data_ready=False):
        """检查db是否可以连接"""

        self.db_obj = self.db_dict.get(self.db_type.lower(), None)()  # 直接执行db对应的ping方法

        if not self.db_obj:
            self.sio.log(f"=== 暂时不支持: {self.db_type} ===", status='error')
            if not from_data_ready:
                self.ass_field_fail.append('暂时不支持')
            return False

        self.sio.log(f"=== 测试需要连接的db配置: {self.db_connection} - {type(self.db_connection)} ===")

    def ass_str_or_int_result(self, assert_field_obj):
        """查询结果为一个str或者int,直接使用 self.query_result 来检验"""

        print('ass_str_or_int_result')
        this_val = self.query_result
        rule = assert_field_obj.get('rule')
        expect_val = assert_field_obj.get('expect_val')
        expect_val_type = assert_field_obj.get('expect_val_type')

        self.sio.log(f'=== 断言:{self.assert_description} ===', status='success')
        self.sio.log(f'=== 值:{this_val} ===', status='success')

        try:
            if self.gen_assert_result(this_val=this_val, rule_key=rule, expect_val_type=expect_val_type,
                                      expect_val=expect_val, sio=self.sio):
                self.sio.log('=== Field 断言通过 ===', status='success')
                self.ass_field_success.append(True)
            else:
                self.sio.log('=== Field 断言失败 ===', status='error')
                self.ass_field_fail.append(False)

        except BaseException as e:
            self.sio.log(f'数据异常:{str(e)}', status='error')
            self.sio.log('这种情况一般会因为以下两种原因导致:', status='error')
            self.sio.log('1.查看数据库确认该数据是否有被手动修改过.', status='error')
            self.sio.log(
                '2.查看: case_assertion_api.py 中的 FieldAssertionRuleApi 中的逻辑是否被修改.',
                status='error')
            self.sio.log('=== 断言异常 ===', status="error")
            self.ass_field_fail.append(False)

    def ass_dict_result(self, assert_field_obj):
        """
        查询结果为一个dict,检验key:value
        ps:如果该方法报错,问题会出现在 参数在入库的时候接口没有做好检验 或 者手动修改了数据库的数据
        """

        print('ass_dict_result')
        assert_key = assert_field_obj.get('assert_key')
        this_val = self.query_result.get(assert_key)
        rule = assert_field_obj.get('rule')
        expect_val = assert_field_obj.get('expect_val')
        expect_val_type = assert_field_obj.get('expect_val_type')

        self.sio.log(f'=== 断言:{self.assert_description} ===', status='success')
        self.sio.log(f'=== 字段:{assert_key} ===', status='success')

        try:
            if self.gen_assert_result(this_val=this_val, rule_key=rule, expect_val_type=expect_val_type,
                                      expect_val=expect_val, sio=self.sio):
                self.sio.log('=== Field 断言通过 ===', status='success')
                self.ass_field_success.append(True)
            else:
                self.sio.log('=== Field 断言失败 ===', status='error')
                self.ass_field_fail.append(False)

        except BaseException as e:
            self.sio.log(f'数据异常:{str(e)}', status='error')
            self.sio.log('这种情况一般会因为以下两种原因导致:', status='error')
            self.sio.log('1.查看数据库确认该数据是否有被手动修改过.', status='error')
            self.sio.log(
                '2.查看: case_assertion_api.py 中的 FieldAssertionRuleApi 中的逻辑是否被修改.',
                status='error')
            self.sio.log('=== 断言异常 ===', status="error")
            self.ass_field_fail.append(False)

    def ass_list_result(self, assert_field_obj):
        """
        查询结果为一个[],检验:=,>,>=,<,<=,in,not in
        ps:如果该方法报错,是参数在入库的时候接口没有做好检验或者手动修改了数据库的数据
        """
        # TODO ass_list_result

    def to_ass(self, assert_field_obj):
        """
        assert_field_obj = {
            "assert_key": "id",
            "expect_val": 1,
            "is_expression": 0,
            "python_val_exp": "",
            "expect_val_type": "1",
            "rule": "=="
        }
        :param assert_field_obj: 期望结果
        :return:
        """
        print(json.dumps(assert_field_obj, ensure_ascii=False))
        __func = expect_val_type_dict.get(str(assert_field_obj.get('expect_val_type')))
        assert_field_obj['expect_val'] = __func(assert_field_obj['expect_val'])

        if self.db_type in ['mysql', 'postgresql', 'sqlserver']:
            # TODO 暂时支持唯一数据检验
            if len(self.query_result) == 1 and isinstance(self.query_result, list):
                self.query_result = self.query_result[0]
            self.ass_dict_result(assert_field_obj)

        elif self.db_type in ['redis']:

            self.query_result = json.loads(self.query_result)

            if isinstance(self.query_result, (dict, list)) and bool(assert_field_obj.get('is_expression')):
                self.ass_dict_result(assert_field_obj)
            else:
                self.ass_str_or_int_result(assert_field_obj)

    def main(self):
        """
        field断言
        :this_val: 当前值
        :rule: 规则
        :expect_val_type: 期望值类型
        :expect_val: 期望值
        """

        try:
            self.query_db_connection()
            self.ping_db_connection()

            for ass in self.assert_list:
                query = ass.get('query')
                assert_field_list = ass.get('assert_field_list')
                result_db = self.db_obj.get("db")
                result_cmd = self.db_obj.get("cmd")
                print(result_cmd)
                query_result = getattr(result_db, result_cmd)(query)
                print(query_result)
                self.query_result = query_result
                list(map(self.to_ass, assert_field_list))

            return {
                "success": len(self.ass_field_success),
                "fail": len(self.ass_field_fail),
            }
        except BaseException as e:
            self.sio.log(f"=== {str(e)} ===", status='error')
            result = {
                "success": len(self.ass_field_success),
                "fail": len(self.ass_field_fail),
            }
            return result


if __name__ == '__main__':
    def test_resp_ass():
        """测试断言resp"""
        resp_headers = {
            'Content-Type': 'application/json',
            'Content-Length': '72',
            'Server': 'Werkzeug/2.0.1 Python/3.9.4',
            'Date': 'Thu, 02 Sep 2021 12:48:32 GMT'
        }
        resp_json = {
            "code": 200,
            "data": 1630586912,
            "message": "index"
        }
        resp_ass_dict = {
            # "rule": "__eq__",
            "rule": "==",
            "assert_key": "code",
            "expect_val": 200,
            "is_expression": 1,
            "python_val_exp": "okc.get('code')",
            "expect_val_type": "1"
        }
        new_ass = AssertResponseMain(
            resp_json=resp_json,
            resp_headers=resp_headers,
            assert_description="Resp通用断言",
            **resp_ass_dict
        )
        resp_ass_result = new_ass.main()
        print(resp_ass_result)


    def test_field_ass():
        """测试断言field"""

        def __execute(ass_json):
            """
            执行
            :return:
            """

            new_field_ass = AssertFieldMain(
                sio=StringIOLog(),
                # assert_description=assert_description,
                **ass_json
            )

            new_field_ass.main()

        feild_ass_demo = {
            "version_id_list": [],
            "assert_description": "field断言2022-03-10",
            "is_public": 1,
            "remark": "remark",
            "ass_json": [
                {
                    "db_id": 12,
                    "assert_list": [
                        {
                            "query": "select id, case_name FROM ExileTestPlatform.exile_test_case WHERE id=1;",
                            "assert_field_list": [
                                {
                                    "rule": "==",
                                    "assert_key": "id",
                                    "expect_val": 1,
                                    "is_expression": 0,
                                    "python_val_exp": "",
                                    "expect_val_type": "1"
                                },
                                {
                                    "rule": "==",
                                    "assert_key": "id",
                                    "expect_val": 1,
                                    "is_expression": 1,
                                    "python_val_exp": "obj.get('id')",
                                    "expect_val_type": "1"
                                }
                            ]
                        }
                    ]
                },
                {
                    "db_id": 9,
                    "assert_list": [
                        {
                            "query": "get 127.0.0.1",
                            "assert_field_list": [
                                {
                                    "rule": "==",
                                    "assert_key": "username",
                                    "expect_val": "user_00007",
                                    "is_expression": 1,
                                    "python_val_exp": "obj.get('username')",
                                    "expect_val_type": "2"
                                }
                            ]
                        }
                    ]
                },
                {
                    "db_id": 9,
                    "assert_list": [
                        {
                            "query": "get user_00007",
                            "assert_field_list": [
                                {
                                    "rule": "==",
                                    "assert_key": "7",
                                    "expect_val": "user_00007",
                                    "is_expression": 0,
                                    "python_val_exp": "",
                                    "expect_val_type": "2"
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        assert_description = feild_ass_demo.get('assert_description')
        ass_json_list = feild_ass_demo.get('ass_json')
        print(assert_description)
        list(map(__execute, ass_json_list))

    # test_resp_ass()
    # test_field_ass()
