# -*- coding: utf-8 -*-
"""
@File    : tencentdescriberecordlist.py
@Time    : 2023/5/18 1:08 下午
@Author  : xxlaila
@Software: PyCharm
"""

import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.dnspod.v20210323 import dnspod_client, models
from domains.models.analysis_list import AnalysisList
from showsql.utils.cloud_comm import Tencent_Secret, Tencent_zone
import math
import logging

logger = logging.getLogger('Tencentdomains')

class DescribeRecordList:

    def __init__(self, name, domainid, cloud):
        self.name = name
        self.domainid = domainid
        self.cloud = cloud

    def log(self, message):
        print(f"[{self.cloud}][{self.name}] {message}")

    def get_data_list(self, offset=0):
        try:
            httpProfile = HttpProfile()
            httpProfile.endpoint = "dnspod.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = dnspod_client.DnspodClient(Tencent_Secret(), "", clientProfile)

            req = models.DescribeRecordListRequest()
            params = {
                "Domain": self.name,
                "DomainId": int(self.domainid),
                "Offset": int(offset),
                "Limit": 500
            }
            req.from_json_string(json.dumps(params))
            resp = client.DescribeRecordList(req)
            return json.loads(resp.to_json_string())

        except TencentCloudSDKException as err:
            logger.error("腾讯云获取域名解析列表失败: {}".format(str(err)))

    def assemble_database(self):
        result = self.get_data_list(offset=0)
        subdomain_count = result["RecordCountInfo"]["SubdomainCount"]
        records = self.parse_records(result["RecordList"])
        self.write_records_to_database(records)
        if subdomain_count > 500:
            total = math.ceil(subdomain_count / 500)
            for i in range(0, total):
                if i == 0:
                    pass
                else:
                    offset = i * 500
                    result = self.get_data_list(offset=offset)
                    records = self.parse_records(result["RecordList"])
                    self.write_records_to_database(records)


    def parse_records(self, record_list):
        records = []
        for key in record_list:
            defaultns = key.get("DefaultNS", "")
            domain_name = f"{key['Name']}.{self.name}"
            if key["Status"] == "ENABLE":
                status = 1
            else:
                status = 0
            data = {"defaultns": defaultns, "line": key["Line"], "lineid": key["LineId"], "mx": key["MX"],
                    "monitorstatus": key["MonitorStatus"], "subdomain": key["Name"], "secordid": key["RecordId"],
                    "remark": key["Remark"], "status": status, "ttl": key["TTL"], "type": key["Type"],
                    "updatedon": key["UpdatedOn"], "value": key["Value"], "weight": key["Weight"],
                    "cloud": self.cloud, "domainid": self.domainid, "domain_name": domain_name}
            records.append(data)
        return records


    def write_records_to_database(self, records):
        for data in records:
            obj, create = AnalysisList.objects.update_or_create(
                lineid=data["lineid"], subdomain=data["subdomain"], line=data["line"],
                type=data["type"], value=data["value"], domainid=self.domainid, defaults=data)

            if create:
                logger.info(f"{data['domain_name']} 新增成功，value={data['value']}")
            else:
                logger.info(f"{data['domain_name']} 更新成功，value={data['value']}")
