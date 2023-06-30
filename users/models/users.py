# -*- coding: utf-8 -*-
"""
@File    : users.py
@Time    : 2022/11/8 2:08 下午
@Author  : xxlaila
@Software: PyCharm
"""

from django.db import models
import logging
import uuid

__all__ = ['Users']
logger = logging.getLogger(__name__)


class Users(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(null=True, blank=True, max_length=128, verbose_name=('中文名'))
    english_name = models.CharField(null=True, blank=True, max_length=128, verbose_name=('英文名'))
    mailbox = models.EmailField(verbose_name=('邮箱'))
    eid = models.IntegerField(null=True, blank=True, verbose_name=("工号"))
    phone = models.IntegerField(null=True, blank=True, verbose_name=('电话'))
    updated_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    created_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')
    is_active = models.IntegerField(null=True, blank=True, default=1, verbose_name=("用户状态"))
    is_authenticated = models.IntegerField(null=True, blank=True, default=1, verbose_name=("登录状态"))
    is_super = models.IntegerField(null=True, blank=True, default=0, verbose_name=("管理员"))
    is_staff = models.IntegerField(null=True, blank=True, default=0)


    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']
        verbose_name = 'Users'
        verbose_name_plural = 'Users'
