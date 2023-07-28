import type { CloudSecretItem, DetailType, DomainDetailType, PartialKeyOf } from '@/types'

export const DetailTitle: { [P in DetailType]: string } = {
  add: '新建数据',
  edit: '编辑数据',
  detail: '基本信息'
}

// 云类型
export const CLOUD_DICT = {
  Tencent: '腾讯云',
  Huawei: '华为云',
  Aliyun: '阿里云'
}

export const CloudSecretItemDetailDict: PartialKeyOf<CloudSecretItem, string>[] = [
  {
    name: '所属云',
    secretkey: 'SecretKey',
    created_by: '创建人',
    updated_time: '更新时间'
  },
  {
    tags: '标签',
    comment: '备注',
    secretid: 'SecretId',
    created_time: '创建时间'
  }
]

export const DomainDetailDict: PartialKeyOf<DomainDetailType, string>[] = [
  {
    subdomain: '主机名',
    line: '线路',
    type: '记录类型',
    domain_name: '域名',
    status_label: '状态',
    ttl: 'ttl',
    cloud: '云',
    created_by: '创建人',
    created_time: '创建时间'
  },
  {
    value: '记录值',
    mx: 'MX值',
    weight: '记录权重',
    remark: '备注',
    secordid: '记录id',
    demand_by: '需求人',
    editd_by: '修改人',
    updated_time: '更新时间'
  }
]

export const RecordTypeDict = [
  {
    key: 'A',
    desc: 'A 记录是最常用类型，将域名指向一个 IPv4 地址，如 8.8.8.8'
  },
  {
    key: 'CNAME',
    desc: '将域名指向另一个域名地址，与其保持相同解析，如 https://www.dnspod.cn'
  },
  {
    key: 'MX',
    desc: '用于邮件服务器，相关参数一般由邮件注册商提供'
  },
  {
    key: 'TXT',
    desc: '可填写附加文本信息，常用于域名验证'
  },
  {
    key: 'AAAA',
    desc: '将域名指向一个 IPv6 地址，如 ff06:0:0:0:0:0:0:c3'
  },
  {
    key: 'NS',
    desc: '域名服务器记录，可将指定域名交由其他 DNS 服务商解析管理'
  },
  {
    key: 'CAA',
    desc: '用于指定域名的证书颁发机构（CA），减少证书颁发风险'
  },
  {
    key: 'SRV',
    desc: '用于标识某台服务器使用了某个服务，常见于微软系统的目录管理。格式为「服务名字.协议类型」，如 _sip._tcp'
  },
  {
    key: 'HTTPS',
    desc: 'HTTPS 服务绑定记录，有助于提升 HTTPS 安全性及性能'
  },
  {
    key: 'SVCB',
    desc: '新型服务绑定记录类型，允许服务指向多个客户端，并关联自定义参数值'
  },
  {
    key: 'SPF',
    desc: '用于指定发送邮件的服务器，是一种高效的反垃圾邮件解决方案'
  },
  {
    key: '显性URL',
    desc: '将一个域名重定向至某个具体网页，且显示实际 URL 。仅支持 301 重定向，该记录要求双方域名均已完成备案。'
  },
  {
    key: '隐性URL',
    desc: '将一个域名重定向至某个具体网页，但隐藏实际 URL 。仅支持 301 重定向，该记录要求双方域名均已完成备案。'
  }
]

export function convertDictStr<T>(dict: T, key: string) {
  if (Object.prototype.hasOwnProperty.call(dict, key)) {
    return dict[key]
  }

  return ''
}
