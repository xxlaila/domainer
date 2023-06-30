# -*- coding: utf-8 -*-
"""
@File    : edncryption.py
@Time    : 2023/1/16 3:35 下午
@Author  : xxlaila
@Software: PyCharm
"""

from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
from settings.models.additive_solution import AdditiveSolution

import os
envir = os.getenv("ENV", "test")

class Prpcrypt:

    def __init__(self):
        self.key = getprivatekey().encode('utf-8')
        self.mode = AES.MODE_CBC

        # 加密函数，如果text不足16位就用空格补足为16位，
        # 如果大于16当时不是16的倍数，那就补足为16的倍数。

    def pwdencryption(self, text):
        """
        密码加密
        """
        cryptor = AES.new(self.key, self.mode, b'0000000000000000')
        # 这里密钥key 长度必须为16（AES-128）,
        # 24（AES-192）,或者32 （AES-256）Bytes 长度
        # 目前AES-128 足够目前使用
        length = 16
        count = len(text)
        if count < length:
            add = (length - count)
            # \0 backspace
            text = text + ('\0' * add)
        elif count > length:
            add = (length - (count % length))
            text = text + ('\0' * add)
        self.ciphertext = cryptor.encrypt(text.encode('utf-8'))
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext).decode(encoding='utf-8')


    def pwddecryption(self ,text):
        """
        密码解密,解密后，去掉补足的空格用strip() 去掉
        """
        cryptor = AES.new(self.key, self.mode, b'0000000000000000')
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.decode().rstrip('\0')


def getprivatekey():
    try:
        if envir == "test":
            key = AdditiveSolution.objects.get(env=envir)
        else:
            key = AdditiveSolution.objects.get(env=envir)
        return key.private_key
    except Exception as e:
        print("加密私钥为空 %s" % e)
        return False