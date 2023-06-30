# -*- coding: utf-8 -*-
"""
@File    : cloud_secret.py
@Time    : 2022/11/3 11:14 上午
@Author  : xxlaila
@Software: PyCharm
"""

from django.db import models
import logging
import uuid
from django.urls import reverse
from showsql.models.slow_results import CLOUD_CHOICES

__all__ = ['Cloud_Secret']
logger = logging.getLogger(__name__)

class Cloud_Secret(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(choices=CLOUD_CHOICES, default='tencent', db_index=True, max_length=32, verbose_name=('所属云'))
    secretid = models.CharField(null=True, blank=True, max_length=256, verbose_name=('SecretId'))
    secretkey = models.CharField(null=True, blank=True, max_length=256, verbose_name=('SecretKey'))
    comment = models.TextField(blank=True, verbose_name=('备注'))
    created_by = models.CharField(max_length=128, blank=True, default='', verbose_name=('创建人'))
    updated_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    created_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']
        verbose_name = 'Cloud_Secret'
        verbose_name_plural = 'Cloud_Secret'

    # def get_absolute_url(self):
    #     return reverse('')
