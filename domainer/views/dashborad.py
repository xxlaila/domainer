# -*- coding: utf-8 -*-
"""
@File    : dashborad.py
@Time    : 2023/3/7 11:10 上午
@Author  : xxlaila
@Software: PyCharm
"""
from rest_framework.views import APIView
from rest_framework.response import Response

class DashboradApiView(APIView):

    def get(self, request, *args, **kwargs):
        return Response({"code": 0, "msg": "欢迎使用域名管理平台", "data": ""}, status=200)
