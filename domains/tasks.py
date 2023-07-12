# -*- coding: utf-8 -*-
"""
@File    : tasks.py
@Time    : 2023/5/19 11:03 上午
@Author  : xxlaila
@Software: PyCharm
"""
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from domains.utils.tencentdescribedomainlist import DescribeDomainList
from domains.utils.aliyundescribedomains import AliyunDescribeDomains
from domains.utils.tencentcdndomainlist import CdnDomainList
from domains.utils.huaweicdndomainlist import HuaweiCdnDomain

@shared_task()
def get_domain_list():
    result = DescribeDomainList().wirte_database()
    if result == "ok":
        AliyunDescribeDomains().assemble_database()

# @shared_task()
# def get_aliyun_domain():
#     AliyunDescribeDomains().assemble_database()

@shared_task()
def get_tencent_cnd():
    CdnDomainList().wirte_database()

@shared_task()
def get_huawei_cdn():
    HuaweiCdnDomain().wirte_database()