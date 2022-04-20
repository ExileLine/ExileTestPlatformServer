# -*- coding: utf-8 -*-
# @Time    : 2021/9/1 8:13 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_var_conversion.py
# @Software: PyCharm


import json
from common.libs.CaseDrivenResult import MainTest

if __name__ == '__main__':
    d0 = "${resp响应断言引用}"
    d1 = "前面${token}后面"
    d2 = "前面${user_id}后面${token}还有啊${okc}"
    d3 = {
        "user_id": "${user_id}",
        "token": "${token}",
        "aaa": "${okc}",
        "bbb": "${yyx9999}"
    }
    d4 = ["${user_id}", "${username}"]
    d5 = {'url': 'http://127.0.0.1:7272/api', 'headers': {}, 'data': {}}
    d6 = {'url': 'http://127.0.0.1:7272/api', 'headers': {}, 'data': {"key": "${user_id}"}}
    d7 = {'url': 'http://127.0.0.1:7272/api', 'headers': {}, 'data': {"key": "${aaa}"}}
    d8 = {'url': 'http://127.0.0.1:7272/api', 'headers': {}, 'data': {"key": "${resp响应断言引用}"}}

    m = MainTest()
    # r0 = m.var_conversion(d0)
    # print('=', r0, type(r0))
    # print(m.var_conversion(d1))
    # print(m.var_conversion(d2))
    # print(m.var_conversion(d3))
    # print(m.var_conversion(d4))

    # result5 = m.var_conversion(d5)
    # print(result5, type(result5))
    #
    # result6 = m.var_conversion(d6)
    # print(result6, type(result6))
    #
    # result7 = m.var_conversion(d7)
    # print(result7, type(result7))
    #
    # result8 = m.var_conversion(d8)
    # print(result8, type(result8))

    # m._var_conversion(d3)

    import re
    from common.libs.db import project_db


    def yyx(d3):
        """1"""
        json_str = json.dumps(d3, ensure_ascii=False)
        var_name_list = re.findall('\\$\\{([^}]*)', json_str)
        print(var_name_list)
        sql = f"""
                select id, var_name, var_value, var_type, is_active 
                from exile_test_variable 
                where {f"var_name in {tuple(var_name_list)}" if len(var_name_list) > 1 else f"var_name='{var_name_list[-1]}'"} and is_deleted=0;
                """
        query_result = project_db.select(sql=sql)
        d = {}
        for val in query_result:
            d[val.get('var_name')] = val.get('var_value')
        print(d)
        findall_list = re.findall(r'\$\{(.*?)\}(.*?")', json_str)
        print(findall_list)
        if findall_list:
            print('=' * 100)
            for i in findall_list:
                print(i)
                _key = i[0]
                print(_key)
                _val = d[_key]
                print(_val)
                if _val:
                    print('val:', _val)
                    if i[1] and i[1] != '"':
                        print('1====')
                        _j = json.dumps(_val, ensure_ascii=False)
                        json_str = json_str.replace('"${' + _key + '}"', _j.replace('"', '\\"'))
                        print(json_str)
                    else:
                        if isinstance(_val, (dict, list)):
                            print('2====')
                            _j = json.dumps(_val, ensure_ascii=False)
                            json_str = json_str.replace('"${' + _key + '}"', _j)
                            print(json_str)
                        elif isinstance(_val, str):
                            print('4====')
                            json_str = json_str.replace('"${' + _key + '}"', _val)
                            print(json_str)
                        else:
                            print('3====')
                            _j = json.dumps(_val, ensure_ascii=False)
                            json_str = json_str.replace('"${' + _key + '}"', _j)
                            print(json_str)

                        # return "${" + _key + "}"

        return json.loads(json_str)


    yyx(d3)
