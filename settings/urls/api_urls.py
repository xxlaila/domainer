# -*- coding: utf-8 -*-
"""
@File    : urls.py
@Time    : 2023/3/9 2:15 下午
@Author  : xxlaila
@Software: PyCharm
"""

from rest_framework.routers import DefaultRouter
from settings import api
from django.urls import include, path

app_name = "settings"
router = DefaultRouter()
router.register(r'cloud_secret', api.CloudSecretViewSet)
# router.register(r'rpcrypt', api.AdditiveSolutionViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

urlpatterns += router.urls