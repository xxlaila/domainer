# -*- coding: utf-8 -*-
"""
@File    : cloud_comm.py
@Time    : 2023/2/27 12:11 下午
@Author  : xxlaila
@Software: PyCharm
"""

from django.core.cache import cache
from settings.models.cloud_secret import Cloud_Secret
from settings.models.zone import Zone
from tencentcloud.common import credential
from huaweicloudsdkcore.auth.credentials import BasicCredentials

def Tencent_Secret():
    cred = cache.get('Tencent_Credential')
    if cred is None:
        cred_result = Cloud_Secret.objects.filter(comment='腾讯云密钥')
        secretid = ''
        secretkey = ''
        for i in cred_result:
            secretid = i.secretid
            secretkey = i.secretkey
        cred = credential.Credential(secretid, secretkey)
        cache.set('Tencent_Credential', cred, 7200)
    return cred

def Tencent_zone():
    result = cache.get('Tencent_Zones')
    if result is not None:
        return result

    result = {}
    for i in Zone.objects.filter(cloud='Tencent').values_list('name', 'byname'):
        result[i[0]] = i[1]

    cache.set('Tencent_Zones', result, 7200)
    return result

def Huawei_Secret():
    credentials = cache.get('Huawei_Credentials')
    if credentials is None:
        cred_result = Cloud_Secret.objects.filter(comment='华为云密钥')
        ak = ''
        sk = ''
        for i in cred_result:
            ak = i.secretid
            sk = i.secretkey
        credentials = BasicCredentials(ak, sk)
        cache.set('Huawei_Credentials', credentials, 7200)
    return credentials

def Huawei_zone():
    result = cache.get('Huawei_Zones')
    if result is None:
        result = {}
        for i in Zone.objects.filter(cloud='Huawei'):
            result[i.name] = i.byname
        cache.set('Huawei_Zones', result, 7200)
    return result


def Aliyun_Secret():
    cred = cache.get('Aliyun_Credential')
    if cred is None:
        cred_result = Cloud_Secret.objects.filter(comment='阿里云密钥')
        secretid = ''
        secretkey = ''
        for i in cred_result:
            secretid = i.secretid
            secretkey = i.secretkey
        cred = secretid, secretkey
        cache.set('Aliyun_Credential', cred, 7200)
    return cred