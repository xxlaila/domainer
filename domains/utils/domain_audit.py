# -*- coding: utf-8 -*-
"""
@File    : domain_audits.py
@Time    : 2023/5/30 3:53 下午
@Author  : xxlaila
@Software: PyCharm
"""

from domains.models.domain_audit import DomainAudit
from domains.models.analysis_list import AnalysisList
import logging

logger = logging.getLogger('audits')

def record_audit_logs(records, action):
    """
    记录日志审计
    :param records:
    :param action:
    :return:
    """
    source_record = ""
    if action == "add":
        source_record = ""
    elif action == "modify":
        if int(records['status']) == int(1):
            status = "ENABLE"
        else:
            status = "DISABLE"
        source_record = f"域名: {records['domain_name']}, 域名id: {records['domainid']}, " \
                        f"线路: {records['line']}, 名称: {records['subdomain']}, " \
                        f"secordid: {records['secordid']}, 备注: {records['remark']}, " \
                        f"状态: {status}, 类型: {records['type']}, 解析值: {records['value']}"
    else:
        result = AnalysisList.objects.filter(domainid=records["domainid"], secordid=records["secordid"],
                                             cloud=records["cloud"]).values()
        if int(result[0]['status']) == int(1):
            status = "ENABLE"
        else:
            status = "DISABLE"
        source_record = f"域名: {result[0]['domain_name']}, 域名id: {result[0]['domainid']}, " \
                        f"线路: {result[0]['line']}, 名称: {result[0]['subdomain']}, " \
                        f"secordid: {result[0]['secordid']}, 备注: {result[0]['remark']}, " \
                        f"状态: {status}, 类型: {result[0]['type']}, 解析值: {result[0]['value']}"
    news_record = ""
    if action == "delete":
        news_record = ""
    elif action == "modify":
        result = AnalysisList.objects.filter(domainid=records["domainid"], secordid=records["secordid"],
                                             cloud=records["cloud"]).values().first()
        if int(result['status']) == int(1):
            status = "ENABLE"
        else:
            status = "DISABLE"
        news_record = f"域名: {result['domain_name']}, 域名id: {result['domainid']}, " \
                        f"线路: {result['line']}, 名称: {result['subdomain']}, " \
                        f"secordid: {result['secordid']}, 备注: {result['remark']}, " \
                        f"状态: {status}, 类型: {result['type']}, 解析值: {result['value']}"
    else:
        if int(records['status']) == int(1):
            status = "ENABLE"
        else:
            status = "DISABLE"
        news_record = f"域名: {records['domain_name']}, 域名id: {records['domainid']}, 线路: {records['line']}, " \
                      f"名称: {records['subdomain']}, secordid: {records['secordid']}, 备注: {records['remark']}," \
                      f"状态: {status}, 类型: {records['type']}, 解析值: {records['value']}"
    try:
        data = {"name": records["domain_name"], "domainid": records["domainid"], "cloud": records["cloud"],
                "secordid": records["secordid"], "source_record": source_record, "news_record": news_record,
                "action": action, "created_by": records["created_by"]}
        DomainAudit.objects.create(**data)
        logger.info(f"添加审计日志成功: {data['name']}, {data['secordid']}, {data['domainid']}")
    except Exception as e:
        logger.error(f"添加审计日志报错: {str(e)}")
        return f"添加审计日志报错: {str(e)}"
