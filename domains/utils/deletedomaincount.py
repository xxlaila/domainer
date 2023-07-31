# -*- coding: utf-8 -*-
"""
@File    : deletedomaincount.py
@Time    : 2023/7/31 4:53 下午
@Author  : xxlaila
@Software: PyCharm
"""
import logging
from domains.models.domain_list import DomainList

logger = logging.getLogger('DeleteDomainCount: ')


def delete_domain_count(data):
    try:
        counts = DomainList.objects.filter(domainid=data["domainid"]).first()
        if counts and int(counts.recordCount) > 1:
            counts.recordCount = int(counts.recordCount) - 1
            counts.save()
    except Exception as e:
        logger.error(f"同步数据库条数错误: {e}")
        return f"同步数据库条数错误: {e}"
