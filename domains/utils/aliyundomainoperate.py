# -*- coding: utf-8 -*-
"""
@File    : aliyundomainoperate.py
@Time    : 2023/5/24 11:31 上午
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
from common.cloud_comm import Aliyun_Secret
import logging
from domains.models.analysis_list import AnalysisList
from domains.utils.domain_audit import record_audit_logs
from rest_framework.exceptions import ValidationError

logger = logging.getLogger('Aliyundomains')

class AliyunDomainRecord:

    def __init__(self, data):
        self.data = data
        self.access_key_id = Aliyun_Secret()[0]
        self.access_key_secret = Aliyun_Secret()[1]
        self.name = data["name"]
        self.domainid = data["domainid"]
        self.domain_name = data["domain_name"]
        self.subdomain = data["subdomain"]
        self.type = data["recordtype"]
        self.value = data["value"]
        self.remark = data["remark"]
        self.secordid = data["secordid"]
        self.line = data["recordline"]
        self.status = data["status"]
        self.created_by = data["created_by"]

    def create_client(self):
        config = open_api_models.Config(
            # 必填，您的 AccessKey ID,
            access_key_id=self.access_key_id,
            # 必填，您的 AccessKey Secret,
            access_key_secret=self.access_key_secret
        )
        config.endpoint = f'alidns.cn-shenzhen.aliyuncs.com'
        return Alidns20150109Client(config)

    # 判断域名是否唯一
    def determine_domain_unique(self):
        domain_name = f"{self.subdomain}.{self.name}"
        obj = AnalysisList.objects.filter(domain_name=domain_name).values()
        if obj:
            raise ValidationError({"code": -1, "msg": "域名存在，请勿重复添加", "data": self.data})
        else:
            res = self.add_resolution()
            return res

    # 增加域名解析
    def add_resolution(self):
        client = self.create_client()
        add_domain_record_request = alidns_20150109_models.AddDomainRecordRequest(
            domain_name=self.name,
            rr=self.subdomain,
            type=self.type,
            value=self.value,
            line="default"
        )
        runtime = util_models.RuntimeOptions()
        try:
            response = client.add_domain_record_with_options(add_domain_record_request, runtime)
            res = response.body.to_map()
            if "RecordId" in res:
                self.update_record_remark(secordid=res["RecordId"], action="add")
                try:
                    self.domain_recordinfo(res["RecordId"], action="add")
                    return res["RecordId"]
                except Exception as e:
                    return e
            else:
                return "阿里云新增域名未知的错误: {}".format(str(res))
        except Exception as error:
            # 如有需要，请打印 error
            logger.error("添阿里云添加域名解析报错: {}".format(str(error)))

    # 修改域名解析记录
    def modify_record_domain(self):
        client = self.create_client()
        update_domain_record_request = alidns_20150109_models.UpdateDomainRecordRequest(
            record_id=self.secordid,
            rr=self.subdomain,
            type=self.type,
            value=self.value,
            line="default"
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            response = client.update_domain_record_with_options(update_domain_record_request, runtime)
            res = response.body.to_map()
            if "RecordId" in res:
                self.update_record_remark(res["RecordId"])
                self.domain_recordinfo(res["RecordId"])
                return res["RecordId"]
        except Exception as error:
            # 如有需要，请打印 error
            logger.error("阿里云修改域名解析报错: {}".format(str(error)))

    # 修改域名解析备注
    def update_record_remark(self, secordid='', action=''):
        client = self.create_client()
        update_domain_record_remark_request = alidns_20150109_models.UpdateDomainRecordRemarkRequest(
            record_id=secordid,
            remark=self.remark
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            response = client.update_domain_record_remark_with_options(update_domain_record_remark_request, runtime)
            return response.body.to_map()
        except Exception as error:
            # 如有需要，请打印 error
            logger.error("阿里云修改域名备注错误: {}".format(str(error)))

    # 查询域名解析记录，同时写入数据库
    def domain_recordinfo(self, secordid, action=""):
        client = self.create_client()
        describe_domain_record_info_request = alidns_20150109_models.DescribeDomainRecordInfoRequest(
            record_id=secordid
        )
        runtime = util_models.RuntimeOptions()
        try:
            response = client.describe_domain_record_info_with_options(describe_domain_record_info_request, runtime)
            res = response.body.to_map()
            self.write_records_to_database(res, action)
            return res
        except Exception as error:
            # 如有需要，请打印 error
            logger.error("阿里云查询域名解析记录错误: {}".format(str(error)))

    def write_records_to_database(self, records, action):
        if "Priority" in records:
            mx = records["Priority"]
        else:
            mx = ""
        if "Remark" in records:
            remark = records["Remark"]
        else:
            remark = ''
        if "Weight" in records:
            weight = records["Weight"]
        else:
            weight = ""
        if records["Status"] == "ENABLE":
            status = 1
        else:
            status = 0
        domain_name = f"{self.subdomain}.{self.name}"
        data = {"defaultns": "", "domainid": self.domainid, "line": records["Line"],
                "lineid": '', "mx": mx, "monitorstatus": "",
                "subdomain": records["RR"], "secordid": records["RecordId"], "remark": remark,
                "status": status, "ttl": records["TTL"], "type": records["Type"],
                "value": records["Value"], "weight": weight, "cloud": "Aliyun",
                "domain_name": domain_name, "created_by": self.created_by, "editd_by": self.created_by,
                "demand_by": "", "updatedon": ""}
        data.update({"domainid": self.domainid})
        new_data = data
        obj, create = AnalysisList.objects.update_or_create(
            subdomain=data["subdomain"], secordid=data["secordid"], cloud=data["cloud"],
            domainid=self.domainid, defaults=data)
        if action == "add":
            record_audit_logs(new_data, action)
        if create:
            logger.info(f"{data['domain_name']} 新增成功，value={data['value']}")
        else:
            logger.info(f"{data['domain_name']} 更新成功，value={data['value']}")

    # 删除域名解析记录
    def delete_domain_record(self):
        """
        :return:
        {
          "RequestId": "33EF9135-657E-5766-9B75-5346DBE7A522",
          "RecordId": "830790258296073216"
        }
        """
        client = self.create_client()
        delete_domain_record_request = alidns_20150109_models.DeleteDomainRecordRequest(
            record_id=self.secordid
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            response = client.delete_domain_record_with_options(delete_domain_record_request, runtime)
            res = response.body.to_map()
            if "RecordId" in res:
                records = {"secordid": res["RecordId"], "cloud": "Aliyun", "domainid": self.domainid,
                           "status": self.status, "created_by": self.created_by, "type": self.type,
                           "line": self.line, "remark": self.remark, "subdomain": self.subdomain,
                           "domain_name": self.domain_name, "value": self.value}
                record_audit_logs(records, action="delete")
                AnalysisList.objects.filter(domain_name=self.domain_name, secordid=res["RecordId"]).delete()
                return res["RecordId"]
            else:
                return f"error: {res}"
        except Exception as error:
            # 如有需要，请打印 error
            logger.error("阿里云删除域名解析记录错误: {}".format(str(error)))

    # 暂停和启用域名解析记录
    def modify_record_status(self):
        """
        :return:
        {
          "Status": "Disable",
          "RequestId": "AE3D11C7-7BF0-5E35-B155-2C737157FEBB",
          "RecordId": "830790258296073216"
        }
        """
        if self.status == 1:
            status = "Enable"
        else:
            status = "Disable"
        client = self.create_client()
        set_domain_record_status_request = alidns_20150109_models.SetDomainRecordStatusRequest(
            record_id=self.secordid,
            status=status
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            response = client.set_domain_record_status_with_options(set_domain_record_status_request, runtime)
            res = response.body.to_map()
            if "RecordId" in res:
                records = {"secordid": res["RecordId"], "cloud": "Aliyun", "domainid": self.domainid,
                           "status": self.status, "created_by": self.created_by, "type": self.type,
                           "line": self.line, "remark": self.remark, "subdomain": self.subdomain,
                           "domain_name": self.domain_name, "value": self.value}
                queryset = AnalysisList.objects.filter(domain_name=self.domain_name, domainid=self.domainid,
                                                       cloud="Aliyun", secordid=res["RecordId"])
                record_audit_logs(records, action="status")
                queryset.update(status=int(self.status))
                self.domain_recordinfo(secordid=res["RecordId"], action="status")
                return res["RecordId"]
            return res
        except Exception as error:
            # 如有需要，请打印 error
            logger.error("阿里云修改域名解析记录状态错误: {}".format(str(error)))
