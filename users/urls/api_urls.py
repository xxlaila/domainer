# -*- coding: utf-8 -*-
"""
@File    : urls.py
@Time    : 2023/3/3 5:17 下午
@Author  : xxlaila
@Software: PyCharm
"""
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from users import api
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


app_name = "users"
router = DefaultRouter()
router.register(r'user', api.UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]

urlpatterns += router.urls