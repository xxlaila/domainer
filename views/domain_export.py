# -*- coding: utf-8 -*-
"""
@File    : domain_export.py
@Time    : 2023/7/19 10:31 上午
@Author  : xxlaila
@Software: PyCharm
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from domains.models.analysis_list import AnalysisList
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import pandas as pd
from django.http import StreamingHttpResponse
from urllib.parse import quote
from io import BytesIO
from datetime import datetime
import pytz

class DomainExportAPIView(APIView):

    @swagger_auto_schema(
        operation_summary='导出域名\n',
        operation_description='有以下操作: \n'
                              '1、导出所有: {domainid: 主域名id, cloud: 云， domain_name： 主域名， '
                              'action：动作 {all代表导出所有，ids则为空}, ids: }\n'
                              '2、导出所选: {domainid: 主域名id, cloud: 云， domain_name： 主域名， '
                              'action：动作{导出选中的记录，action 动作为空}, ids: 多个id用逗号分割}\n'
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
                name='domain_name', in_=openapi.TYPE_STRING, type=openapi.TYPE_STRING,
                description='域名'),
            openapi.Parameter(
                name='action', in_=openapi.TYPE_STRING, type=openapi.TYPE_STRING,
                description='动作'),
            openapi.Parameter(
                name='ids', in_=openapi.TYPE_STRING, type=openapi.TYPE_STRING,
                description='选中记录'),
        ],
        responses={
            200: openapi.Response(description="成功"),
            404: openapi.Response(description="无数据"),
        },
    )
    def get(self, request, *args, **kwargs):
        domainid = request.GET.get("domainid")
        cloud = request.GET.get("cloud")
        domain_name = request.GET.get("domain_name")
        action = request.GET.get("action")
        ids = request.GET.get("ids")

        # 将传递的ids参数拆分为ID列表
        id_list = ids.split(",")

        if action == "all":
            queryset = AnalysisList.objects.filter(domainid=domainid, cloud=cloud)
        else:
            queryset = AnalysisList.objects.filter(id__in=id_list)

        # Create a DataFrame from the queryset
        data = list(queryset.values())
        df = pd.DataFrame(data)

        # Convert timezone-aware datetime columns to timezone-naive datetimes
        for col in df.columns:
            if isinstance(df[col].iloc[0], datetime) and df[col].iloc[0].tzinfo is not None:
                df[col] = df[col].apply(lambda dt: dt.astimezone(pytz.UTC).replace(tzinfo=None))

        # Rename columns to match verbose_name or custom names if needed
        # For example:
        # df.rename(columns={"defaultns": "Default NS"}, inplace=True)

        # Create a response with a streaming iterator
        response = StreamingHttpResponse(self.df_to_excel_iterator(df), content_type='application/vnd.ms-excel')
        file_name = quote(f"{domain_name}_域名列表.xlsx")
        response['Content-Disposition'] = f"attachment; filename={file_name}"
        return response

    def df_to_excel_iterator(self, dataframe):
        # Convert DataFrame to Excel bytes
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='openpyxl')
        dataframe.to_excel(writer, index=False)
        writer.close()  # Close the writer after writing
        output.seek(0)

        # Yield bytes from the output buffer as the file is being written
        while True:
            data = output.read(4096)
            if not data:
                break
            yield data

