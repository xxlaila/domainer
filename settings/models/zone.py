# -*- coding: utf-8 -*-
"""
@File    : zone.py
@Time    : 2022/11/29 2:51 下午
@Author  : xxlaila
@Software: PyCharm
"""

from django.db import models
import logging
import uuid
from showsql.models.slow_results import CLOUD_CHOICES

__all__ = ['Zone']
logger = logging.getLogger(__name__)

class Zone(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(null=True, blank=True, max_length=128, verbose_name=('地区'))
    byname = models.CharField(null=True, blank=True, max_length=128, verbose_name=('别名'))
    cloud = models.CharField(choices=CLOUD_CHOICES, default='tencent', db_index=True, max_length=32, verbose_name=('所属云'))
    created_by = models.CharField(max_length=128, blank=True, default='', verbose_name=('创建人'))
    updated_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    created_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')

    def __str__(self):
        return self.byname

    class Meta:
        ordering = ['-created_time']
        verbose_name = 'Zone'
        verbose_name_plural = 'Zone'