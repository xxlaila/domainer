# -*- coding: utf-8 -*-
"""
@File    : additive_solution.py
@Time    : 2023/1/16 3:42 下午
@Author  : xxlaila
@Software: PyCharm
"""

from django.db import models
import logging
import uuid

__all__ = ['AdditiveSolution']
logger = logging.getLogger(__name__)

ENV_TYPE = (
    ("dev", "dev"),
    ("test", "test"),
    ("uat", "uat"),
    ("pre", "pre"),
    ("prod", "prod")
)

class AdditiveSolution(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    env = models.CharField(choices=ENV_TYPE, blank=True, null=True, default='', max_length=12, verbose_name=("环境"))
    private_key = models.CharField(null=True, blank=True, max_length=128, verbose_name=("私钥"))
    remark = models.CharField(null=True, blank=True, max_length=128, verbose_name=("备注"))
    created_by = models.CharField(max_length=128, blank=True, default='', verbose_name=('创建人'))
    date_updated = models.DateTimeField(auto_now=True, null=True, verbose_name=('更新时间',))
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name=('创建时间',))

