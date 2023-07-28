import type { CLOUD_TYPE_KEY } from './enum'

export type DomainItemType = {
  /** 全局唯一id	*/
  id: string
  /** 域名id	每个域名唯一id */
  domainid: string
  /** 有效DNS	*/
  effectivedns: string
  /** 付费套餐	*/
  isvip: string
  /** 名称	主域名 */
  name: string
  /** 所属账号	*/
  owner: string
  /** punycode编码	域名的唯一标识，当域名(name)为中文的时候，这里是英文或者是转码标识符 */
  punycode: string
  /** 记录数量	*/
  recordCount: string
  /** 备注	*/
  remark: string
  /** 搜索引擎推送优化	*/
  searchenginepush: string
  /** 状态	*/
  status: string
  /** 状态	*/
  status_label: string
  /** 添加时间	*/
  createdon: string
  /** 更新时间	*/
  updatedon: string
  /** 开通VIP自动续费	*/
  vipautorenew: string
  /** 云 */
  cloud: CLOUD_TYPE_KEY
  /** 云 */
  cloud_label: string
}

export type DomainDetailType = {
  /**	全局id */
  id: string
  /**	默认记录 */
  defaultns: string

  domainid: string
  /**	线路 */
  line: string
  /**	线路Id */
  lineid: string
  /**	MX值 */
  mx: string
  /**	记录监控状态 */
  monitorstatus: string
  /** 域名后缀 */
  name?: string
  /**	主机名	解析头 */
  subdomain: string
  /**	记录Id	解析记录唯一id，非常重要 */
  secordid: string
  /**	备注 */
  remark: string
  /**	记录状态 */
  status: string | number
  /**	记录状态 */
  status_label: string
  /**	缓存时间 */
  ttl: number
  /**	记录类型 */
  type: string
  /**	更新时间 */
  updatedon: string
  /**	记录值 */
  value: string
  /**	记录权重 */
  weight: string
  /**	云 */
  cloud: CLOUD_TYPE_KEY
  /**	完整域名 */
  domain_name: string
  /**	创建人 */
  created_by: string
  /**	修改人 */
  editd_by: string
  /**	需求人 */
  demand_by: string
  /**	创建时间 */
  created_time: string
  /**	更新时间 */
  updated_time: string
}

export type DomainAuditLogType = {
  /** id */
  id: string
  /** 域名 */
  name: string
  /** 云 */
  cloud: string
  /** 记录Id */
  secordid: string
  /** 动作 */
  action: string
  /** 创建人 */
  created_by: string
  /** 创建时间 */
  created_time: string
  /** 源记录 */
  source_record: string
  /** 新记录 */
  news_record: string
}

// 列表搜索字段
export type DomainSearchProps = {
  domain_name: string
}

// 列表详情搜索
export type DomainDetailSearchProps = Partial<DomainDetailType>

export type DomainAuditLogSearchProps = {
  domain_name?: string
  name?: string
  domainid?: string
  cloud?: string
}

// 操作类型
export type DomainActionType = 'add' | 'modify' | 'delete' | 'status'

export type DomainDetailUpdateProps = DomainDetailSearchProps & { action: DomainActionType }

export type DomainExportProps = DomainAuditLogSearchProps & { action: 'all' | 'ids'; ids: string }
