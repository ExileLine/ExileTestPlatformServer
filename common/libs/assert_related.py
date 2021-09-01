# -*- coding: utf-8 -*-
# @Time    : 2021/9/1 5:20 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : assert_related.py
# @Software: PyCharm


class AssertMain:
    """
    eq     :equal（等于）
    gt     :greater than（大于）
    ge     :greater and equal（大于等于）
    lt     :less than（小于）
    le     :less and equal（小于等于）
    ne     :not equal (不等于)
    """

    rule_dict = {
        '1': '__eq__',
        '2': '__gt__',
        '3': '__ge__',
        '4': '__lt__',
        '5': '__le__',
        '6': '__ne__'
    }

    expect_val_type_dict = {
        '1': 'int',
        '2': 'str',
        '3': 'list',
        '4': 'dict'
    }

    def __init__(self, this_val, expect_val, rule, expect_val_type):
        self.this_val = this_val
        self.expect_val = expect_val
        self.rule = self.rule_dict.get(rule, '')
        self.expect_val_type = self.expect_val_type_dict.get(expect_val_type, '')

    def check_dict_val(self):
        """检查"""

        if not hasattr(self.this_val, self.rule):
            print('rule_dict 不存在 key: {}'.format(self.rule))
            return False
        if not hasattr(self.expect_val, '__{}__'.format(self.expect_val_type)):
            print('expect_val_type_dict 不存在 key: {}'.format(self.expect_val_type))
            return False

        return True

    def assert_main(self):
        """
        断言
        :this_val: 当前值
        :rule: 规则
        :expect_val_type: 期望值类型
        :expect_val: 期望值
        """

        if self.check_dict_val():
            try:
                """
                等价于以下三种
                int(expect_val)
                getattr(expect_val, '__int__')()
                expect_val.__int__()
                """
                __expect_val = getattr(self.expect_val, '__{}__'.format(self.expect_val_type))()
                print(__expect_val, type(__expect_val))

                """
                解析:
                this_val = 1
                rule = rule_dict.get('1')
                expect_val = 1
                bool(getattr(a, rule)(expect_val)) 等价 bool(this_val == expect_val) 
                this_val == expect_val
                """
                print('{} {} {}'.format(self.this_val, self.rule, __expect_val))
                __assert_bool = getattr(self.this_val, self.rule)(__expect_val)
                if isinstance(__assert_bool, bool) and __assert_bool:
                    print('true')
                    return True, '断言通过'
                else:
                    print('false')
                    return False, '断言失败'

            except BaseException as e:
                return False, str(e)

        else:
            return False, "参数异常"


if __name__ == '__main__':
    am = AssertMain(this_val=1, rule='1', expect_val_type='1', expect_val=1)
    am.assert_main()
