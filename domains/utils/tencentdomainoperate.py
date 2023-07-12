# -*- coding: utf-8 -*-
"""
@File    : tencentdomainoperate.py
@Time    : 2023/5/24 11:58 上午
@Author  : xxlaila
@Software: PyCharm
"""

import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.dnspod.v20210323 import dnspod_client, models
from showsql.utils.cloud_comm import Tencent_Secret, Tencent_zone
from domains.models.analysis_list import AnalysisList
import logging
from domains.utils.domain_audit import record_audit_logs
from django.db import connection
from rest_framework.exceptions import ValidationError

logger = logging.getLogger('Tencentdomains')

class TencentDomainRecord:

    def __init__(self, data):
        self.data = data
        self.name = data["name"]
        self.domain_name = data["domain_name"]
        self.domainid = data["domainid"]
        self.subdomain = data["subdomain"]
        self.recordtype = data["recordtype"]
        self.value = data["value"]
        self.status = data["status"]
        self.recordline = data["recordline"]
        self.secordid = data["secordid"]
        self.remark = data["remark"]
        self.created_by = data["created_by"]
        self.editd_by = data["editd_by"]
        self.demand_by = data["demand_by"]

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
        try:
            httpProfile = HttpProfile()
            httpProfile.endpoint = "dnspod.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = dnspod_client.DnspodClient(Tencent_Secret(), "", clientProfile)

            req = models.CreateRecordRequest()
            params = {
                "Domain": self.name,
                "DomainId": int(self.domainid),
                "SubDomain": self.subdomain,
                "RecordType": self.recordtype,
                "RecordLine": "默认",
                "Value": self.value,
                "Status": "ENABLE"
            }
            req.from_json_string(json.dumps(params))

            resp = client.CreateRecord(req)
            # 输出json格式的字符串回包
            secordid = json.loads(resp.to_json_string())["RecordId"]
            if secordid:
                self.modify_record_remark(secordid=secordid, action="add")
                # self.describe_record(secordid=secordid, action="add")
            return json.loads(resp.to_json_string())
        except TencentCloudSDKException as err:
            logger.error("腾讯云添加域名解析错误: {}".format(str(err)))

    # 修改域名解析
    def modify_record_domain(self):
        if self.status == 1:
            status = "ENABLE"
        else:
            status = "DISABLE"
        try:
            httpProfile = HttpProfile()
            httpProfile.endpoint = "dnspod.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = dnspod_client.DnspodClient(Tencent_Secret(), "", clientProfile)

            req = models.ModifyRecordRequest()
            params = {
                "Domain": self.name,
                "SubDomain": self.subdomain,
                "RecordType": self.recordtype,
                "RecordLine": "默认",
                "Value": self.value,
                "Status": status,
                "RecordId": int(self.secordid)
            }
            req.from_json_string(json.dumps(params))
            resp = client.ModifyRecord(req)
            # self.describe_record(secordid=self.secordid,  action="modify")
            self.modify_record_remark(secordid=self.secordid, action="modify")
            # 输出json格式的字符串回包
            return json.loads(resp.to_json_string())

        except TencentCloudSDKException as err:
            logger.error("腾讯云修改域名解析错误:{} ".format(str(err)))

    # 修改域名备注
    def modify_record_remark(self, secordid='', action=''):
        try:
            httpProfile = HttpProfile()
            httpProfile.endpoint = "dnspod.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = dnspod_client.DnspodClient(Tencent_Secret(), "", clientProfile)

            req = models.ModifyRecordRemarkRequest()
            params = {
                "Domain": self.subdomain + '.' + self.name,
                "DomainId": int(self.domainid),
                "RecordId": int(secordid),
                "Remark": self.remark
            }
            req.from_json_string(json.dumps(params))

            resp = client.ModifyRecordRemark(req)
            # 写入数据库
            self.describe_record(secordid=secordid, action=action)
            # 输出json格式的字符串回包
            return json.loads(resp.to_json_string())

        except TencentCloudSDKException as err:
            logger.error("腾讯云修改域名备注错误: {}".format(str(err)))

    # 查询记录
    def describe_record(self, secordid='', action=''):
        try:
            httpProfile = HttpProfile()
            httpProfile.endpoint = "dnspod.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = dnspod_client.DnspodClient(Tencent_Secret(), "", clientProfile)

            req = models.DescribeRecordRequest()
            params = {
                "Domain": self.subdomain + '.' + self.name,
                "DomainId": int(self.domainid),
                "RecordId": int(secordid)
            }
            req.from_json_string(json.dumps(params))

            resp = client.DescribeRecord(req)
            # 输出json格式的字符串回包
            result = json.loads(resp.to_json_string())
            # records = self.parse_records(result["RecordInfo"])
            self.write_records_to_database(result["RecordInfo"], action)
            return result["RecordInfo"]
        except TencentCloudSDKException as err:
            logger.error("腾讯云查询域名详情错误: {}".format(str(err)))

    def parse_records(self, record_list):
        records = []
        for key in record_list:
            defaultns = key.get("DefaultNS", "")
            domain_name = f"{self.subdomain}.{self.name}"
            data = {"defaultns": defaultns, "line": key["Line"], "lineid": key["LineId"], "mx": key["MX"],
                    "monitorstatus": key["MonitorStatus"], "name": key["Name"], "secordid": key["RecordId"],
                    "remark": key["Remark"], "status": key["Status"], "ttl": key["TTL"], "type": key["Type"],
                    "updatedon": key["UpdatedOn"], "value": key["Value"], "weight": key["Weight"],
                    "cloud": "Tencent", "domainid": self.domainid, "domain_name": domain_name}
            records.append(data)
        return records

    def write_records_to_database(self, records, action):
        domain_name = f"{self.subdomain}.{self.name}"
        data = {"defaultns": "", "domainid": records["DomainId"], "line": records["RecordLine"],
                "lineid": records["RecordLineId"], "mx": records["MX"], "monitorstatus": records["MonitorStatus"],
                "subdomain": records["SubDomain"], "secordid": records["Id"], "remark": records["Remark"],
                "status": records["Enabled"], "ttl": records["TTL"], "type": records["RecordType"],
                "value": records["Value"], "weight": records["Weight"], "cloud": "Tencent",
                "domain_name": domain_name, "created_by": self.created_by, "editd_by": self.created_by,
                "demand_by": "", "updatedon": records["UpdatedOn"]}

        data.update({"domainid": self.domainid})
        new_data = data
        obj, create = AnalysisList.objects.update_or_create(
            secordid=data["secordid"], cloud=data["cloud"], domainid=self.domainid, defaults=data)
        if action == "add":
            record_audit_logs(new_data, action)
        if create:
            logger.info(f"{data['domain_name']} 新增成功，value={data['value']}")
        else:
            logger.info(f"{data['domain_name']} 更新成功，value={data['value']}")

    # 删除对应解析数据
    def delete_domain_record(self):
        try:
            httpProfile = HttpProfile()
            httpProfile.endpoint = "dnspod.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = dnspod_client.DnspodClient(Tencent_Secret(), "", clientProfile)

            req = models.DeleteRecordRequest()
            params = {
                "Domain": self.domain_name,
                "DomainId": int(self.domainid),
                "RecordId": int(self.secordid)
            }
            req.from_json_string(json.dumps(params))
            resp = client.DeleteRecord(req)
            res = json.loads(resp.to_json_string())
            if "RequestId" in res:
                records = {"secordid": self.secordid, "cloud": "Tencent", "domainid": self.domainid,
                           "status": self.status, "created_by": self.created_by, "type": self.recordtype,
                           "line": self.recordline, "remark": self.remark, "subdomain": self.subdomain,
                           "domain_name": self.domain_name, "value": self.value}
                record_audit_logs(records, action="delete")
                AnalysisList.objects.filter(domain_name=self.domain_name, secordid=self.secordid,
                                            cloud="Tencent").delete()
                return res["RequestId"]
            else:
                return f"error: {res}"
        except TencentCloudSDKException as err:
            logger.error("腾讯云删除域名解析记录失败: {}".format(str(err)))


    # 设置解析记录状态
    def modify_record_status(self):
        """
        :param Domain: test.baidu.com
        :param DomainId: 62691180
        :param RecordId: 1474182740
        :param status:  ENABLE/DISABLE
        :return:
        {
            "RecordId": 1474182740,
            "RequestId": "6d6c85bf-6040-46c2-8bdb-9b3812cc7437"
          }
        """
        if self.status == 1:
            status = "ENABLE"
        else:
            status = "DISABLE"
        try:
            httpProfile = HttpProfile()
            httpProfile.endpoint = "dnspod.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = dnspod_client.DnspodClient(Tencent_Secret(), "", clientProfile)

            req = models.ModifyRecordStatusRequest()
            params = {
                "Domain": self.domain_name,
                "DomainId": int(self.domainid),
                "RecordId": int(self.secordid),
                "Status": status
            }
            req.from_json_string(json.dumps(params))
            resp = client.ModifyRecordStatus(req)
            # 输出json格式的字符串回包
            secordid = json.loads(resp.to_json_string())["RecordId"]
            records = {"secordid": secordid, "cloud": "Tencent", "domainid": self.domainid,
                       "status": self.status, "created_by": self.created_by, "type": self.recordtype,
                       "line": self.recordline, "remark": self.remark, "subdomain": self.subdomain,
                       "domain_name": self.domain_name, "value": self.value}
            queryset = AnalysisList.objects.filter(domain_name=self.domain_name, domainid=self.domainid,
                                                   cloud="Tencent", secordid=secordid)
            # print(connection.queries[-1])
            record_audit_logs(records, action="status")
            queryset.update(status=int(self.status))
            self.describe_record(secordid=secordid, action="status")
            return secordid

        except TencentCloudSDKException as err:
            logger.error("腾讯云设置域名记录状态错误: {}".format(str(err)))