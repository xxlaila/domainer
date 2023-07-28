import type { CLOUD_TYPE_KEY } from './enum'

export interface CloudSecretItem {
  /** Id */
  id: string
  /** 所属云 */
  name: CLOUD_TYPE_KEY
  /** SecretId */
  secretid: string
  /** SecretKey */
  secretkey: string
  /** 备注 */
  comment: string
  /** 标签 */
  tags: string
  /** 创建人 */
  created_by: string
  /** 更新时间 */
  updated_time: string
  /** 创建时间 */
  created_time: string
}
