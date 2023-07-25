# -*- coding: utf-8 -*-
"""
@File    : healthcheck.py
@Time    : 2023/7/17 2:59 下午
@Author  : xxlaila
@Software: PyCharm
"""

from django.db import connections
from rest_framework.response import Response
from rest_framework.views import APIView

class HealthCheckAPIView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            # 检查默认数据库连接
            default_db_conn = connections['default']
            default_db_conn.cursor()

            return Response({"code": 0, "msg": "success", "data": ""}, status=200)
        except Exception as e:
            # 数据库连接错误，返回 HTTP 500 响应和错误消息
            return Response({"code": 0, "msg": f"Database connection error: {str(e)}", "data": ""}, status=200)