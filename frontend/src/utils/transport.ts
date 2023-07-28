import type { CommonAPIReturn } from '@/types'
import { getOALoginUrl } from '../utils'
import axios from 'axios'
import type { AxiosRequestConfig, AxiosResponse } from 'axios'
import { ElMessage } from 'element-plus'

console.log(import.meta.env)
export const transport = axios.create({
  baseURL: import.meta.env.VITE_BASE_API,
  withCredentials: true
})

// 登录过期拦截
const interceptLogin = (response: AxiosResponse) => {
  const { code, msg } = response.data || {}

  if (code === 403) {
    ElMessage({
      type: 'error',
      duration: 2000,
      message: `${msg || '登录过期'}！即将跳转到登录页面！`
    })

    setTimeout(() => {
      window.location.href = getOALoginUrl()
    }, 2000)
  }
}

transport.interceptors.response.use(
  (res) => {
    // interceptLogin(res)

    return res
  },
  (error) => {
    const { message, response } = error || {}

    let msg = ''

    if (response) {
      // interceptLogin(response)
      msg = response.data && response.data.msg
    }

    ElMessage.error(msg || message || '未知错误')

    return Promise.reject(error)
  }
)

export const Requests = {
  request: <T, D = any>(url: string, config?: AxiosRequestConfig<D>) =>
    transport
      .request<CommonAPIReturn<T>>({
        url,
        ...config
      })
      .then((res) => res.data),
  get: <T>(url: string, config?: AxiosRequestConfig) =>
    transport.get<CommonAPIReturn<T>>(url, config).then((res) => res.data),
  post: <T, D = any>(url: string, data?: D, config?: AxiosRequestConfig) =>
    transport.post<CommonAPIReturn<T>>(url, data, config).then((res) => res.data)
}
