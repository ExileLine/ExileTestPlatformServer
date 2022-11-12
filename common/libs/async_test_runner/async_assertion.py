# -*- coding: utf-8 -*-
# @Time    : 2022/7/28 15:03
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : async_assertion.py
# @Software: PyCharm

import json
import redis
import operator

from common.libs.data_dict import GlobalsDict
from common.libs.execute_code import execute_code
from common.libs.db import project_db
from common.libs.db import MyPyMysql, MyPostgreSql, MySqlServer

resp_source_tuple = GlobalsDict.resp_source_tuple()
rule_dict_op = GlobalsDict.rule_dict_op()
value_type_dict = GlobalsDict.value_type_dict()


class BaseAsyncAssertion:
    """BaseAsyncAssertion"""

    def __init__(self, logs_key, data_logs, sio=None):
        self.logs_key = logs_key  # response_assert 或 field_assert
        self.data_logs = data_logs
        self.sio = sio

    async def common_assert(self, assert_key, rule, expect_val, expect_val_type, assert_val):
        """

        :param assert_key:
        :param rule:
        :param expect_val:
        :param expect_val_type:
        :param assert_val:
        :return:
        """

        # 获取内置函数如:int,str...
        # 将需要断言的值进行转换
        # 如果出现异常很大几率是手动修改了数据库的数据(因为case_assertion_api.py中的CheckAssertion新增断言时会进行校验)
        native_function = value_type_dict.get(expect_val_type)
        try:
            assert_val = native_function(assert_val)
            expect_val = native_function(expect_val)
        except BaseException as e:
            self.sio.log(f"数据异常->内置函数:{native_function}转换值:{assert_val} 时失败", status="error")
            self.sio.log(f"异常描述->{e}", status="error")
            await self.data_logs.add_logs(
                key=self.logs_key,
                val=f"数据异常->内置函数:{native_function}转换值:{assert_val} 时失败\n异常描述->{e}"
            )
            return False

        # 日志
        kv = '=== 键值:{} ==='.format({assert_key: assert_val})
        self.sio.log(kv)
        message = f'{assert_val}:{type(assert_val)} [{rule}] {expect_val}:{expect_val_type}'
        self.sio.log(f'function: {native_function}')
        self.sio.log(message)
        await self.data_logs.add_logs(
            key=self.logs_key,
            val=[f"{kv}", f"function: {native_function}", f"{message}"]
        )

        op_function = rule_dict_op.get(rule)
        try:
            if op_function != 'contains':
                assert_result = getattr(operator, op_function)(assert_val, expect_val)
            else:
                assert_result = getattr(operator, op_function)(str(assert_val), str(expect_val))
            return assert_result
        except BaseException as e:
            self.sio.log(f"数据异常->规则:{op_function}错误", status="error")
            self.sio.log(f"异常描述->{e}", status="error")
            await self.data_logs.add_logs(
                key=self.logs_key,
                val=f"数据异常->规则:{op_function}错误\n异常描述->{e}"
            )
            return False


class AsyncAssertionResponse(BaseAsyncAssertion):
    """异步响应断言"""

    def __init__(self, http_code, resp_headers, resp_json, case_resp_ass_info, data_logs, desc=None, sio=None):
        """

        :param http_code: HTTP状态码
        :param resp_headers: 响应头
        :param resp_json: 响应体
        :param case_resp_ass_info: 断言规则
        :param data_logs: 日志对象
        :param desc: 描述
        :param sio: 日志缓存
        """
        super(AsyncAssertionResponse, self).__init__(logs_key='response_assert', data_logs=data_logs, sio=sio)
        self.http_code = http_code
        self.resp_headers = resp_headers
        self.resp_json = resp_json
        self.case_resp_ass_info = case_resp_ass_info
        self.data_logs = data_logs
        self.desc = desc
        self.sio = sio
        self.response_source_dict = {
            "response_body": self.resp_json,
            "response_headers": self.resp_headers
        }
        self.count = {
            "success": 0,
            "fail": 0,
            "flag": None
        }

    async def main_assert(self, rule, response_source, assert_key, expect_val, expect_val_type, is_expression,
                          python_val_exp, **kwargs):
        """

        :param rule: 规则
        :param response_source: 响应来源
        :param assert_key: 取值的key
        :param expect_val:  期望值
        :param expect_val_type:  期望值类型
        :param is_expression: 是否启用表达式
        :param python_val_exp:  表达式
        :return:
        """

        self.sio.log(f'=== 断言:{self.desc} ===')
        await self.data_logs.add_logs(
            key="response_assert",
            val=f"=== 断言:{self.desc} ==="
        )

        if response_source not in resp_source_tuple:
            self.sio.log(f"响应来源:{response_source}不存在，无法断言", status="error")
            await self.data_logs.add_logs(
                key="response_assert",
                val=f"响应来源:{response_source}不存在，无法断言"
            )
            return False
        if rule not in rule_dict_op:
            self.sio.log(f"规则:{rule}不存在，无法断言", status="error")
            await self.data_logs.add_logs(
                key="response_assert",
                val=f"规则:{rule}不存在，无法断言"
            )
            return False
        if expect_val_type not in value_type_dict:
            self.sio.log(f"期望值类型:{expect_val_type}不存在，无法断言", status="error")
            await self.data_logs.add_logs(
                key="response_assert",
                val=f"期望值类型:{expect_val_type}不存在，无法断言"
            )
            return False

        # 取值
        source_data = self.response_source_dict.get(response_source)
        try:
            if is_expression:
                expression_result = execute_code(code=python_val_exp, data=source_data)
                assert_val = expression_result.get('result_data')
                self.sio.log(f"=== 公式取值结果: {assert_val} ===")
                await self.data_logs.add_logs(
                    key="response_assert",
                    val=f"=== 公式取值结果: {assert_val} ==="
                )
            else:
                assert_val = source_data.get(assert_key)
                self.sio.log(f"=== 取值结果: {assert_val} ===")
                await self.data_logs.add_logs(
                    key="response_assert",
                    val=f"=== 取值结果: {assert_val} ==="
                )
        except BaseException as e:
            self.sio.log(f"数据异常->取值失败:{source_data},键:{assert_key},表达式:{python_val_exp}", status="error")
            self.sio.log(f"异常描述->{e}", status="error")
            await self.data_logs.add_logs(
                key="response_assert",
                val=f"数据异常->取值失败:{source_data},键:{assert_key},表达式:{python_val_exp}\n异常描述->{e}"
            )
            return False

        assert_result = await self.common_assert(
            assert_key=assert_key,
            rule=rule,
            expect_val=expect_val,
            expect_val_type=expect_val_type,
            assert_val=assert_val
        )
        return assert_result

    async def gen_ass_json(self, ass_json):
        """断言规则"""

        for ass in ass_json:
            ass_result = await self.main_assert(**ass)
            if ass_result:
                self.sio.log('=== Response 断言通过 ===', status='success')
                self.count['success'] += 1
                await self.data_logs.add_logs(
                    key="response_assert",
                    val="=== Response 断言通过 ===",
                    flag=True
                )
            else:
                self.sio.log('=== Response 断言失败 ===', status="error")
                self.count['fail'] += 1
                await self.data_logs.add_logs(
                    key="response_assert",
                    val="=== Response 断言失败 ===",
                    flag=False
                )

    async def main(self):
        """main"""

        print('=== AsyncAssertionResponse ===')
        await self.data_logs.add_logs(
            key="response_assert",
            val="=== 响应断言 ==="
        )
        for ass in self.case_resp_ass_info:
            ass_json = ass.get('ass_json')
            await self.gen_ass_json(ass_json)
        self.count['flag'] = False if self.count.get('fail') > 0 else True
        return self.count


class DBUtil:
    """DBUtil"""

    @staticmethod
    def get_mysql(**kwargs):
        """连接:Mysql"""

        db = MyPyMysql(**kwargs, debug=True)  # MySql实例
        ping = db.db_obj().open
        return {
            "db": db,
            "cmd": "select"
        }

    @staticmethod
    def get_redis(**kwargs):
        """连接:Redis"""

        kwargs.update({"decode_responses": True})  # bytes to str
        pool = redis.ConnectionPool(**kwargs)
        db = redis.Redis(connection_pool=pool)  # Redis实例
        db.ping()

        return {
            "db": db,
            "cmd": "execute_command"
        }

    @staticmethod
    def get_postgresql(**kwargs):
        """连接:PostgreSQL"""

        db = MyPostgreSql(**kwargs)  # postgreSql实例
        return {
            "db": db,
            "cmd": "select"
        }

    @staticmethod
    def get_mongodb(**kwargs):
        """连接:Mongodb"""

    @staticmethod
    def get_es(**kwargs):
        """连接:ES"""

    @staticmethod
    def get_oracle(**kwargs):
        """连接:Oracle"""

    @staticmethod
    def get_db2(**kwargs):
        """连接:DB2"""

    @staticmethod
    def get_sqlserver(**kwargs):
        """连接:SqlServer"""

        connection = {
            "server": f"{kwargs['host']}:{kwargs['port']}",
            "user": kwargs['user'],
            "password": kwargs['password']
        }
        db = MySqlServer(**connection)  # Sqlserver实例
        return {
            "db": db,
            "cmd": "select"
        }


class AsyncAssertionField(BaseAsyncAssertion, DBUtil):
    """异步字段断言"""

    def __init__(self, case_field_ass_info, data_logs, desc=None, sio=None):
        """

        :param case_field_ass_info:
        :param data_logs: 日志对象
        :param desc: 描述
        :param sio: 日志缓存
        """
        super(AsyncAssertionField, self).__init__(logs_key='field_assert', data_logs=data_logs, sio=sio)
        self.case_field_ass_info = case_field_ass_info
        self.data_logs = data_logs
        self.desc = desc
        self.sio = sio
        self.count = {
            "success": 0,
            "fail": 0,
            "flag": True  # 调试时候设置为True
        }

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

    async def set_count(self, ass_result):
        """
        set count
        :param ass_result: 断言结果
        :return:
        """

        if ass_result:
            self.sio.log('=== Field 断言通过 ===', status='success')
            self.count['success'] += 1
            await self.data_logs.add_logs(
                key="field_assert",
                val="=== Field 断言通过 ===",
                flag=True
            )
        else:
            self.sio.log('=== Field 断言失败 ===', status="error")
            self.count['fail'] += 1
            await self.data_logs.add_logs(
                key="field_assert",
                val="=== Field 断言失败 ===",
                flag=False
            )

    async def ass_dict_consume(self, assert_description, query_result, assert_field_obj):
        """
        查询结果为一个dict,检验key:value
        :param assert_description: 断言描述
        :param query_result: 查询结果
        :param assert_field_obj: 断言规则
        :return:
        """

        self.sio.log('=== ass_dict_consume ===', status='success')

        assert_key = assert_field_obj.get('assert_key')
        rule = assert_field_obj.get('rule')
        expect_val = assert_field_obj.get('expect_val')
        expect_val_type = assert_field_obj.get('expect_val_type')
        is_expression = assert_field_obj.get('is_expression')
        python_val_exp = assert_field_obj.get('python_val_exp')

        self.sio.log(f'=== 断言:{assert_description} ===', status='success')
        self.sio.log(f'=== 字段:{assert_key} ===', status='success')
        await self.data_logs.add_logs(
            key="field_assert",
            val=[
                f'=== 断言:{assert_description} ===',
                f'=== 字段:{assert_key} ==='
            ]
        )

        if rule not in rule_dict_op:
            self.sio.log(f"规则:{rule}不存在，无法断言", status="error")
            await self.data_logs.add_logs(
                key="field_assert",
                val=f"规则:{rule}不存在，无法断言"
            )
            return False

        if expect_val_type not in value_type_dict:
            self.sio.log(f"期望值类型:{expect_val_type}不存在，无法断言", status="error")
            await self.data_logs.add_logs(
                key="field_assert",
                val=f"期望值类型:{expect_val_type}不存在，无法断言"
            )
            return False

        try:
            if is_expression:
                expression_result = execute_code(code=python_val_exp, data=query_result)
                assert_val = expression_result.get('result_data')
                self.sio.log(f"=== 公式取值结果: {assert_val} ===")
                await self.data_logs.add_logs(
                    key="field_assert",
                    val=f"=== 公式取值结果: {assert_val} ==="
                )
            else:
                assert_val = query_result.get(assert_key)
                self.sio.log(f"=== 取值结果: {assert_val} ===")
                await self.data_logs.add_logs(
                    key="field_assert",
                    val=f"=== 取值结果: {assert_val} ==="
                )

        except BaseException as e:
            self.sio.log(f"数据异常->取值失败:{query_result},键:{assert_key},表达式:{python_val_exp}", status="error")
            self.sio.log(f"异常描述->{e}", status="error")
            await self.data_logs.add_logs(
                key="field_assert",
                val=f"数据异常->取值失败:{query_result},键:{assert_key},表达式:{python_val_exp}\n异常描述->{e}"
            )
            return False

        assert_result = await self.common_assert(
            assert_key=assert_key,
            rule=rule,
            expect_val=expect_val,
            expect_val_type=expect_val_type,
            assert_val=assert_val
        )
        return assert_result

    async def ass_str_or_int_consume(self, assert_description, query_result, assert_field_obj):
        """
        查询结果为一个str或者int,直接使用 query_result 来检验
        :param assert_description: 断言描述
        :param query_result: 查询结果
        :param assert_field_obj: 断言规则
        :return:
        """

        self.sio.log('=== ass_str_or_int_consume ===', status='success')

        assert_key = assert_field_obj.get('assert_key')
        rule = assert_field_obj.get('rule')
        expect_val = assert_field_obj.get('expect_val')
        expect_val_type = assert_field_obj.get('expect_val_type')

        self.sio.log(f'=== 断言:{assert_description} ===', status='success')
        self.sio.log(f'=== 值:{query_result} ===', status='success')
        await self.data_logs.add_logs(
            key="field_assert",
            val=[
                f'=== 断言:{assert_description} ===',
                f'=== 值:{query_result} ==='
            ]
        )

        if rule not in rule_dict_op:
            self.sio.log(f"规则:{rule}不存在，无法断言", status="error")
            await self.data_logs.add_logs(
                key="field_assert",
                val=f"规则:{rule}不存在，无法断言"
            )
            return False

        if expect_val_type not in value_type_dict:
            self.sio.log(f"期望值类型:{expect_val_type}不存在，无法断言", status="error")
            await self.data_logs.add_logs(
                key="field_assert",
                val=f"期望值类型:{expect_val_type}不存在，无法断言"
            )
            return False

        assert_result = await self.common_assert(
            assert_key=assert_key,
            rule=rule,
            expect_val=expect_val,
            expect_val_type=expect_val_type,
            assert_val=query_result
        )
        return assert_result

    async def ass_list_consume(self):
        """1"""

    async def main_assert(self, assert_description, ass, db_result, db_type):
        """

        :param assert_description: 断言描述
        :param ass: 断言规则
        :param db_result: 数据库字典
        :param db_type: 数据库类型
        :return:
        """

        query = ass.get('query')
        assert_field_list = ass.get('assert_field_list')
        db = db_result.get("db")  # 数据库连接对象
        cmd = db_result.get("cmd")  # 数据库对应的查询api

        query_result = getattr(db, cmd)(query)
        print('query:', query)
        print('query_result:', query_result)
        await self.data_logs.add_logs(
            key="field_assert",
            val=[f"=== 语句 ===", query]
        )
        await self.data_logs.add_logs(
            key="field_assert",
            val=[f"=== 查询结果: ===", query_result]
        )

        for assert_field_obj in assert_field_list:
            """
            assert_field_obj = {
                "assert_key": "id",
                "expect_val": 1,
                "is_expression": 0,
                "python_val_exp": "",
                "expect_val_type": "int",
                "rule": "=="
            }
            """
            print('assert_field_obj:', assert_field_obj)
            expect_val_type = assert_field_obj.get('expect_val_type')  # 期望值类型
            expect_val = assert_field_obj.get('expect_val')  # 期望值
            is_expression = assert_field_obj.get('is_expression')
            py_func = value_type_dict.get(str(expect_val_type))  # 反射原生方法
            assert_field_obj['expect_val'] = py_func(expect_val)  # 期望值强转类型重新赋值: 如 int(1)

            if db_type in ('mysql', 'postgresql', 'sqlserver'):  # TODO 暂时支持唯一数据检验
                qr = query_result
                if qr and isinstance(qr, list):
                    sql_query_result = qr[0]
                else:
                    sql_query_result = {}
                ass_result = await self.ass_dict_consume(
                    assert_description=assert_description,
                    query_result=sql_query_result,
                    assert_field_obj=assert_field_obj
                )
                await self.set_count(ass_result)

            elif db_type in ('redis',):
                qr = query_result
                if qr:
                    redis_query_result = json.loads(qr)
                else:
                    redis_query_result = {}
                if isinstance(redis_query_result, (dict, list)) and bool(is_expression):
                    ass_result = await self.ass_dict_consume(
                        assert_description=assert_description,
                        query_result=redis_query_result,
                        assert_field_obj=assert_field_obj
                    )
                    await self.set_count(ass_result)
                else:
                    ass_result = await self.ass_str_or_int_consume(
                        assert_description=assert_description,
                        query_result=redis_query_result,
                        assert_field_obj=assert_field_obj
                    )
                    await self.set_count(ass_result)
            else:
                await self.data_logs.add_logs(
                    key="field_assert",
                    val=f"=== 暂未支持数据库:{db_type} ==="
                )

    async def ping_db_connection(self, db_id, assert_description, name, db_type, db_connection):
        """
        检查db是否可以连接
        :param db_id: 数据库id
        :param assert_description: 断言描述
        :param name: 数据库名称
        :param db_type: 数据库类型
        :param db_connection: 数据库连接配置
        :return:
        """

        db_obj = self.db_dict.get(db_type.lower())

        if not db_obj:
            error_message = f"=== 数据断言:{assert_description} 使用ID为 {db_id} 的数据库数据类型: {db_type} 暂不支持 ==="
            await self.data_logs.add_logs(
                key="field_assert",
                val=error_message
            )
            self.sio.log(error_message, status='error')
            return False
        else:
            try:
                return db_obj(**db_connection)
            except BaseException as e:
                error_message = f"=== 数据断言:{assert_description} 数据库: {db_id}-{name} 连接失败 ==="
                await self.data_logs.add_logs(
                    key="field_assert",
                    val=error_message
                )
                self.sio.log(f'{error_message},{e}', status='error')
                return False

    async def ass_json_untie(self, assert_description, ass_json):
        """
        断言
        :return:
        """

        for index, ass in enumerate(ass_json):
            db_id = ass.get('db_id')
            sql = f"""SELECT * FROM exile_test_databases WHERE id={db_id} and is_deleted=0;"""
            query_db = project_db.select(sql=sql, only=True)

            if query_db:  # 检查db配置是否存在或者是否可用
                name = query_db.get('name')
                db_type = query_db.get('db_type')
                db_connection = query_db.get('db_connection')
                ping_result = await self.ping_db_connection(db_id, assert_description, name, db_type, db_connection)

                if ping_result:
                    # print('ping_result', ping_result, json.dumps(ass, ensure_ascii=False))
                    assert_list = ass.get('assert_list')
                    [
                        await self.main_assert(
                            assert_description=assert_description,
                            ass=ass,
                            db_result=ping_result,
                            db_type=db_type
                        ) for ass in assert_list
                    ]

            else:
                error_message = f"=== 数据断言:{assert_description} 使用ID为 {db_id} 的数据库不存在或禁用 ==="
                await self.data_logs.add_logs(
                    key="field_assert",
                    val=error_message
                )
                self.sio.log(error_message, status='error')
                self.count['fail'] += 1

    async def main(self):
        """main"""

        print('=== AsyncAssertionField ===')
        await self.data_logs.add_logs(
            key="field_assert",
            val="=== 字段断言 ==="
        )
        for field_ass in self.case_field_ass_info:
            assert_description = field_ass.get('assert_description')
            ass_json = field_ass.get('ass_json')
            await self.ass_json_untie(assert_description=assert_description, ass_json=ass_json)

        self.count['flag'] = False if self.count.get('fail') > 0 else True
        return self.count
