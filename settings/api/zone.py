# -*- coding: utf-8 -*-
"""
@File    : zone.py
@Time    : 2023/3/9 2:11 下午
@Author  : xxlaila
@Software: PyCharm
"""

from settings.models.zone import Zone
from rest_framework import permissions
from settings.serializers.zone import ZoneSerializer
from rest_framework import viewsets
from common.page import CustomNumberPagination
from rest_framework.response import Response
from rest_framework import status
from common.responses import BaseResponse
from django.http import Http404
from rest_framework.exceptions import ValidationError
from uuid import UUID
from rest_framework.request import Request
from rest_framework.renderers import JSONRenderer
from rest_framework.exceptions import APIException

class zoneViewSet(viewsets.ModelViewSet):
    queryset = Zone.objects.all().order_by("-created_time")
    serializer_class = ZoneSerializer
    pagination_class = CustomNumberPagination # 局部使用
    renderer_classes = (JSONRenderer,)
    # permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        count = queryset.count()
        return BaseResponse(code=0, msg="success", data={"count": count, "results": serializer.data},
                            status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return BaseResponse(code=0, msg="success", data=serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return BaseResponse(code=0, msg="success", data=serializer.data)

    def create(self, request, *args, **kwargs):
        request.data["created_by"] = str(request.username.english_name)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return BaseResponse(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        ids = kwargs.get('ids', None)
        if ids:
            id_list = ids.split(',')
            # 使用列表推导式校验 id 是否合法，并转换为 UUID 对象列表
            uuid_list = [UUID(x) for x in id_list if len(x) == 36]
            if len(uuid_list) != len(id_list):
                raise ValidationError("Some ids are not valid UUID.")
            # 删除指定的 UUID 对象列表
            queryset = self.filter_queryset(self.get_queryset()).filter(id__in=uuid_list)
            deleted_count = queryset.count()
            if deleted_count != len(uuid_list):
                raise Http404("Some ids do not exist.")
            queryset.delete()
            # 返回删除成功的响应
            return BaseResponse(code=0, msg="删除成功", data="", status=status.HTTP_200_OK)
        else:
            # 删除全部
            queryset = self.filter_queryset(self.get_queryset())
            if not queryset.exists():
                raise Http404("List is empty.")
            queryset.delete()
            try:
                return BaseResponse(code=-1, msg="删除失败", data=dict(request.data), status=status.HTTP_200_OK)
            except Exception as ex:
                raise APIException(str(ex))

    def perform_batch_destroy(self, ids):
        uuid_list = [UUID(x) for x in ids]
        queryset = self.get_queryset().filter(id__in=uuid_list)
        queryset.delete()

    def perform_destroy(self, instance):
        instance.delete()

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() == 'delete' and request.GET.get('ids'):
            request = Request(request)
            ids = request.GET.get('ids')
            try:
                response = self.destroy(request, ids=ids, *args, **kwargs)
            except Http404 as ex:
                response = BaseResponse(code=-1, msg="数据不存在: %s" % str(ex), data="",
                                        status=status.HTTP_200_OK)
            except Exception as ex:
                response = BaseResponse(code=-1, msg="删除失败: %s" % str(ex), data="",
                                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return response
        else:
            return super().dispatch(request, *args, **kwargs)