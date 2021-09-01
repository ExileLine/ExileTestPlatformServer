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
    print(CaseDrivenResult.var_conversion(d1))
    print(CaseDrivenResult.var_conversion(d2))
    print(CaseDrivenResult.var_conversion(d3))
    print(CaseDrivenResult.var_conversion(d4))
