# -*- coding: utf-8 -*-
"""
@File    : huaweicdndomainlist.py
@Time    : 2023/6/30 5:19 下午
@Author  : xxlaila
@Software: PyCharm
"""
from domains.models.cdndomain_list import CdnDomainsList
from showsql.utils.cloud_comm import Huawei_Secret
from huaweicloudsdkcore.auth.credentials import GlobalCredentials
from huaweicloudsdkcdn.v1.region.cdn_region import CdnRegion
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkcdn.v1 import *
import logging, json
from datetime import datetime

logger = logging.getLogger('华为云ecnd: ')

class HuaweiCdnDomain:

    def get_cnd_domain(self):
        client = CdnClient.new_builder() \
            .with_credentials(Huawei_Secret()) \
            .with_region(CdnRegion.value_of("cn-north-1")) \
            .build()
        try:
            request = ListDomainsRequest()
            request.page_size = 10000
            request.page_number = 1
            request.enterprise_project_id = "all"
            response = client.list_domains(request)
            response_dict = response.to_dict()
            return response_dict
        except exceptions.ClientRequestException as e:
            logger.error("获取域名列表报错: {}".format(e.request_id, e.error_msg))

    def wirte_database(self):
        result = self.get_cnd_domain()
        for key in result["domains"]:
            source_ip = []
            if len(key["sources"]) > 1:
                for i in key["sources"]:
                    source_ip.append(i["ip_or_domain"])
            else:
                for ip_or in key["sources"]:
                    source_ip.append(ip_or["ip_or_domain"])
            source_ip = "\n".join(source_ip)
            create_dt = datetime.fromtimestamp(int(key["create_time"]) / 1000)
            update_dt = datetime.fromtimestamp(int(key["modify_time"]) / 1000)
            data = {"resourceid": key["domain_origin_host"]["domain_id"], "domain": key["domain_name"],
                    "cname": key["cname"], "status": key["domain_status"], "servicetype": key["business_type"],
                    "origin": key["domain_name"], "origins": source_ip, "disable": "",
                    "area": key["service_area"], "readonly": "",
                    "product": "", "parentHost": "", "update_time": update_dt.strftime('%Y-%m-%d %H:%M:%S'),
                    "create_time": create_dt.strftime('%Y-%m-%d %H:%M:%S'), "cloud": "Huawei", }
            obj, create = CdnDomainsList.objects.update_or_create(
                cloud=data["cloud"], resourceid=data["resourceid"], domain=data["domain"],
                cname=data["cname"], defaults=data)
            if create == True:
                logger.info("{} 新增成功".format(data['domain'], data["cloud"]))
            else:
                logger.info("{} 更新成功".format(data['domain'], data["cloud"]))

        return "ok"