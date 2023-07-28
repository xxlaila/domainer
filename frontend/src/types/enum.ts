/** 云类型 */
export enum CLOUD_TYPE {
  Tencent = '腾讯云',
  Huawei = '华为云',
  Aliyun = '阿里云'
}

export type CLOUD_TYPE_KEY = keyof typeof CLOUD_TYPE

export type DetailType = 'add' | 'edit' | 'detail'
