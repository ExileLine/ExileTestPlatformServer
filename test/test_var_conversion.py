# -*- coding: utf-8 -*-
# @Time    : 2021/9/1 8:13 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_var_conversion.py
# @Software: PyCharm

import json
from common.libs.CaseDrivenResult import MainTest

d0 = "${token}"
d1 = "前面${token}后面"
d2 = "数字${token}字符串${yyx9999}列表${user_id}字典${okc}"
d3 = "数字${token}字符串${yyx9999}列表${user_id}字典${okc}未找到的${test_none}"
d4 = {
    "test_int": "${token}",
    "test_str": "${yyx9999}",
    "test_dict": "${okc}",
    "test_list": "${user_id}",
    "test_none": "${test_none}"
}
d5 = ["${token}", "${yyx9999}", "${okc}", "${user_id}", "${test_none}", 999, "yang"]

d6_1 = 8888
d6_2 = "yyx"
d6_3 = {'url': 'http://127.0.0.1:7272/api', 'headers': {}, 'data': {}}  #
d6_4 = [1, "a", {"k": "v"}, [{"k": "v"}, [1, 2, 3]]]  #

d7 = {'url': 'http://127.0.0.1:7272/api', 'headers': {}, 'data': d4}
d8 = {'url': 'http://127.0.0.1:7272/api', 'headers': d4, 'data': d4}
d9 = {"data": "前面${user_id}后面${token}还有啊${okc}"}
d10 = "${token}${token}${token}"
d11 = "${token}"

d = {
    "token": 123456,
    "yyx9999": "okc",
    "test_dict": {"a": 1, "b": "okc", "c": {"x": "y"}, "d": [1, {"p": "l"}, []]},
    "test_list": [{"k": "v"}]
}

m = MainTest()


def t(data):
    test = m.var_conversion(data)
    print(test, type(test))


if __name__ == '__main__':
    pass
    # test_000 = t(999)
    # test_000 = t(d0)
    # test_001 = t(d1)
    # test_002 = t(d2)
    # test_003 = t(d3)
    # test_004 = t(d4)
    # test_005 = t(d5)
    # test_006_1 = t(d6_1)
    # test_006_2 = t(d6_2)
    # test_006_3 = t(d6_3)
    # test_006_4 = t(d6_4)
    # test_007 = t(d7)
    # test_008 = t(d8)
    # test_009 = t(d9)
    # test_010 = t(d10)
    # test_011 = t(d11)
