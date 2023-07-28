# -*- coding: utf-8 -*-
"""
@File    : domain_audits.py
@Time    : 2023/5/25 2:28 下午
@Author  : xxlaila
@Software: PyCharm
"""
from django.db import models
import logging
import uuid
from domains.models.domain_list import CLOUD_CHOICES

__all__ = ['DomainAudit']
logger = logging.getLogger(__name__)

class DomainAudit(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(null=True, blank=True, max_length=128, verbose_name="域名")
    domainid = models.CharField(null=True, blank=True, max_length=256, verbose_name="域名标识")
    cloud = models.CharField(choices=CLOUD_CHOICES, db_index=True, max_length=32, verbose_name='云')
    secordid = models.BigIntegerField(null=True, blank=True, verbose_name="记录Id")
    source_record = models.TextField(null=True, blank=True, verbose_name="源记录")
    news_record = models.TextField(null=True, blank=True, verbose_name="新记录")
    action = models.CharField(null=True, blank=True, max_length=16, verbose_name="动作")
    created_by = models.CharField(max_length=128, blank=True, null=True, verbose_name='修改人')
    created_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_time']
        verbose_name = 'DomainAudit'
        verbose_name_plural = 'DomainAudit'


