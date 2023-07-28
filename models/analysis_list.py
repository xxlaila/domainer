# -*- coding: utf-8 -*-
"""
@File    : analysis_list.py
@Time    : 2023/5/18 1:02 下午
@Author  : xxlaila
@Software: PyCharm
"""
from django.db import models
import logging
import uuid
from domains.models.domain_list import CLOUD_CHOICES

__all__ = ['AnalysisList']
logger = logging.getLogger(__name__)

MonitorStatus__CHOICES = (
    ("OK", "正常"),
    ("WARN", "告警"),
    ("DOWN", "宕机")
)

ENABLE = 1
DISABLE = 0
STATUS_CHOICES = (
    (ENABLE, "Enable"),
    (DISABLE, "Disable"),
)

class AnalysisList(models.Model):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    defaultns = models.CharField(null=True, blank=True, max_length=32, verbose_name="默认记录")
    domainid = models.CharField(null=True, blank=True, max_length=256, verbose_name="域名标识")
    line = models.CharField(null=True, blank=True, max_length=32, verbose_name="线路")
    lineid = models.CharField(null=True, blank=True, max_length=32, verbose_name="线路Id")
    mx = models.CharField(null=True, blank=True, max_length=32, verbose_name="MX值")
    monitorstatus = models.CharField(choices=MonitorStatus__CHOICES, max_length=12, verbose_name="记录监控状态")
    subdomain = models.CharField(null=True, blank=True, max_length=64, verbose_name="主机名")
    secordid = models.BigIntegerField(null=True, blank=True, verbose_name="记录Id")
    remark = models.CharField(null=True, blank=True, max_length=256, verbose_name="备注")
    # status = models.CharField(null=True, blank=True, max_length=32)
    status = models.IntegerField(choices=STATUS_CHOICES, verbose_name="记录状态")
    ttl = models.CharField(null=True, blank=True, max_length=12, verbose_name="缓存时间")
    type = models.CharField(null=True, blank=True, max_length=32, verbose_name="记录类型")
    updatedon = models.DateTimeField(auto_now=True, null=True, verbose_name="更新时间")
    value = models.CharField(null=True, blank=True, max_length=128, verbose_name="记录值")
    weight = models.CharField(null=True, blank=True, max_length=32,  verbose_name="记录权重")
    cloud = models.CharField(choices=CLOUD_CHOICES, db_index=True, max_length=32, verbose_name='云')
    domain_name = models.CharField(null=True, max_length=128, blank=True, verbose_name="域名")
    created_by = models.CharField(max_length=128, blank=True, null=True, verbose_name='创建人')
    editd_by = models.CharField(max_length=128, blank=True, null=True, verbose_name="修改人")
    demand_by = models.CharField(max_length=128, blank=True, null=True, verbose_name='需求人')
    created_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return self.subdomain

    class Meta:
        ordering = ['-updated_time']
        verbose_name = "AnalysisList"
        verbose_name_plural = "AnalysisList"
