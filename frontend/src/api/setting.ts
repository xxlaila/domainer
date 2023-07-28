import type { CloudSecretItem, ListParamType } from '@/types'
import { Requests } from '@/utils'

/**
 * 获取云密钥管理列表
 * @param params ListParamType
 */
export const getSkeySettingLists = (params: ListParamType) =>
  Requests.get<{
    count: number
    results: CloudSecretItem[]
  }>('/settings/cloud_secret/', { params })

/**
 * 删除云密钥管理列表
 * @param id string
 * @returns Promise<CommonAPIReturn<CloudSecretItem>>
 */
export const deleteSkeySetting = (ids: string) =>
  Requests.request<CloudSecretItem>('/settings/cloud_secret/', {
    method: 'delete',
    params: { ids }
  })

/**
 * 更新地区管理
 * @param id String id
 * @param params Partial<CloudSecretItem> 参数
 */
export const updateCloudSecretItemById = (id: string, params: Partial<CloudSecretItem>) =>
  Requests.request<CloudSecretItem>(`/settings/cloud_secret/${id}/`, {
    method: 'PATCH',
    data: params
  })

/**
 * 新增地区项
 * @param id String id
 * @param params Partial<CloudSecretItem> 参数
 */
export const addCloudSecretItem = (params: Partial<CloudSecretItem>) =>
  Requests.request<CloudSecretItem>(`/settings/cloud_secret/`, {
    method: 'POST',
    data: params
  })
