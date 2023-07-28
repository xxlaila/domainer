# -*- coding: utf-8 -*-
"""
@File    : domain_search.py
@Time    : 2023/7/20 2:00 下午
@Author  : xxlaila
@Software: PyCharm
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from domains.core.domainhandle import DomainHandle

import logging
logger = logging.getLogger(__name__)

class DomainSearchApiView(APIView):

    @swagger_auto_schema(
        operation_summary='域名解析搜索\n',
        operation_description='有以下几种情况: \n'
                              '1、根据域名查询对应解析，有ecnd 返回cdn 后端ip\n'
                              '2、根据ip查询对应的域名'
                              '3、请求成功：{"data":{}, "msg":"success","status":200}\n'
                              '注：要求登录，否则返回 403',
        manual_parameters=[
            openapi.Parameter(
                name='domain_name', in_=openapi.TYPE_STRING, type=openapi.TYPE_STRING,
                description='域名')
        ],
        responses={
            200: openapi.Response(description="成功"),
            404: openapi.Response(description="无数据"),
        },
    )
    def post(self, request, *args, **kwargs):
        try:
            domain = request.data["domain"]
            result = DomainHandle(domain).select_domain()
            return Response({"code": 0, "msg": "success", "data": result}, status=200)
        except Exception as e:
            logger.error(f"域名检索错误: {e}")
            return Response({"code": -1, "msg": "error", "data": str(e)}, status=200)