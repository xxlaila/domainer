/*
 * @Author: yanjiao.lu@zhenai.com
 * @Date: 2023-07-20 16:47:07
 * @Last Modified by: yanjiao.lu@zhenai.com
 * @Last Modified time: 2023-07-20 16:49:23
 */
import { ref } from 'vue'
import type { CommonAPIReturn } from '@/types'
import { ElMessage } from 'element-plus'

/**
 * 提交处理方法
 * @param post: (params: D) => Promise<CommonAPIReturn<T>> 请求数据方法
 * @param callback: (data: T) => void 请求成功回调方法
 * @param msg: 操作成功后的提示文字，默认为：修改成功！
 */
export const useSubmit = <T, D = null>(options: {
  post: (param: any) => Promise<CommonAPIReturn<T>>
  callback?: (data: T, param?: D) => void
  msg?: string
  hideSuccessDialog?: boolean // 隐藏
}) => {
  const { msg, callback, post, hideSuccessDialog } = options
  const successMsg = msg ? msg : '修改成功！'
  const loading = ref(false)

  const submit = async (param?: D) => {
    loading.value = true

    try {
      const { code, data, msg: serverMsg } = await post(param)

      loading.value = false
      if (code === 0) {
        !hideSuccessDialog &&
          ElMessage({
            showClose: true,
            message: serverMsg || successMsg,
            type: 'success'
          })

        callback && callback(data, param)
      } else {
        ElMessage({
          showClose: true,
          message: serverMsg || '未知错误',
          type: 'error'
        })
      }
    } catch (error) {
      loading.value = false
    }
  }

  return {
    loading,
    submit
  }
}
