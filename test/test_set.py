# -*- coding: utf-8 -*-
# @Time    : 2021/11/11 9:37 上午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_set.py
# @Software: PyCharm


l1 = [1, 2, 3]
l2 = [1, 2, 7, 8, 9]

# 交集(激活)
jj = list(set(l1).intersection(set(l2)))
print("交集(激活)", jj)

# 并集
bj = list(set(l1).union(set(l2)))
print("并集", bj)

# 差集
cj1 = list(set(l1).difference(set(l2)))
cj2 = list(set(l2).difference(set(l1)))
print("l1的差集", cj1)
print("l2的差集", cj2)

if __name__ == '__main__':
    pass
