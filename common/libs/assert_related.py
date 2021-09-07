# -*- coding: utf-8 -*-
# @Time    : 2021/9/1 5:20 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : assert_related.py
# @Software: PyCharm

import redis
from loguru import logger

from common.libs.db import MyPyMysql
from app.models.test_case_config.models import TestDatabases


class ReturnDB:
    """获取DB"""

    def __init__(self, db_id=None):
        self.db_id = db_id
        self.db_type = None
        self.db_connection = None

    def check_db(self):
        """检查是否存在该db的连接配置"""

        # <----------调试代码---------->
        from ApplicationExample import create_app
        app = create_app()
        with app.app_context():
            query_db = TestDatabases.query.get(self.db_id)
        # <----------调试代码---------->

        if query_db:
            db_obj = query_db.to_json()
            db_type = db_obj.get('db_type')
            db_connection = db_obj.get('db_connection')
            self.db_type = db_type
            self.db_connection = db_connection
            return True
        else:
            return False

    def get_mysql(self):
        """mysql"""
        db = MyPyMysql(**self.db_connection, debug=True)  # MySql实例
        ping = db.db_obj().open
        return db

    def get_redis(self):
        """redis"""
        pool = redis.ConnectionPool(**self.db_connection)
        db = redis.Redis(connection_pool=pool)  # Redis实例
        db.ping()
        return db

    def main(self):
        """main"""
        db_dict = {
            "mysql": self.get_mysql,
            "redis": self.get_redis
        }
        if self.check_db() and self.db_type:
            print(self.db_connection, type(self.db_connection))
            return db_dict.get(self.db_type.lower())()
        else:
            return None


class AssertMain:
    """
    eq     :equal（等于）
    gt     :greater than（大于）
    ge     :greater and equal（大于等于）
    lt     :less than（小于）
    le     :less and equal（小于等于）
    ne     :not equal (不等于)
    contains: in
    """

    rule_dict = {
        '=': '__eq__',
        '>': '__gt__',
        '>=': '__ge__',
        '<': '__lt__',
        '<=': '__le__',
        '!=': '__ne__',
        'in': '__contains__'
    }

    def __init__(self, resp_json=None, resp_headers=None, assert_description=None, assert_key=None, rule=None,
                 expect_val=None, expect_val_type=None, is_expression=None, python_val_exp=None, db_id=None, query=None,
                 assert_list=None):

        self.resp_json = resp_json
        self.resp_headers = resp_headers

        """resp ass"""
        self.assert_description = assert_description
        self.this_val = None
        self.assert_key = assert_key
        self.rule = self.rule_dict.get(rule, '')  # 转换
        self.expect_val = expect_val
        self.expect_val_type = expect_val_type
        self.is_expression = is_expression
        self.python_val_exp = python_val_exp

        """field ass"""
        self.db_id = db_id
        self.query = query
        self.assert_list = assert_list
        self.db_type = None
        self.test_db = None
        if self.db_id:
            try:
                self.test_db = ReturnDB(db_id=self.db_id).main()
            except BaseException as e:
                logger.error("=== 连接:{}-db 失败:{} === ".format(self.db_type, str(e)))

    def get_resp_this_val(self):
        """用键获取需要断言的值"""
        if self.is_expression:  # 公式取值
            pass
            # TODO 公式取值
        else:  # 直接常规取值:紧限于返回值的第一层键值对如:{"code":200,"message":"ok"}
            self.this_val = self.resp_json.get(self.assert_key)

    def assert_resp_main(self):
        """
        resp断言
        :this_val: 当前值
        :rule: 规则
        :expect_val_type: 期望值类型
        :expect_val: 期望值
        ps:如果该方法报错,是参数在入库的时候接口没有做好检验或者手动修改了数据库的数据
        """
        self.get_resp_this_val()

        try:
            """
            解析:
            this_val = 1
            rule = rule_dict.get('1')
            expect_val = 1
            bool(getattr(a, rule)(expect_val)) 等价 bool(this_val == expect_val) 
            this_val == expect_val
            """
            logger.info('=== 断言:{} ==='.format(self.assert_description))
            message = '{}:{} {} {}:{}'.format(
                self.this_val,
                type(self.this_val),
                self.rule,
                self.expect_val,
                type(self.expect_val)
            )
            logger.info(message)
            __assert_bool = getattr(self.this_val, self.rule)(self.expect_val)
            if isinstance(__assert_bool, bool) and __assert_bool:
                logger.success('=== 断言通过 ===')
                return {
                    "status": True,
                    "message": message
                }
            else:
                logger.error('=== 断言失败 ===')
                return {
                    "status": False,
                    "message": message
                }

        except BaseException as e:
            return False, str(e)

    def assert_field_main(self):
        """
        field断言
        :this_val: 当前值
        :rule: 规则
        :expect_val_type: 期望值类型
        :expect_val: 期望值
        """
        query_result = self.test_db.select(self.query, only=True)
        print(query_result)

        def __ass_dict_result():
            """
            查询结果为一个dict,检验key:value
            ps:如果该方法报错,是参数在入库的时候接口没有做好检验或者手动修改了数据库的数据
            """
            for ass in self.assert_list:
                print(ass)
                __key = ass.get('assert_key')
                print(__key)
                __result_key = query_result.get(__key)
                print(__result_key)

                this_val = __result_key
                __rule = self.rule_dict.get(ass.get('rule'), '')
                __expect_val = ass.get('expect_val')
                logger.info('=== 断言:{} ==='.format(self.assert_description))
                logger.info(
                    '{}:{} [{}.{}] {}:{}'.format(
                        this_val, type(this_val), ass.get('rule'), __rule, __expect_val, type(__expect_val))
                )
                __assert_bool = getattr(this_val, __rule)(__expect_val)
                print(__assert_bool)
                if isinstance(__assert_bool, bool) and __assert_bool:
                    logger.success('=== 断言通过 ===')
                    return True, '断言通过'
                else:
                    logger.error('=== 断言失败 ===')
                    return False, '断言失败'

            return

        def __ass_list_result():
            """
            查询结果为一个[],检验:=,>,>=,<,<=,in,not in
            ps:如果该方法报错,是参数在入库的时候接口没有做好检验或者手动修改了数据库的数据
            """

            return

        __ass_dict_result()

    def go_test(self):
        """调试"""
        print('\n'.join(['%s:%s' % item for item in self.__dict__.items()]))


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
            "rule": "=",
            "assert_key": "code",
            "expect_val": 200,
            "is_expression": 0,
            "python_val_exp": "okc.get('a').get('b').get('c')[0]",
            "expect_val_type": "1"
        }
        new_ass = AssertMain(
            resp_json=resp_json,
            resp_headers=resp_headers,
            assert_description="Resp通用断言",
            **resp_ass_dict
        )
        resp_ass_result = new_ass.assert_resp_main()
        print(resp_ass_result)


    def test_field_ass():
        """测试断言field"""
        field_ass_dict = {
            "assert_list": [
                {
                    "assert_key": "id",
                    "expect_val": 1,
                    "expect_val_type": "1",
                    "rule": "="
                },
                {
                    "assert_key": "id",
                    "expect_val": 2,
                    "expect_val_type": "1",
                    "rule": "="
                }
            ],
            "db_id": 1,
            "query": "select * from ExilicTestPlatform.exilic_test_case where id=1;"
        }

        new_ass = AssertMain(
            assert_description="Field通用断言",
            **field_ass_dict
        )
        field_ass_result = new_ass.assert_field_main()


    test_field_ass()
    # print(ReturnDB(db_id=1).main().select("""select * from ExilicTestPlatform.exilic_test_case where id=1;"""))
