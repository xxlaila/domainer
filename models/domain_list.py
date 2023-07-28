# -*- coding: utf-8 -*-
"""
@File    : domain_list.py
@Time    : 2023/5/18 12:16 下午
@Author  : xxlaila
@Software: PyCharm
"""

from django.db import models
from django.db.models import F
import logging
import uuid

__all__ = ['DomainList']
logger = logging.getLogger(__name__)

CLOUD_CHOICES = (
    ("Tencent", "腾讯云"),
    ("Huawei", "华为云"),
    ("Aliyun", "阿里云")
)

SearchEnginePush_CHOICES = (
    ("Yes", "是"),
    ("No", "否"),
)

Status_CHOICES = (
    ("ENABLE", "正常"),
    ("PAUSE", "暂停"),
    ("SPAM", "封禁")
)

class DomainList(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    domainid = models.CharField(null=True, blank=True, max_length=256, verbose_name="域名标识")
    effectivedns = models.CharField(null=True, blank=True, max_length=258, verbose_name="有效DNS")
    isvip = models.CharField(null=True, blank=True, max_length=16, verbose_name="付费套餐")
    name = models.CharField(null=True, blank=True, max_length=64, verbose_name="名称")
    owner = models.CharField(null=True, blank=True, max_length=128, verbose_name="所属账号")
    punycode = models.CharField(null=True, blank=True, max_length=64, verbose_name="punycode编码")
    recordCount = models.IntegerField(null=True, blank=True, verbose_name="记录数量")
    remark = models.CharField(null=True, blank=True, max_length=64, verbose_name="备注")
    searchenginepush = models.CharField(choices=SearchEnginePush_CHOICES, null=True, blank=True,
                                        max_length=64, verbose_name="搜索引擎推送优化")
    status = models.CharField(choices=Status_CHOICES, max_length=12, null=True, blank=True, verbose_name="状态")
    createdon = models.DateTimeField(auto_now_add=True, null=True, verbose_name="添加时间")
    updatedon = models.DateTimeField(auto_now=True, null=True, verbose_name="更新时间")
    vipautorenew = models.CharField(null=True, blank=True, max_length=32, verbose_name="开通VIP自动续费")
    cloud = models.CharField(choices=CLOUD_CHOICES, db_index=True, max_length=32, verbose_name='云')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', '-name', F('recordCount').desc(nulls_last=True)]
        verbose_name = "DomainList"
        verbose_name_plural = "DomainList"