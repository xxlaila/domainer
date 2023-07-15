# -*- coding: utf-8 -*-
"""
@File    : tencentcdndomainlist.py
@Time    : 2023/6/30 12:30 下午
@Author  : xxlaila
@Software: PyCharm
"""

import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.cdn.v20180606 import cdn_client, models
from showsql.utils.cloud_comm import Tencent_Secret, Tencent_zone
from domains.models.cdndomain_list import CdnDomainsList
import logging

logger = logging.getLogger('腾讯云ecnd')

class CdnDomainList:

    def get_cnd_domain(self):
        try:
            # 实例化一个http选项，可选的，没有特殊需求可以跳过
            httpProfile = HttpProfile()
            httpProfile.endpoint = "cdn.tencentcloudapi.com"

            # 实例化一个client选项，可选的，没有特殊需求可以跳过
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            # 实例化要请求产品的client对象,clientProfile是可选的
            client = cdn_client.CdnClient(Tencent_Secret(), "", clientProfile)

            # 实例化一个请求对象,每个接口都会对应一个request对象
            req = models.DescribeDomainsRequest()
            params = {
                "Offset": 0,
                "Limit": 1000
            }
            req.from_json_string(json.dumps(params))

            # 返回的resp是一个DescribeDomainsResponse的实例，与请求对象对应
            resp = client.DescribeDomains(req)
            # 输出json格式的字符串回包
            return json.loads(resp.to_json_string())

        except TencentCloudSDKException as err:
            logger.error(f"获取ecnd 列表失败 {str(err)}")

    def wirte_database(self):
        result = self.get_cnd_domain()
        for key in result["Domains"]:
            data = {"resourceid": key["ResourceId"], "domain": key["Domain"], "cname": key["Cname"],
                    "status": key["Status"], "servicetype": key["ServiceType"], "origin": key["Origin"]["ServerName"],
                    "disable": key["Disable"], "area": key["Area"], "readonly": key["Readonly"],
                    "product": key["Product"], "parentHost": key["ParentHost"], "update_time": key["UpdateTime"],
                    "create_time": key["CreateTime"], "cloud": "Tencent", "origins": key["Origin"]["Origins"]}
            obj, create = CdnDomainsList.objects.update_or_create(
                cloud=data["cloud"], resourceid=data["resourceid"], domain=data["domain"],
                cname=data["cname"], defaults=data)
            if create == True:
                logger.info(f"{data['domain']} {data['cloud']} 新增成功")
            else:
                logger.info(f"{data['domain']} {data['cloud']}更新成功")

        return "ok"