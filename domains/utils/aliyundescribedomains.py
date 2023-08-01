# -*- coding: utf-8 -*-
"""
@File    : aliyundescribedomains.py
@Time    : 2023/5/23 11:23 上午
@Author  : xxlaila
@Software: PyCharm
"""

import sys
from typing import List
from alibabacloud_alidns20150109.client import Client as Alidns20150109Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_alidns20150109 import models as alidns_20150109_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient
import json, math
from common.cloud_comm import Aliyun_Secret
from domains.models.domain_list import DomainList
from domains.utils.aliyundescribedomainrecords import AliyunDescribeDomainRecords
import logging
from domains.models.analysis_list import AnalysisList

logger = logging.getLogger('阿里云域名列表')

class AliyunDescribeDomains:

    def __init__(self):
        self.access_key_id = Aliyun_Secret()[0]
        self.access_key_secret = Aliyun_Secret()[1]

    def create_client(self):
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            access_key_id=self.access_key_id,
            access_key_secret=self.access_key_secret,
            endpoint='alidns.cn-hangzhou.aliyuncs.com'
        )
        return Alidns20150109Client(config)

    def get_data_list(self, page_number=1):
        # 工程代码泄露可能会导致AccessKey泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html
        client = self.create_client()
        describe_domains_request = alidns_20150109_models.DescribeDomainsRequest(
            page_size=100,
            page_number=page_number
        )
        runtime = util_models.RuntimeOptions()
        try:
            response = client.describe_domains_with_options(describe_domains_request, runtime)
            # 打印 API 的返回值
            response_domain_dict = response.body.to_map()
            return response_domain_dict
        except Exception as error:
            logger.error(f"Error occurred: {error}")

    def assemble_database(self):
        try:
            result = self.get_data_list(page_number=1)
            subdomain_count = result["TotalCount"]
            self.write_records_to_database(result["Domains"])
            if subdomain_count > 100:
                total = math.ceil(subdomain_count / 100) + 1
                for page_number in range(2, total):
                    result = self.get_data_list(page_number=page_number)
                    self.write_records_to_database(result["Domains"])
        except Exception as e:
            logger.error(f"阿里云获取域名解析列表错误: {e}")
            return "no"

    def write_records_to_database(self, result):
        for domain in result["Domain"]:
            if "RegistrantEmail" in domain:
                owner = domain["RegistrantEmail"]
            else:
                owner = ""
            if "InstanceEndTime" in domain:
                updatedon = domain["InstanceEndTime"]
            else:
                updatedon = ""

            data = {"cloud": "Aliyun", "name": domain["DomainName"], "punycode": domain["PunyCode"],
                    "domainid": domain["DomainId"]}

            defaults = {"effectivedns": domain["DnsServers"]["DnsServer"], "createdon": domain["CreateTime"],
                        "owner": owner, "isvip": "", "remark": "",
                        "searchenginepush": "", "status": "", "updatedon": updatedon, "vipautorenew": "", }

            obj = DomainList.objects.filter(cloud="Tencent", name=data["name"], punycode=data["punycode"]).first()
            if obj is not None:
                pass
            else:
                obj, create = DomainList.objects.update_or_create(
                    cloud=data["cloud"], name=data["name"], punycode=data["punycode"], domainid=data["domainid"],
                    defaults=defaults)
                if create:
                    logger.info(f"{data['punycode']} {data['cloud']}新增成功")
                    AliyunDescribeDomainRecords(data["name"], data["domainid"], data["cloud"]).assemble_database()
                else:
                    logger.info(f"{data['punycode']} {data['cloud']} 更新成功")
            record_count = AnalysisList.objects.filter(cloud="Aliyun", domainid=data["domainid"]).count()
            DomainList.objects.filter(cloud="Aliyun", domainid=data["domainid"]).update(recordCount=record_count)