/*
 * @Author: cc2victoria@gmail.com
 * @Date: 2023-07-20 17:06:34
 * @Last Modified by: cc2victoria@gmail.com
 * @Last Modified time: 2023-07-24 14:38:37
 */

import type {
  DomainItemType,
  DomainSearchProps,
  DomainDetailSearchProps,
  DomainDetailType,
  DomainAuditLogType,
  DomainAuditLogSearchProps,
  DomainDetailUpdateProps,
  DomainExportProps,
  ListParamType
} from '@/types'
import { Requests, transport } from '@/utils'
/**
 * 获取所有域名
 * @param options ListParamType<DomainSearchProps>
 */
export const getDomainList = (params: ListParamType<DomainSearchProps>) =>
  Requests.get<{
    count: number
    results: DomainItemType[]
  }>('/domains/list/', { params })

/**
 * 获取域名下所有解析
 * @param options ListParamType<DomainSearchProps>
 */
export const getDomainDetailList = (params: ListParamType<DomainDetailSearchProps>) =>
  Requests.get<{
    count: number
    results: DomainDetailType[]
  }>('/domains/detail/', { params })

/**
 * 获取域名的审计日志
 * @param options ListParamType<Partial<DomainAuditLogType>
 */
export const getDomainAuditList = (params: ListParamType<DomainAuditLogSearchProps>) =>
  Requests.get<{
    count: number
    results: DomainAuditLogType[]
  }>('/domains/domain_audit/', { params })

/**
 * 更新域名信息
 * @param data DomainDetailUpdateProps
 */
export const updateDomainInfo = (data: DomainDetailUpdateProps) =>
  Requests.post<DomainDetailType>('/domains/record/', data)

/**
 * 导出域名
 * @param params DomainDetailUpdateProps
 * @return blob
 */
export const exportDomain = (params: DomainExportProps) =>
  transport.get<Blob>('/domains/domain_export/', { params, responseType: 'blob' })
