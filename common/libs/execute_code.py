# -*- coding: utf-8 -*-
# @Time    : 2021/9/12 12:54 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : execute_code.py
# @Software: PyCharm

from requests import structures


def execute_code(code, data):
    """

    :param code: 取值公式(Python)
    :param data: 取值数据源
    :return:
    """
    __obj = data

    if isinstance(__obj, dict):
        rs = code.split('.')
        rs[0] = '__obj'
        new_rule_str = '.'.join(rs)
    elif isinstance(__obj, list):
        rs = code.split("[")
        rs[0] = '__obj'
        new_rule_str = '['.join(rs)
    elif isinstance(__obj, str):
        # todo 切片,函数,正则
        # d = data_self
        # rs = rule_str.split("[")
        # rs[0] = 'd'
        new_rule_str = code
    elif isinstance(__obj, structures.CaseInsensitiveDict):
        __obj = dict(__obj)
        rs = code.split('.')
        rs[0] = '__obj'
        new_rule_str = '.'.join(rs)
    else:
        raise TypeError("取值参数类型应该为:JSON,Dict,List,Str 而不是: {}".format(type(__obj)))

    # print("exec:{}".format(new_rule_str))

    try:
        _locals = locals()
        # print(_locals)
        # print(globals())
        exec(f"""rule_result={new_rule_str}""", globals(), _locals)
        rule_result = _locals['rule_result']

        print('数据源:', __obj)
        print('表达式:', new_rule_str)
        print('结果:', rule_result)

        if rule_result:
            resp_data = {
                "bool": True,
                "message": f"操作成功:{new_rule_str}",
                "result_data": rule_result
            }
            return resp_data

        else:
            resp_data = {
                "bool": False,
                "message": "取值为空",
                "result_data": None
            }
            return resp_data
    except BaseException as e:
        resp_data = {
            "bool": False,
            "message": f"取值公式错误:{str(e)}",
            "result_data": None
        }
        return resp_data


if __name__ == '__main__':
    c1 = "okc.get('a').get('b').get('c')[0]"
    d1 = {
        "a": {
            "b": {
                "c": [
                    "abc",
                    2,
                    3
                ]
            }
        }
    }
    print(execute_code(code=c1, data=d1))

    print('-' * 33)
    c2 = "okc[2].get('c')"
    d2 = [{"a": "123"}, {"b": "456"}, {"c": {"b": [1, 2, 3, 4]}}]
    print(execute_code(code=c2, data=d2))

    print('-' * 33)


    class A:
        pass


    c3 = ""
    a = A()
    execute_code(code=c3, data=a)
