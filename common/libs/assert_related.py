# -*- coding: utf-8 -*-
# @Time    : 2021/9/1 5:20 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : assert_related.py
# @Software: PyCharm

import redis

from app.models.test_case_config.models import TestDatabases
from common.libs.db import MyPyMysql
from common.libs.execute_code import execute_code
from common.libs.StringIOLog import StringIOLog
from common.libs.data_dict import rule_dict


class AssertMain:
    """
    断言类
    """

    @classmethod
    def get_assert(cls, this_val, rule, expect_val):
        """
        断言
        :param this_val: 当前值
        :param rule: 规则比较符
        :param expect_val: 期望值
        :return:
        """
        this_val_type = type(this_val)
        expect_val_type = type(expect_val)

        if not this_val_type == expect_val_type:
            raise TypeError("当前值:{} 类型:{} 与 期望值:{} 类型:{} 不一致,无法用于比较.".format(
                this_val, expect_val_type, expect_val, expect_val_type
            ))
        if not hasattr(this_val, rule):
            raise AttributeError("当前值:{} 没有属性:{}".format(this_val, rule))

        result = getattr(this_val, rule)(expect_val)

        return result

    def go_test(self):
        """调试"""
        print('\n'.join(['%s:%s' % item for item in self.__dict__.items()]))


class AssertResponseMain(AssertMain):
    """Response 断言类"""

    def __init__(self, sio=None, resp_json=None, resp_headers=None, assert_description=None, assert_key=None, rule=None,
                 expect_val=None, expect_val_type=None, is_expression=None, python_val_exp=None):
        self.sio = sio if sio else StringIOLog()
        self.resp_json = resp_json
        self.resp_headers = resp_headers
        self.assert_description = assert_description
        self.this_val = None
        self.assert_key = assert_key
        self.rule = rule
        self.expect_val = expect_val
        self.expect_val_type = expect_val_type
        self.is_expression = is_expression
        self.python_val_exp = python_val_exp

    def set_this_val(self):
        """
        用键获取需要断言的值
        :return:
        """
        if self.is_expression:  # 公式取值
            result_json = execute_code(code=self.python_val_exp, data=self.resp_json)
            result = result_json.get('result_data')
            self.sio.log("=== 公式取值结果: {} ===".format(result))
            self.this_val = result

        else:  # 直接常规取值:紧限于返回值的第一层键值对如:{"code":200,"message":"ok"}
            self.this_val = self.resp_json.get(self.assert_key)

    def main(self):
        """
        resp断言
        :this_val: 当前值
        :rule: 规则
        :expect_val_type: 期望值类型
        :expect_val: 期望值
        ps:如果该方法报错,是参数在入库的时候接口没有做好检验或者手动修改了数据库的数据
        """
        self.set_this_val()

        self.sio.log('=== 断言:{} ==='.format(self.assert_description))
        self.sio.log('=== 键值:{} ==='.format({self.assert_key: self.this_val}))
        message = '{}:{} {} {}:{}'.format(
            self.this_val,
            type(self.this_val),
            self.rule,
            self.expect_val,
            type(self.expect_val)
        )
        self.sio.log(message)

        try:
            rule = rule_dict.get(self.rule)  # 从字典中取出反射的规则函数
            if self.get_assert(this_val=self.this_val, rule=rule, expect_val=self.expect_val):
                self.sio.log('=== 断言通过 ===', status='success')
                return {
                    "status": True,
                    "message": message
                }
            else:
                self.sio.log('=== 断言失败 ===', status="error")
                return {
                    "status": False,
                    "message": message
                }
        except BaseException as e:
            self.sio.log('数据异常:{}'.format(str(e)), status='error')
            self.sio.log('这种情况一般会因为以下两种原因导致:', status='error')
            self.sio.log('1.查看数据库确认该数据是否有被手动修改过.', status='error')
            self.sio.log(
                '2.查看: case_ass_rule_api.py 中的 RespAssertionRuleApi 中的逻辑是否被修改.',
                status='error')
            self.sio.log('=== 断言异常 ===', status="error")
            return {
                "status": False,
                "message": message
            }


class AssertFieldMain(AssertMain):
    """Field 断言类"""

    def __init__(self, sio=None, resp_json=None, resp_headers=None, assert_description=None, db_id=None, query=None,
                 assert_list=None):
        self.sio = sio if sio else StringIOLog()
        self.resp_json = resp_json
        self.resp_headers = resp_headers
        self.assert_description = assert_description
        self.db_id = db_id
        self.query = query
        self.assert_list = assert_list

        self.current_db_type = None
        self.current_db_connection = {}
        self.current_db_obj = None

        self.query_result_status = None
        self.ass_field_success = []
        self.ass_field_fail = []
        self.ass_field_error = []

        self.db_dict = {
            "mysql": self.get_mysql,
            "redis": self.get_redis,
            "postgresql": self.get_postgresql,
            "mongodb": self.get_mongodb,
            'es': self.get_es,
            "oracle": self.get_oracle,
            "db2": self.get_db2
        }

    def get_mysql(self):
        """连接:Mysql"""

        db = MyPyMysql(**self.current_db_connection, debug=True)  # MySql实例
        ping = db.db_obj().open
        return db

    def get_redis(self):
        """连接:Redis"""

        pool = redis.ConnectionPool(**self.current_db_connection)
        db = redis.Redis(connection_pool=pool)  # Redis实例
        db.ping()
        return db

    def get_postgresql(self):
        """连接:PostgreSQL"""

    def get_mongodb(self):
        """连接:Mongodb"""

    def get_es(self):
        """连接:ES"""

    def get_oracle(self):
        """连接:Oracle"""

    def get_db2(self):
        """连接:DB2"""

    def query_db_connection(self):
        """查询db配置是否存在或者可用"""

        from ApplicationExample import create_app
        app = create_app()
        with app.app_context():
            query_db = TestDatabases.query.get(self.db_id)

        if not query_db or query_db.is_deleted != 0:
            self.sio.log(f"=== 数据库不存在或禁用: {self.db_id} === ", status='error')
            self.ass_field_error.append('数据库不存在或禁用')
            return False

        db_obj = query_db.to_json()
        self.current_db_type = db_obj.get('db_type', '')
        self.current_db_connection = db_obj.get('db_connection')
        return True

    def ping_db_connection(self):
        """检查db是否可以连接"""

        self.current_db_obj = self.db_dict.get(self.current_db_type.lower(), None)()

        if not self.current_db_obj:
            self.sio.log(f"=== 暂时不支持: {self.current_db_type} ===", status='error')
            self.ass_field_error.append('暂时不支持')
            return False

        self.sio.log(f"=== 测试需要连接的db配置: {self.current_db_connection} - {type(self.current_db_connection)} ===")

    def execute_order(self):
        """执行语句"""

        result = self.current_db_obj.select(self.query)

        return result

    def ass_dict_result(self, query_result):
        """
        查询结果为一个dict,检验key:value
        ps:如果该方法报错,问题会出现在 参数在入库的时候接口没有做好检验 或 者手动修改了数据库的数据
        """
        for ass in self.assert_list:
            # print(ass)
            __key = ass.get('assert_key')
            # print(__key)
            __result_key = query_result.get(__key)
            # print(__result_key)
            __rule = ass.get('rule')
            __expect_val = ass.get('expect_val')

            self.sio.log('=== 断言:{} ==='.format(self.assert_description))
            self.sio.log('=== 字段:{} ==='.format(__key))
            message = '{}:{} [{}] {}:{}'.format(
                __result_key, type(__result_key), __rule, __expect_val, type(__expect_val)
            )
            self.sio.log(message)

            try:
                rule = rule_dict.get(__rule)  # 从字典中取出反射的规则函数
                if self.get_assert(this_val=__result_key, rule=rule, expect_val=__expect_val):
                    self.sio.log('=== 断言通过 ===', status='success')
                    self.ass_field_success.append(message)
                else:
                    self.sio.log('=== 断言失败 ===', status='error')
                    self.ass_field_fail.append(message)

            except BaseException as e:
                self.sio.log('数据异常:{}'.format(str(e)), status='error')
                self.sio.log('这种情况一般会因为以下两种原因导致:', status='error')
                self.sio.log('1.查看数据库确认该数据是否有被手动修改过.', status='error')
                self.sio.log(
                    '2.查看: case_ass_rule_api.py 中的 FieldAssertionRuleApi 中的逻辑是否被修改.',
                    status='error')
                self.sio.log('=== 断言异常 ===', status="error")
                self.ass_field_error.append(message)

        return {
            "success": len(self.ass_field_success),
            "fail": len(self.ass_field_fail),
            "error": len(self.ass_field_error)
        }

    def ass_list_result(self, query_result):
        """
        查询结果为一个[],检验:=,>,>=,<,<=,in,not in
        ps:如果该方法报错,是参数在入库的时候接口没有做好检验或者手动修改了数据库的数据
        """
        # TODO ass_list_result
        return

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
            self.execute_order()

            query_result = self.execute_order()
            result = self.ass_dict_result(query_result)
            # result = self.ass_list_result(query_result) # TODO ass_list_result
            return result

        except BaseException as e:
            self.sio.log("=== {} ===".format(str(e)), status='error')
            result = {
                "success": len(self.ass_field_success),
                "fail": len(self.ass_field_fail),
                "error": len(self.ass_field_error)
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
            "data": 1630586912.8031318,
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
        field_ass_dict = {
            "assert_list": [
                {
                    "assert_key": "id",
                    "expect_val": 1,
                    "expect_val_type": "1",
                    # "rule": "__eq__",
                    "rule": "=="
                },
                {
                    "assert_key": "case_name",
                    "expect_val": "测试用例B1",
                    "expect_val_type": "2",
                    # "rule": "__eq__",
                    "rule": "=="
                }
            ],
            "db_id": 1,
            "query": "select * FROM ExileTestPlatform.exile_test_case WHERE id=1;"
        }

        new_ass = AssertFieldMain(
            assert_description="Field通用断言",
            **field_ass_dict
        )
        field_ass_result = new_ass.main()


    """test"""
    # test_resp_ass()
    # test_field_ass()
    # print(ReturnDB(db_id=1).main().select("""select * from ExilicTestPlatform.exile_test_case where id=1;"""))
