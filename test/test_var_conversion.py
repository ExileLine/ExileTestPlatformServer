# -*- coding: utf-8 -*-
# @Time    : 2021/9/1 8:13 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_var_conversion.py
# @Software: PyCharm


from common.libs.CaseDrivenResult import CaseDrivenResult

if __name__ == '__main__':
    d1 = "前面${username}后面"
    d2 = "前面${user_id}后面${username}还有啊"
    d3 = {
        "user_id": "${user_id}",
        "username": "${username}"
    }
    d4 = ["${user_id}", "${username}"]
    d5 = {'url': 'http://127.0.0.1:7272/api', 'headers': {}, 'data': {}}
    d6 = {'url': 'http://127.0.0.1:7272/api', 'headers': {}, 'data': {"key": "${user_id}"}}
    d7 = {'url': 'http://127.0.0.1:7272/api', 'headers': {}, 'data': {"key": "${aaa}"}}
    print(CaseDrivenResult.var_conversion(d1))
    print(CaseDrivenResult.var_conversion(d2))
    print(CaseDrivenResult.var_conversion(d3))
    print(CaseDrivenResult.var_conversion(d4))

    result5 = CaseDrivenResult.var_conversion(d5)
    result6 = CaseDrivenResult.var_conversion(d6)
    result7 = CaseDrivenResult.var_conversion(d7)
    print(result5, type(result5))
    print(result6, type(result6))
    print(result7, type(result7))
