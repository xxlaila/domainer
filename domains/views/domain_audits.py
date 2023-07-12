# -*- coding: utf-8 -*-
"""
@File    : domain_audits.py
@Time    : 2023/6/17 5:17 下午
@Author  : xxlaila
@Software: PyCharm
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from domains.models.domain_audit import DomainAudit
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from common.page import CustomNumberPagination
from django.db.models import Q
from domains.serializers.domain_audit import DomainAuditSerializer
from rest_framework.exceptions import ValidationError

class DomainAuditAPIView(APIView):

    page = CustomNumberPagination()

    def get_filters(self):
        filters = Q()
        domain_name = self.request.query_params.get("domain_name", "").strip()
        name = self.request.query_params.get("name")
        domainid = self.request.query_params.get("domainid")
        cloud = self.request.query_params.get("cloud")
        if domain_name:
            filters &= Q(name__icontains=domain_name)
        if domainid:
            filters &= Q(domainid=domainid)
        if cloud:
            filters &= Q(cloud=cloud)
        if not domainid and not cloud:
            raise ValidationError({"code": -1, "msg": "参数不正确", "data": "domainid 或 cloud 参数不能为空"})
        return filters

    @swagger_auto_schema(
        operation_summary='新增域名解析获取部分展示数据\n',
        operation_description='有以下几种情况: \n'
                              '1、请求体：get 直接请求\n'
                              '2、{"domainid": "域名id", "cloud": "云"}\n'
                              '3、请求成功：{"data":{}, "msg":"success","status":200}\n'
                              '注：要求登录，否则返回 403',
        manual_parameters=[
            openapi.Parameter(
                name='domainid', in_=openapi.TYPE_STRING, type=openapi.TYPE_STRING,
                description='域名id'),
            openapi.Parameter(
                name='cloud', in_=openapi.TYPE_STRING, type=openapi.TYPE_STRING,
                description='云'),
        ],
        responses={
            200: openapi.Response(description="成功"),
            404: openapi.Response(description="无数据"),
        },
    )
    def get(self, request, *args, **kwargs):
        try:
            queryset = DomainAudit.objects.filter(self.get_filters()).values()
        except ValidationError as e:
            return Response(e.detail, status=200)
        ser = self.page.paginate_queryset(DomainAuditSerializer(queryset, many=True).data, request)
        count = queryset.count()
        if count == 0:
            return Response({"code": -1, "msg": "无数据", "data": "null"}, status=200)
        return Response({"code": 0, "msg": "success", "data": {"count": count, "results": ser}}, status=200)