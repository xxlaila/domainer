# -*- coding: utf-8 -*-
"""
@File    : domain_record.py
@Time    : 2023/5/25 12:15 下午
@Author  : xxlaila
@Software: PyCharm
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from domains.models.domain_list import DomainList
from domains.models.analysis_list import AnalysisList
from common.page import CustomNumberPagination
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from domains.serializers.domain_list import DomainListSerializer
from domains.serializers.analysis_list import AnalysisListSerializer
from domains.utils.tencentdomainoperate import TencentDomainRecord
from domains.utils.aliyundomainoperate import AliyunDomainRecord
from rest_framework.exceptions import ValidationError
import asyncio

import logging
logger = logging.getLogger(__name__)

class DomainListAPIView(APIView):

    page = CustomNumberPagination()

    def get_queryset(self):
        queryset = DomainList.objects.all()
        filters = self.get_filters()
        return queryset.filter(filters)

    def get_filters(self):
        filters = Q()
        domain_name = self.request.query_params.get("domain_name", "").strip()

        if domain_name:
            filters &= Q(punycode__icontains=domain_name)

        return filters

    @swagger_auto_schema(
        operation_summary='获取所有的域名列表\n',
        operation_description='有以下几种情况: \n'
                              '1、请求体：get 直接请求\n'
                              '{"domain_name": "域名"}\n'
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
    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            results = self.page.paginate_queryset(DomainListSerializer(queryset, many=True).data, request)
            return Response({"code": 0, "msg": "success", "data": {"count": queryset.count(), "results": results}},
                            status=200)
        except Exception as e:
            logger.error("domains 请求查无结果：{}".format(str(e)))
            return Response({"code": -1, "msg": "无筛选结果", "data": "null"}, status=200)

class DomainDetailsAPIView(APIView):

    page = CustomNumberPagination()

    def get_filters(self):
        filters = Q()
        subdomain = self.request.query_params.get("subdomain", "").strip()
        domainid = self.request.query_params.get("domainid")
        cloud = self.request.query_params.get("cloud")
        if subdomain:
            filters &= Q(subdomain=subdomain)
        if domainid:
            filters &= Q(domainid=domainid)
        if cloud:
            filters &= Q(cloud=cloud)
        if not domainid and not cloud and not subdomain:
            raise ValidationError({"code": -1, "msg": "参数不正确", "data": "domainid、cloud、subdomain参数不能为空"})
        return filters

    @swagger_auto_schema(
        operation_summary='获取指定域名的所有解析记录\n',
        operation_description='有以下几种情况: \n'
                              '1、请求体：get 直接请求\n'
                              '2、{"domainid": "域名id", "cloud": "云", "subdomain": "解析头"}\n'
                              '3、请求成功：{"data":{}, "msg":"success","status":200}\n'
                              '注：要求登录，否则返回 403',
        manual_parameters=[
            openapi.Parameter(
                name='subdomain', in_=openapi.TYPE_STRING, type=openapi.TYPE_STRING,
                description='解析头'),
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
        queryset = AnalysisList.objects.filter(self.get_filters())
        ser = self.page.paginate_queryset(queryset, request)
        serializer = AnalysisListSerializer(ser, many=True).data
        count = queryset.count()
        if count == 0:
            return Response({"code": 0, "msg": "无数据", "data": []}, status=200)

        return Response({"code": 0, "msg": "success", "data": {"count": count, "results": serializer}}, status=200)

def doamin_action(data):
    cloud_actions = {
        "Tencent": {
            "add": TencentDomainRecord(data).determine_domain_unique,
            "modify": TencentDomainRecord(data).modify_record_domain,
            "delete": TencentDomainRecord(data).delete_domain_record,
            "status": TencentDomainRecord(data).modify_record_status
        },
        "Aliyun": {
            "add": AliyunDomainRecord(data).determine_domain_unique,
            "modify": AliyunDomainRecord(data).modify_record_domain,
            "delete": AliyunDomainRecord(data).delete_domain_record,
            "status": AliyunDomainRecord(data).modify_record_status
        }
    }
    cloud = data.get("cloud")
    if cloud not in cloud_actions:
        return {"error": "Invalid cloud"}
    action = data.get("action")
    if action not in cloud_actions[cloud]:
        return {"error": "Invalid action"}
    result = cloud_actions[cloud][action]()

    return result

class DomainAddRecordAPIView(APIView):

    Record_Type = (
        ("A", "A"),
        ("CNAME", "CNAME"),
        ("MX", "MX"),
        ("TXT", "TXT"),
        ("NS", "NS"),
        ("AAAA", "AAAA"),
        ("SRV", "SRV"),
        ("CAA", "CAA"),
        ("SRV", "SRV"),
        ("HTTPS", "HTTPS"),
        ("SVCB", "SVCB"),
        ("SPF", "SPF"),
        ("显性URL", "显性URL"),
        ("隐形URL", "隐形URL")
    )

    @swagger_auto_schema(
        operation_summary='新增域名解析获取部分展示数据\n',
        operation_description='有以下几种情况: \n'
                              '1、请求体：get 直接请求\n'
                              '2、{"domainid": "域名id", "cloud": "云", "name": "解析头"}\n'
                              '3、请求成功：{"data":{}, "msg":"success","status":200}\n'
                              '注：要求登录，否则返回 403',
        manual_parameters=[
            openapi.Parameter(
                name='domainid', in_=openapi.TYPE_STRING, type=openapi.TYPE_STRING,
                description='域名id'),
            openapi.Parameter(
                name='cloud', in_=openapi.TYPE_STRING, type=openapi.TYPE_STRING,
                description='云'),
            openapi.Parameter(
                name='punycode', in_=openapi.TYPE_STRING, type=openapi.TYPE_STRING,
                description='域名'),
        ],
        responses={
            200: openapi.Response(description="成功"),
            404: openapi.Response(description="无数据"),
        },
    )
    def get(self, request, *args, **kwargs):
        domainid = request.GET.get("domainid")
        cloud = request.GET.get("cloud")
        punycode = request.GET.get("punycode")
        data = {
            "recordtype": self.Record_Type,
            "punycode": punycode,
            "cloud": cloud,
            "domainid": domainid
        }
        return Response({"code": 0, "msg": "success", "data": {"results": data}}, status=200)

    @swagger_auto_schema(
        operation_summary='增加域名解析记录\n',
        operation_description='需要以下必填参数: \n'
                              '{"name": "主域名"}\n'
                              '{"domain_name": "添加域名时为空"}\n'
                              '{"domainid": "域名id\n'
                              '{"subdomain": "主机记录"}\n'
                              '{"type": "解析类型"}\n'
                              '{"line": "默认"}\n'
                              '{"status": "状态"}\n'
                              '{"value": "解析记录"}\n'
                              '{"cloud": "云"}\n'
                              '{"remark": "备注"}\n'
                              '2、请求成功：{ "data": 返回list对象, "msg":"success","status":200}\n'
                              '注：要求登录，否则返回 403',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='主域名'),
                'domain_name': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='添加域名时为空'),
                'domainid': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='域名id'),
                'subdomain': openapi.Schema(type=openapi.TYPE_STRING, description='主机记录'),
                'recordtype': openapi.Schema(type=openapi.TYPE_STRING, description='解析类型'),
                'status': openapi.Schema(type=openapi.TYPE_STRING, description='状态'),
                'line': openapi.Schema(type=openapi.TYPE_STRING, description='默认'),
                'value': openapi.Schema(type=openapi.TYPE_STRING, description='解析记录'),
                'cloud': openapi.Schema(type=openapi.TYPE_STRING, description='云'),
                'remark': openapi.Schema(type=openapi.TYPE_STRING, description='备注'),
            }
        )
    )
    async def post(self, request, *args, **kwargs):
        data = {
            "name": request.data.get("name"),
            "domain_name": request.data.get("domain_name"),
            "domainid": request.data.get("domainid"),
            "subdomain": request.data.get("subdomain").strip(),
            "recordtype": request.data.get("type"),
            # "recordline": request.data.get("recordline", "默认"),
            "value": request.data.get("value").strip(),
            "remark": request.data.get("remark").strip(),
            "status": request.data.get("status"),
            "secordid": request.data.get("secordid") or None,
            "weight": request.data.get("weight"),
            "ttl": request.data.get("ttl"),
            "created_by": request.username.english_name,
            "editd_by": request.data.get("editd_by") or None,
            "demand_by": request.data.get("demand_by") or None,
            "cloud": request.data.get("cloud"),
            "action": request.data.get("action")
        }
        if not isinstance(data["ttl"], int):
            return Response({"code": -1, "msg": "TTL 值不是整型", "data": data}, status=200)
        if data["ttl"] < 1 or data["ttl"] > 86400:
            return Response({"code": -1, "msg": "TTL 值不能小于1或大于86400, 默认600", "data": data}, status=200)

        if data["cloud"] == "Aliyun":
            data.update({"recordline": "default"})
        elif data["cloud"] == "Tencent":
            data.update({"recordline": "默认"})
        else:
            return Response({"code": -1, "msg": "线路选择不能为空", "data": data}, status=200)
        check = DomainList.objects.filter(name=data["name"], domainid=data["domainid"], cloud=data["cloud"])
        if check:
            try:
                obj = await asyncio.to_thread(doamin_action(data))
            except ValidationError as e:
                return Response(e.detail, status=200)
            if obj:
                return Response({"code": 0, "msg": "success", "data": obj}, status=200)
            else:
                return Response({"code": -1, "msg": "error", "data": obj}, status=200)
        else:
            return Response({"code": -1, "msg": "域名和域名id不匹配", "data": data}, status=200)
