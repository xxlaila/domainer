/*
 * @Author: yanjiao.lu@zhenai.com
 * @Date: 2023-07-20 16:27:29
 * @Last Modified by: yanjiao.lu@zhenai.com
 * @Last Modified time: 2023-07-21 11:09:30
 */
import { shallowRef, ref, triggerRef, unref, watchEffect } from 'vue'
import { ElMessage } from 'element-plus'
import type { CommonAPIReturn, ListParamType } from '@/types'
import { usePagination } from './usePagination'

export const useList = <T>() => {
  const list = shallowRef<T[]>([])
  const count = ref(0)

  const setCount = (val: number) => (count.value = val)
  const setList = (val: T[]) => (list.value = val)

  return { list, count, setCount, setList }
}

/**
 * 分页列表
 * @param options
 *    @param get：Function 获取分页列表方法
 *    @param initParam: Object 初始搜索参数
 * @returns
 */
export const usePagiLists = <T, D = null>(options: {
  get: (param: ListParamType<D>) => Promise<
    CommonAPIReturn<{
      count: number
      results: T[]
    }>
  >
  initParam?: D
  callback?: (data: { count: number; results: T[] }) => void
  pageSize?: number
  pageIndex?: number
}) => {
  const { get, callback, pageSize, pageIndex } = options
  const initParam = options.initParam ? options.initParam : ({} as D)
  const loading = ref(false)
  const error = shallowRef<any>(null)
  const { page, size, setPage, setSize } = usePagination(pageIndex || 1, pageSize || 8)
  const { count, list, setCount, setList } = useList<T>()
  const params = shallowRef<D>(initParam)

  // 一般用于搜索，会将页数重置为1
  const submit = (val: D) => {
    params.value = { ...params.value, ...val }

    // 非第一页的时候重置页码为1
    if (page.value !== 1) {
      setPage(1)
    } else {
      // 强制触发更新
      triggerRef(params)
    }
  }

  // 只更新参数，不更改页数进行搜索
  const setParams = (val: D) => {
    params.value = { ...params.value, ...val }

    triggerRef(params)
  }

  const search = async () => {
    loading.value = true
    error.value = null

    try {
      const {
        code,
        data,
        msg: errorMsg
      } = await get({
        page: unref(page),
        size: unref(size),
        ...unref(params)
      })

      loading.value = false
      setCount(data.count || 0)
      setList(data.results || [])

      // 提示用户接口异常
      if (code !== 0) {
        ElMessage({
          showClose: true,
          message: errorMsg || '未知错误',
          type: 'error'
        })
      }

      callback && callback(data)
    } catch (err) {
      error.value = err
      loading.value = false
    }
  }

  watchEffect(() => search())

  return {
    page,
    size,
    count,
    list,
    setCount,
    setList,
    setPage,
    setSize,
    params,
    setParams,
    submit,
    error,
    loading,
    retry: search
  }
}
