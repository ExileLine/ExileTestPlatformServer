# -*- coding: utf-8 -*-
# @Time    : 2022/7/25 09:52
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : my_md5.py
# @Software: PyCharm

import json
import hashlib


def my_md5(data):
    """md5"""

    encode_value = str.encode(data)
    # print(encode_value)
    m = hashlib.md5()
    m.update(encode_value)
    r = m.hexdigest()
    return r


if __name__ == '__main__':
    d = {
        "a": "好的",
        "b": "嗯嗯"
    }
    val = json.dumps(d, ensure_ascii=False)
    res = my_md5(val)
    print(res)
