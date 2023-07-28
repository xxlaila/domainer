# -*- coding: utf-8 -*-
"""
@File    : tencentdescribedomainlist.py
@Time    : 2023/5/18 1:09 下午
@Author  : xxlaila
@Software: PyCharm
"""

import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.dnspod.v20210323 import dnspod_client, models
from domains.models.domain_list import DomainList
from common.cloud_comm import Tencent_Secret
from domains.utils.tencentdescriberecordlist import DescribeRecordList
from domains.utils.aliyundescribedomains import AliyunDescribeDomains
import logging

logger = logging.getLogger('Tencentdomains')

class DescribeDomainList:

    def get_domain_list(self):
        try:
            cred = credential.Credential("SecretId", "SecretKey")
            httpProfile = HttpProfile()
            httpProfile.endpoint = "dnspod.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = dnspod_client.DnspodClient(Tencent_Secret(), "", clientProfile)

            req = models.DescribeDomainListRequest()
            params = {
                "Type": "ALL",
                "Offset": 0,
                "Limit": 3000
            }
            req.from_json_string(json.dumps(params))

            resp = client.DescribeDomainList(req)

            return json.loads(resp.to_json_string())

        except TencentCloudSDKException as err:
            logger.error(f"腾讯云域名列表获取失败: {str(err)}")

    def wirte_database(self):
        try:
            result = self.get_domain_list()
            for key in result["DomainList"]:

                data = {"cloud": "Tencent", "name": key["Name"], "punycode": key["Punycode"],
                        "domainid": key["DomainId"]}

                defaults = {"effectivedns": key["EffectiveDNS"], "isvip": key["IsVip"], "owner": key["Owner"],
                            "recordCount": key["RecordCount"], "remark": key["Remark"], "status": key["Status"],
                            "searchenginepush": key["SearchEnginePush"], "createdon": key["CreatedOn"],
                            "updatedon": key["UpdatedOn"], "vipautorenew": key["VipAutoRenew"]}
                obj, create = DomainList.objects.update_or_create(
                    cloud=data["cloud"], name=data["name"], punycode=data["punycode"], domainid=data["domainid"],
                    defaults=defaults)
                if create:
                    logger.info(f"{data['punycode']} {data['cloud']} 新增成功")
                    DescribeRecordList(data["name"], data["domainid"], data["cloud"]).assemble_database()
                else:
                    logger.info(f"{data['punycode']} {data['cloud']}更新成功")
            return "ok"
        except Exception as e:
            logger.error(f"处理域名记录时出现异常: {e}")
            return "no"
