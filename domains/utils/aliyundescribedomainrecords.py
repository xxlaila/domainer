# -*- coding: utf-8 -*-
"""
@File    : aliyundescribedomainrecords.py
@Time    : 2023/5/23 3:44 下午
@Author  : xxlaila
@Software: PyCharm
"""

import sys
import math
from typing import List
from alibabacloud_alidns20150109.client import Client as Alidns20150109Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_alidns20150109 import models as alidns_20150109_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient
from common.cloud_comm import Aliyun_Secret
from domains.models.analysis_list import AnalysisList
import logging

logger = logging.getLogger('阿里云域名解析列表')

class AliyunDescribeDomainRecords:

    def __init__(self, domain_name, domainid, cloud):
        self.domain_name = domain_name
        self.domainid = domainid
        self.cloud = cloud
        self.access_key_id = Aliyun_Secret()[0]
        self.access_key_secret = Aliyun_Secret()[1]

    def create_client(self):
        config = open_api_models.Config(
            # 必填，您的 AccessKey ID,
            access_key_id=self.access_key_id,
            # 必填，您的 AccessKey Secret,
            access_key_secret=self.access_key_secret
        )
        # 访问的域名
        config.endpoint = f'alidns.cn-hangzhou.aliyuncs.com'
        return Alidns20150109Client(config)


    def get_data_list(self, page_number=1):
        client = self.create_client()
        describe_domain_records_request = alidns_20150109_models.DescribeDomainRecordsRequest(
            domain_name=self.domain_name,
            page_number=page_number,
            page_size=500
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            response = client.describe_domain_records_with_options(describe_domain_records_request, runtime)
            response_domain_dict = response.body.to_map()
            return response_domain_dict
        except Exception as error:
            # 如有需要，请打印 error
            logger.error(f"Error occurred: {error}")

    def assemble_database(self):
        try:
            result = self.get_data_list(page_number=1)
        except:
            return
        if not result:
            return
        subdomain_count = result["TotalCount"]
        records = self.parse_records(result["DomainRecords"])
        self.write_records_to_database(records)
        if subdomain_count > 500:
            total = math.ceil(subdomain_count / 500)
            for page_number in range(2, total):
                result = self.get_data_list(page_number=page_number)
                if not result:
                    return
                records = self.parse_records(result["DomainRecords"])
                self.write_records_to_database(records)

    def parse_records(self, record_list):
        records = []
        for key in record_list["Record"]:
            if "Priority" in key:
                mx = key["Priority"]
            else:
                mx = ""
            if "Remark" in key:
                remark = key["Remark"]
            else:
                remark = ''
            if "Weight" in key:
                weight = key["Weight"]
            else:
                weight = ""
            if key["Status"] == "ENABLE":
                status = 1
            else:
                status = 0
            data = {"defaultns": "", "domainid": self.domainid, "line": key["Line"], "lineid": "",
                    "mx": mx, "monitorstatus": "", "subdomain": key["RR"], "secordid": key["RecordId"],
                    "remark": remark, "status": status, "ttl": key["TTL"], "type": key["Type"],
                    "updatedon": "", "value": key["Value"], "weight": weight,
                    "cloud": self.cloud, "domain_name": f'{key["RR"]}.{key["DomainName"]}'
                    }
            records.append(data)
        return records


    def write_records_to_database(self, records):
        for data in records:
            obj, create = AnalysisList.objects.update_or_create(
               subdomain=data["subdomain"], secordid=data["secordid"],
                cloud=data["cloud"], domainid=self.domainid, defaults=data)
            if create:
                logger.info(f"{data['domain_name']} 新增成功，value={data['value']}")
            else:
                logger.info(f"{data['domain_name']} 更新成功，value={data['value']}")
