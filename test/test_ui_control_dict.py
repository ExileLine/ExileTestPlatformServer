# -*- coding: utf-8 -*-
# @Time    : 2023/5/11 16:34
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test_ui_control_dict.py
# @Software: PyCharm


import json

from common.libs.data_dict import UiControlDict

if __name__ == '__main__':
    res1 = UiControlDict.get_uc_dict()
    print(json.dumps(res1, ensure_ascii=False))

    res2 = UiControlDict.get_uc_mapping()
    print(json.dumps(res2, ensure_ascii=False))
