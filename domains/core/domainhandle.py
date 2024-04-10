# -*- coding: utf-8 -*-
"""
@File    : domainhandle.py
@Time    : 2023/5/19 2:35 下午
@Author  : xxlaila
@Software: PyCharm
"""
import re, requests
from domains.models.analysis_list import AnalysisList
from domains.models.domain_list import DomainList
from domains.models.domain_list import CLOUD_CHOICES
from domains.models.cdndomain_list import CdnDomainsList, ECND_STATUS_CHOICES, AREA_CHOICES
from domains.models.analysis_list import STATUS_CHOICES

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

    def check_domain(self, domain):
        try:
            response = requests.head("http://" + domain)
            # 检查响应状态码是否在 2xx 范围内，表示请求成功
            if response.status_code >= 200 and response.status_code < 300:
                return True, "域名正常"
            else:
                return False, "域名请求失败"
        except Exception as e:
            return False, str(e)

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
            params = {
                "ip": self.name,
                "accessKey": "alibaba-inc"
            }
            response = requests.post("https://ip.taobao.com/outGetIpInfo", params=params)
            data = response.json()
            if response.status_code == 200:
                result = data.get("data")
                if result:
                    msg = f"IP: {result['ip']} \n" \
                          f"运营商: {result['isp']} \n" \
                          f"城市: {result['city']} \n" \
                          f"归属地: {result['region']} \n"
                    return msg
            else:
                return f"查询失败: {self.name}"

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
                ECND_STATUS_CHOICES_DICT = dict(ECND_STATUS_CHOICES)
                AREA_CHOICES_DICT = dict(AREA_CHOICES)
                CLOUD_CHOICES_DICT = dict(CLOUD_CHOICES)

                for cnd in cdn_records:
                    status_display = ECND_STATUS_CHOICES_DICT[cnd['status']]
                    area_display = AREA_CHOICES_DICT[cnd['area']]
                    cloud_display = CLOUD_CHOICES_DICT[cnd['cloud']]
                    cnd_ips.append(f"所属产品: {cnd['product']}, 加速区域: {area_display}, 回源地址: {cnd['origins']}, "
                                   f"加速服务状态: {status_display}, 云: {cloud_display}")
            else:
                cnd_ips.append(f"cnd 在华为云和腾讯云不存在，请联系运维配合进行检查")

        is_normal, message = self.check_domain(domain_name)
        if is_normal:
            cnd_ips.append(f"域名 {domain_name} 正常\n")
        else:
            cnd_ips.append(f"域名 {domain_name} 异常: {message}\n")

        return "\n".join(cnd_ips)