import { ElMessage, ElMessageBox } from 'element-plus'
import { useSubmit } from './useSubmit'
import type { CommonAPIReturn } from '@/types'

/**
 * 批量删除
 * @param post 删除数据方法
 * @param key 页面提示文字关键词
 * @param callback 删除成功回调函数
 * @returns
 */
export const useBatchDelete = <T extends { id: string }, D = string>({
  post,
  key,
  callback
}: {
  post: (param: D) => Promise<CommonAPIReturn<T>>
  key: keyof T
  callback?: () => void
}) => {
  const selectedRows: Ref<T[]> = ref([])
  const onSelctionChange = (rows: T[]) => {
    selectedRows.value = rows
  }
  const { loading, submit } = useSubmit<T, D>({
    post: (param: D) => post(param),
    msg: '删除成功！',
    callback: () => {
      selectedRows.value = []

      callback && callback()
    }
  })

  const onItemDelete = async (title: string, id: D) => {
    if (!id) {
      return ElMessage.warning('请选择要删除的数据！')
    }

    await ElMessageBox.confirm(`确认删除：${title}`, '删除', {
      showCancelButton: false,
      confirmButtonText: '确定',
      async beforeClose(action, instance, done) {
        if (action === 'confirm') {
          instance.confirmButtonLoading = true
          instance.confirmButtonText = '删除中...'

          await submit(id)

          instance.confirmButtonLoading = false
          done()
        } else {
          done()
        }
      }
    })
  }

  const onBatchDelete = (rows: T[]) => {
    const { names, ids } = rows.reduce(
      (
        acc: {
          names: string[]
          ids: string[]
        },
        item
      ) => {
        acc.names.push(`${item[key]}`)
        acc.ids.push(item.id)

        return acc
      },
      { names: [], ids: [] }
    )

    onItemDelete(names.join(','), ids.join(',') as D)
  }

  return {
    onSelctionChange,
    loading,
    submit,
    onBatchDelete,
    selectedRows
  }
}
