# -*- coding: utf-8 -*-
# @Time    : 2021/9/1 5:20 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : assert_related.py
# @Software: PyCharm


from loguru import logger

from common.libs.db import MyPyMysql


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
                 expect_val=None, expect_val_type=None, is_expression=None, python_val_exp=None, db_id=None, sql=None,
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
        self.sql = sql
        self.assert_list = assert_list
        if self.db_id:
            # TODO 通过db_id在数据库配置表中查出对应的数据可以配置
            # TODO ping通该需要断言的数据库后执行测试的sql,否则返回False
            DB = {
                # 'user': CONFIG_OBJ.MYSQL_USERNAME,
                # 'password': CONFIG_OBJ.MYSQL_PASSWORD,
                # 'host': CONFIG_OBJ.MYSQL_HOSTNAME,
                # 'port': CONFIG_OBJ.MYSQL_PORT,
                # 'db': CONFIG_OBJ.MYSQL_DATABASE
            }
            self.db = MyPyMysql(**DB)

    def get_resp_this_val(self):
        """用键获取需要断言的值"""
        if self.is_expression:  # 公式取值
            pass
        else:  # 直接常规取值:紧限于返回值的第一层键值对如:{"code":200,"message":"ok"}
            self.this_val = self.resp_json.get(self.assert_key)

    def assert_resp_main(self):
        """
        resp断言
        :this_val: 当前值
        :rule: 规则
        :expect_val_type: 期望值类型
        :expect_val: 期望值
        """
        self.get_resp_this_val()

        try:
            __expect_val = self.this_val
            """
            解析:
            this_val = 1
            rule = rule_dict.get('1')
            expect_val = 1
            bool(getattr(a, rule)(expect_val)) 等价 bool(this_val == expect_val) 
            this_val == expect_val
            """
            logger.info('=== 断言:{} ==='.format(self.assert_description))
            logger.info('{} {} {}'.format(self.this_val, self.rule, __expect_val))
            __assert_bool = getattr(self.this_val, self.rule)(__expect_val)
            if isinstance(__assert_bool, bool) and __assert_bool:
                # print('true')
                return True, '断言通过'
            else:
                # print('false')
                return False, '断言失败'

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
                    "expect_val": "1",
                    "expect_val_type": "1",
                    "rule": "="
                }
            ],
            "sql": "SELECT * FROM exilic_test_case WHERE id=1;"
        }
        new_ass = AssertMain(
            assert_description="Field通用断言",
            **field_ass_dict
        )
        field_ass_result = new_ass.assert_field_main()
        print(field_ass_result)
