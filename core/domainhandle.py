# -*- coding: utf-8 -*-
"""
@File    : domainhandle.py
@Time    : 2023/5/19 2:35 下午
@Author  : xxlaila
@Software: PyCharm
"""
import re
from domains.models.analysis_list import AnalysisList
from domains.models.domain_list import DomainList
from domains.models.domain_list import CLOUD_CHOICES
from domains.models.cdndomain_list import CdnDomainsList, STATUS_CHOICES, AREA_CHOICES

class DomainHandle:

    def __init__(self, name):
        self.name = name

    def select_domain(self):
        ip_pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        match_ip = re.match(ip_pattern, self.name)
        if match_ip:
            return self.handle_ip()
        else:
            return self.handle_domain()

    def handle_ip(self):
        result = AnalysisList.objects.filter(value=self.name).values(
            "line", "subdomain", "status", "value", "domain_name", "domainid")
        if result:
            records = list(result)
            msg = []
            for record in records:
                if record['status'] == 1:
                    msg.append(f"线路：{record['line']}，解析名称：{record['domain_name']}，状态：启用")
            if msg:
                return "\n".join(msg)
            else:
                return "未查询到该解析记录"
        else:
            return "未查询到该解析记录"

    def handle_domain(self):
        match = re.match(r"(.*\.)?([^.]+\.[^.]+)$", self.name)
        domain_name = match.group(2)
        try:
            domain_list = DomainList.objects.get(name=domain_name)
        except DomainList.DoesNotExist:
            return "域名不存在或不在腾讯云和阿里云"

        domain_id = domain_list.domainid
        subdomain = match.group(1)[:-1]
        analysis_results = AnalysisList.objects.filter(
            domainid=domain_id, subdomain=subdomain, domain_name=self.name
        ).values("line", "subdomain", "status", "value", "type")

        cnd_ips = []
        if analysis_results:
            for result in analysis_results:
                status_display = dict(STATUS_CHOICES).get(result['status'])
                msg = f"线路：{result['line']}，解析地址：{result['value']}，状态：{status_display}, 记录类型: {result['type']}"
                cnd_ips.append(msg)
        else:
            return {"code": -1, "data": f"{self.name} 解析不存在"}

        if analysis_results[0]['type'] == "CNAME":
            cdn_records = CdnDomainsList.objects.filter(domain=self.name).values(
                "origins", "product", "area", "status", "cloud")

            if cdn_records:
                STATUS_CHOICES_DICT = dict(STATUS_CHOICES)
                AREA_CHOICES_DICT = dict(AREA_CHOICES)
                CLOUD_CHOICES_DICT = dict(CLOUD_CHOICES)

                for cnd in cdn_records:
                    status_display = STATUS_CHOICES_DICT[cnd['status']]
                    area_display = AREA_CHOICES_DICT[cnd['area']]
                    cloud_display = CLOUD_CHOICES_DICT[cnd['cloud']]
                    cnd_ips.append(f"所属产品: {cnd['product']}, 加速区域: {area_display}, 回源地址: {cnd['origins']}, "
                                   f"加速服务状态: {status_display}, 云: {cloud_display}")
            else:
                cnd_ips.append(f"cnd 在华为云和腾讯云不存在，请联系运维配合进行检查")

        return "\n".join(cnd_ips)