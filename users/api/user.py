# -*- coding: utf-8 -*-
"""
@File    : user.py
@Time    : 2022/11/30 6:57 下午
@Author  : xxlaila
@Software: PyCharm
"""

from rest_framework import permissions
from users.serializers.user import UserSerializers
from django.contrib.auth.models import User
from rest_framework import viewsets
from common.page import CustomNumberPagination

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    pagination_class = CustomNumberPagination # 局部使用
    permission_classes = [permissions.IsAuthenticated]
