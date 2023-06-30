# -*- coding: utf-8 -*-
"""
@File    : responses.py
@Time    : 2023/3/23 5:53 下午
@Author  : xxlaila
@Software: PyCharm
"""
from django.http import JsonResponse

class BaseResponse(JsonResponse):
    def __init__(self, data, code=None, msg=None, **kwargs):
        data = {
            'code': code if code is not None else 0,
            'msg': msg if msg is not None else 'success',
            'data': data
        }
        super().__init__(data, **kwargs)

