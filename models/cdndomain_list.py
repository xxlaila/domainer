# -*- coding: utf-8 -*-
"""
@File    : cdndomain_list.py
@Time    : 2023/6/30 12:01 下午
@Author  : xxlaila
@Software: PyCharm
"""

from django.db import models
from django.db.models import F
import logging
import uuid
from domains.models.domain_list import CLOUD_CHOICES

__all__ = ['CdnDomainsList']
logger = logging.getLogger(__name__)


READONLY_CHOICES = (
    ("normal", "未锁定"),
    ("mainland", "中国境内锁定"),
    ("overseas", "中国境外锁定"),
    ("global", "全球锁定")
)

AREA_CHOICES = (
    ("mainland", "中国境内加速"),
    ("overseas", "中国境外加速"),
    ("mainland_china", "中国大陆"),
    ("outside_mainland_china", "中国大陆境外"),
    ("global", "全球加速")
)

DISABLE_CHOICES = (
    ("normal", "正常状态"),
    ("overdue", "账号欠费导致域名关闭，充值完成后可自行启动加速服务"),
    ("malicious", "域名出现恶意行为，强制关闭加速服务"),
    ("ddos", "域名被大规模 DDoS 攻击，关闭加速服务"),
    ("idle", "域名超过 90 天内无任何操作、数据产生，判定为不活跃域名自动关闭加速服务，可自行启动加速服务"),
    ("unlicensed", "域名未备案 / 备案注销，自动关闭加速服务，备案完成后可自行启动加速服务"),
    ("capping", "触发配置的带宽阈值上限"),
    ("readonly", "域名存在特殊配置，被锁定"),
)


SERVICETYPE_CHOICES = (
    ("web", "静态加速"),
    ("download", "下载加速"),
    ("media", "流媒体点播加速"),
    ("hybrid", "动静加速"),
    ("dynamic", "动态加速"),
    ("video", "点播加速"),
    ("wholeSite", "全站加速")
)

STATUS_CHOICES = (
    ("rejected", "域名审核未通过，域名备案过期/被注销导致"),
    ("processing", "部署中"),
    ("configuring", "配置中"),
    ("configure_failed", "配置失败"),
    ("checking", "审核中"),
    ("check_failed", "审核未通过"),
    ("deleting", "删除中"),
    ("closing", "关闭中"),
    ("online", "已启动"),
    ("offline", "已关闭"),
)

class CdnDomainsList(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    resourceid = models.CharField(null=True, blank=True, max_length=64, verbose_name="域名ID")
    domain = models.CharField(null=True, blank=True, max_length=256, db_index=True, verbose_name="加速域名")
    cname = models.CharField(null=True, blank=True, max_length=512, db_index=True, verbose_name="CNAME 地址")
    status = models.CharField(choices=STATUS_CHOICES, max_length=32, verbose_name="加速服务状态")
    servicetype = models.CharField(choices=SERVICETYPE_CHOICES, max_length=32, verbose_name="业务类型")
    origin = models.TextField(null=True, blank=True, verbose_name="源站配置详情")
    origins = models.TextField(null=True, blank=True, verbose_name="回源地址")
    disable = models.CharField(choices=DISABLE_CHOICES, max_length=32, verbose_name="封禁状态")
    area = models.CharField(choices=AREA_CHOICES, max_length=32, verbose_name="加速区域")
    readonly = models.CharField(choices=READONLY_CHOICES, max_length=32, verbose_name="锁定状态")
    product = models.CharField(null=True, blank=True, max_length=16, verbose_name="所属产品")
    parentHost = models.CharField(null=True, blank=True, max_length=128, verbose_name="主域名")
    cloud = models.CharField(choices=CLOUD_CHOICES, db_index=True, max_length=32, verbose_name='云')
    create_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, null=True, verbose_name="更新时间")

    class Meta:
        ordering = ['-domain']
        verbose_name = "CdnDomainsList"
        verbose_name_plural = "CdnDomainsList"