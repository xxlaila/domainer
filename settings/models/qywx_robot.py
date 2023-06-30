# -*- coding: utf-8 -*-
"""
@File    : qywx_robot.py
@Time    : 2023/3/9 11:38 上午
@Author  : xxlaila
@Software: PyCharm
"""

from django.db import models
import logging
import uuid

__all__ = ['QywxRobot']
logger = logging.getLogger(__name__)

class QywxRobot(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(null=True, blank=True, db_index=True, max_length=32, verbose_name=('名称'))
    byname = models.CharField(null=True, blank=True, max_length=128, verbose_name=('别名'))
    key = models.CharField(null=True, blank=True, max_length=64, verbose_name="KEY")
    created_by = models.CharField(max_length=128, blank=True, default='', verbose_name=('创建人'))
    updated_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    created_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_time']
        verbose_name = 'QywxRobot'
        verbose_name_plural = 'QywxRobot'