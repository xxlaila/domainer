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
    def get_status_string(status):
        return "ENABLE" if status == 1 else "DISABLE"

    def format_record(record, status):
        return f"域名: {record['domain_name']}, 域名id: {record['domainid']}, " \
               f"线路: {record['line']}, 名称: {record['subdomain']}, " \
               f"secordid: {record['secordid']}, 备注: {record['remark']}, " \
               f"状态: {status}, 类型: {record['type']}, 解析值: {record['value']}"

    source_record = ""
    news_record = ""
    if action == "add":
        source_record = ""
    elif action == "modify":
        source_record = format_record(records, get_status_string(int(records['status'])))
    else:
        result = AnalysisList.objects.filter(domainid=records["domainid"], secordid=records["secordid"],
                                             cloud=records["cloud"]).values().first()
        source_record = format_record(result, get_status_string(int(result['status'])))
    if action == "delete":
        news_record = ""
    elif action == "modify":
        result = AnalysisList.objects.filter(domainid=records["domainid"], secordid=records["secordid"],
                                             cloud=records["cloud"]).values().first()
        news_record = format_record(result, get_status_string(int(result['status'])))
    else:
        news_record = format_record(records, get_status_string(int(records['status'])))
    try:
        data = {"name": records["domain_name"], "domainid": records["domainid"], "cloud": records["cloud"],
                "secordid": records["secordid"], "source_record": source_record, "news_record": news_record,
                "action": action, "created_by": records["created_by"]}
        DomainAudit.objects.create(**data)
        logger.info(f"添加审计日志成功: {data['name']}, {data['secordid']}, {data['domainid']}")
    except Exception as e:
        logger.error(f"添加审计日志报错: {str(e)}")
        return f"添加审计日志报错: {str(e)}"
