# -*- coding: utf-8 -*-
# @Time    : 2021/9/20 10:26 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_stringIO.py
# @Software: PyCharm


from common.libs.StringIOLog import StringIOLog

if __name__ == '__main__':
    sio = StringIOLog()
    r = []
    for i in range(10, 21):
        sio.log(i)
        r.append(sio.get_stringio())
    print(r)
    sio.log('999')
    print(sio.get_stringio())
