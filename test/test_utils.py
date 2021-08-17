# -*- coding: utf-8 -*-
# @Time    : 2021/8/17 4:43 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_utils.py
# @Software: PyCharm

from common.libs.utils import AssertMain

am = AssertMain(this_val=1, rule='1', expect_val_type='1', expect_val=1)
am.ass_resp_main()
am1 = AssertMain(this_val=1, rule='1', expect_val_type='14', expect_val=1)
am1.ass_resp_main()

if __name__ == '__main__':
    pass
