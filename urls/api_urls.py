# -*- coding: utf-8 -*-
"""
@File    : api_urls.py
@Time    : 2023/5/19 11:44 上午
@Author  : xxlaila
@Software: PyCharm
"""
from rest_framework.routers import DefaultRouter
from domains import api
from django.urls import include, path, re_path
from domains.views.domain_record import DomainListAPIView, DomainDetailsAPIView, DomainAddRecordAPIView
from domains.views.domain_audits import DomainAuditAPIView
from domains.views.domain_export import DomainExportAPIView
from domains.views.domain_search import DomainSearchApiView

app_name = "domains"
router = DefaultRouter()
router.register(r'domain_list', api.DomainListViewSet)
router.register(r'analysis_list', api.AnalysisListViewSet)
router.register(r'domain_auth', api.DomainAuditViewSet)
router.register(r'domain_cdn', api.DomainListViewSet)

urlpatterns = [
    path("list/", DomainListAPIView.as_view(), name="domain-list"),
    path("detail/", DomainDetailsAPIView.as_view(), name="domain-detail"),
    path("record/", DomainAddRecordAPIView.as_view(), name="domain-record"),
    path("domain_audit/", DomainAuditAPIView.as_view(), name="domain-audit"),
    path("domain_export/", DomainExportAPIView.as_view(), name="domain-export"),
    path("search/", DomainSearchApiView.as_view(), name="doamin-search"),
]

urlpatterns += router.urls