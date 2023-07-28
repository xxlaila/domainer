import { Requests } from '@/utils'

/**
 * 获取云密钥管理列表
 * @param params ListParamType
 */
export const getHomeData = () => Requests.get<string>('/home')
