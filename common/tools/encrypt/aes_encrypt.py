# -*- coding: utf-8 -*-
# @Time    : 2022/7/8 18:11
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : aes_encrypt.py
# @Software: PyCharm

import base64

from Cryptodome.Cipher import AES


class AESEncrypt:

    def __init__(self, secret_key, value, fill_in):
        if len(secret_key) != 32:
            raise ValueError('secret_key 长度应为 32')
        if len(fill_in) != 1:
            raise ValueError('fill_in 长度应为 1')
        if not value:
            raise ValueError('value 不能为空')
        self.secret_key = secret_key
        self.aes = AES.new(str.encode(self.secret_key), AES.MODE_ECB)
        self.value = value
        self.fill_in = fill_in
        self.encrypt_str = ""
        self.decrypt_str = ""

    def encrypt(self):
        """加密"""

        encode_value = str.encode(self.value.rjust(16, self.fill_in))  # 加密数据不足16位向左补y符号, 并转换为bytes
        self.encrypt_str = str(
            base64.encodebytes(self.aes.encrypt(encode_value)),
            encoding='utf-8'
        )  # 使用aes加密bytes并使用base64编码bytes
        return self.encrypt_str

    def decrypt(self):
        """解密"""

        decrypt_str = (
            self.aes.decrypt(base64.decodebytes(self.encrypt_str.encode(encoding='utf-8')))
                .decode()
                .replace(self.fill_in, '')
        )
        self.decrypt_str = decrypt_str
        return self.decrypt_str


if __name__ == '__main__':
    a = AESEncrypt(secret_key="YYX6DGQKK859DN11F9GN3ZFFJGVD1YYX", value="yangyuexiong", fill_in="y")
    print(a.encrypt())
    print(a.decrypt())
